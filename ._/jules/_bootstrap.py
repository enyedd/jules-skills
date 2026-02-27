import os, json, re, sys

def parse_yaml_frontmatter(content):
    """Extracts only the YAML block between --- markers."""
    match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match: return {}
    data = {}
    for line in match.group(1).splitlines():
        if ':' in line:
            key, value = line.split(':', 1)
            data[key.strip().lower()] = value.strip()
    return data

def main():
    skill_base_path = "./._/skills"
    discovered_skills = []

    if os.path.exists(skill_base_path):
        for skill_id in os.listdir(skill_base_path):
            skill_dir = os.path.join(skill_base_path, skill_id)
            skill_md = os.path.join(skill_dir, "SKILL.md")

            if os.path.isdir(skill_dir) and os.path.exists(skill_md):
                try:
                    with open(skill_md, 'r') as f:
                        meta = parse_yaml_frontmatter(f.read())
                        discovered_skills.append({
                            "id": skill_id,
                            "name": meta.get("name", skill_id),
                            "description": meta.get("description", "No description")
                        })
                except Exception as e:
                    print(f"Error loading {skill_id}: {e}", file=sys.stderr)

    # This output is what Jules sees in his startup context
    print("--- ASP SKILL REGISTRY START ---")
    print(json.dumps(discovered_skills, indent=2))
    print("--- ASP SKILL REGISTRY END ---")
    print(f"System: {len(discovered_skills)} skills indexed. Ready for task-based activation.")

if __name__ == "__main__":
    main()