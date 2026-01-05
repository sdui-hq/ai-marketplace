# Sdui AI marketplace

[![Tests](https://github.com/sdui-hq/ai-marketplace/actions/workflows/test.yml/badge.svg)](https://github.com/sdui-hq/ai-marketplace/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub last commit](https://img.shields.io/github/last-commit/sdui-hq/ai-marketplace)](https://github.com/sdui-hq/ai-marketplace/commits/main)

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

### command-safety

Pre-execution validator that blocks dangerous bash commands before they run.

Read more [here](https://github.com/sdui-hq/ai-marketplace/blob/main/plugins/command-safety/README.md).

**Install:**

```bash
/plugin install command-safety@ai-marketplace
```

### lint-runner

Automatically runs linting when Claude completes implementation.

Read more [here](https://github.com/sdui-hq/ai-marketplace/blob/main/plugins/lint-runner/README.md).

**Install:**

```bash
/plugin install lint-runner@ai-marketplace
```

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
