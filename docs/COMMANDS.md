# Commands Reference

## Overview

Claude Reactor provides **29 slash commands** that extend Claude Code's capabilities. Commands are executed via `/command-name [args]` syntax and leverage the pipeline infrastructure.

---

## Command Categories

```
┌─────────────────────────────────────────────────────────────────┐
│                     COMMAND HIERARCHY                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Pipeline Commands (Core)                                        │
│  ├── /p              Bootstrap pipeline + v2 mode               │
│  ├── /pipeline       Manage pipeline lifecycle                  │
│  ├── /pipeline-check Verify pipeline health                     │
│  ├── /p-install      Quick pipeline install                     │
│  └── /auto-workflow  Run full 8-phase workflow                  │
│                                                                  │
│  Context Commands                                                │
│  ├── /context-save   Save before compaction                     │
│  ├── /context-restore Recover after reset                       │
│  ├── /generate-context Create PROJECT_CONTEXT                   │
│  └── /archive-context Cleanup ephemeral context                 │
│                                                                  │
│  Memory Commands                                                 │
│  ├── /mem            Fetch memory by ID                         │
│  ├── /remember       Structured knowledge capture               │
│  └── /global-fact    Add to global facts                        │
│                                                                  │
│  Skill Commands                                                  │
│  └── /load-skills    Load project-specific skills               │
│                                                                  │
│  Development Commands                                            │
│  ├── /plan           Feature planning                           │
│  ├── /review         Code review (3 hats)                       │
│  ├── /work           Isolated git worktree session              │
│  └── /playwright-test E2E browser testing                       │
│                                                                  │
│  AI Integration Commands                                         │
│  ├── /ccs            Delegate to CCS CLI                        │
│  ├── /llama          LlamaCPP API proxy                         │
│  └── /model          Switch AI model                            │
│                                                                  │
│  System Commands                                                 │
│  ├── /hooks-lite     Enable minimal hooks                       │
│  ├── /check-mcps     Verify MCP connections                     │
│  ├── /v1             Disable v2 for session                     │
│  ├── /v1-once        One-time v1 bypass                         │
│  └── /test-p         Debug slash command caching                │
│                                                                  │
│  Domain-Specific                                                 │
│  ├── /ha             Home Assistant control                     │
│  └── /novel-os       Novel-OS manuscript context                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Core Pipeline Commands

### /p - Pipeline Bootstrap

**Purpose**: Initialize the v2.0 pipeline with skill management and sandbox orchestration.

**Philosophy**: "Load light, Plan deep, Lock constraints, Execute fast."

**Usage**:
```bash
/p                    # Bootstrap pipeline
/p "task description" # Bootstrap + start task
```

**What It Does**:
1. Verifies pipeline components (symlinks, configs)
2. Installs/repairs if needed
3. Detects project type (frontend/backend/devops/docs)
4. Enables v2 sandbox-first mode
5. Loads project-specific skills
6. Recalls global preferences from memory

**Output**:
```
Pipeline: ✅ All components verified
Project Type: Frontend (Node/TypeScript)
Skills: 8 core + 3 project-specific loaded
Active Constraints: [from memory]
v2 Mode: ✓ Enabled
```

---

### /pipeline

**Purpose**: Manage the OmniMCP pipeline lifecycle.

**Usage**:
```bash
/pipeline status      # Show current state
/pipeline restart     # Restart all components
/pipeline logs        # View pipeline logs
```

---

### /pipeline-check

**Purpose**: Health check for pipeline components.

**Checks**:
- MCP server connectivity
- Symlink integrity
- Hook execution
- Memory system access

**Usage**:
```bash
/pipeline-check       # Full health check
```

---

### /p-install

**Purpose**: Quick pipeline installation to current project.

**Usage**:
```bash
/p-install            # Install to current directory
```

---

### /auto-workflow

**Purpose**: Execute the complete 8-phase workflow automatically.

**Phases**:
1. DISCOVER - Scan codebase structure
2. CONTEXT - Load memory and preferences
3. PLAN - Sequential thinking breakdown
4. SAFETY - Security and dependency checks
5. EXECUTE - Sandbox-first implementation
6. VERIFY - Tests and linting
7. REVIEW - Code review agents
8. COMMIT - Git operations

**Usage**:
```bash
/auto-workflow "Add user authentication feature"
```

---

## Context Management Commands

### /context-save

**Purpose**: Preserve session context before compaction.

**When to Use**:
- Before running `/compact`
- When context is getting full (>80k tokens)
- Before long-running operations

**Actions**:
```python
mcp__unified-orchestrator__session_checkpoint(
    summary="Current work summary",
    achievements=["Completed items"],
    pending_tasks=["Remaining items"]
)
```

---

### /context-restore

**Purpose**: Recover session context after compaction or restart.

**When to Use**:
- After `/compact` command
- On session start
- When context appears lost

**Actions**:
```python
mcp__unified-orchestrator__session_restore(
    include_infrastructure=True,
    include_tasks=True,
    auto_detect_project=True
)
```

---

### /generate-context

**Purpose**: Create ephemeral PROJECT_CONTEXT skill from a plan.

**Usage**:
```bash
/generate-context @plan.md
```

**Creates**: `.claude/skills/PROJECT_CONTEXT.md` with locked constraints.

---

### /archive-context

**Purpose**: Archive ephemeral PROJECT_CONTEXT after task completion.

**Usage**:
```bash
/archive-context
```

**Actions**:
- Moves PROJECT_CONTEXT.md to archive
- Cleans up session state
- Saves completion to memory

---

## Memory Commands

### /mem

**Purpose**: Fetch full memory details by ID (Progressive Disclosure).

**Usage**:
```bash
/mem 2640             # Fetch memory ID 2640
```

**Output**: Full memory content with metadata, formatted for readability.

---

### /remember

**Purpose**: Structured knowledge capture for future recall.

**When to Use**:
- After solving tricky bugs
- When making architectural decisions
- After discovering API gotchas
- Before context reset

**Usage**:
```bash
/remember The Omada API requires cookies from login response to be sent with all requests
```

**Structure**:
```
Type: [decision|gotcha|pattern|insight|api|architecture]
Summary: One-line description
Files: file:line references
Details: Full explanation
Prevention: How to avoid (for gotchas)
```

---

### /global-fact

**Purpose**: Add a fact to GLOBAL FACTS section in CLAUDE.md.

**Usage**:
```bash
/global-fact "Always use port 3001 for dev server on this machine"
```

**Persists**: Across all sessions for all projects.

---

## Skill Commands

### /load-skills

**Purpose**: Analyze project and load only relevant skills (~84% token savings).

**Detection**:
| Files | Project Type | Skills Loaded |
|-------|--------------|---------------|
| package.json, tsconfig.json | Frontend | dev-browser, sequential-thinking |
| requirements.txt, pyproject.toml | Backend | debugging-playbook, tdd-enforcer |
| Dockerfile, docker-compose.yml | DevOps | portmon, pipeline-health-check |
| docs/, mkdocs.yml | Documentation | auto-docs, docs-first |

**Usage**:
```bash
/load-skills          # Reload skills for current project
```

**Output**:
```
Project Type: Frontend
Core Skills: 8 (always loaded)
Project Skills: 3 (based on detection)
Total Active: 11 / 53 total
Estimated Token Savings: ~84%
```

---

## Development Commands

### /plan

**Purpose**: Convert feature description into structured implementation plan.

**Usage**:
```bash
/plan "Add user authentication"
/plan --issue 42      # Plan from GitHub issue
```

**Process**:
1. Research phase - Search codebase patterns
2. Design phase - Sequential thinking breakdown
3. Output structured plan with components, risks, scope

---

### /review

**Purpose**: Comprehensive code review through THREE lenses.

**Lenses**:
- 🔒 **Security**: Injection, secrets, auth, OWASP Top 10
- ⚡ **Performance**: N+1 queries, memory leaks, caching
- 🏗️ **Architecture**: Patterns, SRP, coupling, tests

**Usage**:
```bash
/review               # Review staged changes
/review file.ts       # Review specific file
/review --pr 123      # Review PR diff
```

**Output**:
```markdown
## Code Review Summary

