# Instructor Guide

**Course:** Agentic AI: Comprehensive Course
**Trainer:** Rajesh Gheware
**Client:** Enterprise client
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

### Day 1: Foundations & AI-Assisted Development

| Slot | Session | Slides | Labs | Setup Script |
|------|---------|--------|------|-------------|
| A | Session 1: Introduction to Agentic AI | `session1-introduction-to-agentic-ai.html` | `session-1/` (6 labs) | `day1-setup.sh` |
| B | Session 2: AI Coding Assistants & Vibe Coding | `session2-ai-coding-assistants-vibe-coding.html` | `session-2/` (8 labs) | - |
| C | Session 3: Reasoning, Planning & Tool Use | `session3-reasoning-planning-tool-use.html` | `session-3/` (7 labs) | - |
| D | Labs for Sessions 1-3 | - | All above | - |

**Day 1 Setup:** Run `bash scripts/day1-setup.sh` at start (installs Ollama + llama3.2:1b).
**Day 1 Cleanup:** Run `bash scripts/day1-cleanup.sh` at end (frees ~2 GB).

**Teaching Notes:**
- Session 1 sets the foundation -- ensure participants understand the difference between LLMs and agents
- Session 2 introduces AI coding agents early so students can use AI assistants for the remaining 4 days
- Ollama is used for Day 1 demos only; from Day 2 onwards, switch to Groq API
- Have participants create Groq API keys during a break: https://console.groq.com
- Encourage participants to use OpenCode during labs from Day 1 onwards
- Lab time covers sessions 1-3 labs; prioritize session-2 labs (vibe coding) so tools are familiar early

### Day 2: LangChain, RAG & Agents

| Slot | Session | Slides | Labs | Setup Script |
|------|---------|--------|------|-------------|
| A | Session 4: LangChain Fundamentals | `session4-langchain-fundamentals.html` | `session-4/` (8 labs) | `day2-setup.sh` |
| B | Session 5: Building RAG Applications | `session5-building-rag-applications.html` | `session-5/` (8 labs) | - |
| C | Session 6: LangChain Agents & Memory | `session6-langchain-agents-memory.html` | `session-6/` (8 labs) | - |
| D | Labs for Sessions 4-6 | - | All above | - |

**Day 2 Setup:** Run `bash scripts/day2-setup.sh` (verifies Groq API key and packages).
**Day 2 Cleanup:** Run `bash scripts/day2-cleanup.sh` at end.

**Teaching Notes:**
- Verify all participants have working Groq API keys before starting
- Session 4 (LangChain) builds the foundation for Days 2-3 -- ensure all participants grasp LCEL
- Session 5 (RAG) is foundational for the rest of the course -- ensure all participants grasp retrieval patterns
- Session 6 (Agents & Memory) is a significant conceptual jump -- spend extra time on agent types
- Lab 08 (challenge) in each session is optional for faster participants

### Day 3: LangGraph & Multi-Agent Systems

| Slot | Session | Slides | Labs | Setup Script |
|------|---------|--------|------|-------------|
| A | Session 7: LangGraph Stateful Workflows | `session7-langgraph-stateful-workflows.html` | `session-7/` (8 labs) | `day3-setup.sh` |
| B | Session 8: Advanced LangGraph Workflows | `session8-advanced-langgraph-workflows.html` | `session-8/` (8 labs) | - |
| C | Session 9: Multi-Agent Systems | `session9-multi-agent-systems.html` | `session-9/` (8 labs) | - |
| D | Labs for Sessions 7-9 | - | All above | - |

**Day 3 Setup:** Run `bash scripts/day3-setup.sh` (verifies LangGraph packages).
**Day 3 Cleanup:** Run `bash scripts/day3-cleanup.sh` at end (frees resources for Day 4).

**Teaching Notes:**
- Session 7 (LangGraph) is a significant conceptual jump -- spend extra time on StateGraph basics
- The human-in-the-loop pattern in Session 8 often generates good discussion
- Session 9 (Multi-Agent) is where concepts from Days 1-2 come together
- Ensure ChromaDB containers are stopped before Day 4

### Day 4: Observability & Production

| Slot | Session | Slides | Labs | Setup Script |
|------|---------|--------|------|-------------|
| A | Session 10: Observability Fundamentals | `session10-observability-fundamentals.html` | `session-10/` (8 labs) | `day4-setup.sh` |
| B | Session 11: Production Development & Deployment | `session11-production-development-deployment.html` | `session-11/` (8 labs) | - |
| C | Session 12: LangFuse Observability | `session12-langfuse-observability.html` | `session-12/` (9 labs) | - |
| D | Labs for Sessions 10-12 | - | All above + Lab 09 capstone | - |

**Day 4 Setup:** Run `bash scripts/day4-setup.sh` (verifies OTel, LangFuse SDK, and FastAPI packages).
**Day 4 Cleanup:** Run `bash scripts/day4-cleanup.sh` at end (cleans temp files).

