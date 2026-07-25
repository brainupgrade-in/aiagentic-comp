#!/usr/bin/env bash
# setup.sh — One-time environment setup for the FULL 5-day Agentic AI course.
#
# Works on Linux, macOS, and Windows Git Bash. Idempotent: safe to re-run on any
# day. Installs everything all five days need, so there are no per-day setup
# scripts.
#
# Usage (from repo root):
#   bash scripts/setup.sh                  # full setup
#   source scripts/setup.sh                # same, and leaves the venv active
#   bash scripts/setup.sh --verify         # check the environment, install nothing
#   bash scripts/setup.sh --skip-ollama    # skip Ollama + llama3.2:1b (Day 1 local LLM)
#   bash scripts/setup.sh --kernel-only    # re-register the kernel + reconfigure notebooks
#
# Windows participants: run scripts/bootstrap.ps1 in PowerShell instead — it
# installs Git Bash + uv + Ollama and then calls this script.

# Use return when sourced, exit when run directly
_exit_or_return() { local code=${1:-1}; [[ "${BASH_SOURCE[0]}" != "${0}" ]] && return "$code" || exit "$code"; }

set -e

PY_VERSION="3.12"
KERNEL_NAME="gheware-agentic-ai"
KERNEL_DISPLAY="Python 3 (Gheware Agentic AI)"
OLLAMA_MODEL="llama3.2:1b"

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

MODE="full"
SKIP_OLLAMA=0
for arg in "$@"; do
    case "$arg" in
        --verify)      MODE="verify" ;;
        --kernel-only) MODE="kernel" ;;
        --skip-ollama) SKIP_OLLAMA=1 ;;
        -h|--help)     awk 'NR>1 { if ($0 !~ /^#/) exit; sub(/^# ?/, ""); print }' "${BASH_SOURCE[0]}"; _exit_or_return 0 ;;
        *) echo "Unknown option: $arg (try --help)"; _exit_or_return 1 ;;
    esac
done

# ── Platform detection ────────────────────────────────────────────────────────
case "$(uname -s)" in
    Linux*)               OS="linux" ;;
    Darwin*)              OS="mac" ;;
    MINGW*|MSYS*|CYGWIN*) OS="windows" ;;
    *)                    OS="unknown" ;;
esac

if [ "$OS" = "windows" ]; then
    VENV_BIN="$REPO_DIR/.venv/Scripts"
    VENV_PY="$VENV_BIN/python.exe"
else
    VENV_BIN="$REPO_DIR/.venv/bin"
    VENV_PY="$VENV_BIN/python"
fi
VENV_ACTIVATE="$VENV_BIN/activate"

ok()   { echo "  [OK]   $*"; }
warn() { echo "  [WARN] $*"; }
err()  { echo "  [FAIL] $*"; }
step() { echo ""; echo "$*"; }

banner() {
    echo "============================================"
    echo "  Agentic AI Course — $1"
    echo "  Platform: $OS"
    echo "============================================"
}

# ── Verify mode: report only, change nothing ──────────────────────────────────
if [ "$MODE" = "verify" ]; then
    banner "Environment Check"
    FAILED=0

    step "Python virtual environment"
    if [ -x "$VENV_PY" ]; then
        ok "$("$VENV_PY" --version) at .venv"
    else
        err ".venv not found — run: bash scripts/setup.sh"
        FAILED=1
    fi

    if [ -x "$VENV_PY" ]; then
        step "Packages (all 5 days)"
        "$VENV_PY" - <<'PYEOF' || FAILED=1
import importlib.metadata as md
import sys

# module name -> distribution name, grouped by the day that first needs it
PKGS = [
    ("Day 1", "langchain_ollama",    "langchain-ollama"),
    ("Day 2", "langchain",           "langchain"),
    ("Day 2", "langchain_groq",      "langchain-groq"),
    ("Day 2", "langchain_chroma",    "langchain-chroma"),
    ("Day 2", "chromadb",            "chromadb"),
    ("Day 2", "sentence_transformers", "sentence-transformers"),
    ("Day 3", "langgraph",           "langgraph"),
    ("Day 4", "fastapi",             "fastapi"),
    ("Day 4", "uvicorn",             "uvicorn"),
    ("Day 4", "opentelemetry.sdk",   "opentelemetry-sdk"),
    ("Day 4", "langfuse",            "langfuse"),
    ("Day 5", "mcp",                 "mcp"),
    ("All",   "ipykernel",           "ipykernel"),
]
missing = []
for day, module, dist in PKGS:
    try:
        version = md.version(dist)
        print(f"  [OK]   {day:<6} {dist} {version}")
    except md.PackageNotFoundError:
        print(f"  [FAIL] {day:<6} {dist} NOT INSTALLED")
        missing.append(dist)
