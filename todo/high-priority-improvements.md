# High Priority Improvements

These significantly increase engagement and value. Implement if time permits before delivery.

## 1. Add Interactive Chat Demo (1 per day) — NOT NEEDED

**Status:** Already exists in course materials

Challenge labs in Sessions 3, 4, 5, 6 already include interactive `input()` chat loops as bonus sections (Part E). Participants can "talk to their agent" directly in the notebook. A Gradio/Streamlit wrapper would be a nice-to-have for future iterations but is not a gap.

## 2. Add Cost Optimization Content — NOT NEEDED

**Status:** Already covered in Session 2

Token budgeting and context management are covered in Session 2 (AI Coding Assistants & Vibe Coding), Lab 03 (Context Management). Additionally, Session 12 Lab 07 covers cost analysis with LangFuse.

## 3. Smooth Session 6 to 7 Difficulty Jump — OPEN

**Where:** `hands-on/session-7/` (especially Lab 08 challenge)
**What:**
- Add "hint" markdown cells in Session 7 Labs 05-08 with collapsible hints
- Add a "LangGraph Quick Reference" card at the top of Session 7 README
- Consider splitting Session 7 Lab 08 challenge into Part A (guided) and Part B (independent)
**Why:** Session 6 agents are relatively straightforward (tools + memory). Session 7 introduces StateGraph, TypedDict, reducers, conditional edges — a significant conceptual leap. The challenge lab (support request workflow with HITL) is rated HARD. Some participants will get stuck.
**Effort:** ~1-2 hours (add hints, reference card, restructure challenge)
