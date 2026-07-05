# PDA Voice Monitor

A Linux system utility that announces power events (plug/unplug) using text-to-speech via Piper TTS and ONNX models.

[![Tests](https://github.com/yourusername/pda-voice-monitor/actions/workflows/test.yml/badge.svg)](https://github.com/yourusername/pda-voice-monitor/actions/workflows/test.yml)

## Features

- 🔌 **Real-time Power Monitoring**: Detects AC adapter connection/disconnection events
- 🎙️ **Text-to-Speech**: Uses Piper TTS with ONNX models for natural voice synthesis
- ⚡ **Non-blocking**: Speech synthesis runs in background threads
- 🎯 **Customizable**: Configure dialogue lines and voice models
- 📝 **Structured Logging**: Detailed debug information for troubleshooting

## Requirements

- **OS**: Linux only (uses `pyudev` for hardware monitoring)
- **Python**: 3.8+
- **AC Power Supply**: System must have AC adapter for monitoring

## Installation

### Prerequisites

- **Linux** (this tool is Linux-specific, uses `pyudev`)
- **Python 3.8+**
- **Piper TTS model file** — download or provide your own (see "Model Setup" below)

### Quick Start

```bash
# 1. Clone or download the project
cd ray

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download/setup the voice model (IMPORTANT: do this before running)
bash setup_model.sh

# 5. Test it
python main.py --once

# 6. Run continuously
python main.py
```

### Model Setup

**The `PDA.onnx` model file is required and must be in place before running.** You have three options:

1. **Automatic download** (recommended for first-time users):
   ```bash
   bash setup_model.sh
   ```
   This downloads a default English US voice. To use a different model:
   ```bash
   bash setup_model.sh "https://url-to-model.onnx" ./models/sound
   ```
   Piper TTS models are available at: https://huggingface.co/rhasspy/piper

2. **Manual setup**: Download a Piper ONNX model and place it at `models/sound/PDA.onnx`

3. **Custom path**: Use environment variable to override the default model location:
   ```bash
   PDA_MODEL_PATH=/path/to/your/model.onnx python main.py
   ```

### System Installation

```bash
# Install as a package (model must already be set up)
pip install .

# Run as a command
pda-monitor --help
```

## Configuration

Edit `config.json` to customize behavior:

```json
{
  "model_path": "./models/sound/PDA.onnx",
  "log_level": "INFO",
  "audio_device": null,
  "plug_in_messages": [
    "External power source detected.",
    "Charging sequence initiated."
  ],
  "plug_out_messages": [
    "Warning. Operating on internal battery.",
    "Battery mode engaged."
  ]
}
```

### Configuration Options

- **model_path**: Path to Piper ONNX model file (default: `./models/sound/PDA.onnx`)
- **log_level**: Logging verbosity: `DEBUG`, `INFO`, `WARNING`, `ERROR` (default: `INFO`)
- **audio_device**: Audio output device ID (default: `null` for system default)
  - Set to device number to use a specific audio device
  - Find available devices: `python -c "import sounddevice; print(sounddevice.query_devices())"`
- **plug_in_messages**: List of messages to announce when charger is connected
- **plug_out_messages**: List of messages to announce when charger is disconnected

### Environment Variables

- `PDA_MODEL_PATH`: Override model path
- `PDA_LOG_LEVEL`: Set logging level (DEBUG, INFO, WARNING, ERROR)

## Usage

### Run as Monitor Service

```bash
python main.py
```

The monitor will listen for power events and announce them continuously. Press `Ctrl+C` to exit.

### Run Once

```bash
python main.py --once
```

Checks current power state and announces it, then exits.

### Custom Model

```bash
PDA_MODEL_PATH="/path/to/custom/model.onnx" python main.py
```

### Custom Audio Device

List available audio devices:

```bash
python -c "import sounddevice; print(sounddevice.query_devices())"
```

Then set `audio_device` in `config.json` to the device ID:

```json
{
  "audio_device": 5
}
```

### Event Behavior

- **Rapid plug/unplug**: If charger events fire faster than speech completes, only the first event is announced (debounce behavior via state check)
- **Initial state**: On startup, current power state is logged but no announcement is made
- **Thread safety**: Audio playback is serialized with locks to prevent overlapping announcements

```
ray/
├── main.py                 # Entry point
├── pda/
│   ├── __init__.py        # Package initialization
│   ├── config.py          # Configuration management
│   ├── voice_engine.py    # Piper TTS wrapper
│   └── power_monitor.py   # Power event monitoring
├── tests/
│   ├── __init__.py
│   └── test_pda.py        # Unit tests
├── models/
│   └── sound/
│       ├── PDA.onnx       # Voice model (ONNX format)
│       └── voices.json    # Voice metadata
├── config.json            # Configuration file
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Package configuration (PEP 517/518)
└── README.md              # This file
```

## Dependencies

- **piper-tts**: Text-to-speech synthesis
- **pyudev**: Linux power supply monitoring
- **numpy**: Audio array handling
- **sounddevice**: Audio playback
- **onnxruntime**: ONNX model inference

See `requirements.txt` for versions.

## Testing

```bash
# Run tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=pda --cov-report=html
```

## Troubleshooting

### No Audio Output

1. Check if audio device is working: `aplay -l`
2. Verify Piper model is valid: `ls -lh models/sound/PDA.onnx`
3. Enable debug logging: `PDA_LOG_LEVEL=DEBUG python main.py`

### "No AC adapter found"

- Your system may not expose power supply info via `pyudev`
- Check: `grep "POWER_SUPPLY" /sys/devices/virtual/power_supply/*/uevent`

### Permission Denied on Power Supply

```bash
# Run with elevated privileges
sudo python main.py
```

## Advanced: Running as Systemd Service

Create `/etc/systemd/system/pda-monitor.service`:

```ini
[Unit]
Description=PDA Power Monitor
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/ray
ExecStart=/path/to/ray/venv/bin/python main.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:

```bash
sudo systemctl enable pda-monitor
sudo systemctl start pda-monitor
sudo systemctl status pda-monitor
```

## Performance

- **Memory**: ~80-120MB with ONNX model loaded
- **CPU**: <5% during monitoring, ~30% during synthesis (brief)
- **Latency**: ~1-3 seconds from power event to voice output

## Limitations

- **Linux-only**: Requires `pyudev` (not available on Windows/macOS)
- **Root access**: May need elevated privileges for `/sys/devices/virtual/power_supply/`
- **Single voice**: Currently supports one voice model at a time

## Future Enhancements

- [ ] Cross-platform support (Windows/macOS)
- [ ] Multiple voice models
- [ ] Web UI for configuration
- [ ] Power profiles (sleep, game mode, etc.)
- [ ] Integration with system power management
- [ ] Advanced debounce/queue strategies for rapid plug/unplug events

## License

MIT License - See LICENSE file

## Contributing

Contributions welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Changelog

### v1.0.0 (2026-07-05)
- Initial production release
- Full configuration support
- Test suite
- Comprehensive documentation
