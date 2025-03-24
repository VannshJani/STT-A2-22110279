import subprocess
import time
import os
import git


def setup_venv(repo_path):
    venv_path = os.path.join(repo_path, 'myenv')
    if not os.path.exists(venv_path):
        subprocess.run(['python', '-m', 'venv', venv_path])
    return venv_path


# Function to install dependencies
def install_dependencies(venv_path):
    activate_cmd = f'"{venv_path}/Scripts/activate"' if os.name == 'nt' else f'source "{venv_path}/bin/activate"'
    subprocess.run(f"{activate_cmd} && pip install -r algorithms/requirements.txt", shell=True)
    subprocess.run(f"{activate_cmd} && pip install pytest pytest-xdist pytest-run-parallel", shell=True)
    subprocess.run(f"{activate_cmd} && pip install -r algorithms/test_requirements.txt", shell=True)


# Function to execute tests sequentially and detect flaky tests
def execute_sequential_tests(repo_path, venv_path, number_of_runs=10):
    os.environ["PYTHONPATH"] = repo_path
    activate_cmd = f'"{venv_path}/Scripts/activate"' if os.name == 'nt' else f'source "{venv_path}/bin/activate"'

    test_cases_failed = {}  # Dictionary to store test case failure details for each iteration
    all_failed_tests = set()

    for i in range(number_of_runs):
        test_cases_failed[i] = []

        print(f"\nRunning all test cases. Iteration {i + 1}")
        result = subprocess.run(f"{activate_cmd} && pytest -v", shell=True, capture_output=True, text=True)
        all_lines = result.stdout.splitlines()

        for line in all_lines:
            if line.startswith("FAILED"):
                test_case = line.split(" ")[1]
                file = test_case.split("::")[0]
                test_case_name = test_case.split("::")[-1]
                
                all_failed_tests.add(f"{test_case_name}")
                if i==0:
                    test_cases_failed[i].append({
                        "file": file,
                        "test_case": test_case_name,
                        "times_failed": 1
                    })
                else:
                    found = False
                    m=0
                    for test_case_failed in test_cases_failed[i - 1]:
                        if test_case_failed["file"] == file and test_case_failed["test_case"] == test_case_name:
                            test_case_failed["times_failed"] = 1 + test_cases_failed[i-1][m]["times_failed"]
                            found = True
                            break
                        m+=1
                    if not found:
                        test_case_failed["times_failed"] = 1
                    test_cases_failed[i].append(test_case_failed)

        if not test_cases_failed[i]:
            print(f"All Test cases passed in iteration {i + 1}")
        else:
            print(f"{len(test_cases_failed[i])} test cases failed in iteration {i + 1}")

    # Identifying flaky tests
    print()
    flaky_tests = set()
    for i in range(number_of_runs):
        print(f"\nIteration {i + 1}")
        for test_case_failed in test_cases_failed[i]:
            # print(test_case_failed)
            test_case_id = f"{test_case_failed['file']}::{test_case_failed['test_case']}"
            if 1 < test_case_failed["times_failed"] < number_of_runs:
                flaky_tests.add(f"{test_case_failed['test_case']}")
                print(f"Flaky test case: {test_case_failed['file']}::{test_case_failed['test_case']}")
            elif test_case_failed["times_failed"] == number_of_runs:
                print(f"Failed test case: {test_case_failed['file']}::{test_case_failed['test_case']}")

    # Combine all failed and flaky tests
    tests_to_ignore = all_failed_tests.union(flaky_tests)
    print(f"\nTotal failed/flaky tests: {len(tests_to_ignore)}")
    print(f"Failed tests: {len(all_failed_tests)}")
    print(f"Flaky tests: {len(flaky_tests)}")

    # Exclude failed and flaky tests when calculating average time
    if tests_to_ignore:
        ignore_conditions = " and ".join([f'not {test}' for test in tests_to_ignore])
        ignore_args = f'-k "{ignore_conditions}"'
    else:
        ignore_args = ""  # Run all tests if nothing to ignore

    print(f"\nIgnoring tests: {ignore_args}")

    print("\nCalculating average execution time over five repetitions (excluding failed/flaky tests)")
    total_time = 0
    for j in range(3):
        print(f"\nRunning filtered test cases. Iteration {j + 1}")
        start_time = time.time()
        r1 = subprocess.run(f"{activate_cmd} && pytest {ignore_args}", shell=True)
        end_time = time.time()
        print(f"Execution time for iteration {j + 1}: {end_time - start_time:.2f} seconds")
        total_time += end_time - start_time

    average_time_seq = total_time / 3

    return average_time_seq


# Main function
def main():
    url = "https://github.com/keon/algorithms.git"
    repo_path = os.path.abspath("algorithms")

    # Clone repository if not already cloned
    if not os.path.exists(repo_path):
        try:
            repo = git.Repo.clone_from(url, repo_path)
            commit_hash = repo.head.commit.hexsha
            print(f"Repository cloned successfully. Current commit hash: {commit_hash}")
        except Exception as e:
            print(f"Failed to clone repository: {e}")
            return

    # Set up virtual environment
    venv_path = setup_venv(repo_path)
    print(f"Virtual environment set up at: {venv_path}")

    # Install dependencies
    install_dependencies(venv_path)

    # Execute tests sequentially and print outputs
    average_time_seq = execute_sequential_tests(repo_path, venv_path)
    print(
        f"\nAverage sequential execution time (after eliminating failing/flaky tests): {average_time_seq:.2f} seconds"
    )


if __name__ == "__main__":
    main()
