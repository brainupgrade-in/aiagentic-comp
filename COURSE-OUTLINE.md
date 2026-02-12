# Agentic AI: Comprehensive Course

**Duration:** 5 Days | **Trainer:** Rajesh Gheware

---

## Participant Requirements

### Technical Prerequisites

- Basic Python programming knowledge
- Basic understanding of APIs and REST concepts
- Familiarity with command line / terminal
- Familiarity with AI coding assistants (helpful but not required)

### Required Accounts & Tools

- GitHub account (github.com)
- Google account (for Google Classroom access)

### Hardware Requirements

- Stable internet connection
- Access to classroom.google.com and brainupgrade.in URLs

---

## Course Overview

A comprehensive program covering the full spectrum of Agentic AI development -- from foundational concepts to production deployment with enterprise-grade observability. This course focuses on practical implementation using LangChain ecosystem, AI coding agents, Model Context Protocol (MCP), and monitoring with OpenTelemetry.

### Learning Outcomes

- Understand agentic AI fundamentals and architectural patterns
- Use AI coding assistants and vibe coding workflows from Day 1
- Build AI agents using LangChain and its ecosystem
- Develop production-ready agentic applications
- Implement observability with OpenTelemetry and LangFuse
- Monitor and debug agents with LangFuse
- Build production-grade FastAPI endpoints with health probes, secrets, and structured logging
- Understand Model Context Protocol (MCP) architecture and enterprise use cases
- Implement AI safety guardrails: prompt injection defense, output validation, and red team testing
- Complete a capstone project integrating all course concepts
- Leverage agentic IDEs for AI-assisted development

### Target Audience

- Software engineers interested in AI/ML
- AI developers and data scientists
- DevOps engineers deploying AI applications
- Technology professionals upskilling in AI development

---

## Tools & Licensing

### AI & Development

- **Ollama + llama3.2** - Local LLM (MIT / Meta, Free)
- **LangChain / LangGraph** - Agent framework (MIT)
- **ChromaDB** - Vector database (Apache 2.0)
- **FastAPI** - API framework (MIT)

### AI Developer Tools

- **MCP** - Model Context Protocol ecosystem (MIT)
- **OpenCode** - AI-assisted coding in terminal

### Observability

- **OpenTelemetry** - Observability framework (Apache 2.0)
- **LangFuse** - AI tracing and observability (MIT, Self-hosted free)

---

## Lab Environment

### Browser-Based Sandbox (brainupgrade.in)

Each participant will be provided with a dedicated lab environment:

- **Browser-Based IDE** - No local setup required; develop directly in browser
- **Pre-configured Environment** - Python and all tools pre-installed
- **Personal Sandbox** - Isolated environment for each participant
- **Public URL** - Each deployed app gets an internet-accessible URL for testing
- **Persistent Storage** - Work is saved across sessions

### What You Can Do

- Develop LangChain/LangGraph applications
- Build and use AI coding agents and MCP servers
- Configure LangFuse SDK for AI observability
- Build and test FastAPI applications
- Test and troubleshoot AI applications end-to-end

### Lab Access

- Provided on Day 1 of the course
- Valid for duration of the training
- Access via any modern web browser (Chrome, Firefox, Edge)

---

## Day 1: Foundations & AI-Assisted Development

### Session 1: Introduction to Agentic AI

**What is Agentic AI?**
- Definition and key characteristics
- Evolution: Rule-based -> ML -> LLMs -> Agents
- The "chaining" capability and autonomous decision-making

**Agents vs Traditional AI**
- LLM vs Agent: Reasoning loops, action loops, autonomy
- Agents vs Chatbots vs RAG systems
- Core capabilities: Autonomy, Problem Solving, Adaptability

**Architectural Patterns**
- Single Agent architecture
- Multi-Agent systems
- Supervisor/Worker pattern

**Agent Components**
- LLM (Brain) - Core reasoning and language understanding
- Memory (State) - Maintains context and conversation history
- Tools (Actions) - External capabilities (APIs, databases, web)
- Planning (Orchestration) - Task decomposition and execution strategy

### Session 2: AI Coding Assistants & Vibe Coding

**The Agent Loop Model**
- Five phases: Plan, Code, Test, Reflect, Iterate
- Context management and token budgeting
- Tool registries for file operations, search, and testing

**Vibe Coding & Prompt Engineering**
- Natural language to code workflows
- Structured prompt templates for code generation
- Iterative refinement patterns

**AI Coding Agent Comparison**
- OpenCode, Claude Code, GitHub Copilot, Cursor
- Feature scoring: context window, tool use, autonomy
- Choosing the right tool for the task

