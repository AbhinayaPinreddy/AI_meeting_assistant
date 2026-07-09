import wave
import contextlib

def get_audio_duration(filepath):
    try:
        with contextlib.closing(wave.open(filepath, "rb")) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)

        minutes = int(duration // 60)
        seconds = int(duration % 60)

        return f"{minutes} min {seconds} sec"

    except Exception:
        return "Unknown"