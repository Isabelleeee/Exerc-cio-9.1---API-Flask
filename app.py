from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# 1. O Modelo de Dados (Como o objeto deve ser estruturado)
class Produto(BaseModel):
    id: int
    nome: str
    preco: float


# Nosso "Banco de Dados" temporário (Lista de dicionários)
banco_produtos = [
    {"id": 1, "nome": "Sensor Ultrassônico", "preco": 15.50},
    {"id": 2, "nome": "Arduino Uno", "preco": 89.90}
]


# --- 1. GET (Listar todos) ---
@app.get("/produtos")
def listar_todos():
    return banco_produtos


# --- 2. POST (Criar/Inserir um novo produto) ---
@app.post("/produtos")
def criar_produto(novo_produto: Produto):
    # Regra de negócio: não deixa criar com ID repetido
    for produto in banco_produtos:
        if produto["id"] == novo_produto.id:
            raise HTTPException(status_code=400, detail="Esse ID já existe!")

    # Transforma o objeto do Pydantic em um dicionário Python comum e salva
    banco_produtos.append(novo_produto.dict())
    return {"status": "Sucesso", "item_criado": novo_produto}


# --- 3. PUT (Atualizar um produto existente pelo ID) ---
@app.put("/produtos/{produto_id}")
def atualizar_produto(produto_id: int, dados_atualizados: Produto):
    # Procura o produto na lista pelo ID informado na URL
    for index, produto in enumerate(banco_produtos):
        if produto["id"] == produto_id:
            # Atualiza a posição com os novos dados
            banco_produtos[index] = dados_atualizados.dict()
            return {"status": "Atualizado com sucesso", "item": dados_atualizados}

    # Se varrer a lista toda e não achar o ID:
    raise HTTPException(status_code=404, detail="Produto não encontrado")


# --- 4. DELETE (Remover um produto pelo ID) ---
@app.delete("/produtos/{produto_id}")
def deletar_produto(produto_id: int):
    for index, produto in enumerate(banco_produtos):
        if produto["id"] == produto_id:
            banco_produtos.pop(index)  # Remove da lista
            return {"status": f"Produto {produto_id} removido com sucesso"}

    raise HTTPException(status_code=404, detail="Produto não encontrado")