#!/usr/bin/env python3
import os
import sys
import yaml
import re

def validate_skill(skill_path):
    errors = []

    if not os.path.isdir(skill_path):
        return [f"Error: {skill_path} is not a directory"]

    skill_md_path = os.path.join(skill_path, "SKILL.md")
    if not os.path.isfile(skill_md_path):
        errors.append("Error: SKILL.md is missing")
        return errors

    try:
        with open(skill_md_path, 'r') as f:
            content = f.read()

        # Match YAML frontmatter
        match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
        if not match:
            errors.append("Error: SKILL.md must start with YAML frontmatter bounded by ---")
            return errors

        frontmatter_raw = match.group(1)
        metadata = yaml.safe_load(frontmatter_raw)

        if not metadata:
            errors.append("Error: YAML frontmatter is empty")
            return errors

        # Validate name
        name = metadata.get('name')
        if not name:
            errors.append("Error: 'name' field is missing in frontmatter")
        else:
            if not isinstance(name, str):
                errors.append("Error: 'name' must be a string")
            elif not (1 <= len(name) <= 64):
                errors.append("Error: 'name' must be between 1 and 64 characters")
            elif not re.match(r'^[a-z0-9\-]+$', name):
                errors.append("Error: 'name' contains invalid characters (only lowercase a-z, 0-9, and - allowed)")
            elif name.startswith('-') or name.endswith('-'):
                errors.append("Error: 'name' must not start or end with a hyphen")
            elif '--' in name:
                errors.append("Error: 'name' must not contain consecutive hyphens")

            # Match parent directory name
            dir_name = os.path.basename(os.path.abspath(skill_path))
            if name != dir_name:
                errors.append(f"Error: 'name' ({name}) does not match directory name ({dir_name})")

        # Validate description
        description = metadata.get('description')
        if not description:
            errors.append("Error: 'description' field is missing in frontmatter")
        else:
            if not isinstance(description, str):
                errors.append("Error: 'description' must be a string")
            elif not (1 <= len(description) <= 1024):
                errors.append("Error: 'description' must be between 1 and 1024 characters")

    except Exception as e:
        errors.append(f"Error parsing SKILL.md: {str(e)}")

    return errors

def main():
    if len(sys.argv) < 2:
        print("Usage: validate_skill.py <path/to/skill-folder>")
        sys.exit(1)

    skill_path = sys.argv[1]
    errors = validate_skill(skill_path)

    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    else:
        print(f"Skill at {skill_path} is valid.")

if __name__ == "__main__":
    main()
