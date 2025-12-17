# Codex CLI Integration with Workflow Pipeline

## Current Integration Status
✅ **Codex CLI is already integrated as an MCP server**

### What's Already Set Up:
1. **Codex MCP Server**: Running at `/home/crogers2287/.bun/bin/codex mcp-server`
2. **Bridge Script**: `codex_agentic_bridge.sh` provides context to Codex
3. **MCP Configuration**: Enabled in `.mcp.json.filtered`

## Using Codex CLI with the Integrated Workflow

### 1. Direct Codex Commands
```bash
# Execute tasks with Codex
codex exec "review this pull request"
codex exec "refactor this function"
codex exec "write tests for this module"

# Review specific files
codex review path/to/file.js
codex review --diff # Review staged changes
```

### 2. Codex via MCP (Recommended)
In Claude Code, you can directly invoke Codex through the MCP integration:

```python
# Codex is available as an MCP tool
# Use it for plan reviews and code analysis
```

### 3. Enhanced Workflow Integration

#### Before Using Codex:
```bash
# 1. Get project context
/p  # Initialize pipeline

# 2. Check for similar tasks
mcp__unified-orchestrator__smart_recall(
    context="similar_task",
    context_details={"task": "your current task"}
)
```

#### Using Codex in the Workflow:
```
Phase 3 (PLAN): Use Codex for plan review
→ "codex OR gemini → 'Review this plan: [PLAN]'"

Phase 6 (VERIFY): Use Codex for code review
→ codex review --diff
→ codex exec "check for security issues"
```

#### After Codex:
```bash
# Save insights
mcp__unified-orchestrator__smart_remember(
    event_type="task_completion",
    content={
        "task": "Code review with Codex",
        "outcome": "Found 3 optimizations",
        "files_reviewed": ["file1.js", "file2.js"],
        "codex_suggestions": ["suggestion1", "suggestion2"]
    }
)
```

## Codex CLI + Memory System

### 1. Context Sharing
The bridge script (`codex_agentic_bridge.sh`) provides:
- Project context in `/tmp/agentic_pipeline_context.json`
- Session state and recent work
- Memory recall from previous sessions

### 2. Persistent Learning
```bash
# Codex insights are automatically saved to memory
mcp__memlayer__remember(
    content="Codex suggested using async/await for better performance",
    metadata={"source": "codex", "category": "performance"}
)

# Recall Codex insights later
mcp__memlayer__recall(query="Codex performance suggestions")
```

## Advanced Integration Patterns

### 1. Codex as Plan Reviewer
```bash
# After sequential-thinking plan
mcp__sequential-thinking__sequentialthinking(
    thought="Initial plan for feature X",
    thoughtNumber=1,
    totalThoughts=5,
    nextThoughtNeeded=True
)

# Then: Review with Codex
codex exec "Review this implementation plan: [paste plan]"
```

### 2. Codex + ACE Learning
```bash
# Let Codex suggest approach, then ACE executes
codex exec "Suggest best approach for X"

# Execute with ACE learning
mcp__ace__ace_code_retry_start(
    code="# Implementation based on Codex suggestion",
    question="Implement X using Codex's recommended approach"
)
```

### 3. Codex for Documentation
```bash
# Generate docs with Codex
codex exec "Write API documentation for this module"
codex exec "Create README for this project"

# Enhance with context7
mcp__context7__get-library_docs(library="/framework/name")
codex exec "Update docs based on latest API changes"
```

## Best Practices

### 1. Always Provide Context
```bash
# Before sending to Codex
git diff --cached > /tmp/changes.diff
codex exec "Review these changes: $(cat /tmp/changes.diff)"
```

### 2. Use Codex for Specific Tasks
- **Code Reviews**: `codex review` or `codex exec "review"`
- **Refactoring**: `codex exec "refactor this for better performance"`
- **Testing**: `codex exec "write unit tests for this function"`
- **Documentation**: `codex exec "document this API"`
- **Security**: `codex exec "check for security vulnerabilities"`

### 3. Combine with Memory System
```bash
# Save successful Codex suggestions
mcp__unified-orchestrator__smart_remember(
    event_type="task_completion",
    content={
        "task": "Security review with Codex",
        "codex_finding": "Missing input validation",
        "resolution": "Added validation middleware",
        "pattern": "Always validate user input"
    }
)
```

## Troubleshooting

### Codex MCP Not Available:
```bash
# Check if Codex is installed
which codex

# Check MCP server status
ps aux | grep "codex mcp-server"

# Restart if needed
killall codex
codex mcp-server &
```

### Bridge Script Issues:
```bash
# Make sure it's executable
chmod +x /home/crogers2287/sandbox/codex_agentic_bridge.sh

# Test manually
./codex_agentic_bridge.sh
```

## Integration with Git Hooks (Optional)

Add to `.git/hooks/pre-push`:
```bash
#!/bin/bash
# Pre-push Codex review
echo "Running Codex review on changes..."

# Get changes to be pushed
git diff --cached --name-only | while read file; do
    if [[ "$file" =~ \.(js|ts|py|java|cpp)$ ]]; then
        codex review "$file" || true
    fi
done

echo "Review complete."
```

## Summary

Codex CLI is fully integrated into the workflow pipeline:
- ✅ Available as MCP server
- ✅ Bridge script provides context
- ✅ Works with memory system
- ✅ Integrates with all workflow phases

Use Codex for:
1. Plan reviews (Phase 3)
2. Code reviews (Phase 6)
3. Refactoring suggestions
4. Test generation
5. Documentation

The integration ensures Codex has full context from the memory system and contributes its insights back to the persistent knowledge base.