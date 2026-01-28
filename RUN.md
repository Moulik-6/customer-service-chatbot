# How to Run the Customer Service Chatbot

## ✅ Prerequisites Checklist

- [ ] Python 3.7+ installed
- [ ] Git installed (if cloning from repository)
- [ ] Trained model files in `models/intent_classifier_final/`

## 🚀 Quick Start (5 Steps)

### Step 1: Install Dependencies

Open PowerShell/Terminal in the project directory and run:

**Windows (Recommended):**
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt --only-binary :all:
```

**macOS/Linux:**
```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- NLTK (natural language processing)
- PyTorch & Transformers (AI model - optional for advanced features)
- All other dependencies

---

### Step 2: Download NLTK Data

First-time setup only:

```powershell
python scripts/setup_nltk.py
```

This downloads required language data for text processing.

---

### Step 3: Verify Model Files (Optional)

Check that your trained model is present:

```powershell
ls models/intent_classifier_final/
```

You should see these files:
- `config.json`
- `model.safetensors`
- `tokenizer.json`
- `tokenizer_config.json`
- `label_mappings.json`
- `vocab.txt`
- `special_tokens_map.json`

**If files are missing:** See [AI_TRAINING_GUIDE.md](AI_TRAINING_GUIDE.md) for training instructions.

---

### Step 4: Start the Chatbot

```powershell
python app.py
```

You should see:
```
Starting Customer Service Chatbot...
Visit http://localhost:5000 to use the chatbot
 * Running on http://127.0.0.1:5000
```

---

### Step 5: Open in Browser

1. Open your web browser
2. Go to: **http://localhost:5000**
3. Start chatting!

---

## 🧪 Test It Out

Try these queries to test the chatbot:

1. **Greeting**: "Hello" or "Hi there"
2. **Product Info**: "What products do you sell?"
3. **Pricing**: "How much does it cost?"
4. **Order Status**: "Where is my order?"
5. **Support**: "I need help"
6. **Returns**: "How do I return an item?"
7. **Payment**: "What payment methods do you accept?"

---

## ⚙️ Configuration (Optional)

### Change Port

If port 5000 is already in use:

**Windows PowerShell:**
```powershell
$env:FLASK_PORT="8080"
python app.py
```

**Linux/macOS:**
```bash
export FLASK_PORT=8080
python app.py
```

Then visit: http://localhost:8080

### Production Mode

For production deployment:

**Windows PowerShell:**
```powershell
$env:FLASK_DEBUG="False"
$env:FLASK_HOST="0.0.0.0"
python app.py
```

**Linux/macOS:**
```bash
export FLASK_DEBUG=False
export FLASK_HOST=0.0.0.0
python app.py
```

---

## 🔧 Troubleshooting

### Issue: "Module not found"
**Solution:**
```powershell
pip install -r requirements.txt --only-binary :all:
```

### Issue: "NLTK data not found"
**Solution:**
```powershell
python scripts/setup_nltk.py
```

### Issue: "Microsoft Visual C++ 14.0 required" (Windows only)
**Solution:** Use the `--only-binary` flag:
```powershell
pip install -r requirements.txt --only-binary :all:
```

### Issue: "Port 5000 already in use"
**Solution:** Change the port:
```powershell
$env:FLASK_PORT="8080"
python app.py
```

### Issue: "Model not found" warning
**Solution:** This is OK! The app will use NLTK-based intent detection instead. The AI model is optional.
- To use the AI model, ensure files are in `models/intent_classifier_final/`
- Train the model using instructions in [AI_TRAINING_GUIDE.md](AI_TRAINING_GUIDE.md)

---

## 📊 Viewing Conversation Logs

All conversations are automatically logged to `conversation_logs.json` in the project directory.

To view logs:
```powershell
cat conversation_logs.json
# or
notepad conversation_logs.json
```

---

## 🛑 Stopping the Server

Press **Ctrl+C** in the terminal where the app is running.

---

## 📚 Next Steps

- **Customize responses**: Edit `data/knowledge_base.json`
- **Train AI model**: Follow [AI_TRAINING_GUIDE.md](AI_TRAINING_GUIDE.md)
- **Modify UI**: Edit files in `templates/` and `static/`
- **Add new features**: See [README.md](README.md) for architecture details

---

## 🆘 Need Help?

- Check [QUICKSTART.md](QUICKSTART.md) for more examples
- Read [README.md](README.md) for full documentation
- Review [AI_TRAINING_GUIDE.md](AI_TRAINING_GUIDE.md) for model training

---

**Ready to go? Just run:** `python app.py` 🚀
