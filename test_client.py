"""
Test Client - Simple script to test server connection
"""

import json
import sys
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


def test_server(server_url):
    """Test connection to the logging server"""
    
    server_url = server_url.rstrip('/')
    
    print("="*60)
    print("PC LOGGING SERVER - TEST CLIENT")
    print("="*60)
    print(f"Testing server: {server_url}")
    print()
    
    # Test 1: Check server status
    print("[1/3] Testing server status endpoint...")
    try:
        request = Request(f"{server_url}/status", method='GET')
        response = urlopen(request, timeout=5)
        result = json.loads(response.read().decode('utf-8'))
        print(f"   ✓ SUCCESS: {result}")
    except URLError as e:
        print(f"   ✗ FAILED: {e}")
        return False
    except Exception as e:
        print(f"   ✗ FAILED: {e}")
        return False
    
    # Test 2: Send test log
    print()
    print("[2/3] Sending test log data...")
    test_data = {
        "pc_name": "TEST-PC",
        "status": "running",
        "software": ["Test App 1", "Test App 2", "Test App 3"]
    }
    
    try:
        request = Request(
            f"{server_url}/log",
            data=json.dumps(test_data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        response = urlopen(request, timeout=5)
        result = json.loads(response.read().decode('utf-8'))
        print(f"   ✓ SUCCESS: {result.get('message', 'Log sent')}")
    except URLError as e:
        print(f"   ✗ FAILED: {e}")
        return False
    except HTTPError as e:
        print(f"   ✗ FAILED: HTTP {e.code} - {e.reason}")
        try:
            error_body = e.read().decode('utf-8')
            print(f"   Error details: {error_body}")
        except:
            pass
        return False
    except Exception as e:
        print(f"   ✗ FAILED: {e}")
        return False
    
    # Test 3: Retrieve logs
    print()
    print("[3/3] Retrieving all logs...")
    try:
        request = Request(f"{server_url}/logs", method='GET')
        response = urlopen(request, timeout=5)
        logs = json.loads(response.read().decode('utf-8'))
        print(f"   ✓ SUCCESS: Retrieved logs")
        print()
        print("   Logged PCs:")
        for pc_name, info in logs.get('pcs', {}).items():
            print(f"     - {pc_name}: {info.get('status', 'unknown')} ({len(info.get('software', []))} apps)")
    except URLError as e:
        print(f"   ✗ FAILED: {e}")
        return False
    except Exception as e:
        print(f"   ✗ FAILED: {e}")
        return False
    
    print()
    print("="*60)
    print("ALL TESTS PASSED! Server is working correctly.")
    print("="*60)
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_client.py <SERVER_URL>")
        print("Example: python test_client.py http://192.168.56.1:8080")
        print()
        print("Or use test_client.bat")
        sys.exit(1)
    
    server_url = sys.argv[1]
    success = test_server(server_url)
    sys.exit(0 if success else 1)