### 🔒 Security
- [x] Passed: No injection vulnerabilities

### ⚡ Performance
- [ ] Consider adding index for frequent query

### 🏗️ Architecture
- [x] Follows project conventions

### Verdict: 🟢 APPROVE
```

---

### /work

**Purpose**: Start isolated coding session using git worktrees.

**Benefits**:
- Main branch stays pristine
- Easy to abandon failed experiments
- Clean merge history
- Parallel feature development

**Usage**:
```bash
/work feature-name    # Create worktree and start
/work --finish        # Merge and cleanup
```

---

### /playwright-test

**Purpose**: E2E browser testing with Playwright.

**Usage**:
```bash
/playwright-test              # Run all tests
/playwright-test login.spec   # Run specific test
```

---

## AI Integration Commands

### /ccs

**Purpose**: Delegate tasks to CCS CLI with intelligent profile selection.

**Usage**:
```bash
/ccs "fix typo in README"     # Auto-selects optimal profile
```

---

### /llama

**Purpose**: Act as LlamaCPP API agent for local model interactions.

**Usage**:
```bash
/llama "Explain this function"
```

**Reads**: `llamacpp.env` from current directory for API configuration.

---

### /model

**Purpose**: Select a model for the current session.

**Usage**:
```bash
/model opus           # Switch to Opus
/model sonnet         # Switch to Sonnet
/model haiku          # Switch to Haiku
```

---

## System Commands

### /hooks-lite

**Purpose**: Enable minimal hooks configuration for token efficiency.

**Sets**:
- PostToolUse: `{"continue": true}` only
- Stop: Session completion logging
- ~90% token reduction vs full hooks

---

### /check-mcps

**Purpose**: Verify MCP server connection status.

**Checks**:
- Server availability
- Tool count
- Response times
- Error states

---

### /v1

**Purpose**: Emergency bypass - disable v2.0 enforcement for session.

**Usage**:
```bash
/v1                   # Allow v1 tools for this session
```

---

### /v1-once

**Purpose**: One-time bypass - allow single v1 tool call.

**Usage**:
```bash
/v1-once              # Allow next v1 tool only
```

---

## Domain-Specific Commands

### /ha

**Purpose**: Home Assistant conversation slash commands.

**Usage**:
```bash
/ha lights office off
/ha temperature living room
```

---

### /novel-os

**Purpose**: Restore Novel-OS manuscript rebuild context.

**Usage**:
```bash
/novel-os             # Restore context and continue work
```

---

## Creating Custom Commands

### File Structure

```markdown
# ~/.claude/commands/my-command.md

