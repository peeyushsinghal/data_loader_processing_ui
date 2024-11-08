import argparse
from dataset_loader import DatasetLoader

def main():
    parser = argparse.ArgumentParser(description='Dataset loader CLI')
    parser.add_argument('file_path', help='Path to the text file')
    parser.add_argument('--words', type=int, default=100, help='Number of words to return')
    parser.add_argument('--samples', type=int, default=1, help='Number of samples to show')
    
    # Preprocessing options
    parser.add_argument('--remove-punctuation', action='store_true', help='Remove punctuation')
    parser.add_argument('--tokenize', action='store_true', help='Tokenize text')
    parser.add_argument('--pad-length', type=int, help='Pad text to specified length')
    
    # Augmentation options
    parser.add_argument('--random-insertion', type=int, help='Number of random insertions')
    parser.add_argument('--synonym-replacement', type=int, help='Number of synonym replacements')
    
    args = parser.parse_args()
    
    # Initialize loader
    loader = DatasetLoader(args.file_path)
    
    # Prepare options
    preprocess_opts = {
        'remove_punctuation': args.remove_punctuation,
        'tokenize': args.tokenize,
        'pad_length': args.pad_length
    }
    
    augment_opts = {
        'random_insertion': args.random_insertion,
        'synonym_replacement': args.synonym_replacement
    }
    
    # Get samples
    for i in range(args.samples):
        segment_type, segment_id, text = loader.get_random_segment(
            args.words,
            preprocess_opts=preprocess_opts,
            augment_opts=augment_opts
        )
        print(f"\nSample {i+1}:")
        print(f"Type: {segment_type}")
        print(f"ID: {segment_id}")
        print(f"Text: {text}")
        print("-" * 80)

if __name__ == "__main__":
    main() 