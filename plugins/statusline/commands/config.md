---
description: Configure which sections appear in the statusline
allowed-tools: ["Read", "Write", "AskUserQuestion"]
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

## Step 2: Verify Statusline Is Set Up

1. Read `~/.claude/settings.json` and check for `statusLine.command`
2. If not found, read `.claude/settings.local.json` and check for `statusLine.command`
3. If no statusline configuration is found in either file, tell the user to run `/statusline:setup` first and stop

## Step 3: Read Current Configuration

Read `~/.claude/statusline-config.json`. If the file doesn't exist, use these defaults:
- `show_session`: `true`
- `show_branch`: `true`
- `max_session_len`: `30`

Show the user their current configuration before applying changes.

## Step 4: Write Updated Configuration

Build a JSON object from the user's Step 1 selections and write it to `~/.claude/statusline-config.json` using the Write tool:

- `show_session`: `true` if "Session name" selected, else `false`
- `show_branch`: `true` if "Git branch" selected, else `false`
- `max_session_len`: numeric value from truncation choice (30, 20, 0, or custom)

## Step 5: Confirm Changes

Tell the user which sections are now enabled/disabled and that the changes will take effect on the next statusline refresh. Note that the config file persists across plugin updates.
