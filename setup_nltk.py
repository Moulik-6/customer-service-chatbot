"""
Setup script to download required NLTK data
Run this once before first use of the chatbot
"""
import nltk
import os

def download_nltk_data():
    """Download required NLTK datasets"""
    print("Downloading required NLTK data...")
    
    # Create nltk_data directory in user's home
    nltk_data_dir = os.path.expanduser('~/nltk_data')
    os.makedirs(nltk_data_dir, exist_ok=True)
    
    # Download required packages
    try:
        print("Downloading punkt tokenizer...")
        nltk.download('punkt', quiet=False)
        
        print("Downloading stopwords...")
        nltk.download('stopwords', quiet=False)
        
        print("\nNLTK data download completed successfully!")
        print("You can now run the chatbot with: python app.py")
        
    except Exception as e:
        print(f"Error downloading NLTK data: {e}")
        print("Please check your internet connection and try again.")
        return False
    
    return True

if __name__ == '__main__':
    download_nltk_data()
