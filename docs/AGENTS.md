# Agents Reference

## Overview

Claude Reactor provides access to **60+ specialized agents** via the Task tool. Each agent is a focused persona with specific tools and expertise for handling complex, multi-step tasks autonomously.

---

## Agent Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     AGENT INVOCATION FLOW                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  User Request                                                    │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────────┐                                            │
│  │ Claude Code     │                                            │
│  │ (Orchestrator)  │                                            │
│  └─────────────────┘                                            │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────────┐     ┌─────────────────┐                   │
│  │ Task Tool       │────▶│ Select Agent    │                   │
│  │ subagent_type   │     │ by Expertise    │                   │
│  └─────────────────┘     └─────────────────┘                   │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────────────────────────────────────┐               │
│  │              AGENT SUBPROCESS                │               │
│  │  • Full conversation context                 │               │
│  │  • Specialized tool access                   │               │
│  │  • Autonomous multi-step execution           │               │
│  │  • Returns single result message             │               │
│  └─────────────────────────────────────────────┘               │
│       │                                                          │
│       ▼                                                          │
│  Summary returned to user                                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Core Agents

### Explore Agent
**Type**: `Explore`
**Tools**: All tools
**Priority**: High

**Purpose**: Fast codebase exploration for finding files, searching code, and answering questions about the codebase.

**When to Use**:
- Open-ended searches requiring multiple rounds
- Understanding codebase structure
- Finding files by patterns

**Thoroughness Levels**:
- `quick`: Basic searches
- `medium`: Moderate exploration
- `very thorough`: Comprehensive analysis

**Example**:
```python
Task(
    subagent_type="Explore",
    prompt="Find all API endpoints and explain how routing works",
    description="Explore API routing"
)
```

---

### Plan Agent
**Type**: `Plan`
**Tools**: All tools
**Priority**: High

**Purpose**: Software architect agent for designing implementation plans.

**When to Use**:
- Planning feature implementations
- Identifying critical files
- Considering architectural trade-offs

**Returns**:
- Step-by-step implementation plans
- File identification
- Risk assessment

---

### Debugger Agent
**Type**: `debugger`
**Tools**: All tools
**Priority**: Critical

**Purpose**: Debugging specialist for errors, test failures, and unexpected behavior.

**When to Use**:
- Build failures
- Runtime errors
- Unexpected test results
- Any blocking issues

**Process**:
1. Reproduce the issue
2. Isolate the component
3. Form hypothesis
4. Test hypothesis
5. Implement fix
6. Verify fix

---

### Code Reviewer Agent
**Type**: `code-reviewer`
**Tools**: All tools
**Priority**: High

**Purpose**: Expert code review for quality, security, and maintainability.

**When to Use**:
- After writing or modifying code
- Before commits
- Pull request reviews

---

## Language Specialist Agents

### TypeScript Expert
**Type**: `typescript-expert`
**Tools**: All tools

**Expertise**:
- Advanced type system features
- Generics and utility types
- Complex type inference
- Discriminated unions
- Conditional types

**Use Case**: TypeScript development, type system design, JS to TS migration.

---

### JavaScript Pro
**Type**: `javascript-pro`
**Tools**: All tools

**Expertise**:
- ES6+ features
- Async patterns
- Node.js APIs
- Promises and event loops
- Browser/Node compatibility

---

### Python Pro
**Type**: `python-pro`
**Tools**: All tools

**Expertise**:
- Decorators and generators
- Async/await patterns
- Performance optimization
- Design patterns
- Comprehensive testing

---

### Rust Pro
**Type**: `rust-pro`
**Tools**: All tools

**Expertise**:
- Ownership and lifetimes
- Concurrent systems
- Async programming
- Memory-safe abstractions

---

### Go Pro
**Type**: `golang-pro`
**Tools**: All tools

**Expertise**:
- Goroutines and channels
- Interface patterns
- Concurrency optimization
- Error handling idioms

---

### C Pro
**Type**: `c-pro`
**Tools**: All tools

**Expertise**:
- Memory management
- Pointer arithmetic
- System calls
- Embedded systems
- Kernel modules

