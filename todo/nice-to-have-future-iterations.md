# Nice-to-Have / Future Iterations

Low priority. Consider for v2 of the course or if extra time is available.

## 1. Add Failure Case Studies (War Stories)

**Where:** 1-2 slides per day, ideally at session transitions
**What:** Real-world agent failure examples:
- Day 1: Agent hallucination disaster (chatbot confidently gave wrong medical advice)
- Day 2: RAG retrieval failure (wrong document chunk returned, agent gave contradictory answer)
- Day 3: Multi-agent infinite loop (two agents kept delegating to each other)
- Day 4: Cost explosion (runaway agent made 10,000 API calls in a loop)
- Day 5: Prompt injection in production (user tricked agent into revealing system prompt)
**Why:** Enterprise developers love hearing what went wrong. Makes the safety and production content feel urgent rather than theoretical.
**Effort:** ~2 hours (research + create slides)

## 2. Video Walkthroughs for Hard Labs

**Where:** Sessions 7-8 challenge labs, Session 15 capstone
**What:** 5-10 minute screen recordings walking through the solution step-by-step. Host on internal platform or provide as local .mp4 files.
**Why:** Participants who get stuck can watch the walkthrough and catch up without holding back the class.
**Effort:** ~3 hours (record + edit 3-4 videos)

## 3. Enterprise Scale Patterns Slide

**Where:** Session 11 (Production)
**What:** 1 slide on horizontal scaling:
- Load balancer -> multiple FastAPI workers -> shared state via Redis
- Queue-based architecture for long-running agent calls (Celery/Redis)
- Multi-region deployment considerations
- SLA targets: p99 latency, availability, throughput
**Why:** Participants at large tech companies think in terms of thousands of concurrent users. Current S11 covers basics but doesn't address scale.
**Effort:** ~30 minutes

## 4. LLM Comparison Guide

**What:** Reference card comparing when to use different models:
- Groq (fast, free tier) vs Ollama (local, private) vs OpenAI (highest quality)
- Model size trade-offs: 1B (fast, cheap, less accurate) vs 70B (slow, expensive, more accurate)
- Use case mapping: summarization (small model OK) vs complex reasoning (large model needed)
**Where:** Handout or appendix slide
**Effort:** ~30 minutes

## 5. Additional Industry-Specific Examples

**What:** Alternate lab scenarios for different industry verticals:
- Fintech: KYC verification agent, transaction monitoring agent
- Healthcare: Patient triage agent, medical record summarizer
- E-commerce: Product recommendation agent, return processing agent
**Where:** Optional "extension labs" in a separate folder
**Effort:** ~4-6 hours (create alternate lab versions)

## 6. Async Patterns / Queuing

**Where:** Session 11 (Production)
**What:** Brief mention of task queues for background agent execution:
- Why synchronous API calls don't work for 30-second agent responses
- Celery + Redis pattern for background processing
- Webhook callbacks for long-running tasks
- Server-Sent Events (already partially covered in S11 Lab 04)
**Effort:** ~30 minutes
