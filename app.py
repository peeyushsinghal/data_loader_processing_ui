from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
from dataset_loader import DatasetLoader
from dataset_utils import TextPreprocessor, TextAugmenter

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

class ProcessRequest(BaseModel):
    file_path: str
    n_words: Optional[int] = 100
    preprocess_opts: Optional[Dict[str, Any]] = None
    augment_opts: Optional[Dict[str, Any]] = None
    segment_id: Optional[str] = None

class TextRequest(BaseModel):
    text: str
    preprocess_opts: Optional[Dict[str, Any]] = None
    augment_opts: Optional[Dict[str, Any]] = None

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = f"uploads/{file.filename}"
        os.makedirs("uploads", exist_ok=True)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        return {"file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process")
async def process_text(request: ProcessRequest):
    try:
        loader = DatasetLoader(request.file_path)
        
        if request.segment_id:
            segment_type, segment_id, text = loader.get_segment_by_id(
                request.segment_id,
                preprocess_opts=request.preprocess_opts,
                augment_opts=request.augment_opts
            )
        else:
            segment_type, segment_id, text = loader.get_random_segment(
                n_words=request.n_words,
                preprocess_opts=request.preprocess_opts,
                augment_opts=request.augment_opts
            )
        
        return {
            "segment_type": segment_type,
            "segment_id": segment_id,
            "text": text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/preprocess")
async def preprocess_text(request: TextRequest):
    try:
        text = request.text
        
        # Apply preprocessing if specified
        if request.preprocess_opts:
            if request.preprocess_opts.get('remove_punctuation'):
                text = TextPreprocessor.remove_punctuation(text)
            if request.preprocess_opts.get('tokenize'):
                text = ' '.join(TextPreprocessor.tokenize(text))
            if request.preprocess_opts.get('pad_length'):
                text = TextPreprocessor.pad_text(text, request.preprocess_opts['pad_length'])
        
        return {"text": text}
    except Exception as e:
        print(f"Preprocessing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/augment")
async def augment_text(request: TextRequest):
    try:
        text = request.text
        
        # Apply augmentation if specified
        if request.augment_opts:
            if request.augment_opts.get('random_insertion'):
                text = TextAugmenter.random_insertion(text, request.augment_opts['random_insertion'])
            if request.augment_opts.get('synonym_replacement'):
                text = TextAugmenter.synonym_replacement(text, request.augment_opts['synonym_replacement'])
        
        return {"text": text}
    except Exception as e:
        print(f"Augmentation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 