# Instructor Guide

**Course:** Agentic AI: Comprehensive Course
**Trainer:** Rajesh Gheware
**Client:** Oracle
**Duration:** 5 Days (8 hours/day, ~40 hours total)

---

## Daily Schedule Template

| Time | Block | Duration |
|------|-------|----------|
| 09:00 - 09:15 | Day kickoff / recap | 15 min |
| 09:15 - 10:30 | Session A (slides) | 75 min |
| 10:30 - 10:45 | Break | 15 min |
| 10:45 - 12:00 | Session B (slides) | 75 min |
| 12:00 - 13:00 | Lunch | 60 min |
| 13:00 - 14:15 | Session C (slides) | 75 min |
| 14:15 - 14:30 | Break | 15 min |
| 14:30 - 16:30 | Session D (hands-on labs) | 120 min |
| 16:30 - 17:00 | Wrap-up / Q&A | 30 min |

---

## Session-to-Day Mapping

### Day 1: Agentic AI Foundations & LangChain

| Slot | Session | Slides | Labs | Setup Script |
|------|---------|--------|------|-------------|
| A | Session 1: Introduction to Agentic AI | `session1-introduction-to-agentic-ai.html` | `session-1/` (6 labs) | `day1-setup.sh` |
| B | Session 2: Reasoning, Planning & Tool Use | `session2-reasoning-planning-tool-use.html` | `session-2/` (7 labs) | - |
| C | Session 3: LangChain Fundamentals | `session3-langchain-fundamentals.html` | `session-3/` (8 labs) | - |
| D | Labs for Sessions 1-3 | - | All above | - |

**Day 1 Setup:** Run `bash scripts/day1-setup.sh` at start (installs Ollama + llama3.2:1b).
**Day 1 Cleanup:** Run `bash scripts/day1-cleanup.sh` at end (frees ~2 GB).

**Teaching Notes:**
- Session 1 sets the foundation -- ensure participants understand the difference between LLMs and agents
- Ollama is used for Day 1 demos only; from Day 2 onwards, switch to Groq API
- Have participants create Groq API keys during a break: https://console.groq.com
- Lab time covers sessions 1-3 labs; prioritize session-3 labs (LangChain fundamentals)

### Day 2: RAG, Agents & LangGraph

| Slot | Session | Slides | Labs | Setup Script |
|------|---------|--------|------|-------------|
| A | Session 4: Building RAG Applications | `session4-building-rag-applications.html` | `session-4/` (8 labs) | `day2-setup.sh` |
| B | Session 5: LangChain Agents & Memory | `session5-langchain-agents-memory.html` | `session-5/` (8 labs) | - |
| C | Session 6: LangGraph Stateful Workflows | `session6-langgraph-stateful-workflows.html` | `session-6/` (8 labs) | - |
| D | Labs for Sessions 4-6 | - | All above | - |

**Day 2 Setup:** Run `bash scripts/day2-setup.sh` (verifies Groq API key and packages).
**Day 2 Cleanup:** Run `bash scripts/day2-cleanup.sh` at end.

**Teaching Notes:**
- Verify all participants have working Groq API keys before starting
- Session 4 (RAG) is foundational for the rest of the course -- ensure all participants grasp retrieval patterns
- Session 6 (LangGraph) is a significant conceptual jump -- spend extra time on StateGraph basics
- Lab 08 (challenge) in each session is optional for faster participants

### Day 3: Advanced Patterns & Production

| Slot | Session | Slides | Labs | Setup Script |
|------|---------|--------|------|-------------|
| A | Session 7: Advanced LangGraph Workflows | `session7-advanced-langgraph-workflows.html` | `session-7/` (8 labs) | `day3-setup.sh` |
| B | Session 8: Multi-Agent Systems | `session8-multi-agent-systems.html` | `session-8/` (8 labs) | - |
| C | Session 9: Production Application Development | `session9-production-application-development.html` | `session-9/` (8 labs) | - |
| D | Labs for Sessions 7-9 | - | All above | - |

**Day 3 Setup:** Run `bash scripts/day3-setup.sh` (verifies FastAPI packages, pulls ChromaDB).
**Day 3 Cleanup:** Run `bash scripts/day3-cleanup.sh` at end (frees resources for Day 4).

**Teaching Notes:**
- The human-in-the-loop pattern in Session 7 often generates good discussion
- Session 8 (Multi-Agent) is where concepts from Days 1-2 come together
- Session 9 (Production) bridges AI concepts with DevOps -- key for the Oracle audience
- Ensure ChromaDB containers are stopped before Day 5

### Day 4: AI Coding Agents & MCP

| Slot | Session | Slides | Labs | Setup Script |
|------|---------|--------|------|-------------|
| A | Session 10: AI Coding Agents & Vibe Coding | `session10-ai-coding-agents-vibe-coding.html` | `session-10/` (8 labs) | `day4-setup.sh` |
| B | Session 11: Model Context Protocol | `session11-model-context-protocol.html` | `session-11/` (8 labs) | - |
| C | Session 12: Building Custom AI Dev Tools | `session12-building-custom-ai-dev-tools.html` | `session-12/` (8 labs) | - |
| D | Labs for Sessions 10-12 / Review | - | All above | - |

**Day 4 Setup:** Run `bash scripts/day4-setup.sh` (installs MCP SDK, verifies Python and GROQ_API_KEY). Lightweight, ~3-4 GB RAM.
**Day 4 Cleanup:** Run `bash scripts/day4-cleanup.sh` at end (removes temp files, kills stale processes).

