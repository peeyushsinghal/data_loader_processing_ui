import re
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

# List of required NLTK resources
REQUIRED_NLTK_DATA = [
    'punkt',
    'wordnet',
    'averaged_perceptron_tagger',
    'punkt_tab'
]

def download_nltk_data():
    """Download required NLTK data with proper error handling."""
    for resource in REQUIRED_NLTK_DATA:
        try:
            nltk.download(resource, quiet=True)
        except Exception as e:
            print(f"Warning: Failed to download NLTK resource '{resource}'. Error: {str(e)}")
            print(f"Some features may not work properly.")

# Download NLTK data when module is imported
download_nltk_data()

class TextPreprocessor:
    @staticmethod
    def remove_punctuation(text):
        """Remove punctuation from text."""
        return re.sub(r'[^\w\s]', '', text)
    
    @staticmethod
    def tokenize(text):
        """Tokenize text into words."""
        try:
            return word_tokenize(text)
        except LookupError:
            # Fallback tokenization if NLTK data is missing
            print("Warning: Using basic tokenization due to missing NLTK data")
            return text.split()
    
    @staticmethod
    def pad_text(text, length, pad_token='<PAD>'):
        """Pad or truncate text to specified length."""
        words = text.split()
        if len(words) > length:
            return ' '.join(words[:length])
        return ' '.join(words + [pad_token] * (length - len(words)))

class TextAugmenter:
    @staticmethod
    def get_synonyms(word):
        """Get synonyms for a word using WordNet."""
        try:
            synonyms = []
            for syn in wordnet.synsets(word):
                for lemma in syn.lemmas():
                    if lemma.name() != word:
                        synonyms.append(lemma.name())
            return list(set(synonyms))
        except LookupError:
            print("Warning: WordNet data not available. Synonym replacement disabled.")
            return []
    
    @staticmethod
    def random_insertion(text, n=1):
        """Randomly insert n words from the text into the text."""
        words = text.split()
        if len(words) < 2:
            return text
            
        for _ in range(n):
            insert_word = random.choice(words)
            insert_pos = random.randint(0, len(words))
            words.insert(insert_pos, insert_word)
            
        return ' '.join(words)
    
    @staticmethod
    def synonym_replacement(text, n=1):
        """Replace n random words with their synonyms."""
        words = text.split()
        if len(words) < 2:
            return text
            
        for _ in range(n):
            replace_idx = random.randint(0, len(words)-1)
            word = words[replace_idx]
            synonyms = TextAugmenter.get_synonyms(word)
            if synonyms:
                words[replace_idx] = random.choice(synonyms)
                
        return ' '.join(words)