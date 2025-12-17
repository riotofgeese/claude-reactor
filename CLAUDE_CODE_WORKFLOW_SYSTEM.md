# Claude Code Workflow System - Complete Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Core Principles](#core-principles)
3. [Workflow Phases](#workflow-phases)
4. [Skills System](#skills-system)
5. [MCP Integration](#mcp-integration)
6. [Memory Hierarchy](#memory-hierarchy)
7. [Tools & Components](#tools--components)
8. [Installation & Setup](#installation--setup)
9. [Usage Examples](#usage-examples)
10. [Integration with External Tools](#integration-with-external-tools)
11. [Troubleshooting](#troubleshooting)
12. [Best Practices](#best-practices)

## System Overview

The Claude Code Workflow System is a comprehensive, integrated development environment that combines structured thinking, intelligent tooling, and persistent memory to create a continuously improving coding experience. It orchestrates multiple specialized tools through a unified workflow that ensures consistency, reliability, and knowledge retention across sessions.

### Key Components
- **Workflow Engine**: 8-phase structured development process
- **Skills System**: Reusable, composable tools for common tasks
- **MCP Integration**: Model Context Protocol servers for specialized capabilities
- **Memory System**: 4-tier persistent memory for context preservation
- **Protocol Enforcement**: DOING/EXPECTED/IF WRONG methodology
- **External Integrations**: Codex CLI, Serena, Context7, ACE, and more

## Core Principles

### 1. Reality Gap Principle
*"Reality doesn't care about your model. The gap between model and reality is where all failures live."*

### 2. STOP Protocol
When anything fails: STOP. Explain to user. Wait for confirmation before proceeding.

### 3. DOING Protocol (CRITICAL - NON-NEGOTIABLE)
Before EVERY action:
```
DOING: [action]
EXPECT: [predicted outcome]
IF WRONG: [what that means]
```
Execute → Compare → Mismatch = STOP

### 4. Checkpoint Rule
Max 3 actions before verifying reality matches your model. Thinking ≠ verification.

## Workflow Phases

### The Complete 8-Phase Workflow

#### Phase 0: AUTO-WORKFLOW (Default)
For any non-trivial task, invoke the `auto-workflow` skill FIRST:
```bash
auto-workflow skill
```
This automatically runs:
1. Context search (auto-context.sh)
2. Past failure check (negative-cache)
3. Planning (sequential-thinking)
4. Roundtable review (codex + gemini)

Skip to Phase 4 (SAFETY) after auto-workflow completes.

#### Phase 1: PREFLIGHT
Environment validation and preparation:
```bash
preflight-check skill
```
- Verify toolchain versions
- Check git state
- Confirm dependencies installed
- Validate environment setup

#### Phase 2: CONTEXT
Information gathering and research:
```bash
# Read project documentation
docs-first skill → README, CLAUDE.md, CONTRIBUTING

# Check for past failures
negative-cache skill → Query memlayer for failed approaches

# Automatic codebase search
~/.claude/bin/auto-context.sh "task description"

# Get library documentation if needed
context7 → resolve-library-id → get-library-docs
```

#### Phase 3: PLAN
Structured planning and validation:
```bash
# Complex tasks: Use structured reasoning
sequential-thinking MCP

# Bug fixes: Write failing test first
tdd-enforcer skill

# Plan review with AI
codex OR gemini MCP → "Review this plan: [PLAN]"
```

#### Phase 4: SAFETY
Risk mitigation before execution:
```bash
# Git snapshot for rollback
git-handbrake skill → SNAP=$(git stash create "handbrake-$(date +%s)")

# Validate dependencies exist
dependency-check skill
```

#### Phase 5: EXECUTE
Implementation and code creation:
```bash
# Write code with learning system
ACE MCP with automatic retry
# OR use sandbox for isolated execution
run_python MCP
```

#### Phase 6: VERIFY
Quality assurance and testing:
```bash
# Lint gate (before LLM review)
lint-gate skill → eslint/mypy/ruff

# Run tests
pytest / npm test

# UI testing
dev-browser skill → headless Playwright

# Security scan
secret-guard skill
```

#### Phase 7: RECOVERY (If Failed)
Error handling and rollback:
```bash
# Check typed recovery patterns
failure-playbooks skill

# Log failure to memory
negative-cache skill

# Rollback if needed
git checkout -- . && git stash apply $SNAP
```

#### Phase 8: COMMIT
Success documentation and cleanup:
```bash
# Save to memory
smart_remember → task_completion

# Add files individually (NEVER git add .)
git add FILE1 FILE2
```

## Skills System

Skills are composable tools that automate common workflow tasks. Each skill has a specific purpose and integration point.

### Core Skills Matrix

| Skill | Purpose | When to Use | Integration |
|-------|---------|-------------|-------------|
| **auto-workflow** | **MAGIC: Context→Plan→Review** | **START HERE** | Orchestrates other skills |
| preflight-check | Environment validation | Start of task | System checks |
| docs-first | Read project docs | Before planning | File readers |
| negative-cache | Check past failures | Before planning | Memlayer |
| local-context | Semantic code search | Before planning (auto) | Code search |
| dependency-check | Validate imports | Before coding | Package managers |
| git-handbrake | Snapshot for rollback | Before edits | Git |
| lint-gate | Pre-LLM linting filter | After code | Linters |
| tdd-enforcer | Write failing test first | Bug fixes | Test frameworks |
| secret-guard | Scan for credentials | Before commit | Security |
| failure-playbooks | Typed error recovery | When errors occur | Error patterns |
| dev-browser | Headless Playwright | UI testing | Browser automation |
| context7 | Library docs | Need API info | Documentation |
| codex/gemini | Plan review | Plan validation | External AI |
| sequential-thinking | Complex planning | Complex tasks | Structured reasoning |

### Skill Implementation Example
Skills are Markdown files with structured headers:
```markdown
---
description: Brief description
---

<system-reminder>
Implementation instructions and context
</system-reminder>
```

## MCP Integration

Model Context Protocol (MCP) servers provide specialized capabilities that integrate seamlessly into the workflow.

### Core MCP Servers

#### 1. Unified Orchestrator (unified-orchestrator)
**Purpose**: Central coordination, session state, memory rules
**Key Functions**:
```python
# Memory management
mcp__unified-orchestrator__smart_remember(
  event_type="task_completion",
  content={task, outcome, files_changed}
)

# Session restoration
mcp__unified-orchestrator__session_restore(
  include_infrastructure=True,
  include_tasks=True
)

# Infrastructure management
mcp__unified-orchestrator__save_infrastructure(
  name="prod-api",
  infra_type="server",
  environment="production"
)
```

#### 2. ACE (ace)
**Purpose**: Code execution with automatic learning and retry
**Key Functions**:
```python
# Start with retry loop
mcp__ace__ace_code_retry_start(
  code="implementation",
  question="what problem this solves",
  max_iterations=5
)

# Continue with improved code
mcp__ace__ace_code_retry_continue(
  session_id="from_start",
  improved_code="fixed code"
)
```

#### 3. Sequential Thinking (sequential-thinking)
**Purpose**: MANDATORY for complex tasks - structured reasoning
**When Required** (from orchestrator.py lines 48-56):
- Breaking down complex problems
- Planning and design
- Analysis needing course correction
- Multi-step solutions
- Tasks requiring context over multiple steps

#### 4. Context7 (context7)
**Purpose**: Documentation lookup - ALWAYS use before new libraries
**Usage Pattern**:
```python
# First: Resolve library ID
mcp__context7__resolve-library_id(libraryName="react")

# Then: Get documentation
mcp__context7__get-library-docs(
  context7CompatibleLibraryID="/facebook/react",
  topic="hooks",
  mode="code"  # "code" for API, "info" for guides
)
```

#### 5. Serena (serena)
**Purpose**: Semantic code navigation and editing
**Key Functions**:
```python
# Get file overview
mcp__serena__get_symbols_overview(relative_path="src/main.js")

# Find symbols
mcp__serena__find_symbol(
  name_path_pattern="authenticateUser",
  relative_path="src",
  include_body=True
)

# Edit symbols precisely
mcp__serena__replace_symbol_body(
  name_path="User/authenticate",
  relative_path="src/User.js",
  body="new implementation"
)
```

#### 6. Memlayer (memlayer)
**Purpose**: Persistent semantic storage
**Key Functions**:
```python
# Store information
mcp__memlayer__remember(
    content="Important pattern or insight",
    metadata={"category": "security", "priority": "high"}
)

# Retrieve information
mcp__memlayer__recall(query="authentication patterns", limit=10)
```

#### 7. Additional MCPs
- **browser-tools**: Web automation and screenshots
- **fast-port-checker**: Port utilities
- **flowlens**: Browser flow debugging
- **claude-mem**: Session-persistent memory
- **omada-mcp-server**: Network management

## Memory Hierarchy

The system uses a 4-tier memory architecture to ensure no valuable context is lost.

### Tier 1: Session Memory
- **Persistence**: Current conversation only
- **Features**: Unlimited context through automatic summarization
- **Restoration**: Enhanced by memory recall on session start

### Tier 2: Smart Memory (unified-orchestrator)
- **Persistence**: Session-to-session, project-scoped
- **Events**: task_completion, error_resolution, infrastructure, deployment
- **Commands**:
```python
# Success storage
mcp__unified-orchestrator__smart_remember(
  event_type="task_completion",
  content={
    "task": "What was done",
    "outcome": "Result achieved",
    "files_changed": ["file1.py", "file2.js"],
    "lessons": ["Key insights"]
  }
)

# Session checkpoint (before compaction)
mcp__unified-orchestrator__session_checkpoint(
  summary="Current work summary",
  achievements=["completed items"],
  pending_tasks=["todo items"]
)
```

### Tier 3: Semantic Memory (memlayer + claude-mem)
- **Persistence**: Permanent, cross-project
- **Purpose**: Long-term storage of insights, patterns, solutions
- **Features**: 1600+ memories, automatic recall, semantic search

### Tier 4: Documentation Cache (DocVault)
- **Persistence**: Local files, version-controlled
- **Purpose**: Auto-downloaded library documentation
- **Features**:
  - Automatic detection via `detector.py`
  - Categorization (frontend, backend, testing, etc.)
  - Version-specific storage
  - Fast local retrieval

## Tools & Components

### Global Pipeline Agent
A performance-optimized agent that provides context and guidance:
```python
# Session start (2s budget)
agent.run_session_start()

# Text entry analysis (800ms budget)
agent.run_text_entry(prompt)
```

### DocVault System
Automatic documentation management:
- **detector.py**: Scans for libraries and dependencies
- **auto-docs.sh**: Hook for downloading documentation
- Caches docs locally for instant access

### Protocol Enforcement
**pre-tool-use-protocol.sh** hook enforces DOING/EXPECTED/IF WRONG:
```bash
# Triggers for significant operations
# Provides color-coded reminders
# Logs protocol compliance
```

### Git Integration
```bash
# Handbrake (before risky edits)
SNAP=$(git stash create "handbrake-$(date +%s)")

# Individual file commits (NEVER git add .)
git add specific_file.py
```

## Installation & Setup

### 1. Install Enhanced Pipeline
```bash
# Run the enhanced installer
~/.claude/install-pipeline-enhanced.sh

# What it installs:
- Skills directory (symlinked)
- Filtered MCP config (enabled servers only)
- Condensed CLAUDE.md (45% token reduction)
- Critical hooks (DOING/EXPECTED/IF WRONG)
- Command directory (slash commands)
```

### 2. MCP Server Configuration
```bash
# Check enabled MCPs
python3 -c "
import json
with open('/home/crogers2287/.claude/mcp.json') as f:
    data = json.load(f)
    for k, v in data.get('mcpServers', {}).items():
        if v.get('enabled'):
            print(f'✅ {k}')
"
```

### 3. Codex CLI Integration (Optional)
```bash
# Add all MCP servers to Codex CLI
~/.claude/add_mcps_to_codex.sh

# Use in Codex CLI
codex  # All MCPs available via natural language
```

### 4. Verify Installation
```bash
# Check all components
/p  # Initialize and verify pipeline

# Test MCP connections
mcp__unified-orchestrator__get_all_rules

# Test memory
mcp__memlayer__get_stats()
```

## Usage Examples

### Example 1: New Feature Implementation
```
User: Add user authentication to this Express.js app

Workflow:
1. auto-workflow → Runs context, failures, planning, review
2. Context: docs-first reads project README, negative-cache checks auth attempts
3. Planning: sequential-thinking breaks down into:
   - Install passport.js
   - Configure JWT strategy
   - Create auth routes
   - Add middleware
4. Review: codex suggests using refresh tokens
5. Safety: git-handbrake creates snapshot
6. Execute: ACE implements with retry learning
7. Verify: lint-gate passes, tests run
8. Remember: smart_remember saves auth pattern
```

### Example 2: Bug Fix
```
User: Fix the failing login endpoint

Workflow:
1. tdd-enforcer → Write failing test first
2. Context: local-context finds login route
3. Context7: Gets passport.js docs
4. Execute: ACE fixes and learns from attempts
5. Verify: Test now passes
6. Remember: failure_playbooks records pattern
```

### Example 3: Code Review
```
User: Review this pull request for security issues

Workflow:
1. Context: git-handbrake (if testing locally)
2. codex/gemini: "Review for security vulnerabilities"
3. context7: Gets security best practices docs
4. Execute: ACE runs security scanning
5. secret-guard: Checks for exposed credentials
6. Remember: smart_remember saves security patterns
```

## Integration with External Tools

### Codex CLI Integration
All MCP servers are available in Codex CLI:
```bash
# Setup complete
codex

# Usage examples:
"Use sequential-thinking to plan X"
"Get context7 docs for React"
"Remember to memlayer: JWT pattern"
"Use serena to find auth middleware"
```

### Serena Integration
Semantic code navigation:
```python
# Find and navigate code
mcp__serena__find_symbol("User/authenticate")

# Edit with precision
mcp__serena__replace_symbol_body(
    name_path=" authenticate",
    relative_path="models/User.js",
    body="new implementation"
)
```

### ACE Learning System
Code execution with persistent learning:
```python
# ACE learns from both success and failure
# Retry loop automatically improves approaches
# Knowledge persists across sessions
```

## Troubleshooting

### Common Issues

#### 1. MCP Server Not Starting
```bash
# Check server status
ps aux | grep mcp

# Restart specific server
codex mcp remove <name>
codex mcp add <name> -- <command>
```

#### 2. Memory Not Persisting
```bash
# Check memlayer database
ls -la /home/crogers2287/mcp-server-memlayer/memlayer-storage

# Verify claude-mem plugin enabled
grep '"claude-mem@thedotmack": true' ~/.claude/settings.json
```

#### 3. Protocol Not Triggering
```bash
# Check hook exists
ls -la ~/.claude/hooks/pre-tool-use-protocol.sh

# Verify permissions
chmod +x ~/.claude/hooks/pre-tool-use-protocol.sh
```

#### 4. Context7 Not Working
```bash
# Test library resolution
mcp__context7__resolve-library-id(libraryName="express")

# Check internet connection
curl -I https://context7.com
```

### Performance Issues

#### Memory Usage
- Session memory auto-compacts
- Use memory rules to filter recall
- Clear old cache entries

#### Tool Timeouts
- Check performance budgets:
  - Session start: 2s
  - Text entry: 800ms
  - Fast checks: 100ms

## Best Practices

### 1. Always Follow Protocol
- DOING/EXPECTED/IF WRONG before EVERY action
- Verify reality every 3 actions
- Stop on mismatch

### 2. Use Memory Effectively
```python
# Save insights immediately
mcp__unified-orchestrator__smart_remember(
  event_type="task_completion",
  content={task, outcome, lessons}
)

# Recall before similar tasks
mcp__unified-orchestrator__smart_recall(
  context="similar_task"
)
```

### 3. Leverage Auto-Workflow
- Start with `auto-workflow` for non-trivial tasks
- Trust the sequential thinking process
- Use AI reviews for validation

### 4. Documentation First
```python
# Always get docs before using new libraries
mcp__context7__resolve-library_id(libraryName)
mcp__context7__get_library-docs(library_id, topic="api")
```

### 5. Safety Always
```bash
# Before risky changes
SNAP=$(git stash create "handbrake-$(date +%s)")

# Verify before commit
lint-gate
pytest
secret-guard
```

### 6. Clean Commits
```bash
# NEVER git add .
git add file1.py file2.js  # Add individually
```

## Advanced Features

### Custom Skills Creation
Create new skills by adding Markdown files to `~/.claude/skills/`:
```markdown
---
description: Your skill description
---

<system-reminder>
Skill implementation and usage instructions
</system-reminder>
```

### Custom MCP Integration
Add new MCP servers to `~/.claude/mcp.json`:
```json
{
  "mcpServers": {
    "your-server": {
      "command": "node",
      "args": ["path/to/server.js"],
      "enabled": true
    }
  }
}
```

### Memory Rules Customization
Configure automatic memory rules in orchestrator:
```python
# Custom event types
event_types=["custom_event", "special_pattern"]

# Auto-save triggers
save_on=["file_save", "test_pass", "deployment"]
```

## Summary

The Claude Code Workflow System provides:
1. **Structure**: 8-phase consistent development process
2. **Intelligence**: AI-powered tools that learn and improve
3. **Memory**: 4-tier persistent knowledge system
4. **Integration**: Seamless tool orchestration
5. **Flexibility**: Adaptable to any project or workflow
6. **Reliability**: Protocol enforcement and safety measures

By following this system, developers create high-quality code while continuously building a knowledge base that improves future work. The integration of specialized tools like Codex CLI, Serena, Context7, and ACE creates a comprehensive development environment that adapts and learns with every use.

## Quick Reference Commands

```bash
# Initialize workflow
/p

# Auto-workflow for tasks
auto-workflow

# Memory operations
smart_remember → task completion
negative-cache → check failures
memlayer recall → search patterns

# Safety
git-handbrake → create snapshot
dependency-check → validate imports

# Quality
lint-gate → pre-review
secret-guard → scan secrets

# Documentation
context7 → get library docs
docs-first → read project docs

# Planning
sequential-thinking → structured plan
codex/gemini → review plan

# Execution
ace → code with learning
serena → navigate/modify code

# External Integration
codex → use in CLI with all MCPs
```

This system represents a complete, production-ready workflow for modern software development, combining the best of human expertise with AI assistance in a structured, reliable framework.