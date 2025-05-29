import uuid
import requests
import os
from typing import TypedDict
from dotenv import load_dotenv

load_dotenv()

JIRA_BASE_URL = "https://diyaverma1967.atlassian.net"
JIRA_API_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY", "PT")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_ORG = os.getenv("GITHUB_ORG", "diyaverma1967")

def create_jira_ticket(title: str, description: str) -> dict:
    url = f"{JIRA_BASE_URL}/rest/api/3/issue"
    auth = (JIRA_API_EMAIL, JIRA_API_TOKEN)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {
        "fields": {
            "project": {"key": JIRA_PROJECT_KEY},
            "summary": title[:100],
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": description[:255]}
                        ]
                    }
                ]
            },
            "issuetype": {"name": "Task"}
        }
    }
    try:
        response = requests.post(url, json=payload, headers=headers, auth=auth)
        response.raise_for_status()
        data = response.json()
        print(f"[JIRA] Ticket created: {data['key']}")
        return {
            "ticket_id": data["key"],
            "description": description,
            "status": "created"
        }
    except Exception as e:
        print(f"[JIRA ERROR] {e}")
        return {"ticket_id": "JIRA-FAIL", "description": description, "status": "error"}

def create_github_repo(title: str, description: str) -> dict:
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    payload = {
        "name": title[:80],
        "description": description[:200],
        "private": True,
        "auto_init": True
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        username = GITHUB_ORG
        print(f"[GitHub] Repo created: {title}")
        return {
            "repo_name": title,
            "description": f"https://github.com/{username}/{title}",
            "status": "repo-created"
        }
    except Exception as e:
        print(f"[GITHUB ERROR] {e}")
        return {"repo_name": title, "description": description, "status": "error"}
