import os
import requests
import yaml

GITHUB_API = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
ORG_NAME = "NML-Actions"
DOCS_DIR = "docs"
ACTIONS_DIR = os.path.join(DOCS_DIR, "actions")
MKDOCS_FILE = "mkdocs.yml"
INDEX_FILE = os.path.join(DOCS_DIR, "index.md")

# Ensure docs/actions exists
os.makedirs(ACTIONS_DIR, exist_ok=True)

def fetch_repos(org):
    repos = []
    page = 1
    while True:
        url = f"{GITHUB_API}/orgs/{org}/repos?per_page=100&page={page}"
        res = requests.get(url, headers=HEADERS)
        data = res.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos

def fetch_action_yaml(repo_name):
    url = f"{GITHUB_API}/repos/{ORG_NAME}/{repo_name}/contents/action.yml"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        return yaml.safe_load(requests.get(res.json()['download_url']).text)
    return None

def fetch_readme_md(repo_name):
    url = f"{GITHUB_API}/repos/{ORG_NAME}/{repo_name}/readme"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        download_url = res.json().get("download_url")
        if download_url:
            return requests.get(download_url).text
    return None

def write_action_doc(repo, action_data):
    name = action_data.get("name", repo)
    desc = action_data.get("description", "")
    usage = f"```yaml\nuses: {ORG_NAME}/{repo}@main\n```"

    # Try fetching README.md
    readme_content = fetch_readme_md(repo)
    readme_section = f"\n---\n\n## README\n\n{readme_content}" if readme_content else ""

    md_content = f"# {name}\n\n**Description:** {desc}\n\n## Usage\n\n{usage}{readme_section}\n"
    path = os.path.join(ACTIONS_DIR, f"{repo}.md")
    with open(path, "w") as f:
        f.write(md_content)

    return {
        "title": name,
        "path": f"actions/{repo}.md"
    }

def update_mkdocs(nav_entries):
    mkdocs_config = {
        "site_name": "Internal Actions Marketplace",
        "theme": {
            "name": "material"
        },
        "nav": [
            {"Home": "index.md"},
            {"Actions": nav_entries}
        ]
    }
    with open(MKDOCS_FILE, "w") as f:
        yaml.dump(mkdocs_config, f, sort_keys=False)

def generate_index(nav_entries):
    html_cards = ""
    for entry in nav_entries:
        for name, path in entry.items():
            html_cards += f"""
<div class="card">
  <h3>{name}</h3>
  <a href="{path}">View Action</a>
</div>
"""
    index_content = f"""<!-- Auto-generated Index Page -->
<style>
.cards {{ display: flex; flex-wrap: wrap; gap: 1rem; }}
.card {{
  background: #0d1117;
  padding: 1rem;
  width: 250px;
  border-radius: 10px;
  border: 1px solid #444;
  color: white;
}}
.card a {{ color: #58a6ff; text-decoration: none; }}
</style>

<div class="cards">
{html_cards}
</div>
"""
    with open(INDEX_FILE, "w") as f:
        f.write(index_content)

def main():
    repos = fetch_repos(ORG_NAME)
    nav_entries = []

    for repo in repos:
        action_data = fetch_action_yaml(repo["name"])
        if action_data:
            entry = write_action_doc(repo["name"], action_data)
            nav_entries.append({entry["title"]: entry["path"]})

    update_mkdocs(nav_entries)
    generate_index(nav_entries)

if __name__ == "__main__":
    main()
