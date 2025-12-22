# Documentation Index

## Overview

Claude Reactor documentation is organized by component. Start with the README for a high-level overview, then dive into specific areas.

---

## Quick Navigation

| Document | Purpose | Key Topics |
|----------|---------|------------|
| [README](../README.md) | Project overview and quick start | Installation, features, quick commands |
| [ARCHITECTURE](ARCHITECTURE.md) | System design and data flows | Layers, components, token efficiency |
| [SKILLS](SKILLS.md) | 53 skills reference | Core skills, project-specific, custom creation |
| [AGENTS](AGENTS.md) | 60+ agent personas | Specialists, usage patterns, selection guide |
| [COMMANDS](COMMANDS.md) | 29 slash commands | /p, /plan, /review, /work, and more |
| [HOOKS](HOOKS.md) | Hook system configuration | PreToolUse, PostToolUse, Stop hooks |
| [MCP_INTEGRATION](MCP_INTEGRATION.md) | 16 MCP servers | Server list, setup, v2.0 protocol |
| [WORKFLOW_SYSTEM](WORKFLOW_SYSTEM.md) | Full workflow details | 8-phase pipeline, state machine |
| [AGENTIC_SETUP](AGENTIC_SETUP.md) | Setup guide | Installation, configuration |
| [PIPELINE](PIPELINE.md) | Pipeline internals | Phase execution, recovery |
| [INSTALL](INSTALL.md) | Installation details | Prerequisites, manual setup |
| [INTEGRATIONS](INTEGRATIONS.md) | External integrations | IDE, CI/CD, external tools |

---

## By Use Case

### Getting Started
1. [README](../README.md) - Overview and quick start
2. [AGENTIC_SETUP](AGENTIC_SETUP.md) - Detailed setup
3. [INSTALL](INSTALL.md) - Installation details

### Understanding the System
1. [ARCHITECTURE](ARCHITECTURE.md) - How everything fits together
2. [WORKFLOW_SYSTEM](WORKFLOW_SYSTEM.md) - The 8-phase pipeline
3. [PIPELINE](PIPELINE.md) - Pipeline internals

### Using Features
1. [COMMANDS](COMMANDS.md) - Available slash commands
2. [SKILLS](SKILLS.md) - Skill system and loading
3. [AGENTS](AGENTS.md) - Specialized agent personas

### Configuration
1. [MCP_INTEGRATION](MCP_INTEGRATION.md) - MCP servers
2. [HOOKS](HOOKS.md) - Hook configuration
3. [INTEGRATIONS](INTEGRATIONS.md) - External tools

---

## Document Statistics

| Document | Lines | Size | Last Updated |
|----------|-------|------|--------------|
| ARCHITECTURE.md | ~750 | 35KB | Dec 21, 2025 |
| WORKFLOW_SYSTEM.md | ~500 | 22KB | Dec 21, 2025 |
| AGENTS.md | ~650 | 21KB | Dec 21, 2025 |
| SKILLS.md | ~400 | 15KB | Dec 21, 2025 |
| COMMANDS.md | ~400 | 14KB | Dec 21, 2025 |
| AGENTIC_SETUP.md | ~250 | 9KB | Dec 21, 2025 |
| MCP_INTEGRATION.md | ~200 | 7KB | Dec 21, 2025 |
| HOOKS.md | ~150 | 5KB | Dec 21, 2025 |
| PIPELINE.md | ~100 | 4KB | Dec 17, 2025 |
| INSTALL.md | ~50 | 2KB | Dec 17, 2025 |
| INTEGRATIONS.md | ~50 | 2KB | Dec 17, 2025 |

---

## Key Concepts Reference

### Pipeline Phases
```
DISCOVER → CONTEXT → PLAN → SAFETY → EXECUTE → VERIFY → REVIEW → COMMIT
```
See: [WORKFLOW_SYSTEM](WORKFLOW_SYSTEM.md), [PIPELINE](PIPELINE.md)

### Token Efficiency (v2.0)
```
v1.0: 5 tool calls = ~3,000 tokens
v2.0: 1 sandbox call = ~300 tokens
Savings: 70-90%
```
See: [ARCHITECTURE](ARCHITECTURE.md), [MCP_INTEGRATION](MCP_INTEGRATION.md)

### Memory Hierarchy
```
L1 Session → L2 Project → L3 Infrastructure → L4 Global
```
See: [ARCHITECTURE](ARCHITECTURE.md)

### Skill Loading
```
Core (8) → Project Detection → Specific Skills
Savings: ~84% vs loading all
```
See: [SKILLS](SKILLS.md)

---

## External Resources

- [Claude Code Documentation](https://docs.anthropic.com/claude-code)
- [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk)
- [MCP Specification](https://modelcontextprotocol.io/)

---

## Contributing to Docs

When updating documentation:

1. **Keep consistent style**: Use the existing ASCII diagram format
2. **Include examples**: Code snippets and usage patterns
3. **Cross-reference**: Link to related documents
4. **Update index**: Add new docs to this INDEX.md

### Document Template
```markdown
# Title

## Overview
Brief description.

---

## Section 1

### Subsection
Content with examples.

---

## Section 2
More content.

---

## Quick Reference
Summary table.
```
