import time
from flask import Flask, request, abort, Response, stream_with_context, url_for
app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/music', methods=["POST"])
def hello():
    def gen():
        yield ("h")
        yield ("e")
        yield ("l")
        yield ("l")
        yield ("o")
        time.sleep(10)
        yield "\n"
        yield "w"
        yield "ord"
    return Response(stream_with_context(gen()))

@app.route('/upload/', methods=["post"])
def upload():
    for f in request.files:
        if request.files[f].mimetype == "audio/mpeg":
        request.files[f].save("./az.mp3")
        print(request.files[f].mimetype)
        print(request.files[f].name)
        print(request.files[f].filename)
        print(request.files[f].content_type)
    # print(files)
    # print(dir(request.files[f]))
    return "bb"
# @app.teardown_request
# def show_teardown(exception):
#     print('after with block')
#     time.sleep(10)
#     print("end")

