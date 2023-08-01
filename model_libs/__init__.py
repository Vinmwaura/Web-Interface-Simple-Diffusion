import os
import sys

# Change to match name of folder if needed.
all_libs = [
    "simple_diffusion"
]

dir_path = os.path.dirname(os.path.abspath(__file__))

for lib_folder in all_libs:
    lib_path = os.path.join(dir_path, lib_folder)
    if os.path.isdir(lib_path):
        sys.path.append(lib_path)
