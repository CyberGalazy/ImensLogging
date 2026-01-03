"""
Software Detection Utility
Detects running software on Windows systems
"""

import platform
import subprocess
import socket
from typing import List


def get_pc_name() -> str:
    """
    Get the computer name.
    
    Returns:
        Computer name as string
    """
    return socket.gethostname()


def get_running_software() -> List[str]:
    """
    Detect running software/processes on Windows.
    Filters out system processes and focuses on user applications.
    
    Returns:
        List of software/application names
    """
    if platform.system() != 'Windows':
        raise NotImplementedError("Software detection currently only supports Windows")
    
    # Common system processes to exclude
    excluded_processes = {
        'svchost.exe', 'explorer.exe', 'dwm.exe', 'winlogon.exe',
        'csrss.exe', 'smss.exe', 'services.exe', 'lsass.exe',
        'spoolsv.exe', 'taskhost.exe', 'taskhostw.exe', 'conhost.exe',
        'dllhost.exe', 'audiodg.exe', 'sihost.exe', 'RuntimeBroker.exe',
        'SearchIndexer.exe', 'SearchProtocolHost.exe', 'SearchFilterHost.exe',
        'WmiPrvSE.exe', 'MsMpEng.exe', 'SecurityHealthService.exe',
        'chrome.exe', 'msedge.exe', 'firefox.exe',  # Browsers (we'll get them separately)
    }
    
    # Common application names to look for (without .exe)
    gaming_apps = {
        'steam', 'epicgameslauncher', 'origin', 'uplay', 'battlenet',
        'discord', 'teamspeak', 'mumble', 'obs64', 'obs32', 'streamlabs',
        'spotify', 'vlc', 'chrome', 'firefox', 'msedge',
        'notepad++', 'code', 'pycharm', 'intellij',
        'counter-strike', 'csgo', 'cs2', 'valorant', 'league of legends',
        'fortnite', 'apex', 'overwatch', 'minecraft', 'roblox'
    }
    
    try:
        # Get all running processes
        result = subprocess.run(
            ['tasklist', '/FO', 'CSV', '/NH'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode != 0:
            raise Exception("Failed to get process list")
        
        processes = []
        lines = result.stdout.strip().split('\n')
        
        for line in lines:
            if not line.strip():
                continue
            
            # Parse CSV format: "Image Name","PID","Session Name","Session#","Mem Usage"
            parts = line.split('","')
            if len(parts) >= 1:
                process_name = parts[0].strip('"').lower()
                
                # Skip excluded system processes
                if process_name in excluded_processes:
                    continue
                
                # Remove .exe extension and add to list
                if process_name.endswith('.exe'):
                    app_name = process_name[:-4]
                    
                    # Only include if it's a known app or looks like user software
                    # (not a random system process)
                    if (app_name in gaming_apps or 
                        len(app_name) > 2 and 
                        not app_name.startswith('dll') and
                        not app_name.startswith('ms')):
                        # Format nicely (capitalize first letter)
                        formatted_name = app_name.capitalize().replace('_', ' ')
                        if formatted_name not in processes:
                            processes.append(formatted_name)
        
        # Also try to get window titles for better detection
        try:
            window_titles = get_window_titles()
            for title in window_titles:
                # Extract app name from window title
                for app in gaming_apps:
                    if app in title.lower():
                        formatted = app.capitalize().replace('_', ' ')
                        if formatted not in processes:
                            processes.append(formatted)
        except:
            pass  # Window title detection is optional
        
        return sorted(processes) if processes else []
        
    except subprocess.TimeoutExpired:
        raise Exception("Process detection timed out")
    except Exception as e:
        raise Exception(f"Error detecting software: {e}")


def get_window_titles() -> List[str]:
    """
    Get titles of visible windows (Windows only).
    This helps identify running applications.
    
    Returns:
        List of window titles
    """
    if platform.system() != 'Windows':
        return []
    
    try:
        # Use PowerShell to get window titles
        ps_command = """
        Get-Process | Where-Object {$_.MainWindowTitle -ne ""} | 
        Select-Object -ExpandProperty MainWindowTitle
        """
        
        result = subprocess.run(
            ['powershell', '-Command', ps_command],
            capture_output=True,
            text=True,
            timeout=3
        )
        
        if result.returncode == 0:
            titles = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
            return titles
        return []
    except:
        return []


if __name__ == "__main__":
    # Test the detection
    print("PC Name:", get_pc_name())
    print("\nDetecting running software...")
    try:
        software = get_running_software()
        print(f"\nFound {len(software)} applications:")
        for app in software:
            print(f"  - {app}")
    except Exception as e:
        print(f"Error: {e}")

