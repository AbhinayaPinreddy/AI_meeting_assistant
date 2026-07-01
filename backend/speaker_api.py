import requests

COLAB_URL = "https://halves-valuables-earwig.ngrok-free.dev/diarize"

def get_speaker_transcript(audio_path):

    with open(audio_path, "rb") as f:

        response = requests.post(
            COLAB_URL,
            files={"file": f}
        )

    response.raise_for_status()

    return response.json()["speaker_transcript"]