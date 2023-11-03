import osmnx as ox
import networkx as nx
from shapely.geometry import LineString
from networkx.readwrite.graphml import GraphMLWriter


ox.settings.all_oneway = True
ox.settings.log_console = True
# Step 1: Download street network data using OSMnx
place_name = "Gushan District, Kaohsiung, Taiwan"
graph = ox.graph_from_place(place_name, network_type="all")

# Step 2: Perform any analysis or data retrieval you need
# For example, let's say you want to add a 'population' attribute to each node.
# You can create a dictionary of node ID to population value.
your_population_data = { '7843459363': 15,'7843459364':22,'7843459368':78}
population_data = {
    node_id: population_value for node_id, population_value in your_population_data.items()
}

# Step 3: Modify the attributes of nodes or add new attributes
for node in graph.nodes(data=True):
    print(node)
    '''
    node_id = node[0]
    if node_id in population_data:
        node[1]['population'] = population_data[node_id]
    '''
# Step 4: Save the modified graph if needed
# You can save the graph with the added attributes using OSMnx or NetworkX functions.
# For example, to save as a shapefile:




for node in graph.nodes(data=True):
    if 'geometry' in node[1] and isinstance(node[1]['geometry'], LineString):
        node[1]['geometry'] = LineString(node[1]['geometry']).wkt

# Step 4: Save the modified graph as a GraphML file
# Use GraphMLWriter to handle custom node attributes
writer = GraphMLWriter()
nx.write_graphml(graph,'000.graphml')

