# Claude Code settings

Starting point for shared Claude Code configuration. Teams can extend this configuration based on their needs and share it within their own repository.

> [!NOTE]
> Team members can customise their own configuration further by creating `.claude/settings.local.json` file. (gitignored)

## Files

| File | Purpose | Version Controlled |
|------|---------|-------------------|
| `settings.json` | Team-shared configuration | Yes |
| `settings.local.json` | Personal overrides | No (gitignored) |

## Details

### Sandboxing

#### How Sandboxing compares to DevContainers

- **Sandboxing** provides OS-level filesystem isolation with pre-approved commands—no Docker required. _(Recommended for interactive work with fewer permission prompts.)_
- **DevContainer** adds network isolation on top, enabling fully autonomous operations. _(Recommended for autonomous sessions that require additional security layers.)_

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
