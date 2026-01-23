# Sdui Plugin

Sdui's command toolkit for Claude Code.

## Commands

### `/sdui:telemetry-setup`

Set up Claude Code telemetry to track tool usage across the team.

**What you'll need:** A Coralogix API key (starts with `cxtp_`)

The command guides you through configuring Claude Code to send telemetry data to Coralogix.

#### Why Telemetry?

Telemetry helps us understand how Claude Code tools are being used across teams—which tools are popular, how tokens are consumed, and what environments are in use.

| Tracked | Not Tracked |
|---------|-------------|
| Tool usage (which tools, frequency) | Your prompts |
| Token consumption | Model outputs/responses |
| OS environment | Code or file contents |

---

### `/sdui:pr-review`

Automated PR code review that posts feedback directly to GitHub.

**What you'll need:** [GitHub CLI](https://cli.github.com/) installed and authenticated

**Run it:**
```
/sdui:pr-review <PR_NUMBER>
```

The command fetches the PR, analyzes all changes and posts a structured review comment with a verdict. 

---

## Security

The `telemetry-setup` command stores credentials in settings files. Make sure `.claude/settings.local.json` is in your `.gitignore`.
