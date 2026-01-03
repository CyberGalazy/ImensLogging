# Gaming Zone PC Logging System

A distributed logging system to track PC status, running software, and timestamps for your gaming zone. Features a central server (runs on your laptop) that collects logs from client agents running on each gaming PC.

## Features

- **Track PC Status**: Log which PCs are running or offline
- **Track Software**: Automatically detect and record what software is running on each PC
- **Time Tracking**: Automatically timestamps all log entries
- **Centralized Monitoring**: All logs collected on your laptop via HTTP server
- **Auto-Detection**: Clients automatically detect running software
- **Simple Storage**: Data stored in JSON format for easy access
- **Easy Queries**: Get info about specific PCs or all PCs via API

## Requirements

**For Building (your laptop with Python):**
- Python 3.6 or higher
- PyInstaller (installed automatically by build scripts)

**For Running (gaming PCs - NO Python needed!):**
- Windows OS (for automatic software detection)
- Standalone executables (built once, then no Python needed)
- All PCs must be on the same network

## Deployment Architecture

```
┌─────────────┐
│   Laptop    │  ← Server (collects all logs)
│  (Server)   │
└──────┬──────┘
       │ HTTP (port 8080)
       │
   ┌───┴───┬──────────┬──────────┐
   │       │          │          │
┌──▼──┐ ┌──▼──┐   ┌──▼──┐   ┌──▼──┐
│PC-01│ │PC-02│   │PC-03│   │PC-04│  ← Clients (send logs)
└─────┘ └─────┘   └─────┘   └─────┘
```

## Quick Start - Deployment Guide

### Option A: Standalone Executables (Recommended - No Python on Clients!)

**Build once on your laptop (with Python), then deploy .exe files:**

1. **Build the executables:**
   ```bash
   # Build client executable
   python build_client.py
   
   # Build server executable  
   python build_server.py
   ```
   
   This creates:
   - `dist/pc_logging_client.exe` - Copy to each gaming PC
   - `dist/pc_logging_server.exe` - Use on your laptop

2. **Deploy to gaming PCs:**
   - Copy `pc_logging_client.exe` to each gaming PC
   - Copy `client_config.txt` to each gaming PC
   - Copy `start_client_standalone.bat` to each gaming PC
   - Edit `client_config.txt` with your laptop's IP

3. **Run:**
   - **Laptop:** Double-click `start_server_standalone.bat` (or run `pc_logging_server.exe`)
   - **Gaming PCs:** Double-click `start_client_standalone.bat` (or run `pc_logging_client.exe`)

**No Python installation needed on gaming PCs!**

---

### Option B: Python Installation Required

If you prefer to run Python scripts directly:

### Step 1: Setup Server on Your Laptop

1. **Find your laptop's IP address:**
   ```powershell
   ipconfig
   ```
   Look for "IPv4 Address" (e.g., `192.168.1.100`)

2. **Start the server:**
   ```bash
   # Option 1: Use the batch file
   start_server.bat
   
   # Option 2: Run directly
   python server.py
   ```
   
   The server will start on port 8080 and display:
   ```
   Server running on http://0.0.0.0:8080
   Waiting for logs from gaming zone PCs...
   ```

3. **Keep the server running** - it will collect logs from all clients.

### Step 2: Deploy Clients to Gaming PCs

For each gaming PC:

1. **Copy the entire project folder** to the gaming PC (or clone from your repo)

2. **Start the client:**
   ```bash
   # Option 1: Use the batch file (replace with your laptop's IP)
   start_client.bat 192.168.1.100
   
   # Option 2: Run directly
   python client.py http://192.168.1.100:8080
   ```

3. **The client will:**
   - Auto-detect the PC name
   - Auto-detect running software every 30 seconds
   - Send updates to your laptop server
   - Run continuously until stopped (Ctrl+C)

### Step 3: View Logs

**Option A: View in JSON file**
- Logs are saved in `pc_logs.json` on your laptop
- Open with any text editor or JSON viewer

**Option B: View via API**
- Open browser: `http://localhost:8080/logs`
- Or use: `http://YOUR_LAPTOP_IP:8080/logs`

**Option C: Use the logger programmatically**
```python
from pc_logger import PCLogger

logger = PCLogger()
logger.print_summary()  # Print formatted summary
```

## Advanced Usage