### Session 3: Reasoning, Planning & Tool Use

**Reasoning Architectures**
- ReAct pattern (Reasoning + Acting)
- Chain-of-Thought (CoT)
- Tree-of-Thought (ToT)
- Reflection patterns

**Tool Calling**
- Why tools matter in agentic AI
- API calling patterns
- Custom tool development

**Memory Systems**
- Short-term memory (conversation context)
- Long-term memory (persistent storage)
- Episodic memory (experience-based)

### Session 4: Hands-on Labs

**Lab 1: Environment Setup & Meet Your LLM**
- Set up LangChain environment
- Configure local LLM with Ollama

**Lab 2: Vibe Coding Workflows**
- Practice AI-assisted coding patterns
- Build simple programs using natural language descriptions

**Lab 3: Reasoning Patterns**
- Implement ReAct and Chain-of-Thought
- Test reasoning with tool use

---

## Day 2: LangChain, RAG & Agents

### Session 4: LangChain Fundamentals

**LangChain Overview**
- Why LangChain? (70M+ monthly downloads, Production-ready 1.0)
- Core philosophy and design principles

**Core Components**
- Foundation Layer - Models (LLMs), Prompts (Templates), Chains (Workflows)
- Intelligence Layer - Memory (State), Tools (Actions), Agents (Reasoning)
- Data Layer - Retrievers (RAG), Document Loaders, Vector Stores

**Working with Models & Prompts**
- Model integrations with Groq API (cloud, free)
- ChatPromptTemplate and message types
- LCEL (LangChain Expression Language)

**Chains & Output Parsing**
- Chain composition with pipe syntax
- StrOutputParser, JSON parsing
- Pydantic output parsers

### Session 5: Building RAG Applications

**Retrieval-Augmented Generation**
- Why RAG matters for agents
- RAG architecture overview
- Embedding models

**Vector Stores & ChromaDB**
- ChromaDB architecture and setup
- Collections and metadata
- Similarity search strategies
- Document ingestion pipeline

**Building RAG Pipelines**
- Query processing
- Context retrieval
- Response generation with citations

### Session 6: LangChain Agents & Memory

**Agent Types**
- ReAct agents
- Function-calling agents
- Custom agents

**Tool Integration**
- Built-in tools
- Custom tool creation
- Multi-tool orchestration

**Memory & Conversation Management**
- ConversationBufferMemory
- ConversationSummaryMemory
- Session management and persistence

### Session 4 Labs

**Lab 4: LangChain Fundamentals**
- Build chains with LCEL
- Create prompt templates
- Parse structured outputs

**Lab 5: RAG-Powered Q&A Agent**
- Build vector store from documents
- Create retrieval chain with memory
- Add conversational context

---

## Day 3: LangGraph & Multi-Agent Systems

### Session 7: LangGraph Stateful Workflows

**StateGraph - Stateful Workflows**
- StateGraph - Define and manage workflow state
- Nodes - Processing steps in the workflow
- Edges - Connections between nodes (including cycles)
- Checkpointing - Save and resume workflow state
- Human-in-Loop - Pause for human approval/input

### Session 8: Advanced LangGraph Workflows

**Complex Workflow Patterns**
- Multi-branch state graphs
- Parallel node execution
- Error handling and retry logic
- Conditional routing strategies

**State Management Deep Dive**
- TypedDict state definitions
- State reducers and annotations
- Checkpoint persistence backends
- State recovery and resumption

**Human-in-the-Loop Patterns**
- Interrupt points and approval gates
- User input collection mid-workflow
- Timeout and escalation handling

### Session 9: Multi-Agent Systems

**Multi-Agent Architectures**
- Supervisor/Worker pattern implementation
- Peer-to-peer agent communication
- Agent handoffs and delegation

**Agent Collaboration Patterns**
- Task decomposition and distribution
- Result aggregation strategies
- Conflict resolution between agents

**Production Agent Patterns**
- Agent specialization and roles
- Load balancing across agents
- Fallback and redundancy

### Session 3 Labs

**Lab 6: LangGraph Workflow**
- Create multi-step stateful workflow
- Implement conditional branching
- Add human approval checkpoint

**Lab 7: Multi-Agent System**
- Create supervisor agent with specialized workers
- Implement task delegation logic
- Test agent collaboration

---

## Day 4: Observability & Production

### Session 10: Observability Fundamentals

**Three Pillars of Observability**
- Metrics - Quantitative measurements over time
- Logs - Discrete events and messages
- Traces - Request flow across services

**OpenTelemetry Overview**
- Vendor-neutral observability framework
- Traces, metrics, logs collection
- Instrumentation: auto vs manual
- OTLP (OpenTelemetry Protocol)

