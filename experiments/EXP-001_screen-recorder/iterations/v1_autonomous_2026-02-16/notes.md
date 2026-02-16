# Notes - v1_autonomous_2026-02-16

## Approach
Skapade två filer:
- `record.sh` - Shell-skript som matchar target repos stil (setup.sh)
- `record.py` - Python-wrapper för mer kontroll och CLI

## Kod-beslut

### Varför Python wrapper?
Shell-skript är bra för enkla "kör och glöm" inspelningar, men Python ger:
- Argparse CLI med hjälptext
- Verifiering att fil skapades
- Filstorlek-output
- Bättre felhantering

### Varför -t istället för signal?
Se `failures/terminate_corrupts_video.md`.

## Test-resultat
```
Input: 30 fps, 1920x1080
Output: h264, CRF 20, veryfast preset
Duration: 5.00s (exact)
Frames: 103
Size: 165 KB
Bitrate: 278 kbits/s
```

## OS-stöd
Koden stödjer:
- Windows: gdigrab (testat)
- Linux: x11grab (ej testat)
- macOS: avfoundation (ej testat)
