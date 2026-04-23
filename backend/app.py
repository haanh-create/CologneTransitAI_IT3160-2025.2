from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from engine import TransitEngine
import os

app = Flask(__name__)
CORS(app)

# Path to the data file
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cologne_network.json")
FRONTEND_PATH = os.path.join(os.path.dirname(__file__), "..", "frontend")

# Initialize engine
engine = TransitEngine(DATA_PATH)

# --- Serve Frontend Static Files ---
@app.route('/')
def index():
    return send_from_directory(FRONTEND_PATH, 'index.html')

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory(os.path.join(FRONTEND_PATH, 'js'), filename)

# --- API Routes ---
@app.route('/api/network', methods=['GET'])
def get_network():
    return jsonify(engine.get_network_data())

@app.route('/api/lines', methods=['GET'])
def get_lines():
    return jsonify({
        "all_lines": engine.get_all_lines(),
        "disabled_lines": list(engine.disabled_lines)
    })

@app.route('/api/admin/toggle-line', methods=['POST'])
def toggle_line():
    data = request.json
    line_name = data.get('line')
    disabled = data.get('disabled', True)
    
    if not line_name:
        return jsonify({"error": "Line name is required"}), 400
        
    disabled_list = engine.toggle_line(line_name, disabled)
    return jsonify({"success": True, "disabled_lines": disabled_list})

@app.route('/api/find-path', methods=['POST'])
def find_path():
    data = request.json
    start_id = data.get('start_node')
    end_id = data.get('end_node')
    
    if not start_id or not end_id:
        return jsonify({"error": "Start and End nodes are required"}), 400
        
    result = engine.find_path(int(start_id), int(end_id))
    return jsonify(result)

if __name__ == '__main__':
    # Check if data exists, if not, print warning
    if not os.path.exists(DATA_PATH):
        print(f"CRITICAL: Data file not found at {DATA_PATH}. Please run scripts/fetch_data.py first.")
    
    app.run(debug=True, port=5000)
