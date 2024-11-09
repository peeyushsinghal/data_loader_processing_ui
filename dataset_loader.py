import os
import re
import random
from dataset_utils import TextPreprocessor, TextAugmenter

class DatasetLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.text = self._load_file()
        self.segments = self._extract_segments()
        
    def _load_file(self):
        """Load text file."""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _extract_segments(self):
        """Extract segments from text based on format."""
        # First try to find dialogue format (Character: text)
        dialogue_segments = re.findall(r'[A-Za-z ]+:\n[^:]+', self.text)
        
        if dialogue_segments:
            # Process dialogue format
            cleaned_segments = []
            for segment in dialogue_segments:
                parts = segment.split(':\n', 1)
                if len(parts) == 2:
                    character, dialogue = parts
                    dialogue = ' '.join(dialogue.split())
                    if dialogue:
                        cleaned_segments.append(('CHARACTER', character.strip(), dialogue))
            return cleaned_segments
        
        # Try paragraphs
        paragraphs = [p.strip() for p in re.split(r'\n\s*\n', self.text) if p.strip()]
        
        # If more than one paragraph, treat as paragraphs
        if len(paragraphs) > 1:
            return [('PARAGRAPH', f'P{i+1}', ' '.join(p.split())) 
                   for i, p in enumerate(paragraphs)]
        
        # If single paragraph or no paragraphs, split by lines
        lines = self.text.split('\n')
        return [('LINE', f'L{i+1}', line.strip()) 
                for i, line in enumerate(lines) if line.strip()]
    
    def get_random_segment(self, n_words=100, preprocess_opts=None, augment_opts=None):
        """
        Get a random segment with optional preprocessing and augmentation.
        
        Args:
            n_words (int): Number of words to return
            preprocess_opts (dict): Preprocessing options
            augment_opts (dict): Augmentation options
            
        Returns:
            tuple: (segment_type, segment_id, text)
        """
        if not self.segments:
            return None, None, None
        
        # Select random segment
        segment_type, segment_id, text = random.choice(self.segments)
        
        # Apply preprocessing if specified
        if preprocess_opts:
            if preprocess_opts.get('remove_punctuation'):
                text = TextPreprocessor.remove_punctuation(text)
            if preprocess_opts.get('tokenize'):
                text = ' '.join(TextPreprocessor.tokenize(text))
            if preprocess_opts.get('pad_length'):
                text = TextPreprocessor.pad_text(text, preprocess_opts['pad_length'])
        
        # Apply augmentation if specified
        if augment_opts:
            if augment_opts.get('random_insertion'):
                text = TextAugmenter.random_insertion(text, augment_opts['random_insertion'])
            if augment_opts.get('synonym_replacement'):
                text = TextAugmenter.synonym_replacement(text, augment_opts['synonym_replacement'])
        
        # Split into words and get n_words
        words = text.split()
        if len(words) <= n_words:
            return segment_type, segment_id, ' '.join(words)
        
        start_idx = random.randint(0, len(words) - n_words)
        selected_words = words[start_idx:start_idx + n_words]
        
        return segment_type, segment_id, ' '.join(selected_words) 
    
    def get_segment_by_id(self, segment_id, preprocess_opts=None, augment_opts=None):
        """Get a specific segment by ID and apply processing."""
        # Find the segment with matching ID
        for segment in self.segments:
            if segment[1] == segment_id:
                segment_type, _, text = segment
                
                # Apply preprocessing if specified
                if preprocess_opts:
                    if preprocess_opts.get('remove_punctuation'):
                        text = TextPreprocessor.remove_punctuation(text)
                    if preprocess_opts.get('tokenize'):
                        text = ' '.join(TextPreprocessor.tokenize(text))
                    if preprocess_opts.get('pad_length'):
                        text = TextPreprocessor.pad_text(text, preprocess_opts['pad_length'])
                
                # Apply augmentation if specified
                if augment_opts:
                    if augment_opts.get('random_insertion'):
                        text = TextAugmenter.random_insertion(text, augment_opts['random_insertion'])
                    if augment_opts.get('synonym_replacement'):
                        text = TextAugmenter.synonym_replacement(text, augment_opts['synonym_replacement'])
                
                return segment_type, segment_id, text
                
        return None, None, None