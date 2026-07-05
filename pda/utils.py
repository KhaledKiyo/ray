"""Utility functions for PDA Voice Monitor."""

import logging
import sys
from typing import Optional


def setup_logging(log_level: str = "INFO") -> None:
    """Configure logging for the application.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    if log_level not in valid_levels:
        log_level = "INFO"

    logging.basicConfig(
        level=getattr(logging, log_level),
        format="[%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def check_platform() -> bool:
    """Check if running on Linux (required for udev).

    Returns:
        True if on Linux, False otherwise
    """
    import platform

    if platform.system() != "Linux":
        logging.error("This application requires Linux (for udev power monitoring)")
        return False
    return True
