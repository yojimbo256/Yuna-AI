# 🧠 Yuna AI – Personal Cognitive Assistant

**Version:** 1.0.0  
📅 **Last Updated:** March 15, 2025  

---

## 🌟 What is Yuna?

**Yuna AI** is a **modular cognitive assistant** designed to support **personal memory recall, behavioral adaptation, and reasoning** through a flexible, API-first architecture.

Key features:
- ✅ Persistent long-term memory with vector search
- ✅ Conversational reasoning powered by LLMs
- ✅ Behavior adaptation through feedback loops
- ✅ Cloud GPU offloading for compute-heavy tasks
- ✅ FastAPI backend + Streamlit UI for local interaction

---

## 🧩 Architecture Overview

```text
Yuna-AI/
│
├── src/
│   └── api/
│       ├── adaptive_decision_engine.py              # ADE: Core decision-making engine
│       ├── cognitive_load_distribution.py           # CLD: Offloads tasks to local/cloud GPU
│       ├── cognitive_logic_unit.py                  # CLU: Main message routing & logic engine
│       ├── cognitive_reasoning_engine.py            # CRE: Reasoning, inference, knowledge querying
│       ├── fastapi_app.py                           # FastAPI app wiring
│       ├── neural_optimization_feedback_loop.py     # NOFL: Feedback loop & learning adjustment
│       ├── self_sustaining_ai_memory.py             # SSAM: Stores & retrieves contextual memory
│       ├── streamlit_chat_ui.py                     # Development UI (Streamlit, temp until React UI)
│       ├── yuna_personality_behavioral_system.py    # YPBS: Tone, emotion, persona shaping
│       └── templates/                               # Streamlit templates
│
├── data/
│   ├── database/                 # SQLite files
│   ├── yuna_log.txt             # Logs
│   ├── yuna_memory.json         # Optional memory snapshot
│   ├── yuna_tasks.json          # Task queue (planned)
│
├── scripts/
│   ├── setup_yuna.py            # Local launcher & automation
│   ├── init_db.py
│   ├── migrate_db.py
│   ├── generate_ssl.sh
│
├── tests/
│   ├── test_memory.py
│   ├── test_chat.py
│   └── test_api.py
│
├── config/
│   ├── config.ini
│   └── requirements.txt
│
├── frontend/                    # Placeholder for future React.js migration
├── README.md
└── LICENSE
```

---

## 🚀 Getting Started

### 1️⃣ Set up environment

```bash
cd ~/Yuna-AI
python3 -m venv venv
source venv/bin/activate
pip install -r config/requirements.txt
```

### 2️⃣ Launch backend + Streamlit UI

```bash
export PYTHONPATH=$(pwd)/src
uvicorn src.api.cognitive_logic_unit:app --port 5002 --reload &
uvicorn src.api.cognitive_reasoning_engine:app --port 5003 --reload &
uvicorn src.api.self_sustaining_ai_memory:app --port 5004 --reload &
streamlit run src/api/streamlit_chat_ui.py
```

🔗 Visit: [http://localhost:8501](http://localhost:8501)

---

## 🔍 Core Capabilities

- 🧠 Memory Recall Engine (SSAM + SQLite + ChromaDB)
- 🤖 Reasoning & Inference (CRE + LLM)
- 🔁 Adaptive Learning Loop (NOFL + feedback tracking)
- 👤 Personalized Behavior (YPBS + emotion tone)
- ⚙️ Decision Engine (ADE + logic graphing)
- ☁️ Cloud/Local Task Offloading (CLD + cloud GPU API)

---

## 🧪 How to Use

1. Open the UI and chat with Yuna.
2. Messages are routed through CLU → CRE → SSAM.
3. Results are returned, and memory is updated.
4. Feedback is routed to NOFL to improve responses over time.

---

## 🧠 Quickstart Script

You can also launch everything from one file:

```bash
python3 scripts/setup_yuna.py
```

---

## 👨‍💻 Contributing

We welcome contributions:

- Fork & PR for new modules
- Suggestions for model optimization
- Prototypes for better UI (React preferred)

---

## 📄 License

**MIT License** – Open-source and built for research, collaboration, and future innovation.

---

> 👁️ Yuna AI is a functional prototype developed for both an active **PhD dissertation** and a **patent submission**.  
> Its architecture demonstrates modular, ethical, and adaptive AI design in real-world personal cognitive assistants.


