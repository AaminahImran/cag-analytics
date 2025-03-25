# LLM Test Application

A simple command-line application for testing interactions with Anthropic's Claude AI models.

## Setup

1. Install dependencies:
   ```
   pip install -e .
   ```

2. Create a `.env` file in the project root with your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

3. Run the application:
   ```
   python llm_test.py
   ```

## Usage

Enter prompts at the command line. The application will send your prompt to Claude and display the response.

Type 'quit', 'exit', or 'q' to exit the application.
