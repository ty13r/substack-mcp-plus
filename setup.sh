#!/bin/bash
# Substack MCP Plus - Quick Setup Script
# This script sets up your development environment automatically

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Header
echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}   Substack MCP Plus - Environment Setup${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to get Python command
get_python_cmd() {
    # Check for specific versions first (prefer newer)
    if command_exists python3.12; then
        echo "python3.12"
    elif command_exists python3.11; then
        echo "python3.11"
    elif command_exists python3.10; then
        echo "python3.10"
    elif command_exists python3; then
        echo "python3"
    elif command_exists python; then
        echo "python"
    else
        echo ""
    fi
}

# Step 1: Check Python installation
echo -e "${YELLOW}Step 1: Checking Python installation...${NC}"
PYTHON_CMD=$(get_python_cmd)

if [ -z "$PYTHON_CMD" ]; then
    echo -e "${RED}❌ Python is not installed!${NC}"
    echo "Please install Python 3.8 or higher from https://python.org"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Found Python $PYTHON_VERSION${NC}"

# Check Python version is 3.10+ (required for MCP)
PYTHON_MAJOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info.major)')
PYTHON_MINOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info.minor)')

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
    echo -e "${RED}❌ Python 3.10 or higher is required!${NC}"
    echo -e "${RED}   The MCP package requires Python 3.10+${NC}"
    echo -e ""
    echo -e "${YELLOW}To install Python 3.10+:${NC}"
    echo -e "  macOS: brew install python@3.12"
    echo -e "  Ubuntu: sudo apt install python3.12"
    echo -e "  Or download from https://python.org${NC}"
    exit 1
fi

# Step 2: Create virtual environment
echo ""
echo -e "${YELLOW}Step 2: Setting up virtual environment...${NC}"

if [ -d "venv" ]; then
    echo -e "${BLUE}Virtual environment already exists${NC}"
    # Check if existing venv has correct Python version
    if [ -f "venv/bin/python" ]; then
        VENV_PYTHON_VERSION=$(venv/bin/python --version 2>&1 | awk '{print $2}')
        VENV_MAJOR=$(venv/bin/python -c 'import sys; print(sys.version_info.major)' 2>/dev/null)
        VENV_MINOR=$(venv/bin/python -c 'import sys; print(sys.version_info.minor)' 2>/dev/null)
        
        if [ "$VENV_MAJOR" = "3" ] && [ "$VENV_MINOR" -lt 10 ]; then
            echo -e "${YELLOW}⚠️  Existing venv uses Python $VENV_PYTHON_VERSION (too old)${NC}"
            echo -e "${YELLOW}   Removing old venv and creating new one...${NC}"
            rm -rf venv
            $PYTHON_CMD -m venv venv
            echo -e "${GREEN}✓ Created new virtual environment with Python $PYTHON_VERSION${NC}"
        fi
    fi
else
    $PYTHON_CMD -m venv venv
    echo -e "${GREEN}✓ Created virtual environment with Python $PYTHON_VERSION${NC}"
fi

# Step 3: Activate virtual environment
echo ""
echo -e "${YELLOW}Step 3: Activating virtual environment...${NC}"

# Detect OS for activation script
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source venv/Scripts/activate 2>/dev/null || source venv/Scripts/activate
else
    # macOS/Linux
    source venv/bin/activate
fi

echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Step 4: Upgrade pip
echo ""
echo -e "${YELLOW}Step 4: Upgrading pip...${NC}"
python -m pip install --upgrade pip --quiet
echo -e "${GREEN}✓ Pip upgraded${NC}"

# Step 5: Install dependencies
echo ""
echo -e "${YELLOW}Step 5: Installing dependencies...${NC}"
pip install -e . --quiet
pip install pytest pytest-asyncio pytest-cov pytest-mock --quiet
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Step 6: Create .env file if it doesn't exist
echo ""
echo -e "${YELLOW}Step 6: Setting up environment configuration...${NC}"

if [ -f ".env" ]; then
    echo -e "${BLUE}.env file already exists${NC}"
else
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${GREEN}✓ Created .env file from template${NC}"
        echo -e "${YELLOW}⚠️  Please edit .env with your Substack credentials${NC}"
    else
        echo -e "${RED}❌ .env.example not found${NC}"
    fi
fi

# Step 7: Run tests
echo ""
echo -e "${YELLOW}Step 7: Running tests to verify setup...${NC}"
python -m pytest tests/unit/test_block_builder.py -q

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Basic tests passing${NC}"
else
    echo -e "${RED}❌ Tests failed - please check error messages${NC}"
fi

# Step 8: Create test content directory
echo ""
echo -e "${YELLOW}Step 8: Creating test content directory...${NC}"
mkdir -p test_content
echo -e "${GREEN}✓ Created test_content directory${NC}"

# Summary
echo ""
echo -e "${BLUE}================================================${NC}"
echo -e "${GREEN}✨ Setup Complete!${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""
echo "Next steps:"
echo "1. Edit .env with your Substack credentials"
echo "2. Run: python debug_auth.py (to test authentication)"
echo "3. Run: python -m pytest (to run all tests)"
echo "4. Configure Claude Desktop with the MCP server"
echo ""
echo -e "${YELLOW}To activate the virtual environment in the future:${NC}"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "   source venv/Scripts/activate"
else
    echo "   source venv/bin/activate"
fi
echo ""
echo -e "${GREEN}Happy testing! 🚀${NC}"