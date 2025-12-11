from flask import Flask, request, Response, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import requests
import threading
import time
from collections import defaultdict
import logging
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/load_balancer.log'),
        logging.StreamHandler()
    ]
)

# Backend server configuration
BACKENDS = [
    {"name": "ServerA", "url": "http://localhost:5001", "type": "video", "healthy": True, "color": "#FF6B6B"},
    {"name": "ServerB", "url": "http://localhost:5002", "type": "api", "healthy": True, "color": "#4ECDC4"},
    {"name": "ServerC", "url": "http://localhost:5003", "type": "image", "healthy": True, "color": "#95E1D3"}
]

# Metrics tracking
active_connections = defaultdict(int)
total_requests = defaultdict(int)
failed_requests = defaultdict(int)
response_times = defaultdict(list)
request_history = []  # Last 50 requests for visualization
current_index = 0
lock = threading.Lock()

# Algorithm selection
ALGORITHM = "content-based"

def get_healthy_backends():
    """Return only healthy backends"""
    return [b for b in BACKENDS if b["healthy"]]

def broadcast_metrics():
    """Broadcast current metrics to all connected dashboard clients"""
    metrics_data = {
        "algorithm": ALGORITHM,
        "backends": [{
            "name": b["name"],
            "type": b["type"],
            "healthy": b["healthy"],
            "active": active_connections[b["name"]],
            "total": total_requests[b["name"]],
            "failed": failed_requests[b["name"]],
            "avg_response": round(sum(response_times[b["name"]][-10:]) / len(response_times[b["name"]][-10:]) * 1000, 2) if response_times[b["name"]] else 0,
            "color": b["color"]
        } for b in BACKENDS],
        "recent_requests": request_history[-20:]  # Last 20 requests
    }
    socketio.emit('metrics_update', metrics_data)

def round_robin():
    """Round-robin algorithm"""
    global current_index
    backends = get_healthy_backends()
    if not backends:
        return None
    
    with lock:
        backend = backends[current_index % len(backends)]
        current_index += 1
    
    return backend

def least_connections():
    """Least connections algorithm"""
    backends = get_healthy_backends()
    if not backends:
        return None
    
    return min(backends, key=lambda b: active_connections[b["name"]])

def content_based_routing(path):
    """Content-based routing - L7 intelligence"""
    backends = get_healthy_backends()
    if not backends:
        return None
    
    # Route based on URL path
    if path.startswith('video/'):
        video_servers = [b for b in backends if b["type"] == "video"]
        if video_servers:
            # Among video servers, pick least busy
            return min(video_servers, key=lambda b: active_connections[b["name"]])
    
    elif path.startswith('api/'):
        api_servers = [b for b in backends if b["type"] == "api"]
        if api_servers:
            return min(api_servers, key=lambda b: active_connections[b["name"]])
    
    elif path.startswith('image/'):
        image_servers = [b for b in backends if b["type"] == "image"]
        if image_servers:
            return min(image_servers, key=lambda b: active_connections[b["name"]])
    
    # Fallback to round-robin
    return round_robin()

def file_size_based_routing(path):
    """File-size based routing"""
    backends = get_healthy_backends()
    if not backends:
        return None
    
    large_file_extensions = ['.mp4', '.mkv', '.avi', '.zip', '.iso']
    is_large_file = any(path.endswith(ext) for ext in large_file_extensions) or 'video/' in path
    
    if is_large_file:
        # Large files go to least busy server
        return min(backends, key=lambda b: active_connections[b["name"]])
    else:
        return round_robin()

