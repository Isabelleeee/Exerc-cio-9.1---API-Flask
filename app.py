import os  # Importante: precisamos do 'os' para ler a porta da Azure
from flask import Flask, jsonify

app = Flask(__name__)

# Rota básica do hello world (Part A)
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
    # Em produção (Azure), o debug=True causa problemas de segurança e instabilidade.
    # Além disso, a Azure injeta a porta dinamicamente. Se não houver, usa a 8000 local.
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)