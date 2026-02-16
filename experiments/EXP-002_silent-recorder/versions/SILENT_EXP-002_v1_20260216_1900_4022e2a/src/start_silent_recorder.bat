@echo off
:: Startar Silent Screen Recorder i bakgrunden
:: Använder pythonw.exe för att undvika terminal

cd /d "%~dp0"
start "" pythonw.exe silent_recorder.pyw
