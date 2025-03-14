"""Module for generating memes based on AI model test results."""
import logging
import os
import random
from typing import Dict, Any, Optional, List, Tuple
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)


class MemeGenerator:
    """Generates memes for AI models based on test results."""

    def __init__(self, templates_dir: str = "templates"):
        """Initialize the meme generator.

        Args:
            templates_dir: Directory containing meme templates
        """
        self.templates_dir = templates_dir
        self.default_font = None
        self.meme_templates = {
            "low_score": [
                {"text_top": "I ASKED FOR GPT-4", "text_bottom": "BUT GOT A MAGIC 8-BALL"},
                {"text_top": "YOUR MODEL", "text_bottom": "STILL LOADING..."},
                {"text_top": "THEY SAID AI WOULD TAKE OUR JOBS", "text_bottom": "THIS ONE'S SAFE"},
            ],
            "medium_score": [
                {"text_top": "NOT GREAT", "text_bottom": "NOT TERRIBLE"},
                {"text_top": "WHEN YOUR MODEL WORKS", "text_bottom": "BUT ONLY SOMETIMES"},
                {"text_top": "GOOD ENOUGH", "text_bottom": "FOR GOVERNMENT WORK"},
            ],
            "high_score": [
                {"text_top": "IMPRESSIVE MODEL", "text_bottom": "STILL CAN'T EXPLAIN ITS REASONING"},
                {"text_top": "WHEN YOUR MODEL ACES THE TEST", "text_bottom": "BUT FAILS IN PRODUCTION"},
                {"text_top": "GREAT PERFORMANCE", "text_bottom": "SUSPICIOUSLY GREAT..."},
            ],
        }
        
        # Try to load a default font
        try:
            # This is a placeholder - in a real implementation, you'd include fonts
            self.default_font = ImageFont.load_default()
        except Exception as e:
            logger.warning(f"Could not load default font: {str(e)}")

    def _create_blank_meme(self, width: int = 800, height: int = 600, 
                          color: Tuple[int, int, int] = (255, 255, 255)) -> Image.Image:
        """Create a blank meme template.

        Args:
            width: Width of the image
            height: Height of the image
            color: Background color (RGB)

        Returns:
            PIL Image object
        """
        return Image.new("RGB", (width, height), color)

    def _add_text_to_image(self, image: Image.Image, text_top: str, text_bottom: str) -> Image.Image:
        """Add text to the top and bottom of an image.

        Args:
            image: PIL Image object
            text_top: Text to add to the top
            text_bottom: Text to add to the bottom

        Returns:
            PIL Image with text added
        """
        if not self.default_font:
            logger.warning("No font available, cannot add text to image")
            return image
            
        draw = ImageDraw.Draw(image)
        width, height = image.size
        
        # Add top text
        draw.text((width/2, height*0.1), text_top.upper(), 
                 fill=(0, 0, 0), font=self.default_font, anchor="mm")
        
        # Add bottom text
        draw.text((width/2, height*0.9), text_bottom.upper(), 
                 fill=(0, 0, 0), font=self.default_font, anchor="mm")
        
        return image

    def generate_meme(self, test_results: Dict[str, Any], 
                     output_path: str = "meme.png") -> str:
        """Generate a meme based on test results.

        Args:
            test_results: Dictionary containing test results
            output_path: Path to save the meme

        Returns:
            Path to the saved meme
        """
        logger.info("Generating meme for model")
        
        overall_score = test_results.get("overall_score", 0.0)
        model_name = test_results.get("model_name", "Unknown Model")
        
        # Determine score category
        if overall_score < 0.4:
            score_category = "low_score"
        elif overall_score < 0.7:
            score_category = "medium_score"
        else:
            score_category = "high_score"
        
        # Select a random template
        template = random.choice(self.meme_templates[score_category])
        
        # Create a blank meme (in a real implementation, you'd load a template image)
        meme_image = self._create_blank_meme()
        
        # Add text
        meme_image = self._add_text_to_image(
            meme_image, 
            template["text_top"], 
            template["text_bottom"]
        )
        
        # Save the meme
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
        meme_image.save(output_path)
        
        logger.info(f"Meme saved to {output_path}")
        return output_path


def generate_model_meme(test_results: Dict[str, Any], 
                       output_path: str = "meme.png") -> str:
    """Generate a meme for a model based on test results.

    Args:
        test_results: Dictionary containing test results
        output_path: Path to save the meme

    Returns:
        Path to the saved meme
    """
    generator = MemeGenerator()
    return generator.generate_meme(test_results, output_path)
