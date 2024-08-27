from flask import Flask, jsonify
from flask_cors import CORS
import speedtest
import threading

app = Flask(__name__)
CORS(app)

# Variável global para armazenar o último resultado do teste de velocidade
last_result = None

# Função para realizar o teste de velocidade
def run_speedtest():
    global last_result
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        
        download_speed = st.download() / 1_000_000  # converte para Mbps
        upload_speed = st.upload() / 1_000_000      # converte para Mbps
        ping = st.results.ping
        
        resultados = {
            "download_speed_mbps": download_speed,
            "upload_speed_mbps": upload_speed,
            "ping_ms": ping,
            "server": st.results.server
        }
        
        last_result = resultados
    
    except speedtest.ConfigRetrievalError as e:
        print(f"ConfigRetrievalError: {e}")
        last_result = {"error": "Unable to retrieve configuration from Speedtest."}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        last_result = {"error": "An unexpected error occurred during the speed test."}

@app.route('/speedtest', methods=['GET'])
def speedtest_route():
    global last_result
    if not last_result:
        return jsonify({"status": "Test in progress"}), 202
    else:
        result = last_result
        last_result = None
        return jsonify(result)

@app.route('/start_speedtest', methods=['POST'])
def start_speedtest():
    thread = threading.Thread(target=run_speedtest)
    thread.start()
    return jsonify({"status": "Speed test started"}), 200
