# Workflow Integration Guide: ACE + Sequential-Thinking + Context7 + Serena

## The Complete Pipeline Flow

### 1. ORCHESTRATOR (unified-agentic-mcp)
The orchestrator is the central hub that coordinates all tools:

```bash
# Get all rules and workflow
mcp__unified-orchestrator__get_all_rules

# Get thinking rules specifically
mcp__unified-orchestrator__get_thinking_rules

# Use structured thinking for ANY task
mcp__unified-orchestrator__think_through(task="description", task_type="code/general")
```

### 2. SEQUENTIAL THINKING (MANDATORY for complex tasks)
Use BEFORE any significant work:

```python
mcp__sequential-thinking__sequentialthinking(
    thought="Current analysis step",
    thoughtNumber=1,
    totalThoughts=5,
    nextThoughtNeeded=True
)
```

**When to use (from orchestrator.py line 48-56):**
- Breaking down complex problems
- Planning and design
- Analysis needing course correction
- Multi-step solutions
- Tasks requiring context over multiple steps

### 3. ACE LEARNING SYSTEM
For code execution with automatic retry and learning:

```python
# Start agentic retry loop
mcp__ace__ace_code_retry_start(
    code="your code here",
    question="what problem this solves",
    max_iterations=5
)

# If fails, continue with improved code
mcp__ace__ace_code_retry_continue(
    session_id="from_start",
    improved_code="fixed code"
)
```

ACE learns from BOTH successes and failures.

### 3b. **CODEX CLI INTEGRATION**
Codex CLI is available as an MCP server for expert code review and analysis:

```bash
# Direct Codex commands (via MCP)
codex exec "review this pull request"
codex exec "refactor this function"
codex review path/to/file.js

# In workflow phases:
Phase 3 (PLAN): "codex OR gemini → 'Review this plan: [PLAN]'"
Phase 6 (VERIFY): codex review --diff
```

Codex integrates with the memory system to persist insights and patterns.

### 4. CONTEXT7 (Documentation Lookup)
**ALWAYS use before working with any library/technology:**

```python
# Resolve library ID first
mcp__context7__resolve-library_id(libraryName="react")

# Get documentation
mcp__context7__get-library-docs(
    context7CompatibleLibraryID="/facebook/react",
    topic="hooks",  # optional
    mode="code"  # "code" for API, "info" for guides
)
```

### 5. SERENA (Semantic Code Navigation)
For intelligent code search and modification:

```python
# Get overview of file symbols
mcp__serena__get_symbols_overview(relative_path="src/components/Button.jsx")

# Find specific symbols
mcp__serena__find_symbol(
    name_path_pattern="Button",
    relative_path="src/components",
    include_body=True
)

# Edit symbols precisely
mcp__serena__replace_symbol_body(
    name_path="Button/handleClick",
    relative_path="src/components/Button.jsx",
    body="new function body"
)
```

## The Correct Workflow Order

### For ANY Non-Trivial Task:

1. **CONTEXT FIRST**
   ```bash
   docs-first skill → README, CLAUDE.md
   ```

2. **PAST FAILURES**
   ```bash
   negative-cache skill → Query for similar issues
   ```

3. **SEQUENTIAL THINKING**
   ```bash
   mcp__sequential-thinking__sequentialthinking(...)
   ```

4. **CONTEXT7 DOCS**
   ```bash
   mcp__context7__resolve-library_id(...)
   mcp__context7__get-library-docs(...)
   ```

5. **PLAN REVIEW**
   ```bash
   codex OR gemini → "Review this plan: [PLAN]"
   ```

6. **SAFETY (Git Handbrake)**
   ```bash
   SNAP=$(git stash create "handbrake-$(date +%s)")
   ```

7. **EXECUTE (with ACE if code)**
   ```bash
   # If writing code:
   mcp__ace__ace_code_retry_start(...)
   # OR use Serena for navigation:
   mcp__serena__find_symbol(...)
   ```

8. **VERIFY**
   ```bash
   lint-gate
   pytest / npm test
   ```

9. **REMEMBER**
   ```bash
   mcp__unified-orchestrator__smart_remember(...)
   ```

## Integration Points

### Memory Rules (Automatic)
- **Save on**: task_completion, error_resolution
- **Recall on**: session_start, error_encountered, similar_task
- **Auto-behaviors**: Context saving before compaction

### Tools Status Check
```bash
# Check what's enabled
python3 -c "
import json
with open('/home/crogers2287/.claude/mcp.json') as f:
    data = json.load(f)
    for k, v in data.get('mcpServers', {}).items():
        if v.get('enabled'):
            print(f'✅ {k}')
        else:
            print(f'❌ {k}')
"
```

### Current Enabled Tools:
- ✅ **ace** - Code execution with learning
- ✅ **sequential-thinking** - Structured planning
- ✅ **context7** - Documentation lookup
- ✅ **serena** - Semantic code navigation
- ✅ **unified-orchestrator** - Central coordination
- ✅ **memlayer** - Persistent storage
- ✅ **browser-tools** - Web automation
- ✅ **fast-port-checker** - Port utilities
- ✅ **flowlens** - Browser debugging
- ✅ **claude-mem-search** - Semantic memory

## Critical Reminders

1. **Sequential thinking is MANDATORY** for complex tasks (line 1136)
2. **Always use context7** before working with new libraries
3. **ACE learns automatically** - let it retry and improve
4. **Serena understands code structure** - use it for navigation
5. **Memory is automatic** - but call smart_remember for important completions
6. **NEVER skip git-handbrake** for risky edits

## Testing the Integration

```python
# Test all systems are working
mcp__unified-orchestrator__get_all_rules

# Test sequential thinking
mcp__sequential-thinking__sequentialthinking(
    thought="Testing integration workflow",
    thoughtNumber=1,
    totalThoughts=1,
    nextThoughtNeeded=False
)

# Test context7
mcp__context7__resolve-library_id(libraryName="express")

# Test ACE
mcp__ace__ace_help(topic="quick_start")

# Test Serena
mcp__serena__initial_instructions()
```

This integration ensures you're never "flying blind" - always have docs, context, and structured thinking supporting your work.