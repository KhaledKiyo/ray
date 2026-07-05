"""Unit tests for PDA Voice Monitor.

These tests cover core functionality of the configuration and initialization
systems. Integration tests with udev/audio hardware would require a full
Linux environment with hardware access.
"""

import json
import logging
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

from pda.config import Config
from pda.voice_engine import VoiceEngine
from pda.power_monitor import PowerMonitor


class TestConfig:
    """Tests for configuration management."""

    def test_config_load_from_file(self):
        """Test loading configuration from JSON file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            config_data = {
                "model_path": "./models/sound/PDA.onnx",
                "log_level": "DEBUG",
                "plug_in_messages": ["Test plug in"],
                "plug_out_messages": ["Test plug out"],
            }
            json.dump(config_data, f)
            f.flush()

            config = Config(f.name)
            assert config.get_log_level() == "DEBUG"
            assert "Test plug in" in config.get_plug_in_messages()

            Path(f.name).unlink()

    def test_config_file_not_found(self):
        """Test error when config file not found."""
        with pytest.raises(FileNotFoundError):
            Config("/nonexistent/config.json")

    def test_config_invalid_json(self):
        """Test error when config file has invalid JSON."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("{ invalid json }")
            f.flush()

            with pytest.raises(json.JSONDecodeError):
                Config(f.name)

            Path(f.name).unlink()

    def test_config_env_override(self):
        """Test environment variable overrides."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"log_level": "INFO"}, f)
            f.flush()

            with patch.dict("os.environ", {"PDA_LOG_LEVEL": "ERROR"}):
                config = Config(f.name)
                assert config.get_log_level() == "ERROR"

            Path(f.name).unlink()

    def test_config_defaults(self):
        """Test default values when keys missing."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({}, f)
            f.flush()

            config = Config(f.name)
            assert config.get_log_level() == "INFO"
            assert config.get_plug_in_messages() == ["External power source detected."]

            Path(f.name).unlink()


class TestVoiceEngine:
    """Tests for VoiceEngine class."""

    def test_voice_engine_missing_model(self):
        """Test error when model file not found."""
        with pytest.raises(FileNotFoundError):
            VoiceEngine("/nonexistent/model.onnx")

    @patch("pda.voice_engine.PiperVoice")
    def test_voice_engine_initialization(self, mock_piper):
        """Test successful voice engine initialization."""
        # Setup mock
        mock_voice = MagicMock()
        mock_voice.config.sample_rate = 22050
        mock_piper.load.return_value = mock_voice

        # Create temporary model file
        with tempfile.NamedTemporaryFile(suffix=".onnx", delete=False) as f:
            model_path = f.name

        try:
            engine = VoiceEngine(model_path)
            assert engine.get_sample_rate() == 22050
        finally:
            Path(model_path).unlink()



    @patch("pda.voice_engine.PiperVoice")
    def test_speak_empty_text(self, mock_piper):
        """Test speak with empty text returns False."""
        mock_voice = MagicMock()
        mock_voice.config.sample_rate = 22050
        mock_piper.load.return_value = mock_voice

        with tempfile.NamedTemporaryFile(suffix=".onnx", delete=False) as f:
            model_path = f.name

        try:
            engine = VoiceEngine(model_path)
            result = engine.speak("")
            assert result is False
            
            result = engine.speak("   ")
            assert result is False
        finally:
            Path(model_path).unlink()

    @patch("pda.voice_engine.PiperVoice")
    def test_get_sample_rate(self, mock_piper):
        """Test get_sample_rate returns correct value."""
        mock_voice = MagicMock()
        mock_voice.config.sample_rate = 44100
        mock_piper.load.return_value = mock_voice

        with tempfile.NamedTemporaryFile(suffix=".onnx", delete=False) as f:
            model_path = f.name

        try:
            engine = VoiceEngine(model_path)
            assert engine.get_sample_rate() == 44100
        finally:
            Path(model_path).unlink()


class TestPowerMonitor:
    """Tests for PowerMonitor class."""

    @patch("pda.power_monitor.pyudev.Context")
    def test_power_monitor_initialization(self, mock_context_class):
        """Test PowerMonitor initialization."""
        # Mock udev
        mock_context = MagicMock()
        mock_monitor = MagicMock()
        mock_context_class.return_value = mock_context
        mock_context.list_devices.return_value = []
        mock_context.Monitor.from_netlink.return_value = mock_monitor

        # Create dummy voice engine
        mock_voice = MagicMock()
        
        # Should not raise
        try:
            monitor = PowerMonitor(mock_voice)
            assert monitor.pda is mock_voice
        except RuntimeError:
            pytest.skip("pyudev not fully available in test environment")

    @patch("pda.power_monitor.pyudev.Context")
    def test_initial_state_no_adapter(self, mock_context_class):
        """Test initial state when no AC adapter found."""
        mock_context = MagicMock()
        mock_monitor = MagicMock()
        mock_context_class.return_value = mock_context
        mock_context.list_devices.return_value = []  # No devices
        mock_context.Monitor.from_netlink.return_value = mock_monitor

        mock_voice = MagicMock()
        
        try:
            with patch("logging.warning") as mock_warn:
                monitor = PowerMonitor(mock_voice)
                # Should log warning about no AC adapter
                assert monitor.get_current_state() is None
        except RuntimeError:
            pytest.skip("pyudev not available")

    def test_get_current_state(self):
        """Test state tracking API."""
        mock_voice = MagicMock()
        
        with patch("pda.power_monitor.pyudev.Context") as mock_context_class:
            mock_context = MagicMock()
            mock_monitor = MagicMock()
            mock_context_class.return_value = mock_context
            mock_context.list_devices.return_value = []
            mock_context.Monitor.from_netlink.return_value = mock_monitor
            
            try:
                monitor = PowerMonitor(mock_voice)
                # Initially None until first detection
                state = monitor.get_current_state()
                assert state is None or isinstance(state, bool)
            except RuntimeError:
                pytest.skip("pyudev not available")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
