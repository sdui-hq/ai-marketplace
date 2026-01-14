# DevContainer for Claude Code

A containerised development environment for running Claude Code with network isolation.

## Why DevContainer?

DevContainers provide **dual isolation** (filesystem + network) that enables autonomous Claude Code operation and provide a consistent development environment for team members.

### How DevContainer compares to Sandboxing

- DevContainer provides filesystem + network isolation, enabling fully autonomous operations. 
- Sandboxing provides OS-level filesystem isolation with pre-approved commands—no Docker required. 

[!NOTE]
> Use DevContainer for unattended/autonomous sessions that require network isolation and additional security layers.
> Use Sandboxing for everyday interactive work that requires fewer permission prompts.

## Usage

1. Open this repository in VS Code
2. Click "Reopen in Container" when prompted (or use Command Palette: `Dev Containers: Reopen in Container`)
3. Wait for the container to build
4. Run Claude Code: `claude`

## What's Included

- Node.js 20 with Claude Code pre-installed
- Git with delta for better diffs
- GitHub CLI (`gh`)
- fzf for fuzzy finding

## Security

The container uses a whitelist-based network firewall that only allows connections to explicitly allowed domains.

All other outbound connections are blocked.

### Adding allowed domains

Edit `init-firewall.sh` and add domains to the `for domain in` loop:

```bash
for domain in \
    "registry.npmjs.org" \
    "your-new-domain.com" \  # Add here
    ...
```

## Persistence

The following are persisted across container rebuilds:
- Claude Code configuration (`~/.claude`)
- Command history (`/commandhistory`)
