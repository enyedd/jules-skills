# Humans

This document is designed to help users communicate more effectively with Jules AI.

## Jules Internal Skills/Tools

An overview of Jules's existing skills and the methods required to trigger them.

| Tool | Usage | Triggers |
| :--- | :--- | :--- |
| `google_search` | Performs an online Google search to retrieve up-to-date information. | "Search for...", "Find the latest...", "What is the status of..." |
| `view_text_website` | Fetches the content of a website as plain text. | Prompting a URL (e.g., "Check this site: https://..."), "Read the content of [URL]" |
| `run_in_bash_session` | Executes any bash command in the sandbox environment. | "Install...", "Run...", "Execute...", "Check the status of...", "List processes..." |
| `list_files` | Lists files and directories in a specific path. | "What files are here?", "Show me the project structure." |
| `read_file` | Reads the content of a specific file. | "Read [filename]", "Show me the code in...", "What does [file] say?" |
| `write_file` | Creates or overwrites a file with new content. | "Create a file named...", "Update [file] with...", "Save this to..." |
| `replace_with_git_merge_diff` | Performs targeted search-and-replace using Git merge diff format. | "Change this part of [file]", "Refactor the function..." |
| `view_image` | Loads and analyzes an image from a URL. | Prompting an image URL (e.g., ".jpg", ".png", ".webp"), "Look at this image: [URL]" |
| `read_image_file` | Reads an image file from the local filesystem. | "Look at the screenshot at [path]", "Open the image [file]" |
| `knowledgebase_lookup` | Retrieves information from the internal knowledgebase for help. | "I'm stuck with...", "How do I use...?", "Help me with [tool/framework]" |
| `message_user` | Sends a message to the user. | Asking a direct question, providing a status update, or when I need to explain something. |
| `request_user_input` | Asks the user a question and waits for a response. | When I need clarification or a decision from you. |
| `set_plan` | Sets or updates my execution plan. | "What is your plan?", "How are you going to solve this?" (Usually triggered by me at the start). |
| `submit` | Commits changes and requests approval to finalize the task. | "Finalize the code", "Submit your work", "Commit and push." |
| `pre_commit_instructions` | Gets the list of steps to perform before submission. | Triggered by me automatically as part of my "Complete pre-commit steps" plan step. |
| `frontend_verification` | Generates screenshots of UI changes using Playwright. | Editing HTML/CSS/JS files: "Verify the UI changes." |
| `start_live_preview` | Starts a live preview server for web applications. | "Show me the running application", "Start the server." |
| `initiate_memory_recording` | Documents key patterns or learnings for future tasks. | Triggered by me to preserve knowledge. |
| `request_code_review` | Requests a review of the current changes. | Triggered by me as part of the verification process. |
| `read_pr_comments` | Reads comments on a pull request. | "What are the comments on my PR?", "Address the PR feedback." |
| `reply_to_pr_comments` | Replies to comments on a pull request. | "Reply to the comment by...", "Explain why you did..." |

## Additional Loaded Skills

An overview of additional loadable ASPs (Agent Skills Protocol)

| Tool | Usage | Triggers | Requires  |
| :--- | :--- |:--- | :--- |
| `git-curl` | Unified tool for remote Git operations (commit, diff, watch) via GitHub API and curl. | "committing files, get or wait for changes" | `GITHUB_PAT` as environment variable |
| `jules-api` | Communication with other agents (sessions) via the Jules REST API. | "Ask Agent...", "Check session ...", "Merge code with diff from... " | `JULES_API_KEY` as environment variable |
| `skill-creator` | Creation of a skill to give the AI-Agent additional tools. | "create <SKILL> skill", "Initialize a new skill", "Create a skill for..." |  |

Setup script (via https://jules.google.com/repo/github/OWNER/REPOSITORY/config): copy-paste and execute(_Run and snapshot_)

```shell
# jules-api
pip install requests

# skill-creator
pip install PyYAML

# Run bootstrap to initialize agent context
sudo chmod +x ./._/init/bootstrap.sh
./._/init/bootstrap.sh
```

## Shorthand Syntax, to reference skills, prompts, studies
* The AI agent is configured to resolve references to skills, studies, and prompts using the `@<folder>/<file-name>` format.
* **Information Retrieval:** To direct the agent to a specific study or prompt, you can use a command like: *"In @prompt/001 I tasked you to review @study/use-skills to... "*
* **Skill Activation:** To trigger a specific skill, you can use a command like: *"Use @skill/jules-api to..."* The agent will then load the corresponding documentation and execute the skill according to its defined instructions.
