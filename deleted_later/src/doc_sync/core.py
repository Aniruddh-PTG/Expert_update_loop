import boto3
from pathlib import Path
from typing import List, Dict, Tuple
from docx import Document
from git import Repo
import difflib

class DocumentSync:
    def __init__(self, repo_path: str, bedrock_client=None):
        self.repo = Repo(repo_path)
        self.bedrock_client = bedrock_client or boto3.client('bedrock-runtime')
        
    def get_latest_changes(self, file_path: str) -> Tuple[str, str]:
        """Get the current and previous versions of a file"""
        commits = list(self.repo.iter_commits(paths=file_path, max_count=2))
        if len(commits) < 2:
            return None, None
            
        current = commits[0].tree[file_path].data_stream.read()
        previous = commits[1].tree[file_path].data_stream.read()
        return current, previous
        
    def extract_docx_text(self, docx_content: bytes) -> str:
        """Extract text from docx content"""
        doc = Document(docx_content)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
        
    def compute_semantic_diff(self, old_text: str, new_text: str) -> List[Dict]:
        """Compute semantic differences between texts"""
        diff = difflib.unified_diff(
            old_text.splitlines(),
            new_text.splitlines(),
            lineterm=''
        )
        return list(diff)
        
    def get_claude_explanation(self, diff: List[str]) -> str:
        """Get Claude's explanation of the changes"""
        prompt = f"""Please explain the following changes in plain English, focusing only on what changed without suggesting any actions:

{''.join(diff)}

Explanation:"""
        
        response = self.bedrock_client.invoke_model(
            modelId='anthropic.claude-v2',
            body=prompt
        )
        return response['body'].read().decode() 