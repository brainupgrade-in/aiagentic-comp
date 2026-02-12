"""
Lab 03: Function Calling & Tool Binding
=========================================
Goal: Understand how LLMs make structured tool calls using bind_tools(),
      and how to process the results manually.

What you'll learn:
- How bind_tools() teaches the LLM about available tools
- The structure of a tool call (name, args, id)
- How to execute tool calls and return results via ToolMessage
- The difference between an agent (automatic) and manual tool execution
"""

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage

load_dotenv()

print("=" * 50)
print("  Function Calling & Tool Binding")
print("=" * 50)

# ============================================================
# Step 1: Create tools
# ============================================================

@tool
def calculate_emi(principal: float, rate: float, months: int) -> str:
    """Calculate monthly EMI (Equated Monthly Installment) for a loan.

    Args:
        principal: Loan amount in rupees
        rate: Annual interest rate (e.g., 8.5 for 8.5%)
        months: Loan tenure in months
    """
    r = rate / 100 / 12  # Monthly interest rate
    if r == 0:
        emi = principal / months
    else:
        emi = principal * r * (1 + r)**months / ((1 + r)**months - 1)
    return f"EMI: Rs {emi:,.0f}/month for {months} months at {rate}% on Rs {principal:,.0f}"

@tool
def get_exchange_rate(currency: str) -> str:
    """Get the current exchange rate of INR against a foreign currency.

    Args:
        currency: Currency code (USD, EUR, GBP, JPY)
    """
    rates = {"USD": 83.5, "EUR": 91.2, "GBP": 106.8, "JPY": 0.56}
    rate = rates.get(currency.upper())
    if rate:
        return f"1 {currency.upper()} = Rs {rate}"
    return f"Exchange rate not available for {currency}"

print("Tools created: calculate_emi, get_exchange_rate")

# ============================================================
# Step 2: Bind tools to the LLM
# ============================================================
# bind_tools() tells the LLM what tools are available.
# The LLM can then output STRUCTURED tool calls instead of plain text.

llm = ChatGroq(model="llama-3.3-70b-versatile")
llm_with_tools = llm.bind_tools([calculate_emi, get_exchange_rate])
print("Tools bound to LLM!")

# ============================================================
# Step 3: LLM generates a tool call
# ============================================================
# When the LLM decides a tool is needed, it returns a structured
# tool_calls list instead of (or alongside) text content.

print("\n--- Step 3: LLM Generates a Tool Call ---")
response = llm_with_tools.invoke("What's the EMI for a Rs 50 lakh home loan at 8.5% for 20 years?")

print(f"Content:    '{response.content}'")
print(f"Tool calls: {response.tool_calls}")

if response.tool_calls:
    tc = response.tool_calls[0]
    print(f"\n  Tool name: {tc['name']}")
    print(f"  Arguments: {tc['args']}")
    print(f"  Call ID:   {tc['id']}")

# ============================================================
# Step 4: Execute the tool call manually
# ============================================================
# Unlike an agent, bind_tools() does NOT execute the tool.
# YOU must execute it and send the result back.

print("\n--- Step 4: Execute the Tool Call ---")
tools_map = {"calculate_emi": calculate_emi, "get_exchange_rate": get_exchange_rate}

if response.tool_calls:
    tc = response.tool_calls[0]
    tool_result = tools_map[tc["name"]].invoke(tc["args"])
    print(f"Tool result: {tool_result}")

    # ============================================================
    # Step 5: Send result back to LLM for final answer
    # ============================================================
    # The full cycle: Human → AI (tool call) → Tool result → AI (answer)
    # We use ToolMessage to send the tool output back.

    print("\n--- Step 5: LLM Generates Final Answer ---")
    messages = [
        HumanMessage(content="What's the EMI for a Rs 50 lakh home loan at 8.5% for 20 years?"),
        response,  # The AI message with tool_calls
        ToolMessage(content=tool_result, tool_call_id=tc["id"]),
    ]
    final = llm_with_tools.invoke(messages)
    print(f"Final answer: {final.content}")

# ============================================================
# Step 6: Compare — with vs without tools
# ============================================================

print("\n--- Step 6: Same Question Without Tools ---")
raw_response = llm.invoke("What's the EMI for a Rs 50 lakh home loan at 8.5% for 20 years?")
print(f"Without tools: {raw_response.content[:200]}...")
print("\n(The bound-tools version is structured and uses the actual formula!)")

# ============================================================
# TODO 1: Exchange rate tool call
# ============================================================
# Ask llm_with_tools about exchange rates:
# "How many rupees is 500 USD?"
# Print the tool_calls to see which tool the LLM chooses
# and what arguments it passes.

# response = llm_with_tools.invoke("How many rupees is 500 USD?")
# print(f"\nTool calls: {response.tool_calls}")

# ============================================================
# TODO 2: Complete the full cycle
# ============================================================
# For your exchange rate question above, complete the full cycle:
# 1. Get the tool call from the LLM
# 2. Execute the tool using tools_map
# 3. Send the result back as a ToolMessage
# 4. Print the final answer

# if response.tool_calls:
#     tc = response.tool_calls[0]
#     result = tools_map[tc["name"]].invoke(tc["args"])
#     messages = [
#         HumanMessage(content="How many rupees is 500 USD?"),
#         response,
#         ToolMessage(content=result, tool_call_id=tc["id"]),
#     ]
#     final = llm_with_tools.invoke(messages)
#     print(f"Final answer: {final.content}")

print("\n" + "=" * 50)
print("Lab 03 complete! Key takeaways:")
print("- bind_tools() teaches the LLM what tools exist")
print("- The LLM returns structured tool_calls (name + args + id)")
print("- YOU execute the tool and return results via ToolMessage")
print("- create_react_agent (Lab 02) automates this entire loop")
print("- Manual approach gives you full control over tool execution")
