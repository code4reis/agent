from flask import Flask, jsonify
from flask_cors import CORS
import json, os

app = Flask(__name__)
CORS(app)

arquivo = 'consumo.json'

@app.route('/consumo', methods=['GET'])
def obter_consumo():

    if not os.path.exists(arquivo):
        return jsonify({"erro": "Arquivo não encontrado"}), 404

    try: 
        with open(arquivo, 'r') as file:
            dados_consumo = json.load(file)
        return jsonify(dados_consumo)
    except FileNotFoundError:
        return jsonify({"erro": "Arquivo não encontrado"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Erro ao decodiciador o JSON"}), 500
    