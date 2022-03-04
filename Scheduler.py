from Parser import parse
from DepGraph import DepGraph
from Visualizer import visualize

if __name__ == '__main__':
    
    instructions = parse()

    #for ixn in instructions:
    #    print(ixn)

    # build graph
    graph = DepGraph(instructions)
    graph.printDebug()
    visualize(graph)
    #graph.printDebug()


