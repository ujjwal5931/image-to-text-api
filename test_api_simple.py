import requests

try:
    # Test the languages endpoint
    response = requests.get("http://localhost:8000/languages")
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {str(e)}") 