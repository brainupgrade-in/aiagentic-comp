# Agentic AI Course

5-day enterprise training by Rajesh Gheware. 15 sessions, 119 labs + solutions.
- Slides: `presentation/` (15 HTML decks) · Labs: `hands-on/session-{1..15}/`
- Outline: `course-outline-agentic-ai.pdf` · Repo: `brainupgrade-in/aiagentic-comp`

## Environment

**Platform:** Native Ubuntu Linux — NOT Codespaces (`.devcontainer/` unused here)
**Python:** 3.12 · **Venv:** `.venv/` · `python3 -m venv .venv && pip install -r requirements.txt`
**Instructor:** 12 CPU / 16 GB RAM · **Participants:** 8+ CPU / 16 GB RAM (Ubuntu/macOS/Win Git Bash)

## Tech Stack & Key Decisions

| Component | Choice | Note |
|-----------|--------|------|
| LLM Day 1 | Ollama + llama3.2:1b+ | Local inference; 3b/70b also viable |
| LLM Days 2-5 | Groq free API (primary) | Each participant gets own key at console.groq.com |
| LLM alt providers | OpenRouter, Big Pickle, Claude, OpenAI | Taught as provider-agnostic patterns — fallback chains, cost/latency tradeoffs |
| Vibe coding | OpenCode (opencode.ai), Claude CLI | Day 1 — agent-assisted dev, prompt-to-code |
| Observability | LangFuse Cloud (free tier), **v4 SDK** | S12 Labs 01-08: MockLangFuse (JSON) shaped like the v4 client. Lab 09: real traces to each participant's **own** cloud project — they self-register at cloud.langfuse.com and put their keys in `.env`. Offline fallback: `langfuse-server.sh` (local FastAPI+SQLite, set `LANGFUSE_HOST=http://localhost:3000`) |
| Vector DB | ChromaDB | In-process, no server |
| API | FastAPI | Async, AI-native |
| Agents | `create_agent` from `langchain.agents` | **Not** `langgraph.prebuilt.create_react_agent` (deprecated in LangGraph v1, removed in v2) |
| MCP | MCP Python SDK `mcp>=1.28` | Standard protocol |
| Deployment | Docker + Kubernetes | Day 4: containerize FastAPI agent, deploy to K8s (Deployments, Services, Ingress, HPA, Secrets, NetworkPolicies) |

## Library API Versions (course is on the 1.x / v4 lines)

Everything below is already migrated across labs, solutions, decks and docs. If you
see the left-hand column anywhere, it is stale — the packages no longer expose it.

| Don't use (removed) | Use instead | Where it applies |
|---------------------|-------------|------------------|
| `from langgraph.prebuilt import create_react_agent` | `from langchain.agents import create_agent` | Session 6 labs, session 13 deck |
| `create_react_agent(llm, tools, prompt=...)` | `create_agent(llm, tools, system_prompt=...)` | same — positional args unchanged |
| `from langfuse.callback import CallbackHandler` | `from langfuse.langchain import CallbackHandler` | Sessions 12, 15 |
| `CallbackHandler(user_id=…, session_id=…, tags=…, trace_name=…)` | `CallbackHandler(trace_context={"trace_id": …})`; attributes go in the run config `metadata` as `langfuse_user_id` / `langfuse_session_id` / `langfuse_tags`, trace name via `run_name` | Sessions 12, 15 |
| `handler.get_trace_id()` | `trace_id = langfuse.create_trace_id()` **before** the run, bound via `trace_context` | Sessions 12, 15 |
| `handler.flush()` | `langfuse.flush()` (client-level); `langfuse.shutdown()` to drain on exit | Sessions 12, 15 |
| `langfuse.score(...)` | `langfuse.create_score(name=…, value=…, data_type="NUMERIC"\|"CATEGORICAL", trace_id=…)` | Sessions 12, 15 |
| `langfuse.trace()` / `trace.generation(usage={...})` | `langfuse.start_as_current_observation(name=…)` / `(as_type="generation", …)` then `.update(usage_details={…}, cost_details={…})` | Session 12 |
| `langfuse.fetch_traces()` | `langfuse.api.trace.list(...)` → `.data`, fields `total_cost`, `user_id`, `observations` | Session 12 |
| `from langfuse.decorators import observe, langfuse_context` | `from langfuse import observe, get_client, propagate_attributes` | Session 15 lab 04 |
| `langfuse_context.update_current_trace(...)` | `with propagate_attributes(user_id=…, session_id=…, tags=[…], trace_name=…):` | Session 15 lab 04 |
| `langfuse_context.update_current_observation(...)` | `get_client().update_current_span(...)` | Session 15 lab 04 |
| `prompt.prompt` in a ChatPromptTemplate | `prompt.get_langchain_prompt()` (converts `{{var}}` → `{var}`) | Session 12 lab 06 |

