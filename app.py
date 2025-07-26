import requests
import json, numpy as np, os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
# Using a try-except block to handle the import error
try:
    from sentence_transformers import SentenceTransformer
    sentence_transformer_available = True
except ImportError:
    sentence_transformer_available = False
    print("Warning: SentenceTransformer could not be imported. Using fallback mode.")
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

# Configure Hugging Face token if available
if HUGGINGFACE_TOKEN:
    import huggingface_hub
    huggingface_hub.login(token=HUGGINGFACE_TOKEN)

# --- Load Database and Model ---
print("Loading database...")
with open('embeddings.json', 'r', encoding='utf-8') as f:
    knowledge_base = json.load(f)
vectors = np.array([item['vector'] for item in knowledge_base])

# Load the model only if SentenceTransformer is available
if sentence_transformer_available:
    try:
        print("Loading SentenceTransformer model...")
        # Try to use a local model if available
        model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder='./model_cache')
        print("✅ Database and model loaded.")
    except Exception as e:
        print(f"Error loading SentenceTransformer model: {e}")
        print("Switching to fallback mode (using pre-computed embeddings only)")
        model = None
else:
    model = None
    print("✅ Database loaded. Model loading skipped (using pre-computed embeddings only).")

# --- RAG function ---
def get_rag_response(query):
    global model  # Reference the global sentence transformer model
    
    if sentence_transformer_available and model is not None:
        # Embed the query using SentenceTransformer
        query_vector = model.encode([query])[0]
        
        # Find similar context
        similarities = cosine_similarity([query_vector], vectors)[0]
        top_k_indices = np.argsort(similarities)[-3:][::-1]  # Get top 3 most similar items
    else:
        # Fallback: If SentenceTransformer is not available, use all content
        # This is a simplified approach for demo purposes
        print("Using fallback mode: sending all knowledge base entries to Gemini")
        top_k_indices = range(min(3, len(knowledge_base)))  # Just use the first 3 items or fewer
    
    # Extract relevant contexts
    contexts = [knowledge_base[i]['content'] for i in top_k_indices]
    combined_context = "\n".join(contexts)
    
    # Extract the actual question from potential prompt engineering
    actual_query = query
    if "IMPORTANT:" in query and "Mirza Yoosha Minhaj" in query:
        # This is coming from the web interface with the CONVERSATION_ENHANCER
        # Just use the original query without extracting anything
        pass
    
    # Generate response with Gemini (using a different variable name)
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