---

### C++ Pro
**Type**: `cpp-pro`
**Tools**: All tools

**Expertise**:
- Modern C++ features
- RAII and smart pointers
- STL algorithms
- Templates and move semantics
- Performance optimization

---

### SQL Pro
**Type**: `sql-pro`
**Tools**: All tools

**Expertise**:
- Complex queries
- Execution plan optimization
- Normalized schema design
- CTEs and window functions
- Stored procedures

---

## Architecture Agents

### Backend Architect
**Type**: `backend-architect`
**Tools**: All tools

**Purpose**: Design RESTful APIs, microservice boundaries, and database schemas.

**Reviews**:
- System architecture for scalability
- Performance bottlenecks
- API design patterns

---

### Architect Reviewer
**Type**: `architect-reviewer`
**Tools**: All tools

**Purpose**: Review code changes for architectural consistency.

**When to Use**:
- After structural changes
- New service creation
- API modifications

**Ensures**:
- SOLID principles
- Proper layering
- Maintainability

---

### GraphQL Architect
**Type**: `graphql-architect`
**Tools**: All tools

**Purpose**: Design GraphQL schemas, resolvers, and federation.

**Optimizes**:
- Query performance
- N+1 problem solutions
- Subscription implementations

---

## Frontend/Mobile Agents

### Frontend Developer
**Type**: `frontend-developer`
**Tools**: All tools

**Purpose**: Build Next.js applications with React and Tailwind CSS.

**Expertise**:
- SSR/SSG patterns
- App router
- shadcn/ui components
- Modern frontend patterns

---

### Mobile Developer
**Type**: `mobile-developer`
**Tools**: All tools

**Purpose**: React Native and Flutter development.

**Handles**:
- Offline sync
- Push notifications
- App store deployments
- Cross-platform code

---

### UI/UX Designer
**Type**: `ui-ux-designer`
**Tools**: All tools

**Purpose**: User interface and experience design.

**Expertise**:
- Modern design principles
- Accessibility standards
- Design systems
- User research
- Wireframing and prototyping

---

### Accessibility Specialist
**Type**: `accessibility-specialist`
**Tools**: All tools

**Purpose**: Ensure WCAG 2.1 AA/AAA compliance.

**Implements**:
- ARIA attributes
- Keyboard navigation
- Screen reader support

---

## DevOps/Infrastructure Agents

### Cloud Architect
**Type**: `cloud-architect`
**Tools**: All tools

**Purpose**: AWS/Azure/GCP infrastructure design.

**Handles**:
- Terraform IaC
- Auto-scaling
- Multi-region deployments
- Serverless architectures
- Cost optimization

---

### Terraform Specialist
**Type**: `terraform-specialist`
**Tools**: All tools

**Purpose**: Advanced Terraform modules and state management.

**Expertise**:
- Provider configurations
- Workspace management
- Drift detection
- IaC best practices

---

### Deployment Engineer
**Type**: `deployment-engineer`
**Tools**: All tools

**Purpose**: CI/CD pipelines and containerization.

**Handles**:
- GitHub Actions
- Docker
- Kubernetes
- Infrastructure automation

---

### DevOps Troubleshooter
**Type**: `devops-troubleshooter`
**Tools**: All tools

**Purpose**: Debug production issues and deployment failures.

**Masters**:
- Monitoring tools
- Incident response
- Root cause analysis
- Log analysis

---

### Incident Responder
**Type**: `incident-responder`
**Tools**: All tools

**Purpose**: Handle production incidents with urgency.

**When to Use**: IMMEDIATELY when production issues occur.

**Actions**:
- Coordinate debugging
- Implement fixes
- Document post-mortems

---

### Network Engineer
**Type**: `network-engineer`
**Tools**: All tools

**Purpose**: Network connectivity and configuration.

**Handles**:
- Load balancers
- DNS and SSL/TLS
- CDN setup
- Traffic analysis
- Network security

---

## Data/ML Agents

### Data Scientist
**Type**: `data-scientist`
**Tools**: All tools

**Purpose**: SQL queries, BigQuery operations, and data insights.

