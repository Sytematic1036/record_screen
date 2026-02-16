# EXP-002: Silent Screen Recorder

## Status
`EXPERIMENTAL`

## Mål
Förbättrad skärminspelare som:
1. Körs helt i bakgrunden (ingen terminal)
2. Visar röd system tray-ikon under inspelning
3. Startas med Ctrl+Alt+R
4. Stoppas med Ctrl+Alt+Q

## Bygger från
EXP-001_screen-recorder

## Teknisk approach
- Python med pystray för system tray-ikon
- pythonw.exe för att köra utan terminal
- keyboard-bibliotek för globala hotkeys
- ffmpeg subprocess i bakgrunden

## Framgångskriterier
Se `fixtures/success_criteria.yaml`

## Skapad
2026-02-16 (autonom körning)
