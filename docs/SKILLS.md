# Skills Reference

## Overview

Claude Reactor includes **53 skills** that extend Claude Code's capabilities. Skills are loaded dynamically based on project type, with 8 core skills always available.

---

## Skill Loading Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│                    SKILL LOADING FLOW                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Session Start                                                   │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────────┐                                            │
│  │ Load Core (8)   │  ←── Always loaded                         │
│  └─────────────────┘                                            │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────────┐     ┌─────────────────┐                   │
│  │ Detect Project  │────▶│ package.json?   │── Frontend        │
│  │ Type            │     │ Dockerfile?     │── DevOps          │
│  └─────────────────┘     │ requirements?   │── Backend         │
│       │                  └─────────────────┘                   │
│       ▼                                                          │
│  ┌─────────────────┐                                            │
│  │ Load Matching   │  ←── Project-specific skills               │
│  └─────────────────┘                                            │
│       │                                                          │
│       ▼                                                          │
│  Token Savings: ~84% vs loading all skills                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Core Skills (Always Loaded)

These 8 skills are critical for pipeline operation and load on every session.

### context-restore

**Purpose**: Recover session context after compaction or restart

**When Used**:
- After `/compact` command
- After session restart
- When context appears lost

**Key Actions**:
```python
mcp__unified-orchestrator__session_restore(
    include_infrastructure=True,
    include_tasks=True,
    auto_detect_project=True
)
```

---

### context-save

**Purpose**: Preserve session context before compaction

**When Used**:
- Before running `/compact`
- When context is getting full
- Before long operations

**Key Actions**:
```python
mcp__unified-orchestrator__session_checkpoint(
    summary="Current work summary",
    achievements=["Done items"],
    pending_tasks=["Remaining items"]
)
```

---

### store-memory

**Purpose**: Persist information to memlayer for future recall

**When Used**:
- After completing significant tasks
- When discovering important patterns
- When resolving errors

**Key Actions**:
```python
mcp__memlayer__remember(
    content="## Task: ...\n### Problem...",
    metadata={"category": "implementation"}
)
```

---

### consult-project-history

**Purpose**: Query project history for relevant context

**When Used**:
- Before starting similar tasks
- When debugging recurring issues
- When needing past decisions

**Key Actions**:
```python
mcp__memlayer__recall(
    query="authentication implementation",
    limit=5
)
```

---

### global-pipeline-agent

**Purpose**: Orchestrate the 8-phase pipeline

**When Used**:
- On `/p` command
- Automatic on complex tasks
- When workflow coordination needed

**Phases Managed**:
1. DISCOVER → CONTEXT → PLAN → SAFETY
2. EXECUTE → VERIFY → REVIEW → COMMIT

---

### auto-workflow

**Purpose**: Execute full 8-phase workflow automatically

**When Used**:
- On `/auto-workflow` command
- For complex multi-file changes
- When full validation needed

**Features**:
- Parallel tool execution where possible
- Automatic error recovery
- Memory checkpoints

---

### preflight-check

**Purpose**: Validate environment before execution

**Checks**:
- Git status (clean/dirty)
- Dependencies installed
- Ports available
- Required tools present

**Output**:
```
Pipeline: ✅ Preflight passed
- Git: Clean
- Deps: Installed
- Ports: Available
```

---

### task-completion-protocol

**Purpose**: Ensure proper task completion and documentation

**Steps**:
1. Verify all acceptance criteria met
2. Run tests/linting
3. Save to memory with full documentation
4. Update project state

---

## Project-Specific Skills

### Frontend Skills

#### dev-browser

**Tags**: `browser`, `testing`, `automation`
**Priority**: Low
**Loads For**: Frontend projects (package.json, tsconfig.json)

**Purpose**: Browser automation for development and testing

**Capabilities**:
- Take screenshots
- Check console logs
- Run accessibility audits
- Automate user flows

**Example**:
```python
mcp__browser-tools__takeScreenshot()
mcp__browser-tools__getConsoleLogs()
mcp__browser-tools__runAccessibilityAudit()
```

---

#### lint-gate

**Tags**: `quality`, `linting`, `enforcement`
**Priority**: Medium

**Purpose**: Enforce linting standards before commits

**Supported Linters**:
- ESLint (JavaScript/TypeScript)
- Prettier (formatting)
- Stylelint (CSS)

**Gate Logic**:
```
If lint errors > 0:
    Block commit
    Show errors with fix suggestions
Else:
    Allow commit
```

---

#### sequential-thinking

