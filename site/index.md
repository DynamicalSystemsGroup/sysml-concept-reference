# Understand the concepts behind SysML v2

A source-backed catalogue of KerML and SysML concepts, their properties, relationships and underlying mechanisms.

[Explore the concept browser](../docs/concept-browser.html)

## Start with the foundations

The first slice separates four mechanisms that can otherwise look like “containment”: **model ownership**, **namespace membership**, **feature context**, and **composition versus reference**.

Browse 17 focus concepts and eight supporting ancestors. Inspect 180 property declarations, normalized bounds and defaults, effective inheritance and original source links.

Start with [PartUsage](../docs/concepts/part-usage.md), [PartDefinition](../docs/concepts/part-definition.md), [PortUsage](../docs/concepts/port-usage.md) and [ConnectionUsage](../docs/concepts/connection-usage.md): source-checked draft profiles connecting properties, relationships, examples and representative graphical notation to evidence.

## Read the evidence

| Guide | What you will find |
|---|---|
| [RDF inventory guide](../docs/rdf-inventory.md) | How the catalogue is structured, queried, validated and reproduced |
| [Official specification sources](../docs/official-machine-readable-specs.md) | OMG metamodels, JSON schemas, library archives and version caveats |
| [Language research](../docs/language-research.md) | The earlier PDF-derived inventory, semantic distinctions and known gaps |
| [Roadmap](../docs/roadmap.md) | Work toward complete metamodel, syntax, library and semantic coverage |
| [Publishing guide](../docs/publishing.md) | How this GitHub Pages site is built and updated |

## Query and reuse the catalogue

Download the [RDF files and source manifest](../data/), or explore the [saved SPARQL queries](../queries/). Everything is maintained as reviewable files in the [GitHub repository](https://github.com/DynamicalSystemsGroup/sysml-concept-reference).

The catalogue uses RDF for linked records, SHACL for inventory integrity, and SPARQL for exploration. OWL currently describes the catalogue vocabulary; it does not implement SysML semantic reasoning.

## Coverage is explicit

This is an initial research inventory. Representative notation for four profiles has been checked against the official specification. Effective properties account for explicit redefinitions and declaration identity. Constraint bodies are not evaluated, and examples have not been executed. No language completeness or conformance claim is made. See the [coverage limits](../docs/rdf-inventory.md#evidence-limits-and-next-work).
