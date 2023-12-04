# LinuxAndWindowsAsOne

![GitHub](https://img.shields.io/github/license/pentestfunctions/LinuxAndWindowsAsOne)
![GitHub last commit](https://img.shields.io/github/last-commit/pentestfunctions/LinuxAndWindowsAsOne)
![GitHub issues](https://img.shields.io/github/issues/pentestfunctions/LinuxAndWindowsAsOne)
![GitHub stars](https://img.shields.io/github/stars/pentestfunctions/LinuxAndWindowsAsOne)

## Introduction

**LinuxAndWindowsAsOne** is a script that allows you to seamlessly integrate Windows and Linux environments by adding Linux binaries to your Windows system. This tool is especially useful for penetration testers and security professionals who need access to Linux tools within a Windows environment.

The script creates batch scripts that act as wrappers for Linux binaries, making them accessible from the Windows command prompt. Additionally, it adds these batch script directories to your system PATH, ensuring that you can easily run Linux commands from the Windows terminal.

## Prerequisites

Before using **LinuxAndWindowsAsOne**, make sure you have the following prerequisites:

- Windows 10 or later
- Windows Subsystem for Linux (WSL) installed
- Administrative privileges on your Windows system

WSL can be installed with
- https://www.kali.org/docs/wsl/wsl-preparations/

### Updating!
- Important notes: Whenever you install new applications in your WSL, you will need to rerun the kali-tools.py script and it will automatically add the new tools to your environment variables.
- If your graphical interfactes (konsole/burpsuite/brave-browser etc have issues use the Graphicalfix.bat)

## Installation

1. Clone the **LinuxAndWindowsAsOne** repository to your Windows system.

```bash
git clone https://github.com/pentestfunctions/LinuxAndWindowsAsOne.git
```

2. Move the script to a folder on your C:\\ drive, such as `C:\\Tools\\kali-tools.py`.

## Usage

### Running the Script

**LinuxAndWindowsAsOne** is designed to be run as an administrator because it modifies environment variables and system PATH. To execute the script:

1. Right-click on the script file, e.g., `kali-tools.py`, and select "Run as administrator."
2. The script will check if you have administrative privileges and, if not, prompt you to run with elevated privileges.

#### Problems?

If the script has problems running as it is, make sure you have python installed on Windows and CD into your folder such as 
```bash
mkdir C:\Tools
cd C:\Tools
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/pentestfunctions/LinuxAndWindowsAsOne/main/kali-tools.py' -OutFile 'kali-tools.py'"
python kali-tools.py
```

### Configuration

Before running the script, make sure to configure the following settings in the script:

- `linux_distro`: Set this variable to the name of your preferred Linux distribution within WSL (e.g., 'kali-linux' or 'ubuntu').

### Adding Linux Binaries to Windows

The script will automatically identify the Linux binaries available in your WSL distribution and create batch scripts for each of them. These batch scripts act as wrappers, allowing you to run Linux commands from the Windows command prompt.
- It's also important to note, to use the linux python instead of windows python you will need to type in "lpython" instead of python as this is a safety measure to not interfere with python on windows.

### PATH Configuration

The script will also add the directory containing the batch scripts to your system PATH to make these commands accessible from any terminal window. If you encounter any issues, you might need to restart your terminal for the changes to take effect.

## Contributing

If you find any issues or have suggestions for improvement, please [open an issue](https://github.com/pentestfunctions/LinuxAndWindowsAsOne/issues) on the GitHub repository. We welcome contributions and pull requests from the community.


## Ideas
1. Find all paths correctly and add them.
2. Automatically find WSL distro and let the user menu select which they want
3. Whenever apt-get or other well known installation commands are run, their respective commands will auto add/update.
4. Add more exclusions other than python/lpython for things that windows has as well as the linux distro (*just add an l at the front to represent linux)
5. Some piping doesn't work see below:
   ```bash
   echo "deb http://http.kali.org/kali kali-rolling main non-free contrib" sudo tee /etc/apt/sources.list
   ```