if missing:
    print(f"\n  {len(missing)} package(s) missing — run: bash scripts/setup.sh")
    sys.exit(1)
PYEOF

        step "Jupyter kernel"
        if "$VENV_PY" -m jupyter kernelspec list 2>/dev/null | grep -q "$KERNEL_NAME"; then
            ok "kernel '$KERNEL_NAME' registered"
        else
            warn "kernel '$KERNEL_NAME' not registered — run: bash scripts/setup.sh --kernel-only"
        fi
    fi

    step "API keys (.env)"
    if [ -f "$REPO_DIR/.env" ]; then
        # shellcheck disable=SC1090
        set +e; . "$REPO_DIR/.env" 2>/dev/null; set -e
        [ -n "$GROQ_API_KEY" ] && [ "$GROQ_API_KEY" != "gsk_your_key_here" ] \
            && ok "GROQ_API_KEY set (Days 2-5)" \
            || warn "GROQ_API_KEY not set — get one free at https://console.groq.com"
        [ -n "$GITHUB_TOKEN" ] && [ "$GITHUB_TOKEN" != "ghp_your_lab_submit_token_here" ] \
            && ok "GITHUB_TOKEN set (lab submission)" \
            || warn "GITHUB_TOKEN not set — needed by scripts/submit-lab.sh"
    else
        warn ".env not found — copy it: cp .env.example .env"
    fi

    step "Day 1 local LLM"
    if command -v ollama &>/dev/null; then
        ollama list 2>/dev/null | grep -q "${OLLAMA_MODEL%%:*}" \
            && ok "Ollama + $OLLAMA_MODEL available" \
            || warn "Ollama installed but $OLLAMA_MODEL not pulled — run: ollama pull $OLLAMA_MODEL"
    else
        warn "Ollama not installed (Day 1 only) — run: bash scripts/setup.sh"
    fi

    echo ""
    echo "============================================"
    [ "$FAILED" -eq 0 ] && echo "  Environment OK" || echo "  Environment INCOMPLETE — see [FAIL] above"
    echo "============================================"
    echo ""
    _exit_or_return "$FAILED"
fi

# ── Kernel-only mode ──────────────────────────────────────────────────────────
if [ "$MODE" = "kernel" ]; then
    banner "Kernel Repair"
    if [ ! -x "$VENV_PY" ]; then
        err ".venv not found — run the full setup first: bash scripts/setup.sh"
        _exit_or_return 1
    fi
    step "Registering Jupyter kernel '$KERNEL_NAME'..."
    "$VENV_PY" -m pip install --quiet ipykernel
    "$VENV_PY" -m ipykernel install --user --name "$KERNEL_NAME" --display-name "$KERNEL_DISPLAY"
    ok "kernel registered"
    step "Pointing every notebook at it..."
    "$VENV_PY" "$REPO_DIR/scripts/configure-notebooks.py"
    echo ""
    echo "Done. Reload VS Code so it picks up the kernel."
    echo ""
    _exit_or_return 0
fi

# ── Full setup ────────────────────────────────────────────────────────────────
banner "One-Time Setup (all 5 days)"

# [1/7] uv — installs and manages Python itself, plus fast package installs
step "[1/7] Checking uv..."
if command -v uv &>/dev/null; then
    ok "$(uv --version)"
else
    if [ "$OS" = "windows" ]; then
        err "uv not found on Windows."
        echo "       Run scripts/bootstrap.ps1 from PowerShell first — it installs"
        echo "       Git Bash, uv and Ollama, then re-runs this script."
        _exit_or_return 1
    fi
    echo "  Installing uv..."
    curl -fsSL https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
    command -v uv &>/dev/null || {
        err "uv installed but not on PATH. Open a new terminal and re-run this script."
        _exit_or_return 1
    }
    ok "$(uv --version)"
fi

# [2/7] Python 3.12 — uv downloads a private build, no sudo, no PPA
step "[2/7] Ensuring Python $PY_VERSION..."
uv python install "$PY_VERSION"
ok "Python $PY_VERSION available"

# [3/7] Virtual environment
step "[3/7] Creating .venv..."
if [ -x "$VENV_PY" ] && "$VENV_PY" -c "import sys; sys.exit(0 if sys.version_info[:2]==(3,${PY_VERSION#3.}) else 1)" 2>/dev/null; then
    ok "existing .venv is $("$VENV_PY" --version)"
else
    [ -e "$REPO_DIR/.venv" ] && { echo "  Replacing .venv (wrong Python version)"; rm -rf "$REPO_DIR/.venv"; }
    uv venv --python "$PY_VERSION" "$REPO_DIR/.venv"
    ok "created .venv with $("$VENV_PY" --version)"
fi

