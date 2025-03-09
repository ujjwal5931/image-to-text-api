import requests
import os
import json
import traceback

# Path to a test image
test_image_path = "test_images/sample_text.png"

if not os.path.exists(test_image_path):
    print(f"Test image not found: {test_image_path}")
    exit(1)

try:
    # Test the extract-text endpoint with detail=1
    files = {'image': open(test_image_path, 'rb')}
    data = {'languages': 'en', 'detail': '1'}
    
    print(f"Sending request to http://localhost:8000/extract-text")
    print(f"Image: {test_image_path}")
    print(f"Detail level: 1")
    
    response = requests.post("http://localhost:8000/extract-text", files=files, data=data, timeout=60)
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\nExtracted text with details:")
        
        if "results" in result:
            for item in result["results"]:
                print(f"- Text: {item['text']}")
                print(f"  Confidence: {item['confidence']:.2f}")
                print(f"  Bounding Box: {item['bounding_box']}")
            
            print(f"\nProcessing time: {result.get('processing_time', 0):.2f} seconds")
        else:
            print("No 'results' key in the response. Full response:")
            print(json.dumps(result, indent=2))
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Error: {str(e)}")
    traceback.print_exc()
finally:
    # Close the file
    if 'files' in locals() and 'image' in files:
        files['image'].close() 