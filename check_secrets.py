#!/usr/bin/env python3
"""
🔐 Check GitHub Secrets Configuration
Verify if Render secrets are set up correctly
"""

import requests
import sys

def check_secrets():
    """Check if secrets are configured (we can't read values, only check if workflow runs)"""
    
    print("="*60)
    print("🔐 GitHub Secrets Checker")
    print("="*60)
    print()
    
    repo = "GF154/fanerstudio"
    
    print("📋 Required Secrets for Render Deployment:")
    print()
    print("  1. RENDER_API_KEY")
    print("     └─ Get from: https://dashboard.render.com/u/settings")
    print()
    print("  2. RENDER_SERVICE_ID")
    print("     └─ Get from: Render Dashboard → Service → Settings")
    print()
    print("  3. RENDER_SERVICE_URL (Optional)")
    print("     └─ Example: https://your-service.onrender.com")
    print()
    
    print("="*60)
    print("📍 How to Add Secrets:")
    print("="*60)
    print()
    print(f"1. Go to: https://github.com/{repo}/settings/secrets/actions")
    print("2. Click 'New repository secret'")
    print("3. Add each secret with name and value")
    print("4. Save")
    print()
    
    print("="*60)
    print("🔍 Verify Secrets:")
    print("="*60)
    print()
    print("You cannot view secret values (security).")
    print("To verify they work:")
    print()
    print("  1. Push a commit to master branch")
    print("  2. Go to: https://github.com/{}/actions".format(repo))
    print("  3. Check if workflow runs without secret errors")
    print()
    
    # Try to check latest workflow run
    print("="*60)
    print("🤖 Checking Latest Workflow...")
    print("="*60)
    print()
    
    try:
        url = f"https://api.github.com/repos/{repo}/actions/runs?per_page=1"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('workflow_runs'):
                run = data['workflow_runs'][0]
                
                conclusion = run.get('conclusion', 'in_progress')
                status = run.get('status', 'unknown')
                name = run['name']
                
                print(f"📊 Latest Workflow: {name}")
                print(f"📈 Status: {status}")
                print(f"✓ Conclusion: {conclusion}")
                print()
                
                if conclusion == 'failure':
                    print("⚠️  Last workflow failed!")
                    print("   → Check if it's a secrets error")
                    print(f"   → View logs: {run['html_url']}")
                elif conclusion == 'success':
                    print("✅ Last workflow succeeded!")
                    print("   → Secrets are likely configured correctly")
                else:
                    print(f"🔄 Workflow is {status}")
                    
            else:
                print("ℹ️  No workflow runs found yet")
        else:
            print(f"⚠️  Could not fetch workflow status (HTTP {response.status_code})")
            
    except Exception as e:
        print(f"❌ Error checking workflows: {e}")
    
    print()
    print("="*60)
    print("💡 Tips:")
    print("="*60)
    print()
    print("• Secrets are encrypted and cannot be viewed after creation")
    print("• Update secrets by creating new ones with same name")
    print("• Secrets are available in all workflows")
    print("• Use workflow logs to debug secret issues")
    print()

if __name__ == "__main__":
    check_secrets()

