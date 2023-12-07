# LinuxAndWindowsAsOne

![GitHub last commit](https://img.shields.io/github/last-commit/pentestfunctions/LinuxAndWindowsAsOne)
![GitHub issues](https://img.shields.io/github/issues/pentestfunctions/LinuxAndWindowsAsOne)
![GitHub stars](https://img.shields.io/github/stars/pentestfunctions/LinuxAndWindowsAsOne)

## Introduction

**LinuxAndWindowsAsOne** is a script that allows you to seamlessly integrate Windows and Linux environments by adding Linux binaries to your Windows system. This tool is especially useful for penetration testers and security professionals who need access to Linux tools within a Windows environment.

The script creates batch scripts that act as wrappers for Linux binaries, making them accessible from the Windows command prompt. Additionally, it adds these batch script directories to your system PATH, ensuring that you can easily run Linux commands from the Windows terminal.

## INSTALL PREFERRED METHOD

1. Install Python
   - https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe

2. Install WSL with Kali Linux
   - https://www.kali.org/docs/wsl/wsl-preparations/

3. Open a COMMAND PROMPT (NOT POWERSHELL) as ADMINISTRATOR. 

```bash
mkdir C:\Tools
cd C:\Tools
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/pentestfunctions/LinuxAndWindowsAsOne/main/LinuxAndWindowsAsOne.py' -OutFile 'LinuxAndWindowsAsOne.py'"
python LinuxAndWindowsAsOne.py
```

4. While it runs, answer the questions for any conflicts - such as "whoami" exists on linux and windows. Choosing to keep the windows variant will make the linux version "lwhoami" 

Close your terminal and open a new one - Run any command!

- Optional:
  1. Rerun the script anytime when you install new software to WSL
  2. Rerun the script anytime you wish to reorganize the conflicts, such as changing curl to for linux from lcurl

### Updating!
- Important notes: Whenever you install new applications in your WSL, you will need to rerun the kali-tools.py script and it will automatically add the new tools to your environment variables.
- If your graphical interfactes (konsole/burpsuite/brave-browser etc have issues use the Graphicalfix.bat)

#### Problems?

- Open a ticket.

### Adding Linux Binaries to Windows

The script will automatically identify the Linux binaries available in your WSL distribution and create batch scripts for each of them. These batch scripts act as wrappers, allowing you to run Linux commands from the Windows command prompt.
- It's also important to note, to use the linux python instead of windows python you will need to type in "lpython" instead of python as this is a safety measure to not interfere with python on windows.

### PATH Configuration

The script will also add the directory containing the batch scripts to your system PATH to make these commands accessible from any terminal window. If you encounter any issues, you might need to restart your terminal for the changes to take effect.

## Contributing

If you find any issues or have suggestions for improvement, please [open an issue](https://github.com/pentestfunctions/LinuxAndWindowsAsOne/issues) on the GitHub repository. We welcome contributions and pull requests from the community.


## Ideas
1. Automatically find WSL distro and let the user menu select which they want
2. Whenever apt-get or other well known installation commands are run, their respective commands will auto add/update.
3. Some piping doesn't work see below:
   ```bash
   echo "deb http://http.kali.org/kali kali-rolling main non-free contrib" | sudo tee /etc/apt/sources.list
   ```
