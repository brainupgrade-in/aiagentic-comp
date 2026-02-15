#!/bin/bash
#
# Install Jupyter kernel spec for Oracle Agentic AI course
# This creates a kernel that VS Code and Jupyter can discover
#

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Installing Jupyter kernel spec for Gheware Agentic AI course...${NC}"

# Get the project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
VENV_PYTHON="$PROJECT_ROOT/.venv/bin/python"

# Check if virtual environment exists
if [ ! -f "$VENV_PYTHON" ]; then
    echo -e "${YELLOW}Warning: Python virtual environment not found at $VENV_PYTHON${NC}"
    echo "Creating virtual environment..."
    cd "$PROJECT_ROOT"
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install ipykernel jupyter
else
    echo "Found Python virtual environment at $VENV_PYTHON"
fi

# Install ipykernel if not already installed
echo "Ensuring ipykernel is installed..."
"$VENV_PYTHON" -m pip install ipykernel jupyter --quiet

# Install the kernel spec
echo "Installing kernel spec..."
"$VENV_PYTHON" -m ipykernel install \
    --user \
    --name gheware-agentic-ai \
    --display-name "Python 3 (Gheware Agentic AI)"

echo -e "${GREEN}✓ Kernel spec installed successfully${NC}"

# Verify installation
echo ""
echo "Installed kernels:"
jupyter kernelspec list

echo ""
echo -e "${GREEN}Done! You can now select 'Python 3 (Gheware Agentic AI)' as the kernel in VS Code or Jupyter.${NC}"
