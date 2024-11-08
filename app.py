from flask import Flask, request, jsonify
from dataset_loader import DatasetLoader

app = Flask(__name__)

@app.route('/get_random_segment', methods=['POST'])
def get_random_segment():
    try:
        data = request.get_json()
        
        # Required parameters
        file_path = data.get('file_path')
        if not file_path:
            return jsonify({'error': 'file_path is required'}), 400
            
        # Optional parameters
        n_words = data.get('n_words', 100)
        
        # Preprocessing options
        preprocess_opts = {
            'remove_punctuation': data.get('remove_punctuation', False),
            'tokenize': data.get('tokenize', False),
            'pad_length': data.get('pad_length')
        }
        
        # Augmentation options
        augment_opts = {
            'random_insertion': data.get('random_insertion'),
            'synonym_replacement': data.get('synonym_replacement')
        }
        
        # Initialize loader and get segment
        loader = DatasetLoader(file_path)
        segment_type, segment_id, text = loader.get_random_segment(
            n_words,
            preprocess_opts=preprocess_opts,
            augment_opts=augment_opts
        )
        
        return jsonify({
            'segment_type': segment_type,
            'segment_id': segment_id,
            'text': text
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 