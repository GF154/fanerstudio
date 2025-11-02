#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 Faner Studio - Auto Watch & Deploy
Automatically watches for file changes and deploys to GitHub/Render
"""

import time
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
import hashlib

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'═' * 60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}  {text}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'═' * 60}{Colors.ENDC}\n")

def print_success(text):
    """Print success message"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{Colors.OKGREEN}[{timestamp}] ✅ {text}{Colors.ENDC}")

def print_info(text):
    """Print info message"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{Colors.OKCYAN}[{timestamp}] ℹ️  {text}{Colors.ENDC}")

def print_warning(text):
    """Print warning message"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{Colors.WARNING}[{timestamp}] ⚠️  {text}{Colors.ENDC}")

def print_error(text):
    """Print error message"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{Colors.FAIL}[{timestamp}] ❌ {text}{Colors.ENDC}")

def run_command(command):
    """Run shell command"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def get_file_hash(filepath):
    """Get MD5 hash of a file"""
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

def get_project_state():
    """Get hash of all tracked files"""
    file_hashes = {}
    
    # Get list of tracked files
    success, output = run_command("git ls-files")
    if not success:
        return {}
    
    files = output.strip().split('\n')
    
    for file in files:
        if file and os.path.exists(file):
            file_hashes[file] = get_file_hash(file)
    
    return file_hashes

def has_changes(old_state, new_state):
    """Check if there are changes between states"""
    return old_state != new_state

def auto_deploy():
    """Automatically deploy changes"""
    print_info("Starting auto-deploy...")
    
    # Add all files
    success, _ = run_command("git add .")
    if not success:
        print_error("Failed to add files")
        return False
    
    # Generate commit message with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"🤖 Auto-deploy - {timestamp}"
    
    # Commit changes
    success, output = run_command(f'git commit -m "{commit_msg}"')
    if not success:
        if "nothing to commit" in output.lower():
            print_warning("No changes to commit")
            return False
        print_error("Failed to commit changes")
        return False
    
    print_success(f"Committed: {commit_msg}")
    
    # Push to GitHub
    print_info("Pushing to GitHub...")
    success, _ = run_command("git push origin master")
    if not success:
        print_error("Failed to push to GitHub")
        return False
    
    print_success("Pushed to GitHub successfully!")
    print_info("🚀 Render auto-deploy triggered!")
    print_info("⏱️  ETA: 3-5 minutes")
    print_info("🌐 https://fanerstudio-1.onrender.com")
    
    return True

def watch_and_deploy(check_interval=10):
    """Watch for changes and auto-deploy"""
    print_header("🤖 FANER STUDIO - AUTO WATCH & DEPLOY")
    
    print_info(f"Monitoring project for changes...")
    print_info(f"Check interval: {check_interval} seconds")
    print_info("Press Ctrl+C to stop\n")
    
    # Get initial state
    previous_state = get_project_state()
    print_success("Initial state captured")
    print_info(f"Tracking {len(previous_state)} files\n")
    
    deploy_count = 0
    
    try:
        while True:
            time.sleep(check_interval)
            
            # Get current state
            current_state = get_project_state()
            
            # Check for changes
            if has_changes(previous_state, current_state):
                print("")
                print_warning("Changes detected!")
                
                # Show changed files
                changed_files = []
                for file in current_state:
                    if file not in previous_state or current_state[file] != previous_state[file]:
                        changed_files.append(file)
                
                if changed_files:
                    print_info(f"Changed files ({len(changed_files)}):")
                    for file in changed_files[:5]:  # Show first 5
                        print(f"   📝 {file}")
                    if len(changed_files) > 5:
                        print(f"   ... and {len(changed_files) - 5} more")
                
                print("")
                
                # Auto-deploy
                if auto_deploy():
                    deploy_count += 1
                    previous_state = current_state
                    print("")
                    print_success(f"Deployment #{deploy_count} complete!")
                    print("")
                else:
                    print_error("Deployment failed, will retry on next change")
                    print("")
            else:
                # Show alive indicator
                print(f"{Colors.OKCYAN}[{datetime.now().strftime('%H:%M:%S')}] 👁️  Watching...{Colors.ENDC}", end='\r')
    
    except KeyboardInterrupt:
        print("\n")
        print_header("📊 DEPLOYMENT SUMMARY")
        print_info(f"Total deployments: {deploy_count}")
        print_success("Auto-watch stopped. Goodbye! 👋")
        print("")

def main():
    """Main function"""
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Check if git is available
    success, _ = run_command("git --version")
    if not success:
        print_error("Git not found! Please install Git first.")
        sys.exit(1)
    
    # Check if in a git repository
    success, _ = run_command("git status")
    if not success:
        print_error("Not in a git repository!")
        sys.exit(1)
    
    # Start watching
    watch_and_deploy(check_interval=10)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)

