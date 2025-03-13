"""Mock tester for AI models."""
import os
import time
import logging
import json
import random
from typing import List, Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MockTester:
    """Mock class for testing AI models without actually loading them."""
    
    def __init__(self, model_name: str):
        """Initialize the mock tester.
        
        Args:
            model_name: Name of the model to simulate
        """
        self.model_name = model_name
        self.results: Dict[str, Any] = {
            "model_name": model_name,
            "device": "mock",
            "generations": [],
            "metrics": {},
            "overall_score": 0.0,
            "load_time": 0.5  # Simulate fast loading
        }
        
        logger.info(f"Initialized mock tester for {model_name}")
    
    def test_generation(self, prompts: List[str], max_length: int = 100) -> Dict[str, Any]:
        """Simulate testing the model's text generation capabilities.
        
        Args:
            prompts: List of prompts to generate text from
            max_length: Maximum length of generated text
            
        Returns:
            Dictionary with generation results
        """
        logger.info(f"Mock testing generation with {len(prompts)} prompts")
        
        generations = []
        total_time: float = 0.0
        
        # Responses for different types of prompts
        responses = {
            "hello": "Hello! How can I assist you today?",
            "what": "That's an interesting question. Let me think about it...",
            "explain": "Let me explain this concept in simple terms...",
            "write": "Here's a creative piece I've written for you...",
            "how": "Here are the steps to accomplish that task..."
        }
        
        for i, prompt in enumerate(prompts):
            try:
                logger.info(f"Generating mock text for prompt {i+1}/{len(prompts)}")
                
                # Simulate generation time
                generation_time = random.uniform(0.1, 1.0)
                time.sleep(0.1)  # Small actual delay for realism
                
                # Generate mock text based on prompt
                prompt_lower = prompt.lower()
                response_type = next((key for key in responses if key in prompt_lower), "default")
                
                if response_type == "default":
                    generated_text = f"{prompt} [Mock response: This is a simulated response from {self.model_name}]"
                else:
                    generated_text = f"{prompt}\n\n{responses[response_type]}"
                
                # Add some randomness to the length
                if random.random() > 0.5:
                    generated_text += " " + " ".join(["word"] * random.randint(10, 50))
                
                # Store results
                generations.append({
                    "prompt": prompt,
                    "generated_text": generated_text,
                    "generation_time": generation_time
                })
                
                total_time += generation_time
                
            except Exception as e:
                logger.error(f"Error in mock generation for prompt {i+1}: {str(e)}")
                generations.append({
                    "prompt": prompt,
                    "error": str(e)
                })
        
        # Calculate average generation time
        avg_time = total_time / len(prompts) if prompts else 0
        
        # Store results
        self.results["generations"] = generations
        self.results["avg_generation_time"] = avg_time
        
        logger.info(f"Mock generation completed. Average time: {avg_time:.2f} seconds")
        
        return self.results
    
    def test_with_dataset(
        self, 
        dataset_name: str, 
        subset: Optional[str] = None,
        split: str = "train",
        text_column: str = "text",
        max_samples: int = 10
    ) -> Dict[str, Any]:
        """Simulate testing with a dataset.
        
        Args:
            dataset_name: Name of the dataset
            subset: Subset of the dataset
            split: Split of the dataset
            text_column: Column containing the text
            max_samples: Maximum number of samples to test
            
        Returns:
            Dictionary with test results
        """
        logger.info(f"Mock testing with dataset {dataset_name}")
        
        # Generate mock prompts
        prompts = [
            f"Sample {i} from {dataset_name}" for i in range(max_samples)
        ]
        
        # Test with mock prompts
        return self.test_generation(prompts)
    
    def calculate_metrics(self) -> Dict[str, Any]:
        """Calculate mock metrics.
        
        Returns:
            Dictionary with metrics
        """
        logger.info("Calculating mock metrics")
        
        # Generate random metrics
        metrics = {
            "speed": random.uniform(0.6, 0.9),
            "diversity": random.uniform(0.5, 0.8),
            "coherence": random.uniform(0.7, 0.95)
        }
        
        # Calculate overall score
        overall_score = sum(metrics.values()) / len(metrics)
        
        # Store metrics and overall score
        self.results["metrics"] = metrics
        self.results["overall_score"] = overall_score
        
        logger.info(f"Mock metrics: {metrics}")
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
        
        logger.info(f"Saved mock results to {output_path}")
        
        return output_path


if __name__ == "__main__":
    # Test the mock tester
    tester = MockTester("gpt2-mock")
    results = tester.test_generation([
        "Hello, how are you?",
        "What is artificial intelligence?",
        "Explain quantum computing"
    ])
    tester.calculate_metrics()
    tester.save_results() 