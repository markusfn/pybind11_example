import os
import sys

# --- Configuration ---
MSYS2_UCRT64_ROOT = r'F:\msys64\ucrt64'
PYTHON_ROOT = MSYS2_UCRT64_ROOT

SOURCE_FILE = 'example.cpp'
MODULE_NAME = 'example'

# --- Define a robust user-specific temporary directory ---
# This will resolve to something like C:\Users\YourUser\AppData\Local\Temp\scons_tmp
# This path is generally always user-writable.
# os.environ.get('LOCALAPPDATA') usually gives C:\Users\YourUser\AppData\Local
user_appdata_local = os.environ.get('LOCALAPPDATA', os.path.join(os.path.expanduser('~'), 'AppData', 'Local'))
USER_TEMP_DIR_WIN = os.path.join(user_appdata_local, 'Temp', 'scons_build_tmp')

# Ensure the temporary directory exists before clang++ tries to use it
os.makedirs(USER_TEMP_DIR_WIN, exist_ok=True)
print(f"Using temporary directory for clang++: {USER_TEMP_DIR_WIN}")

# --- Environment Setup ---
env = Environment(
    tools=[], # Start with an empty list of tools to avoid unwanted defaults
    # IMPORTANT: Explicitly define environment variables for the build process.
    ENV={
        'PATH': os.environ['PATH'],  # Inherit current shell's PATH
        'TMPDIR': USER_TEMP_DIR_WIN, # <--- CRITICAL: Force clang++ to use this dir for its temps
        'TEMP': USER_TEMP_DIR_WIN,   # <--- Also set TEMP and TMP for redundancy
        'TMP': USER_TEMP_DIR_WIN
    }
)

env.Tool('mingw') # Load the MinGW toolchain

# Explicitly set the compiler and linker executables
env['CXX'] = os.path.join(MSYS2_UCRT64_ROOT, 'bin', 'clang++')
env['CC'] = os.path.join(MSYS2_UCRT64_ROOT, 'bin', 'gcc')
env['LINK'] = os.path.join(MSYS2_UCRT64_ROOT, 'bin', 'clang++')

# CXXFLAGS for compilation (GCC/Clang style)
env.Append(CXXFLAGS=[
    '-O3',             # Optimization level 3
    '-Wall',           # Enable all warnings
    '-std=c++17',      # Use C++17 standard
    '-fPIC',           # Generate position-independent code
    '-fvisibility=hidden', # Essential for pybind11
])

# Library paths and libraries for linking
env.Append(LIBPATH=[
    os.path.join(PYTHON_ROOT, 'lib'),
])
env.Append(LIBS=[
    'python3.12',
])

# --- Python Includes ---
try:
    python_exe_path = os.path.join(PYTHON_ROOT, "bin", "python.exe")
    if not os.path.exists(python_exe_path):
        print(f"Warning: Python executable not found at {python_exe_path}. Trying 'python' from PATH.")
        python_exe_path = "python" # Fallback, assumes python is in PATH

    # Run the command and capture output/errors
    process = os.popen(f'"{python_exe_path}" -m pybind11 --includes 2>&1')
    output = process.read()
    exit_code = process.close()

    if exit_code:
        print(f"Error running '{python_exe_path} -m pybind11 --includes':")
        print(output)
        print("Please ensure pybind11 is installed for your MSYS2 Python (e.g., via 'pip install pybind11').")
        sys.exit(1)

    python_includes = [path[2:] for path in output.split() if path.startswith('-I')]
    env.Append(CPPPATH=python_includes)

except Exception as e:
    print(f"Unhandled error getting pybind11 includes: {e}")
    sys.exit(1)

PYBIND11_PACMAN_INCLUDE_PATH = os.path.join(MSYS2_UCRT64_ROOT, 'include', 'pybind11')
if os.path.isdir(PYBIND11_PACMAN_INCLUDE_PATH):
    env.Append(CPPPATH=[PYBIND11_PACMAN_INCLUDE_PATH])
else:
    print(f"Warning: Pybind11 include directory not found at {PYBIND11_PACMAN_INCLUDE_PATH}")
    print("Please verify your pybind11 installation or path in SConscript_gpp.py.")
    sys.exit(1)

env.SharedLibrary(MODULE_NAME, SOURCE_FILE)

print(f"Building {MODULE_NAME}.pyd with clang++...")