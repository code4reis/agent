from flask import Flask, jsonify
import psutil, time, json, threading, os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

dados = 'consumo.json'
caminho_arquivo = os.path.abspath(dados)

# Lock para sincronização
monitoramento_lock = threading.Lock()
monitoramento_paused = threading.Event()

def byte2mega(bytes):
    # Converte os bytes para megabytes
    return bytes / 1024 / 1024

def monitoramento(intervalo=1):
    dados_iniciais = psutil.net_io_counters()
    
    while True:
        monitoramento_paused.wait()
        time.sleep(intervalo)
        
        dados_atual = psutil.net_io_counters()
        
        upload = dados_atual.bytes_sent - dados_iniciais.bytes_sent
        download = dados_atual.bytes_recv - dados_iniciais.bytes_recv
        
        mb_upload = byte2mega(upload)
        mb_download = byte2mega(download)
        
        dados_iniciais = dados_atual

        novo_dado = {
            'Hora': time.strftime('%d-%m-%Y %H:%M:%S'),
            "Download (MB)": round(mb_download, 2),
            "Upload (MB)": round(mb_upload, 2)
        }

        # Verifica se o consumo será maior que 1 Megabyte
        if mb_download > 1 or mb_upload > 1:
            with monitoramento_lock:
                try:
                    with open(dados, 'r') as file:
                        dados_consumo = json.load(file)
                except (FileNotFoundError, json.JSONDecodeError):
                    dados_consumo = []

                dados_consumo.append(novo_dado)

                with open(dados, 'w') as file:
                    json.dump(dados_consumo, file, indent=4)

def iniciar_monitoramento():
    global monitoramento_paused
    monitoramento_paused.set()  # Inicia o monitoramento
    thread = threading.Thread(target=monitoramento, daemon=True)
    thread.start()
    print('Monitoramento iniciado, arquivo = ', caminho_arquivo)

@app.route('/consumo', methods=['GET'])
def obter_consumo():
    global monitoramento_paused
    monitoramento_paused.clear()  # Pausa o monitoramento

    try:
        with open(dados, 'r') as file:
            dados_consumo = json.load(file)
        return jsonify(dados_consumo)
    except FileNotFoundError:
        return jsonify({"erro": "Arquivo não encontrado"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Erro ao decodificar o JSON"}), 500
    finally:
        monitoramento_paused.set()  # Retoma o monitoramento


    monitoramento_lock.release()