`requirements.txt` floors track the installed releases (langchain 1.3, langgraph 1.2,
langfuse 4.14, chromadb 1.5, fastapi 0.140, mcp 1.28, ipykernel 7.3).

**One deliberate exception to floors-only:** `ruff>=0.16,<0.17` is capped, because the
formatter's output changes between minor releases and format-on-save is enabled in
`.vscode/settings.json` — an open range would have participants reformatting each
other's files. The cap governs the editor too, not just the CLI: `ruff.importStrategy`
is `fromEnvironment`, so VS Code formats with the `.venv`'s pinned ruff and only falls
back to the extension's bundled binary when the venv has none (i.e. before setup).
Don't widen the cap without re-running `ruff format` across `scripts/` and `reporting/`
in its own commit.

## Resource Usage by Day

| Day | Services | RAM | Cleanup |
|-----|----------|-----|---------|
| 1 | Ollama + LangChain | 3-6 GB | optional |
| 2 | LangChain + Groq + ChromaDB | 2-3 GB | optional |
| 3 | LangGraph + Multi-Agent | 3-4 GB | optional |
| 4 | OTel + LangFuse + FastAPI | 2-3 GB | **stop LangFuse; rm DB/logs** |
| 5 | MCP + Safety + Capstone | 3-4 GB | recommended final cleanup |

## Key Ports

| Port | Service | Active |
|------|---------|--------|
| 3000 | LangFuse local server — **offline fallback only** (course uses cloud) | Day 4 Session 12 Lab 09 |
| 8000 | FastAPI app | Day 4 Session 11 |
| 11434 | Ollama | Day 1 only |

## Lab Pattern

Notebooks: `hands-on/session-NN/labXX_topic.ipynb` (student) · `solutions/labXX_topic.ipynb` (answer)

- Code cells have `"___"` placeholders; validation outputs `[PASS]/[FAIL]` with scoring
- Output dirs: `/tmp/k8s-lab-NN-XX/` · `/tmp/aidev-lab-NN-XX/` · `/tmp/prod-lab-11-XX/` · `/tmp/safety-lab-14-XX/` · `/tmp/capstone-lab-15-XX/`
- Labs build progressively; final lab per session = comprehensive challenge
- Timing: ~60-75 min/session; session 12 ~90-115 min; session 15 ~90-120 min

### Editing notebooks without wrecking the diff

Notebooks are stored with `indent=2` + trailing newline; `ensure_ascii` **varies per
file**. Never blind-write with `json.dump(..., indent=1)` — it reformats the whole file
and turns a 3-line change into a 2,000-line diff. Detect the format by round-tripping:

```python
orig = open(path).read(); nb = json.loads(orig)
ea = next(e for e in (True, False)
          if json.dumps(nb, indent=2, ensure_ascii=e) + "\n" == orig)
```

Also preserve each cell's `source` **shape**: some cells hold a plain string, some a
single-element list, most a list of lines. Splitting a single-element list into lines
is what inflates diffs. Some cells have trailing whitespace on blank lines — match
right-stripped when searching.

### Known non-passing solution notebooks (115/119 pass)

Not regressions — model-capability or authoring issues, verified against current packages:

| Notebook | Cause |
|----------|-------|
| `session-7/solutions/lab01_first_graph.ipynb` | Intentional `KeyError` demo, but the explanatory `print()`s after `app4.invoke()` are unreachable |
| `session-4/solutions/lab05_output_parsers.ipynb` | llama3.2:1b can't emit the pydantic object (llama3.1:8b passes 3/3) |
| `session-3/solutions/lab07_challenge.ipynb` | Scores 6/7 — llama3.2:1b answers without calling a tool |
| `session-6/solutions/lab08_challenge.ipynb` | Groq llama-3.3-70b emits a malformed tool call; A/B-tested — **not** caused by the `create_agent` migration |

The 119 *student* notebooks are not meant to execute clean — they contain `___`
placeholders and report `[TODO]`/`[FAIL]` by design.

