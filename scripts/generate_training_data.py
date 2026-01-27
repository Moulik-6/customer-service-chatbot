"""
Generate training data for intent classification from knowledge base
Creates a dataset suitable for fine-tuning transformer models
"""

import json
import random
from typing import List, Dict

def load_knowledge_base(file_path: str = "data/knowledge_base.json") -> Dict:
    """Load the knowledge base from JSON file"""
    with open(file_path, 'r') as f:
        return json.load(f)


def augment_patterns(pattern: str) -> List[str]:
    """Generate variations of patterns to increase training data"""
    variations = [pattern]
    
    # Add variations with different punctuation
    variations.append(pattern + "?")
    variations.append(pattern + ".")
    
    # Add variations with capitalization
    variations.append(pattern.capitalize())
    variations.append(pattern.upper())
    
    # Add variations with common prefixes
    prefixes = ["can you", "could you", "i need", "i want", "tell me about", "what about"]
    for prefix in prefixes:
        variations.append(f"{prefix} {pattern}")
    
    return variations


def generate_training_data(knowledge_base: Dict) -> List[Dict]:
    """Generate training examples from knowledge base"""
    training_data = []
    
    for intent, data in knowledge_base.items():
        patterns = data.get("patterns", [])
        
        # Add original patterns
        for pattern in patterns:
            training_data.append({
                "text": pattern,
                "label": intent
            })
            
            # Add augmented versions
            augmented = augment_patterns(pattern)
            for aug_pattern in augmented:
                training_data.append({
                    "text": aug_pattern,
                    "label": intent
                })
    
    # Shuffle the data
    random.shuffle(training_data)
    
    return training_data


def split_data(data: List[Dict], train_ratio: float = 0.8):
    """Split data into train and validation sets"""
    random.shuffle(data)
    split_idx = int(len(data) * train_ratio)
    
    train_data = data[:split_idx]
    val_data = data[split_idx:]
    
    return train_data, val_data


def save_dataset(train_data: List[Dict], val_data: List[Dict], 
                 train_file: str = "data/train_data.json", 
                 val_file: str = "data/val_data.json"):
    """Save training and validation data to JSON files"""
    with open(train_file, 'w') as f:
        json.dump(train_data, f, indent=2)
    
    with open(val_file, 'w') as f:
        json.dump(val_data, f, indent=2)
    
    print(f"✅ Saved {len(train_data)} training examples to {train_file}")
    print(f"✅ Saved {len(val_data)} validation examples to {val_file}")


def main():
    """Main function to generate and save training data"""
    print("📚 Loading knowledge base...")
    kb = load_knowledge_base()
    
    print(f"📝 Found {len(kb)} intents")
    for intent in kb.keys():
        print(f"  - {intent}")
    
    print("\n🔄 Generating training data with augmentation...")
    training_data = generate_training_data(kb)
    
    print(f"✨ Generated {len(training_data)} training examples")
    
    print("\n✂️ Splitting into train/validation sets...")
    train_data, val_data = split_data(training_data, train_ratio=0.8)
    
    print("\n💾 Saving datasets...")
    save_dataset(train_data, val_data)
    
    print("\n📊 Dataset Statistics:")
    print(f"  Total examples: {len(training_data)}")
    print(f"  Training set: {len(train_data)}")
    print(f"  Validation set: {len(val_data)}")
    
    # Show sample examples
    print("\n🔍 Sample training examples:")
    for i, example in enumerate(random.sample(train_data, min(5, len(train_data)))):
        print(f"  {i+1}. Text: '{example['text']}' → Label: {example['label']}")


if __name__ == "__main__":
    main()
