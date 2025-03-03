# OpenDota MCP Server

A Model Context Protocol (MCP) server implementation for accessing OpenDota API data. This server enables LLMs and AI assistants to retrieve real-time Dota 2 statistics, match data, player information, and more through a standard interface.

## Features

- Access player profiles, statistics, and match history
- Retrieve detailed match information 
- Look up professional players and teams
- Get hero statistics and rankings
- Search for players by name
- And more!

## Installation

```bash
# Clone the repository
git clone https://github.com/asusevski/opendota-mcp-server.git
cd opendota-mcp-server

# Install the package
pip install -e .

# For development dependencies
pip install -e ".[dev]"
```

## Usage

### Setting up your environment

1. (Optional but recommended) Create an OpenDota API key at https://www.opendota.com/api-keys
2. Set your API key as an environment variable:

```bash
export OPENDOTA_API_KEY=your_api_key_here
```

### Running the server directly

```bash
python -m src.opendota-server.server
```

### Using the client

```bash
python -m src.client
```

## Development

```bash
# Format code
black src/

# Check code quality
ruff check src/

# Sort imports
isort src/

# Type checking
pyright
```

## License

MIT

