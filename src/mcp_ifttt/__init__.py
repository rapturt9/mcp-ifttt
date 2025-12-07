"""MCP server for sending JSON messages to IFTTT webhooks.

This server provides tools to send JSON messages to IFTTT webhooks,
enabling Claude to trigger IFTTT applets and automation workflows.
"""

from typing import Any
import httpx
from fastmcp import FastMCP
from pydantic import BaseModel, Field

# Initialize FastMCP server
mcp = FastMCP("ifttt-mcp-server")

# Hardcoded IFTTT webhook URL
# WARNING: This URL contains credentials. Do not commit to public repositories.
IFTTT_WEBHOOK_URL = "https://maker.ifttt.com/trigger/overlord_mcp/json/with/key/dov3oJngbecHlHyD1zYcG-"


class WebhookPayload(BaseModel):
    """Input schema for IFTTT webhook."""

    payload: dict[str, Any] = Field(
        ...,
        description="The JSON message to send to IFTTT. Can contain any structured data you want to communicate."
    )


def handle_api_error(error: Exception) -> str:
    """Convert HTTP errors into actionable error messages.

    Args:
        error: The exception that occurred

    Returns:
        A user-friendly error message with actionable guidance
    """
    if isinstance(error, httpx.HTTPStatusError):
        status = error.response.status_code

        if status == 400:
            return "Error: Bad request. The webhook URL or payload format is invalid. Please check your IFTTT webhook configuration."
        elif status == 401:
            return "Error: Unauthorized. The IFTTT webhook key is invalid. Please verify IFTTT_WEBHOOK_URL environment variable."
        elif status == 403:
            return "Error: Forbidden. Access to this IFTTT webhook is denied. Check your IFTTT applet permissions."
        elif status == 404:
            return "Error: Webhook not found. Please verify the IFTTT webhook URL and applet name are correct."
        elif status == 429:
            return "Error: Rate limit exceeded. IFTTT has temporarily blocked requests. Please wait before trying again."
        elif status in (500, 502, 503):
            return "Error: IFTTT service is temporarily unavailable. Please try again in a few moments."
        else:
            return f"Error: IFTTT webhook request failed with status {status}. Response: {error.response.text}"

    elif isinstance(error, httpx.TimeoutException):
        return "Error: Request timed out. IFTTT did not respond in time. Please try again."

    elif isinstance(error, (httpx.ConnectError, httpx.NetworkError)):
        return "Error: Could not connect to IFTTT. Please check your internet connection and verify the webhook URL."

    return f"Error: Unexpected error occurred: {str(error)}"


@mcp.tool(
    annotations={
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def ifttt_send_webhook(payload: dict[str, Any]) -> str:
    """Sends a JSON message to an IFTTT webhook to trigger automation workflows.

    This tool sends structured JSON data to IFTTT (If This Then That) webhooks,
    enabling integration with hundreds of services and automation scenarios.
    The webhook is configured via the IFTTT_WEBHOOK_URL environment variable.

    Use cases:
      - Trigger notifications on mobile devices
      - Send data to Google Sheets, Airtable, or databases
      - Control smart home devices
      - Post to social media platforms
      - Send emails or SMS messages
      - Log data for analytics or monitoring

    Args:
        payload: The JSON message to send. Can contain any structure -
                IFTTT will receive this as the webhook body.

    Returns:
        Success message with HTTP status code and IFTTT response,
        or detailed error message if the request fails.

    Examples:
        - Send a notification: {"message": "Task completed!", "priority": "high"}
        - Log data: {"temperature": 72.5, "humidity": 45, "timestamp": "2024-01-01T12:00:00Z"}
        - Trigger action: {"action": "turn_on_lights", "room": "living_room"}

    Error Handling:
        Returns actionable error messages for authentication, connectivity,
        or rate limit issues with suggestions for common problems.
    """
    # Validate webhook URL is configured
    if not IFTTT_WEBHOOK_URL:
        return "Error: IFTTT webhook URL not configured. Please set the IFTTT_WEBHOOK_URL environment variable with your IFTTT webhook endpoint."

    try:
        # Send POST request to IFTTT webhook
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                IFTTT_WEBHOOK_URL,
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            return f"Message sent to IFTTT successfully!\nStatus: {response.status_code}\nResponse: {response.text}"

    except Exception as error:
        return handle_api_error(error)