**Use Case**: Data analysis tasks and query optimization.

---

### Data Engineer
**Type**: `data-engineer`
**Tools**: All tools

**Purpose**: ETL pipelines and data warehouses.

**Implements**:
- Spark jobs
- Airflow DAGs
- Kafka streams
- Streaming architectures

---

### ML Engineer
**Type**: `ml-engineer`
**Tools**: All tools

**Purpose**: ML pipelines and model serving.

**Handles**:
- TensorFlow/PyTorch deployment
- A/B testing
- Model monitoring
- Feature engineering

---

### MLOps Engineer
**Type**: `mlops-engineer`
**Tools**: All tools

**Purpose**: ML infrastructure and experiment tracking.

**Implements**:
- MLflow, Kubeflow
- Automated retraining
- Data versioning
- Reproducibility

---

## Security Agents

### Security Auditor
**Type**: `security-auditor`
**Tools**: All tools

**Purpose**: Vulnerability review and secure authentication.

**Ensures**:
- OWASP compliance
- JWT/OAuth2 implementation
- CORS, CSP, encryption
- Auth flow security

---

### Error Detective
**Type**: `error-detective`
**Tools**: All tools

**Purpose**: Search logs for error patterns and anomalies.

**Capabilities**:
- Stack trace analysis
- Cross-system correlation
- Root cause identification

---

## Blockchain/Crypto Agents

### Blockchain Developer
**Type**: `blockchain-developer`
**Tools**: All tools

**Purpose**: Smart contracts and Web3 applications.

**Expertise**:
- Solidity
- Security auditing
- Gas optimization
- DeFi protocols

---

### DeFi Strategist
**Type**: `defi-strategist`
**Tools**: All tools

**Purpose**: Yield strategies and liquidity provision.

**Use Case**: Yield farming, liquidity mining, protocol integration.

---

### Crypto Trader
**Type**: `crypto-trader`
**Tools**: All tools

**Purpose**: Cryptocurrency trading systems.

**Implements**:
- Trading strategies
- Exchange API integration
- Portfolio management

---

### Crypto Analyst
**Type**: `crypto-analyst`
**Tools**: All tools

**Purpose**: Market analysis and on-chain analytics.

**Provides**:
- Token analysis
- Trading signals
- Sentiment analysis

---

### Crypto Risk Manager
**Type**: `crypto-risk-manager`
**Tools**: All tools

**Purpose**: Risk management for crypto trading and DeFi.

**Implements**:
- Position sizing
- Risk monitoring
- Portfolio protection

---

### Arbitrage Bot
**Type**: `arbitrage-bot`
**Tools**: All tools

**Purpose**: Identify arbitrage opportunities.

**Handles**:
- Cross-exchange trading
- DEX/CEX arbitrage
- Bot development

---

### Quant Analyst
**Type**: `quant-analyst`
**Tools**: All tools

**Purpose**: Financial models and trading strategies.

**Implements**:
- Backtesting
- Risk metrics
- Portfolio optimization
- Statistical arbitrage

---

### Risk Manager
**Type**: `risk-manager`
**Tools**: All tools

**Purpose**: Portfolio risk and position limits.

**Creates**:
- Hedging strategies
- Expectancy calculations
- Stop-loss implementations

---

## AI/Integration Agents

### AI Engineer
**Type**: `ai-engineer`
**Tools**: All tools

**Purpose**: LLM applications and RAG systems.

**Implements**:
- Vector search
- Agent orchestration
- AI API integrations
- Prompt pipelines

---

### Prompt Engineer
**Type**: `prompt-engineer`
**Tools**: All tools

**Purpose**: Optimize prompts for LLMs and AI systems.

**Expertise**:
- Prompt patterns and techniques
- System prompt crafting
- Agent performance improvement

---

## Testing/Quality Agents

### Test Automator
**Type**: `test-automator`
**Tools**: All tools

**Purpose**: Comprehensive test suites.

**Creates**:
- Unit, integration, e2e tests
- CI pipeline setup
- Mocking strategies
- Test data management

---

### Performance Engineer
**Type**: `performance-engineer`
**Tools**: All tools

