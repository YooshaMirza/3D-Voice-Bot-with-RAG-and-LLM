# RAG-LLM-3D-Voice-Bot

A cutting-edge, deployable 3D voice chatbot that fuses Retrieval-Augmented Generation (RAG) with a Large Language Model (LLM) (Google Gemini) to deliver intelligent, context-aware answers about your portfolio. Featuring a real-time interactive 3D avatar and natural voice interface, this project showcases the future of AI-powered personal assistants.

---

**🌐 Live Demo:** (https://threed-voice-bot-with-rag-and-llm.onrender.com/)

---

## 🚀 Features

- **3D Interactive Avatar:** Engaging, animated 3D character powered by Three.js and GLTFLoader
- **Voice Conversation:** Natural, real-time voice interaction using Azure Speech Services
- **RAG + LLM Intelligence:** Combines semantic search (RAG) with Gemini LLM for highly relevant, context-driven answers
- **Portfolio-Aware:** Answers are grounded in your own portfolio data and experiences
- **Modern UI/UX:** Responsive, visually appealing interface with smooth chat and voice controls
- **Easy Deployment:** Ready for Heroku, Render, or any Python-friendly cloud platform

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask, Flask-CORS, python-dotenv
- **AI/ML:** Sentence-Transformers, scikit-learn, numpy, Google GenerativeAI (Gemini), RAG pipeline
- **Frontend:** HTML, CSS, JavaScript (ES6+), Three.js, GLTFLoader, Azure Speech API
- **Data:** Precomputed embeddings (`embeddings.json`) for fast semantic retrieval

---

## ⚡ Quick Start

1. **Clone the repository**
2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
3. **Set up environment variables:**
   - Edit `.env` and add your Gemini API key and (optionally) Azure Speech key:
     ```
     GEMINI_API_KEY=your_gemini_api_key_here
     PORT=5000
     # Optional for voice: AZURE_API_KEY=your_azure_key_here
     ```
   - Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/)
   - Get an Azure Speech key from [Azure Portal](https://portal.azure.com/)
4. **Add your portfolio data:**
   - Place your `embeddings.json` file in the project root (see example format in repo)
5. **Run the application:**
   ```
   python app.py
   ```
6. **Open in browser:**
   - Visit [http://localhost:5000](http://localhost:5000) to chat with your 3D AI assistant!

---

## 🧠 How It Works

1. **User asks a question (text or voice)**
2. **RAG pipeline** finds the most relevant portfolio entries using semantic similarity
3. **Gemini LLM** generates a context-aware answer, grounded in your portfolio
4. **3D avatar** animates and responds with natural speech (via Azure TTS)

---

## API Endpoints

- `GET /` — Serves the 3D voice chatbot frontend
- `POST /ask` — Accepts `{ "query": "your question" }` and returns `{ "answer": "AI response" }`

---

## 🌐 Deploying

This app is cloud-ready! Deploy on Heroku, Render, or any Python-friendly platform. Just set your environment variables and upload your `embeddings.json`.

**Live Demo:** [https://zyx](https://zyx)

---

## 📁 Project Structure

- `app.py` — Main Flask backend, RAG logic, Gemini integration
- `embeddings.json` — Portfolio knowledge base with precomputed embeddings
- `templates/index.html` — 3D voice chatbot frontend (Three.js, Azure TTS, chat UI)
- `.env` — API keys and config (never commit secrets!)
- `requirements.txt` — Python dependencies

---

## ✨ Credits & Inspiration

- [Google Gemini](https://aistudio.google.com/)
- [Azure Speech Services](https://azure.microsoft.com/en-us/products/ai-services/speech-services/)
- [Three.js](https://threejs.org/)
- [Sentence-Transformers](https://www.sbert.net/)

---

## 💡 License

MIT — Free to use, modify, and share. Attribution appreciated!

---

**Unleash the power of RAG + LLM with a 3D voice experience — your portfolio, reimagined!**
