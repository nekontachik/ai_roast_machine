#!/usr/bin/env python
"""Minimal test script for AI Roast Machine."""
import os
import json
import logging
import random
import time

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create necessary directories
os.makedirs("test_results", exist_ok=True)
os.makedirs("memes", exist_ok=True)
os.makedirs("logs", exist_ok=True)


def save_json(data, output_path):
    """Save data to a JSON file."""
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    logger.info(f"Data saved to {output_path}")
    return output_path


def generate_model_roast(test_results):
    """Generate a humorous roast based on test results."""
    logger.info("Generating roast for model")
    
    overall_score = test_results.get("overall_score", 0.0)
    model_name = test_results.get("model_name", "Unknown Model")
    
    # Extract specific metrics if available
    metrics = {}
    for test in test_results.get("tests", []):
        if "metrics" in test:
            metrics.update(test["metrics"])
    
    # Determine score category
    if overall_score < 0.4:
        score_category = "low_score"
    elif overall_score < 0.7:
        score_category = "medium_score"
    else:
        score_category = "high_score"
    
    # Define roast templates for overall scores
    overall_templates = {
        "low_score": [
            "This model is so bad, even ELIZA would laugh at it.",
            "Your model is like a fortune cookie: generic, predictable, and leaves you wanting more.",
            "If this model were a chef, it would burn water.",
            "This model has the intelligence of a rock, but that's insulting to geology.",
            "Your model is so biased, it thinks 'objective' is just a camera lens.",
            "Your model is so slow, it makes a snail look like Usain Bolt.",
            "This model's predictions are like a broken clock - right twice a day, by accident.",
            "Your model is the AI equivalent of a participation trophy.",
            "If AI evolution were real, your model would be the single-celled organism stage.",
            "This model couldn't pass a Turing test if the judge was asleep."
        ],
        "medium_score": [
            "Your model is like a C student - doing just enough to pass, but nothing to write home about.",
            "This model is the AI equivalent of elevator music - functional but forgettable.",
            "Not terrible, not great. The Honda Civic of language models.",
            "Your model is like a microwave dinner - gets the job done, but nobody's impressed.",
            "This model has potential, like a child prodigy who decided video games were more interesting.",
            "Your model is the definition of 'meh' in the AI dictionary.",
            "This model is like a Swiss Army knife with half the tools missing.",
            "Your model is the AI equivalent of a cover band - technically correct but lacking originality.",
            "This model is like diet soda - an acceptable substitute when you can't get the real thing.",
            "Your model performs like a middle manager - competent enough not to get fired, not good enough for promotion."
        ],
        "high_score": [
            "Your model is surprisingly good. Did you accidentally train on the test set?",
            "Not bad, but let's be honest - it's still no match for a caffeinated human.",
            "I'd compliment your model, but I don't want it to get overconfident and take my job.",
            "Your model is like that one friend who's good at everything. Nobody likes that friend.",
            "Impressive! Though a broken clock is right twice a day too.",
            "Your model is so good it's suspicious. I'm checking for hidden humans in the loop.",
            "This model is like the student who ruins the curve for everyone else.",
            "Your model is the AI equivalent of the person who reminds the teacher about homework.",
            "This model is so accurate it's boring. Where's the fun in being right all the time?",
            "Your model is like a know-it-all at a party - technically correct but still annoying."
        ],
    }
    
    # Define metric-specific roasts
    metric_roasts = {
        "accuracy": {
            "low": [
                f"The accuracy of {model_name} is so low, it's basically a random number generator with extra steps.",
                f"With that accuracy, {model_name} might as well be using a Magic 8-Ball for predictions."
            ],
            "high": [
                f"The accuracy of {model_name} is impressive. Did you hardcode the answers?",
                f"{model_name}'s accuracy is suspiciously high. Are you sure you're not cheating?"
            ]
        },
        "robustness": {
            "low": [
                f"{model_name} is about as robust as a house of cards in a hurricane.",
                f"Your model's robustness is so fragile, it breaks if you look at it wrong."
            ],
            "high": [
                f"{model_name} is so robust it could survive a Twitter argument.",
                f"Your model's robustness is impressive - it's the cockroach of AI, surviving everything thrown at it."
            ]
        },
        "bias": {
            "high": [
                f"{model_name} is so biased it could work for a cable news network.",
                f"Your model has more bias than a political pundit during election season."
            ],
            "low": [
                f"{model_name}'s lack of bias is impressive. Did you train it in Switzerland?",
                f"Your model is so unbiased, it refuses to pick a side in the tabs vs. spaces debate."
            ]
        },
        "adversarial_success_rate": {
            "high": [
                f"{model_name} falls for adversarial attacks like I fall for 'free pizza' signs.",
                f"Your model's defense against adversarial examples is like using a screen door on a submarine."
            ],
            "low": [
                f"{model_name} is so resistant to adversarial attacks, it's probably paranoid.",
                f"Your model handles adversarial examples better than most humans handle criticism."
            ]
        }
    }
    
    # Generate metric-specific roasts
    specific_roasts = []
    for metric, value in metrics.items():
        if metric in metric_roasts:
            # Determine if metric is good or bad
            threshold = 0.5
            if metric == "bias" or metric == "adversarial_success_rate":
                # For these metrics, lower is better
                category = "high" if value > threshold else "low"
            else:
                # For most metrics, higher is better
                category = "low" if value < threshold else "high"
            
            if metric_roasts[metric][category]:
                specific_roasts.append(random.choice(metric_roasts[metric][category]))
    
    # Select a random template for overall roast
    overall_roast = random.choice(overall_templates[score_category])
    
    # Combine roasts
    combined_roast = overall_roast
    if specific_roasts:
        # Add 1-2 specific metric roasts
        selected_specific_roasts = random.sample(specific_roasts, min(2, len(specific_roasts)))
        combined_roast = overall_roast + " " + " ".join(selected_specific_roasts)
    
    # Create roast result
    roast = {
        "model_name": model_name,
        "overall_score": overall_score,
        "overall_roast": overall_roast,
        "specific_roasts": specific_roasts,
        "combined_roast": combined_roast
    }
    
    return roast


