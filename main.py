from flask import Flask
from flask_cors import CORS
from bandmonitor import *


app = Flask(__name__)
CORS(app)

if __name__ == '__main__':
    from speed import *
    from bandmonitor import *
    
    # init_db()
    app.run(host='192.168.128.57', port=5000, debug=True)