"""
Mock data and response handlers for testing the OpenDota MCP Server.
"""

from typing import Any, Dict, List

# Mock API responses for unit tests
MOCK_RESPONSES = {
    # Players
    "players/123": {
        "account_id": 123,
        "profile": {
            "personaname": "MockPlayer",
            "name": "Mock Player",
            "steamid": "76561198000000123",
            "avatarfull": "https://example.com/avatar.jpg",
            "profileurl": "https://example.com/profile",
            "loccountrycode": "US",
        },
        "rank_tier": 65,
        "mmr_estimate": {"estimate": 4500},
        "is_pro": False,
    },
    
    # Pro player
    "players/456": {
        "account_id": 456,
        "profile": {
            "personaname": "ProPlayer",
            "name": "Pro Player",
            "steamid": "76561198000000456",
            "avatarfull": "https://example.com/pro_avatar.jpg",
            "profileurl": "https://example.com/pro_profile",
            "loccountrycode": "UA",
        },
        "rank_tier": 80,
        "mmr_estimate": {"estimate": 8000},
        "is_pro": True,
        "team_name": "Mock Team",
        "team_id": 789,
    },
    
    # Pro player recent matches
    "players/456/recentMatches": [
        {
            "match_id": 6789125,
            "player_slot": 128,
            "radiant_win": True,
            "duration": 2200,
            "game_mode": 2,
            "lobby_type": 7,
            "hero_id": 3,
            "start_time": 1593100000,
            "kills": 12,
            "deaths": 2,
            "assists": 8,
            "gold_per_min": 600,
            "xp_per_min": 700,
        },
        {
            "match_id": 6789126,
            "player_slot": 1,
            "radiant_win": False,
            "duration": 1900,
            "game_mode": 2,
            "lobby_type": 7,
            "hero_id": 4,
            "start_time": 1593090000,
            "kills": 8,
            "deaths": 3,
            "assists": 15,
            "gold_per_min": 550,
            "xp_per_min": 650,
        },
    ],
    
    # Player win/loss
    "players/123/wl": {
        "win": 500,
        "lose": 400,
    },
    
    # Player recent matches
    "players/123/recentMatches": [
        {
            "match_id": 6789123,
            "player_slot": 128,
            "radiant_win": False,
            "duration": 2400,
            "game_mode": 2,
            "lobby_type": 7,
            "hero_id": 1,
            "start_time": 1593000000,
            "kills": 10,
            "deaths": 5,
            "assists": 15,
            "gold_per_min": 500,
            "xp_per_min": 600,
        },
        {
            "match_id": 6789124,
            "player_slot": 1,
            "radiant_win": True,
            "duration": 1800,
            "game_mode": 2,
            "lobby_type": 7,
            "hero_id": 2,
            "start_time": 1592990000,
            "kills": 5,
            "deaths": 2,
            "assists": 20,
            "gold_per_min": 450,
            "xp_per_min": 550,
        },
    ],
    
    # Match details
    "matches/6789123": {
        "match_id": 6789123,
        "duration": 2400,
        "start_time": 1593000000,
        "radiant_win": False,
        "radiant_score": 25,
        "dire_score": 40,
        "game_mode": 2,
        "lobby_type": 7,
        "region": 1,
        "players": [
            {
                "account_id": 123,
                "player_slot": 128,
                "hero_id": 1,
                "kills": 10,
                "deaths": 5,
                "assists": 15,
                "gold_per_min": 500,
                "xp_per_min": 600,
            },
            {
                "account_id": 124,
                "player_slot": 129,
                "hero_id": 2,
                "kills": 8,
                "deaths": 3,
                "assists": 12,
                "gold_per_min": 480,
                "xp_per_min": 580,
            },
        ],
    },
    
    # Heroes
    "heroes": [
        {
            "id": 1,
            "name": "npc_dota_hero_antimage",
            "localized_name": "Anti-Mage",
            "primary_attr": "agi",
            "attack_type": "Melee",
            "roles": ["Carry", "Escape", "Nuker"],
        },
        {
            "id": 2,
            "name": "npc_dota_hero_axe",
            "localized_name": "Axe",
            "primary_attr": "str",
            "attack_type": "Melee",
            "roles": ["Initiator", "Durable", "Disabler", "Jungler"],
        },
    ],
    
    # Hero stats
    "heroStats": [
        {
            "id": 1,
            "name": "npc_dota_hero_antimage",
            "localized_name": "Anti-Mage",
            "primary_attr": "agi",
            "attack_type": "Melee",
            "roles": ["Carry", "Escape", "Nuker"],
            "1_pick": 1000,
            "1_win": 500,
            "2_pick": 2000,
            "2_win": 1100,
            "3_pick": 3000,
            "3_win": 1500,
            "4_pick": 4000, 
            "4_win": 2000,
            "5_pick": 5000,
            "5_win": 2500,
            "6_pick": 3000,
            "6_win": 1600,
            "7_pick": 2000,
            "7_win": 1000,
            "8_pick": 1000,
            "8_win": 550,
            "pro_pick": 100,
            "pro_win": 55,
            "pro_ban": 80,
        },
        {
            "id": 2,
            "name": "npc_dota_hero_axe",
            "localized_name": "Axe",
            "primary_attr": "str",
            "attack_type": "Melee",
            "roles": ["Initiator", "Durable", "Disabler", "Jungler"],
            "1_pick": 1200,
            "1_win": 700,
            "2_pick": 2200,
            "2_win": 1300,
            "3_pick": 3200,
            "3_win": 1700,
            "4_pick": 4200,
            "4_win": 2100,
            "5_pick": 5200,
            "5_win": 2700,
            "6_pick": 3200,
            "6_win": 1700,
            "7_pick": 2200,
            "7_win": 1150,
            "8_pick": 1200,
            "8_win": 650,
            "pro_pick": 120,
            "pro_win": 65,
            "pro_ban": 90,
        },
    ],
    
    # Search
    "search?q=dendi": [
        {
            "account_id": 70388657,
            "personaname": "Dendi",
            "similarity": 0.95,
        },
        {
            "account_id": 123456789,
            "personaname": "DendiClone",
            "similarity": 0.8,
        },
    ],
    
    # Pro players
    "proPlayers": [
        {
            "account_id": 70388657,
            "name": "Dendi",
            "team_name": "B8",
            "country_code": "UA",
        },
        {
            "account_id": 111620041,
            "name": "SumaiL",
            "team_name": "Team Liquid",
            "country_code": "PK",
        },
    ],
    
    # Pro matches
    "proMatches": [
        {
            "match_id": 7123456,
            "duration": 2400,
            "start_time": 1593100000,
            "radiant_name": "Team Secret",
            "dire_name": "Team Liquid",
            "league_name": "The International 2023",
            "radiant_score": 30,
            "dire_score": 25,
            "radiant_win": True,
        },
    ],
    
    # Team info
    "teams/1": {
        "name": "Team Secret",
        "tag": "Secret",
        "rating": 1500,
        "wins": 300,
        "losses": 150,
        "last_match_time": 1593100000,
    },
    
    # Team players
    "teams/1/players": [
        {
            "name": "Puppey",
            "account_id": 87278757,
            "games_played": 1000,
            "wins": 650,
            "is_current_team_member": True,
        },
    ],
    
    # Public matches
    "publicMatches": [
        {
            "match_id": 7234567,
            "duration": 1800,
            "start_time": 1593200000,
            "avg_rank_tier": 65,
            "radiant_win": True,
            "radiant_team": [1, 2, 3, 4, 5],
            "dire_team": [6, 7, 8, 9, 10],
        },
    ],
}

def get_mock_response(endpoint: str, params: Dict = None) -> Dict[str, Any]:
    """Get a mock response for the given API endpoint."""
    # Handle query parameters in the endpoint
    if params and "q" in params:
        combined_endpoint = f"{endpoint}?q={params['q']}"
        if combined_endpoint in MOCK_RESPONSES:
            return MOCK_RESPONSES[combined_endpoint]
    
    # Try to find a direct match for the endpoint
    if endpoint in MOCK_RESPONSES:
        return MOCK_RESPONSES[endpoint]
    
    # Return an error response if endpoint not found
    return {"error": f"Mock endpoint not found: {endpoint}"}
