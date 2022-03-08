# instruction-scheduler 

An ILOC Instruction Scheduler for Longest Latency Weighted Path, Longest Latency Instructions, and X heuristics.

## Usage

```console
# Using file
python3 Scheduler.py [-a, -b, -c] [FILE.iloc]

# Using stdin
python3 Scheduler.py [-a, -b, -c] < [FILE.iloc]
cat [FILE.iloc] | python3 Scheduler.py [-a, -b, -c]
```

