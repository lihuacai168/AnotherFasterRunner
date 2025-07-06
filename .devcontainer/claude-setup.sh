#!/bin/bash

# Claude authentication and MCP setup helper script

echo "=== Claude Authentication and Setup Helper ==="
echo ""

# Check if Claude is already authenticated
if claude --version >/dev/null 2>&1; then
    echo "✅ Claude is installed and accessible"
    echo ""
    
    # Try to run a simple command to check auth
    if claude --help >/dev/null 2>&1; then
        echo "✅ Claude appears to be authenticated"
    else
        echo "⚠️  Claude needs authentication"
        echo ""
        echo "Please run: claude"
        echo "And follow the prompts to authenticate."
        echo ""
        read -p "Press Enter to run 'claude' now, or Ctrl+C to exit..."
        claude
    fi
else
    echo "❌ Claude is not installed or not in PATH"
    echo "Please run the devcontainer setup script first."
    exit 1
fi

echo ""
echo "=== Re-adding MCP servers (if needed) ==="

# Function to add MCP server with better error handling
add_mcp_server() {
    local name=$1
    shift
    echo -n "Adding $name MCP server... "
    
    if output=$(claude mcp add "$@" 2>&1); then
        echo "✅ Success"
    else
        if echo "$output" | grep -q "already exists"; then
            echo "✅ Already configured"
        else
            echo "❌ Failed"
            echo "   Error: $output"
        fi
    fi
}

# Re-add all MCP servers
add_mcp_server "context7" --transport http context7 https://mcp.context7.com/mcp
add_mcp_server "sequential-thinking" sequential-thinking npx @modelcontextprotocol/server-sequential-thinking
add_mcp_server "puppeteer" puppeteer npx @modelcontextprotocol/server-puppeteer

# Add magic MCP server if API key is available
if [ -n "$MAGIC_API_KEY" ]; then
    add_mcp_server "magic" magic npx @21st-dev/magic@latest --env API_KEY=$MAGIC_API_KEY
else
    echo ""
    echo "ℹ️  Note: MAGIC_API_KEY not set. Magic MCP server (21st.dev) not configured."
fi

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "You can now use Claude with the following commands:"
echo "  claude --help          # Show help"
echo "  claude mcp list        # List configured MCP servers"
echo "  claude chat           # Start an interactive chat"
echo ""
echo "For UI component generation, ensure MAGIC_API_KEY is set in your environment."