import requests
import time
import os

RECOGNIZE_URL = "https://api.speechtext.ai/recognize"
RESULTS_URL = "https://api.speechtext.ai/results"

API_KEY = os.getenv("SPEECHTEXT_API_KEY")
if not API_KEY:
    raise RuntimeError("SPEECHTEXT_API_KEY is missing")


def speech_to_text(audio_file: str) -> str:
    """
    Convert Hindi audio file to Hindi text using SpeechText.ai
    """
    with open(audio_file, "rb") as f:
        audio_bytes = f.read()

    headers = {
        "Content-Type": "application/octet-stream"
    }

    params = {
        "key": API_KEY,
        "language": "hi-IN",
        "punctuation": True,
        "format": "wav"   # IMPORTANT: ensure input is WAV
    }

    response = requests.post(
        RECOGNIZE_URL,
        headers=headers,
        params=params,
        data=audio_bytes,
        timeout=60
    )

    r = response.json()

    if "id" not in r:
        raise RuntimeError(f"STT failed: {r}")

    task_id = r["id"]

    # Poll results
    while True:
        res = requests.get(
            RESULTS_URL,
            params={
                "key": API_KEY,
                "task": task_id
            },
            timeout=30
        ).json()

        if "status" not in res:
            break

        if res["status"] == "failed":
            raise RuntimeError("STT task failed")

        if res["status"] == "finished":
            break

        time.sleep(4)

    transcript = res.get("results", {}).get("transcript", "")
    return transcript.strip()
