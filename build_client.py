"""
Build script to create standalone executable for the client
Run this on a machine WITH Python installed to create the .exe
"""

import subprocess
import sys
import os

def build_client():
    """Build standalone client executable using PyInstaller"""
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("PyInstaller found")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Build the executable
    print("\nBuilding standalone client executable...")
    print("This may take a few minutes...\n")
    
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single executable file
        "--console",                    # Console application
        "--name", "pc_logging_client",  # Output name
        "--clean",                      # Clean cache
        "--noconfirm",                  # Overwrite without asking
        "client.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("\n" + "="*60)
        print("SUCCESS! Executable created:")
        print("  dist/pc_logging_client.exe")
        print("="*60)
        print("\nCopy this file to your gaming PCs along with:")
        print("  - client_config.txt")
        print("  - start_client.bat (updated to use .exe)")
        print("\nNo Python installation needed on client PCs!")
    except subprocess.CalledProcessError as e:
        print(f"\nERROR: Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_client()

