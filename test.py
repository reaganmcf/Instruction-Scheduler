from os import system

if __name__ == '__main__':
    heuristics = ['-a', '-b', '-c']
    print("Running test suite...")

    print("Making temp dir...", end = " ")
    system("rm -r ./tests")
    system("mkdir ./tests")
    print(" Done!")
    for j in range(3):
        heuristic = heuristics[j]

        print(f"Running Heuristic {heuristic}")

        for i in range(20):
            fname = "bench{:02d}".format(i + 1)
            fpath = f"./benchmarks/{fname}.iloc"
            print(f"- Running {fname}...")
            system(f"python3 Scheduler.py {heuristic} < {fpath} > ./tests/h{heuristic}-opt-{fname}.iloc")

            results_name = "res{:02d}".format(i + 1)
            
            system(f"../ILOC_Simulator/sim < {fpath} > ./tests/h{heuristic}-{results_name}.txt")
            system(f"../ILOC_Simulator/sim < ./tests/h{heuristic}-opt-{fname}.iloc > ./tests/h{heuristic}-opt-{results_name}.txt")

            # Get diff
            print("Diff:")
            system(f"diff ./tests/h{heuristic}-{results_name}.txt ./tests/h{heuristic}-opt-{results_name}.txt --color")

            print("----------\n\n")

        print("-----------------------\n\n")
        
    print("Done !")


