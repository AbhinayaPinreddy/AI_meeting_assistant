import requests

COLAB_URL = "https://halves-valuables-earwig.ngrok-free.dev/diarize"

def get_speaker_transcript(audio_path):
    print("Opening file...")

    with open(audio_path, "rb") as f:
        print("Sending POST request...")

        response = requests.post(
            COLAB_URL,
            files={"file": f},
            timeout=60
        )

        print("Response received:", response.status_code)

    response.raise_for_status()

    print("Parsing JSON...")

    return response.json()["speaker_transcript"]