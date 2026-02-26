#!/usr/bin/env python3
import os
import sys
import zipfile
import subprocess

def package_skill(skill_path, output_dir):
    # Validate first
    validate_script = os.path.join(os.path.dirname(__file__), "validate_skill.py")
    result = subprocess.run([sys.executable, validate_script, skill_path], capture_output=True, text=True)

    if result.returncode != 0:
        print("Validation failed:")
        print(result.stdout)
        print(result.stderr)
        sys.exit(1)

    skill_name = os.path.basename(os.path.normpath(skill_path))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    zip_path = os.path.join(output_dir, f"{skill_name}.skill")

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(skill_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, skill_path)
                zipf.write(file_path, arcname)

    print(f"Skill packaged successfully at {zip_path}")

def main():
    if len(sys.argv) < 2:
        print("Usage: package_skill.py <path/to/skill-folder> [output-directory]")
        sys.exit(1)

    skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."

    package_skill(skill_path, output_dir)

if __name__ == "__main__":
    main()
