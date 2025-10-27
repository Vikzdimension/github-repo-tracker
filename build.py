#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and handle errors"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd)
    if result.returncode != 0:
        print(f"Error running: {cmd}")
        sys.exit(1)

def main():
    # Get project root
    project_root = Path(__file__).parent
    backend_dir = project_root / "backend"
    frontend_dir = project_root / "backend" / "frontend" / "admin-dashboard"
    
    print("Building React app...")
    run_command("npm run build", cwd=frontend_dir)
    
    print("Running migrations...")
    run_command("python manage.py migrate", cwd=backend_dir)
    
    print("Collecting static files...")
    run_command("python manage.py collectstatic --noinput", cwd=backend_dir)
    
    print("Build complete!")
    print("Start server with: python manage.py runserver")

if __name__ == "__main__":
    main()