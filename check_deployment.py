#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Deployment Status Checker
Tcheke status deplwaman GitHub Actions ak Render
"""

import requests
import time
import sys
from datetime import datetime

# Colors for terminal
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text:^60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}\n")

def print_status(emoji, label, status, color=Colors.GREEN):
    """Print formatted status line"""
    print(f"{emoji} {Colors.BOLD}{label:30}{Colors.END} {color}{status}{Colors.END}")

def check_github_actions():
    """Check GitHub Actions workflow status"""
    print_header("🔍 GitHub Actions Status")
    
    repo = "GF154/fanerstudio"
    api_url = f"https://api.github.com/repos/{repo}/actions/runs"
    
    try:
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('workflow_runs'):
                # Get the most recent workflow
                latest = data['workflow_runs'][0]
                
                status = latest['status']
                conclusion = latest.get('conclusion', 'N/A')
                name = latest['name']
                branch = latest['head_branch']
                created = latest['created_at']
                updated = latest['updated_at']
                
                # Status emoji and color
                if status == 'completed':
                    if conclusion == 'success':
                        status_emoji = '✅'
                        status_color = Colors.GREEN
                    else:
                        status_emoji = '❌'
                        status_color = Colors.RED
                elif status == 'in_progress':
                    status_emoji = '🔄'
                    status_color = Colors.YELLOW
                else:
                    status_emoji = '⏸️'
                    status_color = Colors.YELLOW
                
                print_status(status_emoji, "Workflow:", name)
                print_status("🔀", "Branch:", branch)
                print_status("📊", "Status:", f"{status} ({conclusion})", status_color)
                print_status("🕐", "Started:", created)
                print_status("🕐", "Updated:", updated)
                print_status("🔗", "URL:", latest['html_url'], Colors.BLUE)
                
                return status, conclusion
            else:
                print_status("⚠️", "Status:", "No workflows found", Colors.YELLOW)
                return None, None
        else:
            print_status("❌", "Error:", f"HTTP {response.status_code}", Colors.RED)
            return None, None
            
    except Exception as e:
        print_status("❌", "Error:", str(e), Colors.RED)
        return None, None

def check_render_service(service_url=None):
    """Check Render service health"""
    print_header("☁️  Render Service Status")
    
    # Try different possible URLs
    urls_to_try = [
        service_url,
        "https://kreyol-ia-studio.onrender.com",
        "https://fanerstudio.onrender.com"
    ]
    
    for url in urls_to_try:
        if not url:
            continue
            
        print(f"\n🔍 Trying: {Colors.BLUE}{url}{Colors.END}")
        
        try:
            # Try health endpoint
            health_url = f"{url}/health"
            response = requests.get(health_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                print_status("✅", "Service:", "ONLINE", Colors.GREEN)
                print_status("🌐", "URL:", url, Colors.BLUE)
                print_status("💚", "Health:", "Healthy")
                
                if 'version' in data:
                    print_status("📦", "Version:", data['version'])
                if 'service' in data:
                    print_status("🏷️", "Name:", data['service'])
                if 'deployment' in data:
                    print_status("🚀", "Deployment:", data['deployment'])
                
                # Try status endpoint
                try:
                    status_response = requests.get(f"{url}/api/status", timeout=5)
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        print_status("📊", "Environment:", status_data.get('environment', 'N/A'))
                        print_status("🐍", "Python:", status_data.get('python_version', 'N/A'))
                except:
                    pass
                
                return True
                
            elif response.status_code == 503:
                print_status("⚠️", "Service:", "Starting up...", Colors.YELLOW)
                print_status("💡", "Tip:", "Service is deploying, wait a moment")
                return False
            else:
                print_status("❌", "Service:", f"HTTP {response.status_code}", Colors.RED)
                
        except requests.exceptions.ConnectionError:
            print_status("❌", "Connection:", "Unable to connect", Colors.RED)
        except requests.exceptions.Timeout:
            print_status("⏱️", "Timeout:", "Request timed out", Colors.YELLOW)
        except Exception as e:
            print_status("❌", "Error:", str(e), Colors.RED)
    
    print_status("ℹ️", "Note:", "Service URL not found or not ready yet", Colors.YELLOW)
    return False

def monitor_deployment(check_interval=30, max_checks=20):
    """Monitor deployment until completion"""
    print_header("📡 Monitoring Deployment")
    
    print(f"🔄 Checking every {check_interval} seconds (max {max_checks} checks)")
    print(f"⏱️  Maximum wait time: {(check_interval * max_checks) // 60} minutes\n")
    
    for i in range(max_checks):
        print(f"\n{Colors.BOLD}Check #{i+1}/{max_checks} - {datetime.now().strftime('%H:%M:%S')}{Colors.END}")
        print("-" * 60)
        
        # Check GitHub Actions
        status, conclusion = check_github_actions()
        
        # Check Render service
        service_online = check_render_service()
        
        # Determine if we should continue
        if status == 'completed':
            if conclusion == 'success' and service_online:
                print_header("🎉 DEPLOYMENT SUCCESSFUL!")
                print(f"{Colors.GREEN}✅ Workflow completed successfully{Colors.END}")
                print(f"{Colors.GREEN}✅ Service is online and healthy{Colors.END}")
                return True
            elif conclusion == 'failure':
                print_header("❌ DEPLOYMENT FAILED")
                print(f"{Colors.RED}Workflow failed. Check logs at GitHub Actions{Colors.END}")
                return False
        
        # Wait before next check
        if i < max_checks - 1:
            print(f"\n⏳ Waiting {check_interval} seconds before next check...")
            time.sleep(check_interval)
    
    print_header("⏱️ TIMEOUT")
    print(f"{Colors.YELLOW}Reached maximum check limit{Colors.END}")
    print(f"{Colors.YELLOW}Deployment might still be in progress{Colors.END}")
    return False

def main():
    """Main function"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}🇭🇹 Faner Studio - Deployment Checker{Colors.END}")
    print(f"{Colors.CYAN}Check your deployment status on GitHub Actions & Render{Colors.END}")
    
    # Quick status check
    print("\n" + "="*60)
    print(f"{Colors.BOLD}Quick Status Check{Colors.END}")
    print("="*60)
    
    gh_status, gh_conclusion = check_github_actions()
    render_status = check_render_service()
    
    # Show summary
    print_header("📊 Summary")
    
    if gh_status == 'completed' and gh_conclusion == 'success':
        print_status("✅", "GitHub Actions:", "Completed successfully", Colors.GREEN)
    elif gh_status == 'in_progress':
        print_status("🔄", "GitHub Actions:", "In progress", Colors.YELLOW)
    elif gh_status == 'completed' and gh_conclusion == 'failure':
        print_status("❌", "GitHub Actions:", "Failed", Colors.RED)
    else:
        print_status("❓", "GitHub Actions:", "Unknown status", Colors.YELLOW)
    
    if render_status:
        print_status("✅", "Render Service:", "Online", Colors.GREEN)
    else:
        print_status("⏳", "Render Service:", "Not ready yet", Colors.YELLOW)
    
    # Ask if user wants to monitor
    print(f"\n{Colors.BOLD}Options:{Colors.END}")
    print("  1. Monitor continuously (check every 30s)")
    print("  2. Exit")
    
    try:
        choice = input(f"\n{Colors.BOLD}Choice [1/2]:{Colors.END} ").strip()
        
        if choice == '1':
            monitor_deployment()
        else:
            print(f"\n{Colors.CYAN}👋 Bye! Check again later with: python check_deployment.py{Colors.END}\n")
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Interrupted by user{Colors.END}")
        print(f"{Colors.CYAN}👋 Bye!{Colors.END}\n")
        sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Interrupted by user{Colors.END}\n")
        sys.exit(0)

