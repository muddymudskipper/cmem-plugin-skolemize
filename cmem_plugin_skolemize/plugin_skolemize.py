import validators
from uuid import uuid4
from rdflib import Graph
from os import remove
from cmem.cmempy.dp.proxy.graph import get, post
from cmem_plugin_base.dataintegration.description import Plugin, PluginParameter
from cmem_plugin_base.dataintegration.types import StringParameterType
from cmem_plugin_base.dataintegration.plugins import WorkflowPlugin
from cmem_plugin_base.dataintegration.entity import (
    Entities, Entity, EntitySchema, EntityPath,
)


@Plugin(
    label="Skolemize graph",
    plugin_id="skolemize",
    description="Skolemizes graph",
    documentation="""TBD""",
    parameters=[
        PluginParameter(
            param_type = StringParameterType(),
            name="input_graph_iri",
            label="Input graph IRI",
            description="Input graph IRI"
        ),
        PluginParameter(
            param_type=StringParameterType(),
            name="output_graph_iri",
            label="Output graph IRI",
            description="Output graph IRI"
        )
    ]
)


class SkolemizeGraph(WorkflowPlugin):

    def __init__(
        self,
        input_graph_iri,
        output_graph_iri
    ) -> None:
        if not validators.url(input_graph_iri):
            raise ValueError("Input graph IRI parameter is invalid.")
        if not validators.url(output_graph_iri):
            raise ValueError("Output graph IRI parameter is invalid.")
        self.input_graph_iri = input_graph_iri
        self.output_graph_iri = output_graph_iri


    def get_graph(self, i):
        g = Graph()
        g.parse(data=get(i).text, format="nt")
        return g

    def post_graph(self, skolemized_graph):
        temp_file = f"{uuid4()}.ttl"
        skolemized_graph.serialize(temp_file, format="ttl")
        post(self.output_graph_iri, temp_file, replace=True)
        remove(temp_file)

    def skolemize(self, input_graph, output_graph):
        output_graph = input_graph.skolemize(basepath=self.input_graph_iri)
        return output_graph

    def execute(self, inputs=()):
        self.log.info(f"Loading input graph <{self.input_graph_iri}>.")
        input_graph = self.get_graph(self.input_graph_iri)
        self.log.info(f"Loading input graph <{self.output_graph_iri}>.")
        output_graph = self.get_graph(self.output_graph_iri)
        skolemized_graph = self.skolemize(input_graph, output_graph)
        self.log.info("Posting skolemized graph.")
        self.post_graph(skolemized_graph)


