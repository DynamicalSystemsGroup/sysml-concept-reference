# Complete SysML v2 inventory roadmap

## Objective and boundaries

Build a traceable inventory of SysML v2 and the KerML foundations and standard libraries it requires. Keep source definitions, research interpretations and implementation support claims distinct.

“Whole language” requires several distinct coverage dimensions: metamodel, inherited properties, constraints/derivations, concrete syntax, model libraries and behavioral semantics. The Systems Modeling API and Services specification is an adjacent interoperability track, not an implicit part of the language catalogue.

## Starting point

The [seed catalogue](../data/language-inventory.json) indexes dedicated SysML abstract-syntax subsections from the March 2026 Language PDF. It does not expand the full KerML metamodel, all operations/OCL bodies, grammar productions or library declarations. See [research findings](language-research.md) for provenance and generated-answer corrections.

## Work sequence

| Step | Work | Acceptance evidence |
|---|---|---|
| 1. Pin sources | Identify compatible official SysML/KerML specifications, metamodel artifacts, grammars and libraries | Manifest with publisher, version, release/commit identity, retrieval URL, hash and compatibility evidence; unresolved compatibility marked explicitly |
| 2. Extract metamodel | Capture classes/enums, generalizations, declared properties, associations, types, multiplicities, defaults, qualifiers, operations and constraints | Repeatable extraction with origin locations; compare against seed catalogue and official artifact counts |
| 3. Resolve inheritance | Build effective per-class records while retaining each declaration’s origin | Diamond inheritance, redefinitions/subsets and derived properties represented without silent flattening; unresolved references reported |
| 4. Inventory libraries | Catalogue packages, definitions/usages, functions, units and semantic specialization targets | Library symbols linked to pinned source and resolvable dependencies; library elements distinct from metaclasses |
| 5. Cross-reference syntax | Connect textual productions, keywords and graphical notation to semantic constructs | Coverage matrix of productions/notations and metamodel targets; shorthand and implied relationships identified |
| 6. Capture semantics | Index derivations, well-formedness and semantic constraints, implicit relationships and behavioral rules | Section/artifact references, affected kinds and required evaluator capabilities; no implied execution claim |
| 7. Audit completeness | Reconcile artifacts, specification sections, extraction counts and representative models | Coverage report listing matched, absent, unsupported, ambiguous and disputed entries; no unexplained omissions |
| 8. Publish traceability | Connect metamodel, syntax, libraries and semantic rules | Each record links to its authoritative source and related records; coverage gaps remain explicit |

Steps 1–3 have a [focused RDF implementation](rdf-inventory.md): 17 focus classes and eight ancestors, normalized UML bounds/defaults, effective inheritance and preserved redefinition history. Four profiles reconcile selected fields against the seed, explain every active property and connect source-reviewed examples to qualified relationships and verified representative notation. Supporting UML and SysML evidence is hash-pinned. This completes the bounded four-concept milestone, rather than whole-language coverage.

Next, extend the same contract to additional concepts, record engine execution evidence for the connected example, then audit operations, constraint bodies, grammar and standard libraries. Track each coverage dimension separately and preserve unresolved cases.

## Record design

Every inventory record should carry a stable research ID, kind, qualified name, source identity/location, declaration status and review status. Metamodel records additionally need bases, declared/effective properties, relationship roles, constraints and derivations. Keep original declaration text beside normalized fields until normalization has been checked.

Use separate records for syntax productions, graphical notation, library symbols, semantic rules and test examples. Link them rather than mixing them into one table of “components”. Separate model ownership, feature composition, name visibility/import, runtime occurrences and diagram presentation.

A coverage result is not an approval or a conformance result. NotebookLM answers are generated research leads, not normative declarations. Use targeted notebook questions to explain discrepancies; use official source artifacts and reconciliation to establish coverage.

## Audit examples

Check inherited/redefined features, reference versus composite parts, aliases/imports, multiplicities and units, conjugated ports, multi-ended connections, branching/concurrent actions, guarded transitions, requirement satisfaction, verification memberships, metadata and filtered views. Preserve unsupported constructs and unresolved references explicitly.

Examples proposed here are not executed tests. Add actual expected/observed evidence only when a concrete artifact or implementation has been run.

## Publication and verification

Keep reviewed research and reproducible extraction inputs/configuration public where redistribution permits. Keep credentials and local sessions out of Git. Record provenance before incorporating external material. No notebook sharing changes, remote publication, commits or pushes are implied by this plan.

## Graphical coverage baseline

The [notation dashboard](notation-coverage.md) and [source register](notation-register.md) now index all 27 §8.2.3 subsections and all 26 Clause 7 tables: 639 production occurrences and 192 labeled source cells. Six representative records are reconciled to this baseline; shared conventions and the next review batches are recorded. This completes the source-register baseline, not the subsequent full graphical-alternative audit or illustration programme.
