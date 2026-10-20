# Understand the concepts behind SysML v2

A source-backed catalogue of KerML and SysML concepts, their properties, relationships and underlying mechanisms.

[Explore the concept browser](../docs/concept-browser.html)

## Start with the foundations

The first slice separates four mechanisms that can otherwise look like “containment”: **model ownership**, **namespace membership**, **feature context**, and **composition versus reference**.

Browse 15 focus concepts and six supporting ancestors. Inspect 172 property declarations with their declaring classes, explicit qualifiers and original XMI source links. Editorial explanations remain distinct from extracted facts.

## Read the evidence

| Guide | What you will find |
|---|---|
| [RDF inventory guide](../docs/rdf-inventory.md) | How the catalogue is structured, queried, validated and reproduced |
| [Official specification sources](../docs/official-machine-readable-specs.md) | OMG metamodels, JSON schemas, library archives and version caveats |
| [Language research](../docs/language-research.md) | The earlier PDF-derived inventory, semantic distinctions and known gaps |
| [Roadmap](../docs/roadmap.md) | Work toward complete metamodel, syntax, library and semantic coverage |
| [Publishing guide](../docs/publishing.md) | How this GitHub Pages site is built and updated |

## Query and reuse the catalogue

Download the [RDF files and source manifest](../data/), or explore the [saved SPARQL queries](../queries/). Everything is maintained as reviewable files in the [GitHub repository](https://github.com/rororowyourboat/sysmlv2_inventory).

The catalogue uses RDF for linked records, SHACL for inventory integrity, and SPARQL for exploration. OWL currently describes the catalogue vocabulary; it does not implement SysML semantic reasoning.

## Coverage is explicit

This is an initial research inventory. Graphical notation is not yet verified, constraint bodies are not evaluated, and ancestor declarations are not a computed effective property schema. No language completeness or conformance claim is made. See the [coverage limits](../docs/rdf-inventory.md#evidence-limits-and-next-work).
