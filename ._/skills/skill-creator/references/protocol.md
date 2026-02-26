# Agent Skills Protocol

## Directory Structure
- `skill-name/`
  - `SKILL.md` (Required)
  - `scripts/` (Optional: executable code)
  - `references/` (Optional: documentation)
  - `assets/` (Optional: templates, static resources)

## SKILL.md format
Must contain YAML frontmatter followed by Markdown content.

### YAML Frontmatter
```yaml
---
name: skill-name
description: Clear description of what it does and when to use it.
compatibility: (Pre)Requirements that the skill needs to work correctly. 
---
```
- **name**: 1-64 chars, lowercase `a-z`, `0-9`, and `-`. No start/end `-`. No `--`. Must match directory name.
- **description**: 1-1024 chars. Primary triggering mechanism.
- **compatibility**: [OPTIONAL] needed libraries, environment variables, ...  

## Progressive Disclosure
1. **Metadata**: name and description loaded at startup.
2. **Instructions**: full `SKILL.md` loaded when skill is activated.
3. **Resources**: referenced files loaded only when required.

## Validation
Skills can be validated for structure and metadata compliance.
