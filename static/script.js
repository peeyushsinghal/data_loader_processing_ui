document.addEventListener('DOMContentLoaded', function() {
    // UI Elements
    const fileUpload = document.getElementById('file-upload');
    const sampleBtn = document.getElementById('sample-btn');
    const getSampleBtn = document.getElementById('get-sample-btn');
    const applyPreprocessBtn = document.getElementById('apply-preprocess-btn');
    const applyAugmentBtn = document.getElementById('apply-augment-btn');
    const padTextCheckbox = document.getElementById('pad-text');
    const padLengthGroup = document.getElementById('pad-length-group');
    const randomInsertionCheckbox = document.getElementById('random-insertion');
    const synonymReplacementCheckbox = document.getElementById('synonym-replacement');
    const augmentParamsGroup = document.getElementById('augment-params-group');

    let currentFilePath = null;
    let currentSegment = null;  // Store complete segment info

    // Event Listeners
    padTextCheckbox.addEventListener('change', function() {
        padLengthGroup.classList.toggle('hidden', !this.checked);
    });

    [randomInsertionCheckbox, synonymReplacementCheckbox].forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            augmentParamsGroup.classList.toggle('hidden', 
                !randomInsertionCheckbox.checked && !synonymReplacementCheckbox.checked);
        });
    });

    // Apply Preprocessing Button
    applyPreprocessBtn.addEventListener('click', async function() {
        if (!currentSegment) {
            alert('Please get a sample first');
            return;
        }
        await processPreprocessing(currentSegment);
    });

    // Apply Augmentation Button
    applyAugmentBtn.addEventListener('click', async function() {
        if (!currentSegment) {
            alert('Please get a sample first');
            return;
        }
        await processAugmentation(currentSegment);
    });

    fileUpload.addEventListener('change', async function(e) {
        if (e.target.files.length > 0) {
            const file = e.target.files[0];
            const formData = new FormData();
            formData.append('file', file);

            try {
                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                currentFilePath = data.file_path;
                await getNewSample();
            } catch (error) {
                console.error('Error uploading file:', error);
            }
        }
    });

    sampleBtn.addEventListener('click', async function() {
        currentFilePath = 'dataset/tiny-shakespeare.txt';
        await getNewSample();
    });

    getSampleBtn.addEventListener('click', async function() {
        if (currentFilePath) {
            await getNewSample();
        } else {
            alert('Please select a file first');
        }
    });

    async function getNewSample() {
        try {
            const response = await fetch('/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    file_path: currentFilePath,
                    n_words: 100
                })
            });

            const data = await response.json();
            currentSegment = data;  // Store complete segment
            
            // Update UI with original text
            document.getElementById('original-text').textContent = data.text;
            document.getElementById('preprocessed-text').textContent = data.text;
            document.getElementById('augmented-text').textContent = data.text;
        } catch (error) {
            console.error('Error getting new sample:', error);
        }
    }

    // Process preprocessing options
    async function processPreprocessing(originalSegment) {
        if (!originalSegment) return;

        const preprocessOpts = {
            remove_punctuation: document.getElementById('remove-punctuation').checked,
            tokenize: document.getElementById('tokenize').checked,
            pad_length: padTextCheckbox.checked ? 
                parseInt(document.getElementById('pad-length').value) : null
        };

        try {
            // If no preprocessing options selected, show original text
            if (!Object.values(preprocessOpts).some(v => v)) {
                document.getElementById('preprocessed-text').textContent = originalSegment.text;
                return;
            }

            // Create request body with original text
            const requestBody = {
                text: originalSegment.text,
                preprocess_opts: preprocessOpts
            };

            const preprocessResponse = await fetch('/preprocess', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestBody)
            });

            if (!preprocessResponse.ok) {
                throw new Error(`HTTP error! status: ${preprocessResponse.status}`);
            }

            const preprocessData = await preprocessResponse.json();
            if (preprocessData.error) {
                throw new Error(preprocessData.error);
            }

            document.getElementById('preprocessed-text').textContent = preprocessData.text;
        } catch (error) {
            console.error('Error processing text:', error);
            document.getElementById('preprocessed-text').textContent = 
                `Error: ${error.message}. Please try again.`;
        }
    }

    // Process augmentation options
    async function processAugmentation(originalSegment) {
        if (!originalSegment) return;

        const augmentOpts = {
            random_insertion: randomInsertionCheckbox.checked ? 
                parseInt(document.getElementById('random-insertion-count').value) : null,
            synonym_replacement: synonymReplacementCheckbox.checked ? 
                parseInt(document.getElementById('synonym-replacement-count').value) : null
        };

        try {
            // If no augmentation options selected, show original text
            if (!Object.values(augmentOpts).some(v => v)) {
                document.getElementById('augmented-text').textContent = originalSegment.text;
                return;
            }

            // Create request body with original text
            const requestBody = {
                text: originalSegment.text,
                augment_opts: augmentOpts
            };

            const augmentResponse = await fetch('/augment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestBody)
            });

            if (!augmentResponse.ok) {
                throw new Error(`HTTP error! status: ${augmentResponse.status}`);
            }

            const augmentData = await augmentResponse.json();
            if (augmentData.error) {
                throw new Error(augmentData.error);
            }

            document.getElementById('augmented-text').textContent = augmentData.text;
        } catch (error) {
            console.error('Error processing text:', error);
            document.getElementById('augmented-text').textContent = 
                `Error: ${error.message}. Please try again.`;
        }
    }
}); 