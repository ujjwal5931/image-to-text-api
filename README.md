# Image to Text API

A RESTful API for extracting text from images using EasyOCR with support for multiple languages.

## Features

- Extract text from images in 15+ languages
- Support for multiple languages in a single request
- Option to get detailed results including bounding boxes and confidence scores
- Fast and efficient text recognition

## API Endpoints

### GET /

Welcome message and basic information about the API.

### GET /languages

Returns a list of all supported languages with their codes.

### POST /extract-text

Extract text from an uploaded image.

**Parameters:**

- `image`: The image file to extract text from (required)
- `languages`: Comma-separated language codes (default: "en")
- `detail`: Detail level (0 for text only, 1 for text with bounding boxes and confidence scores)

**Example Response (detail=0):**

```json
{
  "text": "Hello world",
  "text_list": ["Hello", "world"],
  "languages": ["en"],
  "processing_time": 0.5
}
```

**Example Response (detail=1):**

```json
{
  "results": [
    {
      "text": "Hello",
      "confidence": 0.95,
      "bounding_box": [[10, 10], [50, 10], [50, 30], [10, 30]]
    },
    {
      "text": "world",
      "confidence": 0.92,
      "bounding_box": [[60, 10], [100, 10], [100, 30], [60, 30]]
    }
  ],
  "languages": ["en"],
  "processing_time": 0.5
}
```

## Supported Languages

- English (en)
- French (fr)
- Spanish (es)
- German (de)
- Italian (it)
- Portuguese (pt)
- Chinese (zh)
- Japanese (ja)
- Korean (ko)
- Russian (ru)
- Arabic (ar)
- Hindi (hi)
- Bengali (bn)
- Thai (th)
- Vietnamese (vi)

## Local Development

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/image-to-text-api.git
   cd image-to-text-api
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   uvicorn main:app --reload
   ```

4. Open http://localhost:8000/docs in your browser to access the Swagger UI.

## Deployment

This API is designed to be deployed on Render. Follow these steps:

1. Push your code to GitHub
2. Create a new Web Service on Render
3. Connect your GitHub repository
4. Use the following settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn -k uvicorn.workers.UvicornWorker main:app`

## License

MIT 