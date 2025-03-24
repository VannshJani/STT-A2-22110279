import subprocess
import time
import os
import git
import json
from itertools import product

def execute_parallel_tests(repo_path, venv_path, processes, threads, dist_mode, repetitions=3):
    os.environ["PYTHONPATH"] = repo_path
    activate_cmd = f'"{venv_path}/Scripts/activate"' if os.name == 'nt' else f'source "{venv_path}/bin/activate"'

    test_cases_failed = {}
    all_failed_tests = []
    total_time = 0
    
    for i in range(repetitions):
        modified = False
        print(f"\nRunning parallel test execution. Iteration {i + 1} with -n {processes} --dist {dist_mode} --parallel-threads {threads}")
        
        command = f"pytest -n {processes} --dist {dist_mode} --parallel-threads {threads}"
        
        start_time = time.time()
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        end_time = time.time()
        total_time += end_time - start_time
        
        all_lines = result.stdout.splitlines()
        num_failed = 0

        for line in all_lines:
            if line.startswith("FAILED"):
                modified = True
                num_failed += 1
                test_case = line.split(" ")[1]
                file = test_case.split("::")[0]
                test_case_name = test_case.split("::")[-1]
                
                all_failed_tests.append([i,test_case_name])
                if i==0:
                    test_cases_failed[test_case_name] = 1
                else:
                    try:
                        test_cases_failed[test_case_name] += 1
                    except KeyError:
                        test_cases_failed[test_case_name] = 1

        
        if test_cases_failed == {} or (modified == False):
            print(f"All Test cases passed in iteration {i + 1}")
        else:
            print(f"{num_failed} test cases failed in iteration {i + 1}")

     # Identifying flaky tests
    print()
    flaky_tests = set()
    for i in range(len(all_failed_tests)):
        if i>0 and all_failed_tests[i][0] != all_failed_tests[i-1][0]:
            print()
        print(f"Failed test case in iteration {all_failed_tests[i][0]}: {all_failed_tests[i][1]}")
   
    for test_case, times_failed in test_cases_failed.items():
        if 1 <= times_failed < repetitions:
            flaky_tests.add(test_case)

    
    print(f"\nTotal flaky tests due to parallelization: {len(flaky_tests)}")
    for test in flaky_tests:
        print(f"Flaky test: {test}")
    
    average_time_parallel = total_time / repetitions
    
    return average_time_parallel, flaky_tests, test_cases_failed

def main():
    url = "https://github.com/keon/algorithms.git"
    repo_path = os.path.abspath("algorithms")

    if not os.path.exists(repo_path):
        try:
            repo = git.Repo.clone_from(url, repo_path)
            print(f"Repository cloned successfully. Commit hash: {repo.head.commit.hexsha}")
        except Exception as e:
            print(f"Failed to clone repository: {e}")
            return

    venv_path = os.path.join(repo_path, 'myenv')
    if not os.path.exists(venv_path):
        subprocess.run(['python', '-m', 'venv', venv_path])

    test_configs = product([1, "auto"], [1, "auto"], ["load", "no"])
    final_results = {}
    
    for processes, threads, dist_mode in test_configs:
        avg_time, flaky_tests, failures = execute_parallel_tests(repo_path, venv_path, processes, threads, dist_mode)
        config_key = f"n-{processes}_threads-{threads}_dist-{dist_mode}"
        final_results[config_key] = {
            "average_time": avg_time,
            "flaky_tests": list(flaky_tests),
            "failures": failures
        }
        print(f"\nAvg parallel execution time (Tpar) with -n {processes}, --parallel {threads}, --dist {dist_mode}: {avg_time:.2f} sec")
    
    with open("results.json", "w") as f:
        json.dump(final_results, f, indent=4)
    print("Results saved to results.json")

if __name__ == "__main__":
    main()