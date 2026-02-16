# EXP-001: Screen Recorder

## Status
`EXPERIMENTAL`

## Mål
Bygg ett program för att spela in hela bildskärmen med ffmpeg. Programmet ska:
- Vara enkelt att använda
- Fungera på Windows (primärt)
- Använda ffmpeg för stabil inspelning
- Kunna startas och stoppas programmatiskt

## Bygger från
Inget tidigare experiment - detta är det första.

## Target Repo
https://github.com/Sytematic1036/record_screen

## Teknisk approach
- Shell/Bash-skript (matchar target repo som är Shell-baserat)
- Python-wrapper för enkel start/stopp
- ffmpeg med gdigrab för Windows

## Framgångskriterier
Se `fixtures/success_criteria.yaml`

## Skapad
2026-02-16 (autonom körning)
