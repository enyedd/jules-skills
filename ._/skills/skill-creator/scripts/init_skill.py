#!/usr/bin/env python3
import os
import sys
import argparse

def init_skill(name, path):
    skill_dir = os.path.join(path, name)
    if os.path.exists(skill_dir):
        print(f"Error: {skill_dir} already exists.")
        sys.exit(1)

    os.makedirs(skill_dir)
    os.makedirs(os.path.join(skill_dir, "scripts"))
    os.makedirs(os.path.join(skill_dir, "references"))
    os.makedirs(os.path.join(skill_dir, "assets"))

    skill_md_content = f"""---
name: {name}
description: A description of what {name} does and when to use it.
---

# {name.replace('-', ' ').title()}

## Usage

Describe how to use this skill.

## Resources

- `scripts/`: Executable code.
- `references/`: Documentation.
- `assets/`: Templates and static resources.
"""

    with open(os.path.join(skill_dir, "SKILL.md"), 'w') as f:
        f.write(skill_md_content)

    print(f"Skill '{name}' initialized at {skill_dir}")

def main():
    parser = argparse.ArgumentParser(description="Initialize a new skill.")
    parser.add_argument("name", help="The name of the skill.")
    parser.add_argument("--path", default="._/skills", help="The directory where the skill will be created.")

    args = parser.parse_args()
    init_skill(args.name, args.path)

if __name__ == "__main__":
    main()
