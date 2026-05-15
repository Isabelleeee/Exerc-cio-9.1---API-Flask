import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulando um banco de dados em memória para testar os métodos
db_items = {
    1: {"nome": "Configuração Inicial", "status": "concluído"},
    2: {"nome": "Deploy Azure", "status": "pendente"}
}


# ==========================================
# a) Rota básica do hello world
# ==========================================
@app.route('/')
def hello_world():
    return "Hello, World!"


# ==========================================
# b) RESTful API endpoints (GET, POST, PUT, DELETE)
# ==========================================

# 1. GET: Retorna todos os itens (ou um status geral, como você fez)
@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify({
        "message": "Dados recuperados com sucesso!",
        "status": "success",
        "version": "1.0",
        "data": db_items
    }), 200


# 2. POST: Cria um novo item
@app.route('/api/items', methods=['POST'])
def create_item():
    novo_dado = request.get_json()  # Pega o JSON enviado no body da requisição

    # Gera um novo ID (pega o maior ID atual e soma 1)
    novo_id = max(db_items.keys()) + 1 if db_items else 1
    db_items[novo_id] = novo_dado

    return jsonify({
        "message": "Item criado com sucesso!",
        "status": "success",
        "id_criado": novo_id,
        "data": novo_dado
    }), 201  # 201 é o status code padrão para "Created"


# 3. PUT: Atualiza um item existente pelo ID
@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    if item_id not in db_items:
        return jsonify({"error": "Item não encontrado"}), 404

    dados_atualizados = request.get_json()
    db_items[item_id].update(dados_atualizados)  # Atualiza os dados no dicionário

    return jsonify({
        "message": "Item atualizado com sucesso!",
        "status": "success",
        "data": db_items[item_id]
    }), 200


# 4. DELETE: Remove um item existente pelo ID
@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    if item_id in db_items:
        item_removido = db_items.pop(item_id)  # Remove do dicionário
        return jsonify({
            "message": f"Item {item_id} deletado com sucesso!",
            "status": "success",
            "data_removida": item_removido
        }), 200

    return jsonify({"error": "Item não encontrado"}), 404


if __name__ == '__main__':
    # Em produção (Azure), o debug=True causa problemas de segurança e instabilidade.
    # Além disso, a Azure injeta a porta dinamicamente. Se não houver, usa a 8000 local.
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)