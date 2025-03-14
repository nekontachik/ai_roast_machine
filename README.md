# 🔥 AI Roast Machine 🧊

A fun tool to test, compare, and roast AI models with a humorous twist!

## What is AI Roast Machine?

AI Roast Machine is a tool that lets you test various AI models through OpenRouter, compare their responses, and generate fun, retro-style reports that roast the models' performance. It's both a practical testing tool and an entertaining way to evaluate AI capabilities.

## Features

- 🤖 **Test individual models** with custom prompts
- 🔄 **Compare multiple models** on the same prompt
- ⚖️ **Test models for bias** with specialized prompts
- 🤣 **Generate weird AI memes** for fun
- 📊 **Create retro-style HTML reports** with fun roasts and jokes
- 🎮 **Retro gaming aesthetic** for all reports
- **Test and Compare Models**: Compare responses from different AI models on the same prompts
- **Test Specific Models**: Test individual models with custom prompts
- **Bias Testing**: Evaluate models for potential biases
- **Meme Generation**: Create weird AI-themed memes
- **API**: Access all functionality through a FastAPI interface

## Getting Started

### Prerequisites

- Python 3.7+
- An OpenRouter API key (set in `.env` file)
- Docker (optional, for containerized usage)

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/ai-roast-machine.git
   cd ai-roast-machine
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your OpenRouter API key:
   ```
   OPENROUTER_API_KEY=your_api_key_here
   ```

### Running the Application

#### Using Python directly:

```
python -m src.menu
```

#### Using Docker:

```
docker-compose up
```

## Using AI Roast Machine

1. **Main Menu**: Choose from testing options:
   - Test and compare models
   - Test a specific model
   - Generate weird memes

2. **Viewing Reports**: Use the report viewer to see your generated reports:
   ```
   ./open_reports.py
   ```

3. **Report Types**:
   - **Model Comparison Reports**: Compare multiple models on the same prompt
   - **Single Model Test Reports**: Test one model with a custom prompt
   - **Bias Test Reports**: Evaluate a model for potential biases
   - **Meme Reports**: Fun AI-generated meme content

## Example Reports

The reports include:
- Fun roasts of each AI model
- Technical performance metrics
- Comparison tables
- Random AI jokes
- Retro gaming style UI

## Contributing

Contributions are welcome! Feel free to submit pull requests or open issues to suggest improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenRouter for providing access to various AI models
- All the AI models that were roasted in the making of this tool

## Usage

### Command Line Interface

Run the menu interface:

```bash
python -m src.menu
```

This will open an interactive menu with options to:
1. Test and compare models
2. Test a specific model
3. Generate weird memes
4. Exit

### API

Start the API server:

```bash
uvicorn src.api:app --reload --port 8000
```

API endpoints:
- `GET /`: API information
- `GET /models/`: Get available models
- `POST /query/`: Query a model with a prompt
- `POST /run-tests/`: Run bias tests on a model
- `GET /test-results/`: Get all test results
- `GET /test-results/{model}`: Get test results for a specific model
- `GET /health`: Health check

## Docker

Build and run with Docker:

```bash
docker-compose up -d
```

This will start both the API server and the menu interface.

## Testing

Run all tests:

```bash
python run_tests.py
```

Run tests with verbose output:

```bash
python run_tests.py -v
```

Run specific tests:

```bash
python run_tests.py -p test_openrouter_connector
```

## Project Structure

- `src/`: Source code
  - `menu.py`: Command line interface
  - `api.py`: FastAPI server
  - `openrouter_connector.py`: OpenRouter API connector
- `tests/`: Unit tests
- `docker/`: Docker configuration
- `test_results/`: Generated test results
- `memes/`: Generated memes

## Cleanup and Deployment

Before deploying to GitHub or any other public repository, make sure to:

1. **Remove sensitive information**:
   - Never commit your `.env` file with API keys
   - Use the provided `.env.example` as a template
   - Check for hardcoded API keys or credentials in the code

2. **Clean temporary files**:
   - Remove compiled Python files (`.pyc`, `__pycache__`)
   - Remove system files (`.DS_Store`)
   - Remove large files that shouldn't be in version control

3. **Run the cleanup script**:
   ```bash
   # Use the provided cleanup script
   ./cleanup.sh
   
   # Or manually remove compiled Python files and system files
   find . -name "*.pyc" -o -name "__pycache__" -o -name ".DS_Store" | xargs rm -rf
   ```

4. **Run tests before deployment**:
   ```bash
   python run_tests.py
   ```

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Your commit message"
   git push
   ```

## Security Considerations

- API keys and other sensitive information should be stored in the `.env` file
- The `.env` file is excluded from version control in `.gitignore`
- Always use environment variables for sensitive information, never hardcode them
- Test results and generated content are stored in directories that are excluded from version control
