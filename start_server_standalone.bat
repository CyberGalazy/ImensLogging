@echo off
REM Start the PC Logging Server (standalone .exe version)
REM No Python installation required!

echo.
echo ========================================
echo PC Logging Server (Standalone)
echo ========================================
echo.

REM Use the standalone executable
if exist pc_logging_server.exe (
    pc_logging_server.exe
) else (
    echo ERROR: pc_logging_server.exe not found!
    echo Please build it first using: python build_server.py
    pause
    exit /b 1
)

pause

