"""Demo runner for the KG + Personality pipeline with visualization"""
from src.kg_personality.kg_builder import KGBuilder
from src.kg_personality.personality import PersonalityEstimator
from pathlib import Path

# Read complex example
SAMPLE = Path("data/complex_example.txt").read_text()


def main():
    # Initialize and build KG
    kg = KGBuilder()
    G = kg.build_from_text(SAMPLE, source_id="doc")
    
    # Get entities and estimate personality
    entities = [n for n, d in G.nodes(data=True) if n.startswith("doc_ent_")]
    pe = PersonalityEstimator()
    personality = pe.estimate_for_entities(entities)
    
    # Merge personality traits and add relationships
    kg.merge_personality(G, personality)
    kg.add_relationships()
    
    # Print text summary
    print("Knowledge Graph Summary:")
    print("\nNodes:")
    for n, d in G.nodes(data=True):
        if n.startswith("doc_ent_"):
            print(f"\n{d.get('text', '')} ({d.get('label', '')}):")
            traits = {k:v for k,v in d.items() if k.startswith('trait_')}
            for trait, score in traits.items():
                print(f"  {trait.replace('trait_', '').capitalize()}: {score:.2f}")
    
    print("\nRelationships:")
    for u, v, d in G.edges(data=True):
        if u.startswith("doc_ent_") and v.startswith("doc_ent_"):
            u_text = G.nodes[u].get('text', u)
            v_text = G.nodes[v].get('text', v)
            rel = d.get('type', 'related_to')
            print(f"{u_text} {rel} {v_text}")
    
    # Generate visualization
    kg.export_to_html("knowledge_graph.html")
    print("\nVisualization saved to knowledge_graph.html")


if __name__ == "__main__":
    main()
