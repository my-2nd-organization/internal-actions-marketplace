import os
import requests
import yaml

ORG = os.environ['ACTION_ORG']
TOKEN = os.environ['GITHUB_TOKEN']
HEADERS = {'Authorization': f'token {TOKEN}'}

MARKETPLACE_MD_DIR = 'docs/actions'
os.makedirs(MARKETPLACE_MD_DIR, exist_ok=True)

# Get all repos in the org
repos = requests.get(f"https://api.github.com/orgs/{ORG}/repos", headers=HEADERS).json()

nav = [
    {'Home': 'index.md'},
    {'Actions': []}
]

for repo in repos:
    name = repo['name']
    default_branch = repo['default_branch']
    action_url = f"https://raw.githubusercontent.com/{ORG}/{name}/{default_branch}/action.yml"
    readme_url = f"https://raw.githubusercontent.com/{ORG}/{name}/{default_branch}/README.md"

    print(f"Processing: {name}")

    # Try fetching action.yml
    r = requests.get(action_url, headers=HEADERS)
    if r.status_code != 200:
        continue
    action = yaml.safe_load(r.text)

    # Generate MD page
    md_path = f"{MARKETPLACE_MD_DIR}/{name}.md"
    with open(md_path, 'w') as f:
        f.write(f"# {action.get('name', name)}\n\n")
        f.write(f"**Description**: {action.get('description', '')}\n\n")
        f.write("## Usage\n```yaml\n")
        f.write(f"uses: {ORG}/{name}@{default_branch}\n")
        f.write("```")

    nav[1]['Actions'].append({action.get('name', name): f"actions/{name}.md"})

# Write mkdocs.yml
with open('mkdocs.yml', 'w') as f:
    f.write("site_name: Internal Actions Marketplace\n")
    f.write("theme:\n  name: material\n")
    f.write("nav:\n")
    for item in nav:
        for label, link in item.items():
            if isinstance(link, list):
                f.write(f"  - {label}:\n")
                for sub in link:
                    for sub_label, sub_link in sub.items():
                        f.write(f"      - {sub_label}: {sub_link}\n")
            else:
                f.write(f"  - {label}: {link}\n")
