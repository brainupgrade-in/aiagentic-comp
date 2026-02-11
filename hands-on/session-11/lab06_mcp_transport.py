#!/usr/bin/env python3
"""
Lab 06: MCP Transport — stdio and SSE Encoding

Implement the two MCP transport encodings: newline-delimited JSON over
stdio, and Server-Sent Events (SSE) over HTTP.

No external packages required — standard library only.
"""

import os
import json
import shutil

WORKDIR = "/tmp/aidev-lab-11-06"

# ── Cleanup & Setup ──────────────────────────────────────────────────────────
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

score = 0
total = 0

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  STEP 1 — stdio Transport                                                  ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("STEP 1: stdio Transport (Newline-Delimited JSON)")
print("=" * 70)
print()
print("  The stdio transport sends JSON-RPC messages as single lines on")
print("  stdin/stdout, each terminated by a newline character (\\n).")
print()
print("  Encoding:  dict -> json.dumps(dict) + '\\n' -> bytes (utf-8)")
print("  Decoding:  bytes -> str (utf-8) -> strip -> json.loads -> dict")
print()
print("  Example:")
print('    >>> msg = {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}')
print("    >>> encoded = (json.dumps(msg) + '\\n').encode('utf-8')")
print("    >>> # Send `encoded` to stdout")
print()
print("  This is the default transport for local MCP servers launched")
print("  as subprocesses (e.g., Claude Desktop spawning a Python server).")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  STEP 2 — SSE Transport                                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("STEP 2: SSE Transport (Server-Sent Events)")
print("=" * 70)
print()
print("  The SSE transport sends MCP messages as HTTP Server-Sent Events.")
print("  Each event has an event type and a data field (JSON).")
print()
print("  Format:")
print("    event: message")
print('    data: {"jsonrpc":"2.0","id":1,"result":{...}}')
print("    ")
print("    (blank line terminates the event)")
print()
print("  Event types used by MCP:")
print("    - 'endpoint'  : initial connection, carries the session URI")
print("    - 'message'   : standard JSON-RPC message")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 1 — Implement encode_stdio_message()                                 ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 1: Implement encode_stdio_message(msg_dict)")
print("=" * 70)
print()

def encode_stdio_message(msg_dict: dict) -> bytes:
    """Encode a JSON-RPC message for stdio transport.

    Args:
        msg_dict: A JSON-RPC message as a Python dict

    Returns:
        UTF-8 encoded bytes: compact JSON + newline
    """
    # TODO: Convert the dict to a compact JSON string (no extra spaces),
    #   append a newline, and encode as UTF-8 bytes.
    #
    # Hint:
    #   return (json.dumps(msg_dict, separators=(',', ':')) + '\n').encode('utf-8')

    return "___"  # Replace with your implementation

