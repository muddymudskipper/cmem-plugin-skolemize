"""Plugin tests."""
from cmem_plugin_skolemize.plugin_skolemize import SkolemizeGraph


def test_execution():
    """Test plugin execution"""
    #entities = 100
    #values = 10

    plugin = SkolemizeGraph(input_graph_iri="https://example.org", output_graph_iri="https://example.org")
    #result = plugin.execute()
    #for item in result.entities:
    #    assert len(item.values) == len(result.schema.paths)

