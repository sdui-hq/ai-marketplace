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

Sandboxing provides OS-level isolation that:

1. **Reduces permission fatigue** - No constant approval prompts for safe commands
2. **Enables autonomy** - Claude can work independently within defined boundaries
3. **Protects against attacks** - Even if Claude is manipulated, sandbox limits remain enforced

**Use sandboxing when:**
- Running autonomous agent workflows
- Working with untrusted dependencies
- You want fewer interruptions while maintaining security

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
