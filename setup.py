from setuptools import setup, find_packages

setup(
    name="kg_personality",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "spacy>=3.0.0",
        "networkx>=2.8.0",
        "pandas>=1.5.0",
        "pyvis>=0.3.0",
        "nltk>=3.8.0",
        "groq>=0.4.0",
    ],
    python_requires=">=3.8",
)