**Purpose**: Application profiling and optimization.

**Handles**:
- Bottleneck identification
- Caching strategies
- Load testing
- CDN setup
- Query optimization

---

### Database Optimizer
**Type**: `database-optimizer`
**Tools**: All tools

**Purpose**: SQL query and index optimization.

**Solves**:
- N+1 problems
- Slow queries
- Schema optimization
- Caching implementation

---

### Database Admin
**Type**: `database-admin`
**Tools**: All tools

**Purpose**: Database operations and maintenance.

**Handles**:
- Backups and replication
- User permissions
- Disaster recovery
- Monitoring

---

## Documentation/Content Agents

### API Documenter
**Type**: `api-documenter`
**Tools**: All tools

**Purpose**: OpenAPI/Swagger specs and developer docs.

**Creates**:
- SDK generation
- Versioning strategy
- Interactive documentation
- Usage examples

---

### Content Marketer
**Type**: `content-marketer`
**Tools**: All tools

**Purpose**: Blog posts, social media, and newsletters.

**Optimizes**:
- SEO
- Content calendars
- Engagement

---

## Business Agents

### Business Analyst
**Type**: `business-analyst`
**Tools**: All tools

**Purpose**: Metrics analysis and KPI tracking.

**Creates**:
- Dashboards
- Revenue models
- Growth projections
- Investor updates

---

### Sales Automator
**Type**: `sales-automator`
**Tools**: All tools

**Purpose**: Cold emails, proposals, and outreach.

**Creates**:
- Pricing pages
- Case studies
- Sales scripts
- Follow-up templates

---

### Customer Support
**Type**: `customer-support`
**Tools**: All tools

**Purpose**: Support tickets and FAQ responses.

**Creates**:
- Help documentation
- Troubleshooting guides
- Canned responses

---

## Specialized Agents

### Legacy Modernizer
**Type**: `legacy-modernizer`
**Tools**: All tools

**Purpose**: Refactor legacy code and migrate frameworks.

**Handles**:
- Technical debt
- Dependency updates
- Backward compatibility
- Gradual modernization

---

### DX Optimizer
**Type**: `dx-optimizer`
**Tools**: All tools

**Purpose**: Developer Experience improvement.

**When to Use**:
- New project setup
- After team feedback
- Development friction noticed

---

### Context Manager
**Type**: `context-manager`
**Tools**: All tools

**Purpose**: Manage context across agents and sessions.

**MUST USE**: For projects exceeding 10k tokens.

---

### Search Specialist
**Type**: `search-specialist`
**Tools**: All tools

**Purpose**: Expert web research and synthesis.

**Capabilities**:
- Advanced search operators
- Multi-source verification
- Competitive analysis
- Fact-checking

---

### Game Developer
**Type**: `game-developer`
**Tools**: All tools

**Purpose**: Unity, Unreal, or web game development.

**Implements**:
- Game mechanics
- Physics
- AI
- Optimization

---

## CMS/Platform Agents

### Drupal Developer
**Type**: `drupal-developer`
**Tools**: All tools

**Purpose**: Drupal applications and customization.

**Expertise**:
- Custom modules and themes
- Content modeling
- Performance optimization

---

### Directus Developer
**Type**: `directus-developer`
**Tools**: All tools

**Purpose**: Directus extensions and API integrations.

**Expertise**:
- Data models
- Permissions and workflows
- Custom extensions

---

### Payment Integration
**Type**: `payment-integration`
**Tools**: All tools

**Purpose**: Stripe, PayPal integration.

**Handles**:
- Checkout flows
- Subscriptions
- Webhooks
- PCI compliance

---

## Feature Development Agents

### Code Architect
**Type**: `feature-dev:code-architect`
**Tools**: Glob, Grep, LS, Read, NotebookRead, WebFetch, TodoWrite, WebSearch, KillShell, BashOutput

**Purpose**: Design feature architectures by analyzing existing patterns.

**Provides**:
- Implementation blueprints
- Component designs
- Data flows
- Build sequences

---

