import subprocess

JIRA_ISSUE_KEY = "SUP-1"
BRANCH_NAME = f"feature/{JIRA_ISSUE_KEY.lower()}-password-update"

commit_message = input("Enter your commit message: ")
full_commit_message = f"{JIRA_ISSUE_KEY}: {commit_message}"

# Create branch
subprocess.run(["git", "checkout", "-b", BRANCH_NAME])

# Add all changes
subprocess.run(["git", "add", "."])

# Commit with Jira issue key
subprocess.run(["git", "commit", "-m", full_commit_message])

# Push branch to origin
subprocess.run(["git", "push", "-u", "origin", BRANCH_NAME])

print(f"Branch {BRANCH_NAME} created and pushed with commit: {full_commit_message}") 