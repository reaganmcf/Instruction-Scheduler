import sys
from Parser import parse
from DepGraph import DepGraph
from Visualizer import visualize
from Heuristics import longestLatencyWeightedPath, highestLatencyInstruction

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Use of command:\n  python3 Scheduler.py -a/b/c < ILOC file\n")
        exit(1)

    # parse instructions
    instructions = parse()

    # build graph
    graph = DepGraph(instructions)

    if sys.argv[1] == "-a":
        print("HEURISTIC: Longest Latency Weighted Path", file = sys.stderr)
    elif sys.argv[1] == "-b":
        print("HEURISTIC: Highest Latency Instruction", file = sys.stderr)
    elif sys.argv[1] == "-c":
        print("HEURISTIC: tbd", file = sys.stderr)
        exit(1)
    else:
        print("INVALID HEURISTIC: Use of command:\n schedule -a/-b/-c < ILOC file\n")
        exit(1)

    # Visualize graph
    visualize(graph)
