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
   llm-test
   ```
   
   Or directly:
   ```
   python llm_test.py
   ```

## Usage

Enter prompts at the command line. The application will send your prompt to Claude and display the response.

Type 'quit', 'exit', or 'q' to exit the application.

### Command Line Options

- `--system-prompt`, `-s`: Specify a system prompt file (default: system_prompt)
- `--model`, `-m`: Choose the Claude model to use (default: claude-3-7-sonnet-latest)
- `--max-tokens`, `-t`: Set maximum tokens for response (default: 1000)
- `--file`, `-f`: Use content from a file as the prompt

### Examples

Use a specific system prompt:
```
llm-test --system-prompt expert_coder
```

Use a different model with increased token limit:
```
llm-test --model claude-3-5-sonnet-latest --max-tokens 2000
```

Process a file:
```
llm-test --file my_document.txt
```
