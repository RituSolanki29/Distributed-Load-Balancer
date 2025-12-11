"""
Automated Algorithm Comparison Test
This script runs tests on all algorithms while you watch the dashboard update in real-time!
"""

import requests
import time
import random
from concurrent.futures import ThreadPoolExecutor
import sys

LOAD_BALANCER_URL = "http://localhost:8080"

def change_algorithm(algorithm):
    """Change load balancing algorithm"""
    try:
        response = requests.post(
            f"{LOAD_BALANCER_URL}/lb/algorithm",
            json={"algorithm": algorithm},
            timeout=5
        )
        return response.ok
    except:
        return False

def send_mixed_requests(duration_seconds, rate_per_second):
    """Send a realistic mix of requests"""
    request_types = ["video", "api", "image"]
    weights = [0.3, 0.5, 0.2]  # 30% video, 50% API, 20% image
    
    start_time = time.time()
    request_count = 0
    
    print(f"   Sending {rate_per_second} requests/second for {duration_seconds} seconds...")
    
    while time.time() - start_time < duration_seconds:
        with ThreadPoolExecutor(max_workers=rate_per_second) as executor:
            for _ in range(rate_per_second):
                req_type = random.choices(request_types, weights=weights)[0]
                
                try:
                    if req_type == "video":
                        url = f"{LOAD_BALANCER_URL}/video/movie_{request_count}.mp4"
                    elif req_type == "api":
                        url = f"{LOAD_BALANCER_URL}/api/users/{request_count}"
                    else:
                        url = f"{LOAD_BALANCER_URL}/image/photo_{request_count}.jpg"
                    
                    executor.submit(requests.get, url, timeout=10)
                    request_count += 1
                
                except:
                    pass
        
        # Show progress
        elapsed = int(time.time() - start_time)
        remaining = duration_seconds - elapsed
        print(f"   Progress: {elapsed}/{duration_seconds}s | {request_count} requests sent | {remaining}s remaining", end='\r')
        
        time.sleep(1)
    
    print(f"\n   ✓ Completed {request_count} requests")
    return request_count

def run_comparison_test():
    """
    Run automated comparison test across all algorithms
    Perfect for demonstrating differences in real-time on the dashboard!
    """
    
    print("\n" + "="*70)
    print("🔬 AUTOMATED ALGORITHM COMPARISON TEST")
    print("="*70)
    print("\n📊 This test will:")
    print("   1. Test each algorithm for 30 seconds")
    print("   2. Send realistic mixed workload (video, API, image requests)")
    print("   3. Update dashboard graphs in REAL-TIME")
    print("   4. Generate comparison data")
    print("\n⚠️  IMPORTANT: Keep the dashboard open in your browser!")
    print("   URL: http://localhost:9000")
    print("\nThe test will take approximately 2-3 minutes total.")
    print("\nPress Enter to start or Ctrl+C to cancel...")
    
    try:
        input()
    except KeyboardInterrupt:
        print("\n\nCancelled.")
        return
    
    algorithms = [
        ("content-based", "Content-Based (L7) - Should show 100% optimization"),
        ("round-robin", "Round Robin - Random distribution"),
        ("least-connections", "Least Connections - Load-based routing"),
        ("file-size", "File-Size Based - Optimized for large files")
    ]
    
    print("\n" + "="*70)
    print("🚀 STARTING COMPARISON TEST")
    print("="*70)
    
    for i, (algo, description) in enumerate(algorithms, 1):
        print(f"\n{'─'*70}")
        print(f"Test {i}/4: {algo.upper()}")
        print(f"Description: {description}")
        print(f"{'─'*70}")
        
        # Change algorithm
        print(f"\n1️⃣  Switching to {algo}...")
        if change_algorithm(algo):
            print(f"   ✓ Algorithm changed to: {algo}")
        else:
            print(f"   ✗ Failed to change algorithm")
            continue
        
        # Wait for switch to take effect
        print("2️⃣  Waiting 3 seconds for algorithm to activate...")
        time.sleep(3)
        
        # Run test
        print(f"3️⃣  Running test workload...")
        test_duration = 30  # seconds
        requests_per_second = 5
        
        total_requests = send_mixed_requests(test_duration, requests_per_second)
        
        print(f"\n   ✓ Test complete: {total_requests} requests sent")
        
        # Pause between tests
        if i < len(algorithms):
            print(f"\n4️⃣  Pausing 5 seconds before next test...")
            print("   (Check the dashboard to see the graphs updating!)")
            time.sleep(5)
    
    print("\n" + "="*70)
    print("✅ ALL TESTS COMPLETED!")
    print("="*70)
    print("\n📊 Check your dashboard at: http://localhost:9000")
    print("\nYou should now see:")
    print("   ✓ Bar chart showing requests per server")
    print("   ✓ Line chart showing response time trends")
    print("   ✓ Optimization rate comparison across algorithms")
    print("   ✓ Updated comparison table with performance metrics")
    print("\n📸 Perfect time to take screenshots for your report!")
    print("\nKey observations to note:")
    print("   • Content-Based should show ~100% optimization")
    print("   • Round-Robin should show ~33% optimization")
    print("   • Different algorithms show different distributions")
    print("   • Response times vary by algorithm efficiency")
    
    print("\n" + "="*70)

