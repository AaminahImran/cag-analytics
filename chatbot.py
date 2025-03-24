"""
Simple command-line chatbot implementation.
The chatbot responds to user input based on predefined patterns and responses.
"""

import re
import random
import sys


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
            (r'weather', ['I don\'t have access to weather information, sorry!']),
            (r'time', ['I don\'t have access to the current time.']),
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
        
        # Check each pattern for a match
        for pattern, responses in self.patterns:
            if re.search(pattern, user_input):
                return random.choice(responses)
        
        # If no pattern matches, return a default response
        return random.choice(self.default_responses)

    def chat(self):
        """Run the chatbot conversation loop."""
        print("SimpleBot: Hello! I'm a simple chatbot. Type 'exit' or 'quit' to end our conversation.")
        
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
