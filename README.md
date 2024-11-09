# Text Dataset Loader

A flexible text dataset loader with preprocessing and augmentation capabilities, available through both CLI and Web UI interfaces.

## Features

- Load and process any text file format
- Support for multiple text formats:
  - Dialogue-based texts (like plays)
  - Paragraph-based texts
  - Line-by-line texts
- Text preprocessing options:
  - Punctuation removal
  - Tokenization
  - Text padding
- Text augmentation options:
  - Random word insertion
  - Synonym replacement
- Multiple interfaces:
  - Web UI (FastAPI + HTML/CSS/JS)
  - Command Line Interface (CLI)
  - Python module

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd text-dataset-loader
```

2. Create and activate virtual environment:
```bash
python -m venv env_dataset
source env_dataset/bin/activate  # On Windows: env_dataset\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Using Web UI
```bash
# Start the FastAPI server
uvicorn app:app --reload

# Open browser at http://localhost:8000
```

### Using CLI
```bash
# Basic usage - get random 100-word segment
python cli.py dataset/sample.txt

# Get 5 samples with preprocessing
python cli.py dataset/sample.txt --samples 5 --remove-punctuation --tokenize
```

### Using as Python Module
```python
from dataset_loader import DatasetLoader

loader = DatasetLoader("dataset/sample.txt")
segment_type, segment_id, text = loader.get_random_segment(
    n_words=100,
    preprocess_opts={'remove_punctuation': True},
    augment_opts={'random_insertion': 2}
)
```

## Project Structure

```
.
├── app.py              # FastAPI server implementation
├── cli.py              # Command line interface
├── dataset_loader.py   # Core dataset loading functionality
├── dataset_utils.py    # Text processing utilities
├── requirements.txt    # Project dependencies
├── static/            # Frontend assets
│   ├── index.html     # Web UI HTML
│   ├── styles.css     # Web UI styles
│   └── script.js      # Web UI JavaScript
└── dataset/           # Sample datasets
    ├── sample.txt
    └── tiny-shakespeare.txt
```

## Detailed Usage

### Command Line Options

```bash
python cli.py [-h] [--words WORDS] [--samples SAMPLES] 
              [--remove-punctuation] [--tokenize] 
              [--pad-length PAD_LENGTH]
              [--random-insertion RANDOM_INSERTION]
              [--synonym-replacement SYNONYM_REPLACEMENT]
              file_path
```

Arguments:
- `file_path`: Path to input text file
- `--words`: Number of words per segment (default: 100)
- `--samples`: Number of samples to generate (default: 1)
- `--remove-punctuation`: Remove punctuation from text
- `--tokenize`: Tokenize the text
- `--pad-length`: Pad text to specified length
- `--random-insertion`: Number of random word insertions
- `--synonym-replacement`: Number of words to replace with synonyms

### Web UI Endpoints

#### POST /upload
Upload a text file for processing.

#### POST /process
Process text with specified options.

Request body:
```json
{
    "file_path": "path/to/file.txt",
    "n_words": 100,
    "preprocess_opts": {
        "remove_punctuation": false,
        "tokenize": false,
        "pad_length": null
    },
    "augment_opts": {
        "random_insertion": null,
        "synonym_replacement": null
    }
}
```

Response:
```json
{
    "segment_type": "PARAGRAPH",
    "segment_id": "P1",
    "text": "Sample text content..."
}
```

## Error Handling

The application handles:
- File not found errors
- Invalid file formats
- Invalid preprocessing/augmentation parameters
- Server errors

Common error messages:
- "file_path is required": Missing file path in request
- "File not found": Invalid file path
- "No valid segments found": Empty or invalid text file

## Notes

- NLTK data is downloaded automatically on first run
- Web UI server runs in reload mode by default
- For large files, CLI interface is recommended
- All text processing is done in memory
- Uploaded files are stored in 'uploads' directory