# Sdui AI marketplace

[![Tests](https://github.com/sdui-hq/ai-marketplace/actions/workflows/test.yml/badge.svg)](https://github.com/sdui-hq/ai-marketplace/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Sdui's marketplace for AI tools

## Installation

Add this marketplace to Claude Code:

```bash
/plugin marketplace add sdui/ai-marketplace
```

Or via CLI:

```bash
claude plugin marketplace add sdui/ai-marketplace
```

## Available Plugins

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

## Shared Configurations

Beyond plugins, this repository provides shared configurations for Claude Code environments.

| Configuration | Description | Location |
|--------------|-------------|----------|
| [DevContainer](./.devcontainer) | Sandboxed Claude Code environment with network isolation | `.devcontainer/` |
| settings.json | Shareable VS Code and Claude Code settings | `.vscode/settings.json` |

### DevContainer

A pre-configured development container for running Claude Code safely with `--dangerously-skip-permissions`. See [.devcontainer/README.md](./.devcontainer/README.md) for details.

### settings.json

Team-shared VS Code settings can be committed to `.vscode/settings.json`. This allows consistent editor configuration across the team (formatting, linting, Claude Code preferences).

## Development

### Add a new plugin to the marketplace

How to create a new plugin: [Claude Code Plugins](https://code.claude.com/docs/en/plugins)

> Recommended: Use Claude Code's plugin command: [/plugin-dev](https://github.com/anthropics/claude-code/tree/main/plugins/plugin-dev)

### Test the marketplace locally

```bash
claude --plugin-dir /path/to/ai-marketplace/plugins/command-safety
```

## License

MIT
