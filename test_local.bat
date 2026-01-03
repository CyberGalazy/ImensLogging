@echo off
REM Test the entire system locally on your laptop
REM This simulates both server and client on the same machine

echo.
echo ========================================
echo LOCAL SYSTEM TEST
echo ========================================
echo.
echo This will test server and client on your laptop
echo Make sure server is running first!
echo.
pause

echo.
echo [1/3] Testing server locally...
python test_client.py http://localhost:8080
if errorlevel 1 (
    echo.
    echo ERROR: Server test failed!
    echo Make sure server is running: start_server_standalone.bat
    pause
    exit /b 1
)

echo.
echo [2/3] Testing client connection...
echo Starting client in test mode...
python client.py http://localhost:8080 --once
if errorlevel 1 (
    echo.
    echo ERROR: Client test failed!
) else (
    echo.
    echo SUCCESS: Client connected!
)

echo.
echo [3/3] Viewing logs...
if exist pc_logs.json (
    echo.
    echo Current logs:
    python -c "import json; data=json.load(open('pc_logs.json')); [print(f\"  {k}: {v['status']} - {len(v.get('software', []))} apps\") for k,v in data.get('pcs', {}).items()]"
) else (
    echo No logs file found yet
)

echo.
echo ========================================
echo Test Complete!
echo ========================================
echo.
echo If all tests passed, your system is working!
echo You can now deploy to gaming PCs.
echo.
pause

