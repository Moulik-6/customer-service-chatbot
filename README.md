# Automated Customer Service Chatbot

## Overview

An intelligent customer service chatbot built with Python, Flask, and Natural Language Processing (NLP) using NLTK. This chatbot can handle common customer queries, provide instant responses, and improve customer support efficiency.

## Features

- 🤖 **Automated Response System**: Handles FAQs about products, pricing, orders, support, and more
- 🧠 **NLP-Powered Intent Detection**: Uses NLTK for natural language understanding
- 💬 **Interactive Web Interface**: Clean and user-friendly chat UI
- 📝 **Conversation Logging**: Tracks all interactions for future analysis
- ⚡ **Real-time Responses**: Instant replies to customer queries
- 🎯 **Multi-Intent Support**: Handles greetings, product info, pricing, order status, support, returns, and more

## Technology Stack

- **Backend**: Python 3.x, Flask
- **NLP**: NLTK (Natural Language Toolkit)
- **Frontend**: HTML5, CSS3, JavaScript
- **Data Storage**: JSON (for conversation logs)

## Project Structure

```
customer-service-chatbot/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── templates/
│   └── index.html             # Chat interface HTML
├── static/
│   ├── style.css              # Stylesheet
│   └── script.js              # Frontend JavaScript
├── conversation_logs.json     # Logged conversations (auto-generated)
└── README.md                  # This file
```

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Moulik-6/customer-service-chatbot.git
   cd customer-service-chatbot
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the chatbot**:
   Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

### Example Queries

The chatbot can respond to various types of queries:

- **Greetings**: "Hello", "Hi", "Good morning"
- **Product Information**: "What products do you sell?", "Tell me about your catalog"
- **Pricing**: "How much does it cost?", "What are your prices?"
- **Order Status**: "Where is my order?", "Track my delivery"
- **Support**: "I need help", "I have a problem"
- **Business Hours**: "When are you open?", "What are your hours?"
- **Payment**: "What payment methods do you accept?", "Can I pay with PayPal?"
- **Returns**: "How do I return an item?", "What is your refund policy?"

### How It Works

1. **User Input**: Customer types a question in the chat interface
2. **NLP Processing**: Message is tokenized and processed using NLTK
3. **Intent Detection**: The system identifies the user's intent by matching keywords
4. **Response Generation**: Appropriate response is selected from the knowledge base
5. **Logging**: Conversation is logged with timestamp and detected intent
6. **Display**: Response is shown in the chat interface

## Customization

### Adding New Intents

To add new intents and responses, edit the `KNOWLEDGE_BASE` dictionary in `app.py`:

```python
KNOWLEDGE_BASE = {
    "your_intent_name": {
        "patterns": ["keyword1", "keyword2", "phrase"],
        "responses": [
            "Response option 1",
            "Response option 2"
        ]
    }
}
```

### Modifying the UI

- **Colors/Styling**: Edit `static/style.css`
- **Layout**: Modify `templates/index.html`
- **Behavior**: Update `static/script.js`

## Future Enhancements

- [ ] Machine Learning-based intent classification
- [ ] Multi-language support
- [ ] Integration with databases for dynamic product information
- [ ] User authentication and session management
- [ ] Analytics dashboard for conversation insights
- [ ] Integration with messaging platforms (WhatsApp, Telegram, etc.)
- [ ] Voice input/output capabilities
- [ ] Sentiment analysis for customer satisfaction tracking

## API Endpoints

- `GET /`: Serves the chat interface
- `POST /chat`: Processes chat messages
  - Request body: `{"message": "user message"}`
  - Response: `{"response": "bot response", "intent": "detected_intent"}`
- `GET /health`: Health check endpoint

## Contributing

This is a minimal college project that can be extended with more features. Contributions are welcome!

## License

This project is created for educational purposes.

## Author

Created as a college project for automated customer service solutions.

## Acknowledgments

- NLTK library for natural language processing
- Flask framework for web development
- Inspired by modern customer service automation needs