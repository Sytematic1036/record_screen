"""
Silent Screen Recorder v2
=========================
Skärminspelning utan synlig terminal.

Hotkeys:
  Ctrl+Alt+R  - Starta inspelning
  Ctrl+Alt+Q  - Stoppa inspelning

System tray-ikon visar status:
  - Röd = spelar in
  - Grå = standby
"""

import subprocess
import threading
import sys
import os
from datetime import datetime
from pathlib import Path
import time

try:
    import pystray
    from PIL import Image, ImageDraw
    import keyboard
except ImportError as e:
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
        self.should_be_recording = False  # Flag för trådsäker kommunikation
        self.process = None
        self.output_dir = Path.home() / "Videos" / "Recordings"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.current_file = None
        self.icon = None
        self.last_state = None  # För att spåra ikonändringar

    def create_icon_image(self, color):
        """Skapa en enkel cirkel-ikon."""
        size = 64
        image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        margin = 4
        draw.ellipse([margin, margin, size - margin, size - margin], fill=color)
        return image

    def get_recording_icon(self):
        """Röd ikon för inspelning."""
        return self.create_icon_image((255, 0, 0, 255))

    def get_standby_icon(self):
        """Grå ikon för standby."""
        return self.create_icon_image((128, 128, 128, 255))

    def do_start_recording(self):
        """Faktiskt starta inspelning (körs i huvudtråden)."""
        if self.recording:
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_file = self.output_dir / f"screen_{timestamp}.mp4"

        cmd = [
            "ffmpeg", "-y",
            "-f", "gdigrab",
            "-framerate", "30",
            "-i", "desktop",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "20",
            "-pix_fmt", "yuv420p",
            str(self.current_file)
        ]

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

    def do_stop_recording(self):
        """Faktiskt stoppa inspelning (körs i huvudtråden)."""
        if not self.recording or not self.process:
            return

        try:
            self.process.stdin.write(b'q')
            self.process.stdin.flush()
            self.process.wait(timeout=5)
        except Exception:
            self.process.terminate()
            try:
                self.process.wait(timeout=2)
            except Exception:
                self.process.kill()

        self.recording = False
        self.process = None

        # Ingen notification - bara ikon ändras till grå

    def on_hotkey_start(self):
        """Callback för Ctrl+Alt+R - sätter bara flagga."""
        self.should_be_recording = True

    def on_hotkey_stop(self):
        """Callback för Ctrl+Alt+Q - sätter bara flagga."""
        self.should_be_recording = False

    def quit_app(self, icon=None, item=None):
        """Avsluta applikationen."""
        self.should_be_recording = False
        if self.recording:
            self.do_stop_recording()
        keyboard.unhook_all()
        if self.icon:
            self.icon.stop()

    def setup_hotkeys(self):
        """Registrera globala hotkeys."""
        keyboard.add_hotkey('ctrl+alt+r', self.on_hotkey_start, suppress=True)
        keyboard.add_hotkey('ctrl+alt+q', self.on_hotkey_stop, suppress=True)

    def check_state(self, icon):
        """Körs i bakgrunden - kollar flaggor och uppdaterar."""
        while True:
            # Kolla om vi ska starta/stoppa
            if self.should_be_recording and not self.recording:
                self.do_start_recording()
            elif not self.should_be_recording and self.recording:
                self.do_stop_recording()

            # Uppdatera ikon om status ändrats
            if self.recording != self.last_state:
                self.last_state = self.recording
                if self.recording:
                    icon.icon = self.get_recording_icon()
                    icon.title = "REC - Spelar in (Ctrl+Alt+Q stoppar)"
                else:
                    icon.icon = self.get_standby_icon()
                    icon.title = "Screen Recorder (Ctrl+Alt+R startar)"

            time.sleep(0.1)  # Kolla 10 gånger per sekund

    def run(self):
        """Kör applikationen."""
        menu = pystray.Menu(
            pystray.MenuItem("Starta (Ctrl+Alt+R)",
                           lambda: setattr(self, 'should_be_recording', True)),
            pystray.MenuItem("Stoppa (Ctrl+Alt+Q)",
                           lambda: setattr(self, 'should_be_recording', False)),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Öppna mapp",
                           lambda: os.startfile(str(self.output_dir))),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Avsluta", self.quit_app)
        )

        self.icon = pystray.Icon(
            "screen_recorder",
            self.get_standby_icon(),
            "Screen Recorder (Ctrl+Alt+R startar)",
            menu
        )

        self.setup_hotkeys()

        # Kör state-checker i bakgrundstråd
        checker = threading.Thread(target=self.check_state, args=(self.icon,), daemon=True)
        checker.start()

        self.icon.run()


if __name__ == "__main__":
    recorder = SilentRecorder()
    recorder.run()
