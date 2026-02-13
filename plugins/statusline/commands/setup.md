---
description: Configure statusline for Claude Code
allowed-tools: ["Read", "Write", "Edit", "Bash", "AskUserQuestion"]
---

Configure the statusline by updating the appropriate settings file based on chosen scope.

## Step 1: Collect Scope Preference

Use the AskUserQuestion tool to ask the user where to install the configuration:

- Question: "Where should the statusline configuration be installed?"
- Header: "Scope"
- Options:
  - Option 1: "User scope (Recommended)" - Description: "Saves to ~/.claude/settings.json - applies to all your Claude Code sessions"
  - Option 2: "Project scope" - Description: "Saves to .claude/settings.local.json - applies only to this project"

## Step 2: Read Existing Settings

Based on the scope selection from Step 1, read the existing settings file. If the file doesn't exist, start with an empty object `{}`.

| Scope | File Path |
|-------|-----------|
| User scope | `~/.claude/settings.json` |
| Project scope | `.claude/settings.local.json` |

## Step 3: Determine Script Path

The statusline script path depends on where the plugin is installed.

For users who installed via marketplace, the script will be at:
`~/.claude/plugins/cache/sdui-marketplace/statusline/<version>/scripts/statusline.sh`

For users testing locally or developing, suggest they use the absolute path to the script in this repository.

Ask the user which applies:
- Question: "How did you install the statusline plugin?"
- Header: "Install"
- Options:
  - Option 1: "Via marketplace (Recommended)" - Description: "Plugin was installed using Claude Code's plugin install command"
  - Option 2: "Local development" - Description: "Testing locally from the repository"

If marketplace: Read the plugin version by listing `~/.claude/plugins/cache/sdui-marketplace/statusline/` to find the installed version directory, then construct the path: `~/.claude/plugins/cache/sdui-marketplace/statusline/<version>/scripts/statusline.sh`
If local development: Ask user to provide the absolute path to the statusline.sh script.

## Step 4: Customize Sections

Use the AskUserQuestion tool to ask two questions:

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

## Step 5: Apply Section Preferences

Write the user's preferences to `~/.claude/statusline-config.json`:

1. Build a JSON object from the user's Step 4 selections:
   - `show_session`: `true` if "Session name" selected, else `false`
   - `show_branch`: `true` if "Git branch" selected, else `false`
   - `max_session_len`: numeric value from truncation choice (30, 20, 0, or custom)
2. Write the JSON file using the Write tool

This config file persists across plugin updates.

## Step 6: Merge Configuration

Merge the following statusline configuration into the settings file, preserving any existing settings:

```json
{
  "statusLine": {
    "type": "command",
    "command": "<SCRIPT_PATH>"
  }
}
```

Replace `<SCRIPT_PATH>` with the determined script path from Step 3.

Before writing the config, ensure the script is executable by running `chmod +x <SCRIPT_PATH>`.

## Step 7: Write Updated Settings

Write the merged configuration back to the appropriate settings file based on the scope selection with proper JSON formatting.

## Step 8: Verify Configuration

Test the statusline with sample data:

1. Run via Bash:
   ```
   echo '{"workspace":{"current_dir":"/home/user/project","project_dir":"/home/user/project"},"session_id":"preview","context_window":{"used_percentage":42,"context_window_size":200000}}' | <SCRIPT_PATH>
   ```
   Replace `<SCRIPT_PATH>` with the path determined in Step 3.

2. Show the output to the user: "Here's a preview of your statusline:"

3. Note: Session name won't appear (test ID doesn't exist in index). Git branch shows the real current branch.

4. If the command fails, suggest checking jq installation and script permissions.

## Step 9: Confirm Success

After writing the file, confirm to the user:
- Statusline has been configured successfully
- The statusline will appear on the next Claude Code session
- Mention the specific file path based on their scope selection
- Note that the statusline requires `jq` to be installed for full functionality

## Features Summary

The statusline displays:
- Current working directory
- Session name (from Claude's session index)
- Git branch name
- Context window usage with color-coded progress bar:
  - Mint (green): < 50% usage
  - Amber (yellow): 50-80% usage
  - Coral (red): > 80% usage
