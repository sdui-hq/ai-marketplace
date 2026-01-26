# Better Init Plugin

Enhances CLAUDE.md initialization with best practices and guidelines.

## What It Does

When you run `/init` or ask Claude to create a CLAUDE.md file, this plugin automatically provides guidance to ensure the generated file follows best practices for effective AI-assisted development.

## Key Guidelines Enforced

- **Structure**: WHAT (tech stack), WHY (purpose), HOW (workflows)
- **Conciseness**: Target <300 lines, ideally under 60
- **Focused instructions**: Respects LLM instruction limits
- **Progressive disclosure**: Reference external docs instead of embedding
- **No style guidelines**: Use deterministic tools (linters) instead

## Installation

This plugin is part of the sdui-plugins marketplace. Enable it in your Claude Code settings.

## Usage

Simply run `/init` or ask Claude to create a CLAUDE.md file. The skill activates automatically.
