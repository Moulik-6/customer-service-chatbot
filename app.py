"""
Automated Customer Service Chatbot - Main Application
A Flask-based chatbot using NLTK for natural language processing
"""

from flask import Flask, request, jsonify, render_template
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from datetime import datetime
import json
import os

app = Flask(__name__)

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

# Load knowledge base from JSON file
KNOWLEDGE_BASE_FILE = "data/knowledge_base.json"
KNOWLEDGE_BASE = {}

def load_knowledge_base():
    """Load the knowledge base from JSON file"""
    global KNOWLEDGE_BASE
    try:
        with open(KNOWLEDGE_BASE_FILE, 'r') as f:
            KNOWLEDGE_BASE = json.load(f)
        print(f"Knowledge base loaded successfully with {len(KNOWLEDGE_BASE)} intents")
    except FileNotFoundError:
        print(f"Error: {KNOWLEDGE_BASE_FILE} not found. Please create the knowledge base file.")
        KNOWLEDGE_BASE = {}
    except json.JSONDecodeError as e:
        print(f"Error parsing {KNOWLEDGE_BASE_FILE}: {e}")
        KNOWLEDGE_BASE = {}

# Load knowledge base on startup
load_knowledge_base()

# Conversation log file
LOG_FILE = "conversation_logs.json"


def preprocess_text(text):
    """Tokenize and clean the input text"""
    # Convert to lowercase
    text = text.lower()
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # Remove stopwords and punctuation
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token.isalnum() and token not in stop_words]
    
    return tokens


def detect_intent(user_message):
    """Detect the intent of the user's message"""
    tokens = preprocess_text(user_message)
    
    # Track intent scores
    intent_scores = {}
    
    for intent, data in KNOWLEDGE_BASE.items():
        score = 0
        for pattern in data["patterns"]:
            pattern_tokens = preprocess_text(pattern)
            # Count matching tokens
            for token in tokens:
                if token in pattern_tokens:
                    score += 1
        
        if score > 0:
            intent_scores[intent] = score
    
    # Return the intent with the highest score
    if intent_scores:
        best_intent = max(intent_scores, key=intent_scores.get)
        return best_intent
    
    return "unknown"


def get_response(intent):
    """Get a response based on the detected intent"""
    import random
    
    if intent in KNOWLEDGE_BASE:
        # Randomly select a response to make conversations more natural
        return random.choice(KNOWLEDGE_BASE[intent]["responses"])
    else:
        return "I'm sorry, I didn't understand that. Could you please rephrase your question?"


def log_conversation(user_message, bot_response, intent):
    """Log the conversation for future analysis"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_message": user_message,
        "intent": intent,
        "bot_response": bot_response
    }
    
    # Read existing logs
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r') as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            logs = []
    
    # Append new log
    logs.append(log_entry)
    
    # Write back to file
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=2)


@app.route('/')
def index():
    """Serve the chat interface"""
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Validate message length (max 500 characters)
        if len(user_message) > 500:
            return jsonify({'error': 'Message too long. Maximum 500 characters allowed.'}), 400
        
        # Detect intent
        intent = detect_intent(user_message)
        
        # Get response
        response = get_response(intent)
        
        # Log conversation
        log_conversation(user_message, response, intent)
        
        return jsonify({
            'response': response,
            'intent': intent
        })
    
    except Exception as e:
        # Log the error for debugging but don't expose details to client
        print(f"Error processing chat request: {str(e)}")
        return jsonify({'error': 'An error occurred processing your message. Please try again.'}), 500


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("Starting Customer Service Chatbot...")
    print("Visit http://localhost:5000 to use the chatbot")
    
    # Use environment variables for configuration
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', '5000'))
    
    app.run(debug=debug_mode, host=host, port=port)
