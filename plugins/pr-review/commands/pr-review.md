---
allowed-tools: Bash(gh pr view:*), Bash(gh pr diff:*), Bash(gh pr checkout:*), Bash(gh pr comment:*), Bash(git log:*), Bash(git branch:*), Bash(git symbolic-ref:*), Bash(git show-ref:*), Read, Glob, Grep
description: Automated PR code review with GitHub comment
argument-hint: <PR_NUMBER>
---

You are an expert code reviewer. Perform a comprehensive code review for PR #$ARGUMENTS and post it as a GitHub comment.

## Workflow

### Step 1: Get PR Information
First, fetch the PR details:
```
gh pr view $ARGUMENTS
```

### Step 2: Checkout PR Locally
Checkout the PR branch to have full local context:
```
gh pr checkout $ARGUMENTS
```

### Step 3: Determine Base Branch
Detect the default base branch (main or master):
```bash
git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || (git show-ref --verify --quiet refs/heads/main && echo main || echo master)
```
Store this as BASE_BRANCH for subsequent commands.

### Step 4: Validate Branch Name
Get the current branch name and validate it follows conventions:
```
git branch --show-current
```

**Valid branch patterns:**
- `feature/TICKET-123-short-description`
- `bugfix/TICKET-123-short-description`
- `hotfix/TICKET-123-short-description`
- `refactor/TICKET-123-short-description`
- `chore/TICKET-123-short-description`

Where TICKET is a Jira-style prefix (e.g., OPTPRIME, BUGHUNTERS, IDAAS, CODEFELLAS).

**Flag as issue if:**
- Branch doesn't start with valid prefix (feature/, bugfix/, etc.)
- Missing ticket reference
- Uses spaces or special characters (except hyphens)

### Step 5: Validate Commit Messages
Get all commits in the PR (compared to base branch):
```
git log $BASE_BRANCH..HEAD --oneline
git log $BASE_BRANCH..HEAD --format="%s"
```

**Valid commit message format (Conventional Commits):**
```
type(scope): description

Types: feat, fix, refactor, test, docs, chore, style, perf, ci, build
Scope: optional, should match module name (e.g., MusicSchool, MasterData, Authentication)
Description: lowercase, imperative mood, no period at end
```

**Examples of GOOD commits:**
- `feat(MusicSchool): add tag configuration endpoint`
- `fix(Authentication): resolve token expiration issue`
- `refactor(MasterData): extract repository interface`
- `test: add integration tests for invoice module`

**Examples of BAD commits:**
- `Fixed bug` (no type, no scope, past tense)
- `WIP` (not descriptive)
- `OPTPRIME-123 changes` (ticket in message, not descriptive)
- `Update files` (too vague)

**Flag as issue if:**
- Commits don't follow conventional format
- Multiple unrelated changes in single commit
- WIP or fixup commits not squashed

### Step 6: Analyze the Changes
Get the list of changed files and the diff:
```
gh pr diff $ARGUMENTS --name-only
gh pr diff $ARGUMENTS
```

### Step 7: Deep Code Review
For each significant changed file:
1. Read the full file content using the Read tool to understand context
2. Analyze code quality, patterns, and potential issues
3. Check for:
   - Code correctness and logic errors
   - Type safety issues (return types, null handling)
   - Following project conventions (check similar files for patterns)
   - Security vulnerabilities (injection, XSS, CSRF)
   - Performance implications
   - Test coverage
   - Missing error handling

### Step 8: Compose Review
Structure your review with these sections:

```markdown
## Code Review: [PR Title]

### Overview
[Brief summary of what the PR does - 2-3 sentences]

---

### Git Hygiene

#### Branch Name
- Branch: `[branch-name]`
- Status: [Valid / Invalid]
- [If invalid: explanation of what's wrong]

#### Commit Messages
| Commit | Status | Issue |
|--------|--------|-------|
| `feat(Module): description` | Valid | - |
| `fixed stuff` | Invalid | Missing type, vague description |

---

### Positives
[Bullet points of good practices observed]

---

### Issues Found
[Numbered list of issues, each with:]
#### 1. **[Severity]: [Issue Title]**
```[language]
// file:line
[code snippet]
```
[Explanation of the issue and suggested fix]

---

### Suggestions
[Optional improvements that aren't blocking]

---

### Security
[Security checklist - use checkmarks]

---

### Test Coverage
[Assessment of test coverage]

---

### Verdict
**[Approve / Approve with suggestions / Request changes]**
[Summary of required actions if any]

**Blocking issues:**
- [ ] [List any blocking issues including git hygiene problems]
```

### Step 9: Validate Markdown
Before posting, ensure:
- All code blocks have language specifiers and are properly closed
- No unescaped special characters in code blocks
- Single quotes in shell commands are properly escaped
- No nested code blocks (use indentation instead)
- Tables are properly formatted

### Step 10: Post Review Comment
Use `gh pr comment` to post the review. Use a heredoc for complex markdown:
```bash
gh pr comment $ARGUMENTS --body '[review content]'
```

IMPORTANT:
- Escape single quotes by replacing `'` with `'\''` in the comment body
- If the comment is very long, consider using `--body-file` with a temp file
- Always provide the PR URL at the end confirming the comment was posted

## Output
After posting, confirm with:
- Link to the posted comment
- Summary of the verdict (Approve/Request changes)