---
description: One-line description for command list
arguments:
  - name: arg1
    description: First argument
    required: true
allowed-tools: Bash(ls:*), Read, Write
---

# Command Title

## Purpose
What this command accomplishes.

## Usage
/my-command arg1

## Steps
1. First action
2. Second action

## Example
Show usage example here.
```

### Installation

1. Create file in `~/.claude/commands/`
2. Commands are available immediately (no restart needed)
3. Access via `/my-command`

### Best Practices

- Keep commands focused on single tasks
- Include clear usage examples
- Use `allowed-tools` for security
- Document expected outputs
- Add error handling guidance

---

## Command Quick Reference

| Command | Purpose | Category |
|---------|---------|----------|
| `/p` | Bootstrap pipeline | Core |
| `/auto-workflow` | Full 8-phase workflow | Core |
| `/context-save` | Save before compact | Context |
| `/context-restore` | Recover after reset | Context |
| `/mem ID` | Fetch memory details | Memory |
| `/remember` | Save learning | Memory |
| `/load-skills` | Load project skills | Skills |
| `/plan` | Feature planning | Dev |
| `/review` | Code review (3 hats) | Dev |
| `/work` | Git worktree session | Dev |
| `/ccs` | CCS CLI delegation | AI |
| `/model` | Switch AI model | System |
| `/check-mcps` | Verify MCPs | System |

