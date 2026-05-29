"""
Auto-reload script for Kivy frontend development.
Watches for file changes and automatically restarts the app.

Usage:
    python frontend_reload.py

The app will restart automatically when you modify any .py files in the frontend folder.
Press Ctrl+C to stop.
"""
import subprocess
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

class ChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.last_restart = 0
    
    def on_modified(self, event):
        # Ignore rapid changes (within 1 second)
        current_time = time.time()
        if current_time - self.last_restart < 1:
            return
        
        if event.src_path.endswith('.py'):
            self.restart_app(event.src_path)
            self.last_restart = current_time
    
    def restart_app(self, changed_file):
        print(f"\n{'='*60}")
        print(f"📝 File changed: {os.path.basename(changed_file)}")
        print(f"{'='*60}")
        print("🔄 Restarting app...\n")
        
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except Exception as e:
                print(f"⚠ Error stopping app: {e}")
                self.process.kill()
        
        # Start new process
        self.process = subprocess.Popen(
            [sys.executable, 'frontend/main.py'],
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
    
    def start_initial_app(self):
        """Start the app for the first time."""
        print("\n" + "="*60)
        print("🚀 Nation Wants to Guess - Frontend (Auto-Reload Mode)")
        print("="*60)
        print("Watching for changes in frontend/ folder...")
        print("Press Ctrl+C to stop\n")
        
        self.process = subprocess.Popen(
            [sys.executable, 'frontend/main.py'],
            cwd=os.path.dirname(os.path.abspath(__file__))
        )

if __name__ == '__main__':
    handler = ChangeHandler()
    handler.start_initial_app()
    
    # Set up file watcher
    observer = Observer()
    observer.schedule(handler, path='frontend', recursive=True)
    observer.start()
    
    try:
        observer.join()
    except KeyboardInterrupt:
        print("\n⛔ Stopping auto-reload...")
        observer.stop()
        if handler.process:
            handler.process.terminate()
            handler.process.wait()
        print("✓ App stopped")
    finally:
        observer.join()
