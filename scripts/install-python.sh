#!/bin/bash
# install-python.sh — Install Python 3.12 on Linux, macOS, or Windows Git Bash
#
# Usage:
#   bash scripts/install-python.sh
#
# Supports:
#   Linux   — apt (Ubuntu/Debian) or dnf (Fedora/RHEL)
#   macOS   — Homebrew (installs brew if missing)
#   Windows — winget (Windows 10/11) or manual download prompt

set -e

TARGET_VERSION="3.12"
TARGET_MINOR=12   # exact version supported by this course

BOLD="\033[1m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
RESET="\033[0m"

info()    { echo -e "${GREEN}[INFO]${RESET}  $*"; }
warn()    { echo -e "${YELLOW}[WARN]${RESET}  $*"; }
error()   { echo -e "${RED}[ERROR]${RESET} $*"; }
heading() { echo -e "\n${BOLD}$*${RESET}"; }

# ── Detect OS ─────────────────────────────────────────────────────────────────
detect_os() {
    case "$(uname -s)" in
        Linux*)   echo "linux" ;;
        Darwin*)  echo "mac" ;;
        MINGW*|MSYS*|CYGWIN*) echo "windows" ;;
        *)        echo "unknown" ;;
    esac
}

# ── Check existing Python ──────────────────────────────────────────────────────
check_python() {
    for cmd in python3.12 python3 python; do
        if command -v "$cmd" &>/dev/null; then
            local minor
            minor=$("$cmd" -c "import sys; print(sys.version_info.minor)" 2>/dev/null || echo "0")
            local major
            major=$("$cmd" -c "import sys; print(sys.version_info.major)" 2>/dev/null || echo "0")
            if [ "$major" -eq 3 ] && [ "$minor" -eq "$TARGET_MINOR" ]; then
                echo "$cmd"
                return 0
            fi
        fi
    done
    return 1
}

check_python_wrong_version() {
    for cmd in python3 python; do
        if command -v "$cmd" &>/dev/null; then
            local minor
            minor=$("$cmd" -c "import sys; print(sys.version_info.minor)" 2>/dev/null || echo "0")
            local major
            major=$("$cmd" -c "import sys; print(sys.version_info.major)" 2>/dev/null || echo "0")
            if [ "$major" -eq 3 ] && [ "$minor" -ne "$TARGET_MINOR" ]; then
                echo "$("$cmd" --version)"
                return 0
            fi
        fi
    done
    return 1
}

# ── Linux ──────────────────────────────────────────────────────────────────────
install_linux() {
    if command -v apt-get &>/dev/null; then
        info "Detected apt (Ubuntu/Debian)"
        info "Adding deadsnakes PPA for Python ${TARGET_VERSION}..."
        sudo apt-get update -qq
        sudo apt-get install -y software-properties-common
        sudo add-apt-repository -y ppa:deadsnakes/ppa
        sudo apt-get update -qq
        sudo apt-get install -y "python${TARGET_VERSION}" "python${TARGET_VERSION}-venv" "python${TARGET_VERSION}-dev"
        # Make python3 point to 3.12 if not already
        if ! python3 --version 2>/dev/null | grep -q "3\.12"; then
            sudo update-alternatives --install /usr/bin/python3 python3 "/usr/bin/python${TARGET_VERSION}" 1 || true
        fi
    elif command -v dnf &>/dev/null; then
        info "Detected dnf (Fedora/RHEL)"
        sudo dnf install -y "python${TARGET_VERSION}" || sudo dnf install -y python3
    elif command -v yum &>/dev/null; then
        info "Detected yum (CentOS/RHEL)"
        sudo yum install -y python3
    else
        error "Unsupported Linux distribution — install Python ${TARGET_VERSION} manually from https://python.org"
        exit 1
    fi
}

# ── macOS ──────────────────────────────────────────────────────────────────────
install_mac() {
    if ! command -v brew &>/dev/null; then
        warn "Homebrew not found — installing Homebrew first..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        # Add brew to PATH for Apple Silicon
        if [ -f "/opt/homebrew/bin/brew" ]; then
            eval "$(/opt/homebrew/bin/brew shellenv)"
        fi
    fi
    info "Installing Python ${TARGET_VERSION} via Homebrew..."
    brew install "python@${TARGET_VERSION}"
    brew link --force "python@${TARGET_VERSION}" || true
}

# ── Windows Git Bash ───────────────────────────────────────────────────────────
install_windows() {
    if command -v winget &>/dev/null; then
        info "Installing Python ${TARGET_VERSION} via winget..."
        winget install --id Python.Python.3.12 --source winget --accept-package-agreements --accept-source-agreements
        warn "Restart Git Bash after installation so PATH updates take effect."
    elif command -v choco &>/dev/null; then
        info "Installing Python ${TARGET_VERSION} via Chocolatey..."
        choco install python312 -y
        warn "Restart Git Bash after installation so PATH updates take effect."
    else
        error "Neither winget nor Chocolatey found."
        echo ""
        echo "  Install Python ${TARGET_VERSION} manually:"
        echo "  1. Download: https://www.python.org/downloads/release/python-3120/"
        echo "  2. Run installer — check 'Add Python to PATH'"
        echo "  3. Restart Git Bash"
        echo ""
        exit 1
    fi
}

# ── Main ───────────────────────────────────────────────────────────────────────
heading "Python Installation Check"
echo "  Required version: Python ${TARGET_VERSION} (exact)"
echo ""

OS=$(detect_os)
info "Detected OS: $OS"

if WRONG_VER=$(check_python_wrong_version); then
    warn "Found $WRONG_VER — this course requires Python ${TARGET_VERSION} exactly."
    warn "Installing Python ${TARGET_VERSION} alongside it..."
    echo ""
    case "$OS" in
        linux)   install_linux ;;
        mac)     install_mac ;;
        windows) install_windows ;;
        *)
            error "Unknown OS — install Python ${TARGET_VERSION} manually from https://python.org"
            exit 1
            ;;
    esac
fi

if PYTHON_CMD=$(check_python); then
    VER=$("$PYTHON_CMD" --version)
    info "Python already installed: $VER ($PYTHON_CMD)"
    info "No installation needed."
    echo ""
    echo "  Run next: bash scripts/initial-setup.sh"
    exit 0
fi

warn "Python 3.${MIN_MINOR}+ not found — installing Python ${TARGET_VERSION}..."
echo ""

case "$OS" in
    linux)   install_linux ;;
    mac)     install_mac ;;
    windows) install_windows ;;
    *)
        error "Unknown OS — install Python ${TARGET_VERSION} manually from https://python.org"
        exit 1
        ;;
esac

echo ""
heading "Verifying installation..."
if PYTHON_CMD=$(check_python); then
    VER=$("$PYTHON_CMD" --version)
    info "Success: $VER"
    echo ""
    echo "  Run next: bash scripts/initial-setup.sh"
else
    error "Python ${TARGET_VERSION} installed but not found in PATH."
    echo ""
    echo "  Try: restart your terminal, then run this script again."
    echo "  Or add Python to PATH manually."
    exit 1
fi
