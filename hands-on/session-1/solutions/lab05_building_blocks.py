"""
Lab 05: The Four Building Blocks — SOLUTION
"""

from datetime import datetime
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

llm = ChatOllama(model="llama3.2:1b")

# Block 1: Brain
print("=" * 50)
print("BLOCK 1: The Brain")
print("=" * 50)
response = llm.invoke([
    SystemMessage(content="You are a helpful assistant. Be concise."),
    HumanMessage(content="Customer says: 'I ordered a laptop but received a phone.' What category and what should we do?"),
])
print(f"Analysis:\n{response.content}\n")

# Block 2: Memory
print("=" * 50)
print("BLOCK 2: Memory")
print("=" * 50)
history = [
    SystemMessage(content="You are a travel assistant. Be concise."),
    HumanMessage(content="I'm planning a trip to Japan in March."),
]
r1 = llm.invoke(history)
history.append(AIMessage(content=r1.content))
history.append(HumanMessage(content="What should I pack?"))
r2 = llm.invoke(history)
print(f"With memory: {r2.content}\n")

# Block 3: Tools
print("=" * 50)
print("BLOCK 3: Tools")
print("=" * 50)


def get_order_status(order_id):
    return {"ORD-001": "Shipped — arriving tomorrow",
            "ORD-002": "Processing — 2 days",
            "ORD-003": "Delivered"}.get(order_id, "Not found")


def send_notification(msg):
    print(f"    [NOTIFICATION]: {msg}")
    return "Sent"


def get_product_info(product_id):
    return {"PROD-101": "Laptop, Rs 65,000, Electronics",
            "PROD-102": "Headphones, Rs 2,500, Electronics"}.get(product_id, "Not found")


status = get_order_status("ORD-001")
response = llm.invoke([
    SystemMessage(content="You are a customer support agent. Use the data provided."),
    HumanMessage(content=f"Order ORD-001: {status}\nCustomer: What is my order status?"),
])
print(f"Agent: {response.content}")
send_notification("Your order ORD-001 is shipped, arriving tomorrow!")
print()

# Block 4: Planning
print("=" * 50)
print("BLOCK 4: Planning")
print("=" * 50)
response = llm.invoke([
    SystemMessage(content="""Break the task into numbered steps. For each step, mention the tool needed.
Tools: web_search, calculator, email_sender, calendar, file_writer."""),
    HumanMessage(content="Organize a team dinner for 8 people this Friday in Bangalore."),
])
print(f"Plan:\n{response.content}\n")

# TODO 1: New tool — product info
print("=" * 50)
print("TODO 1: Product Info Tool")
print("=" * 50)
info = get_product_info("PROD-101")
response = llm.invoke([
    SystemMessage(content="You are a customer support agent. Use the data provided."),
    HumanMessage(content=f"Product PROD-101: {info}\nCustomer: Tell me about product PROD-101"),
])
print(f"Agent: {response.content}\n")

# TODO 2: Multi-block scenario
print("=" * 50)
print("TODO 2: Full Agent Scenario")
print("=" * 50)

# Memory — conversation history
memory = [SystemMessage(content="You are a customer support agent. Use all data provided to help.")]

# Turn 1: Customer mentions a product
memory.append(HumanMessage(content="I ordered PROD-101 yesterday. Order number is ORD-002."))
r = llm.invoke(memory)
memory.append(AIMessage(content=r.content))
print(f"Customer: I ordered PROD-101 yesterday. Order ORD-002.")
print(f"Agent: {r.content}\n")

# Turn 2: Asks about status — agent uses tools + memory
prod = get_product_info("PROD-101")
status = get_order_status("ORD-002")
memory.append(HumanMessage(content=f"[Tool: product={prod}, order={status}]\nWhere is my order?"))
r = llm.invoke(memory)
memory.append(AIMessage(content=r.content))
print(f"Customer: Where is my order?")
print(f"Agent: {r.content}")
print(f"(Tools used: product_info → {prod}, order_status → {status})")

print(f"\n[Memory size: {len(memory)} messages]")
print("\nLab 05 complete!")
