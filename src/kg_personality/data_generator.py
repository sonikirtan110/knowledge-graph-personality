"""Synthetic data generator for knowledge graph examples"""
import random
from pathlib import Path

NAMES = [
    "Alex Johnson", "Maria Garcia", "Wei Chen", "James Smith", "Priya Patel",
    "David Kim", "Sophie Martin", "Omar Hassan", "Lisa Wong", "Tom Anderson"
]

ORGANIZATIONS = [
    "TechCorp", "DataSys Inc.", "AI Solutions", "CloudMatrix", "Neural Labs",
    "Stanford University", "MIT", "Google Research", "Microsoft AI", "DeepMind"
]

SKILLS = [
    "Python", "Machine Learning", "Deep Learning", "Natural Language Processing",
    "Computer Vision", "Data Science", "Neural Networks", "Cloud Computing",
    "Java", "C++"
]

TRAITS = [
    "analytical", "creative", "detail-oriented", "innovative", "leadership",
    "collaborative", "problem-solver", "strategic", "adaptable", "organized"
]

TEMPLATES = [
    "{name} is a {trait} researcher at {org}. They excel in {skill1} and {skill2}.",
    "At {org}, {name} leads the {skill1} team. Their {trait} approach has been crucial for success.",
    "{name}, known for being {trait}, works with {org} on {skill1} projects.",
    "The {skill1} expert {name} collaborates with {org}, bringing their {trait} mindset.",
    "{name} from {org} specializes in {skill1} and {skill2}. Their {trait} nature drives innovation."
]

def generate_example(num_people=3):
    """Generate a synthetic example with specified number of people"""
    paragraphs = []
    used_names = random.sample(NAMES, num_people)
    
    for name in used_names:
        template = random.choice(TEMPLATES)
        org = random.choice(ORGANIZATIONS)
        skill1, skill2 = random.sample(SKILLS, 2)
        trait = random.choice(TRAITS)
        
        paragraph = template.format(
            name=name,
            org=org,
            skill1=skill1,
            skill2=skill2,
            trait=trait
        )
        paragraphs.append(paragraph)
    
    return "\n\n".join(paragraphs)

def main():
    # Generate examples of different sizes
    examples = {
        'small': generate_example(2),
        'medium': generate_example(4),
        'large': generate_example(6)
    }
    
    # Save to data directory
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)
    
    for size, text in examples.items():
        output_file = data_dir / f'{size}_example.txt'
        output_file.write_text(text)
        print(f"Generated {size} example in {output_file}")

if __name__ == '__main__':
    main()