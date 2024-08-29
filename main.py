from config import *
from flask import Flask
from flask_cors import CORS

# Instancia Flask
app = Flask(__name__)

# CORS para permitir requisições de mesma origem http
CORS(app)

# Páginas
from speed import *
from bandmonitor import *

if __name__ == '__main__':
    iniciar_monitoramento()

    ssl_context = None
    if SSL_CERTIFICATE:
        ssl_context = (CRT_PATH, KEY_PATH)

    app.run(
        host=CLIENT_IP,
        port=int(CLIENT_PORT),
        ssl_context=ssl_context,
        debug=True
    )