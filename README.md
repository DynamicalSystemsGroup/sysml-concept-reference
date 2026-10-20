# SysML v2 inventory

Public research toward a source-backed inventory of the SysML v2 language: entities, relationships, properties, constraints, syntax, libraries and behavioral semantics.

The research home is [rororowyourboat/sysmlv2_inventory](https://github.com/rororowyourboat/sysmlv2_inventory). This project inventories language definitions and semantics independently of particular implementations.

## Current evidence

The seed catalogue comes from the OMG SysML 2.0 Language Specification, Part 1, `formal/2026-03-02` (March 2026), queried through the user-provided NotebookLM notebook and checked against its retrieved source text.

It contains **98 named entries** from §§8.3.6–8.3.27: 93 metaclasses, 5 enumerations, 218 declared property signatures and 365 constraint names. These are extraction counts, not a claim of complete SysML/KerML coverage or conformance.

| Resource | Contents |
|---|---|
| [Language research](docs/language-research.md) | Findings, source distinctions, behavioral scope, known uncertainties and query reproduction |
| [Machine-readable inventory](data/language-inventory.json) | Entries, property declarations, general classes, constraint names, source metadata and seven notebook query topics/hashes |
| [Research roadmap](docs/roadmap.md) | Work needed to inventory the complete language and its dependencies |

## Next milestone

Pin compatible official SysML and KerML machine-readable artifacts, then extract and reconcile the complete metamodel, including inherited properties. Standard libraries, syntax and behavior require separate coverage audits. See the roadmap for acceptance criteria.

## Working with the research

No runtime, backend or dependencies are required to read the Markdown and JSON files. The existing `nlm` CLI was used for notebook research; access to that notebook is not necessarily public. Query topics and source references are documented so the research can be revisited without publishing notebook credentials or changing its sharing settings.

Keep source facts, generated answers, interpretations, implementation choices and verification results distinct. Preserve source versions, URLs, hashes and unresolved discrepancies. Do not infer completeness from a summary or from a successful parser example.

Use ignored `sandbox/` for downloaded sources and working evidence. Do not commit credentials, authentication state, raw notebook session files or unpublished working material. Reviewed source-derived records belong in `data/`; explanatory findings and methodology belong in `docs/`.

The seed JSON parses and its counts, unique names/sections, source-backed declaration strings and local documentation links were checked during the original research. After copying, JSON structure/counts and repository documentation links were checked again. No conformance tests exist here yet.
