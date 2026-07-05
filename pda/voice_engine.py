"""Voice synthesis engine using Piper TTS."""

import io
import logging
import wave
from pathlib import Path
from typing import Optional

import numpy as np
import sounddevice as sd
from piper import PiperVoice


class VoiceEngine:
    """Wrapper around Piper TTS for speech synthesis and playback."""

    def __init__(self, model_path: str) -> None:
        """Initialize voice engine with ONNX model.

        Args:
            model_path: Path to Piper ONNX model file

        Raises:
            FileNotFoundError: If model file does not exist
            RuntimeError: If model fails to load
        """
        if not Path(model_path).exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")

        logging.info(f"Loading AI Voice Model from: {model_path}...")
        try:
            self.voice = PiperVoice.load(model_path)
            self.sample_rate: int = self.voice.config.sample_rate
            logging.info(f"Voice loaded successfully! Sample rate: {self.sample_rate}Hz")
        except Exception as e:
            raise RuntimeError(f"Failed to load voice model: {e}")

    def speak(self, text: str, device: Optional[int] = None) -> bool:
        """Generate and play speech from text.

        Args:
            text: Text to synthesize and play
            device: Audio device ID (None uses default)

        Returns:
            True if successful, False if failed
        """
        if not text or not text.strip():
            logging.warning("Empty text provided to speak()")
            return False

        logging.info(f"PDA says: '{text}'")

        try:
            # Synthesize speech to WAV in memory
            audio_data = self._synthesize_to_audio(text)

            if audio_data is None or len(audio_data) == 0:
                logging.error("Synthesis produced empty audio")
                return False

            # Play audio
            sd.play(audio_data, samplerate=self.sample_rate, device=device)
            sd.wait()
            return True

        except Exception as e:
            logging.error(f"Audio playback failed: {e}")
            return False

    def _synthesize_to_audio(self, text: str) -> Optional[np.ndarray]:
        """Synthesize text to audio array.

        Args:
            text: Text to synthesize

        Returns:
            NumPy array of audio data, or None if failed
        """
        try:
            wav_io = io.BytesIO()

            # Use appropriate synthesis method
            with wave.open(wav_io, "wb") as wav_file:
                if hasattr(self.voice, "synthesize_wav"):
                    self.voice.synthesize_wav(text, wav_file)
                else:
                    self.voice.synthesize(text, wav_file)

            # Read back the audio data
            wav_io.seek(0)
            with wave.open(wav_io, "rb") as wav_file:
                raw_audio = wav_file.readframes(wav_file.getnframes())

            # Convert to numpy array
            audio_array = np.frombuffer(raw_audio, dtype=np.int16)
            return audio_array

        except Exception as e:
            logging.error(f"Synthesis failed: {e}")
            return None

    def get_sample_rate(self) -> int:
        """Get audio sample rate in Hz.

        Returns:
            Sample rate in Hz
        """
        return self.sample_rate
