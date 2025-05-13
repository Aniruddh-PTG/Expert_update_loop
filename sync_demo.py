import streamlit as st
import requests
import base64
import os
from docx import Document
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("REPO")
BRANCH = os.getenv("BRANCH", "main")

def github_upload(file_path, file_content, commit_message):
    """Upload a file to GitHub repo using the API."""
    api_url = f"https://api.github.com/repos/{REPO}/contents/{file_path}"
    # Get the SHA if the file exists (for update)
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

st.set_page_config(layout="wide")

# Directories for files
os.makedirs("testlead_files", exist_ok=True)
os.makedirs("modified_files", exist_ok=True)

st.title("BRD/Test Lead GitHub Sync Demo")

col1, col2 = st.columns(2)

# --- Test Lead Section ---
with col1:
    st.header("Test Lead")
    uploaded = st.file_uploader("Upload Test Lead .docx", type="docx")
    upload_success = False
    if uploaded and GITHUB_TOKEN and REPO:
        # Upload original file
        orig_name = uploaded.name
        orig_bytes = uploaded.getbuffer()
        ok1, resp1 = github_upload(orig_name, orig_bytes, f"Upload {orig_name} from Streamlit")
        # Upload modified file
        base, ext = os.path.splitext(orig_name)
        mod_name = f"{base} modified{ext}"
        ok2, resp2 = github_upload(mod_name, orig_bytes, f"Upload {mod_name} from Streamlit")
        if ok1 and ok2:
            st.success(f"Uploaded {orig_name} and {mod_name} to GitHub!")
            upload_success = True
        else:
            st.error(f"Failed to upload: {resp1.get('message', '')} {resp2.get('message', '')}")

# --- Product Owner Section ---
with col2:
    st.header("Product Owner")
    st.write("Latest files for review (from GitHub):")
    if uploaded and upload_success:
        base, ext = os.path.splitext(uploaded.name)
        orig_name = uploaded.name
        mod_name = f"{base} modified{ext}"
        orig_url = f"https://github.com/{REPO}/blob/{BRANCH}/{orig_name}?raw=true"
        mod_url = f"https://github.com/{REPO}/blob/{BRANCH}/{mod_name}?raw=true"
        st.markdown(
            f"<span style='color:#7bb241;font-weight:600'>{orig_name}</span> &nbsp; "
            f"[<a href='{orig_url}' style='color:#7bb241;text-decoration:underline;'>Open Link</a>]",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<span style='color:#7bb241;font-weight:600'>{mod_name}</span> &nbsp; "
            f"[<a href='{mod_url}' style='color:#7bb241;text-decoration:underline;'>Open Link</a>]",
            unsafe_allow_html=True
        )
    else:
        st.info("No files uploaded yet.")

st.caption("Note: .env file is used for GitHub credentials and repo info.")