# RDF concept inventory: first slice

The catalogue describes **language constructs**, rather than a user's SysML model. It is a research representation derived from official OMG XMI, with separate editorial explanations. Open the [offline concept browser](concept-browser.html) to browse it, or use the RDF and SPARQL files directly.

## What is covered

The focus is 15 metaclasses: KerML `Element`, `Relationship`, `Namespace`, `Membership`, `OwningMembership`, `Type`, `Classifier`, `FeatureMembership`, `Feature`, `TypeFeaturing`; SysML `Definition`, `Usage`, `ReferenceUsage`, `PartDefinition`, `PartUsage`.

Their complete superclass ancestry adds six support metaclasses: `Class`, `Structure`, `ItemDefinition`, `ItemUsage`, `OccurrenceDefinition`, `OccurrenceUsage`. For these 21 declarations, the extractor captures 172 directly owned attributes and 200 directly owned constraint names. These are counts for this selected slice, not the whole metamodel. See the generated [extraction report](../data/rdf/extraction-report.json).

Four editorial mechanism records explain model ownership, namespace membership, feature context, and composition/reference. Ten qualified application records link explanations and restrictions to specific source locations. These are curated explanations, not a complete table of permitted concept combinations. Absence of an application record means unreviewed, not prohibited. The browser also shows explanations attached to ancestors, identifying their origin; inheritance does not establish every context-specific permission.

Graphical shape, compartments, edge notation and nesting remain **not yet verified**. A single universal shape per metaclass would be an unsafe assumption. The browser links to SysML §8.2.3 as the next source to inspect. No notation has been invented.

## Files and representation

| File | Purpose |
|---|---|
| [Source manifest](../data/source-manifest.json) | Official URLs, releases, retrieval date, byte lengths, SHA-256 hashes and observed package URIs |
| [Vocabulary](../data/rdf/vocabulary.ttl) | Classes and predicates for the research catalogue |
| [Metamodel slice](../data/rdf/metamodel.ttl) | Generated source-derived records; do not hand-edit |
| [Mechanisms](../data/rdf/mechanisms.ttl) | Curated explanations and qualified applications with evidence |
| [SHACL shapes](../data/rdf/shapes.ttl) | Validation of catalogue records and links |
| [SPARQL queries](../queries/) | Concepts, ancestry declarations, mechanisms and coverage gaps |
| [Browser generator](../scripts/build_browser.py) | RDF-to-HTML build; output works without a server or network |

A metaclass is an individual of `inv:MetaclassRecord`; a property declaration has its own IRI, declaring class, type, qualifier encodings, subset/redefinition links and source locator. `inv:specializes` records a direct XMI generalization between catalogue records. It is deliberately distinct from `rdfs:subClassOf` between classes of user model elements.

The vocabulary uses OWL classes and properties to describe catalogue records. There is no OWL translation of SysML semantics and no OWL reasoning step. SHACL checks our inventory's integrity, not SysML model conformance. OWL's reasoning model and SHACL's validation model serve different purposes: see the [OWL primer](https://www.w3.org/TR/owl2-primer/) and [SHACL specification](https://www.w3.org/TR/shacl/). [SPARQL property paths](https://www.w3.org/TR/sparql11-query/#propertypaths) support ancestor traversal without materializing all inherited declarations.

IRIs under this repository's GitHub URL identify research records and vocabulary terms. They are not OMG identifiers or promises of individually hosted pages. Source-artifact IRIs include the byte hash, and source declarations link directly to the official XMI URL with its `xmi:id` fragment. Source locators remain usable even if a browser downloads rather than displays an XMI link. Plain-language descriptions are marked `EditorialSummary`; structural records are marked `Extracted`.

Referenced declarations outside the selected class scope are retained as `ReferenceOnly` records with names and source locations. Association-owned ends can appear this way. Those records are not fully extracted declarations, and the browser does not pretend to provide full details for them. External UML Boolean/String references are explicitly marked unverified; their definitions have not been downloaded.

## Reproduce and explore

Python 3.11+ and `uv` are required for local builds and checks. `rdflib` and `pyshacl` are pinned **development tools**, with no production dependencies or service. Read the HTML, Turtle and JSON without installing anything.

Select the correct context using the machine's existing helper before environment changes or remote retrieval. For this workspace:

```bash
source ~/.config/direnv/direnvrc
use_dsg
ctxcheck
git status --short
```

If context, identity, SSH agent or remote alias does not match, stop before fetching. No `direnv allow` is needed or run by these scripts.

Fetch missing official XMI into ignored `sandbox/official-sources/`, verify the committed hashes and build:

```bash
uv sync --locked
uv run --locked python scripts/build_inventory.py --fetch
uv run --locked python scripts/check_inventory.py
uv run --locked python scripts/build_browser.py
uv run --locked python -m unittest discover -s tests -v
```

The first command synchronizes the locked development tools. `--fetch` downloads only missing originals; a cached or retrieved hash mismatch fails without replacing that file or changing the manifest. The build without `--fetch` performs no network requests and requires the cached originals. Initial dependency installation can require network access. No raw originals are committed; review publisher terms before redistributing them.

Execute an individual saved query:

```bash
uv run --locked python scripts/check_inventory.py --query queries/part-properties.rq
```

Edit the query's `VALUES ?concept` to inspect a different concept. `part-properties.rq` returns directly declared and ancestor declarations **including redefined ones**. It is not an effective-property calculation. The browser offers the same distinction through its ancestor checkbox. It preserves the declaring class rather than copying a property onto each descendant.

## Evidence limits and next work

All selected generalizations and extracted property type, association, subsetting and redefinition references resolve to indexed nodes in the two hash-pinned XMI files, except the explicitly allowed external UML primitive type references. This establishes structural resolution for the selected slice, not complete compatibility of all artifacts or agreement with every PDF revision.

The SysML XMI's top-level package URI contains `https://ww.omg.org/...`, while its official retrieval URL uses `www.omg.org`. The manifest preserves that observed spelling. Do not use that typo to construct download URLs or silently rewrite provenance.

Bounds and defaults preserve their XMI representation as JSON literals: `present`, literal `type`, and explicit `value` where available. Missing nodes and omitted literal values have different encodings. UML defaults are **not expanded**. Explicit qualifier attributes are retained; absence of a qualifier must not be interpreted as false. `Feature::isComposite` is a language property declaration; an XMI property's `aggregation` describes the metamodel declaration and must not be conflated with it.

Not yet implemented: complete metamodel extraction; computed effective properties with diamond/redefinition handling; constraint bodies, operations or evaluation; standard libraries; syntax-to-semantics mappings; graphical notation; reconciliation against every seed record; model validation or execution. The next bounded extension is to normalize bounds/defaults against pinned UML definitions and audit notation for `PartUsage`, while preserving source encodings and context restrictions.

Tests exercise missing provenance, dangling types, invalid applicability, declaration-origin retention, source hash mismatch, unresolved references, ambiguous focus selection and all curated evidence IDs. Source-dependent tests explicitly skip if originals are missing. No test result establishes language conformance.
