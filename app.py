from flask import Flask, request, abort

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    return request.remote_addr
# app.run()