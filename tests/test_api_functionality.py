#!/usr/bin/env python
"""
Integration-style tests for the OpenDota MCP Server API functionality.
Uses mock responses to test the API tool implementations.
"""

import asyncio
import os
import sys
import unittest
from unittest.mock import patch, AsyncMock

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tests.test_api_mocks import get_mock_response
from src.opendota_server.server import (
    get_player_by_id,
    get_player_recent_matches,
    get_match_data,
    get_player_win_loss,
    get_player_heroes,
    get_hero_stats,
    search_player,
    make_opendota_request,
)

class TestMCPTools(unittest.IsolatedAsyncioTestCase):
    """Test case for MCP server tools."""

    def setUp(self):
        # Patch the make_opendota_request function to use our mock responses
        self.patcher = patch(
            "src.opendota_server.server.make_opendota_request",
            side_effect=self.mock_opendota_request
        )
        self.mock_request = self.patcher.start()
    
    def tearDown(self):
        self.patcher.stop()

    async def mock_opendota_request(self, endpoint, params=None):
        """Mock implementation of make_opendota_request."""
        return get_mock_response(endpoint, params)

    async def test_get_player_by_id(self):
        """Test get_player_by_id function."""
        # Test with normal player
        result = await get_player_by_id(123)
        self.assertIn("Player: MockPlayer", result)
        self.assertIn("Win/Loss: 500/400", result)
        
        # Test with pro player
        result = await get_player_by_id(456)
        self.assertIn("Player: ProPlayer", result)
        self.assertIn("Professional Player: Yes", result)
        self.assertIn("Team: Mock Team", result)

    async def test_get_player_recent_matches(self):
        """Test get_player_recent_matches function."""
        result = await get_player_recent_matches(123, 2)
        self.assertIn("Recent Matches for Player ID 123", result)
        self.assertIn("Match ID: 6789123", result)
        self.assertIn("Match ID: 6789124", result)
        
        # Test with limit
        result = await get_player_recent_matches(123, 1)
        self.assertIn("Match ID: 6789123", result)
        self.assertNotIn("Match ID: 6789124", result)

    async def test_get_match_data(self):
        """Test get_match_data function."""
        result = await get_match_data(6789123)
        self.assertIn("Match ID: 6789123", result)
        self.assertIn("Duration: 40:00", result)
        self.assertIn("Score: 25 - 40", result)
        self.assertIn("Winner: Dire", result)

    async def test_get_player_win_loss(self):
        """Test get_player_win_loss function."""
        result = await get_player_win_loss(123)
        self.assertIn("Win/Loss Record for Player ID 123", result)
        self.assertIn("Wins: 500", result)
        self.assertIn("Losses: 400", result)
        self.assertIn("Total Games: 900", result)
        self.assertIn("Win Rate: 55.56%", result)

    async def test_search_player(self):
        """Test search_player function."""
        result = await search_player("dendi")
        self.assertIn("Players matching 'dendi'", result)
        self.assertIn("Dendi", result)
        self.assertIn("Account ID: 70388657", result)

    @unittest.skip("Hero stats tests need to be implemented")
    async def test_get_hero_stats(self):
        """Test get_hero_stats function."""
        # This would test specific hero stats
        pass

if __name__ == "__main__":
    unittest.main()