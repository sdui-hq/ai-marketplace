# Sdui AI marketplace

[![Tests](https://github.com/sdui-hq/ai-marketplace/actions/workflows/test.yml/badge.svg)](https://github.com/sdui-hq/ai-marketplace/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Sdui's marketplace for AI tools

## Shared Configurations

This repository provides shared configurations for Claude Code.

| Configuration | Description | Location |
|--------------|-------------|----------|
| [settings.json](./.claude/settings.json) | Shared Claude Code settings (sandbox, env vars, etc) | `.claude/settings.json` |
| [DevContainer](./.devcontainer) | Containerised environment with network isolation | `.devcontainer/` |

### Settings

Shared CLI configuration `.claude/settings.json` can be found in the [.claude](./.claude) directory.

### DevContainer

A pre-configured development container with filesystem + network isolation. See [README.md](./.devcontainer/README.md) for details.

> [!NOTE]
> DevContainers are recommended for autonomous Claude sessions that require additional security layers.
> 
> for quick tasks with fewer permission prompts, use [Sandboxing](./.claude/settings.json)

## Plugins

Add this marketplace to Claude Code:

```bash
/plugin marketplace add sdui-hq/ai-marketplace
# or via CLI
claude plugin marketplace add sdui-hq/ai-marketplace
```

### Available Plugins

| Plugin | Description | Type | Install |
|--------|-------------|------|---------|
| [command-safety](./plugins/command-safety) | Blocks dangerous bash commands before execution | Hook | `command-safety@ai-marketplace` |
| [lint-runner](./plugins/lint-runner) | Runs linting when Claude completes tasks | Hook | `lint-runner@ai-marketplace` |
| [pr-review](./plugins/pr-review) | Automated PR code reviews with GitHub CLI | Command | `pr-review@ai-marketplace` |
| [notifications](./plugins/notifications) | Cross-platform desktop notifications for Claude Code events | Hook | `notifications@ai-marketplace` |

Install any plugin:
```bash
/plugin install <plugin>@ai-marketplace
```
## Development

### Add a new plugin to the marketplace

How to create a new plugin: [Claude Code Plugins](https://code.claude.com/docs/en/plugins)

### Test the marketplace locally

```bash
claude --plugin-dir /path/to/ai-marketplace/plugins/command-safety
```
