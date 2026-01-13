"""
Configuration management - TOML config file and environment variables.
"""

import os
from pathlib import Path
from typing import Optional


CONFIG_DIR = Path.home() / ".shutter"
CONFIG_PATH = CONFIG_DIR / "config.toml"


def load_config() -> dict:
    """Load configuration from ~/.shutter/config.toml or environment."""
    # TODO: Implement TOML config loading
    pass


def get_api_key(service: str) -> Optional[str]:
    """
    Get API key for service (OpenRouter, Tavily).

    Checks environment variables first, then config file.
    """
    env_map = {
        "openrouter": "OPENROUTER_API_KEY",
        "tavily": "TAVILY_API_KEY",
    }

    # Check environment first
    env_var = env_map.get(service.lower())
    if env_var and os.getenv(env_var):
        return os.getenv(env_var)

    # TODO: Check config file
    pass


def setup_config():
    """Interactive configuration setup on first run."""
    # TODO: Prompt for API keys and create config
    pass
