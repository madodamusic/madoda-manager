from flask import Flask

from mm_uploads.youtube.test02 import main as yt_auth
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello Word"

@app.route("/youtube")
def youtube():
    return yt_auth()
    # return "end auth: ", res

if __name__ == "__main__":
    app.run()