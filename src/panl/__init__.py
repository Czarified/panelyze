"""Panl: Structural panel analysis utility."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("panelyze")
except PackageNotFoundError:
    # Package is not installed
    __version__ = "unknown"
