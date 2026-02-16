# Failure: process.terminate() korrupterar video

## Datum
2026-02-16

## Vad jag försökte
Stoppa FFmpeg-inspelning med `process.terminate()` efter en angiven tid.

## Vad som hände
```
$ ffprobe test_recording.mp4
[mov,mp4,m4a,3gp,3g2,mj2 @ ...] moov atom not found
test_recording.mp4: Invalid data found when processing input
```

## Varför det misslyckades
MP4-formatet kräver en "moov atom" som skrivs i slutet av filen. Den innehåller metadata om alla video-frames. När FFmpeg termineras abrupt hinner den inte skriva moov atom.

## Alternativa lösningar testade

1. **Skicka 'q' till stdin** - Fungerar i teorin men subprocess stdin är problematiskt
2. **SIGINT/SIGTERM** - Samma problem som terminate()
3. **FFmpeg -t flagga** - FUNGERAR! FFmpeg hanterar avslutning internt

## Lösning som användes
```python
# Lägg till -t i ffmpeg-kommandot
if duration:
    output_args.extend(["-t", str(duration)])
```

## Lärdomar
- Låt verktyg hantera sin egen lifecycle när möjligt
- FFmpeg har inbyggda flags för nästan allt
- `terminate()` är en nödlösning, inte förstaval
