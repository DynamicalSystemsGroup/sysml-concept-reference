# SysML v2 inventory

Public research toward a source-backed inventory of the SysML v2 language: entities, relationships, properties, constraints, syntax, libraries and behavioral semantics.

The research home is [rororowyourboat/sysmlv2_inventory](https://github.com/rororowyourboat/sysmlv2_inventory). This project inventories language definitions and semantics independently of particular implementations.

## Current evidence

The seed catalogue comes from the OMG SysML 2.0 Language Specification, Part 1, `formal/2026-03-02` (March 2026), queried through the user-provided NotebookLM notebook and checked against its retrieved source text.

It contains **98 named entries** from §§8.3.6–8.3.27: 93 metaclasses, 5 enumerations, 218 declared property signatures and 365 constraint names. These are extraction counts, not a claim of complete SysML/KerML coverage or conformance.

| Resource | Contents |
|---|---|
| [GitHub Pages publishing](docs/publishing.md) | Site build, preview, deployment workflow and update instructions |
| [Concept browser](docs/concept-browser.html) | Offline browsing of the first RDF slice: meanings, properties, ancestry, mechanisms and source links |
| [RDF inventory guide](docs/rdf-inventory.md) | Data model, SHACL/SPARQL commands, reproduction and coverage limits |
| [Language research](docs/language-research.md) | Findings, source distinctions, behavioral scope, known uncertainties and query reproduction |
| [Machine-readable inventory](data/language-inventory.json) | Entries, property declarations, general classes, constraint names, source metadata and seven notebook query topics/hashes |
| [Official machine-readable sources](docs/official-machine-readable-specs.md) | Normative artifact URLs, source roles, extraction approach and verification limits |
| [Research roadmap](docs/roadmap.md) | Work needed to inventory the complete language and its dependencies |

A focused RDF slice now derives **15 focus metaclasses plus six ancestors, 172 directly declared properties and 200 constraint names** from two hash-pinned official XMI files. Four mechanisms distinguish ownership, membership, featuring and composition/reference. SHACL validates catalogue integrity; SPARQL traverses ancestry while retaining declaration origins. This is separate from the PDF-derived seed, and graphical notation remains unverified.

## Next milestone

Normalize multiplicities and defaults against pinned UML definitions, audit graphical notation for a representative concept, and extend extraction and reconciliation toward the complete metamodel, including effective inherited properties. Standard libraries, syntax and behavior require separate coverage audits. See the roadmap for acceptance criteria.

## Working with the research

The GitHub Pages setup publishes the concept browser, rendered research notes, data downloads and SPARQL queries from this repository. Build a local preview with `uv run --locked python scripts/build_site.py`; the [publishing guide](docs/publishing.md) covers deployment. Site address: [rororowyourboat.github.io/sysmlv2_inventory](https://rororowyourboat.github.io/sysmlv2_inventory/). The [Pages workflow](https://github.com/rororowyourboat/sysmlv2_inventory/actions/workflows/pages.yml) records deployment status.

No runtime, backend or dependencies are required to read the Markdown, JSON, Turtle or generated HTML files. Open the HTML locally to use its search and property browser. Python and locked `uv` development tools are needed only to rebuild and validate the RDF slice; see the [RDF guide](docs/rdf-inventory.md). The existing `nlm` CLI was used for notebook research; access to that notebook is not necessarily public. Query topics and source references are documented so the research can be revisited without publishing notebook credentials or changing its sharing settings.

Keep source facts, generated answers, interpretations, implementation choices and verification results distinct. Preserve source versions, URLs, hashes and unresolved discrepancies. Do not infer completeness from a summary or from a successful parser example.

Use ignored `sandbox/` for downloaded sources and working evidence. Do not commit credentials, authentication state, raw notebook session files or unpublished working material. Reviewed source-derived records belong in `data/`; explanatory findings and methodology belong in `docs/`.

The seed JSON parses and its counts, unique names/sections, source-backed declaration strings and local documentation links were checked during the original research. After copying, JSON structure/counts and repository documentation links were checked again. The RDF slice also passes SHACL checks and nine catalogue/source-integrity tests; these are not SysML conformance tests. The generated HTML has not received a visual browser check in this environment.
