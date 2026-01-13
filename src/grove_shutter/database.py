"""
SQLite offenders list - local persistent storage of domains with detected injections.

All SQL isolated in this file. Application code uses function-based interface.
"""

import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional, List
from grove_shutter.models import Offender


DB_PATH = Path.home() / ".shutter" / "offenders.db"


def init_db():
    """Initialize offenders database and create tables if needed."""
    # TODO: Create offenders table
    pass


def add_offender(domain: str, injection_type: str):
    """Add or update an offender in the database."""
    # TODO: Insert/update offender record
    pass


def get_offender(domain: str) -> Optional[Offender]:
    """Retrieve offender record by domain."""
    # TODO: Query offender by domain
    pass


def list_offenders() -> List[Offender]:
    """List all offenders in database."""
    # TODO: Query all offenders
    pass


def should_skip_fetch(domain: str) -> bool:
    """
    Check if domain should be skipped entirely (≥3 detections).

    Returns:
        True if domain has ≥3 detections and should be skipped
    """
    # TODO: Check detection count threshold
    pass
