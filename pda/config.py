"""Configuration management for PDA Voice Monitor."""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional


class Config:
    """Load and manage configuration from JSON file or environment variables."""

    def __init__(self, config_file: Optional[str] = None) -> None:
        """Initialize configuration.

        Args:
            config_file: Path to config.json file. If not provided, looks in current directory.

        Raises:
            FileNotFoundError: If config file is not found.
            json.JSONDecodeError: If config file is invalid JSON.
        """
        self.config_file = config_file or "config.json"
        self.config: Dict[str, Any] = {}
        self._load_config()
        self._apply_env_overrides()

    def _load_config(self) -> None:
        """Load configuration from JSON file."""
        if not Path(self.config_file).exists():
            raise FileNotFoundError(f"Config file not found: {self.config_file}")

        try:
            with open(self.config_file, "r") as f:
                self.config = json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Invalid JSON in {self.config_file}: {e}", "", 0)

    def _apply_env_overrides(self) -> None:
        """Apply environment variable overrides."""
        env_model = os.getenv("PDA_MODEL_PATH")
        if env_model:
            self.config["model_path"] = env_model

        env_log = os.getenv("PDA_LOG_LEVEL")
        if env_log:
            self.config["log_level"] = env_log

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        return self.config.get(key, default)

    def get_model_path(self) -> str:
        """Get model file path."""
        path = self.get("model_path", "./models/sound/PDA.onnx")
        return self._resolve_path(path)

    def get_log_level(self) -> str:
        """Get logging level."""
        return self.get("log_level", "INFO")

    def get_plug_in_messages(self) -> List[str]:
        """Get plug-in event messages."""
        return self.get("plug_in_messages", ["External power source detected."])

    def get_plug_out_messages(self) -> List[str]:
        """Get plug-out event messages."""
        return self.get("plug_out_messages", ["Warning. Operating on internal battery."])

    @staticmethod
    def _resolve_path(path: str) -> str:
        """Resolve relative path to absolute path, expanding ~ and env vars.
        
        Args:
            path: Path string that may include ~ or env vars
            
        Returns:
            Resolved absolute path
        """
        # Expand user home directory
        path = os.path.expanduser(path)
        # Expand environment variables
        path = os.path.expandvars(path)
        # Resolve to absolute path
        return str(Path(path).resolve())

    def validate(self) -> bool:
        """Validate configuration.

        Returns:
            True if configuration is valid

        Raises:
            ValueError: If configuration is invalid
        """
        # Check model path exists
        model_path = self.get_model_path()
        if not Path(model_path).exists():
            raise ValueError(f"Model file not found: {model_path}")

        # Check log level is valid
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if self.get_log_level() not in valid_levels:
            raise ValueError(
                f"Invalid log level: {self.get_log_level()}. "
                f"Must be one of: {valid_levels}"
            )

        # Check message lists are non-empty
        if not self.get_plug_in_messages():
            raise ValueError("plug_in_messages cannot be empty")
        if not self.get_plug_out_messages():
            raise ValueError("plug_out_messages cannot be empty")

        return True
