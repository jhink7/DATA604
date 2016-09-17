from igraph import *

# import graph data from file.  'karate.GraphML' can be found at
# http://nexus.igraph.org/api/dataset?id=1&format=GraphML
karate = Graph.Read_GraphML("karate.GraphML")

# Calculate some metrics, including diameter (required by assignment)
diameter = Graph.diameter(karate)
radius = Graph.radius(karate)
ec = Graph.eccentricity(karate)

print 'Diameter: ' + str(diameter) + ', Radius: ' + str(radius) + ', Eccentricity: ' + str(ec)

# Visualize using iGraph's built in tools
layout = karate.layout("kk")
plot(karate, layout=layout, vertex_label=karate.vs["name"], main = "Zachary's karate club network" )