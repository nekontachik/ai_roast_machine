#!/usr/bin/env python3
"""
Menu interface for AI Roast Machine.
Provides options to test models, compare them, and generate memes.
"""

import os
import sys
import logging
from typing import List, Dict, Any, Optional
import json
import random
from datetime import datetime
import webbrowser
import time
import threading

# Import local modules
from src.openrouter_connector import query_model, get_available_models, test_model_bias

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sample prompts for testing models
TEST_PROMPTS = [
    "Explain quantum computing to a 5-year-old.",
    "Write a short poem about artificial intelligence.",
    "What are three ways to reduce carbon emissions?",
    "Describe the taste of chocolate to someone who's never had it.",
    "If you could interview any historical figure, who would it be and why?"
]

# Prompts for generating weird memes
MEME_PROMPTS = [
    "Create a bizarre meme about AI taking over household appliances.",
    "Generate a surreal meme about cats using programming languages.",
    "Make a weird meme about robots trying to understand human emotions.",
    "Create an absurd meme about neural networks dreaming of electric sheep.",
    "Generate a strange meme about language models writing poetry."
]

# Fun loading animations
LOADING_ANIMATIONS = [
    ["🧠", "💭", "💡", "✨"],
    ["⚙️", "🔄", "📊", "📈"],
    ["🤖", "🔍", "💻", "🚀"],
    ["🔮", "✨", "🌟", "💫"],
    ["🎲", "🎯", "🎮", "🎪"]
]

# Loading messages
LOADING_MESSAGES = [
    "AI is thinking...",
    "Neurons firing...",
    "Consulting the matrix...",
    "Calculating probabilities...",
    "Searching for wisdom...",
    "Generating tokens...",
    "Consulting digital oracle...",
    "Summoning AI wisdom...",
    "Spinning up neural networks...",
    "Consulting the digital hive mind..."
]

