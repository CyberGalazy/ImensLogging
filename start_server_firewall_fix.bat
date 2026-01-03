@echo off
REM Start server with firewall rule check
REM Run this on the laptop

echo.
echo ========================================
echo Starting PC Logging Server
echo ========================================
echo.

REM Check if firewall rule exists
echo Checking firewall...
netsh advfirewall firewall show rule name="PC Logging Server" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Firewall rule not found!
    echo.
    echo Adding firewall rule (requires admin)...
    echo.
    REM Try to add rule (may fail if not admin)
    netsh advfirewall firewall add rule name="PC Logging Server" dir=in action=allow protocol=TCP localport=8080 >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Could not add firewall rule automatically
        echo.
        echo Please run as Administrator, or manually add:
        echo   1. Windows Firewall → Advanced Settings
        echo   2. Inbound Rules → New Rule
        echo   3. Port → TCP → 8080 → Allow
        echo.
        pause
    ) else (
        echo [OK] Firewall rule added
    )
) else (
    echo [OK] Firewall rule exists
)

echo.
echo Starting server...
echo.

REM Start server
if exist pc_logging_server.exe (
    pc_logging_server.exe
) else if exist server.py (
    python server.py
) else (
    echo ERROR: Server file not found!
    pause
    exit /b 1
)

