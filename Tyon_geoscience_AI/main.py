# main.py
import subprocess
import sys

def main():
    """Entry point for the application"""
    print("Tyon Geoscience AI - Choose an option:")
    print("1. Run Dashboard")
    print("2. Run Command Line Analysis")
    
    choice = input("Enter choice (1-2): ")
    
    if choice == "1":
        subprocess.run(["streamlit", "run", "dashboard/dashboard_app.py"])
    elif choice == "2":
        print("Command line analysis not implemented yet")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