def quick_visual_test():
    """
    Quick test to show visual differences between algorithms
    Great for live demos!
    """
    print("\n" + "="*70)
    print("⚡ QUICK VISUAL COMPARISON")
    print("="*70)
    print("\nThis will rapidly switch between algorithms")
    print("Watch the dashboard to see routing behavior change!")
    print("\nPress Enter to start...")
    
    try:
        input()
    except KeyboardInterrupt:
        print("\nCancelled.")
        return
    
    algorithms = ["content-based", "round-robin", "least-connections", "file-size"]
    
    print("\n🎬 Starting visual demo...\n")
    
    for cycle in range(2):  # Do 2 cycles
        for algo in algorithms:
            print(f"\n📍 Switching to: {algo.upper()}")
            change_algorithm(algo)
            time.sleep(2)
            
            print(f"   Sending 20 test requests...")
            send_mixed_requests(10, 2)  # 10 seconds, 2 req/s
            
            print("   ⏸️  Pause to observe...")
            time.sleep(3)
    
    print("\n✓ Visual demo complete!")
    print("Notice how different algorithms route requests differently!")

def continuous_comparison(duration_minutes=5):
    """
    Run continuous comparison across algorithms
    Cycles through all algorithms while sending steady traffic
    """
    print(f"\n{'='*70}")
    print(f"🔄 CONTINUOUS COMPARISON TEST ({duration_minutes} minutes)")
    print(f"{'='*70}")
    print("\nThis test cycles through all algorithms continuously")
    print("Perfect for seeing long-term trends and collecting data")
    print(f"\nTotal duration: {duration_minutes} minutes")
    print("\nPress Enter to start...")
    
    try:
        input()
    except KeyboardInterrupt:
        print("\nCancelled.")
        return
    
    algorithms = ["content-based", "round-robin", "least-connections", "file-size"]
    start_time = time.time()
    total_duration = duration_minutes * 60
    cycle = 0
    
    print(f"\n🚀 Starting continuous test...\n")
    
    while time.time() - start_time < total_duration:
        cycle += 1
        algo = algorithms[(cycle - 1) % len(algorithms)]
        
        elapsed_mins = int((time.time() - start_time) / 60)
        remaining_mins = duration_minutes - elapsed_mins
        
        print(f"\n{'─'*70}")
        print(f"Cycle {cycle} | Algorithm: {algo.upper()} | Time: {elapsed_mins}/{duration_minutes} min | Remaining: {remaining_mins} min")
        print(f"{'─'*70}")
        
        change_algorithm(algo)
        time.sleep(2)
        
        # Run for 30 seconds on this algorithm
        send_mixed_requests(30, 3)
        
        time.sleep(3)
    
    print(f"\n{'='*70}")
    print("✅ CONTINUOUS TEST COMPLETED")
    print(f"{'='*70}")
    print(f"\nTotal runtime: {duration_minutes} minutes")
    print("Check dashboard for comprehensive comparison data!")

