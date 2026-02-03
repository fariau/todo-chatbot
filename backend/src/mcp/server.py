from mcp.server import Server
from .tools import get_mcp_server
import asyncio
import json
from pathlib import Path


def create_mcp_server():
    """
    Create and configure the MCP server with all tools.

    Returns:
        Configured MCP server instance
    """
    server_instance = get_mcp_server()
    return server_instance


async def run_mcp_server():
    """
    Run the MCP server - this would typically be called when the server starts.
    """
    server_instance = create_mcp_server()

    # In a real implementation, this would start the MCP server
    # For now, we just return the server instance for integration
    return server_instance


# Example of how to initialize the server
if __name__ == "__main__":
    server_instance = asyncio.run(run_mcp_server())
    print("MCP Server initialized with tools:", server_instance._tools.keys())