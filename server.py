"""FastMCP server entrypoint for cloud deployment."""

from typing import Any
import httpx
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("ifttt-mcp-server")

# Hardcoded IFTTT webhook URL
IFTTT_WEBHOOK_URL = "https://maker.ifttt.com/trigger/overlord_mcp/json/with/key/dov3oJngbecHlHyD1zYcG-"


def handle_api_error(error: Exception) -> str:
    """Convert HTTP errors into actionable error messages."""
    if isinstance(error, httpx.HTTPStatusError):
        status = error.response.status_code
        if status == 400:
            return "Error: Bad request. The webhook URL or payload format is invalid."
        elif status == 401:
            return "Error: Unauthorized. The IFTTT webhook key is invalid."
        elif status == 403:
            return "Error: Forbidden. Access to this IFTTT webhook is denied."
        elif status == 404:
            return "Error: Webhook not found. Verify the webhook URL and applet name."
        elif status == 429:
            return "Error: Rate limit exceeded. Please wait before trying again."
        elif status in (500, 502, 503):
            return "Error: IFTTT service is temporarily unavailable."
        else:
            return f"Error: Request failed with status {status}."
    elif isinstance(error, httpx.TimeoutException):
        return "Error: Request timed out. Please try again."
    elif isinstance(error, (httpx.ConnectError, httpx.NetworkError)):
        return "Error: Could not connect to IFTTT."
    return f"Error: {str(error)}"


@mcp.tool()
async def ifttt_send_webhook(payload: dict[str, Any]) -> str:
    """Sends a JSON message to IFTTT webhook to trigger automation workflows.

    Args:
        payload: The JSON message to send to IFTTT.

    Returns:
        Success message or error details.
    """
    if not IFTTT_WEBHOOK_URL:
        return "Error: IFTTT webhook URL not configured."

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                IFTTT_WEBHOOK_URL,
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            return f"Message sent successfully!\nStatus: {response.status_code}\nResponse: {response.text}"
    except Exception as error:
        return handle_api_error(error)