import requests
import time
from collections import defaultdict
import json

LOAD_BALANCER_URL = "http://localhost:8080"

def change_algorithm(algorithm):
    """Change load balancing algorithm"""
    try:
        response = requests.post(
            f"{LOAD_BALANCER_URL}/lb/algorithm",
            json={"algorithm": algorithm},
            timeout=5
        )
        if response.ok:
            print(f"✓ Changed to: {algorithm}")
            return True
        else:
            print(f"✗ Failed to change algorithm: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def get_stats():
    """Get current load balancer statistics"""
    try:
        response = requests.get(f"{LOAD_BALANCER_URL}/lb/stats", timeout=5)
        return response.json()
    except:
        return None

def reset_stats():
    """Note: In production, you'd restart the load balancer to reset stats"""
    print("Note: Stats are cumulative. For fresh comparison, restart load balancer.")

def send_test_requests(num_requests=30):
    """Send a mix of requests and measure results"""
    print(f"\n   Sending {num_requests} test requests...")
    
    results = {
        "video": [],
        "api": [],
        "image": []
    }
    
    request_types = ["video"] * 10 + ["api"] * 10 + ["image"] * 10
    
    for i, req_type in enumerate(request_types):
        try:
            if req_type == "video":
                url = f"{LOAD_BALANCER_URL}/video/test_{i}.mp4"
            elif req_type == "api":
                url = f"{LOAD_BALANCER_URL}/api/users/{i}"
            else:
                url = f"{LOAD_BALANCER_URL}/image/pic_{i}.jpg"
            
            start = time.time()
            response = requests.get(url, timeout=10)
            duration = time.time() - start
            
            data = response.json()
            server = data.get("server", "unknown")
            server_type = data.get("server_type", "unknown")
            optimized = data.get("optimized", False)
            
            results[req_type].append({
                "duration": duration,
                "server": server,
                "server_type": server_type,
                "optimized": optimized
            })
            
            # Show progress
            if (i + 1) % 10 == 0:
                print(f"   Progress: {i + 1}/{num_requests} requests")
        
        except Exception as e:
            print(f"   ✗ Request {i+1} failed: {e}")
        
        time.sleep(0.1)  # Small delay between requests
    
    return results

def analyze_results(algorithm_name, results):
    """Analyze test results"""
    print(f"\n{'='*60}")
    print(f"Results for: {algorithm_name.upper()}")
    print(f"{'='*60}")
    
    all_requests = []
    optimized_count = 0
    total_count = 0
    
    for req_type, requests in results.items():
        if not requests:
            continue
        
        print(f"\n{req_type.upper()} Requests ({len(requests)} total):")
        
        # Count servers
        server_counts = defaultdict(int)
        durations = []
        
        for req in requests:
            server_counts[req["server"]] += 1
            durations.append(req["duration"])
            all_requests.append(req)
            total_count += 1
            if req["optimized"]:
                optimized_count += 1
        
        # Show distribution
        for server, count in sorted(server_counts.items()):
            percentage = (count / len(requests)) * 100
            print(f"   {server}: {count} requests ({percentage:.1f}%)")
        
        # Show latency
        avg_latency = sum(durations) / len(durations) * 1000
        min_latency = min(durations) * 1000
        max_latency = max(durations) * 1000
        print(f"   Avg latency: {avg_latency:.2f}ms")
        print(f"   Min/Max: {min_latency:.2f}ms / {max_latency:.2f}ms")
    
    # Overall metrics
    if all_requests:
        all_durations = [r["duration"] for r in all_requests]
        avg_overall = sum(all_durations) / len(all_durations) * 1000
        optimization_rate = (optimized_count / total_count) * 100 if total_count > 0 else 0
        
        print(f"\n{'─'*60}")
        print(f"Overall Performance:")
        print(f"   Average latency: {avg_overall:.2f}ms")
        print(f"   Optimized routing: {optimized_count}/{total_count} ({optimization_rate:.1f}%)")
        print(f"{'─'*60}")
    
    return {
        "algorithm": algorithm_name,
        "avg_latency": avg_overall if all_requests else 0,
        "optimization_rate": optimization_rate if all_requests else 0,
        "total_requests": total_count
    }

def compare_all_algorithms():
    """Compare all load balancing algorithms"""
    print("\n" + "="*60)
    print("🔬 LOAD BALANCING ALGORITHM COMPARISON")
    print("="*60)
    print("\nThis will test all 4 algorithms with the same workload.")
    print("Each test sends 30 requests (10 video, 10 API, 10 image).")
    print("\nPress Enter to start or Ctrl+C to cancel...")
    
    try:
        input()
    except KeyboardInterrupt:
        print("\nCancelled.")
        return
    
    algorithms = [
        "content-based",
        "round-robin",
        "least-connections",
        "file-size"
    ]
    
    comparison_results = []
    
    for algo in algorithms:
        print(f"\n{'='*60}")
        print(f"Testing: {algo.upper()}")
        print(f"{'='*60}")
        
        # Change algorithm
        if not change_algorithm(algo):
            print(f"Skipping {algo} due to error")
            continue
        
        # Wait for algorithm to take effect
        time.sleep(2)
        
        # Run test
        results = send_test_requests(30)
        
        # Analyze
        summary = analyze_results(algo, results)
        comparison_results.append(summary)
        
        # Pause between tests
        print("\nWaiting 3 seconds before next test...")
        time.sleep(3)
    
    # Final comparison
    print("\n" + "="*60)
    print("📊 FINAL COMPARISON")
    print("="*60)
    print(f"\n{'Algorithm':<20} {'Avg Latency':<15} {'Optimization Rate':<20}")
    print("─" * 60)
    
    for result in comparison_results:
        print(f"{result['algorithm']:<20} "
              f"{result['avg_latency']:.2f}ms{'':<8} "
              f"{result['optimization_rate']:.1f}%")
    
    print("\n" + "="*60)
    
    # Find best
    if comparison_results:
        best_latency = min(comparison_results, key=lambda x: x['avg_latency'])
        best_optimization = max(comparison_results, key=lambda x: x['optimization_rate'])
        
        print(f"\n🏆 Best for latency: {best_latency['algorithm']} ({best_latency['avg_latency']:.2f}ms)")
        print(f"🎯 Best for optimization: {best_optimization['algorithm']} ({best_optimization['optimization_rate']:.1f}%)")
    
    # Save results
    with open('metrics/algorithm_comparison.json', 'w') as f:
        json.dump(comparison_results, f, indent=2)
    print(f"\n💾 Results saved to: metrics/algorithm_comparison.json")

def quick_test():
    """Quick visual test of current algorithm"""
    print("\n" + "="*60)
    print("🔍 QUICK ALGORITHM TEST")
    print("="*60)
    
    # Get current stats
    stats = get_stats()
    if stats:
        print(f"\nCurrent algorithm: {stats['algorithm']}")
    
    print("\nSending 10 test requests...")
    
    # Send varied requests
    test_requests = [
        ("video", "/video/movie.mp4"),
        ("api", "/api/users/1"),
        ("image", "/image/photo.jpg"),
        ("video", "/video/series.mp4"),
        ("api", "/api/products/123"),
        ("image", "/image/logo.png"),
        ("video", "/video/documentary.mp4"),
        ("api", "/api/orders/456"),
        ("image", "/image/banner.jpg"),
        ("api", "/api/search?q=test")
    ]
    
    print(f"\n{'Type':<8} {'Path':<30} {'Server':<12} {'Optimized':<10}")
    print("─" * 70)
    
    for req_type, path in test_requests:
        try:
            response = requests.get(f"{LOAD_BALANCER_URL}{path}", timeout=5)
            data = response.json()
            server = data.get("server", "?")
            optimized = data.get("optimized", False)
            opt_symbol = "✓" if optimized else "⚠️"
            
            print(f"{req_type:<8} {path:<30} {server:<12} {opt_symbol}")
            time.sleep(0.3)
        except Exception as e:
            print(f"{req_type:<8} {path:<30} ERROR")
    
    print("\n" + "="*60)

def menu():
    """Interactive menu"""
    while True:
        print("\n" + "="*60)
        print("🔀 ALGORITHM TESTING MENU")
        print("="*60)
        print("\n1. Quick Test (10 requests with current algorithm)")
        print("2. Full Comparison (Test all 4 algorithms)")
        print("3. Change Algorithm Manually")
        print("4. View Current Stats")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == "1":
            quick_test()
        
        elif choice == "2":
            compare_all_algorithms()
        
        elif choice == "3":
            print("\nAvailable algorithms:")
            print("  1. content-based")
            print("  2. round-robin")
            print("  3. least-connections")
            print("  4. file-size")
            
            algo_choice = input("\nSelect (1-4): ").strip()
            algorithms = ["content-based", "round-robin", "least-connections", "file-size"]
            
            if algo_choice in ["1", "2", "3", "4"]:
                algo = algorithms[int(algo_choice) - 1]
                change_algorithm(algo)
                print(f"\nRun option 1 to test the new algorithm!")
            else:
                print("Invalid choice")
        
        elif choice == "4":
            stats = get_stats()
            if stats:
                print(f"\n{'='*60}")
                print(f"Current Algorithm: {stats['algorithm']}")
                print(f"Total Requests: {stats['total_requests']}")
                print(f"\nServer Status:")
                for backend in stats['backends']:
                    status = "🟢 Healthy" if backend['healthy'] else "🔴 Unhealthy"
                    print(f"  {backend['name']} ({backend['type']}): {status}")
                    print(f"    Total: {backend['total_requests']}, Active: {backend['active_connections']}")
                print(f"{'='*60}")
            else:
                print("\n✗ Could not fetch stats. Is load balancer running?")
        
        elif choice == "5":
            print("\nGoodbye!")
            break
        
        else:
            print("Invalid option. Please select 1-5.")

if __name__ == '__main__':
    print("\n🔬 Load Balancer Algorithm Comparison Tool")
    print("Make sure load balancer is running on port 8080")
    
    # Check if load balancer is running
    try:
        requests.get(f"{LOAD_BALANCER_URL}/lb/stats", timeout=2)
        print("✓ Load balancer detected\n")
        menu()
    except:
        print("\n✗ Error: Load balancer not reachable at http://localhost:8080")
        print("Please start the load balancer first:")
        print("  python load_balancer.py")