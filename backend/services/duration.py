from pydub import AudioSegment

def get_audio_duration(filepath):

    audio = AudioSegment.from_file(filepath)

    duration = len(audio) // 1000

    minutes = duration // 60
    seconds = duration % 60

    return f"{minutes} min {seconds} sec"