#!/bin/bash
# Rulla tillbaka till version: SILENT_EXP-002_v1_20260216_1900_4022e2a
# Skapad: 2026-02-16 19:00

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET="C:/Users/haege/Kod/record_screen/experiments/EXP-002_silent-recorder/iterations/v1_autonomous_2026-02-16/src"

echo "Rullar tillbaka till: SILENT_EXP-002_v1_20260216_1900_4022e2a"
cp -r "$SCRIPT_DIR/src/"* "$TARGET/"
echo "Klar! Starta om programmet för att aktivera."
