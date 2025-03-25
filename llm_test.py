#!/usr/bin/env python3
"""
A simple script to send a prompt to an LLM and display the response.
"""

import os
import sys
import requests
from dotenv import load_dotenv

def call_llm(prompt):
    """
    Send a prompt to an LLM API and return the response.
    
    Args:
        prompt (str): The user's input prompt
        
    Returns:
        str: The LLM's response
    """
    # Load API key from environment variables
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        return "Error: API key not found. Please set the OPENAI_API_KEY environment variable."
    
    # OpenAI API endpoint
    url = "https://api.openai.com/v1/chat/completions"
    
    # Request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # Request data
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
    
    except requests.exceptions.RequestException as e:
        return f"Error calling LLM API: {str(e)}"

def main():
    """
    Main function to get user input and display LLM response.
    """
    print("LLM Test - Enter a prompt (or 'quit' to exit):")
    
    while True:
        # Get user input
        user_input = input("> ")
        
        # Check if user wants to quit
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        
        # Call LLM and print response
        print("\nSending to LLM...")
        response = call_llm(user_input)
        print("\nLLM Response:")
        print(response)
        print()

if __name__ == "__main__":
    main()
