import streamlit as st
import requests
import base64
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("REPO")
BRANCH = os.getenv("BRANCH", "main")

def get_file_from_github(file_path):
    """Download a file from GitHub repo using the REST API."""
    api_url = f"https://api.github.com/repos/{REPO}/contents/{file_path}?ref={BRANCH}"
    r = requests.get(api_url, headers={"Authorization": f"token {GITHUB_TOKEN}"})
    if r.status_code == 200:
        content = base64.b64decode(r.json()["content"])
        return content
    else:
        return None

def github_upload(file_path, file_content, commit_message):
    """Upload a file to GitHub repo using the REST API."""
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
        if ok1:
            st.success(f"Uploaded {orig_name} to GitHub!")
            upload_success = True
        else:
            st.error(f"Failed to upload: {resp1}")
    elif not GITHUB_TOKEN:
        st.error("No GitHub token found in .env. Please set GITHUB_TOKEN.")

    # --- Update Modified File Button ---
    st.markdown("---")
    st.subheader("Sync Modified File")
    if st.button("Update Modified File on GitHub"):
        # Download the latest Test Lead file from GitHub
        orig_name = "Password Test Case Updated.docx"
        mod_name = "Password Test Case Updated modified.docx"
        content = get_file_from_github(orig_name)
        if content:
            ok, resp = github_upload(mod_name, content, f"Update {mod_name} from Streamlit")
            if ok:
                st.success(f"Updated {mod_name} on GitHub!")
            else:
                st.error(f"Failed to update: {resp}")
        else:
            st.error(f"Could not fetch {orig_name} from GitHub.")

# --- Product Owner Section ---
with col2:
    st.header("Product Owner")
    st.write("Latest files for review (from GitHub):")
    orig_name = "Password Test Case Updated.docx"
    mod_name = "Password Test Case Updated modified.docx"
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

st.caption("Note: .env file is used for GitHub credentials and repo info. Use the Update button to sync the modified file after any change.")