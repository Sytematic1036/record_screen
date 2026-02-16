#!/bin/bash

# ============================================
# Setup-skript för record_screen-projektet
# Helskärmsinspelning med FFmpeg
# ============================================

set -e

echo "==================================="
echo "  Record Screen - Setup"
echo "==================================="
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

echo "Detekterat OS: $OS"
echo ""

# Funktion för att kontrollera om FFmpeg är installerat
check_ffmpeg() {
    if command -v ffmpeg &> /dev/null; then
        echo "✓ FFmpeg är redan installerat"
        ffmpeg -version | head -n 1
        return 0
    else
        return 1
    fi
}

# Installera FFmpeg beroende på OS
install_ffmpeg() {
    echo "Installerar FFmpeg..."
    echo ""

    case $OS in
        linux)
            echo "Kör: sudo apt-get update && sudo apt-get install -y ffmpeg"
            sudo apt-get update
            sudo apt-get install -y ffmpeg
            ;;
        macos)
            if command -v brew &> /dev/null; then
                echo "Kör: brew install ffmpeg"
                brew install ffmpeg
            else
                echo "❌ Homebrew är inte installerat."
                echo "Installera Homebrew först: https://brew.sh"
                exit 1
            fi
            ;;
        windows)
            echo "❌ Automatisk installation stöds inte på Windows."
            echo ""
            echo "Följ dessa steg manuellt:"
            echo "1. Ladda ner FFmpeg från https://ffmpeg.org/download.html"
            echo "2. Packa upp till C:\\ffmpeg"
            echo "3. Lägg till C:\\ffmpeg\\bin i systemets PATH"
            echo ""
            echo "Eller använd winget:"
            echo "  winget install FFmpeg"
            echo ""
            echo "Eller använd Chocolatey:"
            echo "  choco install ffmpeg"
            ;;
        *)
            echo "❌ Okänt operativsystem"
            exit 1
            ;;
    esac
}

# Huvudlogik
echo "Kontrollerar FFmpeg..."
if ! check_ffmpeg; then
    echo ""
    read -p "FFmpeg hittades inte. Vill du installera det? (j/n): " choice
    if [[ "$choice" == "j" ]] || [[ "$choice" == "J" ]] || [[ "$choice" == "y" ]] || [[ "$choice" == "Y" ]]; then
        install_ffmpeg
    else
        echo "Hoppar över FFmpeg-installation."
    fi
fi

echo ""
echo "==================================="
echo "  Setup klar!"
echo "==================================="
echo ""
echo "Nästa steg:"
echo "  - Läs dokumentationen i ffmpeg_fullscreen_recording_only.md"
echo "  - Testa inspelning med kommandot:"
echo ""
if [[ "$OS" == "windows" ]]; then
    echo '    ffmpeg -y -f gdigrab -framerate 30 -i desktop -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p screen.mp4'
elif [[ "$OS" == "linux" ]]; then
    echo '    ffmpeg -y -f x11grab -framerate 30 -i :0.0 -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p screen.mp4'
elif [[ "$OS" == "macos" ]]; then
    echo '    ffmpeg -y -f avfoundation -framerate 30 -i "1:none" -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p screen.mp4'
fi
echo ""
echo "Stoppa inspelning med Ctrl+C"
echo ""
