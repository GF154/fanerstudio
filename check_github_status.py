#!/usr/bin/env python3
"""
Quick check of GitHub Actions status
"""
import requests
import json
from datetime import datetime

repo = "GF154/fanerstudio"
url = f"https://api.github.com/repos/{repo}/actions/runs?per_page=1"

try:
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        data = response.json()
        if data.get('workflow_runs'):
            run = data['workflow_runs'][0]
            
            print("="*60)
            print("🤖 GITHUB ACTIONS - DEPLOYMENT STATUS")
            print("="*60)
            print()
            print(f"📋 Workflow: {run['name']}")
            print(f"🔀 Branch: {run['head_branch']}")
            print(f"📝 Commit: {run['head_sha'][:7]}")
            print(f"👤 Author: {run['head_commit']['author']['name']}")
            print()
            print(f"📊 Status: {run['status'].upper()}")
            print(f"✓ Conclusion: {run.get('conclusion', 'IN PROGRESS').upper()}")
            print()
            print(f"🕐 Started: {run['created_at']}")
            print(f"🕐 Updated: {run['updated_at']}")
            print()
            print(f"🔗 View: {run['html_url']}")
            print()
            print("="*60)
            
            if run['status'] == 'in_progress':
                print("🔄 Deployment is running...")
                print("⏱️  This will take 5-8 minutes total")
                print()
                print("Phases:")
                print("  1. ✓ Code pushed to GitHub")
                print("  2. 🔄 Validation running...")
                print("  3. ⏳ Deploy pending...")
                print("  4. ⏳ Health check pending...")
            elif run['conclusion'] == 'success':
                print("✅ DEPLOYMENT SUCCESSFUL!")
                print()
                print("Your platform is now live:")
                print("  🌐 https://fanerstudio-1.onrender.com")
                print("  📚 https://fanerstudio-1.onrender.com/docs")
            elif run['conclusion'] == 'failure':
                print("❌ DEPLOYMENT FAILED")
                print("Check the logs for details")
                
except Exception as e:
    print(f"Error: {e}")
    print()
    print("View manually:")
    print("https://github.com/GF154/fanerstudio/actions")

