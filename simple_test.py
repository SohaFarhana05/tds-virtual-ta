#!/usr/bin/env python3
"""
Simple API test script for TDS Virtual TA
"""
import requests
import json
import base64
import os


def test_api_endpoint(base_url="http://localhost:8000"):
    """Test the API with sample questions"""
    
    # Test 1: GPT model question
    print("Test 1: GPT model question")
    test_data = {
        "question": "The question asks to use gpt-3.5-turbo-0125 model but the ai-proxy provided by Anand sir only supports gpt-4o-mini. So should we just use gpt-4o-mini or use the OpenAI API for gpt3.5 turbo?"
    }
    
    try:
        response = requests.post(f"{base_url}/api/", json=test_data, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Answer: {result['answer']}")
            print(f"Links: {len(result['links'])} links provided")
            for link in result['links']:
                print(f"  - {link['text']}: {link['url']}")
        else:
            print(f"Error: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test 2: Dashboard scoring question
    print("Test 2: Dashboard scoring question")
    test_data = {
        "question": "If a student scores 10/10 on GA4 as well as a bonus, how would it appear on the dashboard?"
    }
    
    try:
        response = requests.post(f"{base_url}/api/", json=test_data, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Answer: {result['answer']}")
            print(f"Links: {len(result['links'])} links provided")
            for link in result['links']:
                print(f"  - {link['text']}: {link['url']}")
        else:
            print(f"Error: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test 3: Docker vs Podman question
    print("Test 3: Docker vs Podman question")
    test_data = {
        "question": "I know Docker but have not used Podman before. Should I use Docker for this course?"
    }
    
    try:
        response = requests.post(f"{base_url}/api/", json=test_data, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Answer: {result['answer']}")
            print(f"Links: {len(result['links'])} links provided")
            for link in result['links']:
                print(f"  - {link['text']}: {link['url']}")
        else:
            print(f"Error: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test 4: Future exam question
    print("Test 4: Future exam question")
    test_data = {
        "question": "When is the TDS Sep 2025 end-term exam?"
    }
    
    try:
        response = requests.post(f"{base_url}/api/", json=test_data, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Answer: {result['answer']}")
            print(f"Links: {len(result['links'])} links provided")
            for link in result['links']:
                print(f"  - {link['text']}: {link['url']}")
        else:
            print(f"Error: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")


def test_with_image():
    """Test API with image attachment"""
    print("Test 5: Question with image")
    
    # Check if we have an image file to test with
    image_path = "image.png"
    if os.path.exists(image_path):
        try:
            with open(image_path, "rb") as f:
                image_b64 = base64.b64encode(f.read()).decode('utf-8')
            
            test_data = {
                "question": "Should I use gpt-4o-mini which AI proxy supports, or gpt3.5 turbo?",
                "image": image_b64
            }
            
            response = requests.post("http://localhost:8000/api/", json=test_data, timeout=10)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"Answer: {result['answer']}")
                print(f"Links: {len(result['links'])} links provided")
            else:
                print(f"Error: {response.text}")
                
        except Exception as e:
            print(f"Error processing image: {e}")
    else:
        print("No image file found to test with")


if __name__ == "__main__":
    print("Testing TDS Virtual TA API")
    print("="*50)
    
    # Test if API is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ API is running!")
        else:
            print("❌ API is not responding correctly")
            exit(1)
    except requests.exceptions.RequestException:
        print("❌ API is not running. Please start it with: python app.py")
        exit(1)
    
    print("\nRunning tests...\n")
    test_api_endpoint()
    test_with_image()
    print("\nAll tests completed!")
