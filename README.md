# Awesome Malayalam Literary Ontologies

> A curated collection of ontologies, vocabularies, corpora, knowledge graphs, and semantic resources for Malayalam literature and Digital Humanities.

This repository is inspired by the [CLARIAH Awesome Ontologies for Digital Humanities](https://github.com/CLARIAH/awesome-humanities-ontologies), but is focused on **Malayalam literary and cultural data**.

## Project goals

1. Catalogue existing Malayalam literary, linguistic, and cultural semantic resources.
2. Develop **MALO — Malayalam Literary Ontology** as a reusable Linked Data model.
3. Provide Malayalam-specific vocabularies for genres, themes, periods, movements, and cultural entities.
4. Demonstrate how Malayalam NLP outputs can be linked to an ontology and knowledge graph.
5. Make the project useful to Digital Humanities researchers, librarians, computational linguists, and Malayalam scholars.

## Repository structure

```text
ontology/       MALO OWL/Turtle ontology
vocabularies/   Malayalam SKOS-style vocabularies
data/           curated datasets and mappings
examples/       worked RDF examples
scripts/        Python utilities for RDF generation/validation
 docs/          project and methodology notes
```

## MALO — Malayalam Literary Ontology

Namespace: `https://w3id.org/malo/`

Core classes in the first version:

- `malo:LiteraryWork`
- `malo:Author`
- `malo:Character`
- `malo:Place`
- `malo:LiteraryGenre`
- `malo:LiteraryTheme`
- `malo:LiteraryMovement`
- `malo:HistoricalPeriod`
- `malo:Publication`
- `malo:Translation`
- `malo:Adaptation`
- `malo:Manuscript`
- `malo:Motif`
- `malo:Event`

The ontology deliberately reuses established Semantic Web concepts where appropriate rather than replacing standards such as CIDOC-CRM, SKOS, OWL-Time, PROV-O, FOAF, and bibliographic models.

## Initial Malayalam vocabulary

The first vocabulary includes examples of:

- കവിത — poetry
- നോവൽ — novel
- ചെറുകഥ — short story
- നാടകം — drama
- ഭക്തി സാഹിത്യം — devotional literature
- മണിപ്രവാളം — Manipravalam
- മാപ്പിളപ്പാട്ട് — Mappilappattu
- ദളിത് സാഹിത്യം — Dalit literature
- പ്രവാസ സാഹിത്യം — diaspora literature
- പരിസ്ഥിതി — environment
- ജാതി — caste
- ലിംഗം — gender
- കുടിയേറ്റം — migration
- പ്രണയം — love
- മരണം — death

These are **starter concepts**, not a claim that the vocabulary is already a complete scholarly taxonomy. They should be expanded and documented through a transparent curation process.

## Example query

A future SPARQL endpoint should make questions such as the following possible:

> Find Malayalam literary works associated with a place and tagged with the theme of migration.

## Status

**v0.1 — research prototype.**

The ontology and vocabularies are being developed incrementally. Contributions, corrections, and scholarly review are welcome.

## Related resources

- [CLARIAH Awesome Ontologies for Digital Humanities](https://github.com/CLARIAH/awesome-humanities-ontologies)
- [Malayalam WordNet](https://malayalamwordnet.readme.io/)
- [Swathanthra Malayalam Computing corpus](https://github.com/smc/corpus)
- [INTRO — Intertextual, Interpictorial and Intermedial Relations Ontology](https://github.com/BOberreither/INTRO)

## Licence

CC0 1.0 for the curated list and original ontology/vocabulary content unless otherwise stated. External resources retain their own licences.
