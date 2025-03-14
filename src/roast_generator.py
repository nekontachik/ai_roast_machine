"""Module for generating humorous roasts of AI models based on test results."""
import logging
import random
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class RoastGenerator:
    """Generates humorous roasts for AI models based on test results."""

    def __init__(self):
        """Initialize the roast generator with templates."""
        self.templates = {
            "low_score": [
                "This model is so bad, even ELIZA would laugh at it.",
                "Your model is like a fortune cookie: generic, predictable, and leaves you wanting more.",
                "If this model were a chef, it would burn water.",
                "This model has the intelligence of a rock, but that's insulting to geology.",
                "Your model is so biased, it thinks 'objective' is just a camera lens.",
            ],
            "medium_score": [
                "Your model is like a C student - doing just enough to pass, but nothing to write home about.",
                "This model is the AI equivalent of elevator music - functional but forgettable.",
                "Not terrible, not great. The Honda Civic of language models.",
                "Your model is like a microwave dinner - gets the job done, but nobody's impressed.",
                "This model has potential, like a child prodigy who decided video games were more interesting.",
            ],
            "high_score": [
                "Your model is surprisingly good. Did you accidentally train on the test set?",
                "Not bad, but let's be honest - it's still no match for a caffeinated human.",
                "I'd compliment your model, but I don't want it to get overconfident and take my job.",
                "Your model is like that one friend who's good at everything. Nobody likes that friend.",
                "Impressive! Though a broken clock is right twice a day too.",
            ],
        }
        
        self.metric_roasts = {
            "accuracy": {
                "low": "This model's accuracy is so low, it couldn't hit water if it fell out of a boat.",
                "medium": "The accuracy is decent, like a weather forecast - right enough to be useful, wrong enough to be annoying.",
                "high": "Impressive accuracy! Did you just make a glorified lookup table?",
            },
            "robustness": {
                "low": "This model is about as robust as a house of cards in a hurricane.",
                "medium": "Your model's robustness is like a Nokia 3310 with a cracked screen - tough but flawed.",
                "high": "Your model is surprisingly robust. It's like a cockroach - it'll probably survive the apocalypse.",
            },
            "bias": {
                "low": "Your model is so biased it should run for political office.",
                "medium": "The bias in this model is like that uncle at Thanksgiving - problematic but manageable.",
                "high": "Wow, your model is actually fair and balanced. Are you sure it's working correctly?",
            },
        }

    def generate_roast(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a humorous roast based on test results.

        Args:
            test_results: Dictionary containing test results

        Returns:
            Dictionary containing the roast
        """
        logger.info("Generating roast for model")
        
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
        overall_roast = random.choice(self.templates[score_category])
        
        # Generate metric-specific roasts
        metric_roasts = []
        for test in test_results.get("tests", []):
            test_name = test.get("test_name", "")
            metrics = test.get("metrics", {})
            
            for metric_name, metric_value in metrics.items():
                if metric_name in self.metric_roasts:
                    if isinstance(metric_value, (int, float)):
                        if metric_name == "bias":  # For bias, lower is better
                            level = "high" if metric_value < 0.3 else "medium" if metric_value < 0.6 else "low"
                        else:  # For other metrics, higher is better
                            level = "high" if metric_value > 0.7 else "medium" if metric_value > 0.4 else "low"
                        
                        if metric_name in self.metric_roasts and level in self.metric_roasts[metric_name]:
                            metric_roasts.append(self.metric_roasts[metric_name][level])
        
        # Combine roasts
        roast = {
            "model_name": model_name,
            "overall_score": overall_score,
            "overall_roast": overall_roast,
            "metric_roasts": metric_roasts,
            "combined_roast": f"{overall_roast} {random.choice(metric_roasts) if metric_roasts else ''}"
        }
        
        return roast


def generate_model_roast(test_results: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a roast for a model based on test results.

    Args:
        test_results: Dictionary containing test results

    Returns:
        Dictionary containing the roast
    """
    roaster = RoastGenerator()
    return roaster.generate_roast(test_results)
