#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 FANER STUDIO - VERCEL DEPLOYMENT SCRIPT
Script pou deploy sou Vercel

This script will:
1. Check Vercel CLI installation
2. Deploy to Vercel production
3. Show deployment URL
"""

import subprocess
import sys
import os

def check_vercel_cli():
    """Check if Vercel CLI is installed"""
    try:
        result = subprocess.run(
            ["vercel", "--version"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✅ Vercel CLI installed: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        print("❌ Vercel CLI not installed")
        print("\nInstall with: npm i -g vercel")
        return False

def deploy_to_vercel():
    """Deploy to Vercel production"""
    print("\n🚀 Deploying to Vercel Production...")
    print("=" * 60)
    
    # Run vercel deploy
    result = subprocess.run(
        ["vercel", "--prod", "--yes"],
        text=True
    )
    
    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("✅ DEPLOYMENT SUCCESSFUL!")
        print("=" * 60)
        return True
    else:
        print("\n" + "=" * 60)
        print("❌ Deployment failed")
        print("=" * 60)
        return False

def main():
    print("🇭🇹 FANER STUDIO - VERCEL DEPLOYMENT")
    print("=" * 60)
    
    # Check CLI
    if not check_vercel_cli():
        sys.exit(1)
    
    # Deploy
    if deploy_to_vercel():
        print("\n✅ Your platform is now live on Vercel!")
        print("\nNext steps:")
        print("1. Visit your Vercel dashboard: https://vercel.com/dashboard")
        print("2. Add environment variables (SECRET_KEY, etc.)")
        print("3. Test your endpoints")
    else:
        print("\n❌ Deployment failed. Check errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()

