# command-safety

Pre-execution validator that blocks dangerous bash commands before they run.

## What it does

This plugin intercepts all Bash tool calls and validates them against dangerous patterns. If a dangerous command is detected, it blocks execution and logs the attempt.

## Blocked patterns (MVP)

### Destructive operations
- `rm -rf /`, `rm -rf ~`, `rm -rf *` (recursive force delete)
- `del /f /s /q` (Windows force delete)
- `rmdir /s /q`, `rd /s /q` (Windows directory removal)

### Disk overwrite
- `dd if=... of=/dev/...` (raw disk write)
- `mkfs` (format filesystem)
- `format C:` (Windows format)
- `diskpart` (Windows disk partitioning)

### Fork bombs
- `:(){:|:&};:` (Unix fork bomb)
- `%0|%0` (Windows batch fork bomb)
- `while true; do ... & done` (infinite process spawning)

## Installation

Via marketplace:
```bash
/plugin marketplace add sdui-hq/ai-marketplace
/plugin install command-safety@ai-marketplace
```

For local development:
```bash
claude --plugin-dir /path/to/ai-marketplace/plugins/command-safety
```

## Requirements

- Python 3.6+

## Logging

Blocked commands are logged to `.claude/logs/command-safety.log` in the project directory:

```json
{"timestamp": "2026-01-02T12:00:00Z", "command": "rm -rf /", "pattern": "file_destruction", "action": "denied"}
```

## License

MIT
