from DepGraph import DepGraph, DepGraphNode
from Instruction import Instruction, OpCode

# Heuristic 1:
# Longest Latency Weighted Path
def longestLatencyWeightedPath(g: DepGraph) -> DepGraph:
    for node in g.getLeaves():
        llwp_helper(g, node)
    return g

def llwp_helper(g: DepGraph, node: DepGraphNode) -> DepGraphNode:
    ixnWeight = getLatency(node.instruction)
    if len(g.getDependents(node)) == 0:
        node.weight = ixnWeight
    else:
        maxDependentWeight = 0
        for dep in g.getDependents(node):
            llwp_helper(g, dep)
            maxDependentWeight = max(maxDependentWeight, dep.weight)
        
        node.weight = maxDependentWeight + ixnWeight

    return node

# Heuristic 2:
# Highest Latency Instruction
def highestLatencyInstruction(g: DepGraph) -> DepGraph:
    for n in g.nodes.values():
        n.weight = getLatency(n.instruction)

    return g

# Heuristic 3:
# TBD
def heuristic3(g: DepGraph) -> DepGraph:

    return g

def getLatency(instruction: Instruction) -> int:
    op = instruction.opcode

    if op == OpCode.ADD or op == OpCode.SUB:
        return 1
    elif op == OpCode.MUL or op == OpCode.DIV:
        return 3
    elif op == OpCode.LOADI or op == OpCode.OUTPUTAI:
        return 1
    else:
        return 5
