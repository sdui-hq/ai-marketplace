# lint-runner

Stop hook that runs linting when Claude completes a task.

## What it does

This plugin runs your configured lint command whenever Claude attempts to complete a task. If linting fails, it blocks completion and spawns a subagent to fix the errors.

## Configuration

Set the `CLAUDE_LINT_COMMAND` environment variable in your project's `.claude/settings.json`:

```json
{
  "env": {
    "CLAUDE_LINT_COMMAND": "npm run lint"
  }
}
```

This ensures the lint command is project-specific and shared with your team.

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
