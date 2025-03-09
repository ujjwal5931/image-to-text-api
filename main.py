import os
import io
import time
import easyocr
import numpy as np
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from PIL import Image
from typing import List, Optional

# Custom JSON encoder to handle NumPy types
class NumpyJSONEncoder:
    @staticmethod
    def convert_to_json_serializable(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, list):
            return [NumpyJSONEncoder.convert_to_json_serializable(item) for item in obj]
        elif isinstance(obj, dict):
            return {k: NumpyJSONEncoder.convert_to_json_serializable(v) for k, v in obj.items()}
        else:
            return obj

app = FastAPI(
    title="Image to Text API",
    description="API for extracting text from images using EasyOCR with multiple language support",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Dictionary to store reader instances for different language combinations
reader_instances = {}

# Available languages
AVAILABLE_LANGUAGES = {
    "en": "English",
    "fr": "French",
    "es": "Spanish",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "ru": "Russian",
    "ar": "Arabic",
    "hi": "Hindi",
    "bn": "Bengali",
    "th": "Thai",
    "vi": "Vietnamese"
}

@app.get("/", response_class=HTMLResponse)
async def root():
    return FileResponse("static/index.html")

@app.get("/languages")
async def get_languages():
    return {"available_languages": AVAILABLE_LANGUAGES}

def get_reader(languages: List[str]):
    """Get or create an EasyOCR reader for the specified languages"""
    # Sort languages to ensure consistent key for caching
    languages_key = "-".join(sorted(languages))
    
    if languages_key not in reader_instances:
        # Create a new reader instance
        reader_instances[languages_key] = easyocr.Reader(
            languages,
            gpu=False,  # Set to True if GPU is available
            download_enabled=True
        )
    
    return reader_instances[languages_key]

@app.post("/extract-text")
async def extract_text(
    image: UploadFile = File(...),
    languages: str = Form("en"),  # Default to English
    detail: int = Form(0)  # 0 for text only, 1 for text with bounding boxes
):
    # Validate languages
    language_list = [lang.strip() for lang in languages.split(",")]
    for lang in language_list:
        if lang not in AVAILABLE_LANGUAGES:
            raise HTTPException(
                status_code=400, 
                detail=f"Language '{lang}' not supported. Available languages: {', '.join(AVAILABLE_LANGUAGES.keys())}"
            )
    
    try:
        # Read the image
        image_content = await image.read()
        img = Image.open(io.BytesIO(image_content))
        
        # Convert to RGB if image has alpha channel
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        
        # Get the appropriate reader
        reader = get_reader(language_list)
        
        # Start time
        start_time = time.time()
        
        # Perform OCR
        results = reader.readtext(
            image=io.BytesIO(image_content).getvalue(),
            detail=True  # Always get detailed results and format based on detail parameter
        )
        
        # End time
        processing_time = time.time() - start_time
        
        # Format results based on detail level
        if detail == 0:
            text_results = [text for (_, text, _) in results]
            response_data = {
                "text": " ".join(text_results),
                "text_list": text_results,
                "languages": language_list,
                "processing_time": processing_time
            }
        else:
            text_results = []
            for (bbox, text, prob) in results:
                # Convert NumPy types to Python native types
                text_results.append({
                    "text": text,
                    "confidence": float(prob),
                    "bounding_box": NumpyJSONEncoder.convert_to_json_serializable(bbox)
                })
            response_data = {
                "results": text_results,
                "languages": language_list,
                "processing_time": processing_time
            }
        
        # Convert all NumPy types to Python native types
        response_data = NumpyJSONEncoder.convert_to_json_serializable(response_data)
        
        return JSONResponse(content=response_data)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True) 