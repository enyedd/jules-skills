---
name: skill-creator
description: Creation of a skill to give the AI-Agent additional tools. Use when a user requests to create a new skill or when you identify a reusable workflow that would benefit from being encapsulated as a skill. Supports bootstrapping, validation, packaging, and registration in HUMANS.md.
compatibility: Requires `PyYAML` library.
---

# Skill Creator

This skill provides tools and guidance to create, validate, and package other skills.

## Workflow

1.  **Initialize**: Run `scripts/init_skill.py <name> [--path <dir>]` to create the directory structure and `SKILL.md` template.
    -   `<name>` must be 1-64 chars, lowercase alphanumeric and hyphens.
2.  **Develop**:
    -   Identify reusable scripts and place them in `scripts/`.
    -   Extract relevant documentation into `references/`.
    -   Place static templates/resources in `assets/`.
    -   Consult `references/best_practices.md` for guidance on writing agent-focused instructions.
    -   Consult `references/protocol.md` for format specifications.
3.  **Refine SKILL.md**:
    -   Write a concise, keyword-rich description in the frontmatter.
    -   Provide clear, imperative instructions in the body.
4.  **Validate**: Run `scripts/validate_skill.py <path/to/skill>` to ensure compliance with naming and format rules.
5.  **Package**: Run `scripts/package_skill.py <path/to/skill> [output_dir]` to create a `.skill` package.
6.  **Register**: Run `scripts/update_humans.py <name> <usage> <triggers> [requires] [library]` to add the skill to the `HUMANS.md` registry.

## Support Scripts

-   `scripts/init_skill.py`: Bootstraps a new skill.
-   `scripts/validate_skill.py`: Checks for naming and metadata errors.
-   `scripts/package_skill.py`: Validates and zips the skill.
-   `scripts/update_humans.py`: Updates the `HUMANS.md` registry (table and setup script).

## Detailed Guidance

See [Protocol](references/protocol.md) for specifications and [Best Practices](references/best_practices.md) for instruction design.
