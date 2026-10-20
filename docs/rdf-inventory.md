# RDF concept inventory: first slice

The catalogue describes **language constructs**, rather than a user's SysML model. It is a research representation derived from official OMG XMI, with separate editorial explanations. Open the [offline concept browser](concept-browser.html) to browse it, or use the RDF and SPARQL files directly.

## What is covered

The selected slice contains 17 focus metaclasses and eight supporting ancestors: 25 class declarations, 180 directly owned properties and 218 constraint names. See the generated [extraction report](../data/rdf/extraction-report.json) for exact scope.

Four source-checked draft profiles cover PartUsage, PartDefinition, PortUsage and ConnectionUsage. Their effective property sets contain 113, 82, 111 and 121 declarations respectively. Identity-based inheritance deduplicates diamonds, excludes private inherited members, retains explicit redefinition history and reports independent same-name conflicts. Subsetting does not silently remove a declaration.

Four editorial mechanism records distinguish model ownership, namespace membership, feature context and composition/reference. Qualified relationships include conditions and source evidence; absence means unreviewed, not prohibited. The profiles add 164 property meanings, a connected source-reviewed example and representative graphical notation checked against exact official PDF pages. Original SVG redraws are illustrative, not a complete graphical grammar. See the [profile contract](concept-page-contract.md).

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

Referenced declarations outside the selected class scope are retained as `ReferenceOnly` records with names and source locations. Association-owned ends can appear this way. Those records are not fully extracted declarations, and the browser does not pretend to provide full details for them. External UML Boolean/String identities are checked against the pinned OMG UML PrimitiveTypes artifact. Supporting UML metamodel and specification evidence is recorded in the source manifest.

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
uv run --locked python scripts/build_profiles.py
uv run --locked python scripts/check_inventory.py
uv run --locked python scripts/build_browser.py
uv run --locked python -m unittest discover -s tests -v
```

The first command synchronizes the locked development tools. `--fetch` downloads only missing originals; a cached or retrieved hash mismatch fails without replacing that file or changing the manifest. The build without `--fetch` performs no network requests and requires the cached originals. Initial dependency installation can require network access. No raw originals are committed; review publisher terms before redistributing them.

Execute an individual saved query:

```bash
uv run --locked python scripts/check_inventory.py --query queries/part-properties.rq
```

Edit the query's `VALUES ?concept` to inspect a different concept. `part-properties.rq` retains all ancestor declarations, including replaced ones. `effective-properties.rq` selects active declarations; `replaced-properties.rq` exposes replacement history. The browser offers effective, declared, ancestor and replaced views with declaration origins and inheritance paths.

Catalogue IRIs now use `https://github.com/DynamicalSystemsGroup/sysml-concept-reference/`. The [namespace migration](../data/namespace-migration.json) records the exact prefix replacement; saved queries using the former prefix must be updated. This is a research identifier migration, not an assertion of OMG identity or OWL equivalence. The seed retains its historical research repository provenance.

## Evidence limits and next work

All selected generalizations and extracted property type, association, subsetting and redefinition references resolve to indexed nodes in the two hash-pinned XMI files, except the explicitly allowed external UML primitive type references. This establishes structural resolution for the selected slice, not complete compatibility of all artifacts or agreement with every PDF revision.

The SysML XMI's top-level package URI contains `https://ww.omg.org/...`, while its official retrieval URL uses `www.omg.org`. The manifest preserves that observed spelling. Do not use that typo to construct download URLs or silently rewrite provenance.

Bounds and defaults retain raw XMI encodings beside UML-normalized values and evidence. Absent bound nodes normalize to 1; present numeric literals with omitted values normalize to 0; unlimited upper bounds retain `*`. An absent default node means no declared default. Unsupported expressions remain unsupported: the selected slice includes a `Membership.visibility` InstanceValue outside the four profiles. Qualifier normalization is separate from raw explicit attributes. `Feature::isComposite` must not be confused with an XMI property's `aggregation`.

Not yet implemented: complete metamodel extraction; operations and constraint evaluation; standard libraries; complete syntax/notation mappings; reconciliation of every seed record; model validation or execution. The four-profile reconciliation checks selected structural fields only. SHACL validates catalogue integrity, not SysML conformance. OWL describes catalogue vocabulary rather than executable SysML semantics.

Tests cover provenance, normalization, identity-based inheritance, missing evidence, stale effective sets, reconciliation discrepancies, browser interactions and published links. Source-dependent tests explicitly skip if originals are missing. The Node browser smoke check executes the generated application against a DOM test double; it is not a visual layout test.
