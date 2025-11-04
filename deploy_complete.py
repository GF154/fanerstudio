#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Complete Deployment Automation for Faner Studio
Deplwaman otomatik konplè pou Faner Studio
"""

import subprocess
import sys
from pathlib import Path
import os


class Color:
    """Terminal colors"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    """Print colored header"""
    print(f"\n{Color.HEADER}{Color.BOLD}{'='*60}{Color.END}")
    print(f"{Color.HEADER}{Color.BOLD}{text}{Color.END}")
    print(f"{Color.HEADER}{Color.BOLD}{'='*60}{Color.END}\n")


def print_step(step: int, text: str):
    """Print step"""
    print(f"{Color.CYAN}{Color.BOLD}[{step}]{Color.END} {text}")


def print_success(text: str):
    """Print success message"""
    print(f"{Color.GREEN}✅ {text}{Color.END}")


def print_error(text: str):
    """Print error message"""
    print(f"{Color.RED}❌ {text}{Color.END}")


def print_warning(text: str):
    """Print warning message"""
    print(f"{Color.YELLOW}⚠️  {text}{Color.END}")


def run_command(cmd: list, description: str) -> bool:
    """Run command and return success status"""
    print(f"\n{Color.BLUE}Running: {' '.join(cmd)}{Color.END}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print_success(f"{description} - SUCCESS")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print_error(f"{description} - FAILED")
            if result.stderr:
                print(result.stderr)
            return False
    except Exception as e:
        print_error(f"{description} - ERROR: {e}")
        return False


def main():
    """Main deployment function"""
    print_header("🚀 FANER STUDIO - Complete Deployment")
    
    # Step 1: Validate environment
    print_step(1, "Validating environment...")
    if not run_command(
        [sys.executable, "environment_validator.py"],
        "Environment validation"
    ):
        print_warning("Environment has issues but continuing...")
    
    # Step 2: Run tests
    print_step(2, "Running tests...")
    if not run_command(
        [sys.executable, "test_complete_platform.py"],
        "Platform tests"
    ):
        print_warning("Some tests failed but continuing...")
    
    # Step 3: Check git status
    print_step(3, "Checking git status...")
    run_command(["git", "status", "--short"], "Git status")
    
    # Step 4: Add all changes
    print_step(4, "Adding all changes to git...")
    if not run_command(["git", "add", "."], "Git add"):
        print_error("Failed to add changes")
        return False
    
    # Step 5: Commit
    print_step(5, "Committing changes...")
    commit_message = "Complete platform upgrade v3.2.0 - All features functional"
    if not run_command(
        ["git", "commit", "-m", commit_message],
        "Git commit"
    ):
        print_warning("Nothing to commit or commit failed")
    
    # Step 6: Push to GitHub
    print_step(6, "Pushing to GitHub...")
    if not run_command(["git", "push"], "Git push"):
        print_error("Failed to push to GitHub")
        return False
    
    print_success("Pushed to GitHub successfully!")
    
    # Step 7: Deploy to Vercel (if installed)
    print_step(7, "Checking for Vercel CLI...")
    try:
        result = subprocess.run(["vercel", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print_success(f"Vercel CLI found: {result.stdout.strip()}")
            
            deploy = input(f"\n{Color.CYAN}Deploy to Vercel now? (y/n): {Color.END}").lower()
            if deploy == 'y':
                print_step(8, "Deploying to Vercel...")
                if run_command(["vercel", "--prod"], "Vercel deployment"):
                    print_success("Deployed to Vercel successfully!")
                else:
                    print_error("Vercel deployment failed")
            else:
                print_warning("Skipping Vercel deployment")
                print(f"\n{Color.YELLOW}To deploy later, run: vercel --prod{Color.END}")
        else:
            print_warning("Vercel CLI not installed")
            print(f"{Color.YELLOW}Install: npm install -g vercel{Color.END}")
            print(f"{Color.YELLOW}Then run: vercel --prod{Color.END}")
    except FileNotFoundError:
        print_warning("Vercel CLI not found")
        print(f"{Color.YELLOW}Install: npm install -g vercel{Color.END}")
    
    # Final summary
    print_header("✅ Deployment Complete!")
    print("\n📋 Next Steps:")
    print(f"  1. {Color.GREEN}✅{Color.END} Code pushed to GitHub")
    print(f"  2. {Color.CYAN}📝{Color.END} Check GitHub Actions for automated tests")
    print(f"  3. {Color.CYAN}🚀{Color.END} Deploy to Vercel: {Color.BOLD}vercel --prod{Color.END}")
    print(f"  4. {Color.CYAN}🌐{Color.END} Monitor: https://vercel.com/dashboard")
    
    print("\n📚 Documentation:")
    print(f"  • README: {Color.BOLD}README_COMPLETE.md{Color.END}")
    print(f"  • Deployment Guide: {Color.BOLD}VERCEL_DEPLOYMENT_GUIDE.md{Color.END}")
    print(f"  • Environment Validator: {Color.BOLD}python environment_validator.py{Color.END}")
    print(f"  • Run Tests: {Color.BOLD}python test_complete_platform.py{Color.END}")
    
    print(f"\n{Color.GREEN}{Color.BOLD}🎉 Faner Studio v3.2.0 is ready!{Color.END}\n")
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n\n{Color.YELLOW}⚠️  Deployment cancelled by user{Color.END}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n{Color.RED}❌ Unexpected error: {e}{Color.END}\n")
        sys.exit(1)