# [4/7] Packages for all five days
step "[4/7] Installing packages for all 5 days (a few minutes)..."
# CPU-only PyTorch first, so sentence-transformers does not drag in multi-GB CUDA wheels
uv pip install --python "$VENV_PY" torch --index-url https://download.pytorch.org/whl/cpu --quiet
uv pip install --python "$VENV_PY" -r "$REPO_DIR/requirements.txt"
ok "all packages installed"

# [5/7] .env
step "[5/7] Setting up .env..."
if [ -f "$REPO_DIR/.env" ]; then
    ok ".env already exists (left untouched)"
else
    cp "$REPO_DIR/.env.example" "$REPO_DIR/.env"
    ok "created .env from .env.example"
    warn "edit .env and add GROQ_API_KEY (free at https://console.groq.com)"
fi

# [6/7] Jupyter kernel + notebook wiring
step "[6/7] Registering Jupyter kernel and configuring notebooks..."
if command -v code &>/dev/null; then
    code --install-extension ms-toolsai.jupyter --force &>/dev/null \
        && ok "VS Code Jupyter extension installed" \
        || warn "could not install the Jupyter extension — add ms-toolsai.jupyter manually"
else
    warn "'code' CLI not found — install the Jupyter extension manually in VS Code"
fi
"$VENV_PY" -m ipykernel install --user --name "$KERNEL_NAME" --display-name "$KERNEL_DISPLAY"
ok "kernel '$KERNEL_NAME' registered"
"$VENV_PY" "$REPO_DIR/scripts/configure-notebooks.py"

# [7/7] Day 1 extras: Ollama local LLM + OpenCode vibe-coding CLI
step "[7/7] Day 1 tooling (Ollama + OpenCode)..."
if [ "$SKIP_OLLAMA" -eq 1 ]; then
    warn "skipping Ollama (--skip-ollama). Day 1 labs need it: bash scripts/setup.sh"
else
    if command -v ollama &>/dev/null; then
        ok "Ollama already installed"
    else
        case "$OS" in
            linux)
                curl -fsSL https://ollama.com/install.sh | sh ;;
            mac)
                if command -v brew &>/dev/null; then
                    brew install ollama
                else
                    warn "Homebrew not found — install Ollama from https://ollama.com/download"
                fi ;;
            windows)
                warn "Ollama missing — run scripts/bootstrap.ps1, or install from https://ollama.com/download" ;;
        esac
    fi

    if command -v ollama &>/dev/null; then
        # Make sure a server is listening before pulling
        curl -sf http://localhost:11434/ &>/dev/null || { ollama serve &>/dev/null & sleep 3; }
        echo "  Pulling $OLLAMA_MODEL (~1.3 GB)..."
        ollama pull "$OLLAMA_MODEL"
        ok "$OLLAMA_MODEL ready"
    fi
fi

# OpenCode is optional Day 1 vibe-coding tooling — never fail setup over it
if command -v opencode &>/dev/null; then
    ok "OpenCode already installed"
else
    OC_INSTALLER="$(mktemp)"
    if curl -fsSL https://opencode.ai/install -o "$OC_INSTALLER" 2>/dev/null && [ -s "$OC_INSTALLER" ]; then
        bash "$OC_INSTALLER" &>/dev/null || true
        export PATH="$HOME/.local/bin:$PATH"
        command -v opencode &>/dev/null \
            && ok "OpenCode installed (auth: run 'opencode' then /connect, or set GROQ_API_KEY)" \
            || warn "OpenCode installed but not on PATH — add \$HOME/.local/bin, or see https://opencode.ai"
    else
        warn "OpenCode download failed — optional, install later from https://opencode.ai"
    fi
    rm -f "$OC_INSTALLER"
fi

# ── Summary ───────────────────────────────────────────────────────────────────
echo ""
echo "============================================"
echo "  Setup complete — all 5 days ready"
echo "============================================"
echo ""
echo "No per-day setup scripts: this covered Days 1-5."
echo ""
echo "Next steps:"
echo "  1. Add your Groq API key to .env:"
echo "       GROQ_API_KEY=gsk_your_key_here"
echo "  2. Open the first lab — the kernel auto-selects:"
echo "       code hands-on/session-1/lab01_meet_your_llm.ipynb"
echo ""
echo "Anytime:"
echo "  bash scripts/setup.sh --verify     check the environment"
echo "  bash scripts/check-resources.sh    memory / storage / processes"
echo "  bash scripts/cleanup.sh <day>      end-of-day cleanup (1-5, or all)"
echo "  bash scripts/langfuse-server.sh start   Day 4 Session 12 Lab 09"
echo ""

if [[ "${BASH_SOURCE[0]}" != "${0}" ]]; then
    # shellcheck disable=SC1090
    . "$VENV_ACTIVATE"
    echo "Virtual environment activated in this shell: $(python --version)"
else
    echo "Activate the virtual environment in this terminal:"
    echo "  source $VENV_ACTIVATE"
fi
echo ""
