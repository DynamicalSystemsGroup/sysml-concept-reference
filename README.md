# SysML Concept Reference

Public research toward a source-backed inventory of the SysML v2 language: entities, relationships, properties, constraints, syntax, libraries and behavioral semantics.

The research home is [DynamicalSystemsGroup/sysml-concept-reference](https://github.com/DynamicalSystemsGroup/sysml-concept-reference). This project inventories language definitions and semantics independently of particular implementations.

## Current evidence

The seed catalogue comes from the OMG SysML 2.0 Language Specification, Part 1, `formal/2026-03-02` (March 2026), queried through the user-provided NotebookLM notebook and checked against its retrieved source text.

It contains **98 named entries** from §§8.3.6–8.3.27: 93 metaclasses, 5 enumerations, 218 declared property signatures and 365 constraint names. These are extraction counts, not a claim of complete SysML/KerML coverage or conformance.

| Resource | Contents |
|---|---|
| [GitHub Pages publishing](docs/publishing.md) | Site build, preview, deployment workflow and update instructions |
| [Concept browser](docs/concept-browser.html) | Offline browsing of the first RDF slice: meanings, properties, ancestry, mechanisms and source links |
| [Notation coverage](docs/notation-coverage.md) | Source register of 192 labeled cells and 639 grammar occurrences; representative mappings and explicit review gaps |
| [RDF inventory guide](docs/rdf-inventory.md) | Data model, SHACL/SPARQL commands, reproduction and coverage limits |
| [Language research](docs/language-research.md) | Findings, source distinctions, behavioral scope, known uncertainties and query reproduction |
| [Machine-readable inventory](data/language-inventory.json) | Entries, property declarations, general classes, constraint names, source metadata and seven notebook query topics/hashes |
| [Official machine-readable sources](docs/official-machine-readable-specs.md) | Normative artifact URLs, source roles, extraction approach and verification limits |
| [Research roadmap](docs/roadmap.md) | Work needed to inventory the complete language and its dependencies |

The focused RDF slice derives **17 focus metaclasses plus eight ancestors, 180 declared properties and 218 constraint names** from hash-pinned official XMI. Four source-checked draft profiles cover [PartUsage](docs/concepts/part-usage.md), [PartDefinition](docs/concepts/part-definition.md), [PortUsage](docs/concepts/port-usage.md) and [ConnectionUsage](docs/concepts/connection-usage.md). They include 164 property explanations, effective inherited properties, qualified relationships, connected examples and representative graphical notation with precise official source links.

UML normalization preserves raw encodings and distinguishes missing defaults from literal values. Explicit redefinitions retain their history. Examples remain source-reviewed and have not been executed by a SysML engine. See the [page contract](docs/concept-page-contract.md) and [roadmap](docs/roadmap.md) for boundaries and next work.

## Working with the research

The GitHub Pages setup publishes the concept browser, rendered research notes, data downloads and SPARQL queries from this repository. Build a local preview with `uv run --locked python scripts/build_site.py`; the [publishing guide](docs/publishing.md) covers deployment. Site address: [dynamicalsystemsgroup.github.io/sysml-concept-reference](https://dynamicalsystemsgroup.github.io/sysml-concept-reference/). The [Pages workflow](https://github.com/DynamicalSystemsGroup/sysml-concept-reference/actions/workflows/pages.yml) records deployment status.

No runtime, backend or dependencies are required to read the Markdown, JSON, Turtle or generated HTML files. Open the HTML locally to use its search and property browser. Python and locked `uv` development tools are needed only to rebuild and validate the RDF slice; see the [RDF guide](docs/rdf-inventory.md). The existing `nlm` CLI was used for notebook research; access to that notebook is not necessarily public. Query topics and source references are documented so the research can be revisited without publishing notebook credentials or changing its sharing settings.

Keep source facts, generated answers, interpretations, implementation choices and verification results distinct. Preserve source versions, URLs, hashes and unresolved discrepancies. Do not infer completeness from a summary or from a successful parser example.

Use ignored `sandbox/` for downloaded sources and working evidence. Do not commit credentials, authentication state, raw notebook session files or unpublished working material. Reviewed source-derived records belong in `data/`; explanatory findings and methodology belong in `docs/`.

Validation covers extraction provenance, normalization, inheritance, profiles, RDF integrity, generated browser behavior and published links. Source-dependent tests skip when originals are unavailable. These checks do not establish SysML conformance.

The site uses the official [Dynamical Systems Group](https://www.dynamicalsystemsgroup.com/) identity: navy, paper and brass, with locally hosted open-source typography. Asset sources and licenses are recorded in [brand provenance](site/assets/provenance.json).

## License

Copyright 2026 Dynamical Systems Group. Except where otherwise noted, original project code, documentation and illustrations are licensed under the [Apache License 2.0](LICENSE).

Third-party material retains its existing terms. OMG specifications and source-derived material remain subject to the applicable source terms recorded in the [source manifest](data/source-manifest.json). Bundled fonts retain their included SIL Open Font License notices; see [asset provenance](site/assets/provenance.json). DSG names and logos are not included in the Apache license grant.
