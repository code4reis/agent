from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/domaintest')
def domaintest():
    data = request.json