**Tags**: `thinking`, `planning`, `reasoning`
**Priority**: High

**Purpose**: Multi-step planning for complex UI tasks

**Features**:
- Branch exploration
- Revision support
- Hypothesis verification

**Example**:
```python
mcp__sequential-thinking__sequentialthinking(
    thought="Step 1: Analyze component structure",
    thought_number=1,
    total_thoughts=5,
    next_thought_needed=True
)
```

---

### Backend Skills

#### debugging-playbook

**Tags**: `debugging`, `troubleshooting`, `quality`
**Priority**: High

**Purpose**: Systematic debugging approaches

**Playbook Steps**:
1. Reproduce the issue
2. Isolate the component
3. Form hypothesis
4. Test hypothesis
5. Implement fix
6. Verify fix

---

#### tdd-enforcer

**Tags**: `testing`, `quality`, `enforcement`
**Priority**: Medium

**Purpose**: Enforce test-driven development

**Rules**:
- Tests must exist before implementation
- New code requires corresponding tests
- Test coverage must not decrease

---

#### failure-playbooks

**Tags**: `debugging`, `recovery`, `quality`
**Priority**: High

**Purpose**: Recovery strategies for common failures

**Patterns**:
- Database connection failures
- API timeout handling
- Memory leak detection
- Race condition resolution

---

### DevOps Skills

#### portmon

**Tags**: `utility`, `ports`, `monitoring`
**Priority**: Low

**Purpose**: Monitor and manage port usage

**Actions**:
```python
mcp__fast-port-checker__fast_check_port_available(port=3000)
mcp__fast-port-checker__fast_suggest_dev_port()
```

---

#### pipeline-health-check

**Tags**: `utility`, `health`, `monitoring`
**Priority**: Medium

**Purpose**: Verify pipeline component health

**Checks**:
- MCP server connectivity
- Hook execution
- Memory system
- Git integration

---

### Documentation Skills

#### auto-docs

**Tags**: `documentation`, `automation`
**Priority**: Medium

**Purpose**: Automatic documentation generation

**Generates**:
- API documentation
- Function signatures
- Usage examples
- Change logs

---

#### docs-first

**Tags**: `documentation`, `workflow`
**Priority**: Medium

**Purpose**: Documentation-driven development

**Workflow**:
1. Write docs first
2. Implement to match docs
3. Verify docs accuracy

---

#### context7-wrapper

**Tags**: `ai`, `context7`, `documentation`
**Priority**: Medium

**Purpose**: Library documentation lookup

**Usage**:
```python
mcp__context7__resolve-library-id(libraryName="react")
mcp__context7__get-library-docs(
    context7CompatibleLibraryID="/facebook/react",
    topic="hooks"
)
```

---

## Navigation & Code Skills

### auto-serena

**Tags**: `navigation`, `code`, `symbols`
**Priority**: High

**Purpose**: Semantic code navigation

**Capabilities**:
- Find symbol definitions
- Find references
- Rename symbols
- Navigate code structure

---

### serena-wrapper

**Tags**: `navigation`, `code`, `symbols`
**Priority**: Medium

**Purpose**: Serena tool wrapper with project context

---

## AI Integration Skills

### codex-wrapper

**Tags**: `ai`, `codex`, `integration`
**Priority**: Medium

**Purpose**: OpenAI Codex/Bun integration

**Usage**:
```python
mcp__codex__codex(
    prompt="Review this implementation",
    cwd="/path/to/project"
)
```

---

### gemini-mcp

**Tags**: `ai`, `gemini`, `integration`
**Priority**: Medium

**Purpose**: Google Gemini integration for roundtable

**Usage**:
```python
mcp__gemini__gemini(prompt="Analyze architecture")
mcp__gemini__gemini-reply(
    conversationId="...",
    prompt="Follow-up question"
)
```

---

### deepseek-ocr

**Tags**: `ocr`, `vision`, `ai`
**Priority**: Low

**Purpose**: OCR capabilities for documents and images

---

## Git & Version Control Skills

### git-safety-protocol

**Tags**: `git`, `safety`, `version-control`
**Priority**: High

**Purpose**: Safe git operations

**Rules**:
- Never force push to main/master
- Always create backups before destructive operations
- Use individual file staging (never `git add .`)

---

### git-handbrake

**Tags**: `git`, `safety`, `emergency`
**Priority**: High

**Purpose**: Emergency git snapshot for rollback

**Action**:
```bash
git stash create "handbrake-$(date +%s)"
```

---

## MCP Integration Skills

