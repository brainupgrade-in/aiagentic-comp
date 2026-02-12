"""
Lab 05: Secrets & Configuration Management
=============================================
Secure API key handling with .env files
and python-dotenv load_dotenv() for application config.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/prod-lab-12-05"

print("=" * 50)
print("  Lab 05: Secrets & Configuration Management")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: Wrong vs Right
# ============================================================

print("\n--- Step 1: Secrets -- Wrong vs Right ---\n")

print("  WRONG (hardcoded in code):")
print('    GROQ_API_KEY = "gsk_abc123..."  # Anyone with code access can see')
print()
print("  WRONG (committed to git):")
print("    # .env checked into version control")
print('    GROQ_API_KEY=gsk_abc123...  # Visible in git history forever')
print()
print("  RIGHT (.env file + .gitignore + load_dotenv()):")
print("    # .env (never committed)")
print("    GROQ_API_KEY=gsk_abc123...")
print("    LANGFUSE_SECRET_KEY=sk-lf-...")
print("    LANGFUSE_PUBLIC_KEY=pk-lf-...")
print()
print("  RIGHT (Python load_dotenv):")
print("    from dotenv import load_dotenv")
print("    load_dotenv()  # reads .env into os.environ")
print("    api_key = os.getenv('GROQ_API_KEY')")


# ============================================================
# Step 2: .env File and Python load_dotenv() Pattern
# ============================================================

print("\n\n--- Step 2: .env File and Python load_dotenv() ---\n")

env_file_content = textwrap.dedent("""\
    # .env - NEVER commit this file to git
    # Add .env to .gitignore

    # LLM API
    GROQ_API_KEY=gsk_abc123...

    # Observability
    LANGFUSE_SECRET_KEY=sk-lf-...
    LANGFUSE_PUBLIC_KEY=pk-lf-...
    LANGFUSE_HOST=http://localhost:8080

    # Application
    APP_ENV=production
    LOG_LEVEL=INFO
""")

print("  .env file:\n")
for line in env_file_content.strip().split("\n"):
    print(f"    {line}")

print("\n  Python load_dotenv() pattern:")

dotenv_code = textwrap.dedent("""\
    import os
    from dotenv import load_dotenv

    # Load .env file into os.environ
    load_dotenv()  # looks for .env in current dir (or specify path)

    # Access variables
    groq_key = os.getenv("GROQ_API_KEY")
    langfuse_secret = os.getenv("LANGFUSE_SECRET_KEY")
    langfuse_public = os.getenv("LANGFUSE_PUBLIC_KEY")
    app_env = os.getenv("APP_ENV", "development")  # default value
    log_level = os.getenv("LOG_LEVEL", "INFO")

    # Validate required keys at startup
    required_keys = ["GROQ_API_KEY", "LANGFUSE_SECRET_KEY", "LANGFUSE_PUBLIC_KEY"]
    missing = [k for k in required_keys if not os.getenv(k)]
    if missing:
        raise RuntimeError(f"Missing required env vars: {missing}")
""")

for line in dotenv_code.strip().split("\n"):
    print(f"    {line}")

with open(os.path.join(WORKDIR, "env-reference.txt"), "w") as f:
    f.write(env_file_content)


# ============================================================
# Step 3: .gitignore and .env.example Pattern
# ============================================================

print("\n\n--- Step 3: .gitignore and .env.example Pattern ---\n")

print("  The standard pattern for secrets in any project:\n")
print("    1. Create .env with real values (local only)")
print("    2. Create .env.example with placeholder values (committed)")
print("    3. Add .env to .gitignore (never committed)")
print()
print("  .gitignore entry:")
print("    .env")
print("    .env.local")
print("    .env.*.local")
print()
print("  .env.example (committed to git):")
print("    GROQ_API_KEY=your_groq_api_key_here")
print("    LANGFUSE_SECRET_KEY=your_langfuse_secret_here")
print("    LANGFUSE_PUBLIC_KEY=your_langfuse_public_here")
print()
print("  Note: .env files store values in plain text.")
print("  They rely on file permissions and .gitignore for protection.")
print("  For production, consider a vault service (HashiCorp Vault, AWS Secrets Manager).")


# ============================================================
# TODO 1: Create .env file and Python dotenv config
# ============================================================

print("\n\n--- TODO 1: Create .env File and Python dotenv Config ---\n")

print("  Create:")
print("    - A .env file with: GROQ_API_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_PUBLIC_KEY")
print("    - A .env.example with placeholder values")
print("    - A .gitignore entry for .env")
print("    - A Python code snippet showing load_dotenv() usage\n")

todo1_env = textwrap.dedent("""\
    # TODO: .env file for API keys + Python load_dotenv() config

