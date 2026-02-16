# Learnings - EXP-001 Screen Recorder

## Vad fungerade

### FFmpeg -t flagga
Att ge FFmpeg duration direkt med `-t` är mycket stabilare än att försöka stoppa processen manuellt. FFmpeg avslutar korrekt och skriver moov atom.

### gdigrab på Windows
`-f gdigrab -i desktop` fungerar utmärkt för helskärmsinspelning på Windows. Ingen extra konfiguration behövs.

### CRF 20 + veryfast preset
Bra balans mellan kvalitet och filstorlek. 5 sekunder 1920x1080 = ~165 KB.

## Vad INTE fungerade

### process.terminate()
FFmpeg måste avslutas korrekt för att skriva moov atom till mp4-filen. `terminate()` avbryter mitt i och korrupterar filen.

Se `failures/terminate_corrupts_video.md` för detaljer.

### subprocess.PIPE för stderr
FFmpegs stderr-output fyller upp buffern snabbt och blockerar processen. Använd `stderr=None` för att visa output direkt i konsolen istället.

## Patterns för framtida experiment

1. **Använd FFmpeg flags istället för manuell kontroll** - `-t duration`, `-ss start` etc.
2. **Låt stderr gå till konsolen** för kommandoradsprogram med mycket output
3. **Testa med kort duration först** (5s) innan längre inspelningar
