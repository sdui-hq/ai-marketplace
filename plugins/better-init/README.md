# Better Init Plugin

Enhances CLAUDE.md initialization with best practices and guidelines.

## What It Does

When you run `/init` or ask Claude to create a CLAUDE.md file, this plugin automatically provides best practices for creating a CLAUDE.md file.

## Key Guidelines Enforced

- **Structure**: WHAT (tech stack), WHY (purpose), HOW (workflows)
- **Conciseness**: Target <300 lines, ideally under 60
- **Focused instructions**: Respects LLM instruction limits
- **Progressive disclosure**: Reference external docs instead of embedding
- **No style guidelines**: Use deterministic tools (linters) instead

## Usage

Simply run `/init` or ask Claude to create a CLAUDE.md file. The skill activates automatically.
