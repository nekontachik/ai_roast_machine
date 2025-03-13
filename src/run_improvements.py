#!/usr/bin/env python
"""Script to run all improvements for the AI Roast Machine."""
import os
import logging
import argparse
import json
import sys
from typing import Dict, Any, List, Optional

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our modules
from src.mock_tester import MockTester
from src.dataset_generator import DatasetGenerator
try:
    from src.huggingface_tester import HuggingFaceTester
    HUGGINGFACE_AVAILABLE = True
except ImportError:
    HUGGINGFACE_AVAILABLE = False

# Check if we should use real models
USE_REAL_MODELS = os.environ.get("USE_REAL_MODELS", "false").lower() == "true"
MODEL_DEVICE = os.environ.get("MODEL_DEVICE", "cpu")

# Configure logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/improvements.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

logger.info(f"USE_REAL_MODELS: {USE_REAL_MODELS}")
logger.info(f"MODEL_DEVICE: {MODEL_DEVICE}")
logger.info(f"HUGGINGFACE_AVAILABLE: {HUGGINGFACE_AVAILABLE}")

def setup_directories() -> None:
    """Create necessary directories."""
    dirs = ["logs", "datasets", "test_results", "memes"]
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Created directory: {directory}")

def generate_datasets(args: argparse.Namespace) -> Dict[str, str]:
    """Generate test datasets.
    
    Args:
        args: Command line arguments
        
    Returns:
        Dictionary mapping dataset names to file paths
    """
    logger.info("Generating datasets...")
    generator = DatasetGenerator(output_dir="datasets")
    
    if args.custom_prompts:
        # Generate dataset from custom prompts file
        try:
            with open(args.custom_prompts, "r") as f:
                prompts = [line.strip() for line in f if line.strip()]
            
            dataset_name = os.path.splitext(os.path.basename(args.custom_prompts))[0]
            dataset = generator.create_text_generation_dataset(
                dataset_name, 
                prompts
            )
            logger.info(f"Created custom dataset {dataset_name} with {len(prompts)} prompts")
            return {dataset_name: os.path.join("datasets", f"{dataset_name}.json")}
        except Exception as e:
            logger.error(f"Error creating custom dataset: {str(e)}")
            return {}
    else:
        # Generate standard datasets
        datasets = generator.create_standard_test_datasets()
        logger.info(f"Created {len(datasets)} standard datasets")
        return datasets

def test_models(args: argparse.Namespace, datasets: Dict[str, str]) -> Dict[str, Dict[str, Any]]:
    """Test models with the generated datasets.
    
    Args:
        args: Command line arguments
        datasets: Dictionary mapping dataset names to file paths
        
    Returns:
        Dictionary mapping model names to test results
    """
    logger.info("Testing models...")
    results: Dict[str, Dict[str, Any]] = {}
    
    # Get models to test
    models = args.models.split(",") if args.models else ["gpt2", "distilgpt2"]
    
    for model_name in models:
        logger.info(f"Testing model: {model_name}")
        try:
            # Determine which tester to use
            if USE_REAL_MODELS and HUGGINGFACE_AVAILABLE and not model_name.startswith("mock-"):
                logger.info(f"Using HuggingFaceTester for model {model_name}")
                tester = HuggingFaceTester(model_name, device=MODEL_DEVICE)
            else:
                logger.info(f"Using MockTester for model {model_name}")
                tester = MockTester(model_name)
            
            # Test with each dataset
            for dataset_name, dataset_path in datasets.items():
                logger.info(f"Testing {model_name} with dataset {dataset_name}")
                
                # Load dataset
                with open(dataset_path, "r") as f:
                    dataset = json.load(f)
                
                # Test with prompts from dataset
                prompts = dataset.get("prompts", [])
                if prompts:
                    tester.test_generation(prompts[:args.max_samples])
                
                # Calculate metrics
                model_results = tester.calculate_metrics()
                
                # Save results
                results_path = f"test_results/{model_name}_{dataset_name}_results.json"
                with open(results_path, "w") as f:
                    json.dump(model_results, f, indent=2)
                
                logger.info(f"Saved results to {results_path}")
                
                # Store results
                if model_name not in results:
                    results[model_name] = {}
                results[model_name][dataset_name] = model_results
                
        except Exception as e:
            logger.error(f"Error testing model {model_name}: {str(e)}")
    
    return results

def generate_roasts_and_memes(results: Dict[str, Dict[str, Any]]) -> None:
    """Generate roasts and memes for test results.
    
    Args:
        results: Dictionary mapping model names to test results
    """
    logger.info("Generating roasts and memes...")
    
    # Import API functions
    from src.api import generate_roast, generate_meme
    import asyncio
    
    # Create synchronous wrapper functions
    def sync_generate_roast(request):
        """Synchronous wrapper for generate_roast."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(generate_roast(request))
        loop.close()
        return result
    
    def sync_generate_meme(request):
        """Synchronous wrapper for generate_meme."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(generate_meme(request))
        loop.close()
        return result
    
    for model_name, model_results in results.items():
        for dataset_name, result in model_results.items():
            try:
                # Create request object
                class RoastRequest:
                    def __init__(self, test_results):
                        self.test_results = test_results
                
                request = RoastRequest(result)
                
                # Generate roast
                roast_result = sync_generate_roast(request)
                logger.info(f"Generated roast for {model_name} on {dataset_name}")
                
                # Generate meme
                meme_result = sync_generate_meme(request)
                logger.info(f"Generated meme for {model_name} on {dataset_name}: {meme_result['meme_path']}")
                
            except Exception as e:
                logger.error(f"Error generating roast/meme for {model_name} on {dataset_name}: {str(e)}")

def main() -> None:
    """Main function."""
    parser = argparse.ArgumentParser(description="Run improvements for AI Roast Machine")
    parser.add_argument("--models", type=str, help="Comma-separated list of models to test")
    parser.add_argument("--custom-prompts", type=str, help="Path to file with custom prompts")
    parser.add_argument("--max-samples", type=int, default=10, help="Maximum number of samples to test")
    parser.add_argument("--skip-datasets", action="store_true", help="Skip dataset generation")
    parser.add_argument("--skip-testing", action="store_true", help="Skip model testing")
    parser.add_argument("--skip-roasts", action="store_true", help="Skip roast and meme generation")
    
    args = parser.parse_args()
    
    # Setup directories
    setup_directories()
    
    # Generate datasets
    datasets = {}
    if not args.skip_datasets:
        datasets = generate_datasets(args)
    else:
        # Load existing datasets
        if os.path.exists("datasets"):
            for filename in os.listdir("datasets"):
                if filename.endswith(".json"):
                    dataset_name = os.path.splitext(filename)[0]
                    datasets[dataset_name] = os.path.join("datasets", filename)
    
    # Test models
    results = {}
    if not args.skip_testing and datasets:
        results = test_models(args, datasets)
    else:
        # Load existing results
        if os.path.exists("test_results"):
            for filename in os.listdir("test_results"):
                if filename.endswith("_results.json"):
                    parts = os.path.splitext(filename)[0].split("_")
                    if len(parts) >= 3:
                        model_name = parts[0]
                        dataset_name = "_".join(parts[1:-1])
                        
                        with open(os.path.join("test_results", filename), "r") as f:
                            result = json.load(f)
                        
                        if model_name not in results:
                            results[model_name] = {}
                        results[model_name][dataset_name] = result
    
    # Generate roasts and memes
    if not args.skip_roasts and results:
        generate_roasts_and_memes(results)
    
    logger.info("All improvements completed successfully!")

if __name__ == "__main__":
    main() 