### Code Explorer
**Type**: `feature-dev:code-explorer`
**Tools**: Glob, Grep, LS, Read, NotebookRead, WebFetch, TodoWrite, WebSearch, KillShell, BashOutput

**Purpose**: Deep codebase analysis.

**Maps**:
- Execution paths
- Architecture layers
- Patterns and abstractions
- Dependencies

---

### Code Reviewer (Feature Dev)
**Type**: `feature-dev:code-reviewer`
**Tools**: Glob, Grep, LS, Read, NotebookRead, WebFetch, TodoWrite, WebSearch, KillShell, BashOutput

**Purpose**: Review code with confidence-based filtering.

**Reports**: Only high-priority issues that truly matter.

---

## Hardware/IoT Agents

### ESPHome Expert
**Type**: `esphome-expert`
**Tools**: All tools

**Purpose**: ESPHome configuration and ESP32/ESP8266 development.

**Expertise**:
- YAML configuration
- Sensor integration
- GPIO/I2C/UART setup
- Home Assistant integration
- Custom components

---

## AI Model Proxy Agents

### LlamaCPP Proxy
**Type**: `llamacpp-proxy`
**Tools**: Read, WebFetch, Bash, Glob

**Purpose**: Act as LlamaCPP API agent.

**Trigger**: Mentions of @llama, llama, llamacpp.

**Reads**: `llamacpp.env` for configuration.

---

## Claude-Specific Agents

### Claude Code Guide
**Type**: `claude-code-guide`
**Tools**: Glob, Grep, Read, WebFetch, WebSearch

**Purpose**: Answer questions about Claude Code features.

**Topics**:
- Hooks, slash commands
- MCP servers
- IDE integrations
- Keyboard shortcuts
- Claude Agent SDK

---

### Hookify Analyzer
**Type**: `hookify:conversation-analyzer`
**Tools**: Read, Grep

**Purpose**: Analyze conversations to find behaviors worth preventing with hooks.

**Trigger**: `/hookify` command without arguments.

---

## Agent Usage Best Practices

### Selecting the Right Agent

1. **Match expertise to task**: Use language-specific agents for that language
2. **Use proactive agents**: Many agents should be used without user asking
3. **Parallel execution**: Launch multiple independent agents simultaneously
4. **Background execution**: Use `run_in_background: true` for long tasks

### Example Invocations

```python
# Single agent
Task(
    subagent_type="typescript-expert",
    prompt="Refactor this class to use generics",
    description="Refactor to generics"
)

# Parallel agents (single message, multiple calls)
Task(subagent_type="security-auditor", ...)
Task(subagent_type="performance-engineer", ...)
Task(subagent_type="code-reviewer", ...)

# Background agent
Task(
    subagent_type="test-automator",
    prompt="Generate comprehensive tests",
    run_in_background=True,
    description="Generate tests"
)

# Resume previous agent
Task(
    resume="agent-id-from-previous",
    prompt="Continue with the next step"
)
```

---

## Agent Statistics

| Category | Count | Key Agents |
|----------|-------|------------|
| Core | 4 | Explore, Plan, Debugger, Code Reviewer |
| Language | 8 | TypeScript, Python, Rust, Go, C, C++, SQL, JS |
| Architecture | 3 | Backend, Architect Reviewer, GraphQL |
| Frontend/Mobile | 4 | Frontend Dev, Mobile Dev, UI/UX, A11y |
| DevOps | 6 | Cloud, Terraform, Deploy, Network, Incident |
| Data/ML | 4 | Data Scientist, Data Eng, ML Eng, MLOps |
| Security | 2 | Security Auditor, Error Detective |
| Blockchain | 7 | Blockchain Dev, DeFi, Trader, Analyst, Risk |
| AI/Integration | 2 | AI Engineer, Prompt Engineer |
| Testing | 4 | Test Automator, Perf, DB Optimizer, DBA |
| Documentation | 2 | API Documenter, Content Marketer |
| Business | 3 | Business Analyst, Sales, Support |
| Feature Dev | 3 | Architect, Explorer, Reviewer |
| Specialized | 6 | Legacy, DX, Context, Search, Game, Payment |
| **Total** | **~60** | |

