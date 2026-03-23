from pathlib import Path
import os
import requests
from dotenv import load_dotenv

project_root = Path(__file__).resolve().parent.parent
load_dotenv(project_root / ".env")

API_TOKEN = os.getenv("FREELANCER_API_TOKEN")

BASE_URL = "https://www.freelancer.com/api/projects/0.1/projects/active/"

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}"
}


def search_projects(query, limit=10):
    params = {
        "query": query,
        "limit": limit
    }

    try:
        response = requests.get(BASE_URL, headers=HEADERS, params=params, timeout=20)
        print("Status code:", response.status_code)

        if response.status_code != 200:
            print("Response text:", response.text)
            return []

        data = response.json()
        projects = data.get("result", {}).get("projects", [])
        return normalize_projects(projects)

    except Exception as e:
        print(f"Request failed: {e}")
        return []


def normalize_projects(raw_projects):
    normalized = []

    for p in raw_projects:
        project = type("Project", (), {})()

        project.id = p.get("id")
        project.title = p.get("title")
        project.description = p.get("description")
        project.currency = (p.get("currency") or {}).get("code")
        project.min_budget = (p.get("budget") or {}).get("minimum")
        project.max_budget = (p.get("budget") or {}).get("maximum")
        project.bid_count = (p.get("bid_stats") or {}).get("bid_count")
        seo_url = p.get("seo_url", "")
        project.url = f"https://www.freelancer.com/projects/{seo_url}" if seo_url else ""
        project.posted_at = p.get("submitdate")

        normalized.append(project)

    return normalized