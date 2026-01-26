---
name: CLAUDE.md Initialization Guidance
description: This skill should be used when the user asks to "initialize CLAUDE.md", "create CLAUDE.md", "set up CLAUDE.md", "run /init", "help with CLAUDE.md", "improve CLAUDE.md", "review CLAUDE.md", "analyze codebase for CLAUDE.md", "generate project documentation for Claude", or mentions creating or improving project context files for Claude Code.
version: 0.1.0
---

# CLAUDE.md Best Practices

When creating or initializing a CLAUDE.md file, follow these guidelines to produce an effective, high-quality project context file.

## Core Principles

CLAUDE.md is the highest leverage point for Claude Code. It affects every workflow phase and output artifact. Treat it as carefully crafted documentation, not auto-generated content.

### The Three Essential Sections

Structure every CLAUDE.md around three core areas:

**WHAT** - Describe the codebase:
- Tech stack and major dependencies
- Project structure and directory layout
- Key files and their purposes
- Important for monorepos: provide a clear map

**WHY** - Explain the purpose:
- What the project does
- Why components exist
- Business context when relevant

**HOW** - Detail workflows:
- Build and run commands
- Test execution methods
- Deployment procedures
- Verification steps

## Critical Constraints

### Keep It Concise

Target fewer than 300 lines. Aim for under 60 lines when possible.

Every line in CLAUDE.md competes for attention. Irrelevant context degrades performance uniformly across all instructions. Remove anything not universally applicable to every task.

### Respect Instruction Limits

Frontier LLMs can reliably follow approximately 150-200 instructions. Claude Code's system prompt already contains ~50 instructions. Budget the remaining capacity carefully.

Include only:
- Instructions that apply to every task
- Critical project-specific rules
- Essential workflow commands

Exclude:
- Edge cases
- Rarely-needed information
- Task-specific details (put these elsewhere)

### Use Progressive Disclosure

Store detailed, task-specific guidance in separate files. Reference them from CLAUDE.md rather than embedding everything.

**Instead of:**
```markdown
## API Development
[500 lines of API documentation]
```

**Use:**
```markdown
## API Development
See `docs/api-guide.md` for API development guidelines.
```

Create focused documentation files:
- `docs/testing.md` for test procedures
- `docs/deployment.md` for deployment steps
- `docs/architecture.md` for system design

### Avoid Style Guidelines

Do not use CLAUDE.md for code style enforcement. Deterministic tools handle this better:
- Linters (ESLint, Flake8, Biome)
- Formatters (Prettier, Black)
- Pre-commit hooks
- CI checks

Style instructions in CLAUDE.md waste instruction budget and produce inconsistent results. Configure tooling instead.

### Use File:Line Pointers

Reference code locations instead of embedding snippets:

**Instead of:**
```markdown
The authentication middleware looks like:
\`\`\`typescript
export function authMiddleware(req, res, next) {
  // 50 lines of code
}
\`\`\`
```

**Use:**
```markdown
Authentication middleware: `src/middleware/auth.ts:15`
```

Benefits:
- Stays current as code changes
- Reduces CLAUDE.md size
- Claude reads the actual file when needed

## Writing Guidelines

### Be Direct and Specific

State facts and commands clearly:

**Good:**
```markdown
Run tests: `npm test`
Build: `npm run build`
Database: PostgreSQL 14
```

**Avoid:**
```markdown
You might want to run tests using npm test.
The build process can be initiated with npm run build.
We use PostgreSQL for our database needs.
```

### Prioritize Ruthlessly

Ask for each line:
- Does this apply to every task?
- Is this information Claude cannot infer?
- Would removing this cause problems?

If uncertain, remove it. Add back only if problems arise.

### Group Related Information

Organize logically:

```markdown
## Stack
- Language: TypeScript 5.0
- Framework: Next.js 14
- Database: PostgreSQL 14

## Commands
- `npm run dev` - Start development server
- `npm test` - Run test suite
- `npm run build` - Production build

## Structure
- `src/app/` - Next.js app router pages
- `src/lib/` - Shared utilities
- `src/components/` - React components
```

## What to Include

### Always Include

- Primary language and version
- Framework and major dependencies
- Essential build/run/test commands
- Project structure overview (brief)
- Critical conventions that differ from defaults

### Consider Including

- Database and infrastructure details
- Environment setup requirements
- Key architectural decisions
- Important file locations

### Never Include

- Obvious information Claude can infer
- Code snippets (use file:line references)
- Style guides (use linters)
- Comprehensive documentation (link to it)
- Information for specific tasks only

## Example Structure

A well-structured CLAUDE.md:

```markdown
# Project Name

Brief one-line description.

## Stack
- TypeScript 5.0, Node 20
- Next.js 14 (App Router)
- PostgreSQL 14, Prisma ORM

## Commands
- `npm run dev` - Development server
- `npm test` - Run tests
- `npm run db:migrate` - Run migrations

## Structure
- `src/app/` - Pages and API routes
- `src/lib/` - Shared code
- `prisma/` - Database schema

## Guidelines
- All API routes require authentication
- Use server components by default
- Database changes need migrations

## Docs
- API development: `docs/api.md`
- Testing guide: `docs/testing.md`
```

This example is under 30 lines yet covers everything essential.

## Anti-Patterns to Avoid

### The Kitchen Sink

Including everything "just in case" dilutes important instructions. Be selective.

### The Style Guide

Embedding coding standards. Use tooling instead.

### The Tutorial

Explaining how things work in detail. Link to documentation.

### The Changelog

Including historical context or version notes. Keep it current-state only.

### The Copy-Paste

Embedding code blocks. Use file:line references.

## Final Checklist

Before finalizing CLAUDE.md:

- [ ] Under 300 lines (ideally under 60)
- [ ] Has WHAT, WHY, HOW sections
- [ ] No code snippets (file:line references instead)
- [ ] No style guidelines (tooling handles this)
- [ ] Task-specific details in separate files
- [ ] Every line applies to every task
- [ ] Direct, specific language
- [ ] Manually crafted, not auto-generated
