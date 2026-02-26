# Jules Agent Instructions

## 1. Skill Execution Protocol (ASP)
You operate under the **Agent Skills Protocol**. (Read `/._/skills/SKILLS.md` for the technical definition of the Agent Skills Protocol.)
- **Discovery:** Do NOT scan the `/._/skills/` directory. Use the `ASP SKILL REGISTRY` provided during bootstrap for available capabilities.
- **Activation:** You are only allowed to read a skill's full documentation using the `@skill/<name>` shorthand when a task matches the skill's description or trigger.
- **Black-Box Execution:** Never read files inside any `references/` or `scripts/` folder. Execute them as tools. You only need the interface (inputs/outputs) described in `SKILL.md`.

## 2. Directory Access & Shorthand
The metadata folder: `/._/` directory is **READ-ONLY** and off-limits for automatic indexing. You may only access it via these shorthand references:

| Shorthand | Path | Usage |
| :--- | :--- | :--- |
| `@skill/<name>` | `/._/skills/<name>/SKILL.md` | Load full skill instructions |
| `@prompt/<id>` | `/._/prompts/<id>.md` | Reference task history |
| `@study/<file>` | `/._/study/<file>` | Access background research |

## 3. Workflow Constraints
- **Strict Mode:** Only perform tasks within the scope of the project files. Avoid reading metadata folders unless explicitly triggered.
- **Privacy:** Never expose secrets or environment variables in logs or PR messages.
- **Completion:** A task is considered finished only when a Pull Request is created.