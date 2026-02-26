# Agent Skills Protocol (ASP)

## Architecture
Skills are decoupled from the agent's core to save context space.
1. **Registry:** Metadata (YAML) is loaded at startup via `bootstrap.py`.
2. **On-Demand Loading:** Full instructions (`SKILL.md`) are only loaded into context when needed.
3. **External Execution:** Scripts reside in `/scripts/` and are executed by the environment. The agent must not read script source code.

## Activation Flow
1. Identify a matching skill from the Registry.
2. Read `@skill/<skill-name>` to get execution details.
3. Call the required scripts via the environment terminal.
4. Log the execution in `/._/logging/skill-calls.log`.