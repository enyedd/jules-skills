#!/usr/bin/env python3
import os
import sys
import re

def update_humans(skill_name, usage, triggers, requires="", library=""):
    humans_path = "HUMANS.md"
    if not os.path.exists(humans_path):
        print(f"Error: {humans_path} not found.")
        sys.exit(1)

    with open(humans_path, 'r') as f:
        content = f.read()

    # 1. Prevent duplicate skill entries in the table
    if f"| `{skill_name}` |" in content:
        print(f"Skill `{skill_name}` already exists in HUMANS.md table. Skipping table update.")
    else:
        # --- TABLE UPDATE WITH SORTING ---
        table_pattern = r'(## Additional Loaded Skills.*?\n\|.*?\n\|[- \|\:]+?\n)((?:\|.*?\n)*)'
        match = re.search(table_pattern, content, re.DOTALL)

        if not match:
            print("Error: Could not find '## Additional Loaded Skills' table structure.")
            sys.exit(1)

        header_part = match.group(1)
        existing_rows_text = match.group(2).strip()
        rows = [line for line in existing_rows_text.split('\n') if line.strip()]

        # Format 'requires' nicely
        if requires:
            formatted_requires = ", ".join([f"`{r.strip()}`" for r in requires.split(",") if r.strip()])
            formatted_requires += " as environment variable"
        else:
            formatted_requires = ""

        new_row = f"| `{skill_name}` | {usage} | {triggers} | {formatted_requires} |"
        rows.append(new_row)

        # Alphabetical sort
        rows.sort(key=lambda x: x.lower())
        sorted_table_text = header_part + "\n".join(rows) + "\n"
        content = content.replace(match.group(0), sorted_table_text)

    # --- SHELL SCRIPT UPDATE (Multiple Libraries) ---
    if library:
        lib_list = [l.strip() for l in library.split(",") if l.strip()]

        for lib in lib_list:
            pip_cmd = f"pip install {lib}"
            if pip_cmd in content:
                # Library already exists, update the comment above it
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if pip_cmd in line:
                        if i > 0 and lines[i-1].strip().startswith('#'):
                            comment_line = lines[i-1]
                            if skill_name not in comment_line:
                                lines[i-1] = comment_line + f", {skill_name}"
                content = '\n'.join(lines)
            else:
                # Add new entry at the end of the shell block
                shell_block_pattern = r'(```shell\n.*?)(\n```)'
                shell_match = re.search(shell_block_pattern, content, re.DOTALL)

                if shell_match:
                    inner_content = shell_match.group(1)
                    # Ensure inner_content ends with a newline
                    if not inner_content.endswith('\n'):
                        inner_content += '\n'

                    new_entry = f"# {skill_name}\n{pip_cmd}\n"

                    content = (
                        content[:shell_match.start(1)] +
                        inner_content +
                        new_entry +
                        content[shell_match.start(2):]
                    )

    # 4. Save changes
    with open(humans_path, 'w') as f:
        f.write(content)

    print(f"Successfully updated HUMANS.md with `{skill_name}` and its dependencies.")

def main():
    # Usage: script.py "name" "usage" "triggers" "REQ1, REQ2" "LIB1, LIB2"
    if len(sys.argv) < 4:
        print("Usage: update_humans.py <skill_name> <usage> <triggers> [requires] [library]")
        print("Note: Multiple requirements or libraries should be comma-separated strings.")
        sys.exit(1)

    skill_name = sys.argv[1]
    usage = sys.argv[2]
    triggers = sys.argv[3]
    requires = sys.argv[4] if len(sys.argv) > 4 else ""
    library = sys.argv[5] if len(sys.argv) > 5 else ""

    update_humans(skill_name, usage, triggers, requires, library)

if __name__ == "__main__":
    main()
