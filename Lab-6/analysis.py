import json

Tseq = float(input("Enter Tseq (average sequential execution time in seconds): "))

# Load parallel test results from JSON file
with open("results.json", "r") as f:
    results = json.load(f)

print("\nParallel Test Execution Analysis")
print("=" * 60)

analysis = {}

# Process each configuration from the results
for config, data in results.items():
    avg_time = data["average_time"]
    flaky_tests = data["flaky_tests"]
    failures = data["failures"]
    
    # Calculate speedup ratio for current configuration
    speedup = Tseq / avg_time if avg_time > 0 else float('inf')
    
    # Collect unique failed test cases across all repetitions
    failed_tests_set = failures.keys()
    
    analysis[config] = {
        "avg_time": avg_time,
        "speedup": speedup,
        "flaky_tests": flaky_tests,
        "failed_tests": list(failed_tests_set)
    }

    # Print configuration summary
    print(f"\nConfiguration: {config}")
    print(f"  Average Parallel Execution Time: {avg_time:.2f} seconds")
    print(f"  Speedup Ratio (Tseq/Tpar): {speedup:.2f}")
    
    if flaky_tests:
        print("  New Flaky Tests Detected:")
        for t in flaky_tests:
            print(f"    - {t}")
    else:
        print("  No new flaky tests detected.")
    
    if failed_tests_set:
        print("  Failed Tests:")
        for t in failed_tests_set:
            print(f"    - {t}")
    else:
        print("  No test failures detected.")


print("\nSummary Execution Matrix:")
header = "{:<30} {:<20} {:<15} {:<20}".format("Configuration", "Avg Time (s)", "Speedup", "Failure Count")
print(header)
print("-" * len(header))
for config, data in analysis.items():
    print("{:<30} {:<20.2f} {:<15.2f} {:<20}".format(
        config, data["avg_time"], data["speedup"], len(data["failed_tests"])
    ))
