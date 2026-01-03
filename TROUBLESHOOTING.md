# Troubleshooting Guide

## "Connection Refused" Error

This error means the client cannot connect to the server. Follow these steps:

### Step 1: Verify Server is Running

**On your laptop:**
1. Check if the server window is open and shows:
   ```
   Server running on http://0.0.0.0:8080
   Waiting for logs from gaming zone PCs...
   ```

2. If not running, start it:
   - Double-click `start_server_standalone.bat` (or `start_server.bat` if using Python)

### Step 2: Check IP Address

**On your laptop:**
1. Open Command Prompt
2. Run: `ipconfig`
3. Look for "IPv4 Address" under your active network adapter
4. Note the IP (e.g., `192.168.56.1`)

**On gaming PC:**
1. Make sure `client_config.txt` has the correct IP:
   ```
   SERVER_IP=192.168.56.1
   ```
   (Replace with your laptop's actual IP)

### Step 3: Test Network Connectivity

**On gaming PC:**
1. Open Command Prompt
2. Run: `ping 192.168.56.1` (use your laptop's IP)
3. If ping fails:
   - Check both PCs are on same network
   - Check network cables/WiFi
   - Try disabling VPN if active

### Step 4: Check Windows Firewall

**On your laptop (where server runs):**

1. Open Windows Defender Firewall
2. Click "Advanced settings"
3. Click "Inbound Rules" → "New Rule"
4. Select "Port" → Next
5. Select "TCP" and enter port `8080` → Next
6. Select "Allow the connection" → Next
7. Check all profiles (Domain, Private, Public) → Next
8. Name it "PC Logging Server" → Finish

**Or use PowerShell (Run as Administrator):**
```powershell
New-NetFirewallRule -DisplayName "PC Logging Server" -Direction Inbound -LocalPort 8080 -Protocol TCP -Action Allow
```

### Step 5: Test Connection

**On gaming PC:**
1. Run the test script:
   ```
   test_connection.bat
   ```
   
   Or manually test:
   ```
   ping 192.168.56.1
   ```

### Step 6: Verify Port is Open

**On laptop, test if server is listening:**
```powershell
netstat -an | findstr 8080
```

You should see:
```
TCP    0.0.0.0:8080           0.0.0.0:0              LISTENING
```

**On gaming PC, test if port is reachable:**
```powershell
Test-NetConnection -ComputerName 192.168.56.1 -Port 8080
```

Should show: `TcpTestSucceeded : True`

## Common Issues

### Issue: "Address already in use"
**Solution:** Another program is using port 8080
- Change server port: Edit `server.py` or use `python server.py 0.0.0.0 9000`
- Or find and stop the conflicting program

### Issue: "Connection timeout"
**Solution:** 
- Firewall is blocking (see Step 4)
- Wrong IP address (see Step 2)
- Server not running (see Step 1)

### Issue: "Name or service not known"
**Solution:**
- Check IP address format (should be like `192.168.1.100`, not a hostname)
- Make sure you're using IP, not computer name

### Issue: Server shows "Connection refused" in logs
**Solution:**
- Server is running but can't accept connections
- Check firewall rules
- Try binding to specific IP: `python server.py 192.168.56.1 8080`

## Quick Diagnostic Commands

**On Laptop (Server):**
```bash
# Check if server is listening
netstat -an | findstr 8080

# Check firewall rules
netsh advfirewall firewall show rule name="PC Logging Server"
```

**On Gaming PC (Client):**
```bash
# Test network
ping [LAPTOP_IP]

# Test port
Test-NetConnection -ComputerName [LAPTOP_IP] -Port 8080

# Test HTTP connection
curl http://[LAPTOP_IP]:8080/status
```

## Still Not Working?

1. **Check both PCs are on same network:**
   - Same WiFi network, or
   - Same physical network (wired)

2. **Try disabling firewall temporarily** (for testing only):
   - If it works, firewall is the issue - add proper rule

3. **Check antivirus software:**
   - Some antivirus may block connections
   - Add exception for the server executable

4. **Verify server IP binding:**
   - Server should bind to `0.0.0.0` (all interfaces)
   - Or bind to your specific network adapter IP

5. **Check router settings:**
   - Some routers block inter-device communication
   - Check AP isolation / client isolation settings

