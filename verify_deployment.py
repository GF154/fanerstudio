#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Verify Render Deployment Configuration
Diagnostic tool to check Render service setup and identify issues
"""

import asyncio
import httpx
import json
from datetime import datetime
from pathlib import Path

# ============================================================
# CONFIGURATION
# ============================================================

SERVICES = {
    "fanerstudio-1": "https://fanerstudio-1.onrender.com",
    "faner-studio-complete": "https://faner-studio-complete.onrender.com"
}

EXPECTED_ENDPOINTS = [
    "/",
    "/health",
    "/api/info",
    "/api/status",
    "/admin",
    "/docs",
    "/api/translate",
    "/api/performance/system",
    "/api/voices",
    "/api/podcast/templates"
]

# ============================================================
# COLORS
# ============================================================

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

# ============================================================
# UTILITIES
# ============================================================

def print_header(text: str):
    """Print section header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}\n")

def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {text}{Colors.RESET}")

def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}❌ {text}{Colors.RESET}")

def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.RESET}")

def print_info(text: str):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.RESET}")

# ============================================================
# CHECK LOCAL CONFIGURATION
# ============================================================

def check_local_config():
    """Check local project configuration"""
    print_header("📁 LOCAL CONFIGURATION CHECK")
    
    issues = []
    
    # Check render.yaml
    render_yaml = Path("render.yaml")
    if render_yaml.exists():
        print_success("render.yaml exists")
        with open(render_yaml, 'r') as f:
            content = f.read()
            if 'name: faner-studio-complete' in content:
                print_info("   Service name: faner-studio-complete")
            if 'branch: master' in content:
                print_success("   Branch: master ✅")
            else:
                print_warning("   Branch: NOT master (check this!)")
                issues.append("render.yaml branch should be 'master'")
            if 'autoDeploy: true' in content:
                print_success("   Auto-deploy: enabled ✅")
            else:
                print_warning("   Auto-deploy: NOT enabled")
                issues.append("Auto-deploy should be enabled")
    else:
        print_error("render.yaml NOT found!")
        issues.append("Missing render.yaml file")
    
    # Check main.py
    main_py = Path("main.py")
    if main_py.exists():
        print_success("main.py exists")
        try:
            with open(main_py, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'FastAPI' in content:
                    print_success("   FastAPI app found ✅")
                if '@app.get("/admin")' in content:
                    print_success("   Admin endpoint found ✅")
                if '@app.get("/api/status")' in content:
                    print_success("   Status endpoint found ✅")
        except:
            print_warning("   Could not read main.py (encoding issue)")
    else:
        print_error("main.py NOT found!")
        issues.append("Missing main.py file")
    
    # Check requirements.txt
    requirements = Path("requirements.txt")
    if requirements.exists():
        print_success("requirements.txt exists")
        with open(requirements, 'r') as f:
            content = f.read()
            required_packages = ['fastapi', 'uvicorn', 'httpx', 'sqlalchemy']
            for pkg in required_packages:
                if pkg in content.lower():
                    print_success(f"   {pkg} found ✅")
                else:
                    print_warning(f"   {pkg} NOT found")
                    issues.append(f"Missing {pkg} in requirements.txt")
    else:
        print_error("requirements.txt NOT found!")
        issues.append("Missing requirements.txt file")
    
    # Check .github/workflows
    workflows_dir = Path(".github/workflows")
    if workflows_dir.exists():
        yaml_files = list(workflows_dir.glob("*.yml")) + list(workflows_dir.glob("*.yaml"))
        if yaml_files:
            print_success(f"GitHub Actions workflows found: {len(yaml_files)}")
        else:
            print_warning("No workflow files found in .github/workflows/")
    else:
        print_warning(".github/workflows/ directory not found")
    
    return issues

# ============================================================
# CHECK REMOTE SERVICE
# ============================================================

async def check_remote_service(service_name: str, base_url: str):
    """Check remote Render service"""
    print_header(f"🌐 REMOTE SERVICE: {service_name}")
    print_info(f"URL: {base_url}")
    
    issues = []
    working_endpoints = []
    
    async with httpx.AsyncClient(timeout=15.0) as client:
        # Check service availability
        try:
            response = await client.get(base_url)
            if response.status_code == 200:
                print_success(f"Service is online (Status: {response.status_code})")
            else:
                print_warning(f"Service returned status: {response.status_code}")
        except Exception as e:
            print_error(f"Service is OFFLINE or unreachable")
            print_error(f"   Error: {str(e)}")
            issues.append(f"Service {service_name} is not accessible")
            return issues, working_endpoints
        
        # Check individual endpoints
        print(f"\n{Colors.BOLD}Testing Endpoints:{Colors.RESET}")
        for endpoint in EXPECTED_ENDPOINTS:
            try:
                response = await client.get(f"{base_url}{endpoint}")
                if response.status_code == 200:
                    print_success(f"{endpoint:30} → 200 OK")
                    working_endpoints.append(endpoint)
                elif response.status_code == 404:
                    print_error(f"{endpoint:30} → 404 NOT FOUND")
                    issues.append(f"Endpoint {endpoint} not found")
                else:
                    print_warning(f"{endpoint:30} → {response.status_code}")
            except Exception as e:
                print_error(f"{endpoint:30} → ERROR: {str(e)}")
        
        # Check health endpoint details
        try:
            response = await client.get(f"{base_url}/health")
            if response.status_code == 200:
                data = response.json()
                print(f"\n{Colors.BOLD}Health Check Details:{Colors.RESET}")
                print_info(f"   Status: {data.get('status')}")
                print_info(f"   Service: {data.get('service')}")
                print_info(f"   Version: {data.get('version')}")
                
                features = data.get('features', {})
                if features:
                    print(f"\n{Colors.BOLD}   Features:{Colors.RESET}")
                    for feature, status in features.items():
                        if status in ['active', True]:
                            print_success(f"      {feature}: active")
                        else:
                            print_warning(f"      {feature}: {status}")
        except:
            pass
    
    return issues, working_endpoints

# ============================================================
# ANALYZE ISSUES
# ============================================================

def analyze_issues(local_issues, remote_issues, service_name, working_endpoints):
    """Analyze all issues and provide recommendations"""
    print_header("📊 DIAGNOSIS & RECOMMENDATIONS")
    
    total_issues = len(local_issues) + len(remote_issues)
    total_working = len(working_endpoints)
    
    if total_issues == 0 and total_working >= 8:
        print_success("🎉 EVERYTHING LOOKS GOOD!")
        print_info("   All configurations are correct")
        print_info("   All endpoints are working")
        return
    
    if remote_issues:
        print(f"\n{Colors.BOLD}{Colors.RED}🔴 CRITICAL ISSUES:{Colors.RESET}")
        print_error(f"   {len(remote_issues)} endpoint(s) not working\n")
        
        if len(working_endpoints) <= 3:
            print_error("LIKELY CAUSE: Service is running OLD CODE")
            print(f"\n{Colors.BOLD}Solution:{Colors.RESET}")
            print("1. Go to Render Dashboard:")
            print(f"   https://dashboard.render.com")
            print(f"\n2. Select service: {service_name}")
            print("\n3. Check Settings → Build & Deploy:")
            print("   Build Command:")
            print(f"   {Colors.GREEN}pip install --upgrade pip && pip install -r requirements.txt{Colors.RESET}")
            print("\n   Start Command:")
            print(f"   {Colors.GREEN}uvicorn main:app --host 0.0.0.0 --port $PORT{Colors.RESET}")
            print("\n4. Check Settings → General:")
            print(f"   Branch: {Colors.GREEN}master{Colors.RESET} (NOT main!)")
            print(f"   Auto-Deploy: {Colors.GREEN}Yes{Colors.RESET}")
            print("\n5. Manual Deploy:")
            print("   Click 'Manual Deploy' → 'Deploy latest commit'")
            print("\n6. Wait 3-5 minutes for deployment")
            print("\n7. Run this script again to verify")
    
    if local_issues:
        print(f"\n{Colors.BOLD}{Colors.YELLOW}⚠️  LOCAL CONFIGURATION ISSUES:{Colors.RESET}")
        for issue in local_issues:
            print_warning(f"   • {issue}")
    
    print(f"\n{Colors.BOLD}📈 SUMMARY:{Colors.RESET}")
    print(f"   Working endpoints: {total_working}/{len(EXPECTED_ENDPOINTS)}")
    print(f"   Issues found: {total_issues}")
    
    if total_working < 5:
        print(f"\n{Colors.RED}❌ SERVICE NEEDS ATTENTION{Colors.RESET}")
    elif total_working < 8:
        print(f"\n{Colors.YELLOW}⚠️  SERVICE PARTIALLY WORKING{Colors.RESET}")
    else:
        print(f"\n{Colors.GREEN}✅ SERVICE MOSTLY WORKING{Colors.RESET}")

# ============================================================
# MAIN
# ============================================================

async def main():
    """Main diagnostic routine"""
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}{'='*60}")
    print("🔍 RENDER DEPLOYMENT VERIFICATION")
    print(f"{'='*60}{Colors.RESET}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Step 1: Check local configuration
    local_issues = check_local_config()
    
    # Step 2: Check remote services
    all_remote_issues = {}
    all_working_endpoints = {}
    
    for service_name, base_url in SERVICES.items():
        issues, working = await check_remote_service(service_name, base_url)
        all_remote_issues[service_name] = issues
        all_working_endpoints[service_name] = working
    
    # Step 3: Analyze and recommend
    print_header("🔍 WHICH SERVICE IS ACTIVE?")
    
    for service_name, working in all_working_endpoints.items():
        if len(working) >= 5:
            print_success(f"{service_name}: ACTIVE ({len(working)}/{len(EXPECTED_ENDPOINTS)} endpoints)")
        elif len(working) > 0:
            print_warning(f"{service_name}: PARTIAL ({len(working)}/{len(EXPECTED_ENDPOINTS)} endpoints)")
        else:
            print_error(f"{service_name}: INACTIVE or NOT DEPLOYED")
    
    # Analyze main service
    main_service = "fanerstudio-1"  # Current active service
    if main_service in all_remote_issues:
        analyze_issues(
            local_issues,
            all_remote_issues[main_service],
            main_service,
            all_working_endpoints[main_service]
        )
    
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}{'='*60}")
    print("Verification completed!")
    print(f"{'='*60}{Colors.RESET}\n")

if __name__ == "__main__":
    asyncio.run(main())

