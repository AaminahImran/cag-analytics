#!/usr/bin/env python3
"""
A simple script to send a prompt to an LLM and display the response.
"""

import os
import os.path
import sys
import requests
from dotenv import load_dotenv

def call_llm(prompt, system_prompt_path="./prompts/system_prompt.md"):
    """
    Send a prompt to an LLM API and return the response.
    
    Args:
        prompt (str): The user's input prompt
        system_prompt_path (str): Path to the file containing system prompt
        
    Returns:
        str: The LLM's response
    """
    # Load API key from environment variables
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        return "Error: API key not found. Please set the ANTHROPIC_API_KEY environment variable."
    
    # Read system prompt from file
    try:
        if os.path.exists(system_prompt_path):
            with open(system_prompt_path, 'r') as f:
                system_prompt = f.read().strip()
        else:
            system_prompt = "You are Claude, a helpful AI assistant. Provide clear, accurate, and concise responses."
            print(f"Warning: System prompt file not found at {system_prompt_path}. Using default.")
    except Exception as e:
        system_prompt = "You are Claude, a helpful AI assistant. Provide clear, accurate, and concise responses."
        print(f"Error reading system prompt file: {str(e)}. Using default.")
    
    # Anthropic API endpoint
    url = "https://api.anthropic.com/v1/messages"
    
    # Request headers
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01"
    }
    
    # Request data
    data = {
        "model": "claude-3-opus-20240229",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000,
        "system": system_prompt
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        result = response.json()
        return result["content"][0]["text"]
    
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
