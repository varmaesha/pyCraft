"""
Development startup script - runs backend and frontend with auto-reload.

Usage:
    python dev_start.py

This script requires:
    - watchdog (for frontend auto-reload): pip install watchdog

It will:
1. Start FastAPI backend with auto-reload
2. Start Kivy frontend with auto-reload
3. Both will restart automatically on file changes

Stop with Ctrl+C
"""
import os
import subprocess
import sys
import time

def run_backend():
    """Start backend in a new terminal."""
    backend_cmd = [
        sys.executable, '-m', 'uvicorn',
        'backend.main:app',
        '--reload',
        '--host', '127.0.0.1',
        '--port', '8000'
    ]
    
    print("\n" + "="*70)
    print("🚀 Starting Backend (FastAPI)")
    print("="*70)
    print("Backend will reload automatically on changes")
    print("Running: " + ' '.join(backend_cmd))
    print()
    
    return subprocess.Popen(backend_cmd)

def run_frontend():
    """Start frontend in a new process."""
    print("\n" + "="*70)
    print("🎮 Starting Frontend (Kivy)")
    print("="*70)
    print("Frontend will reload automatically with watchdog")
    print("Running: python frontend_reload.py")
    print()
    
    # Wait a moment for backend to start
    time.sleep(3)
    
    return subprocess.Popen([sys.executable, 'frontend_reload.py'])

if __name__ == '__main__':
    print("\n" + "="*70)
    print("Nation Wants to Guess - Development Mode")
    print("="*70)
    
    # Check if watchdog is installed
    try:
        import watchdog
        print("✓ Watchdog is installed - frontend auto-reload enabled")
    except ImportError:
        print("⚠ Watchdog not found - frontend auto-reload disabled")
        print("  Install it with: pip install watchdog")
    
    print("\nStarting both backend and frontend...")
    print("This will open in the same terminal (mixed output)")
    print("Press Ctrl+C to stop everything\n")
    
    # Start both processes
    backend_process = run_backend()
    frontend_process = run_frontend()
    
    print("\n" + "="*70)
    print("✓ Both backend and frontend are running!")
    print("="*70)
    print("\nPress Ctrl+C to stop both services")
    print()
    
    try:
        # Wait for both processes
        while True:
            backend_status = backend_process.poll()
            frontend_status = frontend_process.poll()
            
            if backend_status is not None:
                print("❌ Backend crashed! Restarting...")
                backend_process = run_backend()
            
            if frontend_status is not None:
                print("❌ Frontend crashed! Restarting...")
                frontend_process = run_frontend()
            
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("⛔ Stopping both services...")
        print("="*70)
        
        # Kill both processes
        backend_process.terminate()
        frontend_process.terminate()
        
        try:
            backend_process.wait(timeout=3)
            frontend_process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            backend_process.kill()
            frontend_process.kill()
        
        print("✓ Services stopped\n")
        sys.exit(0)
