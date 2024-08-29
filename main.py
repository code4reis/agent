from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

from speed import *
from bandmonitor import *

if __name__ == '__main__':
    iniciar_monitoramento()
    app.run(host='192.168.128.57', port=5000, debug=True)