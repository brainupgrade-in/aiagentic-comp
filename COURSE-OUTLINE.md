# Agentic AI: Comprehensive Course

**Duration:** 5 Days | **Trainer:** Rajesh Gheware

---

## Participant Requirements

### Technical Prerequisites

- Basic Python programming knowledge
- Basic understanding of APIs and REST concepts
- Familiarity with command line / terminal
- Basic Docker knowledge (helpful but not required)

### Required Accounts & Tools

- GitHub account (github.com)
- Google account (for Google Classroom access)

### Hardware Requirements

- Stable internet connection
- Access to classroom.google.com and brainupgrade.in URLs

---

## Course Overview

A comprehensive program covering the full spectrum of Agentic AI development -- from foundational concepts to production deployment with enterprise-grade observability. This course focuses on practical implementation using LangChain ecosystem, containerization with Docker/Kubernetes, and monitoring with OpenTelemetry.

### Learning Outcomes

- Understand agentic AI fundamentals and architectural patterns
- Build AI agents using LangChain and its ecosystem
- Develop production-ready agentic applications
- Deploy agents using Docker and Kubernetes
- Implement observability with OpenTelemetry, Prometheus, and Grafana
- Monitor and debug agents with LangFuse
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

### Infrastructure

- **Docker** - Containerization (Apache 2.0)
- **Kubernetes** - Container orchestration (Apache 2.0)

### Observability

- **Prometheus** - Metrics collection (Apache 2.0)
- **Grafana** - Visualization (AGPL-3.0, Free tier)
- **OpenTelemetry** - Observability framework (Apache 2.0)
- **LangFuse** - AI tracing (MIT, Self-hosted free)

---

## Lab Environment

### Browser-Based Sandbox (brainupgrade.in)

Each participant will be provided with a dedicated lab environment:

- **Browser-Based IDE** - No local setup required; develop directly in browser
- **Pre-configured Environment** - Python, Docker, Kubernetes, and all tools pre-installed
- **Personal Sandbox** - Isolated environment for each participant
- **Public URL** - Each deployed app gets an internet-accessible URL for testing
- **Persistent Storage** - Work is saved across sessions

### What You Can Do

- Develop LangChain/LangGraph applications
- Build and run Docker containers
- Deploy to Kubernetes cluster
- Configure Prometheus, Grafana, LangFuse
- Test and troubleshoot AI applications end-to-end

### Lab Access

- Provided on Day 1 of the course
- Valid for duration of the training
- Access via any modern web browser (Chrome, Firefox, Edge)

---

## Day 1: Agentic AI Foundations & LangChain

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

### Session 2: Reasoning, Planning & Tool Use

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

### Session 3: LangChain Fundamentals

**LangChain Overview**
- Why LangChain? (70M+ monthly downloads, Production-ready 1.0)
- Core philosophy and design principles

**Core Components**
- Foundation Layer - Models (LLMs), Prompts (Templates), Chains (Workflows)
- Intelligence Layer - Memory (State), Tools (Actions), Agents (Reasoning)
- Data Layer - Retrievers (RAG), Document Loaders, Vector Stores

**Working with Models & Prompts**
- Model integrations with Ollama (local, free)
- ChatPromptTemplate and message types
- LCEL (LangChain Expression Language)

**Chains & Output Parsing**
- Chain composition with pipe syntax
- StrOutputParser, JSON parsing
- Pydantic output parsers

### Session 4: Hands-on Labs

**Lab 1: Environment Setup & First Chain**
- Set up LangChain environment
- Configure local LLM with Ollama
- Create prompt templates
- Build simple chains with LCEL

**Lab 2: Document Processing**
- Load documents (PDF, web pages)
- Implement text splitting
- Parse structured outputs with Pydantic

**Lab 3: Simple Agent with Tools**
- Create custom tools with @tool decorator
- Build calculator + search agent
- Test reasoning patterns

---

## Day 2: RAG Applications & LangChain Ecosystem

### Session 1: Building RAG Applications

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

### Session 2: LangChain Agents & Memory

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

**Lab 4: RAG-Powered Q&A Agent**
- Build vector store from documents
- Create retrieval chain with memory
- Add conversational context

### Session 3: LangChain Ecosystem

**LangGraph - Stateful Workflows**
- StateGraph - Define and manage workflow state
- Nodes - Processing steps in the workflow
- Edges - Connections between nodes (including cycles)
- Checkpointing - Save and resume workflow state
- Human-in-Loop - Pause for human approval/input

### Session 4: Hands-on Labs

**Lab 5: LangGraph Workflow**
- Create multi-step stateful workflow
- Implement conditional branching
- Add human approval checkpoint

---

## Day 3: Advanced Agents & Production Development

### Session 1: Advanced LangGraph Workflows

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

### Session 2: Multi-Agent Systems

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

### Session 3: Production Application Development

**FastAPI Integration**
- Building REST APIs for agents
- Async request handling
- Streaming responses
- Error handling and validation

**Testing AI Applications**
- Unit testing agent components
- Integration testing workflows
- Mocking LLM responses
- Test fixtures and factories

