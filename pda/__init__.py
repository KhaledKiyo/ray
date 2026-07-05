"""PDA Voice Monitor - Linux power event announcer with Piper TTS."""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from pda.voice_engine import VoiceEngine
from pda.power_monitor import PowerMonitor
from pda.config import Config

__all__ = ["VoiceEngine", "PowerMonitor", "Config"]
