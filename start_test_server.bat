@echo off
REM Start server for testing
REM Use this to start server in one window, then test in another

echo.
echo ========================================
echo Starting PC Logging Server for Testing
echo ========================================
echo.
echo Keep this window open!
echo.
echo In another window, run:
echo   test_full_system.bat
echo.
echo Or test with:
echo   python test_client.py http://localhost:8080
echo.
echo ========================================
echo.

if exist pc_logging_server.exe (
    pc_logging_server.exe
) else if exist server.py (
    python server.py
) else (
    echo ERROR: Server file not found!
    pause
    exit /b 1
)

