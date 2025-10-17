# Knowledge Graph with Personality Traits

This project implements a system for extracting knowledge graphs from text while incorporating personality trait analysis. It combines natural language processing, graph theory, and personality modeling to create rich, interactive visualizations of relationships and characteristics found in text.

## Features

- Entity extraction using spaCy NLP
- Automatic relationship detection
- Personality trait modeling (Big Five traits)
- Interactive graph visualization
- Synthetic data generation
- Comprehensive test suite

## System Architecture

```
[Input Text] → [NLP Processing] → [Entity Extraction] → [Knowledge Graph] ↔ [Personality Traits]
```

The system follows a pipeline architecture where:
1. Input text is processed using spaCy NLP
2. Entities are extracted and relationships identified
3. Knowledge graph is constructed using NetworkX
4. Personality traits are analyzed and integrated
5. Interactive visualization is generated using pyvis

## Project Structure

```
.
├── src/
│   └── kg_personality/
│       ├── __init__.py
│       ├── kg_builder.py      # Knowledge graph construction
│       ├── personality.py     # Personality trait analysis
│       └── data_generator.py  # Synthetic data generation
├── data/
│   ├── sample.txt
│   ├── small_example.txt
│   ├── medium_example.txt
│   └── large_example.txt
├── tests/
│   └── test_pipeline.py
├── notebooks/
│   └── demo.xml
├── documentation/
│   └── documentation.pdf
├── run_demo.py
└── requirements.txt
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sonikirtan110/knowledge-graph-personality.git
cd knowledge-graph-personality

# Configure Git (if needed):
git config --global user.name "sonikirtan110"
git config --global user.email "sonikirtan100@gmail.com"
```

2. Create and activate a Python virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Usage

1. Run the demo:
```bash
python run_demo.py
```

2. Generate synthetic data:
```bash
python -m src.kg_personality.data_generator
```

3. Run tests:
```bash
pytest -v
```

4. View visualization:
- Open `knowledge_graph.html` in a web browser
- Interact with nodes to see personality traits and relationships
- Use mouse wheel to zoom and drag to pan

## Project Highlights

### Entity Types
- Person (PERSON)
- Organization (ORG)
- Skills (SKILL)
- Traits (TRAIT)

### Personality Traits
The system analyzes entities for the Big Five personality traits:
- Openness
- Conscientiousness
- Extraversion
- Agreeableness
- Neuroticism

### Relationship Types
- works_at: Person -> Organization
- has_skill: Person -> Skill
- exhibits: Person -> Trait
- mentions: Document -> Entity

## Documentation

For detailed documentation:
1. Install LaTeX if not already installed
2. Compile documentation:
```bash
pdflatex documentation.tex
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details
