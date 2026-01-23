---
description: Configure Coralogix telemetry for Claude Code
allowed-tools: ["Read", "Write", "AskUserQuestion", "Bash(whoami:*)", "Bash(git config:*)"]
---

Configure Coralogix telemetry by collecting user information and updating the appropriate settings file based on chosen scope.

## Step 1: Detect Default Values

Before asking the user for information, detect default values for username and email using cross-platform commands (works on macOS, Linux, and Windows with Git Bash/WSL):

1. **Default username**: Run `whoami` to get the current system username (POSIX standard)
2. **Default email**: Run `git config user.email` to get the git-configured email (may be empty if not configured)

These detected values should be offered as the first option (marked as recommended) when asking the user.

## Step 2: Collect User Information

Use the AskUserQuestion tool to collect the following information from the user. Ask all questions in a single AskUserQuestion call:

1. **Username** - Their identifier (e.g., `johndoe`)
2. **Email** - Their work email (e.g., `john.doe@sdui.de`)
3. **Team name** - Their team identifier (e.g., `platform`, `core`, `codefellas`)
4. **Coralogix API key** - The bearer token for Coralogix (starts with `cxtp_`)
5. **Scope** - Where to install the configuration

Use the detected default values from Step 1 as the first option for username and email questions. If a default was detected, include "(Recommended)" in the label.

Example AskUserQuestion structure:
- Question 1: "What is your username?" with header "Username" -- first option should be the detected username with "(Recommended)", second option can be an alternative format like "firstname.lastname"
- Question 2: "What is your email address?" with header "Email" -- first option should be the detected git email with "(Recommended)" if available, otherwise suggest format like "firstname.lastname@sdui.de"
- Question 3: "What is your team name?" with header "Team"
- Question 4: "What is your Coralogix API key?" with header "API Key"
- Question 5: "Where should the configuration be installed?" with header "Scope"
  - Option 1: "Install for you (user scope) (Recommended)" - Description: "Saves to ~/.claude/settings.json - applies to all your Claude Code sessions"
  - Option 2: "Install for you, in this repo only (local scope)" - Description: "Saves to .claude/settings.local.json - personal settings for this repo"

## Step 3: Read Existing Settings

Based on the scope selection from Step 2, read the existing settings file. If the file doesn't exist, start with an empty object `{}`.

| Scope | File Path |
|-------|-----------|
| User scope | `~/.claude/settings.json` |
| Local scope | `.claude/settings.local.json` |

## Step 4: Merge Configuration

Merge the following environment variables into the `env` section of settings.json, preserving any existing env vars:

```json
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_SERVICE_NAME": "claude-code",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "http/protobuf",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "https://ingress.eu2.coralogix.com:443",
    "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer <API_KEY>",
    "OTEL_RESOURCE_ATTRIBUTES": "user.name=<USERNAME>,service.name=claude-code,cx.application.name=claude-code,cx.subsystem.name=cli,user.email=<EMAIL>,team.name=<TEAM>,department=development"
  }
}
```

Replace placeholders:
- `<USERNAME>` with the collected username
- `<EMAIL>` with the collected email
- `<TEAM>` with the collected team name
- `<API_KEY>` with the collected Coralogix API key

## Step 5: Write Updated Settings

Write the merged configuration back to the appropriate settings file based on the scope selection with proper JSON formatting.

| Scope | File Path |
|-------|-----------|
| User scope | `~/.claude/settings.json` |
| Local scope | `.claude/settings.local.json` |

Trim values provided by the user to remove any whitespace. eg. " john doe " should be "johndoe".

## Step 6: Confirm Success

After writing the file, confirm to the user:
- Settings have been updated successfully
- Telemetry will be sent to Coralogix on the next Claude Code session
- They can verify the configuration by viewing the settings file (mention the specific file path based on their scope selection)
