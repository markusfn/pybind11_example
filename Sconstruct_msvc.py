import os
import sys
from SCons.Script import *

# --- Configuration ---

# Path to your Python installation
PYTHON_ROOT = r"F:\Python\Python313"
PYTHON_LIB_DIR = os.path.join(PYTHON_ROOT, 'libs') # Corrected based on your finding
PYTHON_INCLUDE_DIR = os.path.join(PYTHON_ROOT, 'include')
PYBIND11_INCLUDE_DIR = os.path.join(PYTHON_ROOT, 'Lib', 'site-packages', 'pybind11', 'include')

print(f"Using Python root: {PYTHON_ROOT}")

# --- Verify Python Paths Exist ---
if not os.path.isdir(PYTHON_LIB_DIR):
    print(f"Error: Python lib directory not found: {PYTHON_LIB_DIR}")
    sys.exit(1)
if not os.path.isdir(PYTHON_INCLUDE_DIR):
    print(f"Error: Python include directory not found: {PYTHON_INCLUDE_DIR}")
    sys.exit(1)
if not os.path.isdir(PYBIND11_INCLUDE_DIR):
    print(f"Error: Pybind11 include directory not found: {PYBIND11_INCLUDE_DIR}")
    print("Please ensure pybind11 is installed correctly in your Python environment and its include path is valid.")
    sys.exit(1)


# --- Determine exact Python library name ---
python_lib_found = None
for lib_name_base in ['python313', 'python3', 'python']:
    potential_lib_path = os.path.join(PYTHON_LIB_DIR, f"{lib_name_base}.lib")
    if os.path.exists(potential_lib_path):
        python_lib_found = lib_name_base
        print(f"Found Python library: {potential_lib_path}")
        break

if not python_lib_found:
    print(f"FATAL ERROR: Could not find Python import library (.lib) in {PYTHON_LIB_DIR}.")
    print("Please check the 'libs' folder inside your Python installation for files like 'python313.lib', 'python3.lib', or 'python.lib'.")
    sys.exit(1)

SOURCE_FILE = 'example.cpp'
MODULE_NAME = 'example'

# --- Environment Setup ---
# FIX: Add 'default' tool to ensure standard builders like SharedLibrary are available
env = Environment(tools=['default', 'msvc'])

env.Append(CPPFLAGS=[
    '/W4',       # Warning level 4
    '/Zi',       # Generate debug information for pdb files
    '/std:c++20',# C++20 standard
])

env.Append(LINKFLAGS=[])

env.Append(LIBPATH=[
    PYTHON_LIB_DIR,
])

env.Append(LIBS=[
    python_lib_found,
])

env.Append(CPPPATH=[
    PYTHON_INCLUDE_DIR,
    PYBIND11_INCLUDE_DIR
])

env['SHLIBSUFFIX'] = '.pyd'

# --- Build the Shared Library ---
python_module = env.SharedLibrary(MODULE_NAME, SOURCE_FILE)

Default(python_module)

print(f"Building {MODULE_NAME}.pyd with MSVC...")