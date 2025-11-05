#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 AUTO PUSH - Automatic Git Push on File Changes
Automatically commit and push changes when files are modified
"""

import time
import subprocess
import os
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Files/folders to ignore
IGNORE_PATTERNS = [
    '.git',
    '__pycache__',
    'node_modules',
    '.env',
    '.env.production',
    'venv',
    '*.pyc',
    '.DS_Store',
    'AUTO_PUSH.bat',
    'auto_push.py'
]

class AutoPushHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_push_time = 0
        self.push_delay = 5  # Wait 5 seconds before pushing
        self.pending_changes = False
        
    def should_ignore(self, path):
        """Check if file should be ignored"""
        for pattern in IGNORE_PATTERNS:
            if pattern in path:
                return True
        return False
    
    def on_modified(self, event):
        """Handle file modification"""
        if event.is_directory or self.should_ignore(event.src_path):
            return
        
        self.pending_changes = True
        current_time = time.time()
        
        # Only push if enough time has passed since last push
        if current_time - self.last_push_time > self.push_delay:
            self.push_changes(event.src_path)
    
    def push_changes(self, changed_file):
        """Commit and push changes"""
        try:
            # Get changed file name
            file_name = os.path.basename(changed_file)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"\n{'='*60}")
            print(f"🔄 CHANGEMENT DÉTECTÉ: {file_name}")
            print(f"⏰ {timestamp}")
            print(f"{'='*60}")
            
            # Git add
            print("\n📦 Git add...")
            subprocess.run(['git', 'add', '-A'], check=True)
            
            # Git commit
            commit_msg = f"auto: Update {file_name}"
            print(f"💾 Git commit: {commit_msg}")
            result = subprocess.run(
                ['git', 'commit', '-m', commit_msg],
                capture_output=True,
                text=True
            )
            
            if "nothing to commit" in result.stdout:
                print("   ℹ️  No changes to commit")
                return
            
            # Git push
            print("🚀 Git push...")
            subprocess.run(['git', 'push'], check=True)
            
            print("\n✅ PUSHED SUCCESSFULLY!")
            print(f"{'='*60}\n")
            
            self.last_push_time = time.time()
            self.pending_changes = False
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

def main():
    """Main function"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                  🚀 AUTO PUSH ACTIVATED                      ║
╚══════════════════════════════════════════════════════════════╝

📍 Watching directory: {}
⏱️  Push delay: 5 seconds
🔄 Auto-deploy: Vercel (on push)

Press Ctrl+C to stop...

""".format(os.getcwd()))
    
    event_handler = AutoPushHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 AUTO PUSH STOPPED")
        observer.stop()
    
    observer.join()

if __name__ == "__main__":
    # Check if watchdog is installed
    try:
        import watchdog
        main()
    except ImportError:
        print("❌ Error: 'watchdog' module not installed")
        print("\n📦 Installing watchdog...")
        subprocess.run(['pip', 'install', 'watchdog'], check=True)
        print("\n✅ Installed! Please run the script again.")

