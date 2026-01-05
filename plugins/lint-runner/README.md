# lint-runner

Stop hook that runs linting when Claude completes a task.

## What it does

This plugin runs your configured lint command whenever Claude attempts to complete a task. If linting fails, it blocks completion and spawns a subagent to fix the errors.

## Configuration

Set the `CLAUDE_LINT_COMMAND` environment variable to your lint command:

```bash
export CLAUDE_LINT_COMMAND="npm run lint"
# or
export CLAUDE_LINT_COMMAND="ruff check ."
```

If not set, the hook approves immediately (no-op).

## Installation

Via marketplace:
```bash
/plugin marketplace add sdui-hq/ai-marketplace
/plugin install lint-runner@ai-marketplace
```

For local development:
```bash
claude --plugin-dir /path/to/ai-marketplace/plugins/lint-runner
```

## Requirements

- Python 3.10+

## Logging

Lint failures are logged to `.claude/logs/lint.log` in the project directory with full output for the subagent to read and fix.

## License

MIT
