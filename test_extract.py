import requests
import os
import traceback

# Path to a test image
test_image_path = "test_images/sample_text.png"

if not os.path.exists(test_image_path):
    print(f"Test image not found: {test_image_path}")
    exit(1)

try:
    # Test the extract-text endpoint
    files = {'image': open(test_image_path, 'rb')}
    data = {'languages': 'en', 'detail': '0'}
    
    print(f"Sending request to http://localhost:8000/extract-text")
    print(f"Image: {test_image_path}")
    
    response = requests.post("http://localhost:8000/extract-text", files=files, data=data, timeout=60)
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Extracted text: {result.get('text', '')}")
        print(f"Processing time: {result.get('processing_time', 0):.2f} seconds")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Error: {str(e)}")
    traceback.print_exc()
finally:
    # Close the file
    if 'files' in locals() and 'image' in files:
        files['image'].close() 