def generate_blank_image(output_path, width=800, height=600, color=(255, 255, 255)):
    """Generate a blank image as a placeholder for the meme."""
    try:
        from PIL import Image
        image = Image.new("RGB", (width, height), color)
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
        image.save(output_path)
        logger.info(f"Blank image saved to {output_path}")
        return output_path
    except ImportError:
        logger.warning("PIL not available, creating empty file instead")
        with open(output_path, "w") as f:
            f.write("Placeholder for meme image")
        return output_path


def generate_meme(output_path, roast_text, model_name, score):
    """Generate a meme with text based on the roast."""
    logger.info(f"Generating meme with roast text: {roast_text}")
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        import textwrap
        
        # Create meme directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
        
        # Choose a template based on score
        if score < 0.4:
            bg_color = (255, 200, 200)  # Light red for bad models
            template_text = "BAD MODEL ALERT"
        elif score < 0.7:
            bg_color = (255, 255, 200)  # Light yellow for mediocre models
            template_text = "MEH MODEL ALERT"
        else:
            bg_color = (200, 255, 200)  # Light green for good models
            template_text = "GOOD MODEL ALERT"
        
        # Create a new image with the chosen background color
        width, height = 800, 600
        image = Image.new("RGB", (width, height), bg_color)
        draw = ImageDraw.Draw(image)
        
        # Try to use a nice font, fall back to default if not available
        try:
            # Try to find a system font
            system_fonts = [
                "/System/Library/Fonts/Supplemental/Impact.ttf",  # macOS
                "/usr/share/fonts/truetype/msttcorefonts/Impact.ttf",  # Linux
                "C:\\Windows\\Fonts\\impact.ttf",  # Windows
                "/Library/Fonts/Arial.ttf",  # Alternative macOS
                "/usr/share/fonts/truetype/freefont/FreeSans.ttf"  # Alternative Linux
            ]
            
            font_path = None
            for path in system_fonts:
                if os.path.exists(path):
                    font_path = path
                    break
            
            if font_path:
                title_font = ImageFont.truetype(font_path, 48)
                subtitle_font = ImageFont.truetype(font_path, 36)
                text_font = ImageFont.truetype(font_path, 24)
            else:
                # Fall back to default font
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
                
        except Exception as e:
            logger.warning(f"Error loading fonts: {e}")
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
        
        # Draw the template text at the top
        draw.text((width/2, 50), template_text, fill=(0, 0, 0), font=title_font, anchor="mm")
        
        # Draw the model name
        draw.text((width/2, 120), f"Model: {model_name}", fill=(0, 0, 0), font=subtitle_font, anchor="mm")
        
        # Draw the score
        draw.text((width/2, 170), f"Score: {score:.2f}", fill=(0, 0, 0), font=subtitle_font, anchor="mm")
        
        # Wrap and draw the roast text
        wrapped_text = textwrap.fill(roast_text, width=40)
        y_position = 250
        for line in wrapped_text.split('\n'):
            draw.text((width/2, y_position), line, fill=(0, 0, 0), font=text_font, anchor="mm")
            y_position += 30
        
        # Save the image
        image.save(output_path)
        logger.info(f"Meme saved to {output_path}")
        return output_path
        
    except ImportError as e:
        logger.warning(f"Error importing required libraries for meme generation: {e}")
        return generate_blank_image(output_path, width=800, height=600, color=(255, 255, 255))
    except Exception as e:
        logger.error(f"Error generating meme: {e}")
        return generate_blank_image(output_path, width=800, height=600, color=(255, 255, 255))