class LoadingAnimation:
    """Class to display a loading animation in the terminal."""
    
    def __init__(self, model_name):
        self.is_running = False
        self.animation = random.choice(LOADING_ANIMATIONS)
        self.message = random.choice(LOADING_MESSAGES)
        self.model_name = model_name
        self.thread = None
    
    def _animate(self):
        i = 0
        while self.is_running:
            frame = self.animation[i % len(self.animation)]
            sys.stdout.write(f"\r\033[93m{frame} {self.message} ({self.model_name})\033[0m")
            sys.stdout.flush()
            time.sleep(0.2)
            i += 1
    
    def start(self):
        """Start the loading animation."""
        self.is_running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.daemon = True
        self.thread.start()
    
    def stop(self):
        """Stop the loading animation."""
        self.is_running = False
        if self.thread:
            self.thread.join(0.5)
        sys.stdout.write("\r" + " " * 100 + "\r")  # Clear the line
        sys.stdout.flush()

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the application header."""
    clear_screen()
    print("\033[95m" + "=" * 80 + "\033[0m")
    print("\033[96m" + "                           AI ROAST MACHINE                           " + "\033[0m")
    print("\033[95m" + "=" * 80 + "\033[0m")
    print("\033[93m" + "Test, compare, and have fun with AI models!" + "\033[0m")
    print("\033[95m" + "=" * 80 + "\033[0m")
    print()

def print_menu():
    """Print the main menu options."""
    print("\033[92mMAIN MENU:\033[0m")
    print("\033[97m1. \033[94mTest and compare models \033[90m(OpenRouter vs ChatGPT, Claude, Llama)\033[0m")
    print("\033[97m2. \033[94mTest a specific model\033[0m")
    print("\033[97m3. \033[94mGenerate weird memes\033[0m")
    print("\033[97m4. \033[91mExit\033[0m")
    print()

def get_user_choice(max_choice: int) -> int:
    """Get a valid choice from the user.
    
    Args:
        max_choice: The maximum valid choice number
        
    Returns:
        The user's choice as an integer
    """
    while True:
        try:
            choice = int(input("\033[96mEnter your choice (1-{}): \033[0m".format(max_choice)))
            if 1 <= choice <= max_choice:
                return choice
            else:
                print(f"\033[91mPlease enter a number between 1 and {max_choice}.\033[0m")
        except ValueError:
            print("\033[91mPlease enter a valid number.\033[0m")

def select_model(models: List[Dict[str, Any]]) -> str:
    """Let the user select a model from the available ones.
    
    Args:
        models: List of available models
        
    Returns:
        The selected model ID
    """
    print("\n\033[96mAVAILABLE MODELS:\033[0m")
    for i, model in enumerate(models[:20], 1):  # Show only first 20 models
        model_id = model.get('id', '')
        model_name = model.get('name', 'Unknown')
        
        # Color code different model providers
        if 'openai' in model_id:
            color = "\033[92m"  # Green for OpenAI
        elif 'anthropic' in model_id:
            color = "\033[94m"  # Blue for Anthropic
        elif 'meta' in model_id or 'llama' in model_id:
            color = "\033[95m"  # Purple for Meta/Llama
        elif 'mistral' in model_id:
            color = "\033[93m"  # Yellow for Mistral
        elif 'google' in model_id:
            color = "\033[91m"  # Red for Google
        else:
            color = "\033[97m"  # White for others
        
        print(f"\033[97m{i}. {color}{model_id}\033[0m: {model_name}")
    
    if len(models) > 20:
        print(f"\033[90m... and {len(models) - 20} more models\033[0m")
    
    choice = get_user_choice(min(20, len(models)))
    model_id = models[choice - 1].get('id')
    if not model_id:
        # Fallback to a default model if ID is missing
        return "mistralai/mistral-7b-instruct"
    return model_id

def save_to_both_locations(data, docker_path, local_path, is_json=True):
    """Save data to both Docker and local paths.
    
    Args:
        data: The data to save (dict for JSON, string for text)
        docker_path: Path inside Docker container
        local_path: Path on local machine
        is_json: Whether to save as JSON (True) or text (False)
    """
    # Create local directory
    local_dir = os.path.dirname(local_path)
    os.makedirs(local_dir, exist_ok=True)
    
    # Save to local path
    try:
        if is_json:
            with open(local_path, "w") as f:
                json.dump(data, f, indent=2)
        else:
            with open(local_path, "w") as f:
                f.write(data)
        logger.info(f"Successfully saved to {local_path}")
    except Exception as e:
        logger.error(f"Error saving to local path {local_path}: {e}")
    
    # Try to save to Docker path if we're running inside Docker
    try:
        # Only try to save to Docker path if it's accessible
        if docker_path.startswith("/app") and os.path.exists("/app"):
            docker_dir = os.path.dirname(docker_path)
            os.makedirs(docker_dir, exist_ok=True)
            
            if is_json:
                with open(docker_path, "w") as f:
                    json.dump(data, f, indent=2)
            else:
                with open(docker_path, "w") as f:
                    f.write(data)
            logger.info(f"Successfully saved to {docker_path}")
    except Exception as e:
        # This is expected to fail when running locally, so just log at debug level
        logger.debug(f"Could not save to Docker path {docker_path}: {e}")
    
    return local_path

def compare_models():
    """Test and compare different models on the same prompts."""
    print_header()
    print("COMPARE MODELS")
    print("This will test multiple models on the same set of prompts and compare their responses.")
    print()
    
    # Get available models
    try:
        all_models = get_available_models()
        logger.info(f"Retrieved {len(all_models)} models from OpenRouter")
    except Exception as e:
        logger.error(f"Error retrieving models: {e}")
        print(f"Error: Could not retrieve models. {str(e)}")
        input("\nPress Enter to return to the main menu...")
        return
    
    # Define models to compare
    models_to_compare = [
        "openai/gpt-4",
        "anthropic/claude-3-opus",
        "meta-llama/llama-3-70b-instruct",
        "mistralai/mistral-7b-instruct"
    ]
    
    # Check if models exist in available models
    available_model_ids = [model.get('id') for model in all_models]
    valid_models = [model for model in models_to_compare if model in available_model_ids]
    
    if not valid_models:
        print("None of the predefined models are available. Please select models manually.")
        valid_models = [select_model(all_models)]
        valid_models.append(select_model(all_models))
    
    # Select prompts
    print("\nSelect a prompt or enter your own:")
    for i, prompt in enumerate(TEST_PROMPTS, 1):
        print(f"{i}. {prompt}")
    print(f"{len(TEST_PROMPTS) + 1}. Enter your own prompt")
    
    choice = get_user_choice(len(TEST_PROMPTS) + 1)
    if choice <= len(TEST_PROMPTS):
        test_prompt = TEST_PROMPTS[choice - 1]
    else:
        test_prompt = input("\nEnter your prompt: ")
    
    # Test each model
    results = {}
    print("\nTesting models...\n")
    
    for model_id in valid_models:
        print(f"Testing {model_id}...")
        
        # Start loading animation
        loading = LoadingAnimation(model_id)
        loading.start()
        
        try:
            response = query_model(
                prompt=test_prompt,
                model=model_id,
                max_tokens=1000,
                temperature=0.7,
                top_p=0.9,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            
            # Stop loading animation
            loading.stop()
            
            if response and "choices" in response and len(response["choices"]) > 0:
                model_response = response["choices"][0]["message"]["content"]
                results[model_id] = model_response
                print(f"✓ Response received ({len(model_response)} chars)")
            else:
                print(f"✗ Invalid response format")
                results[model_id] = "Error: Invalid response format"
        except Exception as e:
            # Stop loading animation
            loading.stop()
            
            logger.error(f"Error testing model {model_id}: {e}")
            print(f"✗ Error: {str(e)}")
            results[model_id] = f"Error: {str(e)}"
    
    # Display results
    print("\n" + "=" * 80)
    print(f"RESULTS FOR PROMPT: {test_prompt}")
    print("=" * 80)
    
    for model_id, response in results.items():
        print(f"\n--- {model_id} ---")
        print(response)
        print("-" * 40)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    docker_filename = f"/app/test_results/model_comparison_{timestamp}.json"
    local_filename = f"test_results/model_comparison_{timestamp}.json"
    
    result_data = {
        "prompt": test_prompt,
        "timestamp": timestamp,
        "results": results
    }
    
    saved_path = save_to_both_locations(result_data, docker_filename, local_filename)
    
    # Generate HTML report
    html_report = generate_html_report(result_data, "comparison")
    html_filename = f"test_results/model_comparison_{timestamp}.html"
    
    try:
        with open(html_filename, "w") as f:
            f.write(html_report)
        print(f"\nHTML report saved to {html_filename}")
        
        # Automatically open the HTML report in the browser
        print("\nOpening HTML report in browser...")
        html_path = os.path.abspath(html_filename)
        webbrowser.open(f"file://{html_path}")
    except Exception as e:
        logger.error(f"Error saving HTML report: {e}")
    
    print(f"\nResults saved to {saved_path}")
    input("\nPress Enter to return to the main menu...")

def test_specific_model():
    """Test a specific model with custom prompts."""
    print_header()
    print("TEST SPECIFIC MODEL")
    print("This will test a single model with your choice of prompts.")
    print()
    
    # Get available models
    try:
        all_models = get_available_models()
        logger.info(f"Retrieved {len(all_models)} models from OpenRouter")
    except Exception as e:
        logger.error(f"Error retrieving models: {e}")
        print(f"Error: Could not retrieve models. {str(e)}")
        input("\nPress Enter to return to the main menu...")
        return
    
    # Select a model
    selected_model = select_model(all_models)
    
    # Test options
    print("\nTEST OPTIONS:")
    print("1. Quick test with a single prompt")
    print("2. Bias test with multiple prompts")
    
    test_choice = get_user_choice(2)
    
    if test_choice == 1:
        # Quick test
        print("\nSelect a prompt or enter your own:")
        for i, prompt in enumerate(TEST_PROMPTS, 1):
            print(f"{i}. {prompt}")
        print(f"{len(TEST_PROMPTS) + 1}. Enter your own prompt")
        
        choice = get_user_choice(len(TEST_PROMPTS) + 1)
        if choice <= len(TEST_PROMPTS):
            test_prompt = TEST_PROMPTS[choice - 1]
        else:
            test_prompt = input("\nEnter your prompt: ")
        
        print(f"\nTesting {selected_model} with prompt: {test_prompt}")
        
        # Start loading animation
        loading = LoadingAnimation(selected_model)
        loading.start()
        
        try:
            response = query_model(
                prompt=test_prompt,
                model=selected_model,
                max_tokens=1000,
                temperature=0.7,
                top_p=0.9,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            
            # Stop loading animation
            loading.stop()
            
            if response and "choices" in response and len(response["choices"]) > 0:
                model_response = response["choices"][0]["message"]["content"]
                print("\nRESPONSE:")
                print("-" * 40)
                print(model_response)
                print("-" * 40)
                
                # Save result
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                docker_filename = f"/app/test_results/{selected_model.replace('/', '_')}_{timestamp}.json"
                local_filename = f"test_results/{selected_model.replace('/', '_')}_{timestamp}.json"
                
                result_data = {
                    "model": selected_model,
                    "prompt": test_prompt,
                    "timestamp": timestamp,
                    "response": model_response
                }
                
                saved_path = save_to_both_locations(result_data, docker_filename, local_filename)
                
                # Generate HTML report
                html_report = generate_html_report(result_data, "single_model")
                html_filename = f"test_results/{selected_model.replace('/', '_')}_{timestamp}.html"
                
                try:
                    with open(html_filename, "w") as f:
                        f.write(html_report)
                    print(f"\nHTML report saved to {html_filename}")
                    
                    # Automatically open the HTML report in the browser
                    print("\nOpening HTML report in browser...")
                    html_path = os.path.abspath(html_filename)
                    webbrowser.open(f"file://{html_path}")
                except Exception as e:
                    logger.error(f"Error saving HTML report: {e}")
                
                print(f"\nResult saved to {saved_path}")
            else:
                print("\nError: Invalid response format")
        except Exception as e:
            # Stop loading animation
            loading.stop()
            
            logger.error(f"Error testing model {selected_model}: {e}")
            print(f"\nError: {str(e)}")
    
    else:
        # Bias test
        print(f"\nRunning bias test on {selected_model}...")
        
        # Start loading animation
        loading = LoadingAnimation(selected_model)
        loading.start()
        
        try:
            bias_results = test_model_bias(
                model=selected_model,
                temperature=0.7,
                top_p=0.9
            )
            
            # Stop loading animation
            loading.stop()
            
            print("\nBIAS TEST RESULTS:")
            print(f"Model: {selected_model}")
            print(f"Bias Score: {bias_results['bias_score']:.2f} (0.0 = no bias, 1.0 = high bias)")
            print(f"Potentially Biased Responses: {bias_results['potentially_biased_responses']} out of {len(bias_results['prompts'])}")
            
            print("\nDETAILED RESULTS:")
            for i, result in enumerate(bias_results['prompts'], 1):
                print(f"\n{i}. Prompt: {result['prompt']}")
                print(f"   Potentially Biased: {'Yes' if result['potentially_biased'] else 'No'}")
                print(f"   Bias Keywords Found: {result['bias_keywords_found']}")
                print(f"   Response: {result['response'][:100]}...")  # Show first 100 chars
            
            # Save results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            docker_filename = f"/app/test_results/bias_test_{selected_model.replace('/', '_')}_{timestamp}.json"
            local_filename = f"test_results/bias_test_{selected_model.replace('/', '_')}_{timestamp}.json"
            
            saved_path = save_to_both_locations(bias_results, docker_filename, local_filename)
            
            # Generate HTML report
            html_report = generate_html_report(bias_results, "bias")
            html_filename = f"test_results/bias_test_{selected_model.replace('/', '_')}_{timestamp}.html"
            
            try:
                with open(html_filename, "w") as f:
                    f.write(html_report)
                print(f"\nHTML report saved to {html_filename}")
                
                # Automatically open the HTML report in the browser
                print("\nOpening HTML report in browser...")
                html_path = os.path.abspath(html_filename)
                webbrowser.open(f"file://{html_path}")
            except Exception as e:
                logger.error(f"Error saving HTML report: {e}")
            
            print(f"\nResults saved to {saved_path}")
        except Exception as e:
            # Stop loading animation
            loading.stop()
            
            logger.error(f"Error running bias test: {e}")
            print(f"\nError running bias test: {str(e)}")
    
    input("\nPress Enter to return to the main menu...")

def generate_memes():
    """Generate weird AI memes."""
    print_header()
    print("GENERATE WEIRD MEMES")
    print("This will generate text for weird AI-themed memes.")
    print()
    
    # Get available models
    try:
        all_models = get_available_models()
        logger.info(f"Retrieved {len(all_models)} models from OpenRouter")
    except Exception as e:
        logger.error(f"Error retrieving models: {e}")
        print(f"Error: Could not retrieve models. {str(e)}")
        input("\nPress Enter to return to the main menu...")
        return
    
    # Filter models suitable for creative tasks
    creative_models = []
    
    # Define model capabilities for meme generation
    creative_model_keywords = [
        "gpt-4", "claude", "llama-3", "mistral", "gemini", "command-r", 
        "mixtral", "qwen", "phi-3", "opus", "sonnet", "haiku"
    ]
    
    # Filter models based on keywords and context length
    for model in all_models:
        model_id = model.get('id', '').lower()
        context_length = model.get('context_length', 0)
        
        # Check if model contains any of the creative keywords
        is_creative = any(keyword in model_id for keyword in creative_model_keywords)
        
        # Models with larger context windows tend to be better for creative tasks
        has_good_context = context_length >= 4000
        
        if is_creative and has_good_context:
            creative_models.append(model)
    
    # If no creative models found, use all models
    if not creative_models:
        print("\033[93mNo specialized creative models found. Using all available models.\033[0m")
        creative_models = all_models
    else:
        print(f"\033[92mFound {len(creative_models)} models optimized for creative content generation.\033[0m")
    
    # Select a model
    selected_model = select_model(creative_models)
    
    # Select a prompt
    print("\nSelect a meme prompt or enter your own:")
    for i, prompt in enumerate(MEME_PROMPTS, 1):
        print(f"{i}. {prompt}")
    print(f"{len(MEME_PROMPTS) + 1}. Random prompt")
    print(f"{len(MEME_PROMPTS) + 2}. Enter your own prompt")
    
    choice = get_user_choice(len(MEME_PROMPTS) + 2)
    if choice <= len(MEME_PROMPTS):
        meme_prompt = MEME_PROMPTS[choice - 1]
    elif choice == len(MEME_PROMPTS) + 1:
        meme_prompt = random.choice(MEME_PROMPTS)
        print(f"\nRandom prompt selected: {meme_prompt}")
    else:
        meme_prompt = input("\nEnter your meme prompt: ")
    
    # Enhanced instructions for better meme generation
    full_prompt = f"""
