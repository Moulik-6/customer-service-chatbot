# AI Chatbot Training Guide

## 🎯 Overview
This guide walks you through converting your rule-based chatbot to an AI-powered chatbot using a fine-tuned transformer model.

## 📋 Prerequisites
- Python 3.7+
- Google Colab account (free) OR Kaggle account (free)
- Basic understanding of Python

## 🚀 Step-by-Step Training Process

### Step 1: Generate Training Data (Local)

Run this on your local machine to create training data from your knowledge base:

```bash
python scripts/generate_training_data.py
```

**Output:** This creates:
- `data/train_data.json` (80% of data)
- `data/val_data.json` (20% of data)

**What it does:** Converts your knowledge base patterns into labeled training examples with augmentation.

---

### Step 2: Choose Your Training Platform

**Option A: Google Colab (Recommended)**
- Free GPU (Tesla T4)
- 12-hour session limit
- Easy to use

**Option B: Kaggle Notebooks**
- Free GPU (P100 - better than Colab free tier)
- 30 hours/week GPU quota
- Better for longer training

---

### Step 3: Upload to Colab/Kaggle

#### For Google Colab:
1. Go to [colab.research.google.com](https://colab.research.google.com)
2. Click **File → Upload notebook**
3. Upload `notebooks/train_intent_classifier.ipynb`
4. Click the **folder icon** on the left sidebar
5. Upload `data/train_data.json` and `data/val_data.json`
6. Go to **Runtime → Change runtime type**
7. Select **GPU** as hardware accelerator
8. Click **Save**

#### For Kaggle:
1. Go to [kaggle.com/code](https://kaggle.com/code)
2. Click **New Notebook**
3. Click **File → Import Notebook**
4. Upload `notebooks/train_intent_classifier.ipynb`
5. Click **+ Add Data** on the right
6. Click **Upload** and upload both JSON files from `data/` folder
7. In Settings (right sidebar), enable **GPU** accelerator

---

### Step 4: Run the Training Notebook

Execute all cells in order (Ctrl+F9 in Colab, Shift+Enter for each cell):

1. **Install dependencies** (~2 mins)
2. **Import libraries** (~30 seconds)
3. **Load data** (instant)
4. **Prepare dataset** (~10 seconds)
5. **Tokenize** (~30 seconds)
6. **Load model** (~1 minute)
7. **Train** (~5-10 minutes for 3 epochs)
8. **Evaluate** (~30 seconds)
9. **Test predictions** (instant)
10. **Save model** (~30 seconds)

**Total time:** ~15-20 minutes

---

### Step 5: Download the Trained Model

#### From Google Colab:
Run the last cell to download `intent_classifier_final.zip`, or:
1. Click folder icon
2. Right-click `intent_classifier_final` folder
3. Click **Download**

#### From Kaggle:
1. Click **Save Version** (top right)
2. Select **Save & Run All**
3. After completion, click **Output** tab
4. Download `intent_classifier_final` folder

---

### Step 6: Extract Model to Your Project

1. Extract `intent_classifier_final.zip`
2. Place the `intent_classifier_final/` folder in your `models/` directory:

```
customer-service-chatbot/
├── app.py
├── data/
│   └── knowledge_base.json
├── models/
│   ├── model_inference.py
│   └── intent_classifier_final/          ← Place here
│       ├── config.json
│       ├── model.safetensors
│       ├── tokenizer_config.json
│       ├── vocab.txt
│       └── label_mappings.json
├── notebooks/
│   └── train_intent_classifier.ipynb
├── scripts/
│   ├── generate_training_data.py
│   └── setup_nltk.py
└── ...
```

---s/model_inference.py
```

**Expected output:**
```
Loading model from models/nce.py
```

**Expected output:**
```
Loading model from intent_classifier_final...
✅ Model loaded successfully on cpu
📊 Number of intents: 10

Testing predictions:

Text: 'Hello, how are you?'
  → Intent: greeting (confidence: 98.45%)

Text: 'Where is my order?'
  → Intent: order_status (confidence: 95.23%)
...
```

---

### Step 8: Integrate into Flask App (Optional)

Update [app.py](app.py) to use the AI model instead of rule-based matching.

Add this import at the top:
```python
from models.model_inference import get_intent_classifier
```

Update the `detect_intent` function:
```python
def detect_intent(user_message):
    """Detect intent using AI model"""
    # Add this import at module level: from models.model_inference import get_intent_classifier
    classifier = get_intent_classifier()
    
    if classifier.is_loaded():
        # Use AI model
        intent, confidence = classifier.predict(user_message)
        
        # Fallback to unknown if confidence is too low
        if confidence < 0.5:
            return "unknown"
        return intent
    else:
        # Fallback to rule-based (current implementation)
        tokens = preprocess_text(user_message)
        # ... existing code ...
```

---

## 📊 Expected Results

With the default settings and dataset:
- **Accuracy:** ~85-95%
- **Training time:** 5-10 minutes
- **Model size:** ~250 MB
- **Inference time:** <100ms per message

---

## 🔧 Troubleshooting

### "CUDA out of memory"
- Reduce `per_device_train_batch_size` from 16 to 8 or 4
- Use Colab Pro or Kaggle for better GPUs

### "Model not found" error`models/` directory
- Ensure `intent_classifier_final/` folder is in project root
- Check all files are extracted correctly

### Low accuracy (<80%)
- Generate more training examples
- Increase `num_train_epochs` from 3 to 5
- Add more patterns to `knowledge_base.json`

### Model is slow
- Use CPU for inference (automatic fallback)
- Consider model quantization for faster inference
- Deploy on cloud with GPU support

---

## 🎓 Next Steps

1. **Expand knowledge base:** Add more intents and patterns to `data/knowledge_base.json`
2. **Collect real data:** Use `conversation_logs.json` to improve training
3. **Fine-tune further:** Retrain with conversation logs for better accuracy
4. **Deploy to cloud:** Use Hugging Face Spaces, AWS, or Heroku
5. **Add context:** Implement session management for multi-turn conversations

---

## 💡 Tips for Better Results

- **More data = better model:** Add at least 10-20 patterns per intent
- **Diverse examples:** Include typos, slang, different phrasings
- **Balance classes:** Ensure each intent has similar number of examples
- **Regular retraining:** Update model monthly with real conversation logs
- **Monitor confidence:** Log low-confidence predictions for review

---

## 📚 Additional Resources

- [Hugging Face Transformers Documentation](https://huggingface.co/docs/transformers)
- [Google Colab Tutorials](https://colab.research.google.com)
- [Kaggle Learn](https://www.kaggle.com/learn)
- [DistilBERT Paper](https://arxiv.org/abs/1910.01108)

---

## ❓ Need Help?

If you encounter issues:
1. Check the troubleshooting section above
2. Review notebook cell outputs for error messages
3. Verify all files are in the correct locations
4. Check Python package versions in `requirements.txt`

Happy training! 🚀
