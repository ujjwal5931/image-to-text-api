import requests
import json

# Test parameters
image_path = "test_images/sample_text.png"
api_url = "http://localhost:8000/extract-text"
languages = "en"
detail = 1  # Set detail level to 1 for bounding boxes

# Prepare the request
files = {"image": open(image_path, "rb")}
data = {"languages": languages, "detail": detail}

print(f"Sending request to {api_url}")
print(f"Image: {image_path}")
print(f"Languages: {languages}")
print(f"Detail level: {detail}")

try:
    # Send the request
    response = requests.post(api_url, files=files, data=data)
    
    # Print response status
    print(f"\nResponse status: {response.status_code}")
    
    # Check if the request was successful
    if response.status_code == 200:
        result = response.json()
        print("\nExtracted text with details:")
        
        if "results" in result:
            for item in result["results"]:
                print(f"- Text: {item['text']}")
                print(f"  Confidence: {item['confidence']:.2f}")
                print(f"  Bounding Box: {item['bounding_box']}")
            
            print(f"\nProcessing time: {result['processing_time']:.2f} seconds")
        else:
            print("No 'results' key in the response. Full response:")
            print(json.dumps(result, indent=2))
        
        print("\nFull API response:")
        print(json.dumps(result, indent=2))
    else:
        print(f"Error: {response.status_code} - {response.text}")
except Exception as e:
    print(f"Error: {str(e)}")
finally:
    files["image"].close() 