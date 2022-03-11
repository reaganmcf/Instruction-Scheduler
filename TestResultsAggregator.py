from os import system
import csv
import re

if __name__ == '__main__':
    heuristics = ['-a', '-b', '-c']
    print("Running test suite...")

    output = []

    
    print(" Done!")
    for j in range(3):
        heuristic = heuristics[j]

        print(f"Running Heuristic {heuristic}")

        for i in range(20):
            results_name = "res{:02d}".format(i + 1)

            # Get diff
            reg_file = f"./tests/h{heuristic}-{results_name}.txt" 
            opt_file = f"./tests/h{heuristic}-opt-{results_name}.txt"

            with open(reg_file) as rfile:
                reg_contents = rfile.readlines()
                with open(opt_file) as ofile:
                    opt_contents = ofile.readlines()

                    reg_results = reg_contents[-1][:-1]
                    opt_results = opt_contents[-1][:-1]

                    reg_cycles = int(re.findall("(\\d+) cycles", reg_results)[0])
                    opt_cycles = int(re.findall("(\\d+) cycles", opt_results)[0])
                    
                    print(f"reg = {reg_cycles} vs opt = {opt_cycles}")
                    output.append({
                        "heuristic": str(j),
                        "reg_cycles": reg_cycles, 
                        "opt_cycles": opt_cycles
                    })

            print("----------")

        print("-----------------------\n\n")

    with open('results.csv', 'w') as csvfile:
        fieldnames = ["heuristic", "reg_cycles", "opt_cycles"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in output:
            writer.writerow(row)
        
    print("Done !")


