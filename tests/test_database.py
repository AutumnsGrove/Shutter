"""
Tests for SQLite offenders list.
"""

import pytest
from pathlib import Path


class TestOffendersDatabase:
    """Test suite for offenders list management."""

    def test_init_db(self, tmp_path):
        """Test database initialization."""
        # TODO: Implement test with tmp_path
        pass

    def test_add_offender(self):
        """Test adding domain to offenders list."""
        # TODO: Implement test
        pass

    def test_get_offender(self):
        """Test retrieving offender by domain."""
        # TODO: Implement test
        pass

    def test_detection_threshold(self):
        """Test that ≥3 detections trigger skip."""
        # TODO: Implement test
        pass

    def test_injection_type_tracking(self):
        """Test that injection types are tracked per domain."""
        # TODO: Implement test
        pass
