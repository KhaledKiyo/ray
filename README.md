# PDA Voice Monitor

A Linux system utility that announces power events (plug/unplug) using text-to-speech via Piper TTS and ONNX models.

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
- **Piper TTS model file** (see below)

### Quick Start

```bash
# Clone or download the project
cd ray

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify the model file exists
ls -lh models/sound/PDA.onnx

# Test it
python main.py --once

# Run continuously
python main.py
```

### System Installation

```bash
# Install as a package (requires model file to exist)
pip install .

# Run as a command
pda-monitor --help
```

### Model File Setup

The `PDA.onnx` file (voice model) is not included in the repository. You need to either:

1. **Automatic setup**: Run the provided script (easiest)
   ```bash
   bash setup_model.sh
   ```
   This downloads a default English US model. To use a different model:
   ```bash
   bash setup_model.sh "https://url-to-model.onnx" ./models/sound
   ```

2. **Manual setup**: Place a Piper TTS ONNX model at `models/sound/PDA.onnx`

3. **Environment variable**: `PDA_MODEL_PATH=/path/to/model.onnx python main.py`

**Finding models**: Piper TTS models are available at https://huggingface.co/rhasspy/piper

## Configuration

Edit `config.json` to customize behavior:

```json
{
  "model_path": "./models/sound/PDA.onnx",
  "log_level": "INFO",
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

## Project Structure

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
- [ ] Custom audio output device selection
- [ ] Web UI for configuration
- [ ] Power profiles (sleep, game mode, etc.)
- [ ] Integration with system power management

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