""")

with open(os.path.join(WORKDIR, "env-config.txt"), "w") as f:
    f.write(todo1_env)

checks1 = [
    ("Has .env content",           ".env" in todo1_env),
    ("Has GROQ_API_KEY",           "GROQ_API_KEY" in todo1_env),
    ("Has LANGFUSE_SECRET_KEY",    "LANGFUSE_SECRET_KEY" in todo1_env),
    ("Has LANGFUSE_PUBLIC_KEY",    "LANGFUSE_PUBLIC_KEY" in todo1_env),
    ("Has .gitignore mention",     "gitignore" in todo1_env or ".env" in todo1_env),
    ("Has load_dotenv",            "load_dotenv" in todo1_env),
    ("Has .env.example",           "example" in todo1_env or "placeholder" in todo1_env),
    ("Has os.getenv",              "getenv" in todo1_env or "os.environ" in todo1_env),
    ("Has validation",             "required" in todo1_env.lower() or "missing" in todo1_env.lower() or "validate" in todo1_env.lower()),
]

score1 = sum(1 for _, ok in checks1 if ok)
print(f"  Validating ({score1}/{len(checks1)}):\n")
for name, ok in checks1:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: Secrets quiz
# ============================================================

print("\n\n--- TODO 2: Secrets Management Quiz ---\n")

quiz = [
    {
        "question": "Where should API keys be stored for Python applications?",
        "answer": "___",
        "correct": "env",
        "check": "env",
    },
    {
        "question": "What file should NEVER be committed to git?",
        "answer": "___",
        "correct": ".env",
        "check": ".env",
    },
    {
        "question": "What python-dotenv function loads .env variables into os.environ?",
        "answer": "___",
        "correct": "load_dotenv",
        "check": "load_dotenv",
    },
    {
        "question": "What file with placeholder values IS committed to git?",
        "answer": "___",
        "correct": ".env.example",
        "check": "example",
    },
    {
        "question": "What file prevents .env from being tracked by git?",
        "answer": "___",
        "correct": ".gitignore",
        "check": "gitignore",
    },
]

# YOUR CODE HERE: Fill in quiz answers

score2 = 0
for i, q in enumerate(quiz, 1):
    answer = q["answer"].strip().lower().replace(" ", "").replace("-", "").replace("_", "")
    check = q.get("check", q["correct"].lower().replace(" ", "").replace("-", "").replace("_", ""))
    is_correct = check.replace("-", "").replace("_", "").replace(".", "") in answer.replace(".", "") or check in q["answer"].lower()

    if q["answer"] == "___":
        status = "TODO"
    elif is_correct:
        status = "PASS"
        score2 += 1
    else:
        status = "FAIL"
    print(f"    [{status}] Q{i}: {q['question']}")

print(f"\n  Score: {score2}/{len(quiz)}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 05 Summary ---\n")
print("  Key concepts:")
print("    1. Never hardcode API keys -- use .env files")
print("    2. Add .env to .gitignore (never commit secrets)")
print("    3. Provide .env.example with placeholders (committed)")
print("    4. Use python-dotenv load_dotenv() to inject variables")
print("    5. Validate required env vars at startup with os.getenv()")
print(f"\n  TODO 1: {score1}/{len(checks1)} env config checks")
print(f"  TODO 2: {score2}/{len(quiz)} quiz answers correct")
print(f"\n  Files generated in {WORKDIR}/")