# ── Validate TODO 1 ─────────────────────────────────────────────────────────
total += 1
try:
    test_msg = {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
    encoded = encode_stdio_message(test_msg)
    checks = [
        isinstance(encoded, bytes),
        encoded.endswith(b'\n'),
        b'"jsonrpc"' in encoded or b'"jsonrpc":' in encoded,
        json.loads(encoded.decode('utf-8').strip()) == test_msg,
    ]
    if all(checks):
        score += 1
        print(f"[PASS] encode_stdio_message works: {encoded!r}")
    else:
        print(f"[FAIL] Encoded bytes do not meet requirements")
        print(f"       Got: {encoded!r}")
except Exception as e:
    print(f"[FAIL] Exception: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 2 — Implement decode_stdio_message()                                 ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 2: Implement decode_stdio_message(raw_bytes)")
print("=" * 70)
print()

def decode_stdio_message(raw_bytes: bytes) -> dict:
    """Decode a stdio transport message back to a dict.

    Args:
        raw_bytes: UTF-8 encoded bytes (JSON + newline)

    Returns:
        The parsed JSON-RPC message as a dict
    """
    # TODO: Decode the bytes to a UTF-8 string, strip whitespace,
    #   and parse with json.loads.
    #
    # Hint:
    #   return json.loads(raw_bytes.decode('utf-8').strip())

    return "___"  # Replace with your implementation

# ── Validate TODO 2 ─────────────────────────────────────────────────────────
total += 1
try:
    original = {"jsonrpc": "2.0", "id": 42, "method": "resources/list"}
    raw = (json.dumps(original) + '\n').encode('utf-8')
    decoded = decode_stdio_message(raw)
    if isinstance(decoded, dict) and decoded == original:
        score += 1
        print(f"[PASS] decode_stdio_message round-trips correctly")
    else:
        print(f"[FAIL] Expected {original}, got {decoded}")
except Exception as e:
    print(f"[FAIL] Exception: {e}")

# Also test full round-trip with our encoder
total += 1
try:
    msg = {"jsonrpc": "2.0", "id": 7, "result": {"tools": ["a", "b"]}}
    roundtrip = decode_stdio_message(encode_stdio_message(msg))
    if roundtrip == msg:
        score += 1
        print(f"[PASS] Full encode->decode round-trip works")
    else:
        print(f"[FAIL] Round-trip mismatch: {roundtrip} != {msg}")
except Exception as e:
    print(f"[FAIL] Round-trip exception: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 3 — Implement format_sse_event()                                     ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 3: Implement format_sse_event(event_type, data_dict)")
print("=" * 70)
print()

def format_sse_event(event_type: str, data_dict: dict) -> str:
    """Format a dict as a Server-Sent Event string.

    SSE format:
        event: <event_type>
        data: <json_string>

        (followed by a blank line to terminate the event)

    Args:
        event_type: The SSE event type (e.g., "message", "endpoint")
        data_dict: The data payload as a dict

    Returns:
        Formatted SSE event string
    """
    # TODO: Build the SSE event string.
    #   The format is exactly:
    #     "event: {event_type}\ndata: {json_data}\n\n"
    #   where json_data is a compact JSON serialization of data_dict.
    #
    # Hint:
    #   json_data = json.dumps(data_dict, separators=(',', ':'))
    #   return f"event: {event_type}\ndata: {json_data}\n\n"

    return "___"  # Replace with your implementation

# ── Validate TODO 3 ─────────────────────────────────────────────────────────
total += 1
try:
    msg = {"jsonrpc": "2.0", "id": 1, "result": {"tools": []}}
    sse = format_sse_event("message", msg)
    checks = [
        isinstance(sse, str),
        sse.startswith("event: message\n"),
        "data: " in sse,
        sse.endswith("\n\n"),
    ]
    # Parse the data field back
    data_line = [l for l in sse.split("\n") if l.startswith("data: ")][0]
    parsed_data = json.loads(data_line[len("data: "):])
    checks.append(parsed_data == msg)

    if all(checks):
        score += 1
        print("[PASS] format_sse_event produces valid SSE")
        print(f"       Output:\n         {sse.strip()}")
    else:
        print(f"[FAIL] SSE format incorrect")
        print(f"       Got: {sse!r}")
except Exception as e:
    print(f"[FAIL] Exception: {e}")

# Test endpoint event
total += 1
try:
    endpoint_data = {"uri": "/mcp/session/abc123"}
    sse2 = format_sse_event("endpoint", endpoint_data)
    checks2 = [
        "event: endpoint\n" in sse2,
        "abc123" in sse2,
        sse2.endswith("\n\n"),
    ]
    if all(checks2):
        score += 1
        print("[PASS] Endpoint SSE event formatted correctly")
    else:
        print(f"[FAIL] Endpoint event incorrect: {sse2!r}")
except Exception as e:
    print(f"[FAIL] Exception: {e}")
print()

# ── Save transport examples ─────────────────────────────────────────────────
examples = {
    "stdio_encoded_example": encode_stdio_message(
        {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
    ).decode('utf-8') if isinstance(encode_stdio_message({"jsonrpc": "2.0", "id": 1, "method": "tools/list"}), bytes) else "N/A",
    "sse_event_example": format_sse_event(
        "message", {"jsonrpc": "2.0", "id": 1, "result": {}}
    ) if isinstance(format_sse_event("message", {"jsonrpc": "2.0", "id": 1, "result": {}}), str) else "N/A",
}
out_path = os.path.join(WORKDIR, "transport_examples.json")
with open(out_path, "w") as f:
    json.dump(examples, f, indent=2)
print(f"Transport examples saved to {out_path}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  RESULTS                                                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print(f"Lab 06 Score: {score}/{total}")
print("=" * 70)
