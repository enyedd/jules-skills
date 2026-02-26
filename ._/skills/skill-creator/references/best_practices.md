# Skill Creation Best Practices

## General Principles
- **Agent-Centric**: Write for AI agents, not humans. Use clear, imperative, and structured instructions.
- **Concise**: Only include context the model doesn't already have. Challenge the token cost of every paragraph.
- **Degrees of Freedom**:
  - High (text): Multiple valid approaches.
  - Medium (pseudocode/scripts with params): Preferred patterns.
  - Low (specific scripts): Fragile/critical sequences.

## Resource Usage
- **Scripts**: Use for deterministic reliability or repetitive tasks. Test them!
- **References**: Use for large documentation or data (schemas, policies). Loaded only on demand.
- **Assets**: Use for files that are part of the output (templates, icons).

## Instruction Writing
- Use imperative/infinitive form.
- **Description**: MUST include all "when to use" info. Keywords are essential for matching.
- **Body**: Keep under 500 lines. Use Pattern-based organization (High-level guide, Domain-specific, Conditional details).

## Process
1. Understand functionality via concrete examples.
2. Plan reusable contents (scripts, refs, assets).
3. Initialize (create structure).
4. Implement resources and write `SKILL.md`.
5. Validate and Package.
6. Iterate based on performance.
