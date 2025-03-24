import json
import os
import csv
import sys
from collections import OrderedDict
import matplotlib.pyplot as plt
import pandas as pd

def count_confidence_issues(json_file_path):
    """
    Return a dictionary with counts of confidence issues (HIGH, MEDIUM, LOW)
    from a Bandit JSON report.
    """
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    conf_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for issue in data.get("results", []):
        conf = issue.get("issue_confidence")
        if conf in conf_counts:
            conf_counts[conf] += 1
    return conf_counts

def count_severity_issues(json_file_path):
    """
    Return a dictionary with counts of severity issues (HIGH, MEDIUM, LOW)
    from a Bandit JSON report.
    """
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    sev_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for issue in data.get("results", []):
        sev = issue.get("issue_severity")
        if sev in sev_counts:
            sev_counts[sev] += 1
    return sev_counts

def count_unique_cwes(json_file_path):
    """
    Return the number of unique CWEs from a Bandit JSON report.
    """
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    cwe_set = set()
    for issue in data.get("results", []):
        issue_cwe = issue.get("issue_cwe")
        if issue_cwe and "id" in issue_cwe:
            cwe_set.add(issue_cwe["id"])
    return len(cwe_set)

def main():
    # Check for repository argument in CLI
    if len(sys.argv) != 2:
        print("Usage: python q5_analysis.py <repository_name>")
        sys.exit(1)
    
    repo = sys.argv[1].strip()
    folder = f"bandit_outputs_{repo}"
    
    # Read commit order from new_order_commits.txt (first line = oldest commit, last = newest)
    ordered_commits_file = f"order_commits_{repo}.txt"
    if not os.path.exists(ordered_commits_file):
        print(f"Error: {ordered_commits_file} not found.")
        sys.exit(1)
    
    with open(ordered_commits_file, 'r') as f:
        ordered_commits = [line.strip() for line in f if line.strip()]
    
    print(f"Total commits from {ordered_commits_file}: {len(ordered_commits)}")
    print(f"Oldest commit: {ordered_commits[0]}")
    print(f"Newest commit: {ordered_commits[-1]}")
    
    # Create output CSV file to store results
    csv_filename = f"repo_analysis_{repo}.csv"
    with open(csv_filename, "w", newline="") as csvfile:
        fieldnames = ["commit_hash", "conf_HIGH", "conf_MEDIUM", "conf_LOW",
                      "sev_HIGH", "sev_MEDIUM", "sev_LOW", "unique_CWEs"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Process each commit in the given order (oldest to newest)
        for commit in ordered_commits:
            json_file = f"{commit}.json"
            json_path = os.path.join(folder, json_file)
            if os.path.exists(json_path):
                conf_counts = count_confidence_issues(json_path)
                sev_counts = count_severity_issues(json_path)
                unique_cwes = count_unique_cwes(json_path)
            else:
                print(f"Warning: {json_file} not found in {folder}. Recording zeros.")
                conf_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
                sev_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
                unique_cwes = 0
            
            writer.writerow({
                "commit_hash": commit,
                "conf_HIGH": conf_counts["HIGH"],
                "conf_MEDIUM": conf_counts["MEDIUM"],
                "conf_LOW": conf_counts["LOW"],
                "sev_HIGH": sev_counts["HIGH"],
                "sev_MEDIUM": sev_counts["MEDIUM"],
                "sev_LOW": sev_counts["LOW"],
                "unique_CWEs": unique_cwes
            })
            print(f"Processed commit {commit}: Confidence {conf_counts}, Severity {sev_counts}, Unique CWEs {unique_cwes}")
    
    print(f"Data stored in {csv_filename}")
    
    # Load CSV into DataFrame to calculate averages
    df = pd.read_csv(csv_filename)
    
    avg_conf_HIGH = df['conf_HIGH'].mean()
    avg_conf_MEDIUM = df['conf_MEDIUM'].mean()
    avg_conf_LOW = df['conf_LOW'].mean()
    
    avg_sev_HIGH = df['sev_HIGH'].mean()
    avg_sev_MEDIUM = df['sev_MEDIUM'].mean()
    avg_sev_LOW = df['sev_LOW'].mean()
    
    avg_unique_CWEs = df['unique_CWEs'].mean()
    
    print("\nAverage per Commit:")
    print(f"Confidence Issues: HIGH = {avg_conf_HIGH:.2f}, MEDIUM = {avg_conf_MEDIUM:.2f}, LOW = {avg_conf_LOW:.2f}")
    print(f"Severity Issues: HIGH = {avg_sev_HIGH:.2f}, MEDIUM = {avg_sev_MEDIUM:.2f}, LOW = {avg_sev_LOW:.2f}")
    print(f"Unique CWEs: {avg_unique_CWEs:.2f}")
    
    # Create a numerical index for plotting (optional)
    df['Commit_Index'] = range(1, len(df) + 1)
    
    # Plot 1: Confidence Issues Trend
    plt.figure(figsize=(12, 6))
    plt.plot(df['Commit_Index'], df['conf_HIGH'], marker='o', linestyle='-', label='Confidence HIGH')
    plt.plot(df['Commit_Index'], df['conf_MEDIUM'], marker='o', linestyle='-', label='Confidence MEDIUM')
    plt.plot(df['Commit_Index'], df['conf_LOW'], marker='o', linestyle='-', label='Confidence LOW')
    plt.xlabel('Commit (Oldest to Newest)')
    plt.ylabel('Number of Confidence Issues')
    plt.title('Trend of Confidence Issues per Commit')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    # Plot 2: Severity Issues Trend
    plt.figure(figsize=(12, 6))
    plt.plot(df['Commit_Index'], df['sev_HIGH'], marker='o', linestyle='-', label='Severity HIGH')
    plt.plot(df['Commit_Index'], df['sev_MEDIUM'], marker='o', linestyle='-', label='Severity MEDIUM')
    plt.plot(df['Commit_Index'], df['sev_LOW'], marker='o', linestyle='-', label='Severity LOW')
    plt.xlabel('Commit (Oldest to Newest)')
    plt.ylabel('Number of Severity Issues')
    plt.title('Trend of Severity Issues per Commit')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    # Plot 3: Unique CWEs Trend
    plt.figure(figsize=(12, 6))
    plt.plot(df['Commit_Index'], df['unique_CWEs'], marker='o', color='purple', label='Unique CWEs')
    plt.xlabel('Commit (Oldest to Newest)')
    plt.ylabel('Number of Unique CWEs')
    plt.title('Trend of Unique CWEs per Commit')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
