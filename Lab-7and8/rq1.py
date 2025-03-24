import json
import os
import sys
from collections import OrderedDict, defaultdict

def load_high_severity_issues_with_counts(json_file_path):
    """
    Return a dictionary mapping each high-severity vulnerability identifier to its count.
    The identifier is built from test_id and issue_text.
    """
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    vuln_counts = {}
    for issue in data.get("results", []):
        if issue.get("issue_severity") == "HIGH":
            # Using full issue_text for uniqueness; you might truncate if needed.
            identifier = f"{issue.get('test_id')}_{issue.get('issue_text')}"
            vuln_counts[identifier] = vuln_counts.get(identifier, 0) + 1
    return vuln_counts

def main():
    # Check if repository name is provided as a command-line argument.
    if len(sys.argv) != 2:
        print("Usage: python script.py <repository_name>")
        sys.exit(1)
    
    repo = sys.argv[1].strip()
    folder = f"bandit_outputs_{repo}"
    
    # Read the ordered commit hashes from the external file.
    ordered_commits_file = f"order_commits_{repo}.txt"
    if not os.path.exists(ordered_commits_file):
        print(f"Error: {ordered_commits_file} does not exist.")
        sys.exit(1)
    
    with open(ordered_commits_file, 'r') as f:
        ordered_commits = [line.strip() for line in f if line.strip()]
    
    print(f"Total commits from {ordered_commits_file}: {len(ordered_commits)}")
    print(f"Oldest commit: {ordered_commits[0]}")
    print(f"Newest commit: {ordered_commits[-1]}")
    
    # Build an ordered timeline: commit hash -> vulnerability count dictionary.
    timeline = OrderedDict()
    for commit in ordered_commits:
        json_file = f"{commit}.json"
        json_file_path = os.path.join(folder, json_file)
        if os.path.exists(json_file_path):
            counts = load_high_severity_issues_with_counts(json_file_path)
            timeline[commit] = counts
        else:
            print(f"Warning: {json_file} not found in {folder}. Recording empty counts.")
            timeline[commit] = {}
    
    vuln_history = defaultdict(list)
    previous_counts = {}
    
    for commit in ordered_commits:
        current_counts = timeline[commit]
        # Check for new vulnerabilities or count increases (reintroduction)
        for vuln, count in current_counts.items():
            prev_count = previous_counts.get(vuln, 0)
            if count > prev_count:
                vuln_history[vuln].append({
                    'introduced': commit,
                    'introduced_count': count,
                    'fixed': None,
                    'fixed_count': None
                })
        # Check for vulnerabilities that decreased in count or were removed.
        for vuln, prev_count in previous_counts.items():
            current_count = current_counts.get(vuln, 0)
            if prev_count > current_count:
                # Find the last event for this vulnerability that is still open (not fixed)
                if vuln_history[vuln]:
                    last_event = vuln_history[vuln][-1]
                    if last_event['fixed'] is None:
                        last_event['fixed'] = commit
                        last_event['fixed_count'] = current_count
        previous_counts = current_counts
    
    print("\nHigh-Severity Vulnerability History:")
    for vuln, events in vuln_history.items():
        for idx, event in enumerate(events, start=1):
            print("----------------")
            print(f"Vulnerability {vuln} (Event {idx}): Introduced in commit {event['introduced']} "
                  f"(count: {event['introduced_count']}), Fixed in commit {event['fixed']} "
                  f"(count: {event['fixed_count']})")
    
if __name__ == "__main__":
    main()
