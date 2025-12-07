# IFTTT MCP Server

npx @modelcontextprotocol/inspector \
 uv \
 --directory /Users/ram/Github/mcp-ifttt \
 run \
 mcp-ifttt

A production-ready [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that enables Claude to send JSON messages to IFTTT webhooks, unlocking automation workflows across hundreds of services.

## Features

- **FastMCP-based** with modern Python async/await patterns
- **Dual transport support**: stdio for local development, SSE (Server-Sent Events) for production
- **Production-ready**: Clean architecture with health checks and monitoring capabilities
- **Secure**: Environment-based configuration with no hardcoded secrets
- **Robust error handling**: Actionable error messages guide users toward solutions
- **Pydantic validation**: Runtime input validation ensures data integrity

## What Can You Automate?

With IFTTT webhooks, Claude can trigger actions across 700+ services:

- 📱 Send notifications to mobile devices
- 📊 Log data to Google Sheets, Airtable, or databases
- 🏠 Control smart home devices (lights, thermostats, locks)
- 📧 Send emails via Gmail or SMS via Twilio
- 🐦 Post to social media (Twitter, LinkedIn, Facebook)
- 📝 Create tasks in Todoist, Trello, or Asana
- 🔔 Trigger Slack/Discord notifications
- 🌡️ Log sensor data for analytics
- And much more!

## Quick Start

### Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) for dependency management (recommended) or pip
- An [IFTTT account](https://ifttt.com) with Webhooks service enabled
- Your IFTTT webhook key from [ifttt.com/maker_webhooks/settings](https://ifttt.com/maker_webhooks/settings)

### Local Installation

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/mcp-ifttt.git
cd mcp-ifttt
```

2. **Install dependencies:**

Using uv (recommended):

```bash
uv sync
```

Or using pip:

```bash
pip install -e .
```

3. **Configure your webhook URL:**

Create a `.env` file (use `.env.example` as a template):

```bash
cp .env.example .env
```

Edit `.env` and add your IFTTT webhook URL:

```
IFTTT_WEBHOOK_URL=https://maker.ifttt.com/trigger/your_event_name/json/with/key/your-webhook-key
```

4. **Run the server:**

```bash
# For local development (stdio mode)
uv run mcp-ifttt
# or with pip: python -m mcp_ifttt.server

# For HTTP mode (SSE transport)
TRANSPORT=http uv run mcp-ifttt
```

## Deployment

### Environment Variables for Deployment

When deploying to any platform, set these environment variables:

- `IFTTT_WEBHOOK_URL`: Your IFTTT webhook URL (required)
- `TRANSPORT`: Set to `http` for remote deployment
- `PORT`: Server port (platform-dependent, usually auto-set)

### Deployment Platforms

This FastMCP server can be deployed to:

- **Railway**: Set `TRANSPORT=http` and `IFTTT_WEBHOOK_URL` in environment variables
- **Render**: Use the Python runtime and set environment variables
- **Fly.io**: Deploy with Docker or Python buildpack
- **AWS Lambda**: With appropriate FastMCP adapter
- **Google Cloud Run**: Using Docker container

The server supports SSE (Server-Sent Events) transport for remote deployments.

## Configuration

### Claude Desktop Setup

#### For Local Development (stdio)

Add to your Claude Desktop config at `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "ifttt": {
      "command": "uv",
      "args": ["run", "mcp-ifttt"],
      "cwd": "/path/to/mcp-ifttt",
      "env": {
        "IFTTT_WEBHOOK_URL": "https://maker.ifttt.com/trigger/your_event/json/with/key/your-key"
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
      "cwd": "/path/to/mcp-ifttt",
      "env": {
        "IFTTT_WEBHOOK_URL": "https://maker.ifttt.com/trigger/your_event/json/with/key/your-key"
      }
    }
  }
}
```

#### For Remote Deployment (HTTP/SSE)

```json
{
  "mcpServers": {
    "ifttt": {
      "url": "https://your-deployment-url.com/sse",
      "transport": "sse"
    }
  }
}
```

**Note**: You don't need to include `IFTTT_WEBHOOK_URL` in the client config when using remote deployment - it's configured on the server.

### IFTTT Webhook Setup

1. Go to [IFTTT Webhooks Settings](https://ifttt.com/maker_webhooks/settings)
2. Copy your webhook key
3. Create a new applet:
   - **If**: Webhooks - Receive a web request
   - **Event name**: `your_event_name` (use this in your webhook URL)
   - **Then**: Choose any action (Gmail, Sheets, Notifications, etc.)

Your webhook URL format:

```
https://maker.ifttt.com/trigger/{event_name}/json/with/key/{your_key}
```

## Usage

### Available Tools

#### `ifttt_send_webhook`

Sends a JSON message to your configured IFTTT webhook.

**Parameters:**

- `payload` (object, required): The JSON message to send to IFTTT

**Example:**

```json
{
  "payload": {
    "message": "Task completed!",
    "priority": "high",
    "timestamp": "2024-01-01T12:00:00Z"
  }
}
```

**Response:**

```
Message sent to IFTTT successfully!
Status: 200
Response: "Congratulations! You've fired the your_event_name event"
```

### Example Workflows

**Send a notification:**

```
"Hey Claude, send a notification to IFTTT that the deployment is complete"
```

**Log data to Google Sheets:**

```
"Log this data to my spreadsheet: temperature 72.5, humidity 45%"
```

**Trigger a smart home action:**

```
"Turn on the living room lights via IFTTT"
```

## Development

### Project Structure

```
mcp-ifttt/
├── src/
│   └── mcp_ifttt/
│       ├── __init__.py       # FastMCP server implementation
│       └── server.py         # Server entry point
├── pyproject.toml            # Python dependencies
├── uv.lock                   # Dependency lock file
├── Dockerfile                # Docker build configuration
├── .env.example              # Environment variable template
└── README.md                 # This file
```

### Development Mode

FastMCP supports hot-reload during development. Install development dependencies:

```bash
uv add --dev fastmcp[dev]
```

Run with auto-reload:

```bash
uv run mcp dev mcp_ifttt.server
```

### Testing with MCP Inspector

Test the server using the MCP Inspector:

```bash
# For stdio mode
npx @modelcontextprotocol/inspector uv run mcp-ifttt

# For HTTP mode
TRANSPORT=http uv run mcp-ifttt
# Then in another terminal:
npx @modelcontextprotocol/inspector http://localhost:3000/sse
```

## Environment Variables

| Variable            | Required | Default | Description                                                  |
| ------------------- | -------- | ------- | ------------------------------------------------------------ |
| `IFTTT_WEBHOOK_URL` | Yes      | -       | Your IFTTT webhook URL with key                              |
| `TRANSPORT`         | No       | `stdio` | Transport mode: `stdio` for local, `http` for remote         |
| `PORT`              | No       | `3000`  | HTTP server port (set automatically by deployment platforms) |

## Error Handling

The server provides actionable error messages:

- **400 Bad Request**: Invalid webhook URL or payload format
- **401 Unauthorized**: Invalid IFTTT webhook key
- **403 Forbidden**: Access denied to webhook
- **404 Not Found**: Webhook or applet not found
- **429 Rate Limited**: Too many requests, wait before retrying
- **500/502/503**: IFTTT service temporarily unavailable
- **Connection Errors**: Network or connectivity issues

All errors include suggestions for resolution.

## Monitoring

### Logs

View server logs:

```bash
# Local logs (stderr)
uv run mcp-ifttt 2>&1 | tee server.log

# Deployment platform logs (varies by platform)
# Railway: railway logs
# Render: View in dashboard
# Fly.io: fly logs
```

## Troubleshooting

### "IFTTT webhook URL not configured"

**Solution**: Set the `IFTTT_WEBHOOK_URL` environment variable in `.env` (local) or your deployment platform dashboard (production).

### "Webhook not found" (404)

**Solution**: Verify:

1. The event name in your webhook URL matches your IFTTT applet
2. The webhook key is correct
3. The applet is enabled in IFTTT

### "Connection timeout"

**Solution**:

1. Check your internet connection
2. Verify IFTTT service status at [status.ifttt.com](https://status.ifttt.com)
3. Try increasing timeout in [src/mcp_ifttt/**init**.py](src/mcp_ifttt/__init__.py) (line 111)

### Server won't start on deployment

**Solution**:

1. Check deployment platform logs for errors
2. Verify `TRANSPORT=http` is set in environment variables
3. Ensure `IFTTT_WEBHOOK_URL` is configured in platform environment variables
4. Verify Python 3.10+ is available

## Security Best Practices

- ✅ Never commit `.env` files or hardcode webhook keys
- ✅ Use environment variables for all secrets
- ✅ Rotate webhook keys periodically in IFTTT settings
- ✅ Use your deployment platform's built-in environment variable encryption
- ✅ Monitor webhook usage in IFTTT dashboard
- ✅ Review `.gitignore` to ensure secrets are never committed

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/mcp-ifttt/issues)
- **MCP Documentation**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **IFTTT Help**: [help.ifttt.com](https://help.ifttt.com)

## Acknowledgments

Built with:

- [FastMCP](https://github.com/jlowin/fastmcp) - Modern Python MCP framework
- [httpx](https://www.python-httpx.org/) - Async HTTP client
- [Pydantic](https://docs.pydantic.dev/) - Data validation
- [uv](https://docs.astral.sh/uv/) - Fast Python package manager

---

Made with ❤️ for the Claude ecosystem
