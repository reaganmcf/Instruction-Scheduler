# instruction-scheduler 

An ILOC Instruction Scheduler for the following heuristics: Longest Latency Weighted Path, Longest Latency Instructions, and Random.

You can view more about the actual functionality of each heuristic in `Heuristics.py`.

I initially started this project in C, but after taking a week break and coming back to the C code base it all started falling apart. As a result, I ended up switching over to Python3, and the codebase ended up being much more concise, robust, and I'm confident in the solution I have implemented.

> Note: this **only works with python3**

## Usage

You can pass in an `.iloc` file (or any type, really - as long as it's valid ILOC code), or can pipe in instructions via `stdin`.

You must provide a flag for which heuristic you want to use:
- `-a` is Longest Latency Weighted Path
- `-b` is Longest Latency Instructions
- `-c` is Random

```console
# Using file
python3 Scheduler.py [-a, -b, -c] [FILE.iloc]

# Using stdin
python3 Scheduler.py [-a, -b, -c] < [FILE.iloc]

# or 
cat [FILE.iloc] | python3 Scheduler.py [-a, -b, -c]
```

