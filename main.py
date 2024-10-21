import google.generativeai as genai
import os
import sys
import json
from github import Github

# Configure Google AI
api_key = os.environ.get("INPUT_GOOGLE_API_KEY")
if not api_key:
    print("Error: GOOGLE_API_KEY is not set")
    sys.exit(1)

genai.configure(api_key=api_key)

# Get GitHub context
github_token = os.environ.get("INPUT_GITHUB_TOKEN")
if not github_token:
    print("Error: GITHUB_TOKEN is not set")
    sys.exit(1)

github_repository = os.environ.get("GITHUB_REPOSITORY")
github_event_path = os.environ.get("GITHUB_EVENT_PATH")

if not github_repository or not github_event_path:
    print("Error: Unable to get GitHub context")
    sys.exit(1)

# Read the event payload
with open(github_event_path, 'r') as f:
    event_data = json.load(f)

pull_request_number = event_data.get('pull_request', {}).get('number')
if not pull_request_number:
    print("Error: This action can only run on pull requests")
    sys.exit(1)

# Read the Terragrunt plan
tf_plan = os.environ.get("INPUT_TF_PLAN", "")
if not tf_plan:
    print("Error: No Terragrunt plan provided")
    sys.exit(1)

# Generate explanation
prompt = f"""
// ... (keep the existing prompt) ...
"""

model = genai.GenerativeModel('gemini-pro')
response = model.generate_content(prompt)

explanation = response.text

# Interact with GitHub
g = Github(github_token)
repo = g.get_repo(github_repository)
pr = repo.get_pull(pull_request_number)

# Delete existing comments with the specified heading
comments = pr.get_issue_comments()
for comment in comments:
    if comment.body.startswith("## Terragrunt Plan Explanation"):
        comment.delete()

# Post new comment to GitHub
comment_body = f"## Terragrunt Plan Explanation\n\n{explanation}"
pr.create_issue_comment(comment_body)

print("Old explanations deleted and new explanation posted as a comment on the pull request.")