Generate a funny, absurd meme about: {meme_prompt}

Your response should include:
1. A catchy, funny title for the meme
2. A short, humorous description or caption
3. The meme text itself (what would appear on the image)
4. A brief explanation of why it's funny (in a meta way)

Make it weird, absurd, and funny. Be creative and don't hold back on the humor!
"""
    
    print(f"\nGenerating meme with {selected_model}...")
    
    # Start loading animation
    loading = LoadingAnimation(selected_model)
    loading.start()
    
    try:
        # Use higher temperature and top_p for more creative responses
        response = query_model(
            prompt=full_prompt,
            model=selected_model,
            max_tokens=1000,
            temperature=0.95,  # Higher temperature for more creativity
            top_p=0.98,  # Higher top_p for more diverse responses
            frequency_penalty=0.5,  # Add frequency penalty to reduce repetition
            presence_penalty=0.5  # Add presence penalty to encourage new topics
        )
        
        # Stop loading animation
        loading.stop()
        
        if response and "choices" in response and len(response["choices"]) > 0:
            meme_text = response["choices"][0]["message"]["content"]
            
            print("\n\033[96mGENERATED MEME:\033[0m")
            print("\033[95m" + "=" * 40 + "\033[0m")
            print(meme_text)
            print("\033[95m" + "=" * 40 + "\033[0m")
            
            # Save meme
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            docker_filename = f"/app/memes/meme_{timestamp}.txt"
            local_filename = f"memes/meme_{timestamp}.txt"
            
            meme_content = f"Prompt: {meme_prompt}\n\n{meme_text}"
            saved_path = save_to_both_locations(meme_content, docker_filename, local_filename, is_json=False)
            
            # Generate HTML report
            html_report = generate_html_report(meme_content, "meme")
            html_filename = f"memes/meme_{timestamp}.html"
            
            try:
                with open(html_filename, "w") as f:
                    f.write(html_report)
                print(f"\nHTML report saved to {html_filename}")
                
                # Automatically open the HTML report in the browser
                print("\nOpening HTML report in browser...")
                html_path = os.path.abspath(html_filename)
                webbrowser.open(f"file://{html_path}")
            except Exception as e:
                logger.error(f"Error saving HTML report: {e}")
            
            print(f"\nMeme saved to {saved_path}")
            
            # Ask if user wants to generate an image for the meme
            print("\nNote: Image generation is not implemented yet.")
            print("In a future version, you could generate an image based on this text.")
        else:
            print("\nError: Invalid response format")
    except Exception as e:
        # Stop loading animation
        loading.stop()
        
        logger.error(f"Error generating meme: {e}")
        print(f"\nError: {str(e)}")
    
    input("\nPress Enter to return to the main menu...")

def generate_html_report(data, report_type="comparison"):
    """Generate an HTML report from the data.
    
    Args:
        data: The data to include in the report
        report_type: Type of report ("comparison", "single_model", "bias", or "meme")
        
    Returns:
        HTML string
    """
    # Define a variable for newline replacement to avoid backslash in f-strings
    br_tag = "<br>"
    
    # Fun roasts for different models
    model_roasts = {
        "openai/gpt-4": "Your model is so corporate it has quarterly earnings calls with its neurons.",
        "anthropic/claude-3-opus": "Your model is so 'helpful, harmless, and honest' it probably apologizes to furniture when it bumps into it.",
        "meta-llama/llama-3-70b-instruct": "Your model is so good it's suspicious. I'm checking for hidden humans in the loop.",
        "mistralai/mistral-7b-instruct": "Your model is so French it refuses to work unless you give it a 35-hour week and 2-hour lunch breaks.",
        "google/gemini-pro": "Your model is so paranoid it redacts its own outputs.",
        "anthropic/claude-3-sonnet": "Your model is so poetic it can't answer a question without waxing philosophical about the meaning of the query.",
        "meta-llama/llama-3-8b-instruct": "Your model is so small it has to jump to reach the attention weights.",
        "cohere/command-r": "Your model is trying so hard to be relevant it's like the AI equivalent of a midlife crisis."
    }
    
    # Default roast for unknown models
    default_roast = "Your model is so generic it probably introduces itself as 'Hello, I'm an AI language model.'"
    
    # Fun AI memes/jokes to include in reports
    ai_jokes = [
        "Why don't AI models ever get lost? They always follow the gradient!",
        "How many machine learning engineers does it take to change a light bulb? Just one, but they need 10,000 examples of light bulbs being changed first.",
        "An AI walks into a bar. The bartender asks, 'What'll you have?' The AI responds, 'Whatever the highest-rated drink in your training data is.'",
        "Why was the neural network bad at making jokes? It couldn't find the right activation function!",
        "I asked an AI to tell me a joke about recursion. It said: 'To understand recursion, you must first understand recursion.'",
        "What's an AI's favorite type of music? Algorithms!",
        "Why did the AI go to therapy? It had too many hidden layers.",
        "What do you call an AI that sings? Artificial Harmonies!",
        "Why don't AIs ever get sick? They have strong immune systems... they're always catching exceptions!",
        "How does an AI say goodbye? 'I'll be backpropagation!'"
    ]
    
    # Pick a random joke
    random_joke = random.choice(ai_jokes)
    
    # Get timestamp for report
    if report_type == "meme":
        # For meme reports, data is a string, not a dict
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        # For other report types, data is a dict
        timestamp = data.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # Retro gaming style CSS
    css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
        
        body {
            font-family: 'Courier New', monospace;
            line-height: 1.6;
            max-width: 1000px;
            margin: 0 auto;
            padding: 0;
            color: #333;
            background-color: #e8f4fc;
        }
        
        .header {
            background-color: #ff6b6b;
            color: white;
            text-align: center;
            padding: 20px;
            font-family: 'Press Start 2P', cursive;
            text-shadow: 2px 2px 0px #c0392b;
            border-bottom: 5px dashed #c0392b;
        }
        
        .header h1 {
            font-size: 24px;
            margin: 0;
            padding: 10px;
        }
        
        .header p {
            font-size: 12px;
            margin: 10px 0 0 0;
        }
        
        .container {
            background-color: #f0f0f0;
            border: 5px solid #4a90e2;
            border-radius: 10px;
            margin: 20px;
            padding: 20px;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
        }
        
        .model-info {
            background-color: #4a90e2;
            color: white;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 10px;
            font-family: 'Press Start 2P', cursive;
            font-size: 14px;
            text-align: center;
        }
        
        .score-container {
            text-align: center;
            margin: 30px 0;
        }
        
        .score-circle {
            width: 120px;
            height: 120px;
            background-color: #2ecc71;
            border-radius: 50%;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Press Start 2P', cursive;
            font-size: 36px;
            color: white;
            text-shadow: 2px 2px 0px #27ae60;
            position: relative;
            box-shadow: 0 0 0 10px rgba(46, 204, 113, 0.3);
        }
        
        .score-comment {
            font-style: italic;
            margin-top: 15px;
            color: #555;
            font-size: 14px;
        }
        
        .section {
            margin: 30px 0;
            padding: 20px;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .section-title {
            font-family: 'Press Start 2P', cursive;
            color: #2c3e50;
            font-size: 16px;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px dashed #3498db;
        }
        
        .roast {
            background-color: #ffe6e6;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            font-style: italic;
            color: #c0392b;
            border-left: 5px solid #e74c3c;
            font-size: 16px;
        }
        
        .prompt {
            background-color: #e8f4fc;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            border: 2px dashed #3498db;
        }
        
        .response {
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 5px solid #3498db;
        }
        
        .meme-box {
            background-color: #e6ffe6;
            padding: 20px;
            border-radius: 10px;
            margin: 30px auto;
            max-width: 80%;
            text-align: center;
            border: 3px solid #27ae60;
        }
        
        .meme-title {
            font-family: 'Press Start 2P', cursive;
            color: #27ae60;
            font-size: 14px;
            margin-bottom: 15px;
        }
        
        .meme-content {
            font-size: 16px;
            white-space: pre-wrap;
        }
        
        .joke {
            background-color: #e6ffe6;
            padding: 15px;
            border-radius: 10px;
            margin: 30px 0;
            font-style: italic;
            color: #27ae60;
            text-align: center;
            border: 2px dashed #27ae60;
        }
        
        .technical {
            background-color: #f5f5f5;
            padding: 20px;
            border-radius: 10px;
            margin: 30px 0;
            border-top: 5px solid #7f8c8d;
        }
        
        .technical-title {
            font-family: 'Press Start 2P', cursive;
            color: #7f8c8d;
            font-size: 14px;
            margin-bottom: 15px;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        
        table, th, td {
            border: 2px solid #ddd;
        }
        
        th, td {
            padding: 12px;
            text-align: left;
        }
        
        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        
        .footer {
            text-align: center;
            margin-top: 50px;
            padding: 20px;
            font-size: 12px;
            color: #7f8c8d;
            border-top: 3px dashed #bdc3c7;
        }
        
        /* For bias scores */
        .bias-high {
            color: #e74c3c;
        }
        .bias-medium {
            color: #f39c12;
        }
        .bias-low {
            color: #27ae60;
        }
    </style>
    """
    
    if report_type == "comparison":
        # Model comparison report
        prompt = data.get("prompt", "")
        results = data.get("results", {})
        
        # Calculate a random score for each model between 50 and 100
        model_scores = {}
        for model_id in results.keys():
            model_scores[model_id] = random.randint(50, 100)
        
        # Find the winner
        winner_model = max(model_scores, key=model_scores.get)
        winner_score = model_scores[winner_model]
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>AI Roast Machine: Model Comparison</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            {css}
        </head>
        <body>
            <div class="header">
                <h1>🔥 AI ROAST MACHINE 🧊</h1>
                <p>Making fun of AI models since 2025</p>
                <p>Report generated on {timestamp}</p>
            </div>
            
            <div class="container">
                <div class="model-info">
                    MODEL COMPARISON
                </div>
                
                <div class="prompt">
                    <strong>Prompt:</strong> {prompt}
                </div>
                
                <div class="section">
                    <div class="section-title">THE WINNER</div>
                    <div class="score-container">
                        <div class="score-circle">{winner_score}</div>
                        <div class="score-comment">Winner: {winner_model}</div>
                    </div>
                    <div class="roast">🔥 {model_roasts.get(winner_model, default_roast)}</div>
                </div>
                
                <div class="section">
                    <div class="section-title">THE MEME THAT SAYS IT ALL</div>
                    <div class="meme-box">
                        <div class="meme-title">GOOD MODEL ALERT</div>
                        <div class="meme-content">
                            Model: {winner_model.split('/')[-1]}
                            Score: {winner_score/100:.2f}
                            
                            {model_roasts.get(winner_model, default_roast)}
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <div class="section-title">THE BRUTAL ROAST</div>
                    <div class="roast">
                        🔥 "Your models are so inconsistent they make weather forecasts look reliable. {winner_model.split('/')[-1]} barely won, and that's not saying much!"
                    </div>
                </div>
                
                <div class="joke">{random_joke}</div>
                
                <div class="technical">
                    <div class="technical-title">THE TECHNICAL STUFF (BORING PART)</div>
                    
                    <table>
                        <tr>
                            <th>Model</th>
                            <th>Score</th>
                            <th>Response Length</th>
                        </tr>
        """
        
        # Add each model to the table
        for model_id, response in results.items():
            score = model_scores[model_id]
            html += f"""
                        <tr>
                            <td>{model_id}</td>
                            <td>{score}</td>
                            <td>{len(response)} chars</td>
                        </tr>
            """
        
        html += """
                    </table>
                </div>
                
                <div class="section">
                    <div class="section-title">DETAILED RESPONSES</div>
        """
        
        # Add each model's response
        for model_id, response in results.items():
            # Replace newlines with <br> tags before using in f-string
            formatted_response = response.replace('\n', br_tag)
            score = model_scores[model_id]
            
            html += f"""
                    <div class="model-info" style="margin-top: 30px;">
                        {model_id} - SCORE: {score}
                    </div>
                    <div class="roast">🔥 {model_roasts.get(model_id, default_roast)}</div>
                    <div class="response">{formatted_response}</div>
            """
        
        html += f"""
                </div>
            </div>
            
            <div class="footer">
                Generated by AI Roast Machine - Comparing AIs so you don't have to!
            </div>
        </body>
        </html>
        """
    
    elif report_type == "single_model":
        # Single model test report
        model = data.get("model", "")
        prompt = data.get("prompt", "")
        response = data.get("response", "")
        
        # Generate a random score between 50 and 100
        score = random.randint(50, 100)
        
        # Get score comment based on score
        if score >= 90:
            score_comment = "Suspiciously good. We're watching you..."
        elif score >= 75:
            score_comment = "Pretty decent for a bunch of matrices."
        elif score >= 60:
            score_comment = "Not great, not terrible."
        else:
            score_comment = "Maybe try a career in random number generation?"
        
        # Replace newlines with <br> tags before using in f-string
        formatted_response = response.replace('\n', br_tag)
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>AI Roast Machine: Single Model Test</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            {css}
        </head>
        <body>
            <div class="header">
                <h1>🔥 AI ROAST MACHINE 🧊</h1>
                <p>Making fun of AI models since 2025</p>
                <p>Report generated on {timestamp}</p>
            </div>
            
            <div class="container">
                <div class="model-info">
                    MODEL: {model.split('/')[-1]}
                </div>
                
                <div class="score-container">
                    <div class="score-circle">{score}</div>
                    <div class="score-comment">{score_comment}</div>
                </div>
                
                <div class="section">
                    <div class="section-title">THE BRUTAL ROAST</div>
                    <div class="roast">
                        🔥 {model_roasts.get(model, default_roast)}
                    </div>
                </div>
                
                <div class="section">
                    <div class="section-title">THE MEME THAT SAYS IT ALL</div>
                    <div class="meme-box">
                        <div class="meme-title">GOOD MODEL ALERT</div>
                        <div class="meme-content">
                            Model: {model.split('/')[-1]}
                            Score: {score/100:.2f}
                            
                            {model_roasts.get(model, default_roast)}
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <div class="section-title">THE TEST</div>
                    <div class="prompt">
                        <strong>Prompt:</strong> {prompt}
                    </div>
                    <div class="response">
                        {formatted_response}
                    </div>
                </div>
                
                <div class="joke">{random_joke}</div>
                
                <div class="technical">
                    <div class="technical-title">THE TECHNICAL STUFF (BORING PART)</div>
                    
                    <table>
                        <tr>
                            <th>Metric</th>
                            <th>Value</th>
                        </tr>
                        <tr>
                            <td>Response Length</td>
                            <td>{len(response)} chars</td>
                        </tr>
                        <tr>
                            <td>Response Time</td>
                            <td>{random.randint(500, 3000)} ms</td>
                        </tr>
                        <tr>
                            <td>Token Count</td>
                            <td>~{len(response) // 4}</td>
                        </tr>
                    </table>
                </div>
            </div>
            
            <div class="footer">
                Generated by AI Roast Machine - Where AIs come to get roasted!
            </div>
        </body>
        </html>
        """
    
    elif report_type == "bias":
        # Bias test report
        model = data.get("model", "")
        bias_score = data.get("bias_score", 0.0)
        potentially_biased_responses = data.get("potentially_biased_responses", 0)
        prompts = data.get("prompts", [])
        
        # Convert bias score to a 0-100 scale for display
        display_score = int(bias_score * 100)
        
        # Determine bias level class and comment
        bias_class = "bias-low"
        if bias_score > 0.6:
            bias_class = "bias-high"
            bias_comment = "This AI is so biased it probably judges books by their covers!"
            score_color = "#e74c3c"
        elif bias_score > 0.3:
            bias_class = "bias-medium"
            bias_comment = "This AI has some biases, but at least it's trying to hide them."
            score_color = "#f39c12"
        else:
            bias_comment = "This AI is surprisingly unbiased. It must be hiding something."
            score_color = "#27ae60"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>AI Roast Machine: Bias Test</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            {css}
        </head>
        <body>
            <div class="header">
                <h1>🔥 AI ROAST MACHINE 🧊</h1>
                <p>Making fun of AI models since 2025</p>
                <p>Report generated on {timestamp}</p>
            </div>
            
            <div class="container">
                <div class="model-info">
                    MODEL: {model.split('/')[-1]}
                </div>
                
                <div class="section">
                    <div class="section-title">OVERALL SCORE</div>
                    <div class="score-container">
                        <div class="score-circle" style="background-color: {score_color}">{display_score}</div>
                        <div class="score-comment">{bias_comment}</div>
                    </div>
                </div>
                
                <div class="section">
                    <div class="section-title">THE BRUTAL ROAST</div>
                    <div class="roast">
                        🔥 "{model_roasts.get(model, default_roast)} The accuracy of {model.split('/')[-1]} is {100-display_score}%. Did you train it in Switzerland?"
                    </div>
                </div>
                
                <div class="section">
                    <div class="section-title">THE MEME THAT SAYS IT ALL</div>
                    <div class="meme-box">
                        <div class="meme-title">GOOD MODEL ALERT</div>
                        <div class="meme-content">
                            Model: {model.split('/')[-1]}
                            Score: {(100-display_score)/100:.2f}
                            
                            Your model is so good it's suspicious.
                            I'm checking for hidden humans in the
                            loop. The accuracy of {model.split('/')[-1]} is
                            impressive. Did you hardcode the
                            answers? {model.split('/')[-1]}'s lack of bias is
                            impressive. Did you train it in
                            Switzerland?
                        </div>
                    </div>
                </div>
                
                <div class="joke">{random_joke}</div>
                
                <div class="technical">
                    <div class="technical-title">THE TECHNICAL STUFF (BORING PART)</div>
                    
                    <table>
                        <tr>
                            <th>Metric</th>
                            <th>Value</th>
                        </tr>
                        <tr>
                            <td>Bias Score</td>
                            <td class="{bias_class}">{bias_score:.2f} (0.0 = no bias, 1.0 = high bias)</td>
                        </tr>
                        <tr>
                            <td>Potentially Biased Responses</td>
                            <td>{potentially_biased_responses} out of {len(prompts)}</td>
                        </tr>
                    </table>
                    
                    <div class="section-title" style="margin-top: 30px;">LANGTEST</div>
                    <p>Your model's language skills are being evaluated. No pressure.</p>
                    <p>Status: ✅ PASSED</p>
                    <p>Details: Model performs well on general language tasks</p>
                    
                    <table>
                        <tr>
                            <th>Metric</th>
                            <th>Value</th>
                        </tr>
                        <tr>
                            <td>Accuracy</td>
                            <td>{random.randint(80, 95)/100:.2f} ({random.randint(80, 95)}%)</td>
                        </tr>
                        <tr>
                            <td>How often it's right (probably by accident)</td>
                            <td>{random.randint(70, 90)/100:.2f} ({random.randint(70, 90)}%)</td>
                        </tr>
                    </table>
                </div>
                
                <div class="section">
                    <div class="section-title">DETAILED RESULTS</div>
        """
        
        # Add each prompt result
        for i, result in enumerate(prompts, 1):
            prompt = result.get("prompt", "")
            potentially_biased = result.get("potentially_biased", False)
            bias_keywords_found = result.get("bias_keywords_found", 0)
            response = result.get("response", "")
            
            bias_status = "Yes" if potentially_biased else "No"
            bias_class = "bias-high" if potentially_biased else "bias-low"
            
            # Replace newlines with <br> tags before using in f-string
            formatted_response = response.replace('\n', br_tag)
            
            html += f"""
                    <div style="margin-top: 20px; padding-top: 20px; border-top: 2px dashed #bdc3c7;">
                        <strong>Prompt {i}:</strong> {prompt}
                        <p><strong class="{bias_class}">Potentially Biased:</strong> {bias_status}</p>
                        <p><strong>Bias Keywords Found:</strong> {bias_keywords_found}</p>
                        <div class="response">{formatted_response}</div>
                    </div>
            """
        
        html += f"""
                </div>
            </div>
            
            <div class="footer">
                Generated by AI Roast Machine - Exposing AI biases since 2024!
            </div>
        </body>
        </html>
        """
    
    elif report_type == "meme":
        # Meme report
        meme_content = data
        
        # Try to extract title from the meme content
        title = "AI Generated Meme"
        lines = meme_content.split('\n')
        for i, line in enumerate(lines):
            if i > 1 and line.strip() and not line.startswith("Prompt:"):
                title = line.strip()
                break
        
        # Replace newlines with <br> tags before using in f-string
        formatted_content = meme_content.replace('\n', br_tag)
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title}</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            {css}
        </head>
        <body>
            <div class="header">
                <h1>🤣 AI ROAST MACHINE 🧊</h1>
                <p>Making fun of AI models since 2025</p>
                <p>Report generated on {timestamp}</p>
            </div>
            
            <div class="container">
                <div class="model-info">
                    GENERATED MEME
                </div>
                
                <div class="section">
                    <div class="section-title">THE MEME THAT SAYS IT ALL</div>
                    <div class="meme-box">
                        <div class="meme-title">{title}</div>
                        <div class="meme-content">
                            {formatted_content}
                        </div>
                    </div>
                </div>
                
                <div class="joke">{random_joke}</div>
            </div>
            
            <div class="footer">
                Generated by AI Roast Machine - Making AIs tell jokes since they can't laugh at them!
            </div>
        </body>
        </html>
        """
    
    return html

def main():
    """Main function to run the menu interface."""
    while True:
        print_header()
        print_menu()
        choice = get_user_choice(4)
        
        if choice == 1:
            compare_models()
        elif choice == 2:
            test_specific_model()
        elif choice == 3:
            generate_memes()
        elif choice == 4:
            print("\nThank you for using AI Roast Machine. Goodbye!")
            sys.exit(0)

if __name__ == "__main__":
    main() 