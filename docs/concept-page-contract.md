# Concept-page contract

Contract version 1. The first implementation covers [PartUsage](concepts/part-usage.md), [PartDefinition](concepts/part-definition.md), [PortUsage](concepts/port-usage.md) and [ConnectionUsage](concepts/connection-usage.md). These are source-checked drafts for review, not user-approved or normative interpretations.

## Required content

| Field | What it must explain | Evidence and representation |
|---|---|---|
| Identity and kind | Language, metaclass identity, qualified name and direct bases | Original XMI location and hash-pinned artifact |
| Meaning | What the concept represents, with important distinctions | Editorial explanation linked to official clauses |
| Properties | Meaning, type, metamodel bounds, declared defaults and independent qualifiers | Property declaration identity, normalized values, raw encodings and UML normalization rules |
| Inheritance | Direct declarations, active inherited declarations and replaced declarations | Identity-based resolution, origin and alternative inheritance paths; collisions remain explicit |
| Composability and relationships | Specific examples of ownership, featuring, typing, nesting and endpoint references | Qualified relationship records with conditions and evidence; no universal allowed-pair matrix |
| Example | A small connected model and an explanation of the relevant declarations | Original example with source-review status; parser validation and execution are separate statuses |
| Graphical notation | Shape, labels, edge/node variants, compartments and context restrictions where checked | Exact official section, printed page and one-based PDF page; original redraws labeled separately |
| Reconciliation | Comparison with the existing seed catalogue | Explicit field-level checks and discrepancies, without rewriting the seed |
| Limits | Unsupported rules, incomplete notation coverage and unresolved questions | Visible caveats, never omitted or converted into false defaults |

## Three different kinds of default

1. **Serialization defaults:** an omitted attribute in the XMI may receive a value from UML. A missing bound node means 1, while a present numeric literal with omitted value means 0.
2. **Declared metamodel defaults:** a property's explicit default specification is decoded while preserving its literal kind. No default specification means no declared default. It does not imply false or zero.
3. **SysML modeling defaults:** usage multiplicity, composition and other contextual semantics follow SysML rules, including specialization and ownership context. They are not obtained by copying the metamodel's bounds onto modeled values.

The [property-rule evidence](research/property-rules.md) documents the exact source rules, including the distinction between an absent String literal value and an explicitly empty string. Derived properties still require derivation evaluation; the catalogue does not compute their runtime values.

## Inheritance policy

Resolve declaration identities through the selected complete superclass closure. Deduplicate the same identity reached along diamond paths. Filter private inherited declarations and replace explicitly redefined declarations in the appropriate class context. Retain replaced declarations and their replacements, and preserve alternative paths to each origin.

Same-name declarations are not automatically the same property. Unresolved competing names remain visible and are reported as conflicts. This is a bounded declaration-resolution view, not a full UML conformance engine. The source's apparent `Property::isConsistentWith` OCL defect is documented rather than silently corrected and claimed as executed.

## Graphical and example evidence

Representative variants have been checked against rendered official pages; graphical grammar declarations are now indexed in the [source register](notation-register.md), while complete graphical alternatives remain unaudited. A concept may have several valid representations. Visual nesting is not converted automatically into a semantic ownership or composition statement.

Illustrations in `docs/assets/notation/` are original vector redraws based on the cited syntax. They are not copied official figures. The shared [assembly example](../data/examples/assembly.sysml) is source-reviewed but has not been run through a SysML parser or semantic engine.

## Implementation and validation

- [Profile records](../data/concept-profiles.json) are the curated inputs for examples, qualified relationships and notation evidence.
- [Property explanations](../data/property-explanations.json) contain original editorial paraphrases of source-backed meanings.
- [Profile RDF](../data/rdf/profiles.ttl) exposes the contract as queryable graph records.
- [Seed reconciliation](../data/profile-reconciliation.json) reports the exact selected checks and their results.
- [SHACL shapes](../data/rdf/shapes.ttl) require source locations, conditions, status and linked concepts; they validate catalogue structure rather than SysML models.

Rebuild the normalized metamodel from the hash-pinned originals, then generate profiles, browser and site:

```bash
uv run --locked python scripts/build_inventory.py --fetch
uv run --locked python scripts/build_profiles.py
uv run --locked python scripts/build_notation.py
uv run --locked python scripts/check_inventory.py
uv run --locked python scripts/build_browser.py
uv run --locked python -m unittest discover -s tests -v
uv run --locked python scripts/build_site.py
```

Use the correct development context and run `ctxcheck` plus `git status` before downloading sources, changing dependencies or performing Git operations. Raw originals remain ignored. No commit, push or deployment is implied by building these drafts.
