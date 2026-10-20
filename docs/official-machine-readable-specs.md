# Official machine-readable specification sources

Research date: 2026-10-20. Recommendation: build the metamodel inventory from **both KerML and SysML MOF XMI**, use their JSON schemas to audit serialized property coverage, and inventory the normative library archives separately. This is an extraction recommendation, not a completed extraction.

## Version baseline

OMG lists **KerML 1.0** and **SysML 2.0** as formal versions adopted in September 2025. Their current landing pages reference March 2026 PDF document IDs, while the machine-readable artifact paths remain dated `20250201`. Treat adoption date, PDF revision, artifact path, embedded namespace and downloaded content hash as separate provenance fields; a path date does not identify a PDF revision. Sources: [KerML release page](https://www.omg.org/spec/KerML/1.0), [SysML release page](https://www.omg.org/spec/SysML/2.0), [current SysML PDF cover](https://www.omg.org/spec/SysML/2.0/Language/PDF).

These are candidate sources for a compatible baseline. Their joint listing and release labels do not establish that every external reference resolves or that the artifacts fully match the current PDF revisions; verify those points during acquisition.

## Primary metamodel artifacts

These artifacts appear under **Normative Machine Readable Documents** on the corresponding OMG release pages.

| Artifact | Official URL | Inventory role |
|---|---|---|
| KerML abstract syntax, MOF XMI | [KerML.xmi](https://www.omg.org/spec/KerML/20250201/KerML.xmi) | KerML declarations and metamodel relationships |
| SysML abstract syntax, MOF XMI | [SysML.xmi](https://www.omg.org/spec/SysML/20250201/SysML.xmi) | SysML declarations and their references to foundations |
| KerML abstract-syntax JSON schema | [KerML.json](https://www.omg.org/spec/KerML/20250201/KerML.json) | Cross-check JSON representation |
| SysML abstract-syntax JSON schema | [SysML.json](https://www.omg.org/spec/SysML/20250201/SysML.json) | Cross-check JSON representation |
| Project metadata JSON schema | [KerML-Model-Interchange.json](https://www.omg.org/spec/KerML/20250201/KerML-Model-Interchange.json) | Archive/project metadata, not language concepts |

The [KerML specification](https://www.omg.org/spec/KerML/1.0/PDF), §8.3.1, defines abstract syntax using a CMOF-conformant UML model. Clause 2 gives machine-readable files precedence over conflicting PDF content. Clause 10 distinguishes metamodel-based interchange from textual notation. Thus XMI is the proposed structural source of truth; the PDFs remain needed for grammar and explanatory semantics.

The browsed [SysML JSON schema](https://www.omg.org/spec/SysML/20250201/SysML.json) declares JSON Schema draft 2020-12 and a `$defs` catalogue. Its `AcceptActionUsage` definition includes fields such as `declaredName`, `aliasIds` and `actionDefinition`; references often target `Identified`, with the intended metaclass recorded in `$comment`. Do not interpret every `$defs` entry as a language metaclass or infer declaration ownership from a field's presence.

KerML §10.4.5 specifies inclusion of owned and inherited properties, plus differently named redefined properties, in JSON serialization. This flattening makes JSON useful for field coverage but insufficient by itself to reconstruct which class declared a property. [KerML interchange clauses](https://www.omg.org/spec/KerML/1.0/PDF).

The project metadata schema also demonstrates why provenance needs multiple fields: its `Project` `$id` uses `/20240201/`, although the published artifact URL uses `/20250201/`. Preserve the observed value; do not silently normalize it. [Metadata schema](https://www.omg.org/spec/KerML/20250201/KerML-Model-Interchange.json).

## Normative library sources

These are separate models, rather than additional abstract-syntax metaclasses. OMG lists each archive as normative on the [KerML](https://www.omg.org/spec/KerML/1.0) or [SysML](https://www.omg.org/spec/SysML/2.0) release page.

| Language | Official archive |
|---|---|
| KerML | [Semantic Library](https://www.omg.org/spec/KerML/20250201/Semantic-Library.kpar) |
| KerML | [Data Type Library](https://www.omg.org/spec/KerML/20250201/Data-Type-Library.kpar) |
| KerML | [Function Library](https://www.omg.org/spec/KerML/20250201/Function-Library.kpar) |
| SysML | [Systems Library](https://www.omg.org/spec/SysML/20250201/Systems-Library.kpar) |
| SysML | [Analysis Domain Library](https://www.omg.org/spec/SysML/20250201/Analysis-Domain-Library.kpar) |
| SysML | [Cause and Effect Domain Library](https://www.omg.org/spec/SysML/20250201/Cause-and-Effect-Domain-Library.kpar) |
| SysML | [Geometry Domain Library](https://www.omg.org/spec/SysML/20250201/Geometry-Domain-Library.kpar) |
| SysML | [Metadata Domain Library](https://www.omg.org/spec/SysML/20250201/Metadata-Domain-Library.kpar) |
| SysML | [Quantities and Units Domain Library](https://www.omg.org/spec/SysML/20250201/Quantities-and-Units-Domain-Library.kpar) |
| SysML | [Requirement Derivation Domain Library](https://www.omg.org/spec/SysML/20250201/Requirement-Derivation-Domain-Library.kpar) |

KerML §§10.2–10.3 define KPAR as a ZIP project archive, with top-level `.project.json` and `.meta.json` and model files using textual notation, JSON or XMI. The archive extension alone does not prove its members use textual notation; inspect actual members before choosing a parser. KerML textual model files use `.kerml`. [KerML project interchange](https://www.omg.org/spec/KerML/1.0/PDF).

OMG also lists a normative [SysML v1-to-v2 transformation XMI](https://www.omg.org/spec/SysML/20250201/SysMLv1Tov2.xmi), and an informative [Simple Vehicle example](https://www.omg.org/spec/SysML/2.0). Neither should be merged into the core metaclass inventory. Transformation coverage and examples can be tracked separately.

## Proposed extraction and reconciliation

1. Pin the official artifacts in a source manifest with URL, release, OMG document ID, retrieval date, byte hash, embedded namespaces and licensing reference. Resolve external XMI references explicitly and retain unresolved references as failures.
2. Extract packages, classes, abstract flags, generalizations, enumerations/literals, directly declared properties, types, multiplicities, ownership/composition, ordering/uniqueness, derivation, read-only flags, subsets/redefinitions, operations and constraints wherever represented. Record unavailable information explicitly rather than inventing defaults from PDF summaries.
3. Compute inherited properties as a separate view, retaining declaration owner and redefinition/subsetting provenance. Compare serialization fields against JSON schemas, excluding schema helper definitions from metaclass counts.
4. Reconcile the existing [PDF-derived catalogue](../data/language-inventory.json) by exact qualified name, language and kind. Report additions, missing entries and differing signatures with evidence; preserve its section citations as a useful cross-reference.
5. Inventory library declarations independently, retaining qualified names, library versions, dependencies, typing/specialization and source locations. Link semantic targets back to metamodel concepts without counting library types as metaclasses.
6. Maintain separate coverage for grammar, graphical notation, semantic rules, constraint bodies and executable behavior. A catalogue of names or schema fields does not establish these dimensions or conformance.

## Verification limits

This research inspected OMG release listings, relevant KerML PDF clauses, the opening SysML JSON-schema definition and project metadata schema. The browser rejected XMI with an unsupported `application/xml` content type; KerML JSON retrieval timed out. No complete XMI parse, library archive inspection, byte-level download, hash calculation, cross-artifact validation or new inventory count was performed. Artifact URLs are verified as official release listings; their complete contents still require local acquisition and validation.

## Subsequent focused implementation

After this web research, the two official XMI files were downloaded locally and hash-pinned in the [source manifest](../data/source-manifest.json). A [focused RDF slice](rdf-inventory.md) now validates selected cross-file references and extracts selected declarations. The research limits above describe the earlier web-only investigation; the implementation guide records the additional checks and remaining gaps. Library archives and the complete language baseline remain unvalidated.
