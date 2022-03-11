from matplotlib import pyplot as plt
import numpy as np
import csv

labels = ["Heuristic 1", "Heuristic 2", "Heuristic 3"]
reg_mean_cycles = [0,0,0]
opt_mean_cycles = [0,0,0]


with open("./results.csv") as results_file:
    reader = csv.DictReader(results_file)

    reg_total_cycles = [0,0,0]
    opt_total_cycles = [0,0,0]

    for row in reader:
        heuristic = int(row['heuristic'])
        reg_total_cycles[heuristic] += int(row['reg_cycles'])
        opt_total_cycles[heuristic] += int(row['opt_cycles'])
    
    for i in range(3):
        reg_mean_cycles[i] = reg_total_cycles[i] / 20
        opt_mean_cycles[i] = opt_total_cycles[i] / 20

print(reg_mean_cycles)
print(opt_mean_cycles)

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, reg_mean_cycles, width, label='Regular Cycles')
rects2 = ax.bar(x + width/2, opt_mean_cycles, width, label='Optimized Cycles')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Cycles')
ax.set_title('Mean Cycles for each Hueristic')
ax.set_xticks(x, labels)
ax.legend()

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

fig.tight_layout()

plt.show()

