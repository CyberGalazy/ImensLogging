"""
PC Logging System for Gaming Zone
Tracks PC status, running software, and timestamps
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class PCLogger:
    """
    Main class for logging PC information in the gaming zone.
    Tracks which PCs are running and what software is active on each.
    """
    
    def __init__(self, log_file: str = "pc_logs.json"):
        """
        Initialize the logger with a JSON file for data storage.
        
        Args:
            log_file: Path to the JSON file where logs will be stored
        """
        self.log_file = log_file
        self.logs = self._load_logs()
    
    def _load_logs(self) -> Dict:
        """
        Load existing logs from the JSON file.
        Creates a new file with empty structure if it doesn't exist.
        
        Returns:
            Dictionary containing all logged data
        """
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                # If file is corrupted, start fresh
                return self._get_empty_structure()
        else:
            return self._get_empty_structure()
    
    def _get_empty_structure(self) -> Dict:
        """
        Returns an empty data structure for new logs.
        
        Returns:
            Empty dictionary with proper structure
        """
        return {
            "pcs": {}  # Format: {"PC_NAME": {"status": "running/offline", "software": [], "last_updated": "timestamp"}}
        }
    
    def _save_logs(self):
        """
        Save current logs to the JSON file.
        """
        with open(self.log_file, 'w') as f:
            json.dump(self.logs, f, indent=2)
    
    def _get_timestamp(self) -> str:
        """
        Get current timestamp in readable format.
        
        Returns:
            Current date and time as a string
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def log_pc_status(self, pc_name: str, status: str):
        """
        Log the status of a PC (running or offline).
        
        Args:
            pc_name: Name/ID of the PC (e.g., "PC-01", "Gaming-Rig-1")
            status: Status of the PC ("running" or "offline")
        """
        if pc_name not in self.logs["pcs"]:
            self.logs["pcs"][pc_name] = {
                "status": status,
                "software": [],
                "last_updated": self._get_timestamp()
            }
        else:
            self.logs["pcs"][pc_name]["status"] = status
            self.logs["pcs"][pc_name]["last_updated"] = self._get_timestamp()
        
        self._save_logs()
        print(f"[OK] Logged {pc_name}: {status} at {self._get_timestamp()}")
    
    def log_software(self, pc_name: str, software_list: List[str]):
        """
        Log the software currently running on a specific PC.
        
        Args:
            pc_name: Name/ID of the PC
            software_list: List of software names running on the PC
        """
        if pc_name not in self.logs["pcs"]:
            # If PC doesn't exist, create it first
            self.log_pc_status(pc_name, "running")
        
        # Update software list with timestamp
        self.logs["pcs"][pc_name]["software"] = software_list
        self.logs["pcs"][pc_name]["last_updated"] = self._get_timestamp()
        
        self._save_logs()
        print(f"[OK] Logged software on {pc_name}: {', '.join(software_list)}")
    
    def log_pc_with_software(self, pc_name: str, software_list: List[str], status: str = "running"):
        """
        Log both PC status and software in one call.
        
        Args:
            pc_name: Name/ID of the PC
            software_list: List of software names running on the PC
            status: Status of the PC (default: "running")
        """
        self.log_pc_status(pc_name, status)
        self.log_software(pc_name, software_list)
    
    def get_pc_info(self, pc_name: str) -> Optional[Dict]:
        """
        Get information about a specific PC.
        
        Args:
            pc_name: Name/ID of the PC to query
            
        Returns:
            Dictionary with PC info or None if PC doesn't exist
        """
        return self.logs["pcs"].get(pc_name)
    
    def get_all_pcs(self) -> Dict:
        """
        Get information about all logged PCs.
        
        Returns:
            Dictionary containing all PC information
        """
        return self.logs["pcs"]
    
    def get_running_pcs(self) -> List[str]:
        """
        Get list of all PCs currently marked as running.
        
        Returns:
            List of PC names that are running
        """
        return [pc_name for pc_name, info in self.logs["pcs"].items() 
                if info.get("status") == "running"]
    
    def print_summary(self):
        """
        Print a summary of all logged PCs and their status.
        """
        print("\n" + "="*50)
        print("GAMING ZONE - PC STATUS SUMMARY")
        print("="*50)
        
        if not self.logs["pcs"]:
            print("No PCs logged yet.")
            return
        
        for pc_name, info in self.logs["pcs"].items():
            status = info.get("status", "unknown")
            software = info.get("software", [])
            last_updated = info.get("last_updated", "never")
            
            print(f"\nPC: {pc_name}")
            print(f"  Status: {status.upper()}")
            print(f"  Software: {', '.join(software) if software else 'None'}")
            print(f"  Last Updated: {last_updated}")
        
        print("\n" + "="*50)


# Example usage and main function
if __name__ == "__main__":
    # Create logger instance
    logger = PCLogger()
    
    # Example: Log some PCs with their software
    print("Example logging operations:\n")
    
    # Log PC-01 with running software
    logger.log_pc_with_software(
        "PC-01",
        ["Steam", "Discord", "Chrome"]
    )
    
    # Log PC-02 with different software
    logger.log_pc_with_software(
        "PC-02",
        ["Epic Games Launcher", "Spotify", "OBS Studio"]
    )
    
    # Mark a PC as offline
    logger.log_pc_status("PC-03", "offline")
    
    # Update software on an existing PC
    logger.log_software("PC-01", ["Steam", "Counter-Strike 2", "Discord"])
    
    # Print summary of all PCs
    logger.print_summary()
    
    # Get specific PC info
    print("\nQuerying PC-01 info:")
    pc_info = logger.get_pc_info("PC-01")
    if pc_info:
        print(f"  Status: {pc_info['status']}")
        print(f"  Software: {pc_info['software']}")
    
    # Get all running PCs
    print(f"\nCurrently running PCs: {logger.get_running_pcs()}")

