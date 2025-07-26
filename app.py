import requests
import json, numpy as np, os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai
from dotenv import load_dotenv

# --- Load Environment Variables ---
load_dotenv()  # Load environment variables from .env file

# --- Initialization & Configuration ---
app = Flask(__name__)
CORS(app)

# Get environment variables
# Get environment variables
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
PORT = int(os.environ.get('PORT', 5000))
HUGGINGFACE_TOKEN = os.environ.get('HUGGINGFACE_TOKEN')
AZURE_API_KEY = os.environ.get('AZURE_API_KEY')
AZURE_REGION = os.environ.get('AZURE_REGION', 'eastus')

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# To list all available models, uncomment these lines:
# for model in genai.list_models():
#     print(model.name)



# --- Load Database ---
print("Loading database...")
with open('embeddings.json', 'r', encoding='utf-8') as f:
    knowledge_base = json.load(f)

# --- Hugging Face Inference API for Embeddings ---
HF_EMBEDDING_API = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"
def get_embedding(text):
    headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}
    response = requests.post(HF_EMBEDDING_API, headers=headers, json={"inputs": text})
    if response.status_code == 200:
        return np.array(response.json()[0])
    else:
        raise Exception(f"Hugging Face API error: {response.status_code} {response.text}")

# --- RAG function ---
def get_rag_response(query):
    # Embed the query using Hugging Face Inference API
    try:
        query_vector = get_embedding(query)
    except Exception as e:
        print(f"Embedding error: {e}")
        # Fallback: Use all content if embedding fails
        top_k_indices = range(min(3, len(knowledge_base)))
    else:
        # Compute similarities with all knowledge base vectors
        vectors = np.array([item['vector'] for item in knowledge_base])
        similarities = cosine_similarity([query_vector.reshape(1, -1), vectors])[0]
        top_k_indices = np.argsort(similarities)[-3:][::-1]

    # Extract relevant contexts
    contexts = [knowledge_base[i]['content'] for i in top_k_indices]
    combined_context = "\n".join(contexts)

    # Extract the actual question from potential prompt engineering
    actual_query = query
    if "IMPORTANT:" in query and "Mirza Yoosha Minhaj" in query:
        pass

    # Generate response with Gemini
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""Based only on the following information, answer the user's question.
    If the answer cannot be derived from the provided information, respond with "I don't have enough information to answer that question."

    Information:
    {combined_context}

    User question: {actual_query}
    """
    response = gemini_model.generate_content(prompt)
    return response.text

# --- API Endpoints ---
# --- API Endpoints ---
@app.route("/")
def index():
    return render_template('index.html')  # Serve your HTML file from templates folder


@app.route("/ask", methods=["POST"])
def ask_question():
    data = request.get_json()
    query = data.get("query")
    answer = get_rag_response(query)
    return jsonify({"answer": answer})


# --- SECURE AZURE TTS PROXY ENDPOINT ---
from flask import Response
@app.route("/speak", methods=["POST"])
def speak():
    data = request.get_json()
    ssml = data.get("ssml")
    voice = data.get("voice", "en-US-AndrewMultilingualNeural")
    if not ssml or not AZURE_API_KEY or not AZURE_REGION:
        return jsonify({"error": "Missing SSML, API key, or region."}), 400
    endpoint = f"https://{AZURE_REGION}.tts.speech.microsoft.com/cognitiveservices/v1"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_API_KEY,
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "audio-24khz-160kbitrate-mono-mp3"
    }
    try:
        tts_response = requests.post(endpoint, headers=headers, data=ssml.encode("utf-8"))
        if tts_response.status_code != 200:
            return jsonify({"error": f"Azure TTS error: {tts_response.status_code} {tts_response.text}"}), 400
        return Response(tts_response.content, mimetype="audio/mpeg")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Use the PORT from environment variable, or specify your own port here
    # For example, to use port 8080 instead of 5000, change PORT to 8080
    app.run(host='0.0.0.0', port=PORT)
