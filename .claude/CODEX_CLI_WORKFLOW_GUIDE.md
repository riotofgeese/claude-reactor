# Using Your Workflow in Codex CLI

## Setup Complete ✅

All your MCP servers are now configured and available in Codex CLI:
- unified-orchestrator
- memlayer
- ace
- sequential-thinking
- context7
- serena
- claude-mem
- browser-tools
- fast-port-checker
- omada-mcp-server
- flowlens

## Starting Codex CLI with Full Workflow

```bash
# Basic start
codex

# Start with workspace write access (recommended for workflow)
codex --sandbox workspace-write

# Start with full auto (least friction)
codex --full-auto

# Start in specific directory
codex --cd /path/to/your/project
```

## Workflow Commands in Codex CLI

### 1. Context Gathering
```
Get context7 documentation for React
```
or
```
Use context7 to look up express.js docs
```

### 2. Planning with Sequential Thinking
```
Use sequential-thinking to break down this task: [describe task]
```

### 3. Memory Operations
```
Remember to memlayer: The authentication flow uses JWT tokens with refresh rotation
```

or
```
Recall from memlayer: database connection patterns
```

### 4. Code Navigation with Serena
```
Use serena to find the authentication middleware
```

### 5. Code Execution with ACE
```
Use ace to execute this Python code and learn from failures:
```python
# Your code here
```

### 6. Smart Memory with Unified Orchestrator
```
Save to smart_remember: task completed, implemented user authentication
```

### 7. Browser Automation
```
Use browser-tools to take a screenshot of http://localhost:3000
```

### 8. Port Management
```
Use fast-port-checker to find an available port starting from 3000
```

## Complete Workflow Example

```
User: I need to add user authentication to this Express.js app

Codex: I'll help you add user authentication. Let me start by gathering context.

[Uses context7 to get Express.js and authentication docs]
[Uses sequential-thinking to plan the implementation]
[Uses serena to navigate existing code structure]
[Uses ace to implement the authentication routes]
[Uses memlayer to remember the patterns used]
[Uses smart_remember to save task completion]
```

## Key Features Available

### Memory System
- **memlayer**: Long-term semantic memory
  - "Remember to memlayer: JWT is better than session cookies"
  - "Recall from memlayer: password hashing best practices"

- **claude-mem**: Session-persistent memory
  - Automatically available across sessions

- **unified-orchestrator**: Smart task memory
  - "Save task completion: added auth middleware"
  - Infrastructure and server details

### Code Analysis
- **serena**: Semantic code understanding
  - "Find all database connection code"
  - "Show me the user model definition"

- **ace**: Code execution with learning
  - Executes code in sandbox
  - Learns from failures and retries

### Planning
- **sequential-thinking**: Structured planning
  - Breaks down complex tasks
  - Step-by-step reasoning

### Documentation
- **context7**: Always-available docs
  - "Get docs for any library"
  - No more flying blind

### Development Tools
- **browser-tools**: Web automation
- **fast-port-checker**: Port utilities
- **flowlens**: Browser debugging
- **omada-mcp-server**: Network management

## Pro Tips

### 1. Start with Context
Always ask Codex to check documentation first:
```
Get context7 docs for [library] before implementing
```

### 2. Use Memory Effectively
Save patterns you discover:
```
Remember to memlayer: [pattern/insight]
```

### 3. Plan Complex Tasks
Use sequential-thinking for big features:
```
Use sequential-thinking to plan: [complex task]
```

### 4. Navigate Code Efficientently
Let Serena find relevant code:
```
Use serena to locate: [what you're looking for]
```

### 5. Learn from Execution
ACE learns from every code execution:
```
Use ace to test this: [code snippet]
```

## Configuration

The MCP servers are configured in:
`~/.codex/config.toml`

To update or add more servers:
```bash
codex mcp add <name> -- <command>
codex mcp remove <name>
codex mcp list
```

## Troubleshooting

If MCP tools aren't available:
1. Check server status: `codex mcp list`
2. Restart Codex CLI
3. Check server logs in `~/.codex/logs/`

## Memory Across Sessions

Your memories persist across Codex CLI sessions:
- memlayer: Permanent cross-project memory
- claude-mem: Session to session
- unified-orchestrator: Task and infrastructure memory

This creates a continuously improving development experience where:
1. You never forget useful patterns
2. Documentation is always available
3. Plans are structured and thoughtful
4. Code is executed safely with learning

## Example Session Flow

```
You: Add OAuth login with Google

Codex: I'll help you add Google OAuth. Let me start by planning this properly.

[sequential-thinking] I'll break this down into:
1. Install required packages
2. Configure OAuth credentials
3. Set up Passport.js strategy
4. Create authentication routes
5. Add middleware protection

[context7] Let me get the Passport.js Google OAuth documentation...

[serena] Let me examine your current auth setup...

[ace] I'll implement the OAuth routes step by step...

[memlayer] I'll remember the OAuth configuration pattern...

[unified-orchestrator] Saving task completion: OAuth integration complete
```

Your entire workflow is now seamlessly integrated into Codex CLI!