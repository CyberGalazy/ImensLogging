@echo off
REM Test client - Test server connection
REM Usage: test_client.bat [SERVER_URL]

setlocal enabledelayedexpansion

set SERVER_URL=%1

REM If no URL provided, try to read from config file
if "!SERVER_URL!"=="" (
    set SERVER_IP=
    if exist client_config.txt (
        for /f "tokens=2 delims==" %%a in ('findstr /i "^SERVER_IP=" client_config.txt') do (
            set SERVER_IP=%%a
        )
        set SERVER_IP=!SERVER_IP: =!
    )
    
    if "!SERVER_IP!"=="" (
        echo.
        echo ERROR: Server URL or IP required
        echo.
        echo Usage: test_client.bat [SERVER_URL]
        echo Example: test_client.bat http://192.168.56.1:8080
        echo.
        echo Or set SERVER_IP in client_config.txt
        pause
        exit /b 1
    )
    
    set SERVER_URL=http://!SERVER_IP!:8080
)

echo.
echo Testing server: !SERVER_URL!
echo.

REM Run test client
if exist test_client.exe (
    test_client.exe "!SERVER_URL!"
) else if exist test_client.py (
    python test_client.py "!SERVER_URL!"
) else (
    echo ERROR: test_client.py not found!
    pause
    exit /b 1
)

echo.
pause

