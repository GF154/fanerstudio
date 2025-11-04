"""
Test new Render deployment: faner-studio-complete
"""
import requests
import time

BASE_URL = "https://faner-studio-complete.onrender.com"

def test_endpoint(name, endpoint, method="GET"):
    """Test a single endpoint"""
    url = f"{BASE_URL}{endpoint}"
    try:
        print(f"\n🧪 Testing {name}...")
        print(f"   URL: {url}")
        
        if method == "GET":
            response = requests.get(url, timeout=30)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ SUCCESS!")
            try:
                data = response.json()
                if isinstance(data, dict):
                    for key in list(data.keys())[:3]:
                        print(f"   📦 {key}: {str(data[key])[:50]}...")
            except:
                print(f"   📄 Response length: {len(response.text)} bytes")
            return True
        else:
            print(f"   ❌ FAILED: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        return False

def main():
    print("=" * 70)
    print("🚀 TESTING: faner-studio-complete.onrender.com")
    print("=" * 70)
    
    tests = [
        ("Health Check", "/health"),
        ("API Status", "/api/status"),
        ("API Info", "/api/info"),
        ("Translation API", "/api/translate"),
        ("Voice List", "/api/voices"),
        ("Podcast Templates", "/api/podcast/templates"),
        ("Performance System", "/api/performance/system"),
        ("Admin Dashboard", "/admin"),
        ("Root Page", "/"),
    ]
    
    results = []
    for name, endpoint in tests:
        result = test_endpoint(name, endpoint)
        results.append((name, result))
        time.sleep(1)
    
    print("\n" + "=" * 70)
    print("📊 RESULTS SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n🎯 Score: {passed}/{total} ({passed*100//total}%)")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Platform is fully functional!")
    elif passed >= total * 0.8:
        print("\n✅ Most tests passed! Platform is working well!")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
    
    print("\n🌐 Service URL:", BASE_URL)
    print("=" * 70)

if __name__ == "__main__":
    main()

