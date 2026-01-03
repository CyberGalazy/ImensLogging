@echo off
REM Test connection to the logging server
REM Usage: test_connection.bat [SERVER_IP]

setlocal enabledelayedexpansion

set SERVER_IP=%1

REM If no IP provided, try to read from config file
if "!SERVER_IP!"=="" (
    if exist client_config.txt (
        for /f "tokens=2 delims==" %%a in ('findstr /i "^SERVER_IP=" client_config.txt') do (
            set SERVER_IP=%%a
        )
        set SERVER_IP=!SERVER_IP: =!
    )
)

if "!SERVER_IP!"=="" (
    echo ERROR: Server IP address required
    echo Usage: test_connection.bat [SERVER_IP]
    pause
    exit /b 1
)

set SERVER_URL=http://!SERVER_IP!:8080

echo.
echo ========================================
echo Connection Test
echo ========================================
echo Testing connection to: !SERVER_URL!
echo.

REM Test 1: Ping
echo [1/3] Testing network connectivity (ping)...
ping -n 1 !SERVER_IP! >nul 2>&1
if errorlevel 1 (
    echo   [FAIL] Cannot ping server - check network connection
) else (
    echo   [OK] Network connection works
)

REM Test 2: Port check (using PowerShell)
echo.
echo [2/3] Testing port 8080...
powershell -Command "$result = Test-NetConnection -ComputerName !SERVER_IP! -Port 8080 -WarningAction SilentlyContinue; if ($result.TcpTestSucceeded) { Write-Host '  [OK] Port 8080 is open' } else { Write-Host '  [FAIL] Port 8080 is closed or blocked by firewall' }"

REM Test 3: HTTP connection
echo.
echo [3/3] Testing HTTP connection...
if exist pc_logging_client.exe (
    pc_logging_client.exe "!SERVER_URL!" --once
) else if exist client.py (
    python client.py "!SERVER_URL!" --once
) else (
    echo   [SKIP] Client executable/script not found
)

echo.
echo ========================================
echo Troubleshooting Tips:
echo ========================================
echo 1. Make sure server is running on laptop
echo 2. Check Windows Firewall allows port 8080
echo 3. Verify both PCs are on same network
echo 4. Try: ping !SERVER_IP!
echo ========================================
echo.
pause

