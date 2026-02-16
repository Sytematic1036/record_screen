#!/usr/bin/env python3
"""
Screen Recorder - Python wrapper för FFmpeg skärminspelning

Användning:
    python record.py                    # Spela in tills Ctrl+C
    python record.py --duration 10      # Spela in 10 sekunder
    python record.py --output video.mp4 # Ange filnamn
"""

import subprocess
import sys
import time
import signal
import argparse
from pathlib import Path
from datetime import datetime


def get_ffmpeg_command(output: str, framerate: int = 30, crf: int = 20, duration: int = None) -> list:
    """Returnerar FFmpeg-kommando baserat på OS."""

    base_args = [
        "ffmpeg",
        "-y",  # Skriv över utan att fråga
    ]

    # Windows-specifika argument
    if sys.platform == "win32":
        input_args = ["-f", "gdigrab", "-framerate", str(framerate), "-i", "desktop"]
    elif sys.platform == "darwin":
        input_args = ["-f", "avfoundation", "-framerate", str(framerate), "-i", "1:none"]
    else:  # Linux
        input_args = ["-f", "x11grab", "-framerate", str(framerate), "-i", ":0.0"]

    output_args = [
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", str(crf),
        "-pix_fmt", "yuv420p",
    ]

    # Om duration anges, lägg till -t flaggan
    if duration:
        output_args.extend(["-t", str(duration)])

    output_args.append(output)

    return base_args + input_args + output_args


def record_screen(output: str = None, duration: int = None, framerate: int = 30, crf: int = 20) -> Path:
    """
    Spelar in skärmen.

    Args:
        output: Filnamn för output (default: screen_YYYYMMDD_HHMMSS.mp4)
        duration: Inspelningstid i sekunder (None = tills Ctrl+C)
        framerate: Bildfrekvens (default: 30)
        crf: Kvalitet 0-51, lägre = bättre (default: 20)

    Returns:
        Path till den sparade videofilen
    """

    if output is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = f"screen_{timestamp}.mp4"

    output_path = Path(output)

    print("=" * 40)
    print("  Screen Recorder")
    print("=" * 40)
    print()
    print(f"Output:    {output_path}")
    print(f"Framerate: {framerate} fps")
    print(f"Kvalitet:  CRF {crf}")
    print(f"Duration:  {duration}s" if duration else "Duration:  Tills Ctrl+C")
    print()

    cmd = get_ffmpeg_command(str(output_path), framerate, crf, duration)

    print("Startar inspelning...")
    if not duration:
        print("Tryck Ctrl+C för att stoppa")
    print()

    # Starta FFmpeg-processen
    # Använd DEVNULL för stdout, låt stderr gå till konsolen för feedback
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=None  # Visa FFmpeg-output i konsolen
    )

    def stop_recording(signum=None, frame=None):
        """Stoppar inspelningen genom att skicka 'q' till FFmpeg."""
        print("\nStoppar inspelning...")
        try:
            # Skicka 'q' till FFmpeg för att avsluta korrekt (skriver moov atom)
            process.stdin.write(b'q')
            process.stdin.flush()
        except (BrokenPipeError, OSError):
            # Om stdin redan är stängd, använd terminate som fallback
            process.terminate()

    # Registrera signal handler för Ctrl+C
    signal.signal(signal.SIGINT, stop_recording)
    signal.signal(signal.SIGTERM, stop_recording)

    try:
        # Vänta på att FFmpeg avslutas (hanterar duration internt med -t)
        process.wait()
    except KeyboardInterrupt:
        stop_recording()
        process.wait()

    print()
    print("=" * 40)
    print("  Inspelning klar!")
    print("=" * 40)
    print(f"Sparad som: {output_path}")

    # Verifiera att filen skapades
    if output_path.exists():
        size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"Filstorlek: {size_mb:.2f} MB")
    else:
        print("VARNING: Filen skapades inte!")

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Spela in skärmen med FFmpeg",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exempel:
  python record.py                     # Spela in tills Ctrl+C
  python record.py --duration 10       # Spela in 10 sekunder
  python record.py -o demo.mp4 -d 30   # Spela in 30s till demo.mp4
        """
    )

    parser.add_argument(
        "-o", "--output",
        help="Output-filnamn (default: screen_YYYYMMDD_HHMMSS.mp4)"
    )
    parser.add_argument(
        "-d", "--duration",
        type=int,
        help="Inspelningstid i sekunder (default: tills Ctrl+C)"
    )
    parser.add_argument(
        "-f", "--framerate",
        type=int,
        default=30,
        help="Bildfrekvens (default: 30)"
    )
    parser.add_argument(
        "-q", "--quality",
        type=int,
        default=20,
        dest="crf",
        help="Kvalitet CRF 0-51, lägre=bättre (default: 20)"
    )

    args = parser.parse_args()

    record_screen(
        output=args.output,
        duration=args.duration,
        framerate=args.framerate,
        crf=args.crf
    )


if __name__ == "__main__":
    main()
