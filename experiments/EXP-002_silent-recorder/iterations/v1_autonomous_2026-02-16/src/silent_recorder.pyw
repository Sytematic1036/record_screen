"""
Silent Screen Recorder
======================
Skärminspelning utan synlig terminal.

Hotkeys:
  Ctrl+Alt+R  - Starta inspelning
  Ctrl+Alt+Q  - Stoppa inspelning

System tray-ikon visar status:
  - Röd = spelar in
  - Grå = standby (väntar på Ctrl+Alt+R)
"""

import subprocess
import threading
import sys
import os
from datetime import datetime
from pathlib import Path

# Försök importera nödvändiga bibliotek
try:
    import pystray
    from PIL import Image, ImageDraw
    import keyboard
except ImportError as e:
    # Visa felmeddelande via Windows notification
    import ctypes
    ctypes.windll.user32.MessageBoxW(
        0,
        f"Saknar bibliotek: {e}\n\nKör: pip install pystray pillow keyboard",
        "Silent Recorder - Fel",
        0x10
    )
    sys.exit(1)


class SilentRecorder:
    def __init__(self):
        self.recording = False
        self.process = None
        self.output_dir = Path.home() / "Videos" / "Recordings"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.current_file = None
        self.icon = None

    def create_icon_image(self, color):
        """Skapa en enkel cirkel-ikon."""
        size = 64
        image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        # Rita en fylld cirkel
        margin = 4
        draw.ellipse([margin, margin, size - margin, size - margin], fill=color)
        return image

    def get_recording_icon(self):
        """Röd ikon för inspelning."""
        return self.create_icon_image((255, 50, 50, 255))

    def get_standby_icon(self):
        """Grå ikon för standby."""
        return self.create_icon_image((128, 128, 128, 255))

    def start_recording(self):
        """Starta skärminspelning."""
        if self.recording:
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_file = self.output_dir / f"screen_{timestamp}.mp4"

        cmd = [
            "ffmpeg",
            "-y",
            "-f", "gdigrab",
            "-framerate", "30",
            "-i", "desktop",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "20",
            "-pix_fmt", "yuv420p",
            str(self.current_file)
        ]

        # Starta ffmpeg helt tyst (ingen konsol)
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE

        self.process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            startupinfo=startupinfo,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        self.recording = True
        self.update_icon()

        # Visa notification att inspelning startade
        self.show_notification("REC - Inspelning startad! (Ctrl+Alt+Q för stopp)")

    def stop_recording(self):
        """Stoppa skärminspelning."""
        if not self.recording or not self.process:
            return

        try:
            # Skicka 'q' till ffmpeg för att avsluta korrekt
            self.process.stdin.write(b'q')
            self.process.stdin.flush()
            self.process.wait(timeout=5)
        except Exception:
            # Fallback: terminera processen
            self.process.terminate()
            try:
                self.process.wait(timeout=2)
            except Exception:
                self.process.kill()

        self.recording = False
        self.process = None
        self.update_icon()

        # Visa notification om sparad fil
        self.show_notification(f"Sparad: {self.current_file.name}")

    def show_notification(self, message):
        """Visa Windows notification."""
        if self.icon:
            self.icon.notify(message, "Screen Recorder")

    def update_icon(self):
        """Uppdatera tray-ikonen baserat på status."""
        if self.icon:
            try:
                if self.recording:
                    new_icon = self.get_recording_icon()
                    new_title = "REC - Spelar in... (Ctrl+Alt+Q för att stoppa)"
                else:
                    new_icon = self.get_standby_icon()
                    new_title = "Screen Recorder (Ctrl+Alt+R för att starta)"

                # Uppdatera ikon och titel
                self.icon.icon = new_icon
                self.icon.title = new_title

                # Tvinga uppdatering av menyn också
                self.icon.update_menu()
            except Exception:
                pass  # Ignorera fel vid uppdatering

    def toggle_recording(self):
        """Växla mellan inspelning och stopp."""
        if self.recording:
            self.stop_recording()
        else:
            self.start_recording()

    def on_hotkey_start(self):
        """Callback för Ctrl+Alt+R."""
        if not self.recording:
            self.start_recording()

    def on_hotkey_stop(self):
        """Callback för Ctrl+Alt+Q."""
        if self.recording:
            self.stop_recording()

    def quit_app(self, icon=None, item=None):
        """Avsluta applikationen."""
        if self.recording:
            self.stop_recording()
        keyboard.unhook_all()
        if self.icon:
            self.icon.stop()

    def setup_hotkeys(self):
        """Registrera globala hotkeys."""
        keyboard.add_hotkey('ctrl+alt+r', self.on_hotkey_start, suppress=True)
        keyboard.add_hotkey('ctrl+alt+q', self.on_hotkey_stop, suppress=True)

    def run(self):
        """Kör applikationen."""
        # Skapa menyn för tray-ikonen
        menu = pystray.Menu(
            pystray.MenuItem("Starta inspelning (Ctrl+Alt+R)",
                           lambda: self.start_recording(),
                           visible=lambda item: not self.recording),
            pystray.MenuItem("Stoppa inspelning (Ctrl+Alt+Q)",
                           lambda: self.stop_recording(),
                           visible=lambda item: self.recording),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Öppna Recordings-mapp",
                           lambda: os.startfile(str(self.output_dir))),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Avsluta", self.quit_app)
        )

        # Skapa tray-ikonen
        self.icon = pystray.Icon(
            "screen_recorder",
            self.get_standby_icon(),
            "Screen Recorder (Ctrl+Alt+R för att starta)",
            menu
        )

        # Starta hotkey-lyssnare i egen tråd
        self.setup_hotkeys()

        # Kör tray-ikonen (blockerar)
        self.icon.run()


if __name__ == "__main__":
    recorder = SilentRecorder()
    recorder.run()
