"""Knowledge Graph builder utilities with visualization
"""
from typing import List, Dict, Tuple, Any, Optional
import networkx as nx
import spacy
from pathlib import Path
import json

# Initialize spaCy with custom pipeline
nlp = spacy.load("en_core_web_sm")

# Add custom entity patterns
ruler = nlp.add_pipe("entity_ruler", before="ner")
patterns = [
    {"label": "SKILL", "pattern": [{"LOWER": "python"}]},
    {"label": "SKILL", "pattern": [{"LOWER": "java"}]},
    {"label": "SKILL", "pattern": [{"LOWER": "machine"}, {"LOWER": "learning"}]},
    {"label": "TRAIT", "pattern": [{"LOWER": "creative"}]},
    {"label": "TRAIT", "pattern": [{"LOWER": "analytical"}]},
]
ruler.add_patterns(patterns)

class KGBuilder:
    def __init__(self):
        self.graph = nx.DiGraph()

    def extract_entities(self, text: str) -> List[Tuple[str, str]]:
        doc = nlp(text)
        return [(ent.text, ent.label_) for ent in doc.ents]

    def add_entity(self, node_id: str, label: str, attrs: Dict[str, Any] = None):
        self.graph.add_node(node_id, label=label, **(attrs or {}))

    def add_relation(self, src: str, dst: str, rel_type: str, attrs: Dict[str, Any] = None):
        self.graph.add_edge(src, dst, type=rel_type, **(attrs or {}))

    def build_from_text(self, text: str, source_id: str = "doc"):
        ents = self.extract_entities(text)
        for i, (ent_text, ent_label) in enumerate(ents):
            node_id = f"{source_id}_ent_{i}"
            self.add_entity(node_id, ent_label, {"text": ent_text})
            # link to source doc
            self.add_relation(source_id, node_id, "mentions")
        return self.graph

    def merge_personality(self, graph: nx.DiGraph, personality: Dict[str, Dict[str, float]]):
        # personality: {entity_node_id: {trait:score}}
        for node_id, traits in personality.items():
            if node_id not in graph:
                continue
            for trait, score in traits.items():
                graph.nodes[node_id][f"trait_{trait}"] = float(score)
        return graph
    
    def add_relationships(self):
        """Add relationship edges between entities based on sentence proximity"""
        nodes = list(self.graph.nodes())
        for i, node1 in enumerate(nodes):
            for node2 in nodes[i+1:]:
                if node1 == node2 or not (node1.startswith('doc_ent_') and node2.startswith('doc_ent_')):
                    continue
                    
                n1_text = self.graph.nodes[node1].get('text', '')
                n2_text = self.graph.nodes[node2].get('text', '')
                n1_label = self.graph.nodes[node1].get('label', '')
                n2_label = self.graph.nodes[node2].get('label', '')
                
                if n1_label == 'PERSON' and n2_label == 'ORG':
                    self.add_relation(node1, node2, 'works_at')
                elif n1_label == 'PERSON' and n2_label == 'SKILL':
                    self.add_relation(node1, node2, 'has_skill')
                elif n1_label == 'PERSON' and n2_label == 'TRAIT':
                    self.add_relation(node1, node2, 'exhibits')

    def export_to_html(self, output_path: str):
        """Export graph visualization to HTML using pyvis"""
        try:
            from pyvis.network import Network
        except ImportError:
            print("pyvis not installed. Installing with pip...")
            import subprocess
            subprocess.check_call(["pip", "install", "pyvis"])
            from pyvis.network import Network

        # Create network
        net = Network(height="800px", width="100%", bgcolor="#ffffff", font_color="black")
        
        # Add nodes
        for node, attrs in self.graph.nodes(data=True):
            label = attrs.get('text', node)
            group = attrs.get('label', 'OTHER')
            
            # Create tooltip
            title = f"Type: {group}<br>"
            traits = {k:v for k,v in attrs.items() if k.startswith('trait_')}
            if traits:
                title += "<br>Personality Traits:<br>"
                for trait, score in traits.items():
                    trait_name = trait.replace('trait_', '').capitalize()
                    title += f"{trait_name}: {score:.2f}<br>"
            
            # Node styling
            color = {
                'PERSON': '#4CAF50',
                'ORG': '#2196F3',
                'SKILL': '#FFC107',
                'TRAIT': '#9C27B0'
            }.get(group, '#607D8B')
            
            net.add_node(node, label=label, title=title, color=color)
        
        # Add edges
        for u, v, data in self.graph.edges(data=True):
            title = data.get('type', '')
            net.add_edge(u, v, title=title)
        
        # Save
        net.save_graph(output_path)
        print(f"Graph visualization saved to {output_path}")
        print(f"Graph visualization saved to {output_path}")

    def to_edge_list(self) -> List[Tuple[str, str, Dict[str, Any]]]:
        return [(u, v, d) for u, v, d in self.graph.edges(data=True)]
