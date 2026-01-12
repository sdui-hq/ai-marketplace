# PR Review Plugin

Automated PR code review with GitHub CLI integration for Claude Code.

## Features

- **Full context analysis**: Checks out PR branch locally for complete code understanding
- **Git hygiene validation**: Branch naming and conventional commit message checks
- **Deep code review**: Type safety, security vulnerabilities, performance, test coverage
- **Structured output**: Consistent review format with severity ratings
- **Direct GitHub posting**: Review posted as PR comment automatically

## Prerequisites

- [GitHub CLI](https://cli.github.com/) (`gh`) installed and authenticated
- Git repository with GitHub remote

## Usage

```
/pr-review <PR_NUMBER>
```

Example:
```
/pr-review 30009
```

## What It Does

1. Fetches PR details from GitHub
2. Checks out the PR branch locally
3. Validates branch naming conventions
4. Validates commit messages (Conventional Commits)
5. Analyzes all changed files
6. Performs deep code review
7. Posts structured review as GitHub comment

## Review Output Structure

```markdown
## Code Review: [PR Title]

### Overview
Brief summary of changes

### Git Hygiene
- Branch name validation
- Commit message validation

### Positives
Good practices observed

### Issues Found
Numbered issues with severity, code snippets, and fixes

### Suggestions
Optional improvements

### Security
Security checklist

### Test Coverage
Assessment of tests

### Verdict
Approve / Approve with suggestions / Request changes
```

## Conventions Enforced

### Branch Naming
- `feature/TICKET-123-description`
- `bugfix/TICKET-123-description`
- `hotfix/TICKET-123-description`
- `refactor/TICKET-123-description`
- `chore/TICKET-123-description`

### Commit Messages (Conventional Commits)
```
type(scope): description

Types: feat, fix, refactor, test, docs, chore, style, perf, ci, build
```
