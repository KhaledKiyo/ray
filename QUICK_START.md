# Quick Start Guide

## Installation (60 seconds)

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Verify it works
python main.py --help

# 3. Check current power state
python main.py --once

# 4. Run continuously
python main.py
```

## Common Commands

```bash
# Run with verbose logging
python main.py --verbose

# Use custom config
python main.py --config my-config.json

# Install as package
pip install .

# Run package command
pda-monitor --help
```

## Configuration

Edit `config.json`:

```json
{
  "model_path": "./models/sound/PDA.onnx",
  "log_level": "INFO",
  "plug_in_messages": [
    "Power connected.",
    "Charging started."
  ],
  "plug_out_messages": [
    "Running on battery.",
    "Power lost."
  ]
}
```

Or use environment variables:

```bash
export PDA_LOG_LEVEL=DEBUG
export PDA_MODEL_PATH="/custom/path/model.onnx"
python main.py
```

## Development

```bash
# Install dev dependencies
make dev

# Run tests
make test

# Format code
make format

# Check code quality
make lint

# All tasks
make help
```

## Troubleshooting

**No sound output?**
```bash
# Check audio device
aplay -l

# Test with verbose logging
python main.py --verbose
```

**Model not found?**
```bash
# Check model path
ls -lh models/sound/PDA.onnx

# Override with env var
PDA_MODEL_PATH="/path/to/model.onnx" python main.py
```

**Permission errors?**
```bash
# May need root for power monitoring
sudo python main.py
```

## Next Steps

1. Read [README.md](README.md) for full documentation
2. Check [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
3. See [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md) for status
4. Review [tests/test_pda.py](tests/test_pda.py) for usage examples

## Files Reference

| File | Purpose |
|------|---------|
| main.py | CLI entry point |
| pda/ | Core package |
| config.json | Configuration |
| tests/ | Test suite |
| Makefile | Dev tasks |
| README.md | Full docs |
