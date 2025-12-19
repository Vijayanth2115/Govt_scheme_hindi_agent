from gtts import gTTS
import uuid
import os

def make_tts_safe(text: str) -> str:
    replacements = {
        "uttar_pradesh": "उत्तर प्रदेश",
        "andhra_pradesh": "आंध्र प्रदेश",
        "maharashtra": "महाराष्ट्र",

        "male": "पुरुष",
        "female": "महिला",

        "farmer": "किसान",
        "other": "अन्य",

        "PM_KISAN": "प्रधानमंत्री किसान सम्मान निधि",
        "PMAY": "प्रधानमंत्री आवास योजना",
        "AYUSHMAN_BHARAT": "आयुष्मान भारत योजना"
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    return text


def speak_hindi(text: str) -> str:
    """
    Convert Hindi text to speech.
    RETURNS path to generated mp3 file (IMPORTANT for FastAPI)
    """
    if not text:
        raise ValueError("Empty text passed to TTS")

    safe_text = make_tts_safe(text)

    filename = f"tts_{uuid.uuid4()}.mp3"

    tts = gTTS(
        text=safe_text,
        lang="hi",
        slow=False
    )

    tts.save(filename)

    return filename   # 🔑 THIS WAS MISSING
