# Project 1 Report

## Implementation Details

I initially started this project in C, and made it a long way. However, I found that after taking a few days off that I wasn't able to fully follow the code I wrote before. This resulted in `Segmentation Fault` appearing in various places, which is incredibly frustrating. As a result, I scrapped my C implementation, and restarted the project in Python. This ended up being a fantastic decision, as safely dealing with graph creation / traversal is tremendously easier in Python.

My implementation, like most, can be split up into 4 main parts that I will touch on.

I decided to keep the same data structure that is used in the sample project for storing my instructions in code, hence why I do not discuss it here.

### Parsing

Before we can even think about optimizing, we have to write a parser to read in the instructions. I made sure to allow the program to read in ILOC code through `stdin` or from an input file. The code for this is inside `Parser.py`. The parsing is fairly trivial, and is almost identical to the C implementation provided by the professor.

### DepGraph

Now that we have parsed the instructions, we need to build a dependency graph. I decided to create a `DepGraph` data structure, which represents a graph of `DepGraphNode` objects. The structure for this is defined as:

```py
class DepGraphNode:
  def __init__(self, instruction: Instruction):
      self.id = instruction.id
      self.instruction = instruction
      self.trueDeps = []
      self.antiDeps = []
      self.ioDeps = []
      self.weight = 0

  ...

class DepGraph:
  def __init__(self, instructions: List[Instruction]):
    self.nodes = {}
    self.instructions = instructions

  ...
```

We store _all_ nodes in the graph by the ID of the instruction, which correlates with the line in the source file it occurs on. This means we can look up any node by this ID, allowing the node edges to make sure they are pointing to the same node, and ensuring we don't accidentally have duplicate nodes all over the graph.

#### Building the DepGraph

Inside of the constructor for the DepGraph object, we iterate over the list of all instructions (top-down), and find the following dependencies for each
  - `findTrueDeps()` which finds the TRUE register AND memory dependencies for a given instruction
  - `findAntiDeps()` which finds the ANTI register AND memory dependencies for a given instruction
  - `findIODeps()`, which is only relevant for `outputAI` instructions, insuring they never get re-ordered (ensuring consistency of the program)

We assign all of these dependencies to the `trueDeps`, `antiDeps`, and `ioDeps` fields for the node.

Note that there are various helper functions defined inside `DepGraph` in order to make it easier to use, such as `getPreviousInstructions`, `getLeaves`, `getDependentParents`, `getDependents`, etc. (which are all self-explanatory by their function definition).

### Heuristics

Now that we have built the dependency graph, we need to figure out which heuristic we want to use. The way I have built my `DepGraphNode` data structure, we just need to assign a value to the `weight` field.

 > Note: no matter which heuristic we use, the `loadAI 1024 => r0` instruction gets an incredibly high weight to ENSURE that it gets scheduled first. This is because it's a special instruction, as discussed in class.

Also, every time I mention "an instruction's latency", I am using the following code snippet to assign latencies, as mentioned in the project description.

```py
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
```

#### Heuristic 1: Longest Latency Weighted Path

This heuristic assigns the weight for a node as the instruction's latency + the most path that depends on the instruction. The code for this is given below, and we use a helper method since my implementation is recursive.

```py
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

    # loadI 1024 => r0 is always special
    if node.instruction.id == 0 and node.instruction.opcode == OpCode.LOADI:
        node.weight = 999
        return node

    return node
```

#### Heuristic 2: Highest Latency Instruction

This heuristic is much simpler than the one above, as we just assign the weight for each node to the latency of the instruction. This means that each node with the highest latency will get scheduled first during our scheduling algorithm (which we discuss in the next section)

```py
def highestLatencyInstruction(g: DepGraph) -> DepGraph:
    for node in g.nodes.values():
        if node.instruction.id == 0 and node.instruction.opcode == OpCode.LOADI:
            node.weight = 999
        else:
            node.weight = getLatency(node.instruction)
```

#### Heuristic 3: Custom Heuristic (Random!)

Heuristic 3 was left for us to come up with an implementation ourselves. 

When I took Operating Systems a year ago, one thing that always came up was that when you have a problem that requires a heuristic, especially process scheduling, **random isn't really that bad!**. An example is a lottery scheduler for OS Kernels - which are usually _pretty good_. And, they are obviously trivial to implement. So, I decided to give this one a shot in this project to see how it performs.

The implementation is super simple, minus the bias for the special `loadI1024 => r0` instruction.

```py
def randomWeights(g: DepGraph) -> DepGraph:
    for node in g.nodes.values():
        if node.instruction.id == 0 and node.instruction.opcode == OpCode.LOADI:
            node.weight = 999
        else:
            node.weight = randint(1, 5)
    return g
```

### Scheduling

Now that we have everything set up (parsing, building the graph, assigning weights), we need to actually schedule it all and optimize the code. I knew that I was going to need a data structure to wrap my `DepGraphNode` in order to track the status of a scheduled instruction with greater consistency:

```py
class SchedulerNode:
    def __init__(self, node: DepGraphNode):
        self.node = node
        self.cyclesLeft = getLatency(node.instruction)
    
    def isFinished(self) -> bool:
        return self.cyclesLeft == 0

    def decrementCyclesLeft(self):
        self.cyclesLeft = self.cyclesLeft - 1
```

This allows me to have an idiomatic API for dealing with scheduled instructions.

The code can be found inside `Scheduler.py`, and I'll describe in a high level fashion how it works.

Before entering our scheduler loop, we need to create an active set, initially empty. Create a ready set, which contains all the leaves in the `DepGraph` as `SchedulerNode`s. Also keep track of all `visited_ids` and `finished_ids`, to make it easier to track which nodes are finished / visited (duh).

Now, we enter a `while` loop, and do the following until our condition is met:
1. For all instructions in the active set, call `decrementCyclesLeft()`
2. Remove all finished nodes from the active set, adding all of their IDs the list of finished ids
3. For every dependent of the finished nodes, if all of their parent nodes are finished, and it hasn't been scheduled before, then add it to the ready set.
4. For every node in the ready set, start at the front (the one that was added longest ago), and find the one with the largest weight value (from the heuristic). We call this the "candidate"
5. Remove that candidate node from the ready set, add it to the active set, and add it to the output list of optimized reordered instructions.
6. If the active set and the ready set are both empty, break out of the loop. Otherwise, re-run all these steps

That is the entire scheduling algorithm. But, how do we know it works?

## Test Suite

With 3 different heuristics and 20 benchmarks, that's over 60 times I would have to run around 4-5 commands to check if the output is the same between my optimized code and the original code. This is really annoying, so I made a simple script that checks it all for me. I'm not going to include the script here, but it was just a simple python script that stored temp files between each stage of the output and ran the `diff` utility on each output from the ILOC simulator.

## Results

So, what are the results?
