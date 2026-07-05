#!/usr/bin/env bash
# Download Piper TTS ONNX model
# Usage: ./setup_model.sh [model_url] [output_path]

set -e

# Defaults
MODEL_URL="${1:-https://huggingface.co/rhasspy/piper/resolve/main/en/en_US/amy/medium/en_US-amy-medium.onnx}"
OUTPUT_DIR="${2:-./models/sound}"
FILENAME="PDA.onnx"

echo "🎙️ Setting up Piper TTS model..."
echo "URL: $MODEL_URL"
echo "Output: $OUTPUT_DIR/$FILENAME"

# Create directory
mkdir -p "$OUTPUT_DIR"

# Check if already exists
if [ -f "$OUTPUT_DIR/$FILENAME" ]; then
    echo "✓ Model already exists at $OUTPUT_DIR/$FILENAME"
    ls -lh "$OUTPUT_DIR/$FILENAME"
    exit 0
fi

# Download model
if command -v wget &> /dev/null; then
    echo "📥 Downloading (using wget)..."
    wget -q --show-progress -O "$OUTPUT_DIR/$FILENAME" "$MODEL_URL"
elif command -v curl &> /dev/null; then
    echo "📥 Downloading (using curl)..."
    curl -L -o "$OUTPUT_DIR/$FILENAME" "$MODEL_URL"
else
    echo "✗ Please install wget or curl"
    exit 1
fi

if [ -f "$OUTPUT_DIR/$FILENAME" ]; then
    echo "✓ Model downloaded successfully"
    ls -lh "$OUTPUT_DIR/$FILENAME"
else
    echo "✗ Download failed"
    exit 1
fi