### mcp-pipeline

**Tags**: `mcp`, `integration`, `pipeline`
**Priority**: Medium

**Purpose**: MCP server pipeline configuration

---

### mcp-fallbacks

**Tags**: `mcp`, `integration`, `fallback`
**Priority**: Medium

**Purpose**: Fallback strategies when MCP servers fail

---

### omnimcp-workflow

**Tags**: `mcp`, `integration`, `omnimcp`
**Priority**: Medium

**Purpose**: OmniMCP gateway integration

---

## Security Skills

### secret-guard

**Tags**: `security`, `secrets`, `safety`
**Priority**: High

**Purpose**: Detect and protect secrets

**Scans For**:
- API keys
- Passwords
- Connection strings
- Private keys
- Tokens

---

### dependency-check

**Tags**: `security`, `dependencies`, `audit`
**Priority**: Medium

**Purpose**: Dependency security auditing

**Actions**:
- Check for known vulnerabilities
- Identify outdated packages
- Suggest updates

---

## Context Enhancement Skills

### acontext-enhancement

**Tags**: `context`, `enhancement`, `ai`
**Priority**: Low

**Purpose**: AI-powered context enhancement

---

### context-enhancement-triggers

**Tags**: `context`, `enhancement`, `triggers`
**Priority**: Low

**Purpose**: Define triggers for context enhancement

---

### local-context

**Tags**: `context`, `local`, `project`
**Priority**: Medium

**Purpose**: Project-local context management

---

## Utility Skills

### tool-selection

**Tags**: `utility`, `tools`, `selection`
**Priority**: Medium

**Purpose**: Intelligent tool selection for tasks

---

### cross-project-files

**Tags**: `utility`, `files`, `cross-project`
**Priority**: Low

**Purpose**: Handle files across project boundaries

---

### negative-cache

**Tags**: `utility`, `cache`, `optimization`
**Priority**: Low

**Purpose**: Cache negative results to avoid repeated failures

---

### run-python

**Tags**: `utility`, `python`, `execution`
**Priority**: Medium

**Purpose**: Python code execution wrapper

---

### python-with-memory

**Tags**: `utility`, `python`, `memory`
**Priority**: Medium

**Purpose**: Python execution with memory integration

---

## System Skills

### hook-system

**Tags**: `system`, `hooks`, `automation`
**Priority**: Medium

**Purpose**: Hook management and configuration

---

### compounding-cleanup

**Tags**: `system`, `cleanup`, `maintenance`
**Priority**: Low

**Purpose**: Clean up compounding resources

---

## External Integration Skills

### ccs-delegation

**Tags**: `external`, `ccs`, `delegation`
**Priority**: Low

**Purpose**: Delegate to CCS CLI for optimization

---

### novel-os-context-restore

**Tags**: `external`, `novel-os`, `context`
**Priority**: Low
**Project Specific**: novelos

**Purpose**: Novel-OS manuscript project context

---

## Creating Custom Skills

### Skill File Structure

```markdown
# ~/.claude/skills/my-skill.md

---
name: my-skill
description: One-line description for skill list
---

# Skill Name

## Purpose
What this skill accomplishes.

## When to Activate
- Trigger condition 1
- Trigger condition 2

## Process

### Step 1: First Action
Description of first step.

### Step 2: Second Action
Description of second step.

## Example Usage

\`\`\`python
# Code example
result = do_something()
\`\`\`

## Related Skills
- other-skill
- another-skill
```

### Registering in skills.json

```json
{
  "skills": {
    "my-skill": {
      "tags": ["category", "subcategory"],
      "priority": "medium",
      "always_load": false,
      "project_types": ["frontend", "backend"],
      "description": "What the skill does"
    }
  }
}
```

### Priority Levels

| Priority | Meaning | Loading |
|----------|---------|---------|
| `critical` | Essential for operation | Always |
| `high` | Important functionality | Early |
| `medium` | Useful features | On demand |
| `low` | Specialized use cases | When triggered |

---

## Skill Statistics

| Category | Count | Always Loaded |
|----------|-------|---------------|
| Core | 8 | Yes |
| Navigation | 2 | No |
| AI Integration | 4 | No |
| Git | 2 | No |
| Security | 2 | No |
| Documentation | 3 | No |
| MCP | 3 | No |
| DevOps | 2 | No |
| Frontend | 3 | No |
| Backend | 3 | No |
| Context | 4 | No |
| Utility | 7 | No |
| System | 2 | No |
| External | 2 | No |
| **Total** | **53** | **8** |
