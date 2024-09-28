from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import sys

app = Flask(__name__)
CORS(app)  # This enables CORS for all routes
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

@app.route('/generate-text', methods=['GET', 'POST'])
def generate_text():
    app.logger.debug(f"Received request: {request.method} {request.path}")
    app.logger.debug(f"Request headers: {request.headers}")
    
    if request.method == 'GET':
        app.logger.debug("Handling GET request")
        return jsonify({"message": "GET request received"}), 200
    
    elif request.method == 'POST':
        app.logger.debug("Handling POST request")
        try:
            app.logger.debug(f"Request data: {request.get_data(as_text=True)}")
            if not request.is_json:
                app.logger.error("Request does not contain JSON data")
                return jsonify({"error": "Request must be JSON"}), 400
            
            input_text = request.json.get('text', '')
            generated_text = f"You said: {input_text}"
            
            app.logger.debug(f"Generated text: {generated_text}")
            return jsonify({"generatedText": generated_text}), 200
        except Exception as e:
            app.logger.error(f"Error processing request: {str(e)}", exc_info=True)
            return jsonify({"error": "An error occurred processing your request"}), 500

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(debug=True)