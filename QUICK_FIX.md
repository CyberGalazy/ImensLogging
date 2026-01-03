# Quick Fix Guide - Port 8080 Closed

## Step-by-Step Solution

### Step 1: Verify Server is Running

**On your laptop**, check if server is running:

```cmd
netstat -an | findstr ":8080"
```

**You should see:**
```
TCP    0.0.0.0:8080           0.0.0.0:0              LISTENING
```

**If you DON'T see this:**
- Server is not running
- Start it: Double-click `start_server_standalone.bat`
- Keep the window open!

---

### Step 2: Add Firewall Rule (MOST IMPORTANT)

**On your laptop**, open **PowerShell as Administrator**:

1. Right-click Start button → Windows PowerShell (Admin)
2. Run this command:

```powershell
New-NetFirewallRule -DisplayName "PC Logging Server" -Direction Inbound -LocalPort 8080 -Protocol TCP -Action Allow -Profile Any
```

3. Verify it worked:

```powershell
Get-NetFirewallRule -DisplayName "PC Logging Server"
```

**You should see the rule listed.**

---

### Step 3: Test Locally

**On your laptop**, open browser and go to:
```
http://localhost:8080/status
```

**You should see:**
```json
{"status": "running", "message": "PC Logging Server is active"}
```

**If this works**, server is running correctly!

---

### Step 4: Test from Gaming PC

**On gaming PC**, run:
```cmd
test_connection.bat
```

Or try:
```cmd
ping [LAPTOP_IP]
```

Then test the port:
```powershell
Test-NetConnection -ComputerName [LAPTOP_IP] -Port 8080
```

---

## Still Not Working?

### Option A: Temporarily Disable Firewall (Testing Only)

**On laptop**, temporarily disable firewall to test:
1. Windows Security → Firewall & network protection
2. Turn off firewall for Private network (temporarily!)
3. Test connection
4. **Turn it back on** and add proper rule

### Option B: Use Different Port

If port 8080 is blocked, use port 9000:

**On laptop**, edit `server.py` line 134:
```python
def __init__(self, host='0.0.0.0', port=9000, log_file='pc_logs.json'):
```

Or run:
```cmd
python server.py 0.0.0.0 9000
```

**On gaming PC**, update `client_config.txt`:
```
SERVER_IP=192.168.56.1:9000
```

### Option C: Check Antivirus

Some antivirus software has its own firewall:
- Check antivirus firewall settings
- Add exception for the server executable
- Or temporarily disable to test

---

## Manual Commands (Copy/Paste)

**Check if server running:**
```cmd
netstat -an | findstr ":8080"
```

**Add firewall rule (PowerShell as Admin):**
```powershell
New-NetFirewallRule -DisplayName "PC Logging Server" -Direction Inbound -LocalPort 8080 -Protocol TCP -Action Allow -Profile Any
```

**Test local connection:**
```powershell
Invoke-WebRequest -Uri http://localhost:8080/status
```

**Test from gaming PC:**
```powershell
Test-NetConnection -ComputerName 192.168.56.1 -Port 8080
```