**Performance Optimization**
- Caching strategies for embeddings
- Connection pooling
- Async operations and concurrency

### Session 4: Hands-on Labs

**Lab 6: Advanced LangGraph Application**
- Build multi-branch workflow with human approval
- Implement state persistence
- Add error handling and retries

**Lab 7: Multi-Agent System**
- Create supervisor agent with specialized workers
- Implement task delegation logic
- Test agent collaboration

**Lab 8: Production API**
- Build FastAPI endpoint for agent
- Add streaming responses
- Implement health checks and monitoring endpoints

---

## Day 4: Docker & Kubernetes Deployment

### Session 1: Docker for AI Applications

**Docker Fundamentals**
- Containers vs Virtual Machines
- Docker architecture (daemon, client, registry)
- Images, containers, and layers

**Dockerfile for LangChain**
- FROM, RUN, COPY, WORKDIR, CMD, ENTRYPOINT
- Multi-stage builds for smaller images
- Base images for ML (python:3.11-slim)
- Layer optimization for pip packages

**AI-Specific Patterns**
- Managing large dependencies
- Model caching strategies
- Non-root user for security
- Health checks

**Lab 9: Containerize AI Application**
- Write production Dockerfile
- Build and test container
- Security scanning with Trivy

### Session 2: Kubernetes Fundamentals

**Kubernetes Overview**
- Why Kubernetes for AI workloads
- Architecture: Control plane, nodes, pods
- kubectl CLI basics

**Core Objects**
- Pods - Smallest deployable unit
- Deployments - Declarative updates
- Services - Network abstraction
- ConfigMaps & Secrets - Configuration management

**AI Workload Considerations**
- Memory requirements for LLMs
- Resource requests and limits
- Model loading time and readiness probes

### Session 3: Deploying AI Stack on Kubernetes

**Deployment Strategies**
- Rolling updates
- Horizontal Pod Autoscaler (HPA)
- Service types (ClusterIP, NodePort, LoadBalancer)
- Ingress for HTTP routing

**Configuration & Storage**
- ConfigMaps for app configuration
- Secrets for API keys
- PersistentVolumes and PersistentVolumeClaims
- StatefulSets for databases

**Deploying ChromaDB on Kubernetes**
- StatefulSet configuration
- Persistent storage for embeddings
- Service for internal access

**Lab 10: Deploy Complete AI Stack**
- Deploy LangChain API with Deployment
- Deploy ChromaDB with persistence
- Configure Ingress and secrets

### Session 4: Kubernetes Operations

**Debugging & Troubleshooting**
- kubectl logs, describe, exec
- Pod events and status
- Common issues and fixes

**Scaling & High Availability**
- Horizontal Pod Autoscaler configuration
- Pod Disruption Budgets
- Multi-replica deployments

**Lab 11: Scaling & Operations**
- Configure HPA for API service
- Test auto-scaling under load
- Practice debugging scenarios

---

## Day 5: Observability & Production Operations

### Session 1: Observability Fundamentals

**Three Pillars of Observability**
- Metrics - Quantitative measurements over time
- Logs - Discrete events and messages
- Traces - Request flow across services

**OpenTelemetry Overview**
- Vendor-neutral observability framework
- Traces, metrics, logs collection
- Instrumentation: auto vs manual
- OTLP (OpenTelemetry Protocol)

**Instrumenting Python Applications**
- opentelemetry-python SDK
- Auto-instrumentation for FastAPI
- Custom spans and attributes

### Session 2: Metrics with Prometheus & Grafana

**Prometheus Architecture**
- Pull-based metrics collection
- PromQL query language
- Alert rules and Alertmanager

**Key Metrics for AI Applications**
- Request latency and throughput
- Token usage and costs
- Model inference time
- Memory and CPU utilization
- Queue depth and processing time

**Grafana Dashboards**
- Data sources and panels
- Dashboard design principles
- Alerts and notifications

**Lab 12: Prometheus & Grafana Setup**
- Deploy Prometheus on Kubernetes
- Configure scrape targets
- Create Grafana dashboard for AI metrics

### Session 3: AI-Specific Observability with LangFuse

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
- Latency breakdown

**Lab 13: LangFuse Integration**
- Set up LangFuse (self-hosted)
- Instrument LangChain application
- Analyze traces and costs
- Debug agent execution

### Session 4: Capstone & Production Readiness

**Capstone Project: Production AI Agent**

Deploy a complete, observable AI agent:
1. LangChain agent with RAG
2. Containerized with Docker
3. Deployed on Kubernetes
4. Full observability stack (OTel + Prometheus + Grafana + LangFuse)

**Production Checklist**
- Health checks and readiness probes
- Resource limits and autoscaling
- Secrets management
- Logging and monitoring
- Alerting configuration
- Backup and recovery

**Lab Time & Presentations**
- Complete capstone deployment
- Demo observability dashboards
- Q&A and feedback

**Course Wrap-up**
- Key takeaways
- Learning path recommendations
- Resources and community

---

Copyright (c) 2026 Gheware UniGPS Solutions LLP. All Rights Reserved.
