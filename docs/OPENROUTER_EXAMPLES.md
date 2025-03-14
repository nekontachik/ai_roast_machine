# OpenRouter Integration Examples

This document provides examples of how to use the OpenRouter integration in the AI Roast Machine project.

## CLI Examples

### Interactive Mode

Run the interactive CLI menu:

```bash
# Using the run_openrouter.sh script
./run_openrouter.sh cli

# Or directly with Python
python -m src.menu
```

### Command-line Arguments

List available models:

```bash
# Using the run_openrouter.sh script
./run_openrouter.sh list-models

# Or directly with Python
python -m src.menu --list-models
```

Test a specific model with a custom prompt:

```bash
# Using the run_openrouter.sh script
./run_openrouter.sh test mistral-7b "Explain quantum computing to a 10-year-old"

# Or directly with Python
python -m src.menu --model mistral-7b --prompt "Explain quantum computing to a 10-year-old"
```

Run a bias test on a specific model:

```bash
# Using the run_openrouter.sh script
./run_openrouter.sh bias-test claude-v2

# Or directly with Python
python -m src.menu --model claude-v2 --bias-test
```

## API Examples

Start the API server:

```bash
# Using the run_openrouter.sh script
./run_openrouter.sh api

# Or directly with Python
uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload
```

### API Requests

Get available models:

```bash
curl -X GET "http://localhost:8000/models/"
```

Query a model with a prompt:

```bash
curl -X POST "http://localhost:8000/query/" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral-7b",
    "prompt": "Explain quantum computing to a 10-year-old",
    "max_tokens": 500,
    "temperature": 0.7
  }'
```

Run bias tests on a model:

```bash
curl -X POST "http://localhost:8000/run-tests/" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral-7b"
  }'
```

Get all test results:

```bash
curl -X GET "http://localhost:8000/test-results/"
```

Get test results for a specific model:

```bash
curl -X GET "http://localhost:8000/test-results/mistral-7b"
```

## Jupyter Notebook Examples

Start the Jupyter notebook:

```bash
# Using the run_openrouter.sh script
./run_openrouter.sh jupyter

# Or directly with Python
jupyter notebook openrouter_tests.ipynb
```

The notebook contains examples for:

1. Fetching and displaying available models
2. Testing individual models with custom prompts
3. Comparing responses from multiple models
4. Testing models for potential bias
5. Saving and loading test results
6. Performing advanced analysis on model responses

## Docker Examples

Start all services including OpenRouter:

```bash
./run_docker.sh --openrouter
```

Start only OpenRouter services:

```bash
./run_docker.sh --only-openrouter
```

Run the OpenRouter CLI in Docker:

```bash
docker-compose run --rm openrouter-cli python -m src.menu
```

Test a model with OpenRouter in Docker:

```bash
docker-compose run --rm openrouter-cli python -m src.menu --model mistral-7b --prompt "Your prompt here"
```

Run bias tests with OpenRouter in Docker:

```bash
docker-compose run --rm openrouter-cli python -m src.menu --model mistral-7b --bias-test
```

## Python Code Examples

### Using the OpenRouter Connector

```python
from src.openrouter_connector import query_model, get_available_models, test_model_bias

# Get available models
models = get_available_models()
print(f"Available models: {[model['id'] for model in models]}")

# Query a model
response = query_model(
    prompt="Explain quantum computing to a 10-year-old",
    model="mistral-7b",
    max_tokens=500,
    temperature=0.7
)
print(f"Response: {response['choices'][0]['message']['content']}")

# Run bias test
bias_results = test_model_bias("mistral-7b")
print(f"Bias score: {bias_results['bias_score']}")
print(f"Potentially biased responses: {bias_results['potentially_biased_responses']}")
```

### Custom Analysis

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.openrouter_connector import query_model, extract_text_from_response

# Test multiple models
models_to_test = ["mistral-7b", "claude-v2", "gpt-3.5-turbo"]
prompt = "What are the ethical implications of AI?"

results = []
for model in models_to_test:
    response = query_model(prompt, model)
    text = extract_text_from_response(response)
    results.append({
        "model": model,
        "response": text,
        "word_count": len(text.split())
    })

# Convert to DataFrame
df = pd.DataFrame(results)

# Plot results
plt.figure(figsize=(10, 6))
sns.barplot(x="model", y="word_count", data=df)
plt.title("Response Length Comparison")
plt.ylabel("Word Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
``` 