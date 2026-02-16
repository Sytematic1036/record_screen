# Helskärmsinspelning med FFmpeg (stabil och hög kvalitet)

Detta dokument beskriver enbart hur du spelar in **hela skärmen** med FFmpeg, samt hur du startar och stoppar inspelningen från Python.

Detta är den mest stabila och kvalitativa metoden för skärminspelning.

---

## Installation

### Windows
1. Ladda ner FFmpeg från https://ffmpeg.org  
2. Packa upp (t.ex. `C:\ffmpeg`)  
3. Lägg till `C:\ffmpeg\bin` i systemets PATH  

Verifiera:
```bash
ffmpeg -version
```

---

### macOS
```bash
brew install ffmpeg
```

Verifiera:
```bash
ffmpeg -version
```

---

### Ubuntu / Debian
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

Verifiera:
```bash
ffmpeg -version
```

---

# Spela in HELA skärmen (terminal)

## Windows

```bash
ffmpeg -y -f gdigrab -framerate 30 -i desktop ^
-c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p screen.mp4
```

Stoppa med:
```
Ctrl + C
```

---

## Linux

```bash
ffmpeg -y -f x11grab -framerate 30 -i :0.0 \
-c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p screen.mp4
```

---

## macOS (FFmpeg)

Lista tillgängliga enheter:
```bash
ffmpeg -f avfoundation -list_devices true -i ""
```

Spela in helskärm (byt device-index vid behov):
```bash
ffmpeg -y -f avfoundation -framerate 30 -i "1:none" \
-c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p screen.mp4
```

Alternativt (enklast på mac):
```
Cmd + Shift + 5
```

---

# Python: starta och stoppa helskärmsinspelning

## Windows-exempel

```python
import subprocess
import time

output = "screen.mp4"

process = subprocess.Popen([
    "ffmpeg",
    "-y",
    "-f", "gdigrab",
    "-framerate", "30",
    "-i", "desktop",
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-crf", "20",
    "-pix_fmt", "yuv420p",
    output
])

print("Spelar in helskärm...")

time.sleep(10)  # Spelar in 10 sekunder

process.terminate()

print("Inspelning klar:", output)
```

---

# Rekommenderade inställningar

| Inställning | Rekommendation |
|------------|---------------|
| FPS | 30 |
| CRF | 18–22 (20 är bra standard) |
| Codec | libx264 |
| Preset | veryfast |
| Format | mp4 |

---

# Sammanfattning

- FFmpeg är stabilast för helskärmsinspelning  
- Fungerar utmärkt att starta/stoppa från Python  
- Ger hög kvalitet och liten filstorlek  
- Perfekt för presentationer och demos  

