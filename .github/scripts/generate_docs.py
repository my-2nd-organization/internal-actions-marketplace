import os
import requests
import yaml

# Organization where all action repos live
ORG = "NML-Actions"

# GitHub token for API access (automatically injected in GitHub Actions)
TOKEN = os.environ['GITHUB_TOKEN']
HEADERS = {'Authorization': f'token {TOKEN}'}

MARKETPLACE_MD_DIR = 'docs/actions'
os.makedirs(MARKETPLACE_MD_DIR, exist_ok=True)

# Fetch all repositories in the organization
repos_url = f"https://api.github.com/orgs/{ORG}/repos?per_page=100"
repos = requests.get(repos_url, headers=HEADERS).json()

nav = [
    {'Home': 'index.md'},
    {'Actions': []}
]

for repo in repos:
    name = repo['name']
    default_branch = repo['default_branch']
    action_yml_url = f"https://raw.githubusercontent.com/{ORG}/{name}/{default_branch}/action.yml"

    print(f"Processing: {name}")

    # Try fetching action.yml
    r = requests.get(action_yml_url, headers=HEADERS)
    if r.status_code != 200:
        print(f"❌ Skipping {name}, no action.yml found.")
        continue

    try:
        action_data = yaml.safe_load(r.text)
    except Exception as e:
        print(f"⚠️ Error parsing action.yml for {name}: {e}")
        continue

    action_title = action_data.get('name', name)
    action_desc = action_data.get('description', 'No description available.')

    # Generate Markdown documentation for the action
    md_filename = f"{name}.md"
    md_path = os.path.join(MARKETPLACE_MD_DIR, md_filename)
    with open(md_path, 'w') as f:
        f.write(f"# {action_title}\n\n")
        f.write(f"**Description:** {action_desc}\n\n")
        f.write("## Usage\n")
        f.write("```yaml\n")
        f.write(f"uses: {ORG}/{name}@{default_branch}\n")
        f.write("```\n")

    # Add to navigation
    nav[1]['Actions'].append({action_title: f"actions/{md_filename}"})

# Write updated mkdocs.yml
with open('mkdocs.yml', 'w') as f:
    f.write("site_name: Internal Actions Marketplace\n")
    f.write("theme:\n  name: material\n")
    f.write("nav:\n")
    for section in nav:
        for label, links in section.items():
            if isinstance(links, list):
                f.write(f"  - {label}:\n")
                for link in links:
                    for sub_label, sub_link in link.items():
                        f.write(f"      - {sub_label}: {sub_link}\n")
            else:
                f.write(f"  - {label}: {links}\n")
