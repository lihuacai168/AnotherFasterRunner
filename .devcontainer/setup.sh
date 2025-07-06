#!/bin/bash

# DevContainer setup script for Claude Code and MCP tools

echo "Setting up development environment..."

# Install Poetry
echo "Installing Poetry..."
curl -sSL https://install.python-poetry.org | python3 -
export PATH="/home/vscode/.local/bin:$PATH"

# Install project dependencies
echo "Installing project dependencies with Poetry..."
cd /workspaces/AnotherFasterRunner
poetry install --no-interaction --verbose || {
    echo "Poetry install failed. You may need to install dependencies manually."
}

# Configure GitHub CLI (if not already configured)
if ! gh auth status >/dev/null 2>&1; then
    echo "\n=== GitHub CLI Authentication Required ==="
    echo "Please follow the prompts to authenticate with GitHub:"
    gh auth login
else
    echo "GitHub CLI already authenticated."
fi

# Install Claude Code
echo "Installing Claude Code..."
wget -q https://pub-7c3a1b7d65a64aa2bcea1b0eedd6d63a.r2.dev/anthropic-ai-claude-code-1.0.31.tgz
npm install -g anthropic-ai-claude-code-1.0.31.tgz
rm anthropic-ai-claude-code-1.0.31.tgz

# Function to safely add MCP servers (won't fail if Claude needs auth)
add_mcp_server() {
    local name=$1
    shift
    echo "Adding $name MCP server..."
    if claude mcp add "$@" 2>/dev/null; then
        echo "✅ $name MCP server added successfully"
    else
        echo "⚠️  $name MCP server will be added after Claude authentication"
    fi
}

# Add MCP servers (these commands will be retried after Claude auth if needed)
add_mcp_server "context7" --transport http context7 https://mcp.context7.com/mcp
add_mcp_server "sequential-thinking" sequential-thinking npx @modelcontextprotocol/server-sequential-thinking
add_mcp_server "puppeteer" puppeteer npx @modelcontextprotocol/server-puppeteer

# Add magic MCP server (21st.dev)
if [ -n "$MAGIC_API_KEY" ]; then
    add_mcp_server "magic" magic npx @21st-dev/magic@latest --env API_KEY=$MAGIC_API_KEY
else
    echo "⚠️  WARNING: MAGIC_API_KEY environment variable not set."
    echo "   Magic MCP server (21st.dev) will not be configured."
    echo "   To use it, set MAGIC_API_KEY in your local .env and rebuild the container."
fi

# Claude authentication (interactive)
echo "\n=== Claude Authentication ==="
echo "Claude requires authentication on first use."
echo "When you first run 'claude' command, you'll be prompted to:"
echo "1. Visit https://claude.ai/authorizations"
echo "2. Create a new authorization"
echo "3. Enter the authorization code"
echo ""
echo "To test Claude setup, run: claude --help"
echo ""

echo "\n=== Development Environment Setup Complete! ==="
echo ""
echo "✅ Installed tools:"
echo "   - Poetry (Python dependency management)"
echo "   - GitHub CLI (authenticated if needed)"
echo "   - Claude Code CLI"
echo ""
echo "📦 Project dependencies:"
if poetry check >/dev/null 2>&1; then
    echo "   - Python dependencies installed via Poetry"
else
    echo "   - ⚠️  Python dependencies may need manual installation"
fi
echo ""
echo "🔌 Available MCP servers:"
echo "   - context7: AI-powered documentation and code context"
echo "   - sequential-thinking: Advanced reasoning and problem-solving"
echo "   - puppeteer: Browser automation and testing"
echo "   - magic: UI component generation from 21st.dev"
echo ""
echo "💡 Next steps:"
echo "   1. Run 'claude' to authenticate (if not done already)"
echo "   2. Use 'poetry shell' to activate the virtual environment"
echo "   3. Start coding!"