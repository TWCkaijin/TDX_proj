import osmnx as ox
import matplotlib.pyplot as plt
import os

ox.settings.all_oneway = True
ox.settings.log_console = True
place_name = "Gushan District, Kaohsiung, Taiwan"
graph = ox.graph_from_place(place_name)
#fig,ax = ox.plot_graph(graph)
'''

G = ox.graph_from_place(place_name, network_type="drive")


ox.save_graph_xml()(G, filepath="./data/piedmont.osm")
ox.load_graphml("./data/piedmont.osm")
'''


area = ox.graph_from_place(place_name)
ox.plot_graph(area)

buildings = ox.buildings_from_place(place_name)

nodes,edges = ox.graph_to_gdfs(graph)

cycle_roads = edges.loc[edges['highway']=='cycleway',:]
fig, ax = plt.subplots()
area.plot(ax=ax,facecolor='black')
cycle_roads.plot(ax=ax,linewidth=1,edgecolor="#BC8F8F")
buildings.plot(ax=ax,facecolor = 'Khaki',alpha=0.7)

area.plot(ax=ax,facecolor="black")

# print("finished")