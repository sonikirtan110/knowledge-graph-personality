import pytest
from src.kg_personality.kg_builder import KGBuilder
from src.kg_personality.personality import PersonalityEstimator
from src.kg_personality.data_generator import generate_example


@pytest.fixture
def kg_builder():
    return KGBuilder()

@pytest.fixture
def personality_estimator():
    return PersonalityEstimator(seed=42)

def test_pipeline_runs(kg_builder, personality_estimator):
    text = "Alice works with Bob."
    G = kg_builder.build_from_text(text, source_id="t1")
    entities = [n for n in G.nodes() if n.startswith("t1_ent_")]
    personality = personality_estimator.estimate_for_entities(entities)
    kg_builder.merge_personality(G, personality)
    
    # basic assertions
    assert len(entities) >= 1
    for e in entities:
        assert any(k.startswith("trait_") for k in G.nodes[e].keys())

def test_entity_extraction(kg_builder):
    text = "John is a Python developer at Google. He knows machine learning."
    G = kg_builder.build_from_text(text, source_id="t2")
    
    # Get entity texts
    entity_texts = [
        d.get('text', '') 
        for n, d in G.nodes(data=True) 
        if n.startswith("t2_ent_")
    ]
    
    # Check expected entities are found
    assert "John" in entity_texts
    assert "Python" in entity_texts
    assert "Google" in entity_texts
    assert "machine learning" in entity_texts

def test_relationship_detection(kg_builder):
    text = "Sarah works at Microsoft. She knows Python."
    G = kg_builder.build_from_text(text, source_id="t3")
    kg_builder.add_relationships()
    
    # Find Sarah and Microsoft nodes
    sarah_node = None
    microsoft_node = None
    python_node = None
    
    for n, d in G.nodes(data=True):
        if n.startswith("t3_ent_"):
            if d.get('text') == 'Sarah':
                sarah_node = n
            elif d.get('text') == 'Microsoft':
                microsoft_node = n
            elif d.get('text') == 'Python':
                python_node = n
    
    assert sarah_node and microsoft_node and python_node
    
    # Check relationships
    edges = list(G.edges(data=True))
    relationships = [(u, v, d.get('type')) for u, v, d in edges]
    
    assert (sarah_node, microsoft_node, 'works_at') in relationships
    assert (sarah_node, python_node, 'has_skill') in relationships

def test_personality_trait_values(kg_builder, personality_estimator):
    text = generate_example(num_people=1)  # Get one person example
    G = kg_builder.build_from_text(text, source_id="t4")
    entities = [n for n in G.nodes() if n.startswith("t4_ent_")]
    personality = personality_estimator.estimate_for_entities(entities)
    kg_builder.merge_personality(G, personality)
    
    # Check trait values
    for e in entities:
        traits = {k:v for k,v in G.nodes[e].items() if k.startswith('trait_')}
        assert len(traits) == 5  # Should have all Big Five traits
        for trait_value in traits.values():
            assert 0 <= trait_value <= 1  # Values should be normalized

def test_visualization_export(kg_builder, tmp_path):
    text = generate_example(num_people=2)
    G = kg_builder.build_from_text(text, source_id="t5")
    output_file = tmp_path / "test_graph.html"
    kg_builder.export_to_html(str(output_file))
    
    assert output_file.exists()
    content = output_file.read_text()
    assert 'vis-network' in content  # Should contain vis.js network
    assert 'nodes' in content  # Should have nodes data
    assert 'edges' in content  # Should have edges data