**Teaching Notes:**
- Day 4 connects agent concepts from Days 1-3 with the latest AI developer tools. MCP is conceptually new -- give extra time for protocol architecture. The labs are Python-only (no K8s cluster needed).
- Session 10 introduces AI coding agents and vibe coding workflows -- expect high engagement
- Session 11 (MCP) is a significant conceptual addition -- walk through the protocol architecture carefully
- Session 12 ties everything together by building custom tools -- encourage experimentation during Slot D

### Day 5: Observability & Production Operations

| Slot | Session | Slides | Labs | Setup Script |
|------|---------|--------|------|-------------|
| A | Session 13: Observability Fundamentals | `session13-observability-fundamentals.html` | `session-13/` (8 labs) | `day5-setup.sh` |
| B | Session 14: LangFuse Observability | `session14-langfuse-observability.html` | `session-14/` (8 labs) | - |
| C | Session 15: Capstone & Production Readiness | `session15-capstone-production-readiness.html` | `session-15/` (8 labs) | - |
| D | Labs for Sessions 13-15 | - | All above | - |

**Day 5 Setup:** Run `bash scripts/day5-setup.sh` (starts Prometheus + Grafana + LangFuse via Docker Compose).
**Day 5 Cleanup:** Run `bash scripts/day5-cleanup.sh` at end.

**Teaching Notes:**
- Start the observability stack early -- it takes ~2 min to stabilize
- Session 13 (OTel fundamentals) is conceptual; keep it brief if audience has observability experience
- Session 14 (LangFuse) is AI-specific and usually generates high engagement
- Session 15 (Capstone) is the culmination -- lab08 is the comprehensive challenge
- Day 5 has 3 content sessions + dedicated lab time (Slot D), allowing deeper hands-on practice
- End with course wrap-up, Q&A, and feedback collection

---

## Resource Management

The lab environment runs on GitHub Codespaces with 2-core / 8 GB RAM / 32 GB storage. Resources are tight.

### Memory Budget by Day

| Day | Active Services | Est. RAM | Notes |
|-----|----------------|----------|-------|
| 1 | Ollama + Python | ~5-6 GB | Remove Ollama at end of day |
| 2 | Python + Groq API | ~3-4 GB | Lightest day |
| 3 | Python + ChromaDB + FastAPI | ~4-5 GB | Stop containers at end |
| 4 | Python + MCP SDK | ~3-4 GB | Remove temp files at end |
| 5 | Docker Compose (4 containers) | ~5-7 GB | All containers mem-limited |

### If Resources Run Low

1. Run `bash scripts/check-resources.sh` to diagnose
2. Stop unnecessary containers: `docker stop $(docker ps -q)`
3. Prune Docker: `docker system prune -f && docker volume prune -f`
4. Clear Python cache: `find ~ -name __pycache__ -exec rm -rf {} +`
5. Check for leftover services from previous days

---

## Lab Execution Guide

### Lab Format

All 117 labs follow this pattern:
- Student runs `python hands-on/session-NN/labXX_topic.py`
- Lab prints instructions and has `# TODO` sections with `"___"` placeholders
- Student fills in answers/code in the TODO sections
- Lab validates with `[PASS]/[FAIL]` checks and a score
- Solution is in `hands-on/session-NN/solutions/labXX_topic.py`

### Lab Pacing

| Pace | Approach |
|------|----------|
| **Fast group** | All 8 labs per session, including challenge (lab08) |
| **Normal group** | Labs 01-06, skip lab07/lab08 or assign as homework |
| **Slow group** | Labs 01-04 (core concepts), share solutions for rest |

### OpenCode AI Assistant

Participants can use OpenCode (pre-installed) to help with labs:
- `opencode` -- Launch the TUI
- `opencode 'explain this error'` -- Quick help
- Encourage participants to try labs first, then use AI assistance if stuck

---

## Pre-Course Checklist

- [ ] Verify GitHub Codespace template builds successfully
- [ ] Test all 15 session slides load in browser
- [ ] Run at least lab01 + lab08 from each session to verify
- [ ] Confirm Groq API free tier is working (test with a simple call)
- [ ] Verify Docker images pull correctly in Codespace
- [ ] Prepare Google Classroom with session links
- [ ] Share participant prerequisites 1 week before course

## Post-Course

- [ ] Collect participant feedback
- [ ] Share slides/lab access for reference period
- [ ] Provide certificate of completion
- [ ] Share learning path recommendations for continued study

---

## Key Ports Reference

| Port | Service | Available |
|------|---------|-----------|
| 8000 | FastAPI App | Days 3-5 |
| 3000 | Grafana | Day 5 |
| 9090 | Prometheus | Day 5 |
| 8080 | LangFuse | Day 5 |
| 11434 | Ollama | Day 1 only |

---

## Troubleshooting Common Issues

| Issue | Solution |
|-------|----------|
| Codespace won't start | Check GitHub free tier hours remaining (need ~40 hrs) |
| Ollama out of memory | Ensure using llama3.2:1b (not larger models) |
| Groq API rate limit | Wait 1 min; each participant needs own API key |
| Docker Compose fails | Run `docker system prune -f` then retry |
| Lab validation fails | Compare with solution file; check for trailing spaces |
| Port already in use | Find and kill: `lsof -i :PORT` then `kill PID` |

---

Copyright (c) 2026 Gheware UniGPS Solutions LLP. All Rights Reserved.
