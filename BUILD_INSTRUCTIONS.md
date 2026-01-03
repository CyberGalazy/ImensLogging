# Building Standalone Executables

This guide explains how to create standalone `.exe` files that don't require Python installation on client machines.

## Prerequisites

- Python 3.6+ installed on your laptop (where you'll build)
- Internet connection (to download PyInstaller)

## Building the Executables

### Step 1: Build Client Executable

Run this on your laptop:

```bash
python build_client.py
```

This will:
1. Install PyInstaller if needed
2. Create `dist/pc_logging_client.exe`
3. Bundle Python and all dependencies into a single .exe file

### Step 2: Build Server Executable

```bash
python build_server.py
```

This creates `dist/pc_logging_server.exe`

## Deploying to Gaming PCs

### For Each Gaming PC:

1. **Copy these files:**
   - `pc_logging_client.exe` (from `dist/` folder)
   - `client_config.txt`
   - `start_client_standalone.bat`

2. **Edit `client_config.txt`:**
   ```
   SERVER_IP=192.168.56.1
   ```
   (Replace with your laptop's actual IP)

3. **Double-click `start_client_standalone.bat`**

That's it! No Python installation needed.

## Deploying Server to Your Laptop

1. **Copy these files:**
   - `pc_logging_server.exe` (from `dist/` folder)
   - `start_server_standalone.bat`

2. **Double-click `start_server_standalone.bat`**

## File Sizes

- `pc_logging_client.exe`: ~8-12 MB
- `pc_logging_server.exe`: ~8-12 MB

These are larger because they include Python runtime, but they're completely standalone.

## Troubleshooting

**"PyInstaller not found"**
- The build script will install it automatically
- Or manually: `pip install pyinstaller`

**"Antivirus warning"**
- Some antivirus software flags PyInstaller executables
- This is a false positive - add to exclusions if needed

**"Executable not working"**
- Make sure you're building on Windows
- Try building with: `pyinstaller --onefile --console client.py`

