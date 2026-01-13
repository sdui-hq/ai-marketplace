# CLAUDE.md

## Project Overview

A Claude Code plugin marketplace containing all the plugins we use at Sdui. Uses Python 3.12 with `uv` package manager.

## Technical Stack

@pyproject.toml

## Architecture

**Marketplace Structure:**
- `.claude-plugin/marketplace.json` - Marketplace manifest listing all plugins
- `plugins/<name>/.claude-plugin/plugin.json` - Individual plugin metadata
- `plugins/<name>/` - Plugin directory containing the plugin code

## Testing

Tests live in `tests/` with `conftest.py` auto-discovering plugin paths. Plugin code is tested with pytest.

## Hooks

Refer to the documentation for more information when implementing hooks.
Documentation: https://code.claude.com/docs/en/hooks 