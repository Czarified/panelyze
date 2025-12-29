"""Placeholder tests for panelyze."""

import panelyze


def test_version():
    """Test that version is defined."""
    assert hasattr(panelyze, "__version__")
    assert isinstance(panelyze.__version__, str)
