
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from controller import AppController

# --- App Setup ---
app = Flask(__name__)
CORS(app) # Allow requests from the React frontend

# --- Initialize Controller ---
controller = AppController()

# --- API Routes ---

@app.route('/colorize-layers', methods=['POST'])
def handle_colorize_layers():
    if 'red_file' not in request.files or \
       'green_file' not in request.files or \
       'blue_file' not in request.files:
        return jsonify({"error": "Missing one or more channel files"}), 400

    files = {
        'red': request.files['red_file'],
        'green': request.files['green_file'],
        'blue': request.files['blue_file']
    }

    model_params = {
        'palette': request.form.get('palette', 'natural')
    }

    result, error = controller.colorize_layers(files, model_params)

    if error:
        return jsonify({"error": error}), 500
    
    return jsonify(result), 200

@app.route('/history', methods=['GET'])
def get_history():
    history = controller.get_history()
    return jsonify(history)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(controller.STATIC_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
