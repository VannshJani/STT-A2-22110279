import os
import subprocess
import shutil
import xml.etree.ElementTree as ET

def extract_python_files(folder_path):

    python_files_and_paths = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                python_files_and_paths[file] = os.path.join(root, file)
    return python_files_and_paths


python_files_and_paths = extract_python_files("algorithms/algorithms")
print(f"There are {len(python_files_and_paths)} Python files in the algorithms/algorithms folder.")
generated_ptests_folder = "algorithms/generated_tests" 
files_list = os.listdir(generated_ptests_folder)
print(f"There are {len(files_list)} files in the generated_tests folder.")

remaining_files = []
for file in list(python_files_and_paths.keys()):
    if file in files_list:
        remaining_files.append(file)
print(f"There are {len(remaining_files)} files remaining to be tested.")

print(f"{list(python_files_and_paths.keys())[:5]}")
print(f"{files_list[:5]}")