**Metric Types & Structured Logging**
- Counter, Gauge, Histogram, Summary
- JSON structured logging with trace_id correlation
- AI-specific log fields

**Instrumenting Python Applications**
- opentelemetry-python SDK
- Auto-instrumentation for FastAPI
- Custom spans and attributes
- OTel Collector deployment and configuration

### Session 11: LangFuse Observability

**LangFuse Overview**
- Open-source LLM observability
- Traces for LLM calls
- Prompt management and versioning
- Cost tracking and analytics

**Instrumenting LangChain with LangFuse**
- LangFuse callback handler
- Trace hierarchy (traces, spans, generations)
- User feedback collection
- A/B testing prompts

**Debugging AI Agents**
- Tracing agent reasoning steps
- Tool call visibility
- Token usage per step
- Latency breakdown and cost analysis

### Session 12: Production Development & Deployment

**FastAPI Integration**
- Building REST APIs for agents
- Pydantic models for request/response validation
- Streaming responses with SSE
- Error handling and HTTP status codes

**Production Readiness**
- Health checks and readiness probes
- Python async HealthChecker (readiness, liveness, startup)
- Secrets management (python-dotenv, environment variables)
- Structured JSON logging with AI-specific fields
- Production checklist (health, resources, secrets, observability, alerting, backup)
- Deployment order and resource recommendations

**Testing AI Applications**
- Unit testing agent components
- Mocking LLM responses
- Integration testing workflows

### Session 4 Labs

**Lab 8: Observability Stack**
- Configure OTel TracerProvider and exporters
- Implement structured logging
- Set up OTel Collector pipeline

**Lab 9: LangFuse Integration**
- Instrument LangChain application
- Analyze traces and costs

**Lab 10: Production API**
- Build FastAPI endpoint for agent
- Add health probes and secrets management
- Implement structured logging

---

## Day 5: MCP, Safety & Capstone

### Session 13: Model Context Protocol (MCP)

**MCP Architecture**
- The N×M integration problem and how MCP solves it (N+M)
- Host, Client, Server roles and JSON-RPC 2.0 protocol
- Three primitives: Tools, Resources, Prompts
- Transport essentials: stdio vs SSE

**Enterprise MCP Use Cases**
- Enterprise Data Access: Postgres, Snowflake, BigQuery via natural language
- Developer Productivity: GitHub, Jira, CI/CD integration (25% gains)
- Knowledge & Customer Ops: Confluence, Salesforce, Zendesk unified
- Multi-tool agent pattern and ROI analysis

**Consuming MCP in Applications**
- MCP ecosystem: 1,000+ servers across categories
- Client configuration: Claude Desktop, Claude Code JSON configs
- Multi-server configuration and role-based assignment
- Bridging MCP with LangChain (`langchain-mcp-adapters`)
- Enterprise security: input validation, RBAC, audit logging

### Session 14: AI Safety & Guardrails

**Prompt Injection Defense**
- Direct vs indirect prompt injection
- Detection patterns and classification
- Keyword scanning and structural analysis

**Output Validation & PII Protection**
- Schema validation for LLM outputs
- PII detection (email, phone, SSN, credit card)
- Content filtering and toxicity checks

**Jailbreak Resistance**
- Common jailbreak techniques (DAN, roleplay, encoding)
- Defense layers and system prompt hardening
- Multi-signal scoring for jailbreak detection

**Input Sanitization & Guardrails**
- Sanitization pipeline: length, encoding, content policy
- Pre-guard and post-guard architecture
- Topic restriction and format enforcement

**Safety Monitoring & Red Teaming**
- Safety metrics (counters, gauges, thresholds)
- Red team methodology and test matrices
- Defense scoring and production readiness

### Session 15: Capstone Project (2 Time Slots)

**Capstone: Production AI Agent System**

Build a complete, observable AI agent integrating all course concepts:
1. Architecture design (component mapping, data flows)
2. MCP client configuration and enterprise workflows (from Session 13)
3. AI safety guardrails (from Session 14)
4. FastAPI endpoint (from Session 12)
5. LangFuse instrumentation (from Session 11)
6. Health probes and monitoring (from Session 12)
7. Production deployment configuration
8. Testing and validation
9. Final integration challenge

**Demo & Presentations**
- Present capstone to the group
- Discuss architectural decisions
- Peer review and feedback

**Course Wrap-up**
- Key takeaways across 5 days
- Learning path recommendations
- Resources and community
- Feedback collection

---

Copyright (c) 2026 Gheware UniGPS Solutions LLP. All Rights Reserved.
