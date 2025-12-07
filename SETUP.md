# Setup Guide for IFTTT MCP Server (FastMCP)

## Installation Steps

### 1. Install Python

You need Python 3.10 or higher to run this server. Choose one of these methods:

#### Option A: Using Homebrew (Recommended for macOS)

```bash
brew install python@3.11
```

#### Option B: Using pyenv (Python Version Manager)

```bash
# Install pyenv
curl https://pyenv.run | bash

# Install Python 3.11
pyenv install 3.11
pyenv global 3.11
```

#### Option C: Direct Download

Download from [python.org](https://www.python.org/) and install Python 3.10 or higher.

### 2. Verify Installation

```bash
python3 --version  # Should show v3.10.x or higher
```

### 3. Install uv (Recommended)

uv is a fast Python package manager that makes dependency management easier:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or using pip:

```bash
pip install uv
```

### 4. Install Project Dependencies

#### Using uv (recommended):

```bash
cd /Users/ram/Github/mcp-ifttt
uv sync
```

#### Using pip:

```bash
cd /Users/ram/Github/mcp-ifttt
pip install -e .
```

### 5. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your IFTTT webhook URL:

```bash
IFTTT_WEBHOOK_URL=https://maker.ifttt.com/trigger/your_event_name/json/with/key/your-webhook-key
```

**IMPORTANT**: Replace `your_event_name` and `your-webhook-key` with your actual IFTTT values.

### 6. Test the Server Locally

#### For stdio mode (local Claude Desktop):

```bash
uv run mcp-ifttt
# or with pip: python -m mcp_ifttt.server
```

You should see:

```
Starting IFTTT MCP server (stdio transport)
```

#### For HTTP mode (deployment-compatible):

```bash
TRANSPORT=http uv run mcp-ifttt
```

You should see:

```
Starting IFTTT MCP server on port 3000 (HTTP transport)
```

### 7. Test with MCP Inspector

```bash
# For stdio mode
npx @modelcontextprotocol/inspector uv run mcp-ifttt

# For HTTP mode (in a separate terminal after starting the server)
TRANSPORT=http uv run mcp-ifttt
# Then in another terminal:
npx @modelcontextprotocol/inspector http://localhost:3000/sse
```

## Next Steps

### For Local Development (Claude Desktop)

Update your Claude Desktop config at:

```
~/Library/Application Support/Claude/claude_desktop_config.json
```

Add:

```json
{
  "mcpServers": {
    "ifttt": {
      "command": "uv",
      "args": ["run", "mcp-ifttt"],
      "cwd": "/Users/ram/Github/mcp-ifttt",
      "env": {
        "IFTTT_WEBHOOK_URL": "https://maker.ifttt.com/trigger/your_event_name/json/with/key/your-webhook-key"
      }
    }
  }
}
```

Or if using system Python:

```json
{
  "mcpServers": {
    "ifttt": {
      "command": "python",
      "args": ["-m", "mcp_ifttt.server"],
      "cwd": "/Users/ram/Github/mcp-ifttt",
      "env": {
        "IFTTT_WEBHOOK_URL": "https://maker.ifttt.com/trigger/your_event_name/json/with/key/your-webhook-key"
      }
    }
  }
}
```

Restart Claude Desktop to load the new server.

### For Remote Deployment

1. Choose your deployment platform (Railway, Render, Fly.io, etc.)
2. Set environment variables in your platform:
   - `IFTTT_WEBHOOK_URL`: Your webhook URL
   - `TRANSPORT`: `http`
   - `PORT`: (usually auto-set by platform)
3. Deploy using the included Dockerfile or platform's Python buildpack
4. Access your server at the platform's provided URL

## Troubleshooting

### "Module not found" errors

```bash
# Reinstall dependencies
uv sync
# or
pip install -e .
```

### "Python version not supported"

Ensure you have Python 3.10 or higher:

```bash
python3 --version
```

If needed, install a newer version:

```bash
brew install python@3.11
# or use pyenv to manage multiple versions
```

### Port already in use

```bash
# Find and kill the process using port 3000
lsof -ti:3000 | xargs kill -9

# Or use a different port
PORT=3001 TRANSPORT=http uv run mcp-ifttt
```

### "IFTTT webhook URL not configured"

Make sure your `.env` file exists and contains:

```bash
IFTTT_WEBHOOK_URL=https://maker.ifttt.com/trigger/your_event_name/json/with/key/your-webhook-key
```

Or set it directly in your Claude Desktop config's `env` section.

## Development Mode

FastMCP supports hot-reload during development:

```bash
# Install dev dependencies
uv add --dev fastmcp[dev]

# Run with auto-reload
uv run mcp dev mcp_ifttt.server
```

## Getting Your IFTTT Webhook URL

1. Go to [IFTTT Webhooks Settings](https://ifttt.com/maker_webhooks/settings)
2. Copy your webhook key
3. Create a new applet:
   - **If**: Webhooks - Receive a web request
   - **Event name**: Choose a name (e.g., `claude_message`)
   - **Then**: Choose any action (Gmail, Sheets, Notifications, etc.)
4. Your webhook URL format:
   ```
   https://maker.ifttt.com/trigger/{event_name}/json/with/key/{your_key}
   ```

## Support

If you encounter issues:

1. Check the logs for error messages (stderr output)
2. Verify Python version is 3.10 or higher
3. Ensure all dependencies are installed
4. Review the main [README.md](README.md) for detailed documentation
5. Check that your IFTTT webhook URL is correct and the applet is enabled
