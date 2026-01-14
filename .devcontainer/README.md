# DevContainer for Claude Code

A sandboxed development environment for running Claude Code safely with `--dangerously-skip-permissions`.

## Why DevContainer?

DevContainers provide **dual isolation** (filesystem + network) that enables autonomous Claude Code operation without constant permission prompts.

### DevContainer vs Other Approaches

| Approach | Pros | Cons |
|----------|------|------|
| **DevContainer** | Filesystem + network isolation; team-shareable config; VS Code integrated; reproducible | Requires Docker; slower startup; more setup |
| **Permission prompts** (default) | No setup; works anywhere | Interrupts workflow; 84% more prompts |
| **Docker (manual)** | Full control; lightweight | No VS Code integration; manual config |
| **VM** | Strongest isolation | Heavy; slow; not portable |

### When to Use DevContainer

- Running `--dangerously-skip-permissions` safely
- Isolating client/project environments
- Onboarding team members with consistent tooling
- Preventing accidental data exfiltration

### When NOT to Use

- Quick one-off tasks (permission prompts are fine)
- Environments without Docker
- Projects needing unrestricted network access

## Usage

1. Open this repository in VS Code
2. Click "Reopen in Container" when prompted (or use Command Palette: `Dev Containers: Reopen in Container`)
3. Wait for the container to build
4. Run Claude Code: `claude --dangerously-skip-permissions`

## What's Included

- Node.js 20 with Claude Code pre-installed
- Zsh with Powerlevel10k theme
- Git with delta for better diffs
- GitHub CLI (`gh`)
- fzf for fuzzy finding

## Security

The container uses a whitelist-based network firewall that only allows connections to:

- **Anthropic**: api.anthropic.com, statsig.anthropic.com
- **GitHub**: All GitHub IP ranges (fetched dynamically)
- **VS Code**: marketplace.visualstudio.com, vscode.blob.core.windows.net
- **npm**: registry.npmjs.org
- **Sdui internal**: git.sdui.de, *.sdux.de, grafana.intranet-sdui.de
- **Other tools**: Sentry, Slack, Notion, Jira, Firebase, Coralogix

All other outbound connections are blocked.

## Customization

### Adding allowed domains

Edit `init-firewall.sh` and add domains to the `for domain in` loop:

```bash
for domain in \
    "registry.npmjs.org" \
    "your-new-domain.com" \  # Add here
    ...
```

Rebuild the container after changes.

## Persistence

The following are persisted across container rebuilds:
- Claude Code configuration (`~/.claude`)
- Command history (`/commandhistory`)
