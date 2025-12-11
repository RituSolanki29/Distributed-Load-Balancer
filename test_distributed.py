"""
Distributed Test Client for Laptop 2
Sends requests to Load Balancer on Laptop 1
"""

import requests
import time
import random
from concurrent.futures import ThreadPoolExecutor
import json
import socket

# Load configuration
def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ config.json not found!")
        print("Please ensure config.json is in the same directory.")
        return None

CONFIG = load_config()

if CONFIG:
    LOAD_BALANCER_IP = CONFIG['load_balancer']['ip']
    LOAD_BALANCER_PORT = CONFIG['load_balancer']['port']
    LOAD_BALANCER_URL = f"http://{LOAD_BALANCER_IP}:{LOAD_BALANCER_PORT}"
else:
    LOAD_BALANCER_URL = "http://192.168.1.100:8080"  # Fallback
    print(f"⚠️  Using fallback URL: {LOAD_BALANCER_URL}")

def get_my_ip():
    """Get this laptop's IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "unknown"

def send_request(request_type, request_id):
    """Send a single request to the load balancer"""
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
    """Send continuous load to see distributed system in action"""
    print(f"\n{'='*70}")
    print(f"🚀 DISTRIBUTED LOAD TEST FROM LAPTOP 2")
    print(f"{'='*70}")
    print(f"\n📡 Configuration:")
    print(f"   My IP: {get_my_ip()}")
    print(f"   Target Load Balancer: {LOAD_BALANCER_URL}")
    print(f"   Duration: {duration_seconds} seconds")
    print(f"   Rate: {requests_per_second} requests/second")
    print(f"\n{'='*70}\n")
    
    request_types = ["video", "api", "image"]
    weights = [0.3, 0.5, 0.2]  # 30% video, 50% API, 20% image
    
    start_time = time.time()
    request_count = 0
    success_count = 0
    
    print("Sending requests...\n")
    
    while time.time() - start_time < duration_seconds:
        with ThreadPoolExecutor(max_workers=requests_per_second) as executor:
            futures = []
            for _ in range(requests_per_second):
                req_type = random.choices(request_types, weights=weights)[0]
                future = executor.submit(send_request, req_type, request_count)
                futures.append(future)
                request_count += 1
            
            for future in futures:
                result = future.result()
                if result.get("success"):
                    success_count += 1
        
        elapsed = int(time.time() - start_time)
        remaining = duration_seconds - elapsed
        print(f"   Progress: {elapsed}/{duration_seconds}s | Sent: {request_count} | Success: {success_count} | Remaining: {remaining}s")
        
        time.sleep(1)
    
    print(f"\n{'='*70}")
    print(f"✓ Test Completed!")
    print(f"{'='*70}")
    print(f"   Total requests: {request_count}")
    print(f"   Successful: {success_count} ({success_count/request_count*100:.1f}%)")
    print(f"   Duration: {duration_seconds} seconds")
    print(f"{'='*70}\n")

def burst_test(num_requests=50, concurrent=10):
    """Send a burst of requests"""
    print(f"\n{'='*70}")
    print(f"💥 BURST TEST FROM LAPTOP 2")
    print(f"{'='*70}")
    print(f"\n📡 Configuration:")
    print(f"   My IP: {get_my_ip()}")
    print(f"   Target: {LOAD_BALANCER_URL}")
    print(f"   Requests: {num_requests}")
    print(f"   Concurrent: {concurrent}")
    print(f"\n{'='*70}\n")
    
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
    print(f"\n{'='*70}")
    print(f"Results:")
    print(f"   Successful: {len(successful)}/{num_requests}")
    if successful:
        avg_duration = sum(r["duration"] for r in successful) / len(successful)
        print(f"   Avg latency: {avg_duration*1000:.2f}ms")
    print(f"{'='*70}\n")

def test_connectivity():
    """Test if load balancer is reachable"""
    print(f"\n{'='*70}")
    print(f"🔍 CONNECTIVITY TEST")
    print(f"{'='*70}\n")
    print(f"My IP: {get_my_ip()}")
    print(f"Testing connection to: {LOAD_BALANCER_URL}\n")
    
    try:
        response = requests.get(f"{LOAD_BALANCER_URL}/lb/stats", timeout=5)
        print("✓ Successfully connected to Load Balancer!")
        
        stats = response.json()
        print(f"\nLoad Balancer Status:")
        print(f"   Algorithm: {stats.get('algorithm', 'unknown')}")
        print(f"   Total Requests: {stats.get('total_requests', 0)}")
        print(f"\nBackend Servers:")
        for backend in stats.get('backends', []):
            status = "🟢" if backend.get('healthy') else "🔴"
            print(f"   {status} {backend.get('name')} ({backend.get('type')}) at {backend.get('host')}:{backend.get('port')}")
        
        print(f"\n{'='*70}")
        print("✓ All systems operational!")
        print(f"{'='*70}\n")
        return True
        
    except Exception as e:
        print(f"✗ Failed to connect: {e}\n")
        print("Troubleshooting:")
        print("1. Is Laptop 1 running? (Load Balancer should be active)")
        print("2. Are you on the same network?")
        print("3. Check firewall settings on Laptop 1")
        print(f"4. Try pinging Laptop 1: ping {LOAD_BALANCER_IP}")
        print(f"{'='*70}\n")
        return False

def menu():
    """Interactive menu"""
    while True:
        print(f"\n{'='*70}")
        print(f"🧪 DISTRIBUTED TEST CLIENT - LAPTOP 2")
        print(f"{'='*70}")
        print(f"\nLoad Balancer: {LOAD_BALANCER_URL}")
        print(f"My IP: {get_my_ip()}")
        print("\n1. 🔍 Test Connectivity")
        print("2. 🚀 Continuous Load (30 seconds)")
        print("3. 💥 Burst Test (50 requests)")
        print("4. ⚙️  Custom Continuous Load")
        print("5. ❌ Exit")
        
        choice = input("\n👉 Select option (1-5): ").strip()
        
        if choice == "1":
            test_connectivity()
        
        elif choice == "2":
            if test_connectivity():
                continuous_load(30, 5)
        
        elif choice == "3":
            if test_connectivity():
                burst_test(50, 10)
        
        elif choice == "4":
            if test_connectivity():
                try:
                    duration = int(input("Duration (seconds, default 30): ") or "30")
                    rate = int(input("Requests per second (default 5): ") or "5")
                    continuous_load(duration, rate)
                except ValueError:
                    print("❌ Invalid input. Using defaults.")
                    continuous_load(30, 5)
        
        elif choice == "5":
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid option. Please select 1-5.")

if __name__ == '__main__':
    print("\n" + "="*70)
    print("📡 DISTRIBUTED LOAD BALANCER TEST CLIENT")
    print("="*70)
    print("\nThis is LAPTOP 2 - Sending requests to Load Balancer on LAPTOP 1")
    print(f"Target: {LOAD_BALANCER_URL}")
    print("="*70)
    
    menu()