"""Placeholder tests for panl."""

import panl


def test_version() -> None:
    """Test the version string is present."""
    assert panl.__version__ is not None
    assert isinstance(panl.__version__, str)
