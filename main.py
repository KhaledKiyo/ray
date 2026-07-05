#!/usr/bin/env python3
"""PDA Voice Monitor - Announce power events with text-to-speech.

A Linux system utility that monitors AC power events (plug/unplug) and
announces them using Piper TTS with ONNX models.

Usage:
    python main.py              # Monitor continuously
    python main.py --once       # Check current state and exit
    python main.py --help       # Show help

Configuration:
    - Modify config.json for custom messages and model path
    - Set PDA_MODEL_PATH environment variable to override model
    - Set PDA_LOG_LEVEL environment variable to override log level
"""

import argparse
import logging
import sys
from pathlib import Path

from pda.config import Config
from pda.power_monitor import PowerMonitor
from pda.utils import check_platform, setup_logging
from pda.voice_engine import VoiceEngine


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        prog="pda-monitor",
        description="Linux power event announcer with text-to-speech",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    Monitor continuously
  %(prog)s --once             Check current state and exit
  %(prog)s --config custom.json   Use custom config file

Environment variables:
  PDA_MODEL_PATH              Override model path
  PDA_LOG_LEVEL               Override log level (DEBUG, INFO, WARNING, ERROR)
        """,
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0",
    )

    parser.add_argument(
        "--config",
        default="config.json",
        help="Path to config file (default: config.json)",
    )

    parser.add_argument(
        "--once",
        action="store_true",
        help="Check current power state and exit",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose debug logging",
    )

    return parser.parse_args()


def check_current_state(monitor: PowerMonitor, voice: VoiceEngine) -> None:
    """Check and announce current power state once.

    Args:
        monitor: PowerMonitor instance
        voice: VoiceEngine instance
    """
    state = monitor.get_current_state()
    if state is True:
        logging.info("System is currently plugged in")
        text = "System is running on external power."
    elif state is False:
        logging.info("System is currently on battery")
        text = "System is running on internal battery."
    else:
        logging.warning("Could not determine power state")
        return

    voice.speak(text)


def main() -> int:
    """Main entry point for PDA Voice Monitor.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    args = parse_arguments()

    # Check platform
    if not check_platform():
        return 1

    # Setup logging
    log_level = "DEBUG" if args.verbose else None
    try:
        # Load config first to get log level
        config = Config(args.config)
        if log_level is None:
            log_level = config.get_log_level()
        setup_logging(log_level)
    except Exception as e:
        setup_logging("INFO")
        logging.error(f"Failed to load configuration: {e}")
        return 1

    try:
        # Validate configuration
        config.validate()
    except ValueError as e:
        logging.error(f"Configuration error: {e}")
        return 1

    # Initialize voice engine
    try:
        model_path = config.get_model_path()
        voice = VoiceEngine(model_path)
    except (FileNotFoundError, RuntimeError) as e:
        logging.error(f"Failed to initialize voice engine: {e}")
        return 1

    # Initialize power monitor
    try:
        monitor = PowerMonitor(
            voice,
            plug_in_messages=config.get_plug_in_messages(),
            plug_out_messages=config.get_plug_out_messages(),
            audio_device=config.get_audio_device(),
        )
    except RuntimeError as e:
        logging.error(f"Failed to initialize power monitor: {e}")
        return 1

    # Run in requested mode
    if args.once:
        try:
            check_current_state(monitor, voice)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            logging.error(f"Error: {e}")
            return 1
    else:
        try:
            monitor.start()
        except KeyboardInterrupt:
            pass
        except Exception as e:
            logging.error(f"Fatal error: {e}")
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
