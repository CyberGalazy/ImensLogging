@echo off
setlocal enabledelayedexpansion
REM Start the PC Logging Client (standalone .exe version)
REM No Python installation required!

set SERVER_IP=%1

REM If no IP provided, try to read from config file
if "!SERVER_IP!"=="" (
    if exist client_config.txt (
        for /f "tokens=2 delims==" %%a in ('findstr /i "^SERVER_IP=" client_config.txt') do (
            set SERVER_IP=%%a
        )
        REM Remove any leading/trailing spaces
        set SERVER_IP=!SERVER_IP: =!
    )
)

REM Check if we have an IP
if "!SERVER_IP!"=="" (
    echo.
    echo ========================================
    echo ERROR: Server IP address required
    echo ========================================
    echo.
    echo Option 1: Pass IP as parameter
    echo   start_client_standalone.bat 192.168.1.100
    echo.
    echo Option 2: Edit client_config.txt and set SERVER_IP
    echo   Then just run: start_client_standalone.bat
    echo.
    pause
    exit /b 1
)

set SERVER_URL=http://!SERVER_IP!:8080
echo.
echo ========================================
echo PC Logging Client (Standalone)
echo ========================================
echo Connecting to server: !SERVER_URL!
echo Press Ctrl+C to stop
echo ========================================
echo.

REM Use the standalone executable
if exist pc_logging_client.exe (
    REM Quote the URL to handle any special characters
    pc_logging_client.exe "!SERVER_URL!"
) else (
    echo ERROR: pc_logging_client.exe not found!
    echo Please build it first using: python build_client.py
    pause
    exit /b 1
)

pause

