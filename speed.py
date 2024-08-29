from main import app
from flask import jsonify
import speedtest

# Variável global para armazenar o último resultado do teste de velocidade
last_result = None

# Função para realizar o teste de velocidade
@app.route('/start_speedtest', methods=['GET'])
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
        return jsonify(last_result)
    
    except speedtest.ConfigRetrievalError as e:
        print(f"ConfigRetrievalError: {e}")
        last_result = {"error": "Unable to retrieve configuration from Speedtest."}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        last_result = {"error": "An unexpected error occurred during the speed test."}
