# 📞 Gramaphone

> An AI-powered caller agent for government services — built at Hacktopia Hackathon

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-6.x-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![WebSockets](https://img.shields.io/badge/WebSockets-Real--Time-010101?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 📌 Overview

**Gramaphone** is an AI-driven caller agent designed to automate and streamline citizen interactions with government services. It replaces traditional IVR (Interactive Voice Response) systems with a conversational LLM-powered agent that can understand natural language, respond intelligently, and log interactions — all in real time over WebSockets.

Built during the **Hacktopia Hackathon**, Gramaphone addresses the challenge of making government services more accessible, reducing wait times, and enabling 24/7 automated support for common citizen queries.

---

## 🧩 Architecture

```
┌─────────────────────────────────────────┐
│               User / Caller             │
└──────────────────┬──────────────────────┘
                   │ WebSocket Connection
                   ▼
┌─────────────────────────────────────────┐
│         websocket_llm (Python)          │
│  - Real-time message handling           │
│  - LLM integration (AI responses)       │
│  - Session & conversation management    │
└──────────────────┬──────────────────────┘
                   │ REST / DB calls
                   ▼
┌─────────────────────────────────────────┐
│           webapp (Flask)                │
│  - REST API endpoints                   │
│  - MongoDB integration                  │
│  - Auth & session management            │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│              MongoDB                    │
│  - Conversation logs                    │
│  - User/session data                    │
│  - Government service data              │
└─────────────────────────────────────────┘
```

The project is split into two core modules:

| Module | Stack | Responsibility |
|---|---|---|
| `webapp/` | Flask, MongoDB, Python | REST API, data persistence, admin interface |
| `websocket_llm/` | Python, WebSockets, LLM | Real-time AI caller agent, conversation engine |

---

## ✨ Features

- 🤖 **AI-Powered Conversations** — LLM-driven agent handles natural language queries from citizens
- ⚡ **Real-Time Communication** — WebSocket-based bidirectional messaging for low-latency interactions
- 🗄️ **Persistent Logging** — All conversations stored in MongoDB for audit trails and analytics
- 🏛️ **Government-Focused** — Designed specifically for public service use cases (queries, appointments, status checks, etc.)
- 🌐 **Web Interface** — Frontend dashboard via the `webapp` module for monitoring and management
- 🔐 **Environment-Based Config** — Secrets and connection strings managed via `.env` for security

---

## 📁 Project Structure

```
gramaphone-hacktopia/
│
├── webapp/                  # Flask web application
│   ├── app.py               # Main Flask app & route definitions
│   ├── models/              # MongoDB data models
│   ├── routes/              # API route handlers
│   ├── templates/           # HTML templates (Jinja2)
│   └── static/              # Frontend assets (JS, CSS)
│
├── websocket_llm/           # WebSocket + LLM agent
│   ├── main.py              # WebSocket server entry point
│   ├── agent.py             # LLM agent logic & prompt engineering
│   └── handlers.py          # Message routing & session handling
│
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
└── README.md
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend API | Python, Flask |
| Real-Time Engine | Python WebSockets |
| AI / LLM | LLM integration (configurable) |
| Database | MongoDB (via PyMongo) |
| Frontend | JavaScript (ES6+) |
| Config Management | python-dotenv |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- MongoDB instance (local or Atlas)
- An LLM API key (configured via `.env`)

### 1. Clone the Repository

```bash
git clone https://github.com/dev-fm-thekk/gramaphone-hacktopia.git
cd gramaphone-hacktopia
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory:

```env
MONGO_URI=mongodb://localhost:27017/gramaphone
LLM_API_KEY=your_api_key_here
FLASK_SECRET_KEY=your_secret_key_here
FLASK_ENV=development
WEBSOCKET_PORT=8765
```

### 4. Start the Flask Web App

```bash
cd webapp
python app.py
```

The web app will be available at `http://localhost:5000`.

### 5. Start the WebSocket LLM Agent

In a separate terminal:

```bash
cd websocket_llm
python main.py
```

The WebSocket server will start on `ws://localhost:8765`.

---

## 💬 How It Works

1. A user (citizen) connects to the WebSocket server from the web interface or a compatible client.
2. The **websocket_llm** module receives the user's message and passes it to the LLM agent.
3. The agent constructs a context-aware prompt based on conversation history and the government service domain.
4. The LLM generates a response which is streamed back to the user in real time.
5. The conversation is logged to **MongoDB** via the Flask API for record-keeping and analytics.

---

## 🏛️ Use Cases

Gramaphone is designed to handle common government service interactions such as:

- Answering FAQs about government schemes and programs
- Checking application or request status
- Booking appointments with government offices
- Routing citizens to the correct department
- Providing information in a multilingual, accessible format

---

## 🔮 Roadmap

- [ ] Speech-to-text input (voice caller support)
- [ ] Text-to-speech output (full voice agent)
- [ ] Multi-language support (Malayalam, Hindi, English)
- [ ] Admin dashboard for conversation analytics
- [ ] Integration with government APIs for live data lookup
- [ ] Docker Compose setup for one-command deployment

---

## 👥 Contributors

- **Abhiram A R** — [@dev-fm-thekk](https://github.com/dev-fm-thekk)

Built at **Hacktopia Hackathon** 🏆

---

## 📄 License

This project is open source. Feel free to use, fork, and contribute.

---

> *"Making government services accessible to every citizen, one conversation at a time."*
