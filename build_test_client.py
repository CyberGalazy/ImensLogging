"""
Build script to create standalone executable for the test client
Run this on a machine WITH Python installed to create the .exe
"""

import subprocess
import sys

def build_test_client():
    """Build standalone test client executable using PyInstaller"""
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("PyInstaller found")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Build the executable
    print("\nBuilding standalone test client executable...")
    print("This may take a few minutes...\n")
    
    cmd = [
        sys.executable,                 # Use Python to run PyInstaller module
        "-m", "PyInstaller",
        "--onefile",                    # Single executable file
        "--console",                    # Console application
        "--name", "test_client",        # Output name
        "--clean",                      # Clean cache
        "--noconfirm",                  # Overwrite without asking
        "test_client.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("\n" + "="*60)
        print("SUCCESS! Executable created:")
        print("  dist/test_client.exe")
        print("="*60)
        print("\nYou can now run test_client.exe on any PC (no Python needed)")
    except subprocess.CalledProcessError as e:
        print(f"\nERROR: Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_test_client()

