#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Faner Studio - Auto Deploy Script
Automatically deploy changes to GitHub and Render
"""

import subprocess
import sys
import os
from datetime import datetime
import webbrowser
import time

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
    UNDERLINE = '\033[4m'

def print_header(text):
    """Print formatted header"""
    print("\n" + "═" * 60)
    print(f"  {text}")
    print("═" * 60 + "\n")

def print_success(text):
    """Print success message"""
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")

def print_info(text):
    """Print info message"""
    print(f"{Colors.OKCYAN}ℹ️  {text}{Colors.ENDC}")

def print_warning(text):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")

def run_command(command, capture_output=False):
    """Run shell command and return result"""
    try:
        if capture_output:
            result = subprocess.run(
                command, 
                shell=True, 
                check=True, 
                capture_output=True, 
                text=True
            )
            return result.stdout.strip()
        else:
            subprocess.run(command, shell=True, check=True)
            return True
    except subprocess.CalledProcessError as e:
        return False

def check_git_installed():
    """Check if git is installed"""
    print_info("Checking if Git is installed...")
    result = run_command("git --version", capture_output=True)
    if result:
        print_success(f"Git is installed: {result}")
        return True
    else:
        print_error("Git is not installed!")
        print_info("Please install Git: https://git-scm.com/downloads")
        return False

def check_for_changes():
    """Check if there are uncommitted changes"""
    result = run_command("git status --porcelain", capture_output=True)
    return bool(result)

def show_git_status():
    """Show current git status"""
    print_info("Current changes:")
    print()
    os.system("git status --short")
    print()

def get_commit_message():
    """Get commit message from user or generate auto message"""
    print("📝 Enter commit message (or press Enter for auto-message):")
    message = input("> ").strip()
    
    if not message:
        # Generate auto message with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        message = f"🔄 Auto-deploy - {timestamp}"
    
    return message

def add_files():
    """Stage all files"""
    print_header("📦 STAGE 1: ADDING FILES")
    result = run_command("git add .")
    if result:
        print_success("All files staged successfully!")
        return True
    else:
        print_error("Error adding files!")
        return False

def commit_changes(message):
    """Commit changes"""
    print_header("💾 STAGE 2: COMMITTING CHANGES")
    print(f"Commit message: {message}\n")
    
    result = run_command(f'git commit -m "{message}"')
    if result:
        print_success("Changes committed successfully!")
        return True
    else:
        print_error("Error committing changes!")
        return False

def push_to_github():
    """Push to GitHub"""
    print_header("🚀 STAGE 3: PUSHING TO GITHUB")
    result = run_command("git push origin master")
    
    if result:
        print()
        print_success("Successfully pushed to GitHub!")
        return True
    else:
        print()
        print_error("Error pushing to GitHub!")
        print()
        print_warning("💡 Possible solutions:")
        print("   1. Check your internet connection")
        print("   2. Verify GitHub credentials")
        print("   3. Make sure you have push access to the repository")
        return False

def show_deployment_info():
    """Show deployment information"""
    print_header("🎉 DEPLOYMENT COMPLETE!")
    print_success("Git Status: Pushed to master")
    print(f"{Colors.OKCYAN}🔄 GitHub Actions: Validating code...{Colors.ENDC}")
    print(f"{Colors.OKCYAN}🚀 Render: Auto-deploying...{Colors.ENDC}")
    print(f"{Colors.OKCYAN}⏱️  ETA: 3-5 minutes{Colors.ENDC}")

def show_links():
    """Show deployment links"""
    print_header("📍 DEPLOYMENT LINKS")
    print("🤖 GitHub Actions:")
    print("   https://github.com/GF154/fanerstudio/actions")
    print()
    print("📊 Render Dashboard:")
    print("   https://dashboard.render.com")
    print()
    print("🌐 Live Platform:")
    print("   https://fanerstudio-1.onrender.com")
    print()
    print("📚 API Documentation:")
    print("   https://fanerstudio-1.onrender.com/docs")
    print()

def open_monitoring_pages():
    """Open deployment monitoring pages in browser"""
    response = input("\nOpen monitoring pages? (Y/N): ").strip().upper()
    
    if response == 'Y':
        print()
        print_info("Opening monitoring pages...")
        
        urls = [
            "https://github.com/GF154/fanerstudio/actions",
            "https://dashboard.render.com",
            "https://fanerstudio-1.onrender.com"
        ]
        
        for url in urls:
            webbrowser.open(url)
            time.sleep(2)
        
        print_success("Pages opened!")

def main():
    """Main deployment function"""
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print_header("🚀 FANER STUDIO - AUTO DEPLOY TO GITHUB & RENDER")
    
    # Check if git is installed
    if not check_git_installed():
        sys.exit(1)
    
    print()
    
    # Check for changes
    print_info("Checking for changes...")
    print()
    
    if not check_for_changes():
        print_info("No changes detected in working directory.")
        print()
        print_success("Current status: Clean working tree ✅")
        print()
        print_warning("💡 Make some changes to your files and run this script again.")
        print()
        sys.exit(0)
    
    print_success("Changes detected! Proceeding with deployment...")
    print()
    
    # Show current status
    show_git_status()
    
    print("═" * 60)
    print()
    
    # Get commit message
    commit_message = get_commit_message()
    print()
    
    # Stage files
    if not add_files():
        sys.exit(1)
    
    print()
    
    # Commit changes
    if not commit_changes(commit_message):
        sys.exit(1)
    
    print()
    
    # Push to GitHub
    if not push_to_github():
        sys.exit(1)
    
    print()
    
    # Show deployment info
    show_deployment_info()
    print()
    
    # Show links
    show_links()
    
    # Offer to open monitoring pages
    open_monitoring_pages()
    
    print()
    print("═" * 60)
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print_warning("\n\n⚠️  Deployment cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)

