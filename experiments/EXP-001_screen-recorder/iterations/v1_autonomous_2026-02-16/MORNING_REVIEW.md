# Autonom körning 2026-02-16

## Status
[x] LYCKADES / [ ] DELVIS / [ ] MISSLYCKADES

## Sammanfattning
- Skapade experiment: EXP-001_screen-recorder
- Byggde skärminspelningsprogram med FFmpeg
- Testade med faktisk 5-sekunders inspelning
- Video verifierad: 1920x1080, h264, 165 KB

## Nya filer
```
experiments/EXP-001_screen-recorder/
├── EXPERIMENT.md
├── fixtures/
│   └── success_criteria.yaml
├── iterations/v1_autonomous_2026-02-16/
│   ├── MORNING_REVIEW.md
│   ├── notes.md
│   └── src/
│       ├── record.sh      # Shell-skript för inspelning
│       ├── record.py      # Python-wrapper med CLI
│       └── test_recording.mp4  # Testinspelning (5s)
├── learnings.md
├── failures/
└── annotations/
```

## Framgångskriterier
| Kriterium | Status | Test |
|-----------|--------|------|
| FFmpeg installerat | PASS | `ffmpeg -version` |
| Inspelning fungerar | PASS | 5s testinspelning |
| Kan stoppas | PASS | FFmpeg -t flagga |
| Video spelbar | PASS | `ffprobe` visar duration=5.0 |
| Följer repo-patterns | PASS | Shell-skript som setup.sh |

## Tester
```
$ python record.py --duration 5 --output test_recording.mp4
Frame: 103 fps, 4.86s, 165 KB

$ ffprobe test_recording.mp4
codec_name=h264
width=1920
height=1080
duration=5.000000
```

## Problem & lösningar
1. **Problem:** `process.terminate()` korrupterade video (ingen moov atom)
   **Lösning:** Använd FFmpeg `-t` flagga för duration istället

2. **Problem:** subprocess.PIPE för stderr fylldes upp och blockerade
   **Lösning:** Sätt `stderr=None` så FFmpeg-output går till konsolen

## Rekommenderade nästa steg
1. Granska kod: `git diff`
2. Testa manuellt: `python record.py --duration 10`
3. Om OK: commit och push till target repo
4. Kopiera `src/record.py` och `src/record.sh` till repo root
