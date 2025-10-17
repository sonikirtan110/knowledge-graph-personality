"""Personality extraction utilities
"""
from typing import Dict, List
import spacy

TRAITS = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]

class PersonalityEstimator:
    def __init__(self):
        """Initialize the personality estimator."""
        self.nlp = spacy.load("en_core_web_sm")
        
        # Define trait keywords
        self.trait_keywords = {
            "openness": ["creative", "innovative", "curious", "artistic", "imaginative"],
            "conscientiousness": ["organized", "responsible", "methodical", "thorough", "systematic"],
            "extraversion": ["outgoing", "sociable", "energetic", "assertive", "talkative"],
            "agreeableness": ["cooperative", "compassionate", "helpful", "sympathetic", "kind"],
            "neuroticism": ["anxious", "tense", "worried", "nervous", "stressed"]
        }
    
    def estimate_traits(self, text: str) -> Dict[str, float]:
        """
        Estimate personality traits from text using keyword analysis.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary of trait scores (0-1)
        """
        doc = self.nlp(text.lower())
        
        # Count trait-related words
        trait_counts = {trait: 0 for trait in self.trait_keywords}
        total_relevant_words = 0
        
        for token in doc:
            for trait, keywords in self.trait_keywords.items():
                if token.lemma_ in keywords:
                    trait_counts[trait] += 1
                    total_relevant_words += 1
        
        # Calculate normalized scores
        scores = {}
        for trait, count in trait_counts.items():
            if total_relevant_words > 0:
                scores[trait] = min(count / (total_relevant_words + 1), 1.0)
            else:
                scores[trait] = 0.5  # Default neutral score
        
        return scores
    
    def estimate_for_entities(self, entities: List[str], texts: Dict[str, str] = None) -> Dict[str, Dict[str, float]]:
        """
        Estimate personality traits for multiple entities.
        
        Args:
            entities: List of entity IDs
            texts: Optional dictionary mapping entity IDs to their associated text
            
        Returns:
            Dictionary mapping entity IDs to their trait scores
        """
        out = {}
        for ent in entities:
            if texts and ent in texts:
                scores = self.estimate_traits(texts[ent])
            else:
                # Fallback to default neutral scores
                scores = {trait: 0.5 for trait in TRAITS}
            out[ent] = scores
        return out
