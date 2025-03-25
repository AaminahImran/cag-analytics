# LLM Test Application

A simple application for testing interactions with Anthropic's Claude AI models, available in both command-line and web UI versions. This tool allows you to quickly prototype and test prompts with Claude models.

## Setup

1. Install dependencies:
   ```
   pip install -e .
   ```

2. Create a `.env` file in the project root with your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

3. (Optional) For BigQuery functionality, set up Google Cloud credentials:
   ```
   export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/credentials.json
   ```

## Command-Line Interface

Run the CLI application:
```
llm-test
```

Or directly:
```
python llm_test.py
```

### Command Line Options

- `--system-prompt`, `-s`: Specify a system prompt file (default: system_prompt)
- `--model`, `-m`: Choose the Claude model to use (default: claude-3-7-sonnet-latest)
- `--max-tokens`, `-t`: Set maximum tokens for response (default: 1000)
- `--file`, `-f`: Use content from a file as the prompt

### CLI Examples

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

## Web Interface

Run the Streamlit web interface:
```
streamlit run llm_ui.py
```

### Web UI Features

- Chat-like interface for conversations with the LLM
- Select different system prompts from the sidebar
- View the content of the selected system prompt
- Restart conversations with a single click
- Persistent chat history during your session

## BigQuery Integration

The application includes BigQuery integration for data analysis:

```python
from bigquery_runner import init_client, run_query

# Initialize client
client = init_client()

# Run a query
query = "SELECT * FROM `project.dataset.table` LIMIT 10"
results = run_query(client, query)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
