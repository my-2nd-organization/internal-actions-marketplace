import os
import yaml

MARKETPLACE_DIR = "docs"
ACTIONS_DIR = os.path.join(MARKETPLACE_DIR, "actions")
MKDOCS_YML_PATH = "mkdocs.yml"
SITE_NAME = "Internal Marketplace"

# Step 1: Collect all markdown files inside docs/actions
def collect_actions():
    actions = []
    for filename in sorted(os.listdir(ACTIONS_DIR)):
        if filename.endswith(".md"):
            action_name = filename.replace(".md", "").replace("-", " ").title()
            action_path = f"actions/{filename}"
            actions.append({action_name: action_path})
    return actions

# Step 2: Generate mkdocs.yml dynamically
def generate_mkdocs_yml(actions):
    config = {
        "site_name": SITE_NAME,
        "theme": {
            "name": "material"
        },
        "nav": [
            {"Home": "index.md"},
            {"Actions": actions}
        ]
    }
    with open(MKDOCS_YML_PATH, "w") as f:
        yaml.dump(config, f, sort_keys=False)
    print("✅ mkdocs.yml generated.")

# Step 3: Generate index.md with HTML card-based layout
def generate_index_md(actions):
    index_path = os.path.join(MARKETPLACE_DIR, "index.md")
    html = [
        "<style>",
        ".cards { display: flex; flex-wrap: wrap; gap: 1rem; }",
        ".card { background: #0d1117; padding: 1rem; width: 250px; border-radius: 10px; border: 1px solid #444; color: white; }",
        ".card a { color: #58a6ff; text-decoration: none; }",
        "</style>",
        "<div class='cards'>"
    ]
    for item in actions:
        for name, path in item.items():
            html.append(f"""
  <div class="card">
    <h4>{name}</h4>
    <p><a href="{path}">View Action</a></p>
  </div>
""")
    html.append("</div>")

    with open(index_path, "w") as f:
        f.write("\n".join(html))
    print("✅ index.md generated with cards.")

# Main
if __name__ == "__main__":
    actions = collect_actions()
    generate_index_md(actions)
    generate_mkdocs_yml(actions)
