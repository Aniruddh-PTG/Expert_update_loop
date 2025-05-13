import os
import base64
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import io
from docx import Document
from flask_cors import CORS

from flask_cors import CORS
app = Flask(__name__)
CORS(app)

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("REPO")
BRANCH = os.getenv("BRANCH", "main")

app = Flask(__name__)
CORS(app)

def get_file_from_github(file_path):
    api_url = f"https://api.github.com/repos/{REPO}/contents/{file_path}?ref={BRANCH}"
    r = requests.get(api_url, headers={"Authorization": f"token {GITHUB_TOKEN}"})
    if r.status_code == 200:
        content = base64.b64decode(r.json()["content"])
        return content
    else:
        return None

def github_upload(file_path, file_content, commit_message):
    api_url = f"https://api.github.com/repos/{REPO}/contents/{file_path}"
    r = requests.get(api_url + f"?ref={BRANCH}", headers={"Authorization": f"token {GITHUB_TOKEN}"})
    sha = r.json().get("sha") if r.status_code == 200 else None
    data = {
        "message": commit_message,
        "content": base64.b64encode(file_content).decode(),
        "branch": BRANCH
    }
    if sha:
        data["sha"] = sha
    resp = requests.put(api_url, json=data, headers={"Authorization": f"token {GITHUB_TOKEN}"})
    return resp.status_code in (200, 201), resp.json()

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    orig_name = file.filename
    orig_bytes = file.read()
    ok, resp = github_upload(orig_name, orig_bytes, f"Upload {orig_name} from React")
    return jsonify({"success": ok, "response": resp})

@app.route("/sync-modified", methods=["POST"])
def sync_modified():
    orig_name = "Password Test Case Updated.docx"
    mod_name = "Password Test Case Updated modified.docx"
    content = get_file_from_github(orig_name)
    if content:
        # Modify the DOCX: append a paragraph
        doc = Document(io.BytesIO(content))
        doc.add_paragraph("MODIFIED BY BACKEND")
        out_buf = io.BytesIO()
        doc.save(out_buf)
        out_buf.seek(0)
        mod_content = out_buf.read()
        ok, resp = github_upload(mod_name, mod_content, f"Update {mod_name} from React (with modification)")
        return jsonify({"success": ok, "response": resp})
    else:
        return jsonify({"success": False, "error": f"Could not fetch {orig_name} from GitHub."})

if __name__ == "__main__":
    app.run(debug=True, port=5000) 