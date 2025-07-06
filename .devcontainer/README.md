# DevContainer Setup for AnotherFasterRunner

This devcontainer provides a complete development environment with Claude Code, MCP tools, Poetry, and GitHub CLI pre-configured.

## 🚀 Features

- **Python 3.9** development environment
- **Poetry** for dependency management
- **GitHub CLI** with authentication
- **Claude Code** with MCP (Model Context Protocol) servers
- **Node.js 22** for JavaScript tooling
- Pre-configured MCP servers:
  - **context7**: AI-powered documentation and code context
  - **sequential-thinking**: Advanced reasoning and problem-solving
  - **puppeteer**: Browser automation and testing
  - **magic**: UI component generation from 21st.dev

## 📋 Prerequisites

1. Docker Desktop or compatible Docker environment
2. Visual Studio Code with Remote-Containers extension
3. (Optional) MAGIC_API_KEY for 21st.dev UI components

## 🛠️ Setup Instructions

### 1. Environment Variables

Create a `.env` file in your local machine (not in the repository) with:

```bash
MAGIC_API_KEY=your_api_key_here  # Optional: for 21st.dev UI components
```

### 2. Open in DevContainer

1. Open the project in VS Code
2. Press `F1` and select "Remote-Containers: Reopen in Container"
3. Wait for the container to build and setup to complete

### 3. Post-Setup Authentication

#### GitHub CLI Authentication
The setup script will automatically check if GitHub CLI needs authentication. If required, you'll be prompted to:
1. Choose authentication method (browser recommended)
2. Follow the prompts to complete authentication

#### Claude Authentication
On first use, Claude requires authentication:

1. Run `claude` in the terminal
2. You'll be prompted to visit https://claude.ai/authorizations
3. Create a new authorization
4. Enter the authorization code when prompted

Alternatively, run the helper script:
```bash
.devcontainer/claude-setup.sh
```

## 🔧 Manual Setup (if needed)

If automatic setup fails, you can manually run:

```bash
# Install Poetry dependencies
poetry install

# Authenticate GitHub CLI
gh auth login

# Authenticate Claude
claude

# Re-add MCP servers
.devcontainer/claude-setup.sh
```

## 📝 Usage

### Poetry Commands
```bash
poetry shell          # Activate virtual environment
poetry install        # Install dependencies
poetry add <package>  # Add new dependency
poetry run pytest     # Run tests
```

### Claude Commands
```bash
claude --help         # Show help
claude chat          # Start interactive chat
claude mcp list      # List MCP servers
claude mcp logs      # View MCP server logs
```

### GitHub CLI Commands
```bash
gh auth status       # Check authentication status
gh pr create         # Create pull request
gh pr list           # List pull requests
```

## 🐛 Troubleshooting

### Claude authentication fails
- Ensure you have internet connection
- Try running `claude` directly and follow prompts
- Check that the authorization URL opens correctly

### Poetry install fails
- Check Python version: `python --version` (should be 3.9.x)
- Clear Poetry cache: `poetry cache clear pypi --all`
- Try manual install: `poetry install --verbose`

### MCP servers not working
- Run `.devcontainer/claude-setup.sh` to re-add servers
- Check Claude authentication: `claude mcp list`
- View logs: `claude mcp logs <server-name>`

### Magic MCP server not available
- Ensure MAGIC_API_KEY is set in your local .env file
- Rebuild the container after setting the environment variable

## 📚 Additional Resources

- [Claude Documentation](https://docs.anthropic.com/claude)
- [MCP Protocol Documentation](https://modelcontextprotocol.io)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [GitHub CLI Documentation](https://cli.github.com/manual/)