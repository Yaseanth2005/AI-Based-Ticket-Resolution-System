import os
import sys
import subprocess

def run_app():
    # Ensure current directory is in python path
    os.environ["PYTHONPATH"] = os.getcwd()
    
    app_path = os.path.join("app", "app.py")
    
    print(f"Starting AI Support Engine from {app_path}...")
    
    # Run streamlit via python module
    cmd = [sys.executable, "-m", "streamlit", "run", app_path]
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    run_app()
