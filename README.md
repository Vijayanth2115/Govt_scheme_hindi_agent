**Hindi Government Scheme Voice Agent**



A voice-first, agentic AI system that helps users identify and apply for Indian government welfare schemes through natural Hindi voice conversations.



This project goes beyond a chatbot by implementing a state-machine–based agent that can autonomously reason, ask follow-up questions, confirm user inputs, use tools, maintain memory across turns, and handle failures — all via voice input and voice output.



 **Key Features**



* Voice-first interaction (Hindi only)
* End-to-end pipeline: STT → Agent → Tools → TTS
* True agentic workflow using an explicit state machine
* Conversation memory across turns via session management
* Tool usage for eligibility checks and scheme retrieval
* Failure handling for unclear or incomplete user inputs
* Zoom-style frontend UI simulating a live voice call
* Hindi audio responses (TTS)





**System Architecture**



User (Hindi Voice)

&nbsp;  ↓

Frontend (Mic + Session)

&nbsp;  ↓

FastAPI Backend (/voice)

&nbsp;  ↓

Speech-to-Text (Hindi)

&nbsp;  ↓

Agent (State Machine + Memory)

&nbsp;  ↓

Tools (Eligibility Engine, Scheme KB)

&nbsp;  ↓

Text-to-Speech (Hindi)

&nbsp;  ↓

Audio Response → User







**Tooling**



The agent uses multiple tools during execution:



**1.Eligibility Engine**



Determines which schemes the user qualifies for based on:



* Age
* Income
* State
* Category
* Gender
* Occupation



**2.Scheme Knowledge Base**



Provides:



* Scheme name (Hindi)
* Required documents
* Application steps
* Tools are invoked dynamically based on agent state.







**Project Structure**



**govt-scheme-voice-agent/**

**├── backend/**

**│   ├── main.py              # FastAPI app**

**│   ├── agent.py             # State-machine agent**

**│   ├── memory.py            # Session-based memory**

**│   ├── tools.py             # Eligibility \& scheme tools**

**│   ├── stt.py               # Hindi Speech-to-Text**

**│   ├── tts.py               # Hindi Text-to-Speech**

**│--── requirements.txt**

**│**

**├── frontend/**

**│   └── zoom\_style.html      # Zoom-like voice UI**

**│**

**├── docs/**

**│   ├── architecture.md**

**│   └── architecture\_diagram.png**

**│**

**├── transcripts/**

**│   ├── success\_case.md**

**│   ├── failure\_case.md**

**│   └── edge\_case.md**

**│**

**└── README.md**



**How to Run the Project**



**1.Backend Setup**



&nbsp;	cd backend

&nbsp;	pip install -r requirements.txt

&nbsp;	uvicorn main:app --reload

&nbsp;  Backend runs at:

&nbsp;	http://127.0.0.1:8000

**2. Frontend (Voice UI)**



* Open frontend/zoom\_style.html in a browser
* Allow microphone access
* Click 🎙️ to speak in Hindi
* The agent replies via audio



&nbsp; The frontend automatically:



* Sends audio to backend
* Reuses session ID
* Plays Hindi audio response





**Sample Conversation**



**User (voice):**

“मुझे सरकारी योजनाओं के बारे में जानकारी चाहिए”



**Agent (voice):**

“नमस्कार। मैं एक सरकारी योजना सहायक हूँ।

सबसे पहले, कृपया अपनी उम्र बताइए।”



**Failure Handling**

* Unclear audio → Agent politely asks user to repeat
* Contradictory inputs → Agent re-confirms values
* Missing information → Agent explicitly requests it







