from flask import Flask, request, Response
from pathlib import Path
from werkzeug.utils import secure_filename
import json

from server.auth import auth
from mmanager import MMangaer
app = Flask(__name__)
manager = MMangaer()

@app.route("/")
def hello():
    return "Hello Word"

@app.route("/download_and_upload_to_gdrive", methods=["POST", "PUT"])
def youtube():
    m_content = request.get_json()
    if not m_content: return Response("error: data not found", 400)
    if auth("pass"):
        for m in m_content:
            print(m)
        return json.dumps(m_content)
        # return manager.download_and_upload_to_gdrive()
    else:
        return "auth error"

@app.route("/upload_file", methods=["POST", "PUT"])
def upload_file():
    def is_allowed_file(filename):
        ALLOWED_EXTENSIONS = ('.txt', '.pdf', '.png', '.jpg', '.jpeg', '.gif')
        if str(Path(filename).stem) in ALLOWED_EXTENSIONS:
            return True

    files = request.files
    if not files:
        return "files not found"
    
    for f in files:
        filename = secure_filename( request.files[f].filename )
        if is_allowed_file(filename):
            files[f].save(filename)
            return json.dumps({"post_id": f, "filename":filename})
    
    return "done"
    





if __name__ == "__main__":
    app.run()