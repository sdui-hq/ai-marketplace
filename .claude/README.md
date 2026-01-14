# Shared Claude Code Configuration

This is meant to be a starting point for shared Claude Code configuration. 

Each team can extend this configuration based on their needs and share it with their team by hosting it in their own repository.

> [!NOTE]
> Team members can customise their own configuration further by creating `.claude/settings.local.json` file. (gitignored)

## Files

| File | Purpose | Version Controlled |
|------|---------|-------------------|
| `settings.json` | Team-shared configuration | Yes |
| `settings.local.json` | Personal overrides | No (gitignored) |

## Sandboxing

### How Sandboxing compares to DevContainer

- Sandboxing provides OS-level filesystem isolation with pre-approved commands—no Docker required. 
- DevContainer adds network isolation on top, enabling fully autonomous operations without permission prompts.

[!NOTE]
> Use Sandboxing for everyday interactive work that requires fewer permission prompts.
> Use DevContainer for unattended/autonomous sessions that require network isolation and additional security layers.

## Personal Overrides

Create `.claude/settings.local.json` for personal settings that won't be committed:

```json
{
  "permissions": {
    "allow": [
      "Bash(my-custom-tool:*)"
    ]
  }
}
```

## Learn More

- [Claude Code Settings Documentation](https://code.claude.com/docs/en/settings)
- [Claude Code Sandboxing Guide](https://code.claude.com/docs/en/sandboxing)
