@echo off
echo.
echo ========================================
echo Server Fix - Restart Required
echo ========================================
echo.

echo [1] Finding server process...
for /f "tokens=2" %%a in ('netstat -ano ^| findstr ":8080" ^| findstr "LISTENING"') do (
    echo   Found process using port 8080: PID %%a
    echo   Killing process...
    taskkill /PID %%a /F >nul 2>&1
    if errorlevel 1 (
        echo   [WARNING] Could not kill process - may need admin rights
        echo   Please close server window manually
    ) else (
        echo   [OK] Process killed
    )
)

echo.
echo [2] Waiting 2 seconds...
timeout /t 2 /nobreak >nul

echo.
echo [3] Checking port is free...
netstat -an | findstr ":8080" | findstr "LISTENING"
if errorlevel 1 (
    echo   [OK] Port 8080 is now free
    echo.
    echo ========================================
    echo Next Steps:
    echo ========================================
    echo 1. Start server: start_server_standalone.bat
    echo 2. Wait for "Server running" message
    echo 3. Test: test_server_manual.bat
    echo ========================================
) else (
    echo   [FAIL] Port still in use
    echo   Please close server window manually
)

echo.
pause

