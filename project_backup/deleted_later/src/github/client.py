from github import Github
from typing import Tuple, Optional

class GitHubClient:
    def __init__(self, token: str, repo: str, owner: str):
        self.github = Github(token)
        self.repo = self.github.get_repo(f"{owner}/{repo}")
    
    def get_document_versions(self, file_path: str) -> Tuple[str, str]:
        """
        Get the previous and current versions of a document from GitHub.
        Returns tuple of (previous_content, current_content)
        """
        try:
            # Get the file's commit history
            commits = self.repo.get_commits(path=file_path)
            
            # Get current version
            current_content = self.repo.get_contents(file_path).decoded_content.decode()
            
            # Get previous version
            if commits.totalCount > 1:
                previous_commit = commits[1]  # Skip the current commit
                previous_content = self.repo.get_contents(
                    file_path, 
                    ref=previous_commit.sha
                ).decoded_content.decode()
            else:
                previous_content = current_content
                
            return previous_content, current_content
            
        except Exception as e:
            raise Exception(f"Error fetching document versions: {str(e)}")
    
    def update_document(self, file_path: str, content: str, commit_message: str) -> bool:
        """
        Update a document in the repository
        """
        try:
            current_file = self.repo.get_contents(file_path)
            self.repo.update_file(
                path=file_path,
                message=commit_message,
                content=content,
                sha=current_file.sha
            )
            return True
        except Exception as e:
            raise Exception(f"Error updating document: {str(e)}")
    
    def get_file_diff(self, file_path: str) -> Optional[str]:
        """
        Get the diff between the last two versions of a file
        """
        try:
            commits = self.repo.get_commits(path=file_path)
            if commits.totalCount < 2:
                return None
                
            current_commit = commits[0]
            previous_commit = commits[1]
            
            diff = self.repo.compare(
                previous_commit.sha,
                current_commit.sha
            )
            
            return diff.diff
        except Exception as e:
            raise Exception(f"Error getting file diff: {str(e)}") 