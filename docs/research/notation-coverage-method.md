# Graphical notation coverage: scope and counting method

Research date: 2026-10-21. Source: [OMG SysML 2.0 Part 1, Language](https://www.omg.org/spec/SysML/2.0/Language/PDF), formal/2026-03-02 (March 2026). This investigation used the hash-pinned local PDF and Poppler text in `sandbox/official-sources/`; the live official URL was also checked for document identity. PDF page numbers below are one-based viewer pages. Source identity and SHA-256 are recorded in the [source manifest](../../data/source-manifest.json).

## The denominator needs more than tables

**The specification has 27 graphical-notation subsections, not 27 graphical-notation tables.** The normative graphical grammar is §8.2.3, printed pages 193–255, [PDF pages 225–287](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=225). It includes shared rules, textual productions, graphical productions, alternatives, optional components and partial productions extended elsewhere. A list of shapes, a metaclass list, and a count of representative table rows are therefore different inventories.

The list of tables ([PDF page 28](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=28), printed xviii) identifies **26 Clause 7 tables** to screen. Of these, **24** have titles identifying representative notation (Tables 1–15, 17–24 and 26); Table 16 describes control nodes and Table 25 gives diagram examples. Table 30 defines the graphical BNF conventions. Table 34 records standard views and their default rendering compartments. The table count is verified from the list of tables; this note does not claim a verified total of their rows or visual alternatives.

Do not dismiss Clause 7 notation solely because its table captions say representative. §6.2 distinguishes informative overviews from normative notation subclauses. The selected row and its surrounding prose need their actual context recorded. See [§6.2, PDF page 44](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=44).

## Source layers to index

| Layer | Source boundary | Counting unit |
|---|---|---|
| Representative presentations | Clause 7 Tables 1–26, including control-node and diagram-example tables | Original source row, with continuation rows explicitly joined |
| Graphical grammar | §8.2.3.1–§8.2.3.27 | Production occurrence, grouped by production symbol; alternatives recorded separately |
| General conventions | §8.2.3.1–§8.2.3.2 and conventions reused elsewhere | Reusable rule, with consumers linked |
| Text printed inside graphics | Referenced productions in §8.2.2 | Dependency on a textual production; do not count every text token as another graphical symbol |
| Valid view contents | §9.2.20.1 Table 34 and standard-view definitions | View definition and rendering/filter dependency |
| Meaning and restrictions | Relevant Clause 7 prose, abstract syntax, semantics and cited KerML rules | Applicability or semantic dependency, with separate evidence |

The following are verified section starts, not inferred section end pages. Several sections begin on a page shared with the preceding section.

| §8.2.3 subsection | Topic | Printed start | PDF start |
|---|---|---:|---:|
| 1 | Overview | 193 | 225 |
| 2 | Elements and relationships | 194 | 226 |
| 3 | Dependencies | 195 | 227 |
| 4 | Annotations | 195 | 227 |
| 5 | Namespaces and packages | 197 | 229 |
| 6 | Definitions and usages | 199 | 231 |
| 7 | Attributes | 201 | 233 |
| 8 | Enumerations | 202 | 234 |
| 9 | Occurrences | 203 | 235 |
| 10 | Items | 207 | 239 |
| 11 | Parts | 208 | 240 |
| 12 | Ports | 210 | 242 |
| 13 | Connections | 214 | 246 |
| 14 | Interfaces | 217 | 249 |
| 15 | Allocations | 218 | 250 |
| 16 | Flows | 219 | 251 |
| 17 | Actions | 222 | 254 |
| 18 | States | 232 | 264 |
| 19 | Calculations | 236 | 268 |
| 20 | Constraints | 238 | 270 |
| 21 | Requirements | 240 | 272 |
| 22 | Cases | 246 | 278 |
| 23 | Analysis cases | 246 | 278 |
| 24 | Verification cases | 248 | 280 |
| 25 | Use cases | 249 | 281 |
| 26 | Views and viewpoints | 251 | 283 |
| 27 | Metadata | 255 | 287 |

## Grammar-production label index

An anchored scan of names followed by `=` or `=|` initially detected 620 occurrences and 523 names. A broader source audit found **19 additional occurrences using `|=`**, including visible examples on [PDF page 248](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=248). The register therefore retains **639 declaration occurrences under 523 names**: 523 with `=`, 97 with `=|`, and 19 with `|=`. Five of the `=` occurrences have a space-separated following bar. The reversed and spaced operators are flagged, not silently normalized to a grammar operator.

The reproducible extraction checks label, operator, section and PDF page agreement between Poppler layout and raw modes. It also indexes **192 labeled first-column cells** from the explicit source grid geometry across the 26 tables: 182 representative-notation cells, four control-node dependency cells and six diagram-example cells. Column headers are excluded. Equal labels remain distinct and no continuation cells are joined by inference. This is a labeled-cell count, not a count of unique graphical alternatives. Source grid bounds are retained for review.

The [source register](../notation-register.md) and [coverage dashboard](../notation-coverage.md) expose these units and their representative mappings. Purely textual helper productions count as production occurrences. Graphical right-hand sides, optional symbols and every visual alternative cannot be recovered reliably from plain text and remain a separate review obligation. This index is not a complete rendering specification.

## Rules that affect appearance and composition

The [overview and Table 30, PDF pages 225–226](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=225) establish that graphical grammar primarily constrains containment and connectivity; it generally permits relocation and stretching of elements. Connecting lines may use straight or curved segments and optional line-jump symbols. Accordingly, examples should distinguish required geometry or attachment rules from incidental layout choices.

A compartment is itself a view of selected contents. Textual and graphical compartments use different renderings. Nesting in an illustration is therefore insufficient evidence for a model ownership assertion. Record the graphical containment rule and semantic ownership relation independently.

Partial productions can gain alternatives in later sections. A production-name index must retain every occurrence rather than keeping only its first definition. The distinction between complete and partial productions comes from Table 30 and its following explanation. Mixed-case references import textual grammar, whereas graphical-production names use lowercase and hyphens.

[Table 34 and §9.2.20.1, PDF pages 545–546](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=545) connect standard views to their default compartments. These are a separate coverage obligation; a symbol catalogue alone does not establish valid diagram contents. The note in §8.2.3.26 points to §9.2.18, while the overview and actual standard-view package identify §9.2.20. Preserve that source discrepancy rather than reproducing the former reference as an unquestioned destination.

## KerML boundary

SysML extends the KerML abstract syntax and semantics; [§6.2](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=44) explicitly places the Kernel details in the [KerML specification](https://www.omg.org/spec/KerML/1.0). This does **not** establish a second implied graphical-symbol catalogue to append wholesale. Start with the SysML graphical grammar, follow imported textual productions and semantic references, and retain KerML dependencies as dependencies until their exact clauses are examined.

A text search of the complete §8.2.3 body found two explicit KerML mentions concerning the `SemanticMetadata` metaclass. This is a search finding, not proof that there are only two effective KerML dependencies: imported textual productions and semantic concepts can introduce additional references transitively. A complete dependency audit remains necessary before claiming combined SysML/KerML coverage.

## Proposed record and status policy

Use stable source-row and production-occurrence identifiers independently from curated notation identifiers. Link a curated notation to every supporting row, grammar occurrence and restriction. Store geometry, line style, label grammar, compartments, attachment points, contextual conditions, alternatives, and represented concepts as separate fields. A composite illustration may demonstrate several records without turning those records into one denominator item.

Track indexing, description, illustration and source checking separately. An indexed table row does not imply its visual alternatives are described; an SVG does not imply all source conditions have been checked. Preserve unresolved segmentation and mapping decisions explicitly. Report table-row coverage, grammar-occurrence coverage and curated-variant coverage separately.

The existing eight profile notation records are a starting set to reconcile, not an exhaustive denominator. Their SVG files may bundle multiple forms. Exact remaining counts require source-row segmentation, grammar indexing and review of each existing mapping. SHACL can verify required evidence fields and SPARQL can report recorded coverage; neither establishes the correctness of an unreviewed drawing or tool conformance. [Clause 2, PDF page 35](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=35) also requires textual support sufficient to render graphical text for graphical-notation conformance.

## Verification limits

This note verifies section boundaries, source layers and table counts from the pinned extracted text. It does not claim a visual audit of every table row, every BNF alternative, or an exhaustive count of distinct symbols. Existing visually checked evidence is documented separately in [notation evidence](notation-evidence.md). Drawings should be original illustrative redraws with precise source citations; source-reviewed textual examples must remain distinguished from executed examples.
