import sys
from typing import *
from Parser import parse
from DepGraph import DepGraph, DepGraphNode
from Visualizer import visualize
from Instruction import Instruction
from Heuristics import longestLatencyWeightedPath, highestLatencyInstruction, getLatency

class SchedulerNode:
    def __init__(self, node: DepGraphNode):
        self.node = node
        self.cyclesLeft = getLatency(node.instruction)
    
    def isFinished(self) -> bool:
        return self.cyclesLeft == 0

    def decrementCyclesLeft(self):
        self.cyclesLeft = self.cyclesLeft - 1

def schedule(graph: DepGraph) -> List[Instruction]:
    instructions = []
    
    finished = False
    max_iters = 25

    active_set: List[SchedulerNode] = [] 
    ready_set: List[SchedulerNode] = [SchedulerNode(x) for x in graph.getLeaves()]

    all_visited_ids: List[int] = [x.instruction.id for x in graph.getLeaves()]
    all_finished_ids: List[int] = []

    while not finished:
        # 1. decrease cycles left for all scheduled nodes
        for active_ixn in active_set:
            active_ixn.decrementCyclesLeft()

        # 2. removed finished nodes
        finished_nodes: List[SchedulerNode] = []
        for active_ixn in active_set:
            if active_ixn.isFinished():
                finished_nodes.append(active_ixn)
                active_set = [x for x in active_set if not x.isFinished()]

        print("\t FINISHED_NODES:")
        print(finished_nodes)

        # Add id's of finished instructions to list
        for node in finished_nodes:
            all_finished_ids.append(node.node.id)
        all_finished_ids = list(set(all_finished_ids))

        # 3. Add dependents of finished nodes
        for node in finished_nodes:
            for dep in graph.getDependents(node.node):
                all_parents_finished = True
                parents = graph.getDependentParents(dep)
                for parent in parents:
                    if parent.id not in all_finished_ids:
                        all_parents_finished = False

                # only add deps that are new and if all incoming deps nodes are finished
                if dep.instruction.id not in all_visited_ids and all_parents_finished:
                    all_visited_ids.append(dep.instruction.id)
                    ready_set.append(SchedulerNode(dep))

        print("\t READY SET:")
        for node in ready_set:
            print(f"{node.node.instruction} -- Cycles left: {node.cyclesLeft}")

        # 4. Use node weight to schedule one of the nodes in the ready set
        candidate: SchedulerNode = None
        for node in ready_set:
            if candidate == None:
                candidate = node
            elif node.node.weight > candidate.node.weight:
                candidate = node
        
        # 5. Remove candidate from ready set, and add it to active set, and add it to instructions
        if candidate:
            ready_set = [x for x in ready_set if x.node.id != candidate.node.id]
            active_set.append(candidate)
            instructions.append(candidate.node.instruction)
        else:
            print("\t no candidate, moving on...")

        print("\t ACTIVE SET:")
        for node in active_set:
            print(f"{node.node.instruction} -- Cycles left: {node.cyclesLeft}")
        
        max_iters -= 1
        finished = max_iters == 0

    return instructions

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
        graph = longestLatencyWeightedPath(graph)
    elif sys.argv[1] == "-b":
        print("HEURISTIC: Highest Latency Instruction", file = sys.stderr)
        graph = highestLatencyInstruction(graph)
    elif sys.argv[1] == "-c":
        print("HEURISTIC: tbd", file = sys.stderr)
        exit(1)
    else:
        print("INVALID HEURISTIC: Use of command:\n schedule -a/-b/-c < ILOC file\n")
        exit(1)
        
    graph.printDebug()
    # Visualize graph
    #visualize(graph)

    # Perform scheduling algorithm
    final_instructions = schedule(graph)
    print("----------- FINAL INSTRUCTIONS -----------");
    for ixn in final_instructions:
        print(ixn.iloc_str())

