"""
Integration-style tests for the OpenDota MCP Server API functionality.
Uses mock responses to test the API tool implementations.
"""

import asyncio
import os
import sys
import unittest
from unittest.mock import AsyncMock, patch

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.opendota_server.server import (
    get_hero_stats,
    get_heroes,
    get_match_data,
    get_match_heroes,
    get_player_by_id,
    get_player_heroes,
    get_player_peers,
    get_player_rankings,
    get_player_recent_matches,
    get_player_totals,
    get_player_win_loss,
    get_player_wordcloud,
    get_pro_matches,
    get_pro_players,
    get_public_matches,
    get_team_info,
    make_opendota_request,
    search_player,
)
from tests.test_api_mocks import get_mock_response


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
        return get_mock_response(endpoint, params if params is not None else {})

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

    async def test_get_hero_stats(self):
        """Test get_hero_stats function."""
        # Test with specific hero ID
        result = await get_hero_stats(1)
        self.assertIn("Hero Stats for Anti-Mage", result)
        self.assertIn("Roles:", result)
        self.assertIn("Primary Attribute:", result)
        self.assertIn("Win Rates by Bracket:", result)
        self.assertIn("Pro Scene:", result)
        
        # Test without hero ID (should return all heroes)
        result = await get_hero_stats()
        self.assertIn("Hero Win Rates:", result)
        self.assertIn("Anti-Mage:", result) 
        self.assertIn("win rate", result)

    async def test_get_player_heroes(self):
        """Test get_player_heroes function."""
        result = await get_player_heroes(123)
        self.assertIn("Most Played Heroes for Player ID 123", result)
        self.assertTrue("Anti-Mage" in result or "Axe" in result)

    async def test_get_pro_players(self):
        """Test get_pro_players function."""
        result = await get_pro_players()
        self.assertIn("Professional Players", result)
        self.assertIn("Dendi", result)
        self.assertIn("SumaiL", result)
        self.assertIn("Team Liquid", result)

    async def test_get_pro_matches(self):
        """Test get_pro_matches function."""
        result = await get_pro_matches()
        self.assertIn("Professional Matches", result)
        self.assertIn("Team Secret", result)
        self.assertIn("Team Liquid", result)
        self.assertIn("The International 2023", result)

    async def test_get_player_peers(self):
        """Test get_player_peers function."""
        result = await get_player_peers(123)
        self.assertIn("Peers for Player ID 123", result)
        self.assertIn("Peer1", result)

    async def test_get_heroes(self):
        """Test get_heroes function."""
        result = await get_heroes()
        self.assertIn("Dota 2 Heroes", result)
        self.assertIn("Anti-Mage", result)
        self.assertIn("Axe", result)
        self.assertIn("Primary Attribute:", result)
        self.assertIn("Roles:", result)

    async def test_get_player_totals(self):
        """Test get_player_totals function."""
        result = await get_player_totals(123)
        self.assertIn("Stat Totals for Player ID 123", result)
        self.assertIn("Kills:", result)

    async def test_get_player_rankings(self):
        """Test get_player_rankings function."""
        result = await get_player_rankings(123)
        self.assertIn("Hero Rankings for Player ID 123", result)

    async def test_get_player_wordcloud(self):
        """Test get_player_wordcloud function."""
        result = await get_player_wordcloud(123)
        self.assertIn("Most Common Words for Player ID 123", result)
        self.assertIn("gg:", result)

    async def test_get_team_info(self):
        """Test get_team_info function."""
        result = await get_team_info(1)
        self.assertIn("Team: Team Secret", result)
        self.assertIn("[Secret]", result)
        self.assertIn("Rating: 1500", result)
        self.assertIn("Record: 650-150", result)

    async def test_get_public_matches(self):
        """Test get_public_matches function."""
        result = await get_public_matches()
        self.assertIn("Recent Public Matches", result)
        self.assertIn("Match ID: 7234567", result)
        self.assertIn("Duration: 30:00", result)

    async def test_get_match_heroes(self):
        """Test get_match_heroes function."""
        result = await get_match_heroes(6789123)
        self.assertIn("Heroes in Match 6789123", result)

if __name__ == "__main__":
    unittest.main()
