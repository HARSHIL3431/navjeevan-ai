# 🌾 Navjeevan AI

AI-powered decision support system for Indian farmers using FastAPI + intelligent query processing + real-time insights.

---

## Overview

Navjeevan AI helps farmers:

* 📊 Get smart crop market insights
* 🏛 Discover relevant government schemes
* 📄 Understand required documents
* 🤝 Find traders and buyers
* 🧠 Ask natural language queries and get AI-driven responses

---

## Current Tech Stack

* Backend: FastAPI, Pydantic
* AI: Groq API (LLM-based query parsing)
* Data: JSON datasets (multi-city agriculture data)
* Frontend: HTML, CSS, JavaScript
* Config: python-dotenv

---

## Project Structure

```text
navjeevan-ai/
├── backend/
│   ├── routes/           # API endpoints (chat, etc.)
│   ├── services/         # AI, intent, data processing
│   ├── models/           # request/response schemas
│   ├── config/           # settings and environment config
│   ├── utils/            # helper functions
│   └── main.py           # FastAPI entrypoint
├── frontend/
│   ├── assets/
│   └── pages/
├── prompts/              # AI prompt templates
├── requirements.txt
└── README.md
```

---

## Features

* 🧠 AI-powered intent detection
* 🌍 Multi-city agricultural data support
* 💬 Natural language query handling
* ⚡ FastAPI backend with modular architecture
* 🛡 Error handling and validation
* 🔌 External API integration (Groq)

---

## Setup (Windows)

1. Clone and enter project:

```bash
git clone https://github.com/YOUR_USERNAME/navjeevan-ai.git
cd navjeevan-ai
```

2. Create and activate virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create environment file:

```bash
copy .env.example .env
```

5. Add your API key in `.env`:

```env
GROQ_API_KEY=your_api_key_here
```

6. Run the app:

```bash
uvicorn backend.main:app --reload
```

7. Open:

* API docs: http://127.0.0.1:8000/docs
* Chat endpoint: http://127.0.0.1:8000/chat

---

## Environment Variables

Configured via `.env`:

```env
GROQ_API_KEY=your_api_key_here
```

---

## API Summary

### Chat

* POST /chat

#### Request:

```json
{
  "query": "What is tomato price in Surat?"
}
```

#### Response:

```json
{
  "status": "success",
  "intent": "market_price",
  "response": "Tomato price in Surat is..."
}
```

---

## Frontend Behavior

* Sends user queries to `/chat`
* Displays AI-generated responses
* Handles loading and error states
* Clean UI for farmer-friendly interaction

---

## Notes

* Ensure `.env` file is not committed (already in `.gitignore`)
* AI responses depend on Groq API availability
* Dataset is kept locally for performance and repo cleanliness

---

## Future Improvements

* 📦 Database integration (PostgreSQL / MongoDB)
* 🧠 Context-aware AI (memory-based responses)
* 🌐 Multilingual support (Hindi, Gujarati)
* 📱 Mobile-friendly UI
* 📊 Real-time mandi price APIs

---

## 👨‍💻 Author

Harshil Thakkar & Jiya Sadaria 

---

## 💡 Vision

Empowering Indian farmers with AI-driven insights for smarter agricultural decisions. 
