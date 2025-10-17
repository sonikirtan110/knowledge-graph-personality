"""
Test script for Groq API integration with the Knowledge Graph system.
"""
from kg_personality.api_integration import GroqAPIIntegrator
from kg_personality.kg_builder import KGBuilder

def test_groq_integration():
    # Sample text with clear personality traits
    test_text = """
    Sarah Chen is a highly innovative researcher at TechLab. She consistently 
    demonstrates exceptional problem-solving abilities and creative thinking in 
    her work with AI systems. While she prefers working independently on complex 
    challenges, she's always willing to collaborate and share her insights with 
    the team. Her methodical approach to documentation and systematic testing 
    shows great attention to detail.
    """
    
    print("1. Initializing Groq API Integrator...")
    groq_api = GroqAPIIntegrator()
    
    print("\n2. Testing direct LLM analysis...")
    llm_traits = groq_api.analyze_text_with_llm(test_text)
    print("\nLLM-based trait analysis:")
    for trait, score in llm_traits.items():
        print(f"{trait.capitalize()}: {score:.2f}")
    
    print("\n3. Testing enhanced personality estimation...")
    enhanced_traits = groq_api.enhance_personality_estimation(test_text)
    print("\nEnhanced trait analysis (combining LLM and traditional methods):")
    for trait, score in enhanced_traits.items():
        print(f"{trait.capitalize()}: {score:.2f}")
    
    print("\n4. Testing integration with Knowledge Graph...")
    kg = KGBuilder()
    G = kg.build_from_text(test_text)
    
    # Get entities and their text content
    entities = [n for n in G.nodes() if isinstance(n, str) and n.startswith("doc_ent_")]
    entity_texts = {ent: G.nodes[ent].get('text', '') for ent in entities}
    print(f"\nFound {len(entities)} entities in the text")
    
    # Analyze and merge personality traits
    print("\nAnalyzing personality traits for entities...")
    all_traits = groq_api.personality_estimator.estimate_for_entities(entities, entity_texts)
    for entity, traits in all_traits.items():
        print(f"\nEntity: {entity_texts[entity]}")
        for trait, score in traits.items():
            print(f"{trait.capitalize()}: {score:.2f}")
    
    # Generate visualization
    print("\n5. Generating visualization...")
    kg.export_to_html("knowledge_graph_with_traits.html")
    print("\nVisualization saved as 'knowledge_graph_with_traits.html'")

if __name__ == "__main__":
    print("Starting Groq API Integration Test\n" + "="*40 + "\n")
    test_groq_integration()
    print("\nTest completed successfully!")