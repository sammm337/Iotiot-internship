import requests
import json
import os
import logging
import base64

# Directory setup
INPUT_FILE = "./Input/v_input.json"
OUTPUT_FILE = "./Config/v_fetchedData.json"
LOG_FILE = "./Logs/v_botactivity.log"

# GitHub API Base URL
GITHUB_API = "https://api.github.com/repos/{owner}/{repo}"

# Logging setup
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

def load_input():
    with open(INPUT_FILE, "r") as file:
        return json.load(file)

def fetch_repo_data(owner, repo):
    url = GITHUB_API.format(owner=owner, repo=repo)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    logging.error(f"Failed to fetch repo data for {owner}/{repo}")
    return None

def fetch_languages(owner, repo):
    url = f"{GITHUB_API.format(owner=owner, repo=repo)}/languages"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {}

def fetch_readme(owner, repo):
    url = f"{GITHUB_API.format(owner=owner, repo=repo)}/readme"
    response = requests.get(url)
    if response.status_code == 200:
        readme_content = response.json().get("content", "")
        readme_decoded = base64.b64decode(readme_content).decode("utf-8", errors="ignore")
        return readme_decoded
    return ""

def fetch_commits(owner, repo):
    url = f"{GITHUB_API.format(owner=owner, repo=repo)}/commits"
    response = requests.get(url)
    if response.status_code == 200:
        return [
            {
                "author": commit["commit"]["author"]["name"],
                "email": commit["commit"]["author"]["email"],
                "message": commit["commit"]["message"],
                "date": commit["commit"]["author"]["date"]
            }
            for commit in response.json()
        ]
    return []

def fetch_contributors(owner, repo):
    url = f"{GITHUB_API.format(owner=owner, repo=repo)}/contributors"
    response = requests.get(url)
    if response.status_code == 200:
        return [
            {"username": c["login"], "contributions": c["contributions"]}
            for c in response.json()
        ]
    return []

def main():
    input_data = load_input()
    owner = input_data["github_username"]
    repos = input_data["repos"]

    all_repo_data = []

    for repo_info in repos:
        repo = repo_info["repo_name"]
        logging.info(f"Processing repo {owner}/{repo}")

        repo_data = fetch_repo_data(owner, repo)
        if not repo_data:
            continue

        output_data = {
            "repo_name": repo_data.get("name"),
            "description": repo_data.get("description", ""),
            "created_at": repo_data.get("created_at"),
            "updated_at": repo_data.get("updated_at"),
            "languages": fetch_languages(owner, repo),
            "readme": fetch_readme(owner, repo),
            "commits": fetch_commits(owner, repo),
            "contributors": fetch_contributors(owner, repo)
        }

        all_repo_data.append(output_data)

    with open(OUTPUT_FILE, "w") as file:
        json.dump(all_repo_data, file, indent=4)

    logging.info("Data extraction completed for all repos")

if __name__ == "__main__":
    main()