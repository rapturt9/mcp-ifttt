"""FastMCP server entry point with multi-transport support."""

import os
import sys

from mcp_ifttt import mcp

# Get transport configuration from environment
TRANSPORT = os.getenv("TRANSPORT", "stdio")


def main():
    """Run the MCP server with the configured transport."""
    # Run server with appropriate transport
    if TRANSPORT == "http":
        # HTTP transport for remote deployment
        port = int(os.getenv("PORT", "3000"))
        print(f"Starting IFTTT MCP server on port {port} (HTTP transport)", file=sys.stderr)
        mcp.run(transport="sse", port=port)
    else:
        # stdio transport for local usage (default)
        print("Starting IFTTT MCP server (stdio transport)", file=sys.stderr)
        mcp.run()


if __name__ == "__main__":
    main()
