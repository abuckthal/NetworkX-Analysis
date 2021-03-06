import ghhops_server as hs
import rhino3dm as r
from flask import Flask
import pylab

import networkx as nx
import matplotlib as plt
app = Flask(__name__)
hops = hs.Hops(app)

# at the end of drawing a networkx graph, add pylab.show()

import logging
logging.getLogger("matplotlib").setLevel(logging.WARNING)
logging.getLogger("networkx").setLevel(logging.WARNING)
logging.getLogger("ghhops_server").setLevel(logging.WARNING)


G = nx.Graph()

# turns one rhino point3d into a tuple of coordinates (x, y, z)
def coordify(pt):
    if type(pt) == r.Point3d:
        return (pt.X, pt.Y, pt.Z)
    else:
        print("not a point")

# turns one tuple of coordinates (x, y, z) into a rhino point3d
def uncoordify(pt):
    if type(pt) == tuple:
        return r.Point3d(pt[0], pt[1], pt[2])
    else:
        print("not coordinates")


# finds endpoints (in coordinates) of a rhino3d line
def find_endpoints(input_line):
    if type(input_line == r.Line):
        return (coordify(input_line.PointAt(0)), coordify(input_line.PointAt(1)))


@hops.component(
    "/shortest_path",
    name="Shortest Path",
    description="Calculate the path with fewest nodes between two endpoints",
    inputs=[
        hs.HopsLine("Edges", "E", "Import all edges in the graph", hs.HopsParamAccess.LIST),
        hs.HopsPoint("Start", "S", "Select a starting node"),
        hs.HopsPoint("End", "T", "Select an end point")
    ],

    outputs = [

        hs.HopsCurve("Edges", "E", "Edges", hs.HopsParamAccess.LIST)
    ]
)

def r_shortest_path(edges, start: r.Point3d, end: r.Point3d):
    for count, value in enumerate(map(find_endpoints, edges)):
        G.add_edge(value[0], value[1], weight=edges[count].Length)
    shortest_path_nodes =  nx.shortest_path(G,source=coordify(start), target=coordify(end), weight="weight")
    #print(shortest_path_nodes)
    # print(map(uncoordify, shortest_path_nodes))
    return r.PolylineCurve(r.Point3dList(list(map(uncoordify, shortest_path_nodes))))

if __name__ == "__main__":
   app.run()
