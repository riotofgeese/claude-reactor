# Memory Hierarchy Documentation

## Overview
The integrated pipeline uses a 4-tier memory system designed for persistence, recall, and context preservation across sessions and compactions.

## Tiers (from most to least persistent)

### 1. Semantic Memory (memlayer + claude-mem)
**Persistence**: Permanent, cross-project
**Purpose**: Long-term storage of insights, patterns, and solutions
**Commands**:
```python
# Store information
mcp__memlayer__remember(
    content="Important insight or pattern",
    metadata={"category": "architecture", "priority": "high"}
)

# Retrieve information
mcp__memlayer__recall(query="database connection patterns", limit=5)

# Get all memories (for audit)
mcp__memlayer__get_all_memories(limit=50)
```

**Auto-triggers**:
- Task completions with `smart_reember`
- Error resolutions with lessons learned
- Infrastructure details (servers, databases, APIs)
- Project-specific context

### 2. Smart Memory (unified-orchestrator)
**Persistence**: Session-to-session, project-scoped
**Purpose**: Structured storage of task outcomes and infractions
**Commands**:
```python
# Success storage
mcp__unified-orchestrator__smart_remember(
    event_type="task_completion",
    content={
        "task": "Implemented authentication system",
        "outcome": "JWT tokens with refresh rotation",
        "files_changed": ["auth.py", "models.py"],
        "lessons": ["Use httpOnly cookies for security"]
    }
)

# Failure storage
mcp__unified-orchestrator__smart_remember(
    event_type="error_resolution",
    content={
        "approach": "Direct database connection without pooling",
        "error": "Connection timeouts under load",
        "avoid": "Always use connection pooling"
    },
    extra_metadata={"result": "failure"}
)

# Session checkpoint (before compaction)
mcp__unified-orchestrator__session_checkpoint(
    summary="Implemented OAuth2 integration",
    achievements=["Created auth endpoints", "Added middleware"],
    pending_tasks=["Test refresh token flow"]
)
```

**Memory Rules (Automatic)**:
- Save on: `task_completion`, `error_resolution`, `infrastructure`, `deployment`
- Recall on: `session_start`, `error_encountered`, `similar_task`
- Auto-behavior: Context saving before compaction

### 3. Documentation Cache (DocVault)
**Persistence**: Local files, version-controlled
**Purpose**: Auto-downloaded library documentation for offline access
**Location**: `~/.claude/docvault/docs/{library}/{version}/`
**Commands** (via context7):
```python
# Resolve library ID first
mcp__context7__resolve-library-id(libraryName="react")

# Get documentation (auto-cached)
mcp__context7__get-library-docs(
    context7CompatibleLibraryID="/facebook/react",
    topic="hooks",
    mode="code"  # "code" for API, "info" for guides
)
```

**Features**:
- Automatic detection via `detector.py`
- Categorization (frontend, backend, testing, etc.)
- Version-specific storage
- Fast local retrieval

### 4. Session Memory
**Persistence**: Current conversation only
**Purpose**: Immediate context and working memory
**Features**:
- Unlimited context through automatic summarization
- Preserved across compactions via `session_checkpoint`
- Enhanced by memory recall on session start

## Integration Flow

### Session Start
1. `session_restore` loads:
   - Infrastructure details
   - Current task state
   - Recent work context
   - Project-specific memories

### During Work
1. **Before new task**:
   ```python
   mcp__unified-orchestrator__smart_recall(
       context="similar_task",
       context_details={"task": "current task description"}
   )
   ```

2. **During task**:
   - Use context7 for documentation
   - ACE learns from retries
   - Sequential thinking structures approach

3. **After task**:
   ```python
   mcp__unified-orchestrator__smart_remember(
       event_type="task_completion",
       content={task, outcome, files_changed}
   )
   ```

### Before Compaction
```python
mcp__unified-orchestrator__session_checkpoint(
    summary="Current work summary",
    achievements=["completed items"],
    pending_tasks=["todo items"],
    important_context="critical state to preserve"
)
```

## Memory Recall Patterns

### Error Recovery
```python
# When errors occur
mcp__unified-orchestrator__smart_recall(
    context="error_encountered",
    context_details={"error_type": "connection_timeout"}
)

# Also check semantic memory
mcp__memlayer__recall(query="connection timeout solutions")
```

### Project Context
```python
# Project-specific memories
mcp__memlayer__recall(query="authentication patterns", limit=10)

# Recent work in this project
mcp__unified-orchestrator__smart_recall(
    context="session_start",
    context_details={"project": "current_project"}
)
```

### Infrastructure Recall
```python
# Get saved infrastructure
mcp__unified-orchestrator__get_infrastructure(
    name="prod-api",
    infra_type="server",
    environment="production"
)
```

## Best Practices

1. **Save Early, Save Often**
   - Don't batch memory saves
   - Save immediately after each significant outcome
   - Include lessons learned in failures

2. **Structured Content**
   - Use consistent schemas for events
   - Include file paths changed
   - Tag with categories for easier retrieval

3. **Query Strategies**
   - Start with specific queries, then broaden
   - Use semantic search for patterns
   - Filter by project when relevant

4. **Context Preservation**
   - Always create session checkpoints before compaction
   - Include task state and next steps
   - Save partial progress

## Example Workflow

```python
# 1. Session start - restore context
mcp__unified-orchestrator__session_restore(include_infrastructure=True)

# 2. New task - check for similar work
mcp__unified-orchestrator__smart_recall(
    context="similar_task",
    context_details={"task": "add user authentication"}
)

# 3. Plan - use structured thinking
mcp__sequential-thinking__sequentialthinking(...)

# 4. Research - get docs
mcp__context7__resolve-library_id(libraryName="passport.js")
mcp__context7__get-library-docs(...)

# 5. Execute - with ACE learning
mcp__ace__ace_code_retry_start(...)

# 6. Complete - save outcome
mcp__unified-orchestrator__smart_remember(
    event_type="task_completion",
    content={
        "task": "Added Passport.js authentication",
        "outcome": "Local strategy with JWT tokens",
        "files_changed": ["auth.js", "routes.js"],
        "next": "Add OAuth providers"
    }
)
```

## Troubleshooting

### Memory Not Saving
- Check MCP server status
- Verify memlayer database is running
- Check file permissions for cache directories

### Context Loss After Compaction
- Ensure `session_checkpoint` was called
- Verify checkpoint files exist: `/tmp/session_checkpoint_*.json`
- Check hooks are properly configured

### Slow Recall
- Use memory rules to filter by type/date
- Limit query results with `limit` parameter
- Cache frequently accessed memories

This 4-tier system ensures no valuable context is lost, patterns are preserved, and work continues seamlessly across sessions.