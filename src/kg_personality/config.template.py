# Configuration template for API keys and settings
# Copy this file to config.py and fill in your credentials

# Groq API Configuration
GROQ_API_KEY = "your-api-key-here"  # Replace with your Groq API key

# Model Configuration
DEFAULT_MODEL = "mixtral-8x7b-32768"  # Default model to use
TEMPERATURE = 0.3  # Default temperature for generation

# Analysis Settings
COMBINE_WEIGHT = {
    'llm': 0.6,  # Weight for LLM-based analysis
    'traditional': 0.4  # Weight for traditional analysis
}