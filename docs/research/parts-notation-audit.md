# Parts notation audit

This note records the source-review baseline; current implementation dispositions are in the [published ledger](../parts-ports-notation-audit.md).

This audit accounts for **all eight labeled cells in Table 9 and all 18 production occurrences in §8.2.3.11**. It is a review of this source slice, not a claim that the SVG library renders every alternative, that imported grammar is fully audited, or that a SysML engine has accepted the examples. The working ledger is retained locally in [the published ledger](../../data/parts-ports-audit.json); the explicit deferrals below are part of the result.

The source is OMG *SysML 2.0 Language*, `formal/2026-03-02`, obtained through the [official language PDF](https://www.omg.org/spec/SysML/2.0/Language/PDF). The cached 3,804,140-byte file has SHA-256 `46e6c0476a6f1f34f367d57e039d56659bff75e41d2e4b3d37ca4cadea84a83a`, matching `data/source-manifest.json`. Rendered pages were inspected alongside text extraction. PDF page numbers include the 32-page front matter offset; printed numbers below are the page labels. Existing SVGs were compared as original project illustrations, rather than assumed correct because their metadata cites a production.

## Meaning and boundary of the audit

A part definition classifies structural units and is an item definition; a part usage is an item usage and may be typed by item definitions, including part definitions, or KerML structures. A part is therefore not synonymous with an arbitrary drawn rectangle. The introductory account distinguishes a composite system and its subparts from a part treated as an item in another context. Its attributes, ports, actions and states are separate language features. See [§7.11.1–7.11.2, printed 58–61, PDF 90–93](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=90).

Graphical nesting is not, by itself, proof of model ownership or composition. A compartment is a view selecting members; graphical grammar constrains containment and connectivity of the *notation*. The specification permits relocation and stretching of shapes within the layout, so exact sample pixel positions and aspect ratios are not semantic constraints. Partial productions contribute alternatives across the specification. See [§8.2.3.1, printed 193–194, PDF 225–226](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=225).

The semantic account requires a PartDefinition to specialize the library base part definition. PartUsage has a base-parts specialization and conditional subpart specialization when it is composite and owned by an item definition or usage; actor and stakeholder membership introduce further restrictions. A solid outline does not establish that these semantic conditions have been checked. See [§8.4.7, printed 408–409, PDF 440–441](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=440).

## Table 9: every labeled cell

These are **representative examples**, not an exhaustive enumeration of every prefix, alias, member combination or view. Each row below identifies the source unit in the index. References are to [Table 9, printed 58–60, PDF 90–92](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=90).

| Source unit | Visually explicit alternatives and restrictions | Current representation / deferral |
|---|---|---|
| `table-9/cell-1` — Part Definition, PDF 90 | Sharp-corner rectangle containing the kind and definition name; second form adds a separator, compartment stack and lower-left omission marks. | `part-definition` represents the minimal form. Compartment-bearing form deferred. |
| `table-9/cell-2` — Part, PDF 91 | Solid rounded rectangle containing kind and usage/type; second form adds separator, compartment stack and omission marks. | `part-usage` represents the minimal form. Compartment-bearing form deferred. |
| `table-9/cell-3` — Part with Ports, PDF 91 | Part boundary carries an elongated left-side port containing three child ports. Arrow-bearing child glyphs point inward, outward and both ways in this example; the containing port also has opposed arrows. Two independent right-side ports have no arrows. Labels have side-specific placement; the containing port label is rotated. The textual block declares the child nesting, but does not explicitly declare directions locally; do not infer an entire direction model from that text alone. | `port-glyph` is adequate only for the small undirected primitive. Nested composition, containing-port size/label, arrows and whole example deferred. See Ports grammar for interpretation. |
| `table-9/cell-4` — Part with graphical interconnection view, PDF 91 | Outer part contains two parts; host and nested-part boundary ports connect through three segments. Usage/type and port labels remain distinct. | Minimal part/port/edge primitives exist, but complete composition is deferred. The drawing puts p5 on part3 while the final text names part2.p5: preserve this source inconsistency instead of copying it into a claimed-valid model. |
| `table-9/cell-5` — Owned and separately declared performed actions, PDF 91 | One relationship has a hollow diamond at the part and leads to a perform-action node; the other is an arrow toward a separately declared action and is labeled perform. These are different cases, not interchangeable ownership drawings. | Both complete action alternatives deferred; no action/membership asset currently represents them. |
| `table-9/cell-6` — Explicit reference-subsetted performance, PDF 92 | Part relates to its perform-action usage by the hollow-diamond membership form; this usage relates to a differently named external action by the reference-subsetting line with open triangular end and dotted adornment. | Action, membership and reference-subsetting rendering deferred. |
| `table-9/cell-7` — Action-flow graphical compartment, PDF 92 | Rounded part, name separated from an italic action-flow compartment, two perform-action nodes, downward dashed open-arrow connection. The textual `then` identifies succession; the informal swim-lane description is not a new part metaclass. | Entire behavior compartment deferred. Do not substitute a solid item-flow edge for this dashed succession. |
| `table-9/cell-8` — Parts textual compartment, PDF 92 | Italic parts heading; inherited caret row; ordered/nonunique range multiplicity; redefinition by word or symbol; anonymous redefinition; subsetting by word or symbol; value assignment; ref row; name-only row; final ellipsis. | Every displayed row alternative is recorded in the working ledger. General compartment/row rendering, prefixes, alias/value/relationship formatting and omission marks deferred. |

## §8.2.3.11: every production occurrence

The section spans **PDF 240–242, printed 208–210**. The first definition begins at the end of PDF 240 and its graphic continues onto PDF 241. These page boundaries matter when attaching evidence. Sources: [PDF 240](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=240), [PDF 241](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=241), [PDF 242](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=242).

| Production occurrence (`8.2.3.11/…/1`) | Review finding and rendering status |
|---|---|
| `definition-node`, PDF 240 | Partial addition of part definition node. Minimal `part-definition` illustrates that alternative; other definition kinds are outside this unit. |
| `interconnection-element`, PDF 240 | Contributes part and referential-part alternatives. The printed operator has a separated bar after equals; retain the source spelling and index flag rather than silently normalizing it. Full interconnection composition deferred. |
| `part-def`, PDF 240–241 | Sharp rectangle: name, interconnection view, compartment stack; repeated ports may occur at all four boundaries. Existing asset only illustrates the minimal envelope. |
| `part-def-name-compartment`, PDF 241 | Definition prefix, part-definition kind, then declaration and optional aliases through the shared name production. Existing asset omits prefix alternatives and aliases. |
| `usage-node`, PDF 241 | Partial addition of part usage. Minimal `part-usage` illustrates it. |
| `part`, PDF 241 | Solid rounded envelope; same four-side port, interconnection and compartment capabilities. These capabilities are not implemented by the minimal asset. |
| `part-name-compartment`, PDF 241 | Occurrence-usage prefix, part kind, usage declaration and optional aliases. Existing composite/reference labels illustrate only basic choices. |
| `part-ref`, PDF 241 | Dashed rounded envelope with the same internal and boundary structure; `part-reference` illustrates only the minimal form. |
| `compartment`, PDF 241 | Adds parts, directed-features and interconnection compartments to the shared partial production. All three full compartment alternatives are deferred. |
| `parts-compartment`, PDF 242 | Separator with italic parts heading, followed by contents. Named compartment asset deferred. |
| `parts-compartment-contents`, PDF 242 | Zero or more part rows and optional final ellipsis. Row/omission layout deferred. |
| `parts-compartment-element`, PDF 242 | Optional `el-prefix` (`^` or `/`), occurrence-usage prefix, then shared declaration/value format. A text label slot is not a formatter for this grammar. |
| `directed-features-compartment`, PDF 242 | Separator and italic directed-features heading, then contents. Deferred. |
| `directed-features-compartment-contents`, PDF 242 | Zero or more directed rows and optional ellipsis. Deferred. |
| `directed-features-compartment-element`, PDF 242 | Prints a mandatory `el-prefix`, imported direction, and `Definition-Body-Item*`. The latter spelling differs from textual `DefinitionBodyItem`. Preserve both anomalies; exact row generation deferred pending clarification. |
| `interconnection-compartment`, PDF 242 | Separator and italic interconnection heading above a graphical interconnection view. Deferred. |
| `interconnection-view`, PDF 242 | Partial view contribution containing repeated interconnection elements, repeated dependencies/annotations and optional lower-left omission indication. Existing primitives do not exhaust this content. |
| `general-view`, PDF 242 | Partial addition of interconnection view to general views. Does not create a separate drawable part symbol. Whole-view implementation deferred. |

## Imported dependencies and interpretation limits

Names and aliases come from the definition/usage graphical grammar: definitions reuse declaration syntax, usages can carry an inherited marker, and both can show aliases. The shared compartment stack permits multiple compartments. Inheritance and derivation markers, declaration/value syntax, membership and reference-subsetting lines belong to the shared definition/usage grammar; they must not be invented from the part silhouette. See [§8.2.3.6, printed 199–201, PDF 231–233](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=231).

Definition prefixes depend on abstract/variation and extension-keyword syntax. Occurrence-usage prefixes additionally draw on basic usage flags, individual and temporal-portion syntax, and extension keywords. The shared `usage-cp` prints `usageDeclaration` rather than the textual `UsageDeclaration`; that source capitalization discrepancy is retained as a dependency ambiguity. Direction is one of in/out/inout. A complete formatter therefore needs textual productions and semantic checks beyond the local graphical rule. See [§8.2.2.6, printed 168–170, PDF 200–202](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=200) and [§8.2.2.9, printed 174–175, PDF 206–207](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=206).

Boundary-port children and side-specific labels depend on [§8.2.3.12, printed 210–213, PDF 242–245](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=242). Connections/bindings depend on [§8.2.3.13, printed 214–217, PDF 246–249](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=246). Performed actions and succession require the action grammar in [§8.2.3.17, beginning printed 222, PDF 254](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=254). Dependency/annotation elements, ellipsis and view definitions are further imports. Identifying these dependencies does not claim a full audit of their alternatives.

## Safe next additions

Add original SVGs for a part definition with a separated compartment and a rounded part usage with a separated compartment, plus reusable named parts and interconnection compartments. Show an original composed parts-and-ports example with explicit nesting, labels and attachment coordinates. These additions can address selected gaps while retaining the minimal assets and documenting which prefixes, aliases, row formats and view contents remain unsupported. The optional compartment stack and stretchable geometry permit such original layouts; matching the source's exact sample artwork is unnecessary. [§8.2.3.1 and §8.2.3.11](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=225)

No clear geometry error was found in the three existing minimal part assets: definition is sharp-corner, composite usage solid/rounded, reference usage dashed/rounded. Their editable text slots do not enforce valid SysML declarations. Broader claims that these assets implement their entire cited production would be inaccurate; existing limits need to remain visible. Action membership, reference-subsetting, directed-feature row anomalies and full behavior compartments should remain explicitly deferred until their dependencies are audited and rendered.

## Implementation reconciliation

The descriptions above record the initial source-review findings. The current [per-alternative ledger](../parts-ports-notation-audit.md) is authoritative for asset/deferral status after implementation: it includes minimal PortDefinition, selected two-row compartment nodes and direction-bearing boundary glyphs. Broader layouts and imported grammar are still deferred as recorded there. See the [connected reference](../parts-and-ports.md) and [SVG library](../svg-shapes.html).
