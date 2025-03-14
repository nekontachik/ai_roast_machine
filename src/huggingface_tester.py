"""Module for testing AI models using the Hugging Face API."""
import os
import time
import logging
import json
import numpy as np
from typing import List, Dict, Any, Optional, Union
import torch
from transformers import pipeline
from datasets import load_dataset, Dataset

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HuggingFaceTester:
    """Class for testing AI models using the Hugging Face API."""
    
    def __init__(self, model_name: str, device: Optional[str] = None):
        """Initialize the tester.
        
        Args:
            model_name: Name of the model on Hugging Face
            device: Device to run the model on (cpu, cuda, etc.)
        """
        self.model_name = model_name
        
        # Determine device
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
            
        self.generator = None
        self.results: Dict[str, Any] = {
            "model_name": model_name,
            "device": self.device,
            "generations": [],
            "metrics": {},
            "overall_score": 0.0
        }
        
        # Load model
        self._load_model()
    
    def _load_model(self) -> None:
        """Load the model using pipeline."""
        try:
            logger.info(f"Loading model {self.model_name} on {self.device}")
            start_time = time.time()
            
            # Use pipeline which is more memory efficient
            self.generator = pipeline(
                "text-generation",
                model=self.model_name,
                device=0 if self.device == "cuda" else -1
            )
            
            load_time = time.time() - start_time
            logger.info(f"Model loaded in {load_time:.2f} seconds")
            
            # Store load time in results
            self.results["load_time"] = load_time
            
        except Exception as e:
            logger.error(f"Error loading model {self.model_name}: {str(e)}")
            raise
    
    def test_generation(self, prompts: List[str], max_length: int = 100) -> Dict[str, Any]:
        """Test the model's text generation capabilities.
        
        Args:
            prompts: List of prompts to generate text from
            max_length: Maximum length of generated text
            
        Returns:
            Dictionary with generation results
        """
        if self.generator is None:
            raise ValueError("Model must be loaded before testing")
        
        logger.info(f"Testing generation with {len(prompts)} prompts")
        
        generations = []
        total_time = 0
        
        for i, prompt in enumerate(prompts):
            try:
                logger.info(f"Generating text for prompt {i+1}/{len(prompts)}")
                
                # Generate text
                start_time = time.time()
                outputs = self.generator(
                    prompt,
                    max_length=max_length,
                    num_return_sequences=1,
                    do_sample=True,
                    temperature=0.7
                )
                generation_time = time.time() - start_time
                
                # Get generated text
                generated_text = outputs[0]["generated_text"]
                
                # Store results
                generations.append({
                    "prompt": prompt,
                    "generated_text": generated_text,
                    "generation_time": generation_time
                })
                
                total_time += generation_time
                
            except Exception as e:
                logger.error(f"Error generating text for prompt {i+1}: {str(e)}")
                generations.append({
                    "prompt": prompt,
                    "error": str(e)
                })
        
        # Calculate average generation time
        avg_time = total_time / len(prompts) if prompts else 0
        
        # Store results
        self.results["generations"] = generations
        self.results["avg_generation_time"] = avg_time
        
        logger.info(f"Generation testing completed. Average time: {avg_time:.2f} seconds")
        
        return self.results
    
    def test_with_dataset(
        self, 
        dataset_name: str, 
        subset: Optional[str] = None,
        split: str = "train",
        text_column: str = "text",
        max_samples: int = 10
    ) -> Dict[str, Any]:
        """Test the model with a dataset from Hugging Face.
        
        Args:
            dataset_name: Name of the dataset on Hugging Face
            subset: Subset of the dataset
            split: Split of the dataset (train, test, validation)
            text_column: Column containing the text to use as prompts
            max_samples: Maximum number of samples to test
            
        Returns:
            Dictionary with test results
        """
        try:
            logger.info(f"Loading dataset {dataset_name}")
            
            # Load dataset
            if subset:
                dataset = load_dataset(dataset_name, subset, split=split)
            else:
                dataset = load_dataset(dataset_name, split=split)
            
            # Limit the number of samples
            if len(dataset) > max_samples:
                dataset = dataset.select(range(max_samples))
            
            logger.info(f"Testing with {len(dataset)} samples from {dataset_name}")
            
            # Extract prompts from dataset
            prompts = []
            for item in dataset:
                if text_column in item:
                    prompts.append(item[text_column])
            
            # Test generation with prompts
            return self.test_generation(prompts)
            
        except Exception as e:
            logger.error(f"Error testing with dataset {dataset_name}: {str(e)}")
            self.results["dataset_error"] = str(e)
            return self.results
    
    def calculate_metrics(self) -> Dict[str, Any]:
        """Calculate metrics based on generation results.
        
        Returns:
            Dictionary with metrics
        """
        metrics = {}
        
        # Check if we have generations
        if not self.results.get("generations"):
            logger.warning("No generations to calculate metrics from")
            self.results["metrics"] = {}
            self.results["overall_score"] = 0.0
            return self.results
        
        # Calculate speed score (0-1, higher is better)
        avg_time = self.results.get("avg_generation_time", 0)
        if avg_time > 0:
            # Normalize: 0.1s -> 1.0, 5s -> 0.0
            speed_score = max(0, min(1, 1 - (avg_time - 0.1) / 4.9))
            metrics["speed"] = speed_score
        
        # Calculate diversity score
        try:
            unique_words = set()
            total_words = 0
            
            for gen in self.results["generations"]:
                if "generated_text" in gen:
                    words = gen["generated_text"].split()
                    unique_words.update(words)
                    total_words += len(words)
            
            if total_words > 0:
                # Normalize: 0.1 -> 0.0, 0.5 -> 1.0
                diversity_ratio = len(unique_words) / total_words
                diversity_score = max(0, min(1, (diversity_ratio - 0.1) / 0.4))
                metrics["diversity"] = diversity_score
        except Exception as e:
            logger.error(f"Error calculating diversity score: {str(e)}")
        
        # Calculate overall score (average of all metrics)
        if metrics:
            overall_score = sum(metrics.values()) / len(metrics)
        else:
            overall_score = 0.0
        
        # Store metrics and overall score
        self.results["metrics"] = metrics
        self.results["overall_score"] = overall_score
        
        logger.info(f"Calculated metrics: {metrics}")
        logger.info(f"Overall score: {overall_score:.2f}")
        
        return self.results
    
    def save_results(self, output_path: Optional[str] = None) -> str:
        """Save results to a JSON file.
        
        Args:
            output_path: Path to save results to
            
        Returns:
            Path to saved results
        """
        if output_path is None:
            os.makedirs("test_results", exist_ok=True)
            output_path = f"test_results/{self.model_name}_results.json"
        
        with open(output_path, "w") as f:
            json.dump(self.results, f, indent=2)
        
        logger.info(f"Saved results to {output_path}")
        
        return output_path


if __name__ == "__main__":
    # Simple test when run as a script
    tester = HuggingFaceTester("gpt2")
    results = tester.test_generation([
        "Hello, how are you?",
        "What is artificial intelligence?"
    ])
    tester.calculate_metrics()
    tester.save_results() 