@echo off
REM Start the PC Logging Client on a gaming PC
REM Usage: start_client.bat [SERVER_IP]
REM If SERVER_IP is not provided, reads from client_config.txt

set SERVER_IP=%1

REM If no IP provided, try to read from config file
if "%SERVER_IP%"=="" (
    if exist client_config.txt (
        for /f "tokens=2 delims==" %%a in ('findstr /i "SERVER_IP" client_config.txt') do set SERVER_IP=%%a
        set SERVER_IP=%SERVER_IP: =%
    )
)

REM Check if we have an IP
if "%SERVER_IP%"=="" (
    echo.
    echo ========================================
    echo ERROR: Server IP address required
    echo ========================================
    echo.
    echo Option 1: Pass IP as parameter
    echo   start_client.bat 192.168.1.100
    echo.
    echo Option 2: Edit client_config.txt and set SERVER_IP
    echo   Then just run: start_client.bat
    echo.
    pause
    exit /b 1
)

set SERVER_URL=http://%SERVER_IP%:8080
echo.
echo ========================================
echo PC Logging Client
echo ========================================
echo Connecting to server: %SERVER_URL%
echo Press Ctrl+C to stop
echo ========================================
echo.
python client.py %SERVER_URL%
pause

