import osmnx as ox
import matplotlib.pyplot as plt
import os


place_name = "Gushan District, Kaohsiung, Taiwan"
graph = ox.graph_from_place(place_name)
fig,ax = ox.plot_graph(graph)

area = ox.gdf_from_place(place_name)
area.plot()

buildings = ox.buildings_from_place(place_name)

nodes,edges = ox.graph_to_gdfs(graph)

cycle_roads = edges.loc[edges['highway']=='cycleway',:]
fig, ax = plt.subplots()
area.plot(ax=ax,facecolor='black')
cycle_roads.plot(ax=ax,linewidth=1,edgecolor="#BC8F8F")
buildings.plot(ax=ax,facecolor = 'Khaki',alpha=0.7)

area.plot(ax=ax,facecolor="black")

print("finished")