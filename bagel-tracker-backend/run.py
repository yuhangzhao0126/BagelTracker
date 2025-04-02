import os
from app import create_app
from flask import Flask, jsonify

app = create_app()

# Add a test API endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "success", "message": "Backend is running!"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))  # Use Azure's PORT
    app.run(debug=True, host='0.0.0.0', port=port)
