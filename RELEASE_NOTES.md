# AI Roast Machine 1.0.0 - Release Notes

We're excited to announce the initial release of AI Roast Machine, a fun tool to test, compare, and roast AI models with a humorous twist!

## Features

- 🤖 **Test individual models** with custom prompts
- 🔄 **Compare multiple models** on the same prompt
- ⚖️ **Test models for bias** with specialized prompts
- 🤣 **Generate weird AI memes** for fun
- 📊 **Create retro-style HTML reports** with fun roasts and jokes
- 🎮 **Retro gaming aesthetic** for all reports
- 🌐 **API access** to all functionality through a FastAPI interface
- 🐳 **Docker support** for containerized usage

## What's New

### Core Functionality
- OpenRouter API integration for accessing various AI models
- Interactive menu interface for easy testing and comparison
- Bias testing with specialized prompts
- Meme generation with creative models
- HTML report generation with retro gaming aesthetic

### User Experience
- Colorful terminal interface with ANSI colors
- Loading animations during model response waits
- Automatic opening of HTML reports in the browser
- Easy-to-use report viewer

### Developer Tools
- Comprehensive test suite with pytest
- Docker support for containerized usage
- API access to all functionality
- Cleanup script for easy maintenance

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-roast-machine.git
cd ai-roast-machine

# Install dependencies
pip install -r requirements.txt

# Create a .env file with your OpenRouter API key
echo "OPENROUTER_API_KEY=your_api_key_here" > .env
```

## Running the Application

```bash
# Using Python directly
python -m src.menu

# Using Docker
docker-compose up
```

## Known Issues
- Some models may not be available through OpenRouter
- Meme generation works best with more creative models

## Future Plans
- Support for more AI model providers
- Enhanced bias testing with more sophisticated metrics
- More customization options for HTML reports
- Integration with other AI evaluation frameworks

## Contributors
- Special thanks to all the AI models that were roasted in the making of this tool!

## License
This project is licensed under the MIT License - see the LICENSE file for details. 