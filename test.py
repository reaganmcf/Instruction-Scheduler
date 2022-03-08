from os import system
if __name__ == '__main__':
    print("Running test suite...")

    print("Making temp dir...", end = " ")
    system("rm -r ./tests")
    system("mkdir ./tests")
    print(" Done!")

    for i in range(20):
        fname = "bench{:02d}".format(i + 1)
        fpath = f"./benchmarks/{fname}.iloc"
        print(f"- Running {fname}...")
        system(f"python3 Scheduler.py -a < {fpath} > ./tests/opt-{fname}.iloc")

        results_name = "res{:02d}".format(i + 1)
        
        # Run non-optimized
        system(f"../ILOC_Simulator/sim < {fpath} > ./tests/{results_name}.txt")
        system(f"../ILOC_Simulator/sim < ./tests/opt-{fname}.iloc > ./tests/opt-{results_name}.txt")

        # Get diff
        print("Diff:")
        system(f"diff ./tests/{results_name}.txt ./tests/opt-{results_name}.txt --color")

        print("----------\n\n")
    
    print("Cleaning up temp dir...", end = " ")
    #system("rm -r tests/")
    print("Done !")


