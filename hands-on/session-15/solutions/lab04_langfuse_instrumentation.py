#!/usr/bin/env python3
"""
Lab 04 Solution: Add LangFuse Instrumentation

Write LangFuse instrumentation code: callback handler setup, trace
hierarchy (trace -> span -> generation), and cost tracking fields.

No external packages required -- standard library only.
"""

import os
import json
import shutil
from typing import Dict, List, Any

WORKDIR = "/tmp/capstone-lab-15-04"

# -- Cleanup & Setup ---------------------------------------------------------
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

score = 0
total = 0

# ============================================================================
# STEP 1 -- LangFuse Trace Hierarchy
# ============================================================================

print("=" * 70)
print("STEP 1: LangFuse Trace Hierarchy")
print("=" * 70)
print()
print("  LangFuse organizes observability data in a three-level hierarchy:")
print()
print("  Trace (top level -- one per user request)")
print("    |")
print("    +-- Span (logical step -- e.g., 'retrieve_context')")
print("    |     |")
print("    |     +-- Generation (LLM call -- input/output/tokens/cost)")
print("    |")
print("    +-- Span ('generate_answer')")
print("          |")
print("          +-- Generation (another LLM call)")
print()
print("  +-------------+----------------------------------------------+")
print("  | Level        | What It Captures                            |")
print("  +-------------+----------------------------------------------+")
print("  | Trace        | User ID, session ID, total latency, tags    |")
print("  | Span         | Step name, start/end time, metadata         |")
print("  | Generation   | Model, prompt, completion, tokens, cost     |")
print("  +-------------+----------------------------------------------+")
print()

# ============================================================================
# STEP 2 -- LangFuse Callback Handler Setup
# ============================================================================

print("=" * 70)
print("STEP 2: LangFuse Callback Handler Setup (LangChain)")
print("=" * 70)
print()
print("  LangFuse integrates with LangChain via a callback handler:")
print()
print("  from langfuse.callback import CallbackHandler")
print()
print("  handler = CallbackHandler(")
print("      public_key='pk-...',")
print("      secret_key='sk-...',")
print("      host='http://localhost:3000',    # LangFuse server")
print("      trace_name='support-agent',")
print("      user_id='user-123',")
print("      session_id='session-abc',")
print("  )")
print()
print("  # Pass to any LangChain invoke call:")
print("  result = chain.invoke(input, config={'callbacks': [handler]})")
print()

# ============================================================================
# STEP 3 -- Cost Tracking
# ============================================================================

print("=" * 70)
print("STEP 3: LangFuse Cost Tracking")
print("=" * 70)
print()
print("  LangFuse automatically tracks costs per generation:")
print()
print("  +---------------------+------------------------------------------+")
print("  | Field               | Description                              |")
print("  +---------------------+------------------------------------------+")
print("  | input_tokens        | Number of prompt tokens                  |")
print("  | output_tokens       | Number of completion tokens              |")
print("  | total_tokens        | input_tokens + output_tokens             |")
print("  | input_cost          | Cost of prompt (price * input_tokens)    |")
print("  | output_cost         | Cost of completion                       |")
print("  | total_cost          | input_cost + output_cost                 |")
print("  | model               | Model name (e.g., llama-3.1-70b)        |")
print("  +---------------------+------------------------------------------+")
print()
print("  Cost formula (per generation):")
print("    input_cost  = input_tokens  * price_per_1k_input  / 1000")
print("    output_cost = output_tokens * price_per_1k_output / 1000")
print("    total_cost  = input_cost + output_cost")
print()

# ============================================================================
# TODO 1 -- Define Callback Handler Configuration
# ============================================================================

print("=" * 70)
print("TODO 1: Define the LangFuse callback handler configuration")
print("=" * 70)
print()

handler_config = {
    "public_key": "pk-lf-capstone-demo",
    "secret_key": "sk-lf-capstone-demo",
    "host": "http://localhost:3000",
    "trace_name": "support-agent",
    "user_id": "capstone-user",
    "session_id": "capstone-session-001",
    "tags": ["capstone", "day5"],
    "metadata": {"environment": "development", "version": "1.0.0"},
}

# -- Validate TODO 1 --------------------------------------------------------
total += 1
expected_config = {
    "public_key": "pk-lf-capstone-demo",
    "secret_key": "sk-lf-capstone-demo",
    "host": "http://localhost:3000",
    "trace_name": "support-agent",
    "user_id": "capstone-user",
    "session_id": "capstone-session-001",
    "tags": ["capstone", "day5"],
    "metadata": {"environment": "development", "version": "1.0.0"},
}
if handler_config == expected_config:
    score += 1
    print("[PASS] Callback handler configuration is correct")
else:
    print("[FAIL] Expected:", json.dumps(expected_config, indent=2))
    print("       Got:     ", json.dumps(handler_config, indent=2) if isinstance(handler_config, dict) else handler_config)
print()

# ============================================================================
# TODO 2 -- Map Trace Hierarchy Levels
# ============================================================================

print("=" * 70)
print("TODO 2: Map trace hierarchy levels to what they capture")
print("=" * 70)
print()

trace_hierarchy = {
    "trace":      ["user_id", "session_id", "total_latency", "tags", "metadata"],
    "span":       ["name", "start_time", "end_time", "metadata", "input", "output"],
    "generation": ["model", "prompt", "completion", "input_tokens", "output_tokens", "total_cost"],
}

