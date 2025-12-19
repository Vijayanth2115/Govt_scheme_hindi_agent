import os
import uuid
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from agent import GovtSchemeAgent
from memory import AgentMemory
from stt import speech_to_text
from tts import speak_hindi, make_tts_safe

# =========================
# FastAPI App
# =========================
app = FastAPI(
    title="Hindi Government Scheme Voice Agent",
    description="Voice-to-voice Hindi conversational agent for government schemes",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Session-ID"]
)

# =========================
# Session Store
# =========================
SESSIONS = {}

def get_session(session_id: str) -> GovtSchemeAgent:
    if session_id not in SESSIONS:
        memory = AgentMemory()
        agent = GovtSchemeAgent(memory)
        SESSIONS[session_id] = agent
    return SESSIONS[session_id]

# =========================
# Voice Endpoint
# =========================
@app.post("/voice")
async def voice_agent(
    audio: UploadFile = File(...),
    session_id: str | None = Form(None)
):
    """
    Voice-to-voice Hindi government scheme agent.
    User always sends audio first.
    """

    if not session_id:
        session_id = str(uuid.uuid4())

    agent = get_session(session_id)

    audio_path = f"input_{uuid.uuid4()}_{audio.filename}"
    collected_reply = []
    # print("audio_path:\n",audio_path)

    try:
        # ---------- Save audio ----------
        with open(audio_path, "wb") as f:
            f.write(await audio.read())

        # ---------- Speech-to-Text ----------
        user_text = speech_to_text(audio_path).strip()
        print("user_text:\n",user_text)
        

        # ---------- First agent step ----------
        reply = agent.step(user_text)
        print("reply:\n",reply)
        if reply:
            collected_reply.append(reply)

        # ---------- Auto-run states (EXACTLY like run.py) ----------
        while True:
            if agent.state in ["INTRO", "CHECK_ELIGIBILITY", "FETCH_ALL"]:
                reply = agent.step("")
                if reply:
                    collected_reply.append(reply)
                continue

            if reply is None:
                reply = agent.step("")
                if reply:
                    collected_reply.append(reply)
                continue

            break

        final_reply = "\n".join(collected_reply)
        print("final_reply:\n",final_reply)

        # ---------- Text-to-Speech ----------
        safe_text = make_tts_safe(final_reply)
        
        audio_reply_path = speak_hindi(safe_text)
        # print("audio_reply_path:\n",audio_reply_path)

        return FileResponse(
            audio_reply_path,
            media_type="audio/mpeg",
            filename="response.mp3",
            headers={
                "X-Session-ID": session_id
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)

# =========================
# Reset Endpoint
# =========================
@app.post("/reset")
def reset_session(session_id: str):
    if session_id in SESSIONS:
        del SESSIONS[session_id]
        return {"status": "reset"}
    return {"status": "session_not_found"}