### Server Options

```bash
# Custom host and port
python server.py 0.0.0.0 9000

# Custom log file location
# Edit server.py to change log_file parameter
```

### Client Options

```bash
# Custom PC name
python client.py http://192.168.1.100:8080 --pc-name "Gaming-Rig-1"

# Custom update interval (seconds)
python client.py http://192.168.1.100:8080 --interval 60

# Send one update and exit (for testing)
python client.py http://192.168.1.100:8080 --once
```

### API Endpoints

The server provides REST API endpoints:

- `GET /status` - Check if server is running
- `GET /logs` - Get all logs (JSON)
- `GET /pc/<pc_name>` - Get specific PC info
- `POST /log` - Send log data (used by clients)

### Running as Windows Service (Optional)

To run clients automatically on startup:

1. Create a scheduled task in Windows Task Scheduler
2. Set trigger: "At startup" or "At log on"
3. Action: Run `start_client.bat <SERVER_IP>`
4. Set "Run whether user is logged on or not"

## Local Usage (Standalone)

You can still use the logger locally without the server/client setup:

```python
from pc_logger import PCLogger

# Create a logger instance
logger = PCLogger()

# Log a PC with its running software
logger.log_pc_with_software("PC-01", ["Steam", "Discord", "Chrome"])

# Mark a PC as offline
logger.log_pc_status("PC-02", "offline")

# Update software on a PC
logger.log_software("PC-01", ["Steam", "Counter-Strike 2", "Discord"])

# View summary of all PCs
logger.print_summary()

# Get info about a specific PC
pc_info = logger.get_pc_info("PC-01")
print(pc_info)

# Get list of all running PCs
running_pcs = logger.get_running_pcs()
print(running_pcs)
```

## Data Storage

All logs are stored in `pc_logs.json` in the same directory. The file structure looks like:

```json
{
  "pcs": {
    "PC-01": {
      "status": "running",
      "software": ["Steam", "Discord", "Chrome"],
      "last_updated": "2024-01-15 14:30:00"
    }
  }
}
```

## Methods

- `log_pc_status(pc_name, status)` - Log PC status (running/offline)
- `log_software(pc_name, software_list)` - Log software running on a PC
- `log_pc_with_software(pc_name, software_list, status)` - Log both at once
- `get_pc_info(pc_name)` - Get information about a specific PC
- `get_all_pcs()` - Get all PC information
- `get_running_pcs()` - Get list of running PC names
- `print_summary()` - Print formatted summary of all PCs

## Troubleshooting

### Server Issues

**"Address already in use"**
- Another program is using port 8080
- Change port: `python server.py 0.0.0.0 9000`
- Or stop the conflicting program

**Clients can't connect**
- Check Windows Firewall allows port 8080
- Verify laptop and gaming PCs are on same network
- Ping the laptop IP from gaming PC: `ping 192.168.1.100`
- Check server is actually running

### Client Issues

**"Could not connect to server"**
- Verify server IP address is correct
- Check server is running
- Test connection: `python client.py http://SERVER_IP:8080 --once`

**Software detection not working**
- Make sure you're on Windows
- Some software may not be detected if it's not in the detection list
- Check `detect_software.py` to add custom software names

**PC name detection**
- Client uses computer hostname by default
- Override with: `--pc-name "Custom-Name"`

## File Structure

```
ImensLogging/
├── pc_logger.py              # Core logging class
├── server.py                 # HTTP server (runs on laptop)
├── client.py                 # Client agent (runs on gaming PCs)
├── detect_software.py        # Software detection utility
├── build_client.py           # Build standalone client .exe
├── build_server.py           # Build standalone server .exe
├── start_server.bat          # Quick start server (Python)
├── start_client.bat          # Quick start client (Python)
├── start_server_standalone.bat  # Quick start server (.exe)
├── start_client_standalone.bat  # Quick start client (.exe)
├── client_config.txt         # Client configuration (server IP)
├── pc_logs.json             # Log data (created automatically)
└── README.md                # This file
```

## Notes

- PC names are case-sensitive
- Software lists are replaced (not appended) when updated
- All timestamps are automatically generated
- Data is saved immediately after each logging operation
- Clients send updates every 30 seconds by default
- Server must be running before clients can connect
- All communication is over HTTP (port 8080 by default)



