"""
Lab 05: The Four Building Blocks of an Agent
==============================================
Goal: Experience each of the four agent components hands-on.

What you'll learn:
- Brain (LLM): understands and generates language
- Memory: remembers previous messages
- Tools: takes actions in the real world
- Planning: breaks a big task into steps

Each section demonstrates one building block in action.
"""

from datetime import datetime
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

llm = ChatOllama(model="llama3.2:1b")

# ============================================================
# Building Block 1: THE BRAIN (LLM)
# ============================================================

print("=" * 50)
print("BLOCK 1: The Brain (LLM)")
print("=" * 50)

# The LLM understands language and reasons about it.
response = llm.invoke([
    SystemMessage(content="You are a helpful assistant. Be concise."),
    HumanMessage(content="A customer says: 'I ordered a laptop but received a phone.' What category is this complaint? What should we do?"),
])
print(f"Customer Complaint Analysis:\n{response.content}")
print("\n>>> The Brain understands the problem and reasons about a solution.")
print(">>> But it can't actually look up the order or process a return.\n")

# ============================================================
# Building Block 2: MEMORY
# ============================================================

print("=" * 50)
print("BLOCK 2: Memory")
print("=" * 50)

# WITHOUT memory — each call forgets the previous one
print("--- Without Memory ---")
llm.invoke("I'm planning a trip to Japan in March.")
response = llm.invoke("What should I pack?")
print(f"Q: 'What should I pack?' (after saying Japan in March)")
print(f"A: {response.content}")
print(">>> Without memory, the AI doesn't know WHERE or WHEN!\n")

# WITH memory — we keep conversation history
print("--- With Memory ---")
history = [
    SystemMessage(content="You are a travel assistant. Be concise."),
    HumanMessage(content="I'm planning a trip to Japan in March."),
]
r1 = llm.invoke(history)
history.append(AIMessage(content=r1.content))

history.append(HumanMessage(content="What should I pack?"))
r2 = llm.invoke(history)
print(f"Q: 'What should I pack?' (with conversation history)")
print(f"A: {r2.content}")
print(">>> With memory, the AI remembers Japan + March!\n")

# ============================================================
# Building Block 3: TOOLS
# ============================================================

print("=" * 50)
print("BLOCK 3: Tools")
print("=" * 50)

# Define some tools
def get_order_status(order_id: str) -> str:
    """Simulated database lookup."""
    orders = {
        "ORD-001": "Shipped — arriving tomorrow",
        "ORD-002": "Processing — expected dispatch in 2 days",
        "ORD-003": "Delivered — signed by reception",
    }
    return orders.get(order_id, "Order not found")


def send_notification(message: str) -> str:
    """Simulated notification sender."""
    print(f"    [NOTIFICATION SENT]: {message}")
    return "Notification sent successfully"


# Without tools — the LLM can only guess
print("--- Without Tools ---")
response = llm.invoke("What is the status of order ORD-001?")
print(f"Q: Status of order ORD-001?")
print(f"A: {response.content}\n")
print(">>> Without tools, the AI can't look up real order data.\n")

# With tools — the agent fetches real data
print("--- With Tools ---")
order_status = get_order_status("ORD-001")
response = llm.invoke([
    SystemMessage(content="You are a customer support agent. Use the order data provided to help the customer."),
    HumanMessage(content=f"Order ORD-001 status: {order_status}\n\nCustomer asks: What is the status of my order ORD-001?"),
])
print(f"Q: Status of order ORD-001?")
print(f"A: {response.content}")
send_notification("Your order ORD-001 is shipped and arriving tomorrow!")
print(">>> With tools, the agent fetches real data AND takes action!\n")

# ============================================================
# Building Block 4: PLANNING
# ============================================================

print("=" * 50)
print("BLOCK 4: Planning")
print("=" * 50)

# Ask the LLM to create a plan (task decomposition)
response = llm.invoke([
    SystemMessage(content="""You are a planning assistant. When given a complex task,
break it into numbered steps. For each step, mention which tool would be needed.
Available tools: web_search, calculator, email_sender, calendar, file_writer."""),
    HumanMessage(content="Help me organize a team dinner for 8 people this Friday evening in Bangalore."),
])
print(f"Task: Organize a team dinner")
print(f"Plan:\n{response.content}\n")

print(">>> Planning breaks a complex goal into actionable steps.")
print(">>> Each step uses a specific tool. The agent executes them in order.\n")

# ============================================================
# All Four Together!
# ============================================================

print("=" * 50)
print("ALL FOUR BLOCKS WORKING TOGETHER")
print("=" * 50)

print("""
Imagine: "Check my order ORD-002 and send me an update"

1. BRAIN understands the request
   → "Customer wants order status + notification"

2. PLANNING breaks it into steps
   → Step 1: Look up order
   → Step 2: Send notification

3. TOOLS execute each step""")

status = get_order_status("ORD-002")
print(f"   → get_order_status('ORD-002') = '{status}'")
send_notification(f"Order ORD-002 update: {status}")

print("""
4. MEMORY remembers for next time
   → "Last time customer asked about ORD-002"

This is an AI AGENT — all four blocks working as one system!
""")

# ============================================================
# TODO 1: Add a new tool
# ============================================================
# Create a tool called `get_product_info(product_id)` that returns
# product details (name, price, category). Use it to answer:
# "Tell me about product PROD-101"
#
# def get_product_info(product_id):
#     products = {
#         "PROD-101": "Laptop, Rs 65,000, Electronics",
#         "PROD-102": "Headphones, Rs 2,500, Electronics",
#     }
#     return products.get(product_id, "Product not found")

# TODO: Build and test it

# ============================================================
# TODO 2: Multi-block scenario
# ============================================================
# Build a mini-scenario that uses all four blocks:
# Task: "I ordered PROD-101 yesterday. Where is it?"
# Brain: Understands the question
# Memory: Knows the customer mentioned PROD-101
# Tools: Looks up order status + product info
# Planning: Step 1 → lookup, Step 2 → compose answer

# TODO: Implement the full scenario

print("=" * 50)
print("Lab 05 complete!")
print()
print("Key takeaways:")
print("- Brain (LLM): Understands and reasons")
print("- Memory: Maintains context across messages")
print("- Tools: Bridges the gap to the real world")
print("- Planning: Breaks complex tasks into steps")
print("- Agent = Brain + Memory + Tools + Planning")
