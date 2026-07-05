"""Linux power supply event monitor."""

import logging
import random
import threading
from typing import List, Optional

import pyudev

from pda.voice_engine import VoiceEngine


class PowerMonitor:
    """Monitor AC power supply events using udev.
    
    Note: _current_state is written from the udev polling thread (in start())
    and read from the main thread (in --once mode). This is safe for boolean
    values in CPython due to GIL, but could use a lock for production use
    with other Python implementations.
    """

    def __init__(
        self,
        voice_engine: VoiceEngine,
        plug_in_messages: Optional[List[str]] = None,
        plug_out_messages: Optional[List[str]] = None,
    ) -> None:
        """Initialize power monitor.

        Args:
            voice_engine: VoiceEngine instance for announcements
            plug_in_messages: List of messages to announce when charger plugged in
            plug_out_messages: List of messages to announce when charger unplugged

        Raises:
            RuntimeError: If udev context cannot be initialized
        """
        try:
            self.context = pyudev.Context()
            self.monitor = pyudev.Monitor.from_netlink(self.context)
            self.monitor.filter_by(subsystem="power_supply")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize power monitor: {e}")

        self.pda = voice_engine
        self.plug_in_messages = plug_in_messages or [
            "External power source detected."
        ]
        self.plug_out_messages = plug_out_messages or [
            "Warning. Operating on internal battery."
        ]
        self._current_state: Optional[bool] = None
        self._check_initial_state()

    def _check_initial_state(self) -> None:
        """Check and log the initial AC power state."""
        try:
            for device in self.context.list_devices(subsystem="power_supply"):
                if device.properties.get("POWER_SUPPLY_TYPE") == "Mains":
                    try:
                        is_online = device.attributes.asstring("online") == "1"
                        self._current_state = is_online
                        state = "Plugged In" if is_online else "On Battery"
                        logging.info(
                            f"Monitoring: {device.sys_name} (Initial State: {state})"
                        )
                        return
                    except (KeyError, AttributeError):
                        continue
            logging.warning("No AC adapter found during initialization.")
        except Exception as e:
            logging.error(f"Error checking initial power state: {e}")

    def start(self) -> None:
        """Start monitoring power events (blocking).

        Listens for AC adapter plug/unplug events and announces them.
        Press Ctrl+C to exit.
        """
        logging.info("Listening for power events... (Ctrl+C to exit)")
        try:
            for device in iter(self.monitor.poll, None):
                if device.properties.get("POWER_SUPPLY_TYPE") == "Mains":
                    try:
                        online = device.attributes.asstring("online")
                        if online == "1":
                            self._handle_plug_in()
                        elif online == "0":
                            self._handle_plug_out()
                    except (KeyError, AttributeError):
                        pass
        except KeyboardInterrupt:
            logging.info("Shutting down PDA...")
        except Exception as e:
            logging.error(f"Error during monitoring: {e}")

    def _handle_plug_in(self) -> None:
        """Handle AC adapter connection event."""
        if self._current_state is True:
            return  # Already plugged in, avoid duplicate events
        
        self._current_state = True
        logging.info("🔌 Charger CONNECTED")

        text = random.choice(self.plug_in_messages)
        threading.Thread(target=self.pda.speak, args=(text,), daemon=True).start()

    def _handle_plug_out(self) -> None:
        """Handle AC adapter disconnection event."""
        if self._current_state is False:
            return  # Already unplugged, avoid duplicate events
        
        self._current_state = False
        logging.info("🔋 Charger DISCONNECTED")

        text = random.choice(self.plug_out_messages)
        threading.Thread(target=self.pda.speak, args=(text,), daemon=True).start()

    def get_current_state(self) -> Optional[bool]:
        """Get current power state.

        Returns:
            True if plugged in, False if on battery, None if unknown
        """
        return self._current_state
