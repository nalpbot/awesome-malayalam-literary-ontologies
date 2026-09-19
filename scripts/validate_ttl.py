"""Minimal syntax checker for the MALO Turtle files.

Install rdflib first:
    python -m pip install rdflib

Run:
    python scripts/validate_ttl.py
"""
from pathlib import Path
from rdflib import Graph

ROOT = Path(__file__).resolve().parents[1]
files = list((ROOT / "ontology").glob("*.ttl")) + list((ROOT / "vocabularies").glob("*.ttl")) + list((ROOT / "examples").glob("*.ttl"))

for path in files:
    graph = Graph()
    graph.parse(path, format="turtle")
    print(f"OK  {path.relative_to(ROOT)}  ({len(graph)} triples)")
