# 3D Voice Bot with RAG and LLM

A cutting-edge, deployable 3D voice chatbot that fuses a **Custom Retrieval-Augmented Generation (RAG)** pipeline with Google's **Gemini LLM** to deliver intelligent, context-aware answers about your personal portfolio. Featuring a real-time interactive 3D avatar and a natural voice interface, this project showcases the future of AI-powered personal assistants.


### 🌐 Live Demo
Main Link :- [**https://chatbot-murex-eta-24.vercel.app/**](https://chatbot-murex-eta-24.vercel.app/)       <br><br>
Alternative Link:-[**https://threed-voice-bot-with-rag-and-llm.onrender.com/**](https://threed-voice-bot-with-rag-and-llm.onrender.com/)

---

## 🚀 Features

-   **Interactive 3D Avatar:** Engaging and animated 3D character powered by **Three.js** and `GLTFLoader`.
-   **Natural Voice Conversation:** Real-time, secure voice interaction using **Azure Speech Services**, proxied through the Flask backend to protect API keys.
-   **Custom RAG + LLM Intelligence:** Combines a from-scratch RAG pipeline using **Sentence-Transformers** for semantic search with the **Google Gemini LLM** for highly relevant, context-driven answers.
-   **Portfolio-Aware:** All answers are grounded in your own portfolio data, loaded from a custom `embeddings.json` file.
-   **Modern UI/UX:** Sleek, responsive, and visually appealing interface with smooth controls for both text chat and voice interaction.
-   **Deployable:** Ready for one-click deployment on Render, Heroku, or any other Python-friendly cloud platform.

## 🛠️ Tech Stack

| Category         | Technology                                                                                                  |
| ---------------- | ----------------------------------------------------------------------------------------------------------- |
| **Backend** | Python, Flask, Flask-CORS, python-dotenv                                                                    |
| **AI/ML** | **Custom RAG Pipeline**, Google GenerativeAI (`gemini-1.5-flash`), Sentence-Transformers, scikit-learn, NumPy |
| **Frontend** | HTML5, CSS3, JavaScript (ESM), Three.js, GLTFLoader, Azure Speech API (via backend proxy)                     |
| **Data** | Pre-computed embeddings (`embeddings.json`) for fast and efficient semantic retrieval.                      |
| **Deployment** | Render, Heroku, Docker (optional)                                                                           |

---

## 🧠 How It Works

This project implements a **custom RAG pipeline from scratch** without relying on external frameworks like LangChain or LlamaIndex. The process ensures that the AI's responses are based *only* on the information you provide in your knowledge base.

> *Consider creating a simple diagram to illustrate this flow.*

1. **User Input:** The user asks a question via the frontend (either through text or voice).
2. **Query Embedding:** The Flask backend receives the query and uses the **Hugging Face Inference API** (`sentence-transformers/all-MiniLM-L6-v2`) to convert the text into a vector embedding.
3. **Semantic Search (Retrieve):** The system calculates the **cosine similarity** between the user's query vector and all the pre-computed vectors in `embeddings.json`. It retrieves the top 3 most relevant text chunks from your portfolio.
4. **Prompt Augmentation (Augment):** The retrieved text chunks are injected into a carefully engineered prompt, providing crucial context for the LLM.
5. **Content Generation (Generate):** The augmented prompt is sent to the **Google Gemini (`gemini-1.5-flash`) API**. The LLM generates a natural, human-like answer based *only* on the provided context.
6. **Voice & Animation:** The final text is sent to **Azure Speech Services** to generate audio. The 3D avatar animates while speaking the response, creating an immersive user experience.

---

## ⚡ Quick Start

### Prerequisites
- Python 3.8+
- A [Google AI Studio API Key](https://aistudio.google.com/app/apikey) for Gemini.
- An [Azure Account](https://azure.microsoft.com/) for the Speech Services API key (optional, for voice).
- A [Hugging Face User Access Token](https://huggingface.co/settings/tokens) for the embedding model.

### Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/YooshaMirza/3D-Voice-Bot-with-RAG-and-LLM.git](https://github.com/YooshaMirza/3D-Voice-Bot-with-RAG-and-LLM.git)
    cd 3D-Voice-Bot-with-RAG-and-LLM
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Up Environment Variables:**
    Create a file named `.env` in the root directory and add your API keys.

    ```env
    # .env
    GEMINI_API_KEY="your_google_gemini_api_key_here"
    HUGGINGFACE_TOKEN="your_huggingface_token_here"

    # Optional for voice functionality
    AZURE_API_KEY="your_azure_speech_api_key_here"
    AZURE_REGION="your_azure_speech_region_here" # e.g., eastus

    # Port for the Flask server
    PORT=5000
    ```
    > **Warning:** Never commit your `.env` file to version control. It is included in `.gitignore` by default.

4.  **Add Your Portfolio Data:**
    Make sure your `embeddings.json` file is present in the root of the project. This file should contain the text chunks of your portfolio and their corresponding pre-computed vector embeddings.

5.  **Run the Application:**
    ```bash
    python app.py
    ```

6.  **Open in Browser:**
    Visit **[http://localhost:5000](http://localhost:5000)** to interact with your 3D AI assistant!

---

## 📁 Project Structure

```
.
├── app.py                  # Main Flask backend, RAG logic, and API endpoints
├── embeddings.json         # Your portfolio knowledge base with pre-computed embeddings
├── requirements.txt        # Python dependencies for the backend
├── .env                    # Your secret API keys and configuration
├── templates/
│   └── index.html          # The complete frontend UI, 3D logic, and chat interface
└── ...
```

## ☁️ Deployment

This application is built to be easily deployed on cloud platforms like **Render** or **Heroku**.

1. Push your code to a GitHub repository.
2. Create a new "Web Service" on your chosen platform and link it to your repository.
3. Set the **build command** to `pip install -r requirements.txt`.
4. Set the **start command** to `python app.py`.
5. Add your API keys from your `.env` file to the platform's "Environment Variables" section.
6. Deploy!

---

## ✨ Credits & Inspiration

-   **Google** for the powerful Gemini family of models.
-   **Microsoft Azure** for their high-quality Text-to-Speech services.
-   **Three.js** for making 3D in the browser accessible and fun.
-   The **Hugging Face** community for providing open-source models like Sentence-Transformers.

## 💡 License

This project is licensed under the **MIT License**. Feel free to use, modify, and share it. Attribution is appreciated!

---

### Unleash the power of RAG + LLM with a 3D voice experience — your portfolio, reimagined!