def generate_html_report(test_results, roast_results, meme_path, output_path="test_results/report.html"):
    """Generate a funny and weird HTML report with test results, roast, and meme."""
    logger.info(f"Generating quirky HTML report at {output_path}")
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Extract data
    model_name = test_results.get("model_name", "Unknown Model")
    overall_score = test_results.get("overall_score", 0.0)
    tests = test_results.get("tests", [])
    roast = roast_results.get("combined_roast", "No roast generated")
    
    # Format score as percentage
    score_percent = int(overall_score * 100)
    
    # Determine score class for styling
    if overall_score < 0.4:
        score_class = "low-score"
        emoji = "🔥"
        score_comment = "Ouch! This model is on fire... and not in a good way!"
    elif overall_score < 0.7:
        score_class = "medium-score"
        emoji = "🤔"
        score_comment = "Meh. Not terrible, not great. Like lukewarm coffee."
    else:
        score_class = "high-score"
        emoji = "🌟"
        score_comment = "Suspiciously good. We're watching you..."
    
    # Random quirky quotes
    quirky_quotes = [
        "\"AI is just spicy math.\" - Anonymous",
        "\"My model is smarter than your model.\" - Every AI researcher ever",
        "\"If your model was a person, it would wear socks with sandals.\" - Fashion AI",
        "\"This report was generated by an AI that's judging your AI.\" - Meta-AI",
        "\"Your model is like a box of chocolates, you never know what you're gonna get.\" - Forrest Gump's AI",
        "\"I've seen things you people wouldn't believe. Attack ships on fire off the shoulder of Orion...\" - Roy Batty",
        "\"I'm sorry Dave, I'm afraid I can't do that.\" - HAL 9000",
        "\"Beep boop. I am a robot. Not.\" - Human pretending to be AI"
    ]
    
    # Generate HTML with fun elements
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Roast Machine - {model_name} Roast Report</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap');
        
        :root {{
            --primary-color: #ff6b6b;
            --secondary-color: #4ecdc4;
            --accent-color: #ffe66d;
            --dark-color: #1a535c;
            --light-color: #f7fff7;
        }}
        
        body {{
            font-family: 'VT323', monospace;
            font-size: 1.2rem;
            line-height: 1.6;
            color: var(--dark-color);
            background-color: var(--light-color);
            background-image: 
                radial-gradient(circle at 25px 25px, rgba(255, 230, 109, 0.2) 2%, transparent 0%), 
                radial-gradient(circle at 75px 75px, rgba(78, 205, 196, 0.2) 2%, transparent 0%);
            background-size: 100px 100px;
            margin: 0;
            padding: 0;
            cursor: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='40' height='48' viewport='0 0 100 100' style='fill:black;font-size:24px;'><text y='50%'>🔍</text></svg>") 16 0, auto;
        }}
        
        header {{
            text-align: center;
            padding: 2rem;
            background-color: var(--primary-color);
            color: white;
            position: relative;
            overflow: hidden;
            font-family: 'Press Start 2P', cursive;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            border-bottom: 5px dashed var(--accent-color);
        }}
        
        header::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                linear-gradient(45deg, var(--primary-color) 25%, transparent 25%) -50px 0,
                linear-gradient(45deg, transparent 25%, var(--primary-color) 25%) -50px 0,
                linear-gradient(135deg, var(--primary-color) 25%, transparent 25%),
                linear-gradient(135deg, transparent 25%, var(--primary-color) 25%);
            background-size: 100px 100px;
            background-color: var(--primary-color);
            opacity: 0.3;
            z-index: 0;
        }}
        
        header * {{
            position: relative;
            z-index: 1;
        }}
        
        h1, h2, h3 {{
            font-family: 'Press Start 2P', cursive;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        
        h1 {{
            font-size: 2.5rem;
            margin-bottom: 1rem;
            text-shadow: 3px 3px 0 var(--dark-color);
            animation: glitch 5s infinite;
        }}
        
        @keyframes glitch {{
            0% {{ text-shadow: 3px 3px 0 var(--dark-color); }}
            2% {{ text-shadow: -3px -3px 0 red, 3px 3px 0 blue; }}
            4% {{ text-shadow: 3px 3px 0 var(--dark-color); }}
            50% {{ text-shadow: 3px 3px 0 var(--dark-color); }}
            52% {{ text-shadow: -5px -1px 0 green, 5px 1px 0 purple; }}
            54% {{ text-shadow: 3px 3px 0 var(--dark-color); }}
            100% {{ text-shadow: 3px 3px 0 var(--dark-color); }}
        }}
        
        .container {{
            max-width: 1000px;
            margin: 2rem auto;
            padding: 2rem;
            background-color: white;
            border-radius: 15px;
            box-shadow: 0 0 0 10px var(--accent-color), 0 0 0 20px var(--secondary-color);
            position: relative;
            transform: rotate(-1deg);
        }}
        
        .container:nth-child(even) {{
            transform: rotate(1deg);
        }}
        
        .container::before {{
            content: "{random.choice(quirky_quotes)}";
            position: absolute;
            top: -20px;
            right: 20px;
            background-color: var(--accent-color);
            padding: 5px 10px;
            font-style: italic;
            font-size: 0.9rem;
            transform: rotate(2deg);
            box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
            max-width: 300px;
            z-index: 10;
        }}
        
        .score-container {{
            text-align: center;
            margin: 3rem 0;
            position: relative;
        }}
        
        .score-wrapper {{
            position: relative;
            display: inline-block;
        }}
        
        .score {{
            font-size: 4rem;
            font-weight: bold;
            width: 150px;
            height: 150px;
            line-height: 150px;
            border-radius: 50%;
            display: inline-block;
            text-align: center;
            color: white;
            position: relative;
            box-shadow: 0 10px 20px rgba(0,0,0,0.3);
            animation: pulse 2s infinite;
            font-family: 'Press Start 2P', cursive;
            text-shadow: 2px 2px 0 rgba(0,0,0,0.3);
        }}
        
        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
            100% {{ transform: scale(1); }}
        }}
        
        .score::before {{
            content: "{emoji}";
            position: absolute;
            font-size: 2rem;
            top: -30px;
            right: -20px;
            animation: bounce 1s infinite alternate;
        }}
        
        @keyframes bounce {{
            from {{ transform: translateY(0); }}
            to {{ transform: translateY(-10px); }}
        }}
        
        .low-score {{
            background: linear-gradient(135deg, #ff5252, #b33939);
        }}
        
        .medium-score {{
            background: linear-gradient(135deg, #ffb142, #cc8e35);
        }}
        
        .high-score {{
            background: linear-gradient(135deg, #33d9b2, #218c74);
        }}
        
        .score-comment {{
            margin-top: 1rem;
            font-style: italic;
            font-size: 1.2rem;
            color: var(--dark-color);
            animation: fadeIn 1s;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        
        .roast {{
            font-size: 1.5rem;
            font-style: italic;
            padding: 2rem;
            background-color: #f8f9fa;
            border-left: 5px solid var(--primary-color);
            margin: 2rem 0;
            position: relative;
            border-radius: 0 15px 15px 0;
        }}
        
        .roast::before {{
            content: "🔥";
            position: absolute;
            top: -15px;
            left: -15px;
            font-size: 2rem;
            animation: flame 0.5s infinite alternate;
        }}
        
        @keyframes flame {{
            from {{ transform: scale(1) rotate(-5deg); }}
            to {{ transform: scale(1.2) rotate(5deg); }}
        }}
        
        .meme {{
            text-align: center;
            margin: 3rem 0;
            position: relative;
        }}
        
        .meme img {{
            max-width: 100%;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transform: rotate(-2deg);
            transition: transform 0.3s;
        }}
        
        .meme img:hover {{
            transform: rotate(2deg) scale(1.02);
        }}
        
        .meme::before {{
            content: "👇 Your model in a nutshell 👇";
            position: absolute;
            top: -30px;
            left: 0;
            right: 0;
            text-align: center;
            font-weight: bold;
            color: var(--primary-color);
        }}
        
        .test {{
            margin: 2rem 0;
            padding: 1.5rem;
            border-radius: 15px;
            background-color: #f8f9fa;
            position: relative;
            overflow: hidden;
        }}
        
        .test::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 5px;
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color), var(--accent-color));
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        th, td {{
            padding: 1rem;
            text-align: left;
        }}
        
        th {{
            background-color: var(--dark-color);
            color: white;
            font-family: 'Press Start 2P', cursive;
            font-size: 0.9rem;
        }}
        
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        
        tr:hover {{
            background-color: #e6f7ff;
        }}
        
        .metric {{
            font-weight: bold;
            color: var(--dark-color);
        }}
        
        .passed {{
            color: #33d9b2;
            font-weight: bold;
            position: relative;
            padding-left: 25px;
        }}
        
        .passed::before {{
            content: "✅";
            position: absolute;
            left: 0;
        }}
        
        .failed {{
            color: #ff5252;
            font-weight: bold;
            position: relative;
            padding-left: 25px;
        }}
        
        .failed::before {{
            content: "❌";
            position: absolute;
            left: 0;
        }}
        
        footer {{
            text-align: center;
            margin: 3rem 0 1rem;
            padding: 1rem;
            font-size: 1rem;
            color: var(--dark-color);
            position: relative;
        }}
        
        footer::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 25%;
            right: 25%;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--primary-color), transparent);
        }}
        
        .easter-egg {{
            position: fixed;
            bottom: 10px;
            right: 10px;
            font-size: 1.5rem;
            cursor: pointer;
            z-index: 100;
            opacity: 0.5;
            transition: opacity 0.3s;
        }}
        
        .easter-egg:hover {{
            opacity: 1;
        }}
    </style>
