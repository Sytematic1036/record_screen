#!/bin/bash

# ============================================
# Record Screen - Helskärmsinspelning
# Använder FFmpeg för stabil inspelning
# ============================================

set -e

# Standardvärden
OUTPUT="${1:-screen_$(date +%Y%m%d_%H%M%S).mp4}"
FRAMERATE="${2:-30}"
CRF="${3:-20}"

echo "==================================="
echo "  Screen Recorder"
echo "==================================="
echo ""
echo "Output:    $OUTPUT"
echo "Framerate: $FRAMERATE fps"
echo "Kvalitet:  CRF $CRF"
echo ""

# Detektera operativsystem
OS="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    OS="windows"
fi

echo "OS: $OS"
echo ""

# Kontrollera att FFmpeg finns
if ! command -v ffmpeg &> /dev/null; then
    echo "FEL: FFmpeg är inte installerat!"
    echo "Kör setup.sh för att installera."
    exit 1
fi

echo "Startar inspelning..."
echo "Tryck Ctrl+C för att stoppa"
echo ""

# Starta inspelning beroende på OS
case $OS in
    windows)
        ffmpeg -y -f gdigrab -framerate "$FRAMERATE" -i desktop \
            -c:v libx264 -preset veryfast -crf "$CRF" -pix_fmt yuv420p \
            "$OUTPUT"
        ;;
    linux)
        ffmpeg -y -f x11grab -framerate "$FRAMERATE" -i :0.0 \
            -c:v libx264 -preset veryfast -crf "$CRF" -pix_fmt yuv420p \
            "$OUTPUT"
        ;;
    macos)
        ffmpeg -y -f avfoundation -framerate "$FRAMERATE" -i "1:none" \
            -c:v libx264 -preset veryfast -crf "$CRF" -pix_fmt yuv420p \
            "$OUTPUT"
        ;;
    *)
        echo "FEL: Okänt operativsystem"
        exit 1
        ;;
esac

echo ""
echo "==================================="
echo "  Inspelning klar!"
echo "==================================="
echo "Sparad som: $OUTPUT"