**Scores 10/10 but reports a misleading row:** `session-3/solutions/lab05_tool_calling.ipynb`.
Its TODOs validate structure, not accuracy, so it passes — but on llama3.2:1b the
`summarize_text` question in Steps 4/5 is a near-deterministic miss (0/5 correct over
30 measured calls; it routes to `translate_text`, occasionally `calculate_shipping`).
The lab does *prompt-based* tool calling with no `bind_tools` grammar constraint, so
1b also invents names — `summary_text` for `summarize_text` being the common one.
`parse_tool_choice` now validates against `TOOL_FUNCTIONS` and renders an invented name
as `<invalid: …>`, so it reads as a bad call rather than a wrong tool choice. Enriching
the description does **not** fix the routing (A/B-tested, still 0/8); llama3.1:8b scores
6/6 on the same prompt. Expect the "good descriptions" row to land ~80%, not 100%.

## File Structure

```
├── presentation/       15 HTML decks + shared.css/js, Reveal.js HUD, print support
├── hands-on/           session-{1..15}/ with .ipynb labs + solutions/
├── scripts/            setup.sh (all 5 days, idempotent), bootstrap.ps1 (Windows),
│                       cleanup.sh, configure-notebooks.py, langfuse-server.{sh,py},
│                       submit-lab.sh, check-resources.sh
├── reporting/          generate-dashboard.py, track-lab-comments.py, update-dashboard.sh
├── .github/            ISSUE_TEMPLATE/ (lab-help, bug-report, config)
├── .vscode/            settings.json, extensions.json
├── requirements.txt    All Python deps
└── .env.example        Template for all 5 days
```

## Commands

```bash
# Setup — one run covers all 5 days; no per-day setup scripts
source scripts/setup.sh                 # uv + Python 3.12 + venv + all packages + kernel + Ollama
bash scripts/setup.sh --verify          # check venv/packages/kernel/keys/Ollama
bash scripts/setup.sh --kernel-only     # re-register kernel + reconfigure notebooks
powershell -File scripts/bootstrap.ps1  # Windows: Git Bash + uv + Ollama, then setup.sh
bash scripts/check-resources.sh         # memory/storage/process status

# Per-day
bash scripts/cleanup.sh [1-5|all]       # end-of-day cleanup
bash scripts/langfuse-server.sh start   # offline fallback only — course uses LangFuse Cloud

# Lab submission
bash scripts/submit-lab.sh <session> <lab> "notes"

# Reporting
export GITHUB_TOKEN=$(cat ~/.rajesh/.github_bu)
python3 reporting/generate-dashboard.py --output reporting/dashboard.html --auto-refresh
python3 reporting/track-lab-comments.py          # text report

# Presentation
firefox presentation/index.html
firefox presentation/session1-introduction-to-agentic-ai.html
```

## Lab Tracking

Participants submit via `submit-lab.sh` → GitHub Issue comment (label: `lab-tracking`).
Issues: `https://github.com/brainupgrade-in/aiagentic-comp/issues?q=label%3Alab-tracking`

## Error Recovery

| Issue | Fix |
|-------|-----|
| High memory | `check-resources.sh`; OOM unlikely with 16 GB unless multiple large models |
| Disk space | `du -sh ~/.ollama/models`; `ollama rm <model>` |
| Groq 429 | Wait 60s; stagger class starts. Check whether it's RPM (30) or the daily token cap (100K) — see Groq API below |
| Port conflict | `sudo lsof -i :8000` or `:11434`; stop conflicting service |
| Package conflicts | `rm -rf .venv && python3 -m venv .venv && pip install -r requirements.txt` |

## Groq API

`GROQ_API_KEY` in `.env`. LangChain: `langchain-groq` / `ChatGroq`.

**Measured free-tier limits for `llama-3.3-70b-versatile`** (July 2026 — much tighter
than Groq's headline numbers, and the reason labs must be paced):

| Limit | Value |
|-------|-------|
| Requests / minute | **30** |
| Requests / day | **1,000** |
| Tokens / minute | **12,000** |
| Tokens / day | **100,000** |

Implications: don't run a whole session's notebooks in parallel on one key; the daily
token cap is the one that actually bites during a full-repo test sweep. For headless
sweeps, throttle with `langchain_core.rate_limiters.InMemoryRateLimiter`
(`requests_per_second=0.42`) rather than editing notebooks.

## OpenCode (Optional)

```bash
curl -fsSL https://opencode.ai/install | bash
opencode 'your prompt'   # or just `opencode` for TUI
```
Auth: `/connect` → GitHub Copilot, or set `GROQ_API_KEY`. Tab switches `build`/`plan` agents.

## Git Remote

`https://github.com/brainupgrade-in/aiagentic-comp.git` · branch: `main` · auth: `gh auth login -h github.com`
