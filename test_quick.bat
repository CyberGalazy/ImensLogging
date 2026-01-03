@echo off
REM Quick test - just test the connection, don't check if server is running first

echo.
echo ========================================
echo QUICK SERVER TEST
echo ========================================
echo.
echo Testing server connection...
echo (Make sure server is running in another window)
echo.

python test_client.py http://localhost:8080

if errorlevel 1 (
    echo.
    echo ========================================
    echo TEST FAILED
    echo ========================================
    echo.
    echo Make sure:
    echo   1. Server is running (start_server_standalone.bat)
    echo   2. Server window shows "Server running on http://0.0.0.0:8080"
    echo.
) else (
    echo.
    echo ========================================
    echo TEST PASSED!
    echo ========================================
    echo.
    echo Your server is working correctly!
    echo.
)

echo.
pause

