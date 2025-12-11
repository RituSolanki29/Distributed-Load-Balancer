from flask import Flask, jsonify, request
import sys
import time
import random
import threading

app = Flask(__name__)

# Server configuration from command line arguments
SERVER_NAME = sys.argv[1] if len(sys.argv) > 1 else "ServerA"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 5001
SERVER_TYPE = sys.argv[3] if len(sys.argv) > 3 else "general"

# Server statistics
stats = {
    "total_requests": 0,
    "video_requests": 0,
    "api_requests": 0,
    "image_requests": 0,
    "start_time": time.time()
}

# Simulate different processing times based on server type and request type
PROCESSING_TIMES = {
    "video": {
        "video": 0.05,   # Video server handles video fast
        "api": 0.25,     # Video server handles API slow
        "image": 0.15,   # Video server handles images medium
        "default": 0.10
    },
    "api": {
        "video": 0.30,   # API server handles video slow
        "api": 0.03,     # API server handles API fast
        "image": 0.20,   # API server handles images medium
        "default": 0.15
    },
    "image": {
        "video": 0.25,   # Image server handles video slow
        "api": 0.20,     # Image server handles API medium
        "image": 0.04,   # Image server handles images fast
        "default": 0.12
    },
    "general": {
        "video": 0.15,
        "api": 0.15,
        "image": 0.15,
        "default": 0.15
    }
}

def get_processing_time(request_type):
    """Get processing time based on server type and request type"""
    return PROCESSING_TIMES[SERVER_TYPE].get(request_type, 
           PROCESSING_TIMES[SERVER_TYPE]["default"])

@app.route('/')
def home():
    stats["total_requests"] += 1
    time.sleep(get_processing_time("default"))
    
    return jsonify({
        "server": SERVER_NAME,
        "type": SERVER_TYPE,
        "message": f"Hello from {SERVER_NAME} ({SERVER_TYPE} server)",
        "timestamp": time.time(),
        "port": PORT
    })

@app.route('/health')
def health():
    """Health check endpoint for load balancer"""
    uptime = time.time() - stats["start_time"]
    return jsonify({
        "status": "healthy",
        "server": SERVER_NAME,
        "type": SERVER_TYPE,
        "uptime_seconds": round(uptime, 2),
        "total_requests": stats["total_requests"]
    }), 200

@app.route('/video/<path:filename>')
def video(filename):
    """Simulate video streaming request"""
    stats["total_requests"] += 1
    stats["video_requests"] += 1
    
    processing_time = get_processing_time("video")
    time.sleep(processing_time)
    
    # Simulate video metadata
    file_size_mb = random.randint(50, 500)
    
    response = {
        "server": SERVER_NAME,
        "server_type": SERVER_TYPE,
        "content_type": "video",
        "filename": filename,
        "size_mb": file_size_mb,
        "processing_time_ms": round(processing_time * 1000, 2),
        "optimized": SERVER_TYPE == "video",
        "warning": None if SERVER_TYPE == "video" else f"⚠️  Video request handled by {SERVER_TYPE} server (suboptimal)"
    }
    
    return jsonify(response)

@app.route('/api/<path:endpoint>')
def api(endpoint):
    """Simulate API request"""
    stats["total_requests"] += 1
    stats["api_requests"] += 1
    
    processing_time = get_processing_time("api")
    time.sleep(processing_time)
    
    response = {
        "server": SERVER_NAME,
        "server_type": SERVER_TYPE,
        "content_type": "api",
        "endpoint": endpoint,
        "processing_time_ms": round(processing_time * 1000, 2),
        "optimized": SERVER_TYPE == "api",
        "data": {"id": random.randint(1, 1000), "status": "success"},
        "warning": None if SERVER_TYPE == "api" else f"⚠️  API request handled by {SERVER_TYPE} server (suboptimal)"
    }
    
    return jsonify(response)

@app.route('/image/<path:filename>')
def image(filename):
    """Simulate image request"""
    stats["total_requests"] += 1
    stats["image_requests"] += 1
    
    processing_time = get_processing_time("image")
    time.sleep(processing_time)
    
    file_size_kb = random.randint(10, 500)
    
    response = {
        "server": SERVER_NAME,
        "server_type": SERVER_TYPE,
        "content_type": "image",
        "filename": filename,
        "size_kb": file_size_kb,
        "processing_time_ms": round(processing_time * 1000, 2),
        "optimized": SERVER_TYPE == "image",
        "warning": None if SERVER_TYPE == "image" else f"⚠️  Image request handled by {SERVER_TYPE} server (suboptimal)"
    }
    
    return jsonify(response)

@app.route('/stats')
def server_stats():
    """Return server statistics"""
    uptime = time.time() - stats["start_time"]
    return jsonify({
        "server": SERVER_NAME,
        "type": SERVER_TYPE,
        "port": PORT,
        "uptime_seconds": round(uptime, 2),
        "total_requests": stats["total_requests"],
        "video_requests": stats["video_requests"],
        "api_requests": stats["api_requests"],
        "image_requests": stats["image_requests"]
    })

@app.route('/crash')
def crash():
    """Simulate server crash for fault tolerance demo"""
    def delayed_crash():
        time.sleep(1)
        print(f"\n💥 {SERVER_NAME} CRASHING (simulated)...\n")
        import os
        os._exit(1)
    
    threading.Thread(target=delayed_crash, daemon=True).start()
    return jsonify({"message": f"{SERVER_NAME} will crash in 1 second..."}), 200

if __name__ == '__main__':
    print(f"\n{'='*60}")
    print(f"🚀 Starting {SERVER_NAME}")
    print(f"   Type: {SERVER_TYPE}")
    print(f"   Port: {PORT}")
    print(f"   Optimized for: {SERVER_TYPE} requests")
    print(f"{'='*60}\n")
    
    app.run(host='0.0.0.0', port=PORT, debug=False, threaded=True)