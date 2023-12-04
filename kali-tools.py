import ctypes
import sys
import os
import subprocess

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    print("Script needs to run with admin as we add environment variables")
    print("Terminal needs to restart for new path additions to work (Restart command prompt and try your new linux commands)")
    sys.exit(0)

# Configuration
linux_distro = 'kali-linux'  # Replace with your kali-linux/kali-linux-headless etc (run wsl --list)

# Paths relative to the script's location
script_directory = os.path.dirname(os.path.realpath(__file__))
powershell_script_path = os.path.join(script_directory, 'powershell_scripts')
wrapper_script_path = os.path.join(script_directory, 'wrapper_scripts')

# Ensure the target directories exist
os.makedirs(powershell_script_path, exist_ok=True)
os.makedirs(wrapper_script_path, exist_ok=True)

print("Checking WSL for binaries to add to Windows now... Please wait")

# Get list of directories in user's PATH
cmd = f'wsl -d {linux_distro} bash -c "echo $PATH"'
result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
paths = result.stdout.strip().split(':')

print("Adding WSL binaries to Windows now... Please wait")

executables = set()
for path in paths:
    # List files in each directory in PATH
    cmd = f'wsl -d {linux_distro} -e ls "{path}"'
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    if result.returncode == 0:  # Check if the command was successful
        executables.update(result.stdout.splitlines())

# Create the shared PowerShell script
ps_script_name = "execution.ps1"
ps_script_file = os.path.join(powershell_script_path, ps_script_name)

# Check and create the shared PowerShell script if it does not exist
if not os.path.exists(ps_script_file):
    ps_script_content = """param (
    [string]$Command
)

$wslCommand = "wsl -d kali-linux bash -c"
$bashCommand = $Command
Invoke-Expression "$wslCommand '$bashCommand'"
"""
    with open(ps_script_file, 'w') as ps_file:
        ps_file.write(ps_script_content)
    print(f"Created shared PowerShell script in '{ps_script_file}'")

# Create Batch scripts for each executable
batch_created_count = 0
for exe in executables:
    # Modify the executable name if it's 'python' to not override windows python
    modified_exe_name = 'lpython' if exe == 'python' else exe

    batch_script_name = f"{modified_exe_name}.bat"
    batch_script_file = os.path.join(wrapper_script_path, batch_script_name)

    # Check and create Batch script if it does not exist
    if not os.path.exists(batch_script_file):
        batch_script_content = (
            "@echo off\n"
            "set \"fullCommand=%~n0 %*\"\n"
            f"powershell -ExecutionPolicy ByPass -File \"%~dp0..\\powershell_scripts\\execution.ps1\" \"%fullCommand%\"\n"
        )
        with open(batch_script_file, 'w') as batch_file:
            batch_file.write(batch_script_content)
        batch_created_count += 1

print(f"Created {batch_created_count} new wrapper batch scripts in '{wrapper_script_path}'")

# Function to check if a path is in the system PATH
def is_path_in_system_path(directory):
    system_path = os.environ['PATH']
    return directory.lower() in (path.lower() for path in system_path.split(';'))

if not is_path_in_system_path(wrapper_script_path):
    # Read the current PATH
    current_path = os.environ['PATH']

    # Check if adding the new path exceeds the character limit
    if len(current_path) + len(wrapper_script_path) + 1 > 1024:
        print("Unable to add to PATH. The resulting PATH would be too long.")
    else:
        # Append the new path
        new_path = current_path + ';' + wrapper_script_path

        # Use setx to update the PATH
        subprocess.run(f'setx PATH "{new_path}" /M', shell=True)

        print(f"Added '{wrapper_script_path}' to PATH")
        print("Please restart your system or log out and back in for the changes to take effect.")
else:
    print(f"The directory {wrapper_script_path} is already in the system PATH.")
