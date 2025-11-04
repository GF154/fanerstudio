"""
Test Render service: exs-d44o6m3ipnbc73anp6p0
Find the actual service URL
"""
import requests
import time

# Try different possible URLs
POSSIBLE_URLS = [
    "https://faner-studio-complete.onrender.com",
    "https://faner-studio-complete-d44o.onrender.com",
    "https://fanerstudio.onrender.com",
]

def find_service_url():
    """Try to find the actual service URL"""
    print("=" * 70)
    print("🔍 SEARCHING FOR SERVICE URL...")
    print("=" * 70)
    
    for url in POSSIBLE_URLS:
        try:
            print(f"\n🧪 Trying: {url}")
            response = requests.get(f"{url}/health", timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ FOUND IT!")
                return url
            elif response.status_code == 404:
                print(f"   ❌ Not Found (wrong URL)")
            elif response.status_code == 502:
                print(f"   ⏳ Service exists but not ready yet")
                return url  # Service exists, just not ready
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)[:50]}")
    
    return None

def check_service_info(url):
    """Get service info from Render API if possible"""
    print(f"\n" + "=" * 70)
    print(f"📊 CHECKING SERVICE: {url}")
    print("=" * 70)
    
    endpoints = ["/health", "/api/status", "/api/info", "/"]
    
    for endpoint in endpoints:
        try:
            print(f"\n🧪 {endpoint}")
            response = requests.get(f"{url}{endpoint}", timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ Working!")
            elif response.status_code == 502:
                print(f"   ⏳ Service starting...")
            elif response.status_code == 404:
                print(f"   ❌ Endpoint not found")
            
            time.sleep(1)
        except Exception as e:
            print(f"   ❌ {str(e)[:50]}")

if __name__ == "__main__":
    url = find_service_url()
    
    if url:
        print(f"\n✅ Service URL: {url}")
        check_service_info(url)
    else:
        print("\n❌ Could not find service URL")
        print("\n📋 Next steps:")
        print("1. Go to: https://dashboard.render.com/web/exs-d44o6m3ipnbc73anp6p0")
        print("2. Check the service name at the top")
        print("3. The URL should be: https://[service-name].onrender.com")
        print("4. Tell me what the service name is!")

