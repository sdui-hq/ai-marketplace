# sdui-eng-design

Generate structured feature design documents directly in Claude Code.

## Usage

```
/feature-design-doc <feature name or description>
```

### Example

```
/feature-design-doc SSO login for enterprise customers
```

Claude will generate a design doc covering:

- Overview, Terminology, Current System, Problem Statement
- Goals, Non-Goals
- Proposed Implementation (Storage, Ownership, Monitoring, Analytics)
- Launch Plan (Dependencies, Rollout, Migrations, Testing, Extensions)
- Concerns (Security, Usability, Risk/Abuse, Support)
- Open Questions

Sections that don't apply are removed. The result is saved to `docs/designs/YYYY-MM-design-<feature-name>.md`.

## Installation

The plugin is registered in the marketplace. No additional setup required.
