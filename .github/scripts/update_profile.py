import urllib.request
import json
import re
import os
import sys

# Ensure UTF-8 output across platforms
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

USERNAME = "RAJCHITTORIYA"
LEETCODE_USER = "raj_chittoriya"

# Curated descriptions for flagship projects
CUSTOM_DESCRIPTIONS = {
    "PACK_CHECK": "AI-powered legal metrology compliance inspection system using OCR and intelligent parsing.",
    "dsa": "Structured Java problem-solving implementations covering foundational & advanced DSA patterns.",
    "Secure-Hybrid-Datacenter-Network-Architecture-Multi-Tier-Cloud-Segmentation": "Zero Trust hybrid cybersecurity architecture securing datacenters, AWS multi-VPC & Kubernetes.",
    "quicknotes-react": "Responsive productivity application built with React showcasing component modularity & CRUD hooks.",
    "School-Management": "Web-based institutional ERP application for student records, admissions & administration."
}

def fetch_top_repositories():
    url = f"https://api.github.com/users/{USERNAME}/repos?sort=updated&per_page=100"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            repos = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"[ERROR] Fetching repositories failed: {e}")
        return []

    ignored = {
        "RAJCHITTORIYA", "node", "first_project-demo", "demo-1-", 
        "demo_repo", "Project2", "calculator-project", 
        "2024-28_Raj_Chittoriya_2410030901_5th_Semester_3CSE15", 
        "RAJ_CHITTORIYA_2410030901_IILM-GN"
    }

    filtered = []
    for r in repos:
        if r.get('fork') or r['name'] in ignored:
            continue
        filtered.append(r)

    # Score and sort repos to prioritize flagship projects
    def score_repo(r):
        name = r['name']
        if name in CUSTOM_DESCRIPTIONS:
            return 1000 - list(CUSTOM_DESCRIPTIONS.keys()).index(name)
        return r.get('stargazers_count', 0) * 10 + (r.get('size', 0) // 100)

    filtered.sort(key=score_repo, reverse=True)
    return filtered[:5]

def update_readme_projects():
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        print("[ERROR] README.md not found.")
        return

    top_repos = fetch_top_repositories()
    if not top_repos:
        print("[INFO] No repositories found to update.")
        return

    lines = []
    for r in top_repos:
        name = r['name']
        desc = CUSTOM_DESCRIPTIONS.get(name) or r.get('description') or "Active software development project."
        desc = desc.replace('\n', ' ').strip()
        if len(desc) > 130:
            desc = desc[:127] + "..."
        lang = r.get('language') or 'Code'
        url = r['html_url']
        lines.append(f"- [🔹 **{name}**]({url}) — *{desc}* (`{lang}`)")

    projects_markdown = "\n".join(lines)

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"(<!-- REPOS_START -->)(.*?)(<!-- REPOS_END -->)"
    if re.search(pattern, content, re.DOTALL):
        new_content = re.sub(pattern, f"\\1\n{projects_markdown}\n\\3", content, flags=re.DOTALL)
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("[SUCCESS] README.md dynamic projects section updated.")
    else:
        print("[WARNING] Markers <!-- REPOS_START --> and <!-- REPOS_END --> not found in README.md")

if __name__ == "__main__":
    update_readme_projects()
