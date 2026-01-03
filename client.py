"""
PC Logging Client
Runs on each gaming PC to send status and software info to the server
"""

import json
import socket
import time
import sys
from typing import List, Optional
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

from detect_software import get_running_software, get_pc_name


class LoggingClient:
    """Client that sends PC information to the logging server"""
    
    def __init__(self, server_url: str, pc_name: Optional[str] = None, interval: int = 30):
        """
        Initialize the logging client.
        
        Args:
            server_url: URL of the logging server (e.g., "http://192.168.1.100:8080")
            pc_name: Name of this PC (auto-detected if not provided)
            interval: How often to send updates in seconds (default: 30)
        """
        self.server_url = server_url.rstrip('/')
        self.pc_name = pc_name or get_pc_name()
        self.interval = interval
        self.running = False
    
    def send_log(self, status: str = "running", software: Optional[List[str]] = None) -> bool:
        """
        Send log data to the server.
        
        Args:
            status: PC status ("running" or "offline")
            software: List of running software (auto-detected if None)
            
        Returns:
            True if successful, False otherwise
        """
        if software is None:
            try:
                software = get_running_software()
            except Exception as e:
                print(f"[WARNING] Could not detect software: {e}")
                software = []
        
        data = {
            "pc_name": self.pc_name,
            "status": status,
            "software": software
        }
        
        try:
            request = Request(
                f"{self.server_url}/log",
                data=json.dumps(data).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            
            response = urlopen(request, timeout=5)
            result = json.loads(response.read().decode('utf-8'))
            
            if result.get('status') == 'success':
                print(f"[OK] Sent log for {self.pc_name}: {len(software)} apps detected")
                return True
            else:
                print(f"[ERROR] Server returned: {result.get('message', 'Unknown error')}")
                return False
                
        except URLError as e:
            error_msg = str(e)
            if "refused" in error_msg.lower() or "10061" in error_msg:
                print(f"[ERROR] Connection refused to {self.server_url}")
                print(f"       → Server may not be running")
                print(f"       → Firewall may be blocking port 8080")
                print(f"       → Check IP address is correct")
            else:
                print(f"[ERROR] Could not connect to server at {self.server_url}: {e}")
            return False
        except HTTPError as e:
            print(f"[ERROR] Server error: {e.code} - {e.reason}")
            return False
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
            return False
    
    def test_connection(self) -> bool:
        """Test if server is reachable"""
        try:
            request = Request(f"{self.server_url}/status", method='GET')
            response = urlopen(request, timeout=5)
            result = json.loads(response.read().decode('utf-8'))
            if result.get('status') == 'running':
                print(f"[OK] Server connection successful!")
                return True
            return False
        except URLError as e:
            error_msg = str(e)
            if "refused" in error_msg.lower() or "10061" in error_msg:
                print(f"[ERROR] Connection refused - Server not running or firewall blocking")
                print(f"       Troubleshooting:")
                print(f"       1. Make sure server is running on laptop")
                print(f"       2. Check Windows Firewall allows port 8080")
                print(f"       3. Verify IP address: {self.server_url}")
                print(f"       4. Test with: ping {self.server_url.split('://')[1].split(':')[0]}")
            else:
                print(f"[ERROR] Cannot reach server: {e}")
            return False
        except Exception as e:
            print(f"[ERROR] Cannot reach server: {e}")
            return False
    
    def run_continuous(self):
        """Run continuously, sending logs at regular intervals"""
        print("="*60)
        print("PC LOGGING CLIENT")
        print("="*60)
        print(f"PC Name: {self.pc_name}")
        print(f"Server: {self.server_url}")
        print(f"Update Interval: {self.interval} seconds")
        print("="*60)
        print()
        
        # Test connection first
        if not self.test_connection():
            print("WARNING: Cannot connect to server. Will retry on next update.")
            print()
        
        self.running = True
        
        try:
            while self.running:
                self.send_log()
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print("\n\nShutting down client...")
            # Send offline status before exiting
            self.send_log(status="offline")
            print("Client stopped.")
    
    def send_once(self):
        """Send a single log update"""
        return self.send_log()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='PC Logging Client')
    parser.add_argument('server_url', help='Server URL (e.g., http://192.168.1.100:8080)')
    parser.add_argument('--pc-name', help='PC name (auto-detected if not provided)')
    parser.add_argument('--interval', type=int, default=30, 
                       help='Update interval in seconds (default: 30)')
    parser.add_argument('--once', action='store_true', 
                       help='Send one update and exit (default: continuous)')
    
    args = parser.parse_args()
    
    client = LoggingClient(
        server_url=args.server_url,
        pc_name=args.pc_name,
        interval=args.interval
    )
    
    if args.once:
        client.send_once()
    else:
        client.run_continuous()

