#!/usr/bin/env python3
"""
A simple script to send a prompt to an LLM and display the response.
"""

import os
import os.path
import sys
import requests
import argparse
import json
from dotenv import load_dotenv

def get_system_prompt(system_prompt_path="./prompts/system_prompt.md"):
    """
    Read system prompt from file or use default if file not found.
    
    Args:
        system_prompt_path (str): Path to the file containing system prompt or just the prompt name
        
    Returns:
        str: The system prompt to use
    """
    default_prompt = "You are Claude, a helpful AI assistant. Provide clear, accurate, and concise responses."
    
    # If only a prompt name is provided (without path or extension), construct the full path
    if not os.path.dirname(system_prompt_path) and not system_prompt_path.endswith('.md'):
        system_prompt_path = os.path.join("./prompts", f"{system_prompt_path}.md")
    # If only a prompt name with extension is provided, construct the path
    elif not os.path.dirname(system_prompt_path) and system_prompt_path.endswith('.md'):
        system_prompt_path = os.path.join("./prompts", system_prompt_path)
    
    try:
        if os.path.exists(system_prompt_path):
            with open(system_prompt_path, 'r') as f:
                return f.read().strip()
        else:
            print(f"Warning: System prompt file not found at {system_prompt_path}. Using default.")
            return default_prompt
    except Exception as e:
        print(f"Error reading system prompt file: {str(e)}. Using default.")
        return default_prompt

def call_llm(prompt, system_prompt_path="./prompts/system_prompt.md", model="claude-3-7-sonnet-latest", max_tokens=1000):
    """
    Send a prompt to an LLM API and return the response.
    
    Args:
        prompt (str): The user's input prompt
        system_prompt_path (str): Path to the file containing system prompt
        model (str): The Claude model to use
        max_tokens (int): Maximum tokens for the response
        
    Returns:
        str: The LLM's response
    """
    # Load API key from environment variables
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        return "Error: API key not found. Please set the ANTHROPIC_API_KEY environment variable."
    
    # Get system prompt
    system_prompt = get_system_prompt(system_prompt_path)
    
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
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "system": system_prompt
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        result = response.json()
        return result["content"][0]["text"]
    
    except requests.exceptions.RequestException as e:
        return f"Error calling LLM API: {str(e)}"

def read_file_content(file_path):
    """
    Read content from a file.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        str: Content of the file
    """
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def main():
    """
    Main function to get user input and display LLM response.
    """
    parser = argparse.ArgumentParser(description="Send prompts to an LLM and display responses")
    parser.add_argument("--system-prompt", "-s", 
                        default="system_prompt",
                        help="Name of the prompt file in ./prompts/ directory or full path to prompt file")
    parser.add_argument("--model", "-m",
                        default="claude-3-7-sonnet-latest",
                        help="Claude model to use")
    parser.add_argument("--max-tokens", "-t",
                        type=int,
                        default=1000,
                        help="Maximum tokens for response")
    parser.add_argument("--file", "-f",
                        help="Use content from a file as the prompt")
    args = parser.parse_args()
    
    # If file is provided, use its content as the prompt
    if args.file:
        user_input = read_file_content(args.file)
        print(f"Using content from file: {args.file}")
        print("\nSending to LLM...")
        response = call_llm(user_input, args.system_prompt, args.model, args.max_tokens)
        print("\nLLM Response:")
        print(response)
        return
    
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
        response = call_llm(user_input, args.system_prompt, args.model, args.max_tokens)
        print("\nLLM Response:")
        print(response)
        print()

if __name__ == "__main__":
    main()
