import json
import os
import csv
import sys
from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd

def load_vulns_by_severity_counts(json_file_path):
    """
    Return a dictionary mapping each severity level ("HIGH", "MEDIUM", "LOW")
    to a dictionary of vulnerability identifiers and their occurrence counts from a Bandit JSON report.
    
    A unique identifier is created by concatenating the 'test_id' and the first 50 characters of 'issue_text'.
    """
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    vulns = {"HIGH": {}, "MEDIUM": {}, "LOW": {}}
    for issue in data.get("results", []):
        sev = issue.get("issue_severity")
        if sev in vulns:
            identifier = f"{issue.get('test_id')}_{issue.get('issue_text')[:50]}"
            vulns[sev][identifier] = vulns[sev].get(identifier, 0) + 1
    return vulns

def main():
    # Ensure repository name is passed as a CLI argument.
    if len(sys.argv) != 2:
        print("Usage: python script.py <repository_name>")
        sys.exit(1)
    
    repo = sys.argv[1].strip()
    folder = f"bandit_outputs_{repo}"
    
    # Read commit order from the repository-specific order file (first line oldest, last newest)
    ordered_commits_file = f"order_commits_{repo}.txt"
    if not os.path.exists(ordered_commits_file):
        print(f"Error: {ordered_commits_file} not found.")
        sys.exit(1)
    
    with open(ordered_commits_file, 'r') as f:
        ordered_commits = [line.strip() for line in f if line.strip()]
    
    print(f"Total commits from {ordered_commits_file}: {len(ordered_commits)}")
    print(f"Oldest commit: {ordered_commits[0]}")
    print(f"Newest commit: {ordered_commits[-1]}")
    
    # Prepare CSV file to store the pattern metrics.
    csv_filename = f"severity_patterns_{repo}.csv"
    with open(csv_filename, "w", newline="") as csvfile:
        fieldnames = [
            "commit_hash",
            "introduced_HIGH", "removed_HIGH",
            "introduced_MEDIUM", "removed_MEDIUM",
            "introduced_LOW", "removed_LOW"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Initialize previous vulnerabilities (counts) as empty dictionaries for each severity.
        previous_vulns = {"HIGH": {}, "MEDIUM": {}, "LOW": {}}
        
        # Process each commit (in chronological order: oldest to newest)
        for commit in ordered_commits:
            json_file = f"{commit}.json"
            json_file_path = os.path.join(folder, json_file)
            if os.path.exists(json_file_path):
                current_vulns = load_vulns_by_severity_counts(json_file_path)
            else:
                print(f"Warning: {json_file} not found in {folder}. Recording zeros for commit {commit}.")
                current_vulns = {"HIGH": {}, "MEDIUM": {}, "LOW": {}}
            
            # For each severity, compute the number of vulnerabilities introduced and removed.
            introduced = {}
            removed = {}
            for severity in ["HIGH", "MEDIUM", "LOW"]:
                # Vulnerabilities that are in the current commit but with an increased count compared to previous commit.
                introduced_count = 0
                for vuln, current_count in current_vulns[severity].items():
                    prev_count = previous_vulns[severity].get(vuln, 0)
                    if current_count > prev_count:
                        introduced_count += (current_count - prev_count)
                introduced[severity] = introduced_count
                
                # Vulnerabilities whose counts have decreased.
                removed_count = 0
                for vuln, prev_count in previous_vulns[severity].items():
                    current_count = current_vulns[severity].get(vuln, 0)
                    if prev_count > current_count:
                        removed_count += (prev_count - current_count)
                removed[severity] = removed_count
            
            row = {
                "commit_hash": commit,
                "introduced_HIGH": introduced["HIGH"],
                "removed_HIGH": removed["HIGH"],
                "introduced_MEDIUM": introduced["MEDIUM"],
                "removed_MEDIUM": removed["MEDIUM"],
                "introduced_LOW": introduced["LOW"],
                "removed_LOW": removed["LOW"],
            }
            writer.writerow(row)
            print(f"Processed commit {commit}: Introduced: {introduced}, Removed: {removed}")
            
            previous_vulns = current_vulns  # Update for next iteration.
    
    print(f"Severity pattern data saved to {csv_filename}")
    
    # --- Plotting the trends using the generated CSV ---
    df = pd.read_csv(csv_filename)
    # Create a numerical index for the x-axis (commit order: 1 for oldest, last for newest)
    df['Commit_Index'] = range(1, len(df) + 1)
    
    # Plot introduced vulnerabilities trend for each severity.
    plt.figure(figsize=(12, 6))
    plt.plot(df['Commit_Index'], df['introduced_HIGH'], marker='o', linestyle='-', label='Introduced HIGH')
    plt.plot(df['Commit_Index'], df['introduced_MEDIUM'], marker='o', linestyle='-', label='Introduced MEDIUM')
    plt.plot(df['Commit_Index'], df['introduced_LOW'], marker='o', linestyle='-', label='Introduced LOW')
    plt.xlabel('Commit (Oldest to Newest)')
    plt.ylabel('Number of Vulnerabilities Introduced')
    plt.title('Trend of Vulnerability Introductions per Severity')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    # Plot removed vulnerabilities trend for each severity.
    plt.figure(figsize=(12, 6))
    plt.plot(df['Commit_Index'], df['removed_HIGH'], marker='o', linestyle='-', label='Removed HIGH')
    plt.plot(df['Commit_Index'], df['removed_MEDIUM'], marker='o', linestyle='-', label='Removed MEDIUM')
    plt.plot(df['Commit_Index'], df['removed_LOW'], marker='o', linestyle='-', label='Removed LOW')
    plt.xlabel('Commit (Oldest to Newest)')
    plt.ylabel('Number of Vulnerabilities Removed')
    plt.title('Trend of Vulnerability Removals per Severity')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
