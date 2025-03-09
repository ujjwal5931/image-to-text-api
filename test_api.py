import requests
import argparse
import os
import json

def test_api(image_path, languages="en", detail=0, api_url="http://localhost:8000"):
    """
    Test the image-to-text API with a local image file.
    
    Args:
        image_path (str): Path to the image file
        languages (str): Comma-separated language codes
        detail (int): Detail level (0 for text only, 1 for text with bounding boxes)
        api_url (str): API URL
    """
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found.")
        return
    
    # Get available languages
    try:
        response = requests.get(f"{api_url}/languages")
        available_languages = response.json()["available_languages"]
        print(f"Available languages: {json.dumps(available_languages, indent=2)}")
    except Exception as e:
        print(f"Error getting available languages: {str(e)}")
        return
    
    # Validate languages
    language_list = [lang.strip() for lang in languages.split(",")]
    for lang in language_list:
        if lang not in available_languages:
            print(f"Warning: Language '{lang}' not supported. Available languages: {', '.join(available_languages.keys())}")
            return
    
    # Prepare the request
    files = {"image": open(image_path, "rb")}
    data = {"languages": languages, "detail": detail}
    
    print(f"\nSending request to {api_url}/extract-text")
    print(f"Image: {image_path}")
    print(f"Languages: {languages}")
    print(f"Detail level: {detail}")
    
    try:
        # Send the request
        response = requests.post(f"{api_url}/extract-text", files=files, data=data)
        
        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            print("\nExtracted text:")
            
            if detail == 0:
                print(result["text"])
                print(f"\nProcessing time: {result['processing_time']:.2f} seconds")
            else:
                for item in result["results"]:
                    print(f"- {item['text']} (Confidence: {item['confidence']:.2f})")
                print(f"\nProcessing time: {result['processing_time']:.2f} seconds")
            
            print("\nFull API response:")
            print(json.dumps(result, indent=2))
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        files["image"].close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test the image-to-text API")
    parser.add_argument("image_path", help="Path to the image file")
    parser.add_argument("--languages", "-l", default="en", help="Comma-separated language codes (default: en)")
    parser.add_argument("--detail", "-d", type=int, default=0, choices=[0, 1], help="Detail level (0 for text only, 1 for text with bounding boxes)")
    parser.add_argument("--api-url", "-u", default="http://localhost:8000", help="API URL (default: http://localhost:8000)")
    
    args = parser.parse_args()
    test_api(args.image_path, args.languages, args.detail, args.api_url) 