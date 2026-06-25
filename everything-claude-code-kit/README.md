# Everything Claude Code Kit

A Claude Code toolkit — specialized **agents**, **skills**, rules, and hooks for
productive AI-assisted development. This repo is a Claude Code plugin: install it
directly or copy individual components manually.

> Inspired by [`affaan-m/everything-claude-code`](https://github.com/affaan-m/everything-claude-code)
> (the "Everything Claude Code" plugin from an Anthropic Hackathon winner).
> This is an independently authored kit under a new name.

## What's Inside

```
everything-claude-code-kit/
├── .claude-plugin/
│   ├── plugin.json        # Plugin metadata and component paths
│   └── marketplace.json   # Marketplace catalog for /plugin marketplace add
├── agents/                # Specialized subagents for delegation
│   ├── planner.md             # Feature implementation planning
│   ├── architect.md           # System design decisions
│   ├── tdd-guide.md           # Test-driven development
│   ├── code-reviewer.md       # Quality and security review
│   ├── security-reviewer.md   # Vulnerability analysis
│   ├── build-error-resolver.md# Build error resolution
│   ├── e2e-runner.md          # Playwright E2E testing
│   ├── refactor-cleaner.md    # Dead code cleanup
│   ├── doc-updater.md         # Documentation
│   ├── docs-lookup.md         # Documentation / API lookup
│   ├── python-reviewer.md     # Python code review
│   ├── typescript-reviewer.md # TypeScript / JavaScript review
│   ├── go-reviewer.md         # Go code review
│   └── database-reviewer.md   # Database / SQL review
└── skills/                # Workflow definitions and domain knowledge
    ├── coding-standards/      # Language best practices
    ├── backend-patterns/      # API, database, caching patterns
    └── frontend-patterns/     # React, Next.js patterns
```

## Install

Add as a plugin marketplace from a local checkout:

```
/plugin marketplace add ./everything-claude-code-kit
```

Or copy individual `agents/*.md` and `skills/*/SKILL.md` files into your own
`.claude/` directory.

## License

MIT
