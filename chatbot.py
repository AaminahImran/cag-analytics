"""
Simple command-line chatbot implementation.
The chatbot responds to user input based on predefined patterns and responses.
"""

import re
import random
import sys
import os
import datetime

try:
    from weather_service import get_weather_response
    WEATHER_SERVICE_AVAILABLE = True
except ImportError:
    WEATHER_SERVICE_AVAILABLE = False


class SimpleBot:
    def __init__(self):
        # Define patterns and responses
        self.patterns = [
            (r'hi|hello|hey', ['Hello!', 'Hi there!', 'Hey! How can I help?']),
            (r'how are you', ['I\'m doing well, thanks!', 'I\'m good. How about you?']),
            (r'your name', ['I\'m SimpleBot, nice to meet you!', 'You can call me SimpleBot.']),
            (r'bye|goodbye|exit|quit', ['Goodbye!', 'See you later!', 'Bye!']),
            (r'help', ['I can chat about simple topics. Try saying hello or asking about my name.']),
            (r'thank you|thanks', ['You\'re welcome!', 'No problem!', 'Anytime!']),
            (r'weather in ([\w\s,]+)', ['I\'ll check the weather in {0} for you.']),
            (r'weather forecast for ([\w\s,]+)', ['Let me get the weather forecast for {0}.']),
            (r'weather', ['I can check the weather for you. Try asking "weather in [city name]" or "weather forecast for [city name]".']),
            (r'temperature in ([\w\s,]+)', ['Let me check the temperature in {0} for you.']),
            (r'time', [lambda: f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}."]),
            (r'date', [lambda: f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}."]),
            (r'who (are|made) you', ['I\'m a simple chatbot created as a demo.']),
        ]
        
        # Default responses when no pattern matches
        self.default_responses = [
            "I'm not sure I understand.",
            "Could you rephrase that?",
            "Interesting. Tell me more.",
            "I don't have a response for that yet."
        ]

    def get_response(self, user_input):
        """Generate a response based on user input."""
        user_input = user_input.lower().strip()
        
        # Check for exit command
        if user_input in ['exit', 'quit', 'bye', 'goodbye']:
            return random.choice(self.patterns[3][1])
        
        # Check for weather-related requests
        weather_patterns = [
            (r'weather in ([\w\s,]+)', 'weather'),
            (r'weather forecast for ([\w\s,]+)', 'weather'),
            (r'temperature in ([\w\s,]+)', 'weather')
        ]
        
        for pattern, req_type in weather_patterns:
            match = re.search(pattern, user_input)
            if match and WEATHER_SERVICE_AVAILABLE:
                city = match.group(1).strip()
                try:
                    return get_weather_response(city)
                except Exception as e:
                    return f"Sorry, I had trouble getting the weather information: {str(e)}"
        
        # Check each pattern for a match
        for pattern, responses in self.patterns:
            match = re.search(pattern, user_input)
            if match:
                response_template = random.choice(responses)
                
                # Handle function responses (for dynamic content like time)
                if callable(response_template):
                    return response_template()
                
                # Format the response with any captured groups
                if '{0}' in response_template and match.groups():
                    response = response_template.format(*match.groups())
                else:
                    response = response_template
                    
                return response
        
        # If no pattern matches, return a default response
        return random.choice(self.default_responses)

    def chat(self):
        """Run the chatbot conversation loop."""
        print("SimpleBot: Hello! I'm a simple chatbot. Type 'exit' or 'quit' to end our conversation.")
        
        # Display available features
        features = [
            "- Chat about various topics",
            "- Check weather (try 'weather in London')",
            "- Get current time (try 'what time is it')",
            "- Get current date (try 'what is today's date')"
        ]
        
        print("SimpleBot: Here are some things I can do:")
        for feature in features:
            print(f"SimpleBot: {feature}")
        
        while True:
            try:
                user_input = input("You: ")
                if user_input.lower().strip() in ['exit', 'quit', 'bye', 'goodbye']:
                    print(f"SimpleBot: {self.get_response(user_input)}")
                    break
                
                response = self.get_response(user_input)
                print(f"SimpleBot: {response}")
            
            except KeyboardInterrupt:
                print("\nSimpleBot: Goodbye!")
                break
            except EOFError:
                print("\nSimpleBot: Goodbye!")
                break


def main():
    """Main function to run the chatbot."""
    bot = SimpleBot()
    bot.chat()


if __name__ == "__main__":
    main()