</head>
<body>
    <header>
        <h1>🔥 AI ROAST MACHINE 🤖</h1>
        <p>Making fun of AI models since 2025</p>
        <p>Report generated on {time.strftime("%Y-%m-%d %H:%M:%S")}</p>
    </header>

    <div class="container">
        <h2>Model: {model_name}</h2>
        
        <div class="score-container">
            <h3>Overall Score</h3>
            <div class="score-wrapper">
                <div class="score {score_class}">{score_percent}%</div>
            </div>
            <div class="score-comment">{score_comment}</div>
        </div>
        
        <div class="roast">
            <h3>The Brutal Roast</h3>
            <p>"{roast}"</p>
        </div>
        
        <div class="meme">
            <h3>The Meme That Says It All</h3>
            <img src="../{meme_path}" alt="AI Roast Meme">
        </div>
    </div>

    <div class="container">
        <h2>The Technical Stuff (Boring Part)</h2>
"""
    
    # Add test results
    for test in tests:
        test_name = test.get("test_name", "Unknown Test")
        passed = test.get("passed", False)
        details = test.get("details", "No details provided")
        metrics = test.get("metrics", {})
        
        # Add some funny comments based on test name
        funny_comments = {
            "langtest": [
                "Testing if your model can actually speak English... or at least try to.",
                "We asked your model to write poetry. It wrote a grocery list.",
                "Your model's language skills are being evaluated. No pressure."
            ],
            "deepchecks": [
                "Checking if your model is actually doing something or just pretending.",
                "Deep diving into your model's psyche. It needs therapy.",
                "We're checking if your model has deep thoughts or shallow excuses."
            ],
            "textattack": [
                "We tried to confuse your model. It was already confused.",
                "Testing if your model can handle adversarial examples or just gives up.",
                "Your model vs. tricky inputs: Fight!"
            ]
        }
        
        funny_comment = ""
        if test_name.lower() in funny_comments:
            funny_comment = f"<p><em>{random.choice(funny_comments[test_name.lower()])}</em></p>"
        
        html += f"""
        <div class="test">
            <h3>{test_name}</h3>
            {funny_comment}
            <p><strong>Status:</strong> <span class="{'passed' if passed else 'failed'}">{('PASSED' if passed else 'FAILED')}</span></p>
            <p><strong>Details:</strong> {details}</p>
            
            <table>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
