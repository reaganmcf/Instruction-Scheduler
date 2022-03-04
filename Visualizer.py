import networkx as nx
import matplotlib.pyplot as plt
from DepGraph import DepGraph, DepGraphNode
  
# Defining a Class
class GraphVisualization:
    def __init__(self):
        # visual is a list which stores all 
        # the set of edges that constitutes a
        # graph
        self.visual = []
          
    # addEdge function inputs the vertices of an
    # edge and appends it to the visual list
    def addEdge(self, a, b):
        temp = [a, b]
        self.visual.append(temp)
          
    # In visualize function G is an object of
    # class Graph given by networkx G.add_edges_from(visual)
    # creates a graph with a given list
    # nx.draw_networkx(G) - plots the graph
    # plt.show() - displays the graph
    def visualize(self):
        G = nx.Graph()
        G.add_edges_from(self.visual)
        nx.draw_networkx(G)
        plt.show()
  
def visualize(graph: DepGraph):
    G = GraphVisualization()

    leaves = graph.getLeaves()
    for node in leaves:
        visualize_helper(G, graph, node)
        
    G.visualize()

def visualize_helper(G, depgraph: DepGraph, node: DepGraphNode):
    for dest in node.trueDeps:
        G.addEdge(node.id, dest.id)
    for dest in node.antiDeps:
        G.addEdge(node.id, dest.id)

    for dep in depgraph.getDependents(node):
        visualize_helper(G, depgraph, dep)
