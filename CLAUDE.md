# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Claude Code plugin marketplace for Sdui. Python 3.12 with `uv` package manager.

## Architecture

**Marketplace:** `.claude-plugin/marketplace.json` lists all plugins.

**Plugin structure:**
```
plugins/<name>/
├── .claude-plugin/plugin.json   # Metadata
├── hooks/hooks.json             # Hook registration
├── hooks/*.py                   # Hook implementations
├── commands/*.md                # User-invoked commands
└── skills/<name>/SKILL.md       # Skill definitions
```

**Current plugins:**
- `command-safety` - PreToolUse hook blocking dangerous bash commands
- `lint-runner` - Stop hook running lints after task completion
- `notifications` - Desktop notifications on completion/permission prompts
- `sdui` - Commands for PR review and telemetry setup
- `better-init` - CLAUDE.md initialization guidance skill
- `sdui-eng-design` - Feature design document command

## Plugin Creation Rules

When creating a new plugin, always:
1. Add it to the Available Plugins table in `README.md`
2. Add it to `.claude-plugin/marketplace.json`
3. Create a concise `README.md` inside the plugin directory focused on developer onboarding (usage, examples, what it does)

## Commands

```bash
uv sync --dev                    # Install dependencies
uv run pytest tests/ -v          # Run all tests
uv run pytest tests/test_file.py -v  # Run single test file
uv run flake8 plugins/ tests/    # Lint
```

## Testing

Tests in `tests/` with `conftest.py` auto-discovering plugin paths. Test files mirror plugin structure: `test_validate_command.py`, `test_lint_runner.py`, `tests/notifications/`.

## Hooks

Hook types: PreToolUse, Stop, Notification. See https://code.claude.com/docs/en/hooks

Hook response format: JSON to stdout with `decision` field (`approve`, `block`, `deny`).
