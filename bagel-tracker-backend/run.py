from app import create_app
from flask import Flask, jsonify

app = create_app()

# Add a simple test API endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "success", "message": "Backend is running!"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)