@echo off
echo.
echo ========================================
echo Manual Server Test
echo ========================================
echo.

echo Testing server with different methods...
echo.

echo [Method 1] PowerShell WebRequest:
powershell -Command "try { $r = Invoke-WebRequest -Uri 'http://localhost:8080/status' -UseBasicParsing; Write-Host 'SUCCESS:' $r.StatusCode; Write-Host $r.Content } catch { Write-Host 'ERROR:' $_.Exception.Message }"

echo.
echo [Method 2] PowerShell Test-NetConnection:
powershell -Command "Test-NetConnection -ComputerName localhost -Port 8080"

echo.
echo [Method 3] Check server process:
tasklist | findstr /i "pc_logging_server python"

echo.
echo [Method 4] Check what's using port 8080:
netstat -ano | findstr ":8080"

echo.
echo ========================================
echo If server not responding:
echo ========================================
echo 1. Stop the server (Ctrl+C in server window)
echo 2. Restart: start_server_standalone.bat
echo 3. Check for error messages in server window
echo ========================================
pause

