import json
import os
import sys
from collections import Counter
import matplotlib.pyplot as plt
import csv

def extract_cwes(json_file_path):
    """
    Extracts CWE IDs from a Bandit JSON report.
    Returns a list of CWE IDs (integers) found in the 'issue_cwe' object.
    If a vulnerability appears multiple times in a commit, its CWE will be counted multiple times.
    """
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    cwe_ids = []
    for issue in data.get("results", []):
        issue_cwe = issue.get("issue_cwe")
        if issue_cwe and "id" in issue_cwe:
            cwe_ids.append(issue_cwe["id"])
    return cwe_ids

def main():
    # Ensure at least one repository name is provided as CLI argument.
    if len(sys.argv) < 2:
        print("Usage: python rq3_cwe_coverage.py <repository_name1> [<repository_name2> ...]")
        sys.exit(1)
    
    repo_names = sys.argv[1:]
    global_cwe_counter = Counter()
    
    # Process each repository folder.
    for repo in repo_names:
        folder = f"bandit_outputs_{repo}"
        if not os.path.exists(folder):
            print(f"Warning: Folder {folder} not found. Skipping repository '{repo}'.")
            continue
        
        # List all JSON files in the repository folder.
        json_files = [f for f in os.listdir(folder) if f.endswith(".json")]
        print(f"Processing {len(json_files)} JSON files for repository '{repo}' in folder '{folder}'...")
        
        for json_file in json_files:
            json_path = os.path.join(folder, json_file)
            cwe_ids = extract_cwes(json_path)
            global_cwe_counter.update(cwe_ids)
    
    if not global_cwe_counter:
        print("No CWE data found in the provided repositories.")
        sys.exit(0)
    
    # Sort CWEs by frequency (most common first)
    sorted_cwes = global_cwe_counter.most_common()
    
    # Write the CWE frequency data to a CSV file.
    csv_filename = "cwe_frequency_across_repos.csv"
    with open(csv_filename, "w", newline="") as csvfile:
        fieldnames = ["CWE_ID", "Frequency"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for cwe_id, count in sorted_cwes:
            writer.writerow({"CWE_ID": cwe_id, "Frequency": count})
    
    print(f"CWE frequency data saved to {csv_filename}")
    
    # Plot the most frequent CWEs.
    # For example, plot the top 10 CWEs.
    top_n = 10
    top_cwes = sorted_cwes[:top_n]
    cwe_ids = [f"CWE-{cwe_id}" for cwe_id, _ in top_cwes]
    frequencies = [count for _, count in top_cwes]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(cwe_ids, frequencies, color='skyblue')
    plt.xlabel("CWE ID")
    plt.ylabel("Frequency")
    plt.title("Top {} Most Frequent CWEs Across Repositories".format(top_n))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add labels on top of each bar.
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 1, yval, ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
