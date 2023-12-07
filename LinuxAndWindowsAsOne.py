import subprocess
import os
import re
from pathlib import Path
import ctypes
import sys

# Regular expression pattern to match environment variables enclosed in % signs
env_var_pattern = re.compile(r'%([^%]+)%')

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def is_wsl_installed():
    try:
        subprocess.check_output("wsl -l", stderr=subprocess.STDOUT, shell=True)
        return True
    except subprocess.CalledProcessError as e:
        if 'The Windows Subsystem for Linux optional component is not enabled' in str(e.output):
            return False
        raise

def resolve_env_vars(path):
    match = env_var_pattern.search(path)
    if match:
        env_var_name = match.group(1)
        env_var_value = os.environ.get(env_var_name, '')
        return path.replace(match.group(0), env_var_value)
    return path

def find_linux_paths():
    try:
        wsl_paths = subprocess.check_output("wsl echo $PATH", shell=True).decode().strip().split(':')
        linux_executable_files = set()
        for path_dir in wsl_paths:
            if not path_dir.startswith('/mnt'):
                result = subprocess.check_output(f"wsl find {path_dir} -type f -executable", shell=True).decode().split('\n')
                for file in result:
                    if file:
                        file_name = os.path.splitext(os.path.basename(file))[0]
                        linux_executable_files.add(file_name)
        return linux_executable_files
    except Exception as e:
        print("An error occurred:", str(e))
        return set()

def find_windows_paths(wrapper_script_path):
    windows_paths = [Path(resolve_env_vars(x)) for x in os.environ.get('PATH', '').split(';')]
    windows_executable_files = set()
    for path_dir in windows_paths:
        if path_dir.exists() and path_dir != wrapper_script_path:
            for file in path_dir.iterdir():
                if file.is_file() and file.suffix.lower() in ('.exe', '.bat', '.cmd', '.com'):
                    file_name = os.path.splitext(file.name)[0]
                    windows_executable_files.add(file_name)
    return windows_executable_files

def create_batch_file(script_path, exe_name, ps_script_path):
    batch_script_file = os.path.join(script_path, f"{exe_name}.bat")
    if not os.path.exists(batch_script_file):
        with open(batch_script_file, 'w') as batch_file:
            batch_script_content = (
                "@echo off\n"
                "set \"fullCommand=%~n0 %*\"\n"
                f"powershell -ExecutionPolicy ByPass -File \"%~dp0..\\powershell_scripts\\execution.ps1\" \"%fullCommand%\"\n"
            )
            batch_file.write(batch_script_content)
            print(f"Created batch script for {exe_name}")

def handle_conflicts(conflicts, linux_executables, windows_executables, wrapper_script_path, ps_script_path):
    global_choice = None
    for conflict in conflicts:
        if not global_choice:
            choice = input(f"Conflict for '{conflict}'. Choose 'W' for Windows, 'L' for Linux, 'AW' for all conflicts to Windows by default, 'AL' for all conflicts to use Linux by default: ").lower()
            print("-" * 50)
            if choice in ['aw', 'al']:
                global_choice = choice
            elif choice not in ['w', 'l']:
                print("Invalid choice. Skipping.")
                continue
        else:
            choice = global_choice

        if choice == 'l' and conflict in linux_executables:
            create_batch_file(wrapper_script_path, conflict, ps_script_path)
        elif choice in ['w', 'aw'] and conflict in windows_executables:
            create_windows_conflict_batch_file(wrapper_script_path, conflict, ps_script_path)
        elif choice == 'al' and conflict in linux_executables:
            create_linux_conflict_batch_file(wrapper_script_path, conflict, ps_script_path)

def create_windows_conflict_batch_file(script_path, exe_name, ps_script_path):
    batch_script_file = os.path.join(script_path, f"l{exe_name}.bat")
    linux_batch_script_file = os.path.join(script_path, f"{exe_name}.bat")
    if os.path.exists(linux_batch_script_file):
        os.remove(linux_batch_script_file)
        print(f"Removed Linux Version, Now changed to l{exe_name}")
    if not os.path.exists(batch_script_file):
        with open(batch_script_file, 'w') as batch_file:
            batch_script_content = (
                "@echo off\n"
                "set \"fileName=%~n0\"\n"
                "if \"%fileName:~0,1%\" == \"l\" set \"fileName=%fileName:~1%\"\n"
                "set \"fullCommand=%fileName% %*\"\n"
                f"powershell -ExecutionPolicy ByPass -File \"%~dp0..\\powershell_scripts\\execution.ps1\" \"%fullCommand%\"\n"
            )
            batch_file.write(batch_script_content)
            print(f"Created batch script for {exe_name}")

def create_linux_conflict_batch_file(script_path, exe_name, ps_script_path):
    batch_script_file = os.path.join(script_path, f"{exe_name}.bat")
    windows_batch_script_file = os.path.join(script_path, f"l{exe_name}.bat")
    if os.path.exists(windows_batch_script_file):
        os.remove(windows_batch_script_file)
    if not os.path.exists(batch_script_file):
        with open(batch_script_file, 'w') as batch_file:
            batch_script_content = (
                "@echo off\n"
                "set \"fullCommand=%~n0 %*\"\n"
                f"powershell -ExecutionPolicy ByPass -File \"%~dp0..\\powershell_scripts\\execution.ps1\" \"%fullCommand%\"\n"
            )
            batch_file.write(batch_script_content)
            print(f"Created batch script for {exe_name}")

# Function to check if a path is in the system PATH
def is_path_in_system_path(directory):
    system_path = subprocess.check_output('echo %PATH%', shell=True).decode().strip()
    return directory.lower() in (path.lower() for path in system_path.split(';'))

def main():
    if not is_wsl_installed():
        print("WSL is not installed. Please install WSL to use this script.")
        return

    script_directory = os.path.dirname(os.path.realpath(__file__))
    wrapper_script_path = Path(os.path.join(script_directory, 'wrapper_scripts'))
    powershell_script_path = os.path.join(script_directory, 'powershell_scripts', 'execution.ps1')

    windows_executables = find_windows_paths(wrapper_script_path)
    linux_executables = find_linux_paths()

    conflicts = windows_executables.intersection(linux_executables)
    linux_unique = linux_executables - windows_executables

    if not os.path.exists(powershell_script_path):
        with open(powershell_script_path, 'w') as ps_file:
            ps_file.write("param ($args)\n")
            ps_file.write("wsl $args\n")

    os.makedirs(wrapper_script_path, exist_ok=True)

    for linux_exe in linux_unique:
        create_batch_file(wrapper_script_path, linux_exe, powershell_script_path)

    print(f"If specifying to keep the windows version, you can still access the linux variant by using l as a prefix such as lwhoami")
    print(f"You can rerun this script at anytime and update the windows/linux conflicts")
    print(f"Total number of conflicts: {len(conflicts)}")
    print("-" * 50)
    handle_conflicts(conflicts, linux_executables, windows_executables, wrapper_script_path, powershell_script_path)

    print("Script execution complete.")

    # Adding wrapper_script_path to system PATH
    if not is_path_in_system_path(wrapper_script_path):
        # Get the current PATH
        current_path = os.environ.get('PATH', '')
    
        # Append the current directory to PATH with a semicolon
        new_path = f"{current_path};{wrapper_script_path}"
    
        # Set the updated PATH environment variable
        os.environ['PATH'] = new_path
        
        print(f"Added '{wrapper_script_path}' to PATH")
        print("You may need to open a new terminal for the changes to take effect.")
    else:
        print(f"The directory {wrapper_script_path} is already in the system PATH.")


if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
else:
    main()