# -- Validate TODO 2 --------------------------------------------------------
total += 1
expected_hierarchy = {
    "trace":      ["user_id", "session_id", "total_latency", "tags", "metadata"],
    "span":       ["name", "start_time", "end_time", "metadata", "input", "output"],
    "generation": ["model", "prompt", "completion", "input_tokens", "output_tokens", "total_cost"],
}
if trace_hierarchy == expected_hierarchy:
    score += 1
    print("[PASS] Trace hierarchy mapping is correct")
    for level, fields in trace_hierarchy.items():
        print(f"       {level}: {fields}")
else:
    print("[FAIL] Expected:", expected_hierarchy)
    print("       Got:     ", trace_hierarchy)
print()

# ============================================================================
# TODO 3 -- Write Trace Decorator Pattern
# ============================================================================

print("=" * 70)
print("TODO 3: Write the LangFuse trace decorator code pattern")
print("=" * 70)
print()

trace_decorator_code = '''
from langfuse.decorators import observe, langfuse_context

@observe()
def handle_support_request(question: str, user_id: str, session_id: str):
    langfuse_context.update_current_trace(
        user_id=user_id,
        session_id=session_id,
        tags=["support", "capstone"],
    )
    langfuse_context.update_current_observation(
        metadata={"question_length": len(question)},
    )
    # ... agent logic here ...
    return response
'''

# -- Validate TODO 3 --------------------------------------------------------
total += 1
required_kw = ["from langfuse.decorators import", "@observe",
               "langfuse_context", "update_current_trace",
               "update_current_observation", "user_id", "session_id"]
if isinstance(trace_decorator_code, str) and trace_decorator_code != "___":
    found = [kw for kw in required_kw if kw in trace_decorator_code]
    if len(found) == len(required_kw):
        score += 1
        print("[PASS] Trace decorator code contains all required keywords")
        print(f"       Keywords found: {found}")
    else:
        missing = [kw for kw in required_kw if kw not in trace_decorator_code]
        print(f"[FAIL] Missing keywords: {missing}")
else:
    print("[FAIL] trace_decorator_code must be a non-placeholder string")
print()

# ============================================================================
# TODO 4 -- Calculate Cost Tracking
# ============================================================================

print("=" * 70)
print("TODO 4: Calculate LLM costs for a sample trace")
print("=" * 70)
print()

cost_tracking = {
    "gen1_input_cost":    0.00025,
    "gen1_output_cost":   0.0002,
    "gen1_total_cost":    0.00045,
    "gen2_input_cost":    0.0006,
    "gen2_output_cost":   0.0008,
    "gen2_total_cost":    0.0014,
    "trace_total_cost":   0.00185,
    "trace_total_tokens": 2700,
}

# -- Validate TODO 4 --------------------------------------------------------
total += 1
expected_costs = {
    "gen1_input_cost":    0.00025,
    "gen1_output_cost":   0.0002,
    "gen1_total_cost":    0.00045,
    "gen2_input_cost":    0.0006,
    "gen2_output_cost":   0.0008,
    "gen2_total_cost":    0.0014,
    "trace_total_cost":   0.00185,
    "trace_total_tokens": 2700,
}
cost_ok = True
for key, expected_val in expected_costs.items():
    got = cost_tracking.get(key)
    if isinstance(got, (int, float)) and abs(got - expected_val) < 1e-10:
        continue
    cost_ok = False
    break

if cost_ok:
    score += 1
    print("[PASS] Cost calculations are correct")
    print(f"       Gen 1 cost:    ${cost_tracking['gen1_total_cost']:.5f}")
    print(f"       Gen 2 cost:    ${cost_tracking['gen2_total_cost']:.5f}")
    print(f"       Trace total:   ${cost_tracking['trace_total_cost']:.5f}")
    print(f"       Total tokens:  {cost_tracking['trace_total_tokens']}")
else:
    print("[FAIL] Expected:", expected_costs)
    print("       Got:     ", cost_tracking)
print()

# ============================================================================
# TODO 5 -- Assemble Instrumentation Config
# ============================================================================

print("=" * 70)
print("TODO 5: Assemble the complete instrumentation configuration")
print("=" * 70)
print()

instrumentation_config = {
    "handler": handler_config,
    "trace_hierarchy": trace_hierarchy,
    "cost_model": {
        "model": "llama-3.1-70b-versatile",
        "price_per_1k_input": 0.0005,
        "price_per_1k_output": 0.001,
    },
    "sample_trace_cost": cost_tracking,
}

# -- Validate TODO 5 --------------------------------------------------------
total += 1
try:
    checks = [
        isinstance(instrumentation_config, dict),
        instrumentation_config.get("handler") == expected_config,
        isinstance(instrumentation_config.get("trace_hierarchy"), dict),
        instrumentation_config.get("cost_model", {}).get("model") == "llama-3.1-70b-versatile",
        instrumentation_config.get("cost_model", {}).get("price_per_1k_input") == 0.0005,
        instrumentation_config.get("cost_model", {}).get("price_per_1k_output") == 0.001,
        isinstance(instrumentation_config.get("sample_trace_cost"), dict),
    ]
    if all(checks):
        score += 1
        out_path = os.path.join(WORKDIR, "instrumentation_config.json")
        with open(out_path, "w") as f:
            json.dump(instrumentation_config, f, indent=2)
        print(f"[PASS] Instrumentation config saved to {out_path}")
    else:
        failed = [i for i, c in enumerate(checks) if not c]
        print(f"[FAIL] Config checks failed at indices: {failed}")
        print(f"       Got: {instrumentation_config}")
except Exception as e:
    print(f"[FAIL] Config exception: {e}")
print()

# ============================================================================
# RESULTS
# ============================================================================

print("=" * 70)
print(f"Lab 04 Score: {score}/{total}")
print("=" * 70)
