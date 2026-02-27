#!/usr/bin/env python3
import os
import json
import re
import sys

def parse_yaml_frontmatter(content):
    """Simple regex-based YAML frontmatter parser to avoid PyYAML dependency."""
    match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return {}

    yaml_text = match.group(1)
    data = {}
    for line in yaml_text.splitlines():
        if ':' in line:
            key, value = line.split(':', 1)
            data[key.strip()] = value.strip()
    return data

def discover_skills(skill_paths):
    skills = []
    for base_path in skill_paths:
        full_base_path = os.path.abspath(os.path.join(os.getcwd(), base_path))
        if not os.path.exists(full_base_path):
            continue

        for item in os.listdir(full_base_path):
            skill_dir = os.path.join(full_base_path, item)
            skill_md = os.path.join(skill_dir, "SKILL.md")
            if os.path.isdir(skill_dir) and os.path.exists(skill_md):
                try:
                    with open(skill_md, 'r') as f:
                        content = f.read()
                        data = parse_yaml_frontmatter(content)
                        skills.append({
                            "name": data.get("name", item),
                            "description": data.get("description", "No description provided."),
                            "path": skill_dir
                        })
                except Exception as e:
                    print(f"Warning: Failed to parse {skill_md}: {e}", file=sys.stderr)
    return skills

def check_env():
    env_vars = ["JULES_API_KEY", "JULES_SESSION_ID", "GITHUB_PAT"]
    results = {}
    for var in env_vars:
        results[var] = "Set" if os.environ.get(var) else "Not Set"
    return results

def main():
    # Robust config traversal
    agent_config = config.get("agent_config", config) # Handle both nested and flat config
    skill_paths = agent_config.get("knowledge", {}).get("skill_paths", ["./._/skills"])

    skills = discover_skills(skill_paths)
    env_status = check_env()

    output = {
        "skills": skills,
        "environment": env_status
    }

    # Print JSON output for machine consumption
    print("--- BOOTSTRAP DATA START ---")
    print(json.dumps(output, indent=2))
    print("--- BOOTSTRAP DATA END ---")

    # Print Human readable summary
    print("\n# Agent Bootstrap Summary\n")
    print(f"**Config Found:** {'Yes' if config else 'No'}")
    print(f"**Skills Discovered:** {len(skills)}")
    for s in skills:
        print(f"- **{s['name']}**: {s['description']}")

    print("\n**Environment Variables:**")
    for var, status in env_status.items():
        print(f"- {var}: {status}")

if __name__ == "__main__":
    main()
