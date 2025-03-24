import json
import matplotlib.pyplot as plt

# 1. Load parallel test results from JSON file and ask for Tseq (average sequential time)
Tseq = float(input("Enter Tseq (average sequential execution time in seconds): "))

with open("results.json", "r") as f:
    results = json.load(f)

# 2. Build the execution matrix data
execution_matrix = []

for config, data in results.items():
    avg_time = data["average_time"]
    speedup = Tseq / avg_time if avg_time > 0 else float('inf')
    
    num_reps = 3
    total_failures = sum(data["failures"].values())
    total_tests = 416
    total_runs = total_tests * num_reps

    failure_rate = total_failures / total_runs if total_runs > 0 else 0
    
    execution_matrix.append({
        "config": config,
        "avg_time": avg_time,
        "speedup": speedup,
        "failure_rate": failure_rate,
    })

# 3. Generate a speedup plot for visual comparison
configs = [entry["config"] for entry in execution_matrix]
speedups = [entry["speedup"] for entry in execution_matrix]

plt.figure(figsize=(10, 6))
bars = plt.bar(configs, speedups, color='skyblue')
plt.xlabel("Parallel Configuration")
plt.ylabel("Speedup Ratio (Tseq / Tpar)")
plt.title("Speedup Ratios for Different Parallel Configurations")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

# Annotate bars with speedup values
for bar, sp in zip(bars, speedups):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f"{sp:.2f}", 
             ha='center', va='bottom', fontsize=9)

plt.savefig("speedup_plot.png")
plt.show()

# 4. Print Execution Matrix
print("\nExecution Matrix:")
header = "{:<30} {:<20} {:<15} {:<15}".format("Configuration", "Avg Time (s)", "Speedup", "Failure Rate")
print(header)
print("-" * len(header))
for entry in execution_matrix:
    print("{:<30} {:<20.2f} {:<15.2f} {:<15.5f}".format(
        entry["config"], entry["avg_time"], entry["speedup"], entry["failure_rate"]
    ))

print("\nSpeedup plot saved as 'speedup_plot.png'")
