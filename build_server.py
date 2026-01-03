"""
Build script to create standalone executable for the server
Run this on a machine WITH Python installed to create the .exe
"""

import subprocess
import sys

def build_server():
    """Build standalone server executable using PyInstaller"""
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("PyInstaller found")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Build the executable
    print("\nBuilding standalone server executable...")
    print("This may take a few minutes...\n")
    
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single executable file
        "--console",                    # Console application
        "--name", "pc_logging_server",  # Output name
        "--clean",                      # Clean cache
        "--noconfirm",                  # Overwrite without asking
        "server.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("\n" + "="*60)
        print("SUCCESS! Executable created:")
        print("  dist/pc_logging_server.exe")
        print("="*60)
        print("\nCopy this file to your laptop.")
        print("No Python installation needed!")
    except subprocess.CalledProcessError as e:
        print(f"\nERROR: Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_server()

