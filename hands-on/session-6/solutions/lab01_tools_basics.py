"""
Lab 01: Creating Tools — SOLUTION
"""

from langchain_core.tools import tool

print("=" * 50)
print("  Creating Tools — SOLUTION")
print("=" * 50)

# Step 1: Your first tool
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers together."""
    return a * b

print("\n--- Step 1: Your First Tool ---")
print(f"Tool name:        {multiply.name}")
print(f"Tool description: {multiply.description}")
print(f"Tool arguments:   {multiply.args}")

# Step 2: Call it directly
result = multiply.invoke({"a": 6, "b": 7})
print(f"\n--- Step 2: Direct Invocation ---")
print(f"multiply(6, 7) = {result}")

# Step 3: A realistic tool
@tool
def get_office_info(city: str) -> str:
    """Get UniGPS office details for a given city. Returns address, team size, and facilities."""
    offices = {
        "bangalore": "WeWork Embassy Tech Village, 5th Floor. 200+ employees. HQ — all departments.",
        "mumbai": "Worli Business District, Tower A, 12th Floor. 50 employees. Sales & marketing.",
        "hyderabad": "HITEC City, Cyber Gateway, 8th Floor. 80 employees. Engineering hub.",
        "pune": "Hinjewadi Phase 2, Building C, 4th Floor. 40 employees. QA & DevOps.",
    }
    return offices.get(city.lower(), f"No office found in {city}.")

print(f"\n--- Step 3: Realistic Tool ---")
print(f"Tool name: {get_office_info.name}")
print(f"Tool desc: {get_office_info.description}")
print(f"Tool args: {get_office_info.args}")
print(f"\nResult: {get_office_info.invoke({'city': 'Bangalore'})}")
print(f"Result: {get_office_info.invoke({'city': 'Chennai'})}")

# Step 4: Why docstrings matter
@tool
def bad_tool(x):
    """Do something."""
    return x * 2

@tool
def good_tool(number: float) -> float:
    """Double a number. Use this when you need to multiply any number by 2."""
    return number * 2

print(f"\n--- Step 4: Why Docstrings Matter ---")
print(f"Bad tool:  name='{bad_tool.name}', desc='{bad_tool.description}'")
print(f"           args={bad_tool.args}")
print(f"Good tool: name='{good_tool.name}', desc='{good_tool.description}'")
print(f"           args={good_tool.args}")
print("\nAgents read the description to decide WHICH tool to use!")

# Step 5: Tool with multiple parameters
@tool
def calculate_leave_balance(total_days: int, days_used: int, month: int) -> str:
    """Calculate remaining leave balance for a UniGPS employee.

    Args:
        total_days: Total annual leave allocation
        days_used: Days already taken this year
        month: Current month (1-12) for prorated calculation
    """
    remaining = total_days - days_used
    prorated = round(total_days * month / 12, 1)
    return (f"Used: {days_used}/{total_days} days. "
            f"Remaining: {remaining}. "
            f"Prorated allowance by month {month}: {prorated} days.")

print(f"\n--- Step 5: Multi-Parameter Tool ---")
print(f"Args schema: {calculate_leave_balance.args}")
print(calculate_leave_balance.invoke({"total_days": 24, "days_used": 8, "month": 6}))

# TODO 1: Currency converter tool
@tool
def convert_inr_to_usd(amount_inr: float) -> str:
    """Convert Indian Rupees (INR) to US Dollars (USD) using a fixed exchange rate of 1 USD = 83 INR."""
    usd = amount_inr / 83
    return f"Rs {amount_inr:,.0f} = ${usd:,.2f} USD (rate: 1 USD = Rs 83)"

print(f"\n--- TODO 1: Currency Converter ---")
print(f"Tool: {convert_inr_to_usd.name}")
print(f"Desc: {convert_inr_to_usd.description}")
print(convert_inr_to_usd.invoke({"amount_inr": 10000}))
print(convert_inr_to_usd.invoke({"amount_inr": 50000}))

# TODO 2: Tech recommendation tool
@tool
def get_tech_recommendation(project_type: str) -> str:
    """Get UniGPS recommended technology stack for a project type (backend, frontend, database, infra)."""
    recommendations = {
        "backend": "Python with FastAPI (default) or Java with Spring Boot",
        "frontend": "React with TypeScript (new projects) or Angular (existing apps)",
        "database": "PostgreSQL (relational) or MongoDB (document store)",
        "infra": "AWS EKS (Kubernetes) with Terraform and GitHub Actions CI/CD",
    }
    rec = recommendations.get(project_type.lower())
    if rec:
        return f"UniGPS {project_type.title()} Recommendation: {rec}"
    return f"Unknown project type: '{project_type}'. Available: {', '.join(recommendations.keys())}"

print(f"\n--- TODO 2: Tech Recommendation ---")
print(f"Tool: {get_tech_recommendation.name}")
print(get_tech_recommendation.invoke({"project_type": "backend"}))
print(get_tech_recommendation.invoke({"project_type": "frontend"}))
print(get_tech_recommendation.invoke({"project_type": "devops"}))

print("\n" + "=" * 50)
print("Lab 01 complete! Key takeaways:")
print("- @tool decorator turns functions into agent-compatible tools")
print("- Tools have: name, description, args (auto-generated from function)")
print("- Docstrings are critical — agents read them to pick tools")
print("- Type hints define the input schema for the agent")
print("- .invoke() lets you test tools directly before connecting to agents")
