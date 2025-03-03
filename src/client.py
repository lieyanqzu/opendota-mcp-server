"""
OpenDota MCP Client

Example client for interacting with the OpenDota MCP server.
Demonstrates how to establish a connection and access available API endpoints.
"""

import asyncio
import logging
import os
import sys
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("opendota-client")


async def get_player_info(session: ClientSession, account_id: int) -> Any:
    """Fetch player information from the server."""
    try:
        return await session.call_tool("get_player_by_id", {"account_id": account_id})
    except Exception as e:
        logger.error(f"Error fetching player info: {e}")
        return f"Error: {str(e)}"


async def get_matches(session: ClientSession, account_id: int, limit: int = 5) -> Any:
    """Fetch recent matches for a player."""
    try:
        return await session.call_tool(
            "get_player_recent_matches", {"account_id": account_id, "limit": limit}
        )
    except Exception as e:
        logger.error(f"Error fetching matches: {e}")
        return f"Error: {str(e)}"


async def search_for_player(session: ClientSession, name: str) -> Any:
    """Search for a player by name."""
    try:
        return await session.call_tool("search_player", {"query": name})
    except Exception as e:
        logger.error(f"Error searching for player: {e}")
        return f"Error: {str(e)}"


async def main() -> None:
    """Main function that sets up the MCP client and runs example queries."""
    # Get the absolute path to the server script
    server_script = os.path.join(os.path.dirname(__file__), "opendota_server/server.py")

    # Create server parameters for stdio connection using python interpreter
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[server_script],
        env=os.environ.copy(),  # Pass environment variables to the server
    )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()
                logger.info("Connection initialized")

                # List available resources/tools
                tools = await session.list_tools()
                tool_list = list(tools)
                logger.info(f"Found {len(tool_list)} available tools")

                print("Available OpenDota API Tools:")
                for i, tool in enumerate(tool_list, 1):
                    print(f"{i}. {tool}")
                print("\n" + "-" * 50 + "\n")

                # Example: Search for a player named "Saadman01"
                search_result = await search_for_player(session, "Saadman01")
                print("Search Results for 'Saadman01':")
                print(search_result)
                print("\n" + "-" * 50 + "\n")

                # Example: Get info for a specific player (dota legend Saadman01)
                saadman_id = 329977411
                player_info = await get_player_info(session, saadman_id)
                print(f"Player Info for Dendi (ID: {saadman_id}):")
                print(player_info)
                print("\n" + "-" * 50 + "\n")

                # Example: Get recent matches for the player
                recent_matches = await get_matches(session, saadman_id, 3)
                print(f"Recent Matches for Saadman01 (ID: {saadman_id}):")
                print(recent_matches)

    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
