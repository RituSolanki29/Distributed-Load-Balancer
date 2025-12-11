from flask import Flask, render_template, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

LOAD_BALANCER_URL = "http://localhost:8080"

@app.route('/')
def dashboard():
    """Serve the monitoring dashboard"""
    return render_template('dashboard.html')

@app.route('/simulate')
def simulate():
    """Serve the network simulation page"""
    return render_template('simulate.html')

@app.route('/api/stats')
def get_stats():
    """Proxy stats from load balancer"""
    try:
        response = requests.get(f"{LOAD_BALANCER_URL}/lb/stats", timeout=2)
        return jsonify(response.json())
    except:
        return jsonify({"error": "Load balancer not available"}), 503

@app.route('/api/algorithm', methods=['POST'])
def change_algorithm():
    """Change load balancing algorithm"""
    try:
        import flask
        data = flask.request.json
        response = requests.post(
            f"{LOAD_BALANCER_URL}/lb/algorithm",
            json=data,
            timeout=2
        )
        return jsonify(response.json()), response.status_code
    except:
        return jsonify({"error": "Failed to change algorithm"}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("📊 Dashboard Server Starting")
    print("   URL: http://localhost:9000")
    print("   Load Balancer: http://localhost:8080")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=9000, debug=False)