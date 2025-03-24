import os
import subprocess
import shutil
from typing import List
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np
from bs4 import BeautifulSoup

# Repository URL
REPO_URL = "https://github.com/keon/algorithms.git"
REPO_NAME = "algorithms"
os.environ["PYNGUIN_DANGER_AWARE"] = "true"

# Install dependencies in the active Conda environment
def install_dependencies():
    print("[*] Installing dependencies in Conda environment...")
    dependencies = ["pytest", "pytest-cov", "pytest-func-cov", "coverage", "pynguin"]
    subprocess.run(["pip", "install", "--upgrade", "pip"])
    subprocess.run(["pip", "install"] + dependencies)
    print("[*] Dependencies installed.")

# Clone the repository
def clone_repository():
    if os.path.exists(REPO_NAME):
        shutil.rmtree(REPO_NAME)
    print(f"[*] Cloning repository {REPO_URL}...")
    subprocess.run(["git", "clone", REPO_URL])
    print("[*] Repository cloned.")

# Get the latest commit hash
def get_commit_hash():
    print("[*] Fetching latest commit hash...")
    commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO_NAME).strip().decode()
    print(f"[*] Current commit hash: {commit_hash}")
    return commit_hash

# Run existing test cases (Test Suite A)
def run_existing_tests(file_name = "coverage.xml"):
    print("[*] Running existing test suite...")
    subprocess.run(["pytest", "--cov=algorithms", "--cov-report=term", f"--cov-report=xml:{file_name}"], cwd=REPO_NAME)
    print("[*] Test Suite A executed.")


def generate_coverage_report(name="tests"):
    print("[*] Running coverage for specific test cases...")
    
    # Run tests with coverage (specify source folder)
    subprocess.run(["coverage", "run", "--source", REPO_NAME, "-m", "pytest", name], cwd=REPO_NAME)
    
    print("[*] Generating coverage report...")
    subprocess.run(["coverage", "html"], cwd=REPO_NAME)
    
    print("[*] Coverage report generated. Check 'algorithms/htmlcov/index.html'.")

def extract_python_files(folder_path):
    '''
    Extracts all Python files from the given folder path, including files in subfolders.
    Returns a dictionary mapping filename to its full file path.
    '''
    python_files_and_paths = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                python_files_and_paths[file] = os.path.join(root, file)
    return python_files_and_paths

def get_coverage_data(filename="coverage.xml"):
    '''
    Parses the specified XML file and returns a mapping of Python file basenames
    to their line coverage (as a float, e.g., 1.0 for 100%).
    '''
    coverage_file = os.path.join(REPO_NAME, filename)
    coverage_data = {}
    try:
        tree = ET.parse(coverage_file)
        root = tree.getroot()
        for package in root.findall(".//package"):
            for clazz in package.findall("classes/class"):
                file_name = clazz.attrib.get("filename")
                line_rate = float(clazz.attrib.get("line-rate", "0"))
                # Use the basename for matching
                base = os.path.basename(file_name)
                coverage_data[base] = line_rate
    except Exception as e:
        print(f"[!] Error parsing coverage data: {e}")
    return coverage_data


# Generate additional test cases (Test Suite B) using Pynguin
def generate_tests_with_pynguin():
    print("[*] Generating new test cases using Pynguin...")
    
    source_folder = os.path.join(REPO_NAME, "algorithms")
    generated_tests_folder = os.path.join(REPO_NAME, "generated_tests")
    
    if not os.path.exists(generated_tests_folder):
        os.makedirs(generated_tests_folder)
    
    coverage_data = get_coverage_data()
    python_files_and_paths = extract_python_files(source_folder)
    
    existing_tests = {f.replace("test_", "") for f in os.listdir(generated_tests_folder) if f.startswith("test_")}
    error_dict = {}
    
    for python_file, file_path in python_files_and_paths.items():
        coverage = coverage_data.get(python_file, 0)
        
        
        if python_file in ["unique_bst.py", "count_connected_number_of_component.py","strongly_connected_components_kosaraju.py","minimum_spanning_tree.py","rabin_karp.py","bst.py","delete_node.py"]:
            continue
        
        print(f"[*] Generating test cases for {python_file} (coverage: {coverage*100:.1f}%)...")
        module_name = python_file.replace(".py", "")
        folder_path = file_path.replace(python_file, "")
        splitted_path = folder_path.split("/")[1:]
        final_mod_name = ".".join(splitted_path) + module_name
        test_file_name = final_mod_name.replace(".", "_") + ".py"
        if test_file_name in existing_tests:
            print(f"[!] Test file already exists for {python_file}. Skipping test generation.")
            continue
        try:
            subprocess.run([
                "pynguin",
                "--project-path", "/Users/vannshjani/Library/Mobile Documents/com~apple~CloudDocs/STT/Lab-8/algorithms",
                "--module-name", final_mod_name,
                "--output-path", generated_tests_folder,
                "--maximum_coverage", "100"
            ], check=True)
            print(f"[*] Test generation completed for {python_file}")
        except subprocess.CalledProcessError as e:
            error_dict[python_file] = str(e)
            print(f"[!] Error while generating tests for {python_file}: {e}")
    
    print("[*] Test Suite B generated in", generated_tests_folder)
    
    if error_dict:
        print("\n[!] Errors encountered during test generation:")
        for file, error in error_dict.items():
            print(f"- {file}: {error}")
    

def get_coverage_data_from_index_html(filepath):
    """
    Parses the index.html file generated by coverage and extracts
    file-level coverage data. If available, additional details (class/function)
    can be parsed similarly.

    Parameters:
      - filepath: path to the index.html file.

    Returns:
      A dict mapping file names (as strings) to file coverage ratios (floats between 0 and 1).
    """
    coverage_data = {}
    with open(filepath, "r") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Assuming that the coverage report has a table where the first column is the file name
    # and the last column contains the coverage percentage (e.g., "85.0%").
    table = soup.find("table")
    if not table:
        print(f"[!] No table found in {filepath}.")
        return coverage_data

    rows = table.find_all("tr")
    # Assume the first row is a header row
    for row in rows[1:]:
        cells = row.find_all("td")
        if len(cells) < 2:
            continue
        file_name = cells[0].get_text(strip=True)
        coverage_text = cells[-1].get_text(strip=True).rstrip('%')
        try:
            # Convert to ratio (0 to 1)
            coverage_value = float(coverage_text) / 100.0
            coverage_data[file_name] = coverage_value
        except ValueError:
            continue
    return coverage_data


def analyze_coverage(test_suite_a_coverage, test_suite_b_coverage):

    common_files = set(test_suite_a_coverage.keys()) & set(test_suite_b_coverage.keys())
    common_a = {f: test_suite_a_coverage[f] for f in common_files}
    common_b = {f: test_suite_b_coverage[f] for f in common_files}
    
    # Sort files by Test Suite B coverage (descending) for overall summary
    all_files = sorted(common_files, key=lambda f: common_b.get(f, common_a[f]), reverse=True)
    
    # Prepare coverage values (in percentage) for all files
    a_values_all = {f: common_a[f] * 100 for f in all_files}
    b_values_all = {f: common_b[f] * 100 for f in all_files}
    
    # Compute improvements
    improvements_all = {f: b_values_all[f] - a_values_all[f] for f in all_files}
    
    # Collect files that improved (Test Suite B > Test Suite A)
    improved_files = {f: round(improvements_all[f], 2) for f in all_files if improvements_all[f] > 0}
    
    # Identify and print files where Test Suite A had 0% but Test Suite B had >0% coverage.
    print("\n[+] New Coverage Scenarios (Test Suite A: 0% coverage, Test Suite B: >0%):")
    new_coverage_scenarios = {}
    for f in all_files:
        if common_a[f] == 0.0 and common_b[f] > 0.0:
            new_coverage_scenarios[f] = common_b[f] * 100
            print(f"  {f}: Test Suite A = 0.00%, Test Suite B = {common_b[f]*100:.2f}%")
    if not new_coverage_scenarios:
        print("  None detected.")

    # Summary statistics
    total_files = len(all_files)
    fully_covered_a = sum(1 for v in a_values_all.values() if v == 100.0)
    improved_count = len(improved_files)
    no_improvement = total_files - improved_count
    
    summary_stats = {
        "total_files": total_files,
        "fully_covered_test_suite_a": fully_covered_a,
        "files_improved": improved_count,
        "files_not_improved": no_improvement,
        "improved_files": improved_files
    }
    
    # --- Horizontal Bar Chart for Top 10 Improvements ---
    # Filter top 10 files with highest improvement
    top_improved = sorted([f for f in improved_files], key=lambda f: improvements_all[f], reverse=True)[:10]
    # Prepare values for these top improved files
    a_values = [common_a[f] * 100 for f in top_improved]
    b_values = [common_b[f] * 100 for f in top_improved]
    improvements = [b - a for a, b in zip(a_values, b_values)]
    
    import matplotlib.pyplot as plt
    import numpy as np
    
    total_plotted = len(top_improved)
    fig_height = max(6, 0.5 * total_plotted)
    fig, ax = plt.subplots(figsize=(12, fig_height))
    
    y_positions = np.arange(total_plotted)
    bar_width = 0.4
    
    # Test Suite A bars
    ax.barh(y_positions - bar_width/2, a_values, bar_width, label='Test Suite A Coverage', color='#1f77b4')
    # Test Suite B bars
    ax.barh(y_positions + bar_width/2, b_values, bar_width, label='Test Suite B Coverage', color='#ff7f0e')
    
    ax.set_xlabel('Coverage (%)', fontsize=12)
    ax.set_title('Top 10 Files by Coverage Improvement (Test Suite B vs Test Suite A)', fontsize=14)
    ax.set_yticks(y_positions)
    ax.set_yticklabels(top_improved, fontsize=9)
    ax.invert_yaxis()  # so that the highest improvement is at the top
    ax.set_xlim([0, 110])
    ax.legend()
    
    # Annotate each bar with coverage percentage
    for i, (a_val, b_val) in enumerate(zip(a_values, b_values)):
        ax.annotate(f'{a_val:.1f}%',
                    xy=(a_val, i - bar_width/2),
                    xytext=(5, 0),
                    textcoords="offset points",
                    va='center', ha='left', fontsize=8)
        ax.annotate(f'{b_val:.1f}%',
                    xy=(b_val, i + bar_width/2),
                    xytext=(5, 0),
                    textcoords="offset points",
                    va='center', ha='left', fontsize=8)
    
    plt.tight_layout()
    plt.savefig("coverage_comparison_top10_bar_chart.png")
    plt.show()
    
    # --- Pie Chart for Overall Improvement Statistics ---
    labels = ['Improved', 'Not Improved']
    sizes = [improved_count, no_improvement]
    
    if sum(sizes) == 0:
        print("[!] No data to plot for the pie chart. Skipping pie chart plotting.")
    else:
        colors = ['#66b3ff', '#ff9999']
        fig2, ax2 = plt.subplots()
        ax2.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        ax2.axis('equal')
        plt.title("Overall Files Improvement")
        plt.savefig("overall_improvement_pie_chart.png")
        plt.show()
    
    # Print Summary Statistics
    print("\n[+] Summary Statistics:")
    print(f"  Total files analyzed: {total_files}")
    print(f"  Files 100% covered in Test Suite A: {fully_covered_a}")
    print(f"  Files where Test Suite B improved coverage: {improved_count}")
    print(f"  Files with no improvement: {no_improvement}")
    
    print("\n[+] Improved Files Details:")
    for file, improvement in improved_files.items():
        if file == 'Total':
            continue
        print(f"  {file}: +{improvement:.2f}%")
    
    return summary_stats