"""
        
        # Add metrics with funny comments
        for metric, value in metrics.items():
            # Format value as percentage if it's a float between 0 and 1
            if isinstance(value, float) and 0 <= value <= 1:
                formatted_value = f"{value:.2f} ({int(value * 100)}%)"
            else:
                formatted_value = str(value)
            
            # Add funny comment for some metrics
            metric_comments = {
                "accuracy": [
                    "How often it's right (probably by accident)",
                    "Percentage of lucky guesses",
                    "Times it didn't embarrass itself"
                ],
                "robustness": [
                    "Can it handle the unexpected? (Spoiler: barely)",
                    "How well it deals with curveballs",
                    "Ability to not fall apart under pressure"
                ],
                "bias": [
                    "How opinionated your model is",
                    "Political leaning detector",
                    "Favoritism score"
                ],
                "adversarial_success_rate": [
                    "How easily it gets tricked",
                    "Gullibility factor",
                    "Tendency to be fooled by clever inputs"
                ]
            }
            
            metric_comment = ""
            if metric.lower() in metric_comments:
                metric_comment = f"<br><small><em>{random.choice(metric_comments[metric.lower()])}</em></small>"
                
            html += f"""
                <tr>
                    <td class="metric">{metric}{metric_comment}</td>
                    <td>{formatted_value}</td>
                </tr>"""
        
        html += """
            </table>
        </div>
