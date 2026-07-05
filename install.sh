#!/usr/bin/env bash
# Installation script for PDA Voice Monitor

set -e

echo "🔌 PDA Voice Monitor Installation"
echo "=================================="

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "✓ Found Python $PYTHON_VERSION"

if [[ ! $PYTHON_VERSION =~ ^3\.[8-9]|^3\.1[0-2] ]]; then
    echo "✗ Python 3.8+ required"
    exit 1
fi

# Check Linux
if [[ "$OSTYPE" != "linux"* ]]; then
    echo "✗ This application requires Linux"
    exit 1
fi
echo "✓ Running on Linux"

# Create venv
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip > /dev/null
pip install -q -r requirements.txt

# Verify config
if [ ! -f "config.json" ]; then
    echo "⚠️  config.json not found, copying template..."
    cp config.json.example config.json 2>/dev/null || echo "{}" > config.json
fi

# Test import
echo "🧪 Testing imports..."
python -c "from pda import VoiceEngine, PowerMonitor, Config; print('✓ All imports OK')"

echo ""
echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Activate venv: source venv/bin/activate"
echo "2. Edit config.json with your preferences"
echo "3. Run: python main.py --help"
echo "4. Start monitoring: python main.py"