def compare_test_suites():
    print("[*] Comparing test suites (Test Suite A vs Test Suite B)...")
    
    # Parse the HTML reports generated by coverage.
    report_a = "/Users/vannshjani/Library/Mobile Documents/com~apple~CloudDocs/STT/Lab-8/algorithms/htmlcov/index.html"
    report_b = "/Users/vannshjani/Library/Mobile Documents/com~apple~CloudDocs/STT/Lab-8/new/algorithms/htmlcov/index.html"
    
    test_suite_a_coverage = get_coverage_data_from_index_html(report_a)
    test_suite_b_coverage = get_coverage_data_from_index_html(report_b)
    

    test_suite_a_coverage = {file: rate for file, rate in test_suite_a_coverage.items() if file in test_suite_b_coverage}
    not_present = {file: rate for file, rate in test_suite_b_coverage.items() if file not in test_suite_a_coverage}
    print(f"T-A: {len(test_suite_a_coverage)}")
    print(f"T-B: {len(test_suite_b_coverage)}")

    # # printing files in test_suite_a_coverage
    # print("\n[*] Files in Test Suite A:")
    # for file in test_suite_a_coverage:
    #     print(f"File: {file}")

    # # printing files in test_suite_b_coverage
    # print("\n[*] Files in Test Suite B:")
    # for file in test_suite_b_coverage:
    #     print(f"File: {file}")

    # print files present in  B but not in A
    print("\n[*] Files in Test Suite B but not in Test Suite A:")
    for file in not_present:
        print(f"File: {file}")

    return
    
    print("\n[*] Detailed Coverage Comparison:")
    for file, a_rate in test_suite_a_coverage.items():
        if file == 'Total':
            continue
        b_rate = test_suite_b_coverage.get(file, a_rate)
        improvement = b_rate - a_rate
        print(f"\nFile: {file}")
        print(f"  Test Suite A Coverage: {a_rate*100:.2f}%")
        print(f"  Test Suite B Coverage: {b_rate*100:.2f}%")
        if improvement > 0:
            print(f"  Improvement: {improvement*100:.2f}%")
        else:
            print("  No improvement.")
    
    # Analyze and plot the results
    stats = analyze_coverage(test_suite_a_coverage, test_suite_b_coverage)
    return stats




# Main execution (make sure to uncomment required functions when running the full pipeline)
# install_dependencies()
# clone_repository()
# commit_hash = get_commit_hash()
# run_existing_tests()
# generate_coverage_report()
# generate_tests_with_pynguin()
compare_test_suites()