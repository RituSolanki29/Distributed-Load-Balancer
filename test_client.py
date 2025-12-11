import requests
import time
import random
from concurrent.futures import ThreadPoolExecutor
import sys

LOAD_BALANCER_URL = "http://localhost:8080"

def send_request(request_type, request_id):
    """Send a single request"""
    try:
        if request_type == "video":
            url = f"{LOAD_BALANCER_URL}/video/movie_{request_id}.mp4"
        elif request_type == "api":
            url = f"{LOAD_BALANCER_URL}/api/users/{request_id}"
        elif request_type == "image":
            url = f"{LOAD_BALANCER_URL}/image/photo_{request_id}.jpg"
        else:
            url = LOAD_BALANCER_URL
        
        start = time.time()
        response = requests.get(url, timeout=15)
        duration = time.time() - start
        
        data = response.json()
        server = data.get("server", "unknown")
        optimized = data.get("optimized", False)
        
        status = "✓" if optimized else "⚠️"
        print(f"{status} {request_type.upper():6} → {server:8} ({duration*1000:5.0f}ms)")
        
        return {"success": True, "duration": duration, "server": server}
    
    except Exception as e:
        print(f"✗ {request_type.upper():6} → ERROR ({e})")
        return {"success": False, "error": str(e)}

def continuous_load(duration_seconds=30, requests_per_second=5):
    """
    Send continuous load to see dashboard in action
    """
    print(f"\n{'='*60}")
    print(f"🚀 Starting continuous load test")
    print(f"   Duration: {duration_seconds} seconds")
    print(f"   Rate: {requests_per_second} requests/second")
    print(f"   Watch the dashboard: http://localhost:9000")
    print(f"{'='*60}\n")
    
    request_types = ["video", "api", "image"]
    start_time = time.time()
    request_count = 0
    
    while time.time() - start_time < duration_seconds:
        # Send burst of requests
        with ThreadPoolExecutor(max_workers=requests_per_second) as executor:
            futures = []
            for _ in range(requests_per_second):
                req_type = random.choice(request_types)
                future = executor.submit(send_request, req_type, request_count)
                futures.append(future)
                request_count += 1
            
            # Wait for all requests to complete
            for future in futures:
                future.result()
        
        # Wait for next second
        time.sleep(1)
    
    print(f"\n{'='*60}")
    print(f"✓ Load test completed!")
    print(f"   Total requests sent: {request_count}")
    print(f"{'='*60}\n")

def burst_load(num_requests=50, concurrent=10):
    """
    Send a burst of requests
    """
    print(f"\n{'='*60}")
    print(f"💥 Burst load test")
    print(f"   Requests: {num_requests}")
    print(f"   Concurrent: {concurrent}")
    print(f"{'='*60}\n")
    
    request_types = ["video", "api", "image"]
    results = []
    
    with ThreadPoolExecutor(max_workers=concurrent) as executor:
        futures = []
        for i in range(num_requests):
            req_type = random.choice(request_types)
            future = executor.submit(send_request, req_type, i)
            futures.append(future)
        
        for future in futures:
            result = future.result()
            results.append(result)
    
    successful = [r for r in results if r.get("success")]
    print(f"\n{'='*60}")
    print(f"Results:")
    print(f"   Successful: {len(successful)}/{num_requests}")
    if successful:
        avg_duration = sum(r["duration"] for r in successful) / len(successful)
        print(f"   Avg latency: {avg_duration*1000:.2f}ms")
    print(f"{'='*60}\n")

def test_content_routing():
    """
    Test that L7 content-based routing works correctly
    """
    print(f"\n{'='*60}")
    print(f"🧪 Testing Content-Based Routing (L7 Feature)")
    print(f"{'='*60}\n")
    
    tests = [
        ("video", "video/test.mp4", "ServerA", "Video server"),
        ("api", "api/users/123", "ServerB", "API server"),
        ("image", "image/logo.png", "ServerC", "Image server"),
    ]
    
    print("Sending different request types and checking routing...\n")
    
    for req_type, path, expected_server, expected_type in tests:
        try:
            response = requests.get(f"{LOAD_BALANCER_URL}/{path}")
            data = response.json()
            actual_server = data.get("server")
            optimized = data.get("optimized", False)
            
            if actual_server == expected_server and optimized:
                print(f"✓ {req_type.upper():6} request → {actual_server} ({expected_type}) ✅")
            else:
                print(f"⚠️  {req_type.upper():6} request → {actual_server} (expected {expected_server})")
        except Exception as e:
            print(f"✗ {req_type.upper():6} request failed: {e}")
        
        time.sleep(0.5)
    
    print(f"\n{'='*60}")
    print(f"Content-based routing test completed!")
    print(f"With L7, each request type goes to its optimized server.")
    print(f"{'='*60}\n")

def demonstrate_fault_tolerance():
    """
    Demonstrate fault tolerance
    """
    print(f"\n{'='*60}")
    print(f"🛡️  Fault Tolerance Demonstration")
    print(f"{'='*60}\n")
    print("Instructions:")
    print("1. This test will send continuous requests")
    print("2. Manually stop one of the backend servers (Ctrl+C)")
    print("3. Watch the dashboard show the server as unhealthy")
    print("4. Observe that requests continue to work on remaining servers")
    print("5. Restart the server and see it recover")
    print("\nPress Enter to start (or Ctrl+C to cancel)...")
    
    try:
        input()
    except KeyboardInterrupt:
        print("\nCancelled.")
        return
    
    print("\nSending requests... Stop a backend server now!\n")
    
    try:
        continuous_load(duration_seconds=60, requests_per_second=3)
    except KeyboardInterrupt:
        print("\n\nStopped by user.")

def menu():
    """Interactive menu"""
    while True:
        print(f"\n{'='*60}")
        print("Load Balancer Test Client")
        print(f"{'='*60}")
        print("\n1. Continuous Load (watch dashboard)")
        print("2. Burst Load Test")
        print("3. Test Content-Based Routing (L7)")
        print("4. Demonstrate Fault Tolerance")
        print("5. Single Request Test")
        print("6. Exit")
        print("\nDashboard URL: http://localhost:9000")
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == "1":
            duration = input("Duration in seconds (default 30): ").strip()
            duration = int(duration) if duration else 30
            rate = input("Requests per second (default 5): ").strip()
            rate = int(rate) if rate else 5
            continuous_load(duration, rate)
        
        elif choice == "2":
            num = input("Number of requests (default 50): ").strip()
            num = int(num) if num else 50
            concurrent = input("Concurrent requests (default 10): ").strip()
            concurrent = int(concurrent) if concurrent else 10
            burst_load(num, concurrent)
        
        elif choice == "3":
            test_content_routing()
        
        elif choice == "4":
            demonstrate_fault_tolerance()
        
        elif choice == "5":
            req_type = input("Request type (video/api/image): ").strip().lower()
            if req_type in ["video", "api", "image"]:
                send_request(req_type, 1)
            else:
                print("Invalid type. Use: video, api, or image")
        
        elif choice == "6":
            print("\nGoodbye!")
            break
        
        else:
            print("Invalid option. Please select 1-6.")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Command line mode
        if sys.argv[1] == "continuous":
            duration = int(sys.argv[2]) if len(sys.argv) > 2 else 30
            continuous_load(duration)
        elif sys.argv[1] == "burst":
            num = int(sys.argv[2]) if len(sys.argv) > 2 else 50
            burst_load(num)
        elif sys.argv[1] == "test":
            test_content_routing()
    else:
        # Interactive menu
        menu()