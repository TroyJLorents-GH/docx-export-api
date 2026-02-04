"""
Quick test script for the DOCX Export API
Run: python test_api.py
"""

import requests
import base64

API_URL = "http://localhost:8000"  # Change to your deployed URL

def test_export():
    payload = {
        "doc_type": "resume",
        "file_name": "test_resume",
        "title": "Jane Smith",
        "subtitle": "jane.smith@email.com | (555) 987-6543 | New York, NY",
        "sections": [
            {
                "heading": "Professional Summary",
                "content": "Results-driven **marketing professional** with 7+ years of experience in digital marketing and brand strategy."
            },
            {
                "heading": "Experience",
                "content": """**Marketing Director** at BrandCo (2020-Present)
- Led rebranding initiative increasing brand awareness by 60%
- Managed $2M annual marketing budget
- Built team of 8 marketing specialists

**Senior Marketing Manager** at AdAgency (2017-2020)
- Developed integrated campaigns for Fortune 500 clients
- Increased client retention by 35%"""
            },
            {
                "heading": "Education",
                "content": "**MBA, Marketing**, Columbia Business School (2017)\n**B.A. Communications**, NYU (2014)"
            },
            {
                "heading": "Skills",
                "content": "Digital Marketing, SEO/SEM, Google Analytics, HubSpot, Salesforce, Adobe Creative Suite"
            }
        ],
        "return_format": "base64"
    }

    response = requests.post(f"{API_URL}/export/docx", json=payload)

    if response.status_code == 200:
        data = response.json()
        print(f"✓ Success! Generated: {data['file_name']}")

        # Save the file locally
        docx_bytes = base64.b64decode(data['file_base64'])
        with open(data['file_name'], 'wb') as f:
            f.write(docx_bytes)
        print(f"✓ Saved to: {data['file_name']}")
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.text)


if __name__ == "__main__":
    # First check if API is running
    try:
        health = requests.get(f"{API_URL}/")
        if health.status_code == 200:
            print(f"API is running at {API_URL}")
            test_export()
        else:
            print("API returned unexpected status")
    except requests.exceptions.ConnectionError:
        print(f"Cannot connect to {API_URL}")
        print("Make sure to run: uvicorn main:app --reload")
