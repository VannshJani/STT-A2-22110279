import os
import sys
import shutil

def clone_repo(repo_url, clone_dir):
    """Clone the repository into clone_dir."""
    if os.path.exists(clone_dir):
        print(f"Directory '{clone_dir}' already exists. Removing...")
        shutil.rmtree(clone_dir)
    command = f"git clone {repo_url} {clone_dir}"
    print(f"Cloning repository from {repo_url} into {clone_dir}...")
    ret = os.system(command)
    if ret != 0:
        print(f"Error cloning repository from {repo_url}")
        sys.exit(ret)
    print("Clone complete.")

def get_commit_hashes(repo_dir,repo_url, count=100):
    """Retrieve the last `count` non-merge commit hashes from the repo."""
    print("Retrieving commit hashes...")
    command = f'git log --no-merges -n {count} --pretty=format:"%H"'
    process = os.popen(f"cd {repo_dir} && {command}")
    output = process.read()
    ret = process.close()
    if ret is not None:
        print("Error retrieving commit hashes.")
        sys.exit(ret)
    commits = output.strip().splitlines()[::-1]  # Reverse the list to have oldest first
    
    with open(f"order_commits_{repo_url.split('/')[-1]}.txt", "w") as f:
        f.write("\n".join(commits))
    
    print(f"Found {len(commits)} commits. Saved to order_commits.txt.")
    return commits

def run_bandit_on_commit(repo_dir, commit_hash, output_dir):
    original_dir = os.getcwd()

    print(f"Checking out commit {commit_hash} in '{repo_dir}'...")
    os.chdir(repo_dir)  # Move into cloned_repo
    ret = os.system(f"git checkout {commit_hash}")
    os.chdir(original_dir)
    output_file = os.path.join(output_dir, f"{commit_hash}.json")
    command = f"bandit -r {repo_dir} -f json -o {output_file}"
    print(f"Running Bandit on commit {commit_hash} (cwd={original_dir})...")
    ret = os.system(command)
    print(f"Bandit output saved to {output_file}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python run.py <repository_url>")
        sys.exit(1)
    
    repo_url = sys.argv[1]
    
    clone_dir = f"cloned_repo_{repo_url.split('/')[-1]}"      
    output_dir = f"bandit_outputs_{repo_url.split('/')[-1]}"   
    

    clone_repo(repo_url, clone_dir)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    commits = get_commit_hashes(clone_dir, repo_url,count=100)
    print(f"First commit: {commits[0]}")
    print(f"Last commit: {commits[-1]}")
    
    for i, commit in enumerate(commits, start=1):
        print(f"\n[{i}/{len(commits)}] Analyzing commit {commit} with Bandit...")
        run_bandit_on_commit(clone_dir, commit, output_dir)
    
    print("\nAll commits have been analyzed with Bandit.")
    
    print("Switching back to 'main' branch in cloned_repo...")
    ret = os.system(f"cd {clone_dir} && git checkout main")
    if ret != 0:
        print("Error switching back to main branch.")
        sys.exit(ret)

if __name__ == "__main__":
    main()
