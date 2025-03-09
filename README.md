# Image to Text API

A RESTful API for extracting text from images using EasyOCR with support for multiple languages.

## Features

- Extract text from images in 15+ languages
- Support for multiple languages in a single request
- Option to get detailed results including bounding boxes and confidence scores
- Fast and efficient text recognition
- Memory-optimized for cloud deployment

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

## Deployment Options

### Option 1: Google Cloud Run (Recommended)

Google Cloud Run is ideal for this application due to its generous free tier and ability to handle resource-intensive tasks.

1. Install the Google Cloud SDK:
   - Download from: https://cloud.google.com/sdk/docs/install
   - Initialize with: `gcloud init`

2. Edit the `deploy_to_cloud_run.sh` script:
   - Replace `your-project-id` with your actual Google Cloud project ID

3. Make the script executable and run it:
   ```bash
   chmod +x deploy_to_cloud_run.sh
   ./deploy_to_cloud_run.sh
   ```

4. The script will:
   - Enable required APIs
   - Build and push your Docker container
   - Deploy to Cloud Run
   - Output the service URL

### Option 2: Railway.app

Railway offers a simpler deployment process:

1. Sign up at https://railway.app/

2. Install the Railway CLI:
   ```bash
   npm i -g @railway/cli
   ```

3. Login and deploy:
   ```bash
   railway login
   railway up
   ```

4. Alternatively, connect your GitHub repository in the Railway dashboard for automatic deployments.

### Option 3: Render (Original Option)

This API can also be deployed on Render:

1. Push your code to GitHub
2. Create a new Web Service on Render
3. Connect your GitHub repository
4. Use the following settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn -k uvicorn.workers.UvicornWorker main:app`

## Performance Considerations

- The API now includes image resizing to handle large images efficiently
- Memory management has been improved for cloud deployment
- For best performance, consider using a paid tier with more memory (2GB+)

## License

MIT 