from flask import Flask, jsonify

app = Flask(__name__)

# Rout basica do hello world (Part A)
@app.route('/')
def hello_world():
    return "Hello, World!"

# RESTful API endpoint (Part B)
@app.route('/api/greet', methods=['GET'])
def get_greeting():
    data = {
        "message": "Hello, this is a RESTful response!",
        "status": "success",
        "version": "1.0"
    }
    return jsonify(data), 200

if __name__ == '__main__':
    # Running with debug=True allows for auto-reloading during development
    app.run(debug=True, port=5000)