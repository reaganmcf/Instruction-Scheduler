# instruction-scheduler 

An ILOC Instruction Scheduler for the following heuristics: Longest Latency Weighted Path, Longest Latency Instructions, and Random.

You can view more about the actual functionality of each heuristic in `Heuristics.py`.

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