**Teaching Notes:**
- Session 10 (OTel fundamentals) is conceptual; keep it brief if audience has observability experience
- Session 11 (Production) bridges AI concepts with DevOps -- key for enterprise audiences. Build FastAPI app before instrumenting it.
- Session 12 (LangFuse) uses mock mode with SDK patterns -- data logs to local JSON files. Better flow: build app (Session 11), then instrument it (Session 12).
- **Session 12 Lab 09 is the capstone** -- integrates Session 11 production app with Session 12 LangFuse observability. This demonstrates the full Day 4 progression: theory → build → instrument.
- All Session 12 labs are self-contained -- MockLangfuse is defined in each lab, no pre-setup needed
- Day 4 is lightweight on infrastructure -- all Python in-process (~3-4 GB RAM)

### Day 5: MCP, Safety & Capstone

| Slot | Session | Slides | Labs | Setup Script |
|------|---------|--------|------|-------------|
| A | Session 13: Model Context Protocol | `session13-model-context-protocol.html` | `session-13/` (8 labs) | `day5-setup.sh` |
| B | Session 14: AI Safety & Guardrails | `session14-ai-safety-guardrails.html` | `session-14/` (8 labs) | - |
| C+D | Session 15: Capstone Project | `session15-capstone-project.html` | `session-15/` (8 labs) | - |

**Day 5 Setup:** Run `bash scripts/day5-setup.sh` (installs MCP SDK, verifies environment).
**Day 5 Cleanup:** Run `bash scripts/day5-cleanup.sh` at end.

**Teaching Notes:**
- Session 13 (MCP) focuses on enterprise use cases and consuming MCP -- walk through the N×M problem, then enterprise use cases (data access, dev productivity, knowledge ops), then client config and LangChain bridge
- Session 14 (AI Safety) is critical for enterprise audience -- emphasize OWASP Top 10 for LLMs and production guardrails
- Session 15 (Capstone) uses 2 time slots (Slots C+D) for extended hands-on work
- The capstone integrates all 5 days -- encourage participants to reference previous session labs
- Lab 08 is the comprehensive final challenge -- allow extra time
- End with course wrap-up, Q&A, and feedback collection
- Day 5 is lightweight on infrastructure (no observability stack needed)

---

## Resource Management

The lab environment runs on native Ubuntu Linux installations with 16 GB RAM. Resource constraints are minimal compared to cloud-hosted environments.

### Memory Budget by Day

| Day | Active Services | Est. RAM | Notes |
|-----|----------------|----------|-------|
| 1 | Ollama + Python | ~5-6 GB | Remove Ollama at end of day |
| 2 | Python + Groq API | ~3-4 GB | Lightest day |
| 3 | Python + ChromaDB | ~4-5 GB | Stop containers at end |
| 4 | Python + OTel + mock LangFuse | ~3-4 GB | All in-process, lightweight |
| 5 | Python + MCP SDK | ~3-4 GB | Lightweight |

### If Resources Run Low

1. Run `bash scripts/check-resources.sh` to diagnose
2. Stop unnecessary Python processes
3. Clear Python cache: `find ~ -name __pycache__ -exec rm -rf {} +`
4. Remove temp files: `rm -rf /tmp/ailab-* /tmp/prod-lab-* /tmp/capstone-lab-*`
5. Check for leftover services from previous days (e.g., Ollama on Day 2+)

---

## Lab Execution Guide

### Lab Format

All 117 labs are Jupyter notebooks (.ipynb). The pattern:
- Student opens `hands-on/session-NN/labXX_topic.ipynb` in VS Code or JupyterLab
- Lab has markdown instruction cells and code cells with `# TODO` sections and `"___"` placeholders
- Student fills in answers/code in the TODO cells and runs them
- Lab validates with `[PASS]/[FAIL]` checks and a score
- Solution is in `hands-on/session-NN/solutions/labXX_topic.ipynb`

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
- [ ] Verify all Python packages install correctly in Codespace
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
| 8000 | FastAPI App | Day 4 |
| 11434 | Ollama | Day 1 only |

---

## Troubleshooting Common Issues

| Issue | Solution |
|-------|----------|
| Codespace won't start | Check GitHub free tier hours remaining (need ~40 hrs) |
| Ollama out of memory | Ensure using llama3.2:1b (not larger models) |
| Groq API rate limit | Wait 1 min; each participant needs own API key |
| Python process crash | Check logs, restart with `uvicorn app:app --host 0.0.0.0 --port 8000` |
| Lab validation fails | Compare with solution file; check for trailing spaces |
| Port already in use | Find and kill: `lsof -i :PORT` then `kill PID` |

---

Copyright (c) 2026 Gheware UniGPS Solutions LLP. All Rights Reserved.
