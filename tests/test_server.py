"""
Unit tests for the OpenDota MCP Server functionality.
"""

import asyncio
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.opendota_server.server import (
    format_duration,
    format_rank_tier,
    format_timestamp,
    get_cache_key,
    parse_player,
)


class TestHelperFunctions(unittest.TestCase):
    """Test case for helper functions in the server module."""

    def test_format_duration(self):
        """Test the format_duration function."""
        self.assertEqual(format_duration(65), "1:05")
        self.assertEqual(format_duration(3600), "60:00")
        self.assertEqual(format_duration(0), "0:00")

    def test_format_rank_tier(self):
        """Test the format_rank_tier function."""
        self.assertEqual(format_rank_tier(None), "Unknown")
        self.assertEqual(format_rank_tier(0), "Unknown")
        self.assertEqual(format_rank_tier(10), "Herald 0")
        self.assertEqual(format_rank_tier(21), "Guardian 1")
        self.assertEqual(format_rank_tier(53), "Ancient 3")
        self.assertEqual(format_rank_tier(80), "Immortal")
        self.assertEqual(format_rank_tier(99), "Unknown")  # Invalid tier

    def test_format_timestamp(self):
        """Test the format_timestamp function."""
        self.assertEqual(format_timestamp(0), "1970-01-01 00:00:00")
        self.assertEqual(format_timestamp(None), "Unknown")

    def test_get_cache_key(self):
        """Test the get_cache_key function."""
        self.assertEqual(get_cache_key("players/123"), "players/123")
        self.assertEqual(
            get_cache_key("players/123", {"limit": 5}), "players/123?limit=5"
        )
        # Test sorting of parameters
        self.assertEqual(
            get_cache_key("matches", {"limit": 5, "offset": 10}),
            "matches?limit=5&offset=10",
        )
        self.assertEqual(
            get_cache_key("matches", {"offset": 10, "limit": 5}),
            "matches?limit=5&offset=10",
        )

    def test_parse_player(self):
        """Test the parse_player function."""
        # Test with minimal data
        player_data = {"account_id": 123}
        player = parse_player(player_data)
        self.assertEqual(player.account_id, 123)
        self.assertIsNone(player.personaname)
        self.assertFalse(player.is_pro)

        # Test with complete data
        player_data = {
            "account_id": 456,
            "profile": {
                "personaname": "TestPlayer",
                "name": "Test Player",
                "steamid": "76561198123456789",
                "avatarfull": "https://example.com/avatar.jpg",
                "profileurl": "https://example.com/profile",
                "loccountrycode": "US",
            },
            "rank_tier": 75,
            "mmr_estimate": {"estimate": 5000},
            "is_pro": True,
            "team_name": "Test Team",
            "team_id": 789,
        }
        player = parse_player(player_data)
        self.assertEqual(player.account_id, 456)
        self.assertEqual(player.personaname, "TestPlayer")
        self.assertEqual(player.name, "Test Player")
        self.assertEqual(player.steam_id, "76561198123456789")
        self.assertEqual(player.avatar, "https://example.com/avatar.jpg")
        self.assertEqual(player.profile_url, "https://example.com/profile")
        self.assertEqual(player.rank_tier, 75)
        self.assertEqual(player.mmr_estimate, 5000)
        self.assertEqual(player.country_code, "US")
        self.assertTrue(player.is_pro)
        self.assertEqual(player.team_name, "Test Team")
        self.assertEqual(player.team_id, 789)


if __name__ == "__main__":
    unittest.main()
