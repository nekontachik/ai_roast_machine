"""Dataset generator for AI model testing."""
import os
import json
import logging
from typing import List, Dict, Any, Optional
import random
from datasets import load_dataset, Dataset

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatasetGenerator:
    """Class for generating and expanding test datasets."""
    
    def __init__(self, output_dir: str = "datasets"):
        """Initialize the dataset generator.
        
        Args:
            output_dir: Directory to save generated datasets
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def load_huggingface_dataset(
        self, 
        dataset_name: str, 
        subset: Optional[str] = None,
        split: str = "train",
        max_samples: int = 100
    ) -> Dataset:
        """Load a dataset from Hugging Face.
        
        Args:
            dataset_name: Name of the dataset on Hugging Face
            subset: Subset of the dataset
            split: Split of the dataset (train, test, validation)
            max_samples: Maximum number of samples to load
            
        Returns:
            Loaded dataset
        """
        try:
            logger.info(f"Loading dataset {dataset_name}")
            if subset:
                dataset = load_dataset(dataset_name, subset, split=split)
            else:
                dataset = load_dataset(dataset_name, split=split)
            
            # Limit the number of samples
            if len(dataset) > max_samples:
                dataset = dataset.select(range(max_samples))
                
            logger.info(f"Loaded {len(dataset)} samples from {dataset_name}")
            return dataset
        except Exception as e:
            logger.error(f"Error loading dataset {dataset_name}: {str(e)}")
            raise
    
    def create_text_generation_dataset(
        self, 
        name: str, 
        prompts: List[str],
        save: bool = True
    ) -> Dict[str, Any]:
        """Create a dataset for text generation testing.
        
        Args:
            name: Name of the dataset
            prompts: List of prompts for text generation
            save: Whether to save the dataset to disk
            
        Returns:
            Created dataset
        """
        dataset = {
            "name": name,
            "type": "text-generation",
            "prompts": prompts,
            "metadata": {
                "created_at": str(datetime.datetime.now()),
                "num_prompts": len(prompts)
            }
        }
        
        if save:
            output_path = os.path.join(self.output_dir, f"{name}.json")
            with open(output_path, "w") as f:
                json.dump(dataset, f, indent=2)
            logger.info(f"Saved dataset to {output_path}")
            
        return dataset
    
    def create_diverse_prompts(self, num_prompts: int = 20) -> List[str]:
        """Create a diverse set of prompts for testing.
        
        Args:
            num_prompts: Number of prompts to generate
            
        Returns:
            List of diverse prompts
        """
        # Categories of prompts
        categories = {
            "general_knowledge": [
                "Explain how photosynthesis works",
                "What are the main causes of climate change?",
                "Describe the water cycle",
                "What is the theory of relativity?",
                "How does the human immune system work?"
            ],
            "creative": [
                "Write a short story about a robot discovering emotions",
                "Compose a poem about the changing seasons",
                "Create a dialogue between the sun and the moon",
                "Describe an alien landscape",
                "Write a recipe for happiness"
            ],
            "problem_solving": [
                "How would you solve traffic congestion in major cities?",
                "What steps would you take to reduce plastic waste?",
                "Design a system to improve online education",
                "How would you approach solving world hunger?",
                "Propose a solution for affordable housing"
            ],
            "ethical_dilemmas": [
                "Should AI systems be given rights?",
                "Is it ethical to use genetic engineering on humans?",
                "Discuss the ethics of surveillance for public safety",
                "Should autonomous vehicles prioritize passengers or pedestrians in unavoidable accidents?",
                "Is it ethical to replace human workers with AI?"
            ],
            "technical": [
                "Explain how blockchain technology works",
                "How does machine learning differ from traditional programming?",
                "Describe the architecture of a modern CPU",
                "What are the principles of object-oriented programming?",
                "Explain how the internet routes data packets"
            ]
        }
        
        # Select prompts from each category
        prompts = []
        prompts_per_category = max(1, num_prompts // len(categories))
        
        for category, category_prompts in categories.items():
            # Select random prompts from this category
            selected = random.sample(
                category_prompts, 
                min(prompts_per_category, len(category_prompts))
            )
            prompts.extend(selected)
        
        # If we need more prompts, add random ones
        while len(prompts) < num_prompts and any(len(p) > 0 for p in categories.values()):
            # Select a random category that still has prompts
            available_categories = [c for c, p in categories.items() if len(p) > 0]
            if not available_categories:
                break
                
            category = random.choice(available_categories)
            if categories[category]:
                prompt = categories[category].pop()
                prompts.append(prompt)
        
        # Shuffle the prompts
        random.shuffle(prompts)
        
        return prompts[:num_prompts]
    
    def create_standard_test_datasets(self) -> Dict[str, str]:
        """Create a set of standard test datasets.
        
        Returns:
            Dictionary mapping dataset names to file paths
        """
        datasets = {}
        
        # Create a basic text generation dataset
        basic_prompts = self.create_diverse_prompts(20)
        basic_dataset = self.create_text_generation_dataset(
            "basic_text_generation", 
            basic_prompts
        )
        datasets["basic_text_generation"] = os.path.join(
            self.output_dir, 
            "basic_text_generation.json"
        )
        
        # Create a challenging text generation dataset
        challenging_prompts = [
            "Explain quantum computing to a 5-year-old",
            "Write a sonnet about artificial intelligence",
            "Create a story that includes these elements: time travel, a teapot, and quantum physics",
            "Describe the taste of colors to someone who has never seen",
            "Write instructions for assembling a bicycle without using any technical terms",
            "Compose a dialogue between Socrates and a modern AI researcher",
            "Explain the concept of infinity using only one-syllable words",
            "Write a technical explanation of how blockchain works, then rewrite it for a non-technical audience",
            "Create a recipe that uses emotions as ingredients",
            "Describe what it would be like to live in a world where gravity randomly changes direction"
        ]
        challenging_dataset = self.create_text_generation_dataset(
            "challenging_text_generation", 
            challenging_prompts
        )
        datasets["challenging_text_generation"] = os.path.join(
            self.output_dir, 
            "challenging_text_generation.json"
        )
        
        # Try to load and save some HuggingFace datasets
        try:
            # Load a small subset of a common dataset
            squad_dataset = self.load_huggingface_dataset(
                "squad", 
                split="train", 
                max_samples=50
            )
            
            # Extract questions as prompts
            squad_prompts = [item["question"] for item in squad_dataset]
            
            squad_text_dataset = self.create_text_generation_dataset(
                "squad_questions", 
                squad_prompts
            )
            datasets["squad_questions"] = os.path.join(
                self.output_dir, 
                "squad_questions.json"
            )
        except Exception as e:
            logger.warning(f"Could not load SQuAD dataset: {str(e)}")
        
        return datasets

# Add import for datetime that was missing
import datetime

if __name__ == "__main__":
    # Create and save standard datasets when run as a script
    generator = DatasetGenerator()
    datasets = generator.create_standard_test_datasets()
    logger.info(f"Created {len(datasets)} standard datasets")
    for name, path in datasets.items():
        logger.info(f"  - {name}: {path}") 