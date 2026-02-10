---
description: Configure which sections appear in the statusline
allowed-tools: ["Read", "Edit", "AskUserQuestion"]
---

Configure which information sections are displayed in the Claude Code statusline.

## Step 1: Ask User Preferences

Use the AskUserQuestion tool to ask the user two questions:

**Question 1 (multiSelect):**
- Question: "Which sections do you want to show in the statusline?"
- Header: "Sections"
- multiSelect: true
- Options:
  - Option 1: "Session name (Recommended)" - Description: "Shows the current session name (looked up from Claude's session index)"
  - Option 2: "Git branch (Recommended)" - Description: "Shows the current git branch name"

**Question 2:**
- Question: "Max characters for session name before truncating?"
- Header: "Truncate"
- Options:
  - Option 1: "30 (Recommended)" - Description: "Truncate session names longer than 30 characters"
  - Option 2: "No truncation" - Description: "Show full session name regardless of length"
  - Option 3: "20" - Description: "Truncate session names longer than 20 characters"

The user can also pick "Other" (built into AskUserQuestion) to provide a custom numeric value.

## Step 2: Locate the Installed Script

Find the statusline script path from the user's settings:

1. Read `~/.claude/settings.json` and check for `statusLine.command`
2. If not found, read `.claude/settings.local.json` and check for `statusLine.command`
3. Extract the script path from the command string (e.g. from `"bash /path/to/statusline.sh"`, extract `/path/to/statusline.sh`)
4. If no statusline configuration is found in either file, tell the user to run `/statusline-setup` first and stop

## Step 3: Read Current Script

Read the statusline script at the path determined in Step 2 to get the current configuration values.

## Step 4: Update Configuration

Based on the user's selection, update the configuration variables in the script using the Edit tool:

- If the user selected "Session name", set `SHOW_SESSION=true`, otherwise set `SHOW_SESSION=false`
- If the user selected "Git branch", set `SHOW_BRANCH=true`, otherwise set `SHOW_BRANCH=false`
- For the truncation question:
  - If "30" was selected, set `MAX_SESSION_LEN=30`
  - If "No truncation" was selected, set `MAX_SESSION_LEN=0`
  - If "20" was selected, set `MAX_SESSION_LEN=20`
  - If the user provided a custom value via "Other", set `MAX_SESSION_LEN=<custom_value>`

Each variable is on its own line in the CONFIGURATION section at the top of the script. Use Edit to replace each line individually.

## Step 5: Confirm Changes

Tell the user which sections are now enabled/disabled and that the changes will take effect on the next statusline refresh.
