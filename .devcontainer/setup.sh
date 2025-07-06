#!/bin/bash

# DevContainer setup script for Claude Code and MCP tools

echo "Setting up development environment..."

# Install Claude Code
echo "Installing Claude Code..."
wget -q https://pub-7c3a1b7d65a64aa2bcea1b0eedd6d63a.r2.dev/anthropic-ai-claude-code-1.0.31.tgz
npm install -g anthropic-ai-claude-code-1.0.31.tgz
rm anthropic-ai-claude-code-1.0.31.tgz

# Add context7 MCP server
echo "Adding context7 MCP server..."
claude mcp add --transport http context7 https://mcp.context7.com/mcp

# Add sequential-thinking MCP server
echo "Adding sequential-thinking MCP server..."
claude mcp add sequential-thinking npx @modelcontextprotocol/server-sequential-thinking

# Add puppeteer MCP server
echo "Adding puppeteer MCP server..."
claude mcp add puppeteer npx @modelcontextprotocol/server-puppeteer

# Add magic MCP server (21st.dev)
echo "Adding magic MCP server..."
if [ -n "$MAGIC_API_KEY" ]; then
    claude mcp add magic npx @21st-dev/magic@latest --env API_KEY=$MAGIC_API_KEY
    echo "Magic MCP server configured with API key"
else
    echo "WARNING: MAGIC_API_KEY environment variable not set. Magic MCP server will not be configured."
    echo "Please set MAGIC_API_KEY in your local environment and rebuild the container."
fi

echo "Development environment setup complete!"
echo "Available MCP servers:"
echo "- context7: AI-powered documentation and code context"
echo "- sequential-thinking: Advanced reasoning and problem-solving"
echo "- puppeteer: Browser automation and testing"
echo "- magic: UI component generation from 21st.dev"