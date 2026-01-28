# Quick Start Guide

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Download NLTK data (first time only):**
   ```bash
   python setup_nltk.py
   ```

3. **Run the chatbot:**
   ```bash
   python app.py
   ```

4. **Open your browser:**
   Navigate to `http://localhost:5000`

## Testing the Chatbot

Try these example queries:

### Greetings
- "Hello"
- "Hi there"
- "Good morning"

### Product Information
- "What products do you sell?"
- "Tell me about your catalog"
- "What items are available?"

### Pricing
- "How much does it cost?"
- "What are your prices?"
- "Is it expensive?"

### Order Tracking
- "Where is my order?"
- "Track my delivery"
- "Order status"

### Support
- "I need help"
- "I have a problem"
- "Something is not working"

### Returns
- "How do I return an item?"
- "What is your refund policy?"
- "I want to exchange a product"

### Payment
- "What payment methods do you accept?"
- "Can I pay with PayPal?"
- "Do you accept credit cards?"

### Business Hours
- "When are you open?"
- "What are your hours?"
- "Are you available 24/7?"

## Configuration

Set environment variables before running:

```bash
# Development (default)
export FLASK_DEBUG=True
export FLASK_HOST=127.0.0.1
export FLASK_PORT=5000

# Production
export FLASK_DEBUG=False
export FLASK_HOST=0.0.0.0
export FLASK_PORT=8080
```

## API Usage

### Chat Endpoint
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

Response:
```json
{
  "intent": "greeting",
  "response": "Hello! How can I assist you today?"
}
```

### Health Check
```bash
curl http://localhost:5000/health
```

Response:
```json
{
  "status": "healthy"
}
```

## Troubleshooting

**Issue: NLTK data not found**
- Solution: Run `python setup_nltk.py`

**Issue: Port 5000 already in use**
- Solution: Change port with `export FLASK_PORT=8080`

**Issue: Module not found**
- Solution: Install dependencies with `pip install -r requirements.txt`

## Adding New Intents

Edit `app.py` and add to the `KNOWLEDGE_BASE` dictionary:

```python
"your_intent": {
    "patterns": ["keyword1", "keyword2", "phrase"],
    "responses": [
        "Response option 1",
        "Response option 2"
    ]
}
```

## Project Files

- `app.py` - Main Flask application with NLP logic
- `setup_nltk.py` - NLTK data downloader
- `templates/index.html` - Chat interface
- `static/style.css` - Styling and animations
- `static/script.js` - Frontend chat logic
- `conversation_logs.json` - Auto-generated conversation history

## Features

✅ Natural language understanding  
✅ Intent detection  
✅ Multiple response variations  
✅ Conversation logging  
✅ Modern UI with animations  
✅ Real-time messaging  
✅ Security features  
✅ Easy to extend  