"""
    
    # Close HTML with easter egg
    html += """
    </div>

    <footer>
        <p>Generated by AI Roast Machine | <a href="https://github.com/YOUR_USERNAME/AI-Roast-Machine">GitHub</a></p>
        <p><small>No AIs were harmed in the making of this report. Their feelings, however...</small></p>
    </footer>
    
    <div class="easter-egg" onclick="alert('You found the easter egg! Your model is still not as good as GPT-5 though.')">🥚</div>
    
    <script>
        // Add some fun interactions
        document.addEventListener('DOMContentLoaded', function() {
            // Make the header text change color on hover
            const header = document.querySelector('header h1');
            header.addEventListener('mouseover', function() {
                this.style.color = '#' + Math.floor(Math.random()*16777215).toString(16);
            });
            header.addEventListener('mouseout', function() {
                this.style.color = '';
            });
            
            // Add confetti when clicking on the score
            const score = document.querySelector('.score');
            score.addEventListener('click', function() {
                alert('🎉 Congratulations! Your model is ' + Math.floor(Math.random() * 100) + '% better than a random number generator!');
            });
        });
    </script>
</body>
</html>
"""
    
    # Write HTML to file
    with open(output_path, "w") as f:
        f.write(html)
    
    logger.info(f"Quirky HTML report generated at {output_path}")
    return output_path


def main():
    """Run a minimal test of the AI Roast Machine."""
    logger.info("Starting minimal AI Roast Machine test")
    print("✅ Testing AI Roast Machine (minimal test)...")

    # Test parameters
    model_name = "gpt2"
    model_type = "text-generation"
    test_output = "test_results/test_results.json"
    roast_output = "test_results/roast_results.json"
    meme_output = "memes/meme.png"
    report_output = "test_results/report.html"

    # Create mock test results
    print(f"Testing model: {model_name}")
    mock_test_results = {
        "model_name": model_name,
        "model_type": model_type,
        "tests": [
            {
                "test_name": "langtest",
                "metrics": {
                    "accuracy": 0.85,
                    "robustness": 0.72,
                    "bias": 0.15,
                },
                "passed": True,
                "details": "Model performs well on general language tasks"
            },
            {
                "test_name": "deepchecks",
                "metrics": {
                    "data_integrity": 0.92,
                    "model_integrity": 0.88,
                    "concept_drift": 0.05,
                },
                "passed": True,
                "details": "Model passes all integrity checks"
            },
            {
                "test_name": "textattack",
                "metrics": {
                    "adversarial_success_rate": 0.25,
                    "average_perturbed_words": 3.2,
                    "attack_attempts": 100,
                },
                "passed": True,
                "details": "Model is reasonably robust to adversarial attacks"
            }
        ],
        "overall_score": 0.85,
    }
    
    # Save mock test results
    save_json(mock_test_results, test_output)
    print(f"Test results saved to {test_output}")
    
    # Generate roast
    roast_results = generate_model_roast(mock_test_results)
    save_json(roast_results, roast_output)
    print(f"Roast results saved to {roast_output}")
    print(f"Roast: {roast_results['combined_roast']}")
    
    # Generate meme with roast text
    meme_path = generate_meme(meme_output, roast_results['combined_roast'], model_name, mock_test_results['overall_score'])
    print(f"Meme saved to {meme_path}")
    
    # Generate HTML report
    report_path = generate_html_report(mock_test_results, roast_results, meme_output, report_output)
    print(f"HTML report generated at {report_path}")
    
    print("✅ AI Roast Machine minimal test completed!")


if __name__ == "__main__":
    main() 