@echo off
REM Add Windows Firewall rule for PC Logging Server
REM Must be run as Administrator!

echo.
echo ========================================
echo Adding Firewall Rule for Port 8080
echo ========================================
echo.

REM Check if running as admin
net session >nul 2>&1
if errorlevel 1 (
    echo ERROR: This script must be run as Administrator!
    echo.
    echo Right-click this file and select "Run as administrator"
    pause
    exit /b 1
)

echo Adding firewall rule...
netsh advfirewall firewall add rule name="PC Logging Server" dir=in action=allow protocol=TCP localport=8080

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to add firewall rule
    echo Try adding it manually through Windows Firewall settings
) else (
    echo.
    echo [SUCCESS] Firewall rule added!
    echo Port 8080 is now open for incoming connections
)

echo.
pause

