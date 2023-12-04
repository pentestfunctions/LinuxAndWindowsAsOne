@echo off
setlocal enableDelayedExpansion

REM -- Set the path for the .wslgconfig file
set WSLG_CONFIG_FILE=%USERPROFILE%\.wslgconfig

REM -- Check if the .wslgconfig file exists
if not exist "%WSLG_CONFIG_FILE%" (
    echo [system-distro-env] > "%WSLG_CONFIG_FILE%"
    echo ;disable GPU in system-distro >> "%WSLG_CONFIG_FILE%"
    echo LIBGL_ALWAYS_SOFTWARE=1 >> "%WSLG_CONFIG_FILE%"
    echo .wslgconfig file created and configured.
) else (
    echo .wslgconfig file already exists. Updating file...
    echo [system-distro-env] > "%WSLG_CONFIG_FILE%"
    echo ;disable GPU in system-distro >> "%WSLG_CONFIG_FILE%"
    echo LIBGL_ALWAYS_SOFTWARE=1 >> "%WSLG_CONFIG_FILE%"
    echo .wslgconfig file updated.
)

REM -- Restart WSL
echo Restarting WSL...

REM -- Shutdown WSL
wsl --shutdown

REM -- Get all available WSL distributions and restart each
for /f "skip=1 tokens=1" %%i in ('wsl -l') do (
    set WSL_DISTRO=%%i
    echo Restarting !WSL_DISTRO!...
    wsl -d !WSL_DISTRO! -- echo Restarted !WSL_DISTRO!
)

echo All WSL distributions restarted.

endlocal