def select_backend(path="/"):
    """Select backend based on algorithm"""
    if ALGORITHM == "round-robin":
        return round_robin()
    elif ALGORITHM == "least-connections":
        return least_connections()
    elif ALGORITHM == "content-based":
        return content_based_routing(path)
    elif ALGORITHM == "file-size":
        return file_size_based_routing(path)
    else:
        return round_robin()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    """Main proxy function"""
    start_time = time.time()
    
    backend = select_backend(path)
    
    if not backend:
        logging.error("No healthy backends available")
        return jsonify({"error": "No healthy backends available"}), 503
    
    backend_name = backend["name"]
    backend_url = backend["url"]
    
    # Track connection
    with lock:
        active_connections[backend_name] += 1
        total_requests[backend_name] += 1
    
    # Determine request type for logging
    request_type = "default"
    if path.startswith('video/'):
        request_type = "video"
    elif path.startswith('api/'):
        request_type = "api"
    elif path.startswith('image/'):
        request_type = "image"
    
    try:
        target_url = f"{backend_url}/{path}"
        
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers={k: v for k, v in request.headers if k.lower() != 'host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
            timeout=10
        )
        
        duration = time.time() - start_time
        response_times[backend_name].append(duration)
        
        # Log request for dashboard
        with lock:
            request_history.append({
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "path": f"/{path}",
                "type": request_type,
                "backend": backend_name,
                "duration": round(duration * 1000, 2),
                "status": "success",
                "optimized": backend["type"] == request_type
            })
            if len(request_history) > 50:
                request_history.pop(0)
        
        # Broadcast to dashboard
        broadcast_metrics()
        
        logging.info(f"✓ {request_type.upper()} /{path} → {backend_name} ({duration*1000:.0f}ms)")
        
        return Response(
            resp.content,
            status=resp.status_code,
            headers=dict(resp.headers)
        )
    
    except Exception as e:
        duration = time.time() - start_time
        
        with lock:
            failed_requests[backend_name] += 1
            request_history.append({
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "path": f"/{path}",
                "type": request_type,
                "backend": backend_name,
                "duration": round(duration * 1000, 2),
                "status": "failed",
                "optimized": False
            })
            if len(request_history) > 50:
                request_history.pop(0)
        
        broadcast_metrics()
        
        logging.error(f"✗ {backend_name} error: {e}")
        
        return jsonify({
            "error": "Backend unavailable",
            "backend": backend_name
        }), 502
    
    finally:
        with lock:
            active_connections[backend_name] -= 1

@app.route('/lb/stats')
def stats():
    """Load balancer statistics API"""
    return jsonify({
        "algorithm": ALGORITHM,
        "backends": [{
            "name": b["name"],
            "url": b["url"],
            "type": b["type"],
            "healthy": b["healthy"],
            "active_connections": active_connections[b["name"]],
            "total_requests": total_requests[b["name"]],
            "failed_requests": failed_requests[b["name"]],
            "avg_response_time_ms": round(sum(response_times[b["name"]][-10:]) / len(response_times[b["name"]][-10:]) * 1000, 2) if response_times[b["name"]] else 0
        } for b in BACKENDS],
        "total_requests": sum(total_requests.values()),
        "total_failures": sum(failed_requests.values())
    })

@app.route('/lb/algorithm', methods=['POST'])
def change_algorithm():
    """Change load balancing algorithm"""
    global ALGORITHM
    data = request.json
    new_algo = data.get('algorithm')
    
    valid = ['round-robin', 'least-connections', 'content-based', 'file-size']
    if new_algo in valid:
        ALGORITHM = new_algo
        logging.info(f"Algorithm changed to: {ALGORITHM}")
        broadcast_metrics()
        return jsonify({"message": f"Algorithm changed to {ALGORITHM}"}), 200
    
    return jsonify({"error": "Invalid algorithm"}), 400

def health_check():
    """Health checker background thread"""
    logging.info("Health checker started")
    
    while True:
        for backend in BACKENDS:
            try:
                resp = requests.get(f"{backend['url']}/health", timeout=3)
                was_healthy = backend["healthy"]
                backend["healthy"] = (resp.status_code == 200)
                
                if was_healthy and not backend["healthy"]:
                    logging.warning(f"🔴 {backend['name']} is now UNHEALTHY")
                    broadcast_metrics()
                elif not was_healthy and backend["healthy"]:
                    logging.info(f"🟢 {backend['name']} recovered")
                    broadcast_metrics()
            
            except Exception as e:
                was_healthy = backend["healthy"]
                backend["healthy"] = False
                
                if was_healthy:
                    logging.warning(f"🔴 {backend['name']} health check failed")
                    broadcast_metrics()
        
        time.sleep(5)

if __name__ == '__main__':
    import os
    os.makedirs('logs', exist_ok=True)
    
    # Start health checker
    health_thread = threading.Thread(target=health_check, daemon=True)
    health_thread.start()
    
    logging.info(f"\n{'='*60}")
    logging.info(f"🔄 Load Balancer Starting")
    logging.info(f"   Algorithm: {ALGORITHM}")
    logging.info(f"   Port: 8080")
    logging.info(f"   Dashboard: http://localhost:9000")
    logging.info(f"{'='*60}\n")
    
    # Run with socketio
    socketio.run(app, host='0.0.0.0', port=8080, debug=False, allow_unsafe_werkzeug=True)