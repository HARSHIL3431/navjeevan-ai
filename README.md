# 🌾 Navjeevan AI — Smart Farming & Agriculture Management Platform

![React 19](https://img.shields.io/badge/React-19-blue?logo=react)
![Vite](https://img.shields.io/badge/Vite-5.4-646CFF?logo=vite)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-v4-38BDF8?logo=tailwindcss)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python)
![Open-Meteo](https://img.shields.io/badge/Weather-Open--Meteo-orange)
![Groq AI](https://img.shields.io/badge/AI-Groq_LLM-purple)

**Navjeevan AI** (नवजीवन) is an AI-powered Agriculture Management and Decision Support Platform tailored for Indian farmers, featuring specialized agricultural data for Gujarat districts (*Surat, Navsari, Bardoli, Anand, Rajkot, Ahmedabad, Vadodara, etc.*).

The platform combines a **Clean Architecture FastAPI Backend** with a modern, high-contrast **React 19 / Vite Frontend** inspired by premium ThemeForest agricultural templates.

---

## ✨ Key Features

- 🌤️ **Real-Time Weather Detection & Spray Risk Advisor**: Interactive district lookup fetching live temperature, humidity, 3-day rainfall forecast (mm), and AI-recommended pesticide spraying windows.
- 🌾 **Smart APMC Mandi Price Optimizer**: Real-time mandi prices, nearest mandis, and market price comparisons for wheat, cotton, groundnut, and sugarcane.
- 📋 **Govt Scheme Explainer**: Instant eligibility checking and step-by-step application guidance for **PM Kisan Samman Nidhi** and **PM Fasal Bima Yojana**.
- 📄 **Document Verification Checklist**: Automatic document checklist generator for Kisan Credit Cards (KCC), 7/12 land records, and agricultural loans.
- 📞 **Direct Trader Directory**: Verified contact lookup for local crop buyers and traders in Gujarat.
- 💬 **Interactive AI Assistant**: Natural language chat drawer powered by Groq LLM with intent recognition and instant query chips.
- 🎨 **High-Contrast ThemeForest Design**: Built with Forest Green (`#2F6B2F`), Wheat Gold (`#F7C948`), glassmorphism overlays, and Framer Motion micro-animations.

---

## 🛠️ Full-Stack Technology Stack

| Layer | Technology | Usage |
| :--- | :--- | :--- |
| **Frontend Framework** | **React 19 + Vite 5** | Modular UI component architecture with instant HMR and optimized production bundling |
| **Frontend Styling** | **Tailwind CSS v4** | Custom agricultural design tokens, typography (`Inter` & `Poppins`), and glassmorphism |
| **Animations & Icons** | **Framer Motion + Lucide React** | Micro-interactions, hover scale keyframes, drawer slide-ins, and modern SVG icons |
| **Backend Framework** | **FastAPI** | Asynchronous RESTful API framework built on Starlette and Pydantic validation |
| **AI Intelligence** | **Groq LLM Engine** | High-speed LLM model formatting structured recommendations into natural language |
| **Weather Engine** | **Open-Meteo REST API** | Weather provider with 3-day rain forecasting and in-memory TTL caching |
| **Rule Engine** | **JSON Agronomic Rules** | Deterministic agricultural rules for NPK fertilizer, pest risk, and irrigation |
| **Testing** | **Pytest** | 22+ unit and integration tests covering backend decision services |

---

## 📂 Project Architecture

```text
navjeevan-ai/
├── backend/
│   ├── config/             # Settings & environment variables (.env)
│   ├── decision_engine/    # AdvisoryEngine, RuleProvider & WeatherProvider
│   ├── models/             # Pydantic Request & Response DTOs
│   ├── routes/             # API routes (/chat, /api/v1/weather, /advisory)
│   ├── services/           # Chat service, dataset cache & business logic
│   ├── utils/              # Helper utilities & realtime API wrappers
│   └── main.py             # FastAPI entry point & static asset mount
├── frontend/
│   ├── public/
│   │   └── navjeevan-ai.html # Standalone self-contained single-file HTML app
│   ├── src/
│   │   ├── components/     # 16 Modular React UI Components
│   │   │   ├── Navbar.jsx
│   │   │   ├── Hero.jsx
│   │   │   ├── Features.jsx
│   │   │   ├── WeatherWidget.jsx   # Live Weather & Spray Risk Detector
│   │   │   ├── AboutSection.jsx
│   │   │   ├── ServicesSection.jsx
│   │   │   ├── WhyChooseUs.jsx
│   │   │   ├── ProcessTimeline.jsx
│   │   │   ├── StatsCounter.jsx
│   │   │   ├── GalleryProjects.jsx
│   │   │   ├── Testimonials.jsx
│   │   │   ├── FAQSection.jsx
│   │   │   ├── BlogSection.jsx
│   │   │   ├── ContactSection.jsx
│   │   │   ├── CTASection.jsx
│   │   │   ├── Footer.jsx
│   │   │   └── AIChatModal.jsx     # AI Assistant Overlay Drawer
│   │   ├── App.jsx         # Main App Component
│   │   ├── main.jsx        # React entry point
│   │   └── index.css       # Tailwind CSS v4 & custom design system
│   ├── package.json
│   └── vite.config.js
├── tests/                  # Pytest unit & integration test suites
├── requirements.txt        # Python backend dependencies
└── README.md
```

---

## 🚀 Quick Setup & Installation

### Prerequisites
- **Python** 3.10 or higher
- **Node.js** v18 or higher & **npm**

---

### 1. Backend Setup

```bash
# Clone the repository
git clone https://github.com/HARSHIL3431/navjeevan-ai.git
cd navjeevan-ai

# Create & activate virtual environment (Windows)
python -m venv .venv
.venv\Scripts\activate

# Install backend dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env
```

Add your optional API keys to `.env`:
```env
GROQ_API_KEY=your_groq_api_key_here
```

---

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Build production bundle
npm run build

# Return to root directory
cd ..
```

---

## 🏃 Running the Application

### Option A: Run Unified Full-Stack App (Recommended)

Run the FastAPI server from the root directory:

```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

Open your browser at:
- 🌐 **Web Platform**: [http://localhost:8000](http://localhost:8000) or [http://127.0.0.1:8000](http://127.0.0.1:8000)
- 📖 **Interactive Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- ❤️ **API Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

---

### Option B: Run React Dev Server with HMR

In a separate terminal:

```bash
cd frontend
npm run dev -- --host 0.0.0.0 --port 5173
```

Open React Live Dev Server at:
- ⚡ **React App**: [http://localhost:5173](http://localhost:5173)

---

## 📡 API Endpoints Summary

### 1. Live Weather Detection API
- **`GET /api/v1/weather?location=Surat`**
- Returns temperature (°C), relative humidity (%), 3-day rainfall forecast (mm), and source provider data.

### 2. AI Chat & Intent Router API
- **`POST /chat`**
- **Request Body**: `{"query": "Best market to sell wheat in Surat today"}`
- **Response**: Returns classified intent (`market`, `scheme`, `document`, `contact`, `mandi`), structured data, and natural language AI advice.

### 3. Agricultural Advisory Decision Engine
- **`POST /advisory`**
- Runs pure agronomic rule logic for crop growth stages, NPK fertilizer recommendation, pest risk, and confidence scoring.

---

## 🧪 Running Tests

Run the Pytest suite from the root directory:

```bash
pytest tests/ -v
```

---

## 🌿 Vision & Future Roadmap

Empowering Indian farmers with accessible, real-time AI-driven intelligence for smarter crop decisions.

- 📦 PostgreSQL / MongoDB database persistence
- 🌐 Multilingual Voice Support (Gujarati & Hindi voice assistant)
- 📱 Native Android Mobile App (React Native)
- 🛰️ Satellite Crop Imagery & Disease Scanner Integration

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more details.
