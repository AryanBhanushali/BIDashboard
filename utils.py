"""Generic helper utilities for the BI dashboard."""

from typing import Any

def safe_str(value: Any) -> str:
    """Convert a value to string, returning an empty string for None."""
    return "" if value is None else str(value)