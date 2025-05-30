import os
import requests
import base64
import yaml

# Constants
GITHUB_API_URL = "https://api.github.com"
ORG_NAME = "NML-Actions"
MARKETPLACE_DIR = "docs/actions"
INDEX_MD_PATH = "docs/index.md"
HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}"
}


def get_repos(org):
    """Fetch all repositories under the organization."""
    repos = []
    page = 1
    while True:
        url = f"{GITHUB_API_URL}/orgs/{org}/repos?per_page=100&page={page}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Failed to fetch repos: {response.status_code}")
            break
        data = response.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos


def fetch_action_yaml(repo):
    """Fetch the content of action.yml from the repository."""
    url = f"{GITHUB_API_URL}/repos/{ORG_NAME}/{repo}/contents/action.yml"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return None
    content = base64.b64decode(response.json()["content"]).decode("utf-8")
    return yaml.safe_load(content)


def write_action_docs(repo_name, action_data):
    """Generate a Markdown file for the action."""
    os.makedirs(MARKETPLACE_DIR, exist_ok=True)
    doc_path = os.path.join(MARKETPLACE_DIR, f"{repo_name}.md")
    with open(doc_path, "w") as f:
        f.write(f"# {action_data.get('name', repo_name)}\n\n")
        f.write(f"**Description:** {action_data.get('description', 'No description')}.\n\n")
        f.write("## Usage\n\n")
        f.write(f"```yaml\nuses: {ORG_NAME}/{repo_name}@main\n```\n")


def generate_index(actions_info):
    """Generate index.md with card-style HTML layout."""
    with open(INDEX_MD_PATH, "w") as f:
        f.write("# Internal Actions Marketplace\n\n")
        f.write("<style>\n")
        f.write("""
.cards {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 1rem;
}
.card {
  background: #0d1117;
  padding: 1rem;
  width: 250px;
  border-radius: 10px;
  border: 1px solid #444;
  color: white;
  box-shadow: 0 4px 6px rgba(0,0,0,0.3);
}
.card h4 {
  margin-top: 0;
  margin-bottom: 0.5rem;
}
.card p {
  font-size: 0.9rem;
  color: #ccc;
}
.card a {
  color: #58a6ff;
  text-decoration: none;
  font-weight: bold;
}
.card a:hover {
  text-decoration: underline;
}
</style>\n\n""")
        f.write('<div class="cards">\n')
        for action in actions_info:
            f.write(f"""  <div class="card">
    <h4>{action['name']}</h4>
    <p>{action['description']}</p>
    <p><a href="actions/{action['repo']}/">View Action</a></p>
  </div>\n""")
        f.write("</div>\n")


def main():
    repos = get_repos(ORG_NAME)
    actions_info = []

    for repo in repos:
        repo_name = repo["name"]
        action_data = fetch_action_yaml(repo_name)
        if not action_data:
            print(f"Skipping {repo_name}: action.yml not found.")
            continue

        write_action_docs(repo_name, action_data)

        actions_info.append({
            "repo": repo_name,
            "name": action_data.get("name", repo_name),
            "description": action_data.get("description", "No description available.")
        })

    generate_index(actions_info)


if __name__ == "__main__":
    main()