def stress_test():
    """
    High-load stress test to see performance under pressure
    """
    print("\n" + "="*70)
    print("💪 STRESS TEST")
    print("="*70)
    print("\nThis will send HIGH LOAD to test performance limits")
    print("Great for demonstrating fault tolerance and load balancing")
    print("\n⚠️  Warning: This will generate significant traffic!")
    print("\nPress Enter to start or Ctrl+C to cancel...")
    
    try:
        input()
    except KeyboardInterrupt:
        print("\nCancelled.")
        return
    
    print("\n🔥 Starting stress test with content-based algorithm...\n")
    
    change_algorithm("content-based")
    time.sleep(2)
    
    # Gradually increase load
    loads = [
        (10, 5, "Warm-up"),
        (20, 10, "Medium load"),
        (30, 20, "High load"),
        (20, 30, "Peak load"),
        (10, 20, "Cool down")
    ]
    
    for duration, rate, phase in loads:
        print(f"\n📊 {phase}: {rate} requests/second for {duration} seconds")
        send_mixed_requests(duration, rate)
        time.sleep(2)
    
    print("\n✅ Stress test complete!")
    print("Check dashboard to see how the system handled the load!")

def menu():
    """Interactive menu for different test types"""
    while True:
        print("\n" + "="*70)
        print("🧪 DASHBOARD GRAPH TESTING TOOL")
        print("="*70)
        print("\n📊 Dashboard URL: http://localhost:9000")
        print("\nSelect a test to run:")
        print("\n1. 🔬 Full Comparison Test (2-3 minutes)")
        print("   → Tests all 4 algorithms sequentially")
        print("   → Best for report data and screenshots")
        print("\n2. ⚡ Quick Visual Demo (2 minutes)")
        print("   → Rapid switching between algorithms")
        print("   → Great for live presentations")
        print("\n3. 🔄 Continuous Comparison (5 minutes)")
        print("   → Cycles through algorithms continuously")
        print("   → Best for long-term trend analysis")
        print("\n4. 💪 Stress Test")
        print("   → High-load performance test")
        print("   → Tests system limits")
        print("\n5. ❌ Exit")
        
        choice = input("\n👉 Select option (1-5): ").strip()
        
        if choice == "1":
            run_comparison_test()
        elif choice == "2":
            quick_visual_test()
        elif choice == "3":
            duration = input("\nDuration in minutes (default 5): ").strip()
            duration = int(duration) if duration.isdigit() else 5
            continuous_comparison(duration)
        elif choice == "4":
            stress_test()
        elif choice == "5":
            print("\n👋 Goodbye!")
            break
        else:
            print("\n❌ Invalid option. Please select 1-5.")

if __name__ == '__main__':
    print("\n" + "="*70)
    print("📊 LOAD BALANCER DASHBOARD GRAPH TESTING TOOL")
    print("="*70)
    print("\n✅ Prerequisites:")
    print("   • Load balancer running on port 8080")
    print("   • Dashboard open in browser: http://localhost:9000")
    print("   • All backend servers running")
    
    # Check if load balancer is accessible
    try:
        response = requests.get(f"{LOAD_BALANCER_URL}/lb/stats", timeout=2)
        print("\n✓ Load balancer detected and ready!")
        
        if len(sys.argv) > 1:
            if sys.argv[1] == "auto":
                run_comparison_test()
            elif sys.argv[1] == "quick":
                quick_visual_test()
            elif sys.argv[1] == "continuous":
                duration = int(sys.argv[2]) if len(sys.argv) > 2 else 5
                continuous_comparison(duration)
            elif sys.argv[1] == "stress":
                stress_test()
        else:
            menu()
    
    except:
        print("\n❌ Error: Cannot connect to load balancer!")
        print("\n🔧 Please ensure:")
        print("   1. Load balancer is running: python load_balancer.py")
        print("   2. Backend servers are running")
        print("   3. Port 8080 is not blocked")