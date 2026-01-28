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
- **AI/ML**: Transformers (DistilBERT), PyTorch, scikit-learn
- **Frontend**: HTML5, CSS3, JavaScript
- **Data Storage**: JSON (for conversation logs and knowledge base)
- **Training Platform**: Kaggle/Google Colab (for model training)

## Project Structure

```
customer-service-chatbot/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── data/
│   └── knowledge_base.json    # FAQ patterns and responses
├── models/
│   ├── model_inference.py     # AI model loader and predictor
│   └── intent_classifier_final/  # Trained model (after training)
├── notebooks/
│   └── train_intent_classifier.ipynb  # Colab/Kaggle training notebook
├── scripts/
│   ├── generate_training_data.py      # Data preparation script
│   └── setup_nltk.py                  # NLTK data setup
├── templates/
│   └── index.html             # Chat interface HTML
├── static/
│   ├── style.css              # Stylesheet
│   └── script.js              # Frontend JavaScript
├── conversation_logs.json     # Logged conversations (auto-generated)
├── AI_TRAINING_GUIDE.md       # Guide for training AI model
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
   
   **For Windows** (use pre-built wheels to avoid build errors):
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt --only-binary :all:
   ```
   
   **For macOS/Linux**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK data** (required for first-time setup):
   ```bash
   python scripts/setup_nltk.py
   ```

5. **Verify the trained model** (optional - model is already included):
   - The trained DistilBERT model should be in `models/intent_classifier_final/`
   - It includes: `model.safetensors`, `config.json`, `tokenizer.json`, `label_mappings.json`
   - If missing, train it using the Kaggle notebook (see AI_TRAINING_GUIDE.md)

6. **Run the application**:
   ```bash
   python app.py
   ```

7. **Access the chatbot**:
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
3. **Intent Detection**: 
   - **NLTK-based**: Simple keyword matching for basic intent detection
   - **AI-powered** (optional): Fine-tuned DistilBERT transformer model for advanced classification
4. **Response Generation**: Appropriate response is selected from the knowledge base
5. **Logging**: Conversation is logged with timestamp and detected intent
6. **Display**: Response is shown in the chat interface

**Note**: The chatbot currently uses NLTK-based intent detection. To use the AI model, see `models/model_inference.py` for integration.

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

### Configuration

The application can be configured using environment variables:

- `FLASK_DEBUG`: Set to 'False' for production (default: 'True')
- `FLASK_HOST`: Host to bind to (default: '127.0.0.1')
- `FLASK_PORT`: Port to run on (default: '5000')

Example:
```bash
export FLASK_DEBUG=False
export FLASK_HOST=0.0.0.0
export FLASK_PORT=8080
python app.py
```

## Future Enhancements

- [x] Machine Learning-based intent classification (DistilBERT trained model available)
- [ ] Integrate transformer model into main app.py
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