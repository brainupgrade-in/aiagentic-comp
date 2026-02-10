"""
Lab 03: Function Calling & Tool Binding — SOLUTION
"""

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage

load_dotenv()

print("=" * 50)
print("  Function Calling & Tool Binding — SOLUTION")
print("=" * 50)

# Step 1: Create tools
@tool
def calculate_emi(principal: float, rate: float, months: int) -> str:
    """Calculate monthly EMI (Equated Monthly Installment) for a loan.

    Args:
        principal: Loan amount in rupees
        rate: Annual interest rate (e.g., 8.5 for 8.5%)
        months: Loan tenure in months
    """
    r = rate / 100 / 12
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

# Step 2: Bind tools to the LLM
llm = ChatGroq(model="llama-3.3-70b-versatile")
llm_with_tools = llm.bind_tools([calculate_emi, get_exchange_rate])
print("Tools bound to LLM!")

# Step 3: LLM generates a tool call
print("\n--- Step 3: LLM Generates a Tool Call ---")
response = llm_with_tools.invoke("What's the EMI for a Rs 50 lakh home loan at 8.5% for 20 years?")

print(f"Content:    '{response.content}'")
print(f"Tool calls: {response.tool_calls}")

if response.tool_calls:
    tc = response.tool_calls[0]
    print(f"\n  Tool name: {tc['name']}")
    print(f"  Arguments: {tc['args']}")
    print(f"  Call ID:   {tc['id']}")

# Step 4: Execute the tool call manually
print("\n--- Step 4: Execute the Tool Call ---")
tools_map = {"calculate_emi": calculate_emi, "get_exchange_rate": get_exchange_rate}

if response.tool_calls:
    tc = response.tool_calls[0]
    tool_result = tools_map[tc["name"]].invoke(tc["args"])
    print(f"Tool result: {tool_result}")

    # Step 5: Send result back to LLM
    print("\n--- Step 5: LLM Generates Final Answer ---")
    messages = [
        HumanMessage(content="What's the EMI for a Rs 50 lakh home loan at 8.5% for 20 years?"),
        response,
        ToolMessage(content=tool_result, tool_call_id=tc["id"]),
    ]
    final = llm_with_tools.invoke(messages)
    print(f"Final answer: {final.content}")

# Step 6: Compare — without tools
print("\n--- Step 6: Same Question Without Tools ---")
raw_response = llm.invoke("What's the EMI for a Rs 50 lakh home loan at 8.5% for 20 years?")
print(f"Without tools: {raw_response.content[:200]}...")

# TODO 1: Exchange rate tool call
print("\n--- TODO 1: Exchange Rate Tool Call ---")
response_fx = llm_with_tools.invoke("How many rupees is 500 USD?")
print(f"Content: '{response_fx.content}'")
print(f"Tool calls: {response_fx.tool_calls}")

# TODO 2: Complete the full cycle
print("\n--- TODO 2: Full Cycle for Exchange Rate ---")
if response_fx.tool_calls:
    tc = response_fx.tool_calls[0]
    print(f"Tool chosen: {tc['name']}({tc['args']})")
    result = tools_map[tc["name"]].invoke(tc["args"])
    print(f"Tool result: {result}")

    messages = [
        HumanMessage(content="How many rupees is 500 USD?"),
        response_fx,
        ToolMessage(content=result, tool_call_id=tc["id"]),
    ]
    final = llm_with_tools.invoke(messages)
    print(f"Final answer: {final.content}")

print("\n" + "=" * 50)
print("Lab 03 complete! Key takeaways:")
print("- bind_tools() teaches the LLM what tools exist")
print("- The LLM returns structured tool_calls (name + args + id)")
print("- YOU execute the tool and return results via ToolMessage")
print("- create_react_agent (Lab 02) automates this entire loop")
print("- Manual approach gives you full control over tool execution")
