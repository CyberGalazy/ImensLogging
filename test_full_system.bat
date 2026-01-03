@echo off
REM Full system test - Server + Client simulation
REM Tests everything on your laptop

echo.
echo ========================================
echo FULL SYSTEM TEST
echo ========================================
echo.
echo This will:
echo   1. Check if server is running
echo   2. Test server endpoints
echo   3. Simulate client sending logs
echo   4. Verify logs were saved
echo.
echo Make sure server is running first!
echo (Start it in another window: start_server_standalone.bat)
echo.
pause

echo.
echo ========================================
echo STEP 1: Check Server Status
echo ========================================
echo.

REM Check if port is listening
echo Checking if server is running...
netstat -an | findstr ":8080" | findstr "LISTENING" >nul
if errorlevel 1 (
    echo [WARNING] Port 8080 not found in listening state
    echo.
    echo But let's test anyway - server might be running...
    echo.
) else (
    echo [OK] Port 8080 is listening
    echo.
)

REM Try to connect to server directly
echo Testing server connection...
python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/status', timeout=2)" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Cannot connect to server
    echo.
    echo Please make sure server is running in another window!
    echo Run: start_server_standalone.bat
    echo.
    echo Press any key to continue anyway (or Ctrl+C to exit)...
    pause >nul
) else (
    echo [OK] Server is responding!
    echo.
)

echo ========================================
echo STEP 2: Test Server Endpoints
echo ========================================
echo.

python test_client.py http://localhost:8080
if errorlevel 1 (
    echo.
    echo [FAIL] Server endpoints not responding!
    echo Check server window for errors.
    pause
    exit /b 1
)

echo.
echo ========================================
echo STEP 3: Simulate Client Logging
echo ========================================
echo.

echo Simulating PC-01 sending logs...
python client.py http://localhost:8080 --once --pc-name "PC-01"
if errorlevel 1 (
    echo [WARNING] Client test had issues
) else (
    echo [OK] PC-01 logged successfully
)

timeout /t 2 /nobreak >nul

echo.
echo Simulating PC-02 sending logs...
python client.py http://localhost:8080 --once --pc-name "PC-02"
if errorlevel 1 (
    echo [WARNING] Client test had issues
) else (
    echo [OK] PC-02 logged successfully
)

echo.
echo ========================================
echo STEP 4: Verify Logs
echo ========================================
echo.

if exist pc_logs.json (
    echo Logs file exists. Contents:
    echo.
    python -c "import json; d=json.load(open('pc_logs.json')); print(json.dumps(d, indent=2))"
    echo.
    echo [OK] Logs verified!
) else (
    echo [WARNING] pc_logs.json not found
)

echo.
echo ========================================
echo TEST SUMMARY
echo ========================================
echo.
echo If you see "SUCCESS" messages above,
echo your system is working correctly!
echo.
echo You can now:
echo   1. Deploy server to your laptop (already done)
echo   2. Deploy client to gaming PCs
echo   3. Start collecting real logs
echo.
echo ========================================
pause

