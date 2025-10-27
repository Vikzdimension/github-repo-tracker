#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, cwd=None, check_env=True):
    """Run a command and handle errors"""
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd, 
            check=True,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running: {cmd}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        sys.exit(1)

def check_environment():
    """Check if required environment variables are set"""
    # Load .env file from backend directory
    from dotenv import load_dotenv
    backend_dir = Path(__file__).parent / "backend"
    env_file = backend_dir / ".env"
    
    if env_file.exists():
        load_dotenv(env_file)
    
    required_vars = ['DJANGO_SECRET_KEY', 'DATABASE_URL']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Missing required environment variables: {', '.join(missing_vars)}")
        print(f"Please check your .env file at: {env_file}")
        return False
    return True

def main():
    # Get project root
    project_root = Path(__file__).parent
    backend_dir = project_root / "backend"
    frontend_dir = project_root / "backend" / "frontend" / "admin-dashboard"
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Check if directories exist
    if not frontend_dir.exists():
        print(f"Frontend directory not found: {frontend_dir}")
        sys.exit(1)
    
    if not backend_dir.exists():
        print(f"Backend directory not found: {backend_dir}")
        sys.exit(1)
    
    print("Installing frontend dependencies...")
    run_command("npm ci", cwd=frontend_dir)
    
    print("Building React app...")
    run_command("npm run build", cwd=frontend_dir)
    
    print("Running Django checks...")
    run_command("python manage.py check --deploy", cwd=backend_dir)
    
    print("Running migrations...")
    run_command("python manage.py migrate", cwd=backend_dir)
    
    print("Collecting static files...")
    run_command("python manage.py collectstatic --noinput", cwd=backend_dir)
    
    print("\nBuild complete!")
    print("Start server with: python manage.py runserver")
    print("For production, use: gunicorn backend.wsgi:application")

if __name__ == "__main__":
    main()