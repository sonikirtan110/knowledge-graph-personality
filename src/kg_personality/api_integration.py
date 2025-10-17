"""
Groq API integration for enhancing knowledge graph personality analysis.
"""
import os
from typing import Dict, List, Optional
import groq
from . import config
from .personality import PersonalityEstimator

class GroqAPIIntegrator:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Groq API integration.
        
        Args:
            api_key: Groq API key. If not provided, looks for GROQ_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY") or config.GROQ_API_KEY
        if not self.api_key:
            raise ValueError("Groq API key not found. Please provide it in config.py or set GROQ_API_KEY environment variable.")
        
        self.client = groq.Client(api_key=self.api_key)
        self.personality_estimator = PersonalityEstimator()

    def analyze_text_with_llm(self, text: str) -> Dict[str, float]:
        """
        Analyze text using Groq's LLM to enhance personality trait detection.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary of personality traits and their scores
        """
        prompt = f'''Analyze the following text and rate the Big Five personality traits
        (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism)
        on a scale of 0.0 to 1.0. Provide only the numerical scores in JSON format.
        
        Text to analyze: {text}'''

        completion = self.client.chat.completions.create(
            model=config.DEFAULT_MODEL,
            messages=[{
                "role": "user",
                "content": prompt
            }],
            temperature=config.TEMPERATURE
        )

        # Parse the response to get trait scores
        try:
            response_text = completion.choices[0].message.content
            # Clean up response to ensure it's valid JSON
            response_text = response_text.strip()
            if not response_text.startswith("{"):
                response_text = response_text[response_text.find("{"):]
            if not response_text.endswith("}"):
                response_text = response_text[:response_text.rfind("}") + 1]
            
            import json
            scores = json.loads(response_text)
            
            # Ensure all traits are present
            required_traits = ["openness", "conscientiousness", "extraversion", 
                             "agreeableness", "neuroticism"]
            for trait in required_traits:
                if trait.lower() not in {k.lower() for k in scores.keys()}:
                    scores[trait] = 0.5  # Default score if missing
            
            return scores
        
        except Exception as e:
            print(f"Error parsing LLM response: {e}")
            return {trait: 0.5 for trait in ["openness", "conscientiousness", 
                                           "extraversion", "agreeableness", "neuroticism"]}

    def enhance_personality_estimation(self, text: str, 
                                    base_scores: Optional[Dict[str, float]] = None) -> Dict[str, float]:
        """
        Combine traditional personality estimation with LLM-based analysis.
        
        Args:
            text: Input text to analyze
            base_scores: Optional baseline scores from traditional analysis
            
        Returns:
            Enhanced personality trait scores
        """
        # Get LLM-based analysis
        llm_scores = self.analyze_text_with_llm(text)
        
        if base_scores is None:
            # Use traditional analysis as base
            base_scores = self.personality_estimator.estimate_traits(text)
        
        # Combine scores (simple average for now, could be weighted in future)
        enhanced_scores = {}
        for trait in base_scores:
            enhanced_scores[trait] = (base_scores[trait] + llm_scores.get(trait, 0.5)) / 2
            
        return enhanced_scores