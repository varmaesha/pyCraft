#!/usr/bin/env python3
"""
Simple launcher script for Nation Wants to Guess scoring app.
Checks dependencies and starts the application.
"""
import sys
import subprocess
import os

def check_dependencies():
    """Check if all required packages are installed."""
    required = ['kivy', 'fastapi', 'uvicorn', 'sqlalchemy', 'requests']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is NOT installed")
            missing.append(package)
    
    if missing:
        print(f"\nMissing packages: {', '.join(missing)}")
        print("\nTo install missing packages, run:")
        print(f"  pip install {' '.join(missing)}")
        return False
    
    print("\n✓ All dependencies are installed!")
    return True

def create_database_folder():
    """Ensure database folder exists."""
    db_folder = os.path.join(os.path.dirname(__file__), 'database')
    os.makedirs(db_folder, exist_ok=True)
    print(f"✓ Database folder ready: {db_folder}")

def start_app():
    """Start the Kivy frontend (which auto-starts backend)."""
    print("\n" + "="*50)
    print("Starting Nation Wants to Guess Scoring System")
    print("="*50 + "\n")
    
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    os.chdir(frontend_dir)
    
    print("Launching Kivy app...")
    print("(The backend server will start automatically)\n")
    
    try:
        subprocess.run([sys.executable, 'main.py'])
    except KeyboardInterrupt:
        print("\n\nApp stopped by user.")
    except Exception as e:
        print(f"\nError starting app: {e}")
        sys.exit(1)

if __name__ == '__main__':
    print("Nation Wants to Guess Scoring System\n")
    
    # Check dependencies
    if not check_dependencies():
        print("\nPlease install missing dependencies first:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    
    # Create database folder
    create_database_folder()
    
    # Start app
    start_app()
