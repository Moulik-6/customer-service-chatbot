"""
Model Inference Script
Loads the fine-tuned intent classifier and provides prediction functions
"""

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import json
import os


class IntentClassifier:
    """Wrapper class for the fine-tuned intent classifier"""
    
    def __init__(self, model_path="models/intent_classifier_final"):
        """
        Initialize the intent classifier
        
        Args:
            model_path: Path to the saved model directory
        """
        self.model_path = model_path
        self.model = None
        self.tokenizer = None
        self.label_mappings = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Load model if available
        if os.path.exists(model_path):
            self.load_model()
        else:
            print(f"⚠️ Model not found at {model_path}")
            print("Please train the model first using train_intent_classifier.ipynb")
    
    def load_model(self):
        """Load the trained model, tokenizer, and label mappings"""
        try:
            print(f"Loading model from {self.model_path}...")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            
            # Load model
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_path)
            self.model.to(self.device)
            self.model.eval()
            
            # Load label mappings
            mappings_file = os.path.join(self.model_path, "label_mappings.json")
            if os.path.exists(mappings_file):
                with open(mappings_file, 'r') as f:
                    self.label_mappings = json.load(f)
            else:
                # Use model's built-in mappings
                self.label_mappings = {
                    'id2label': self.model.config.id2label,
                    'label2id': self.model.config.label2id
                }
            
            print(f"✅ Model loaded successfully on {self.device}")
            print(f"📊 Number of intents: {len(self.label_mappings['id2label'])}")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.model = None
            self.tokenizer = None
    
    def predict(self, text: str, return_confidence: bool = True):
        """
        Predict the intent of the given text
        
        Args:
            text: Input text to classify
            return_confidence: Whether to return confidence score
            
        Returns:
            If return_confidence is True: (intent, confidence)
            Otherwise: intent
        """
        if self.model is None or self.tokenizer is None:
            raise ValueError("Model not loaded. Please train the model first.")
        
        # Tokenize input
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=128
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Get predictions
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        # Apply softmax to get probabilities
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
        predicted_class_id = probabilities.argmax().item()
        confidence = probabilities[0][predicted_class_id].item()
        
        # Get intent label
        intent = self.label_mappings['id2label'][str(predicted_class_id)]
        
        if return_confidence:
            return intent, confidence
        else:
            return intent
    
    def predict_top_k(self, text: str, k: int = 3):
        """
        Predict top k intents with their confidence scores
        
        Args:
            text: Input text to classify
            k: Number of top predictions to return
            
        Returns:
            List of tuples: [(intent, confidence), ...]
        """
        if self.model is None or self.tokenizer is None:
            raise ValueError("Model not loaded. Please train the model first.")
        
        # Tokenize input
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=128
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Get predictions
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        # Apply softmax to get probabilities
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
        top_k_probs, top_k_indices = torch.topk(probabilities[0], k)
        
        # Convert to list of (intent, confidence) tuples
        results = []
        for prob, idx in zip(top_k_probs.tolist(), top_k_indices.tolist()):
            intent = self.label_mappings['id2label'][str(idx)]
            results.append((intent, prob))
        
        return results
    
    def is_loaded(self):
        """Check if model is successfully loaded"""
        return self.model is not None and self.tokenizer is not None


# Singleton instance
_classifier_instance = None


def get_intent_classifier(model_path="models/intent_classifier_final"):
    """
    Get or create the intent classifier instance (singleton pattern)
    
    Args:
        model_path: Path to the saved model directory
        
    Returns:
        IntentClassifier instance
    """
    global _classifier_instance
    
    if _classifier_instance is None:
        _classifier_instance = IntentClassifier(model_path)
    
    return _classifier_instance


# Test function
if __name__ == "__main__":
    print("🧪 Testing Intent Classifier\n")
    
    # Initialize classifier
    classifier = get_intent_classifier()
    
    if not classifier.is_loaded():
        print("❌ Model not loaded. Please train the model first.")
        print("\nSteps to train:")
        print("1. Run: python scripts/generate_training_data.py")
        print("2. Upload data/train_data.json and data/val_data.json to Colab/Kaggle")
        print("3. Run notebooks/train_intent_classifier.ipynb")
        print("4. Download the trained model and place it in models/intent_classifier_final/")
    else:
        # Test examples
        test_examples = [
            "Hello, how are you?",
            "Where is my order?",
            "How much does it cost?",
            "I want to return my product",
            "What do you sell?",
            "Thank you so much!",
            "Bye!"
        ]
        
        print("Testing predictions:\n")
        for text in test_examples:
            intent, confidence = classifier.predict(text)
            print(f"Text: '{text}'")
            print(f"  → Intent: {intent} (confidence: {confidence:.2%})\n")
        
        # Test top-k predictions
        print("\nTop 3 predictions for 'I need help with my order':")
        top_k = classifier.predict_top_k("I need help with my order", k=3)
        for i, (intent, conf) in enumerate(top_k, 1):
            print(f"  {i}. {intent}: {conf:.2%}")
