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

# Knowledge base with FAQs and responses
KNOWLEDGE_BASE = {
    "greeting": {
        "patterns": ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"],
        "responses": [
            "Hello! How can I assist you today?",
            "Hi there! What can I help you with?",
            "Hey! I'm here to help. What do you need?"
        ]
    },
    "product_info": {
        "patterns": ["product", "item", "what do you sell", "what products", "catalog"],
        "responses": [
            "We offer a wide range of products including electronics, clothing, and home goods. What specific product are you interested in?",
            "Our product catalog includes various categories. Could you specify which type of product you're looking for?"
        ]
    },
    "pricing": {
        "patterns": ["price", "cost", "how much", "expensive", "cheap", "rate"],
        "responses": [
            "Our prices vary by product. Please visit our website or specify a product for exact pricing.",
            "Product pricing depends on the item. Can you tell me which product you're interested in?"
        ]
    },
    "order_status": {
        "patterns": ["order", "status", "tracking", "delivery", "shipment", "where is my order"],
        "responses": [
            "To check your order status, please provide your order ID and I'll help you track it.",
            "I can help you track your order. Please share your order number."
        ]
    },
    "support": {
        "patterns": ["help", "support", "problem", "issue", "not working", "broken"],
        "responses": [
            "I'm here to help! Please describe your issue and I'll do my best to assist you.",
            "Let me help you with that. Can you provide more details about the problem?"
        ]
    },
    "hours": {
        "patterns": ["hours", "open", "close", "timing", "schedule", "when"],
        "responses": [
            "Our customer service is available 24/7. How can I assist you?",
            "We're here to help you anytime! What do you need assistance with?"
        ]
    },
    "payment": {
        "patterns": ["payment", "pay", "credit card", "debit", "paypal", "payment method"],
        "responses": [
            "We accept various payment methods including credit cards, debit cards, and PayPal. What payment option are you interested in?",
            "You can pay using credit/debit cards or PayPal. Do you need help with a payment?"
        ]
    },
    "return": {
        "patterns": ["return", "refund", "exchange", "money back"],
        "responses": [
            "Our return policy allows returns within 30 days of purchase. Would you like to initiate a return?",
            "You can return products within 30 days. Please provide your order details to proceed."
        ]
    },
    "thanks": {
        "patterns": ["thank", "thanks", "appreciate", "grateful"],
        "responses": [
            "You're welcome! Is there anything else I can help you with?",
            "Happy to help! Let me know if you need anything else."
        ]
    },
    "goodbye": {
        "patterns": ["bye", "goodbye", "see you", "exit", "quit"],
        "responses": [
            "Goodbye! Have a great day!",
            "Thank you for chatting with us. See you soon!"
        ]
    }
}

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
