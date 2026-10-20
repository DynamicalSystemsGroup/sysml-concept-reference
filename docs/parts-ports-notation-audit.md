# Parts and ports notation audit

All eight Table 9 cells, four Table 10 cells and the 18 parts / 20 ports graphical-production occurrences. Every selected local alternative has a representative asset, a partial match with explicit limits, or a documented deferral. This is not whole-language coverage or renderer conformance.

**12 source cells and 38 production occurrences reviewed.** The 106 alternative records are source-local bookkeeping entries, not unique symbols or required SVG counts.

## What reviewed means

Visually inspected pinned source pages alongside text extraction. LocalAlternativesAudited means that the explicit forms in the selected source unit, imported dependencies and source issues have been recorded and assigned a rendering disposition. It does not mean all dependency productions, model combinations or rendering cases are implemented. Source-cell and production counts stay separate.

Every selected unit has a visual review, identified local forms, source pages, and an explicit rendering disposition. Imported grammar and arbitrary prefix combinations are separate dependencies; recording a deferral does not implement them. An asset match is limited to its stated representation scope. Source inconsistencies remain visible.

Rendering dispositions: **23 representative asset records**, **26 partially rendered records**, **57 deferred records**. 6 units record source issues.

[Concept reference](parts-and-ports.md) · [Coverage dashboard](notation-coverage.md) · [Machine-readable ledger](../data/parts-ports-audit.json) · [SPARQL alternatives query](../queries/notation-alternatives.rq)

## Parts

### table-9/cell-1

Source: [PDF 90 / printed 58](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=90).

Dependencies: `compartment-stack`, `part-def`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| minimal-definition | sharp rectangle; solid; part def keyword and definition name | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [part-definition](../shapes/svg/part-definition.svg) — Only the minimal geometry and example label described here; each asset retains its own limitations. |
| definition-with-compartments | sharp rectangle with horizontal separator, compartment stack and lower-left ellipsis; solid; Labels and member selection follow the imported productions; generalized formatting is deferred. | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [part-definition-parts](../shapes/svg/part-definition-parts.svg) — Only the named component geometry and shown example text; no model or generalized grammar validation. / Deferred: Only the named parts compartment is supplied; arbitrary compartment stacks, boundary ports and interconnection contents remain deferred. |

### table-9/cell-2

Source: [PDF 91 / printed 59](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=91).

Dependencies: `compartment-stack`, `part`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| minimal-usage | rounded rectangle; solid; part keyword and usage : definition | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [part-usage](../shapes/svg/part-usage.svg) — Only the minimal geometry and example label described here; each asset retains its own limitations. |
| usage-with-compartments | rounded rectangle with horizontal separator and lower-left ellipsis; solid; Labels and member selection follow the imported productions; generalized formatting is deferred. | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [part-usage-parts](../shapes/svg/part-usage-parts.svg) — Only the named component geometry and shown example text; no model or generalized grammar validation. / Deferred: Only a two-row parts compartment is supplied; other compartments, nesting and boundary composition remain deferred. |

### table-9/cell-3

Source: [PDF 91 / printed 59](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=91).

Dependencies: `8.2.3.12/port-l/1`, `8.2.3.12/port-r/1`, `port-name-compartment`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| nested-boundary-ports | rounded part boundary, elongated rounded p0 port containing three smaller boundary ports; two independent right-edge ports; solid; p0 label rotated; child labels outside left; undirected labels inside right | p0 contains p1/p2/p3; p4/p5 are siblings | Deferred: Requires nested-port composition and directed port glyph variants. |
| incoming-child-port | small rounded square with right-pointing arrow; solid; p1 : PortDef1 | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [port-arrow-right](../shapes/svg/port-arrow-right.svg) — Only the named component geometry and shown example text; no model or generalized grammar validation. / Deferred: Arrow-bearing child geometry only; elongated containing port, nested placement and direction-selection semantics remain deferred. |
| outgoing-child-port | small rounded square with left-pointing arrow; solid; p2 : PortDef2 | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [port-arrow-left](../shapes/svg/port-arrow-left.svg) — Only the named component geometry and shown example text; no model or generalized grammar validation. / Deferred: Arrow-bearing child geometry only; elongated containing port, nested placement and direction-selection semantics remain deferred. |
| bidirectional-ports | elongated p0 and small p3 glyph contain opposed arrows; solid; Labels and member selection follow the imported productions; generalized formatting is deferred. | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [port-arrow-horizontal-both](../shapes/svg/port-arrow-horizontal-both.svg) — Only the named component geometry and shown example text; no model or generalized grammar validation. / Deferred: Arrow-bearing child geometry only; elongated containing port, nested placement and direction-selection semantics remain deferred. |
| undirected-right-port | small rounded square on right boundary; solid; p4 / p5 name and type | Primitive glyph only; host composition and labels deferred | [port-glyph](../shapes/svg/port-glyph.svg) — Only the undirected outline shown by the representative table; the separate boundary grammar includes pdh/pdv, so this is not a full boundary-production implementation. |

### table-9/cell-4

Source: [PDF 91 / printed 59](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=91).

Dependencies: `binding`, `connection-graphical`, `interconnection-view`, `part`, `port-l`, `port-r`.

Source issue: Drawing locates p5 on part3; last textual binding identifies part2.p5. No silent correction.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| nested-interconnection | outer rounded part; two rounded internal parts; boundary ports and three linking segments; solid; part/name/type; port labels | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Composed interconnection example absent; primitive assets do not represent the complete source alternative. |

### table-9/cell-5

Source: [PDF 91 / printed 59](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=91).

Dependencies: `8.2.3.17`, `composite-feature-membership`, `reference-subsetting`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| owned-performance | part above perform-action rounded node with hollow diamond at owning part end; solid; perform action keyword | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Perform action node and membership edge absent. |
| external-performance | part above separately declared action; directed solid line labelled perform; solid; action keyword; perform relationship keyword | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Perform relationship asset absent. |

### table-9/cell-6

Source: [PDF 92 / printed 60](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=92).

Dependencies: `8.2.3.17`, `composite-feature-membership`, `reference-subsetting`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| explicit-reference-subsetting-performance | hollow-diamond ownership edge from part to perform-action node; solid reference-subsetting edge to separately declared action with open triangle and adjacent dotted adornment; solid; distinct action1 and action3 names/types | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Action membership and reference-subsetting assets absent. |

### table-9/cell-7

Source: [PDF 92 / printed 60](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=92).

Dependencies: `8.2.3.17`, `succession`, `Caption says flows; textual then denotes succession. Do not claim item-flow notation.`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| action-flow-compartment | rounded part with separated italic action-flow compartment; two rounded perform nodes joined downward by dashed open-arrow succession; solid nodes; dashed succession; perform action keywords | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Action-flow compartment and succession assets absent. |

### table-9/cell-8

Source: [PDF 92 / printed 60](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=92).

Dependencies: `OccurrenceUsagePrefix`, `UsageDeclaration`, `ValuePart`, `el-prefix`, `parts-compartment`, `usage-cp`.

Source issue: Imported usage-cp prints usageDeclaration, whereas the textual grammar declares UsageDeclaration; no silent normalization.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| inherited-entry | text row in sharp rectangular compartment with italic parts header; solid; caret before name | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Parts textual compartment and semantic label formatter absent. |
| ordered-nonunique-multiplicity | text row in sharp rectangular compartment with italic parts header; solid; range multiplicity followed by ordered and nonunique | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Parts textual compartment and semantic label formatter absent. |
| redefinition-keyword | text row in sharp rectangular compartment with italic parts header; solid; name/type followed by redefines target | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Parts textual compartment and semantic label formatter absent. |
| redefinition-symbol | text row in sharp rectangular compartment with italic parts header; solid; name/type followed by :>> target | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Parts textual compartment and semantic label formatter absent. |
| anonymous-redefinition | text row in sharp rectangular compartment with italic parts header; solid; :>> target without new name/type | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Parts textual compartment and semantic label formatter absent. |
| subsetting-keyword | text row in sharp rectangular compartment with italic parts header; solid; name/type and multiplicity followed by subsets target | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Parts textual compartment and semantic label formatter absent. |
| subsetting-symbol | text row in sharp rectangular compartment with italic parts header; solid; name/type and multiplicity followed by :> target | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Parts textual compartment and semantic label formatter absent. |
| value-binding | text row in sharp rectangular compartment with italic parts header; solid; name = referenced value | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Parts textual compartment and semantic label formatter absent. |
| referential-entry | text row in sharp rectangular compartment with italic parts header; solid; ref before usage name/type | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [part-definition-parts](../shapes/svg/part-definition-parts.svg) — The example row explicitly shows ref spare : Wheel[0..1]; other declaration text is caller-supplied. |
| name-only-entry | text row in sharp rectangular compartment with italic parts header; solid; name without displayed type | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Parts textual compartment and semantic label formatter absent. |
| omitted-members | text row in sharp rectangular compartment with italic parts header; solid; ellipsis below listed members | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [part-definition-parts](../shapes/svg/part-definition-parts.svg), [part-usage-parts](../shapes/svg/part-usage-parts.svg) — Only the literal trailing elision marker in the selected parts compartment. |

### 8.2.3.11/compartment/1

Source: [PDF 241 / printed 209](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=241).

Dependencies: `directed-features-compartment`, `interconnection-compartment`, `parts-compartment`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| parts-compartment-choice | one of three contributed compartment alternatives; solid; Labels and member selection follow the imported productions; generalized formatting is deferred. | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [part-definition-parts](../shapes/svg/part-definition-parts.svg), [part-usage-parts](../shapes/svg/part-usage-parts.svg) — Only the named component geometry and shown example text; no model or generalized grammar validation. / Deferred: Two literal rows and an elision marker only; arbitrary member selection, row counts, prefix/alias/value formatting and semantic checks remain deferred. |
| directed-features-choice | directed features compartment; solid; Labels and member selection follow the imported productions; generalized formatting is deferred. | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: No complete renderer for this imported grammar; explicitly deferred. |
| interconnection-choice | interconnection compartment; solid; Labels and member selection follow the imported productions; generalized formatting is deferred. | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: No complete renderer for this imported grammar; explicitly deferred. |

### 8.2.3.11/definition-node/1

Source: [PDF 240 / printed 208](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=240).

Dependencies: `part-def`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| part-definition-alternative | partial production contributes part-def; solid; Labels and member selection follow the imported productions; generalized formatting is deferred. | Only minimal silhouette represented | [part-definition](../shapes/svg/part-definition.svg) — Only the minimal geometry and example label described here; each asset retains its own limitations. |

### 8.2.3.11/directed-features-compartment-contents/1

Source: [PDF 242 / printed 210](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=242).

Dependencies: `directed-features-compartment-element`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| directed-feature-rows | zero or more directed rows followed by optional ellipsis; solid; Labels and member selection follow the imported productions; generalized formatting is deferred. | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: No row formatter. |

### 8.2.3.11/directed-features-compartment-element/1

Source: [PDF 242 / printed 210](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=242).

Dependencies: `Definition-Body-Item`, `FeatureDirection`, `el-prefix`.

Source issue: el-prefix is mandatory here unlike optional parts-row prefix.

Source issue: Definition-Body-Item is printed; textual syntax defines DefinitionBodyItem. Do not silently equate.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| directed-feature-row | textual row of el-prefix, FeatureDirection and zero or more body items; solid; in/out/inout imported direction | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Defer exact row formatting pending source ambiguity. |

### 8.2.3.11/directed-features-compartment/1

Source: [PDF 242 / printed 210](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=242).

Dependencies: `directed-features-compartment-contents`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| named-directed-features-compartment | horizontal separator; italic directed features title; contents; solid; Labels and member selection follow the imported productions; generalized formatting is deferred. | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Directed-features compartment asset absent. |

### 8.2.3.11/general-view/1

Source: [PDF 242 / printed 210](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=242).

Dependencies: `interconnection-view`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| interconnection-general-view | partial production makes interconnection-view a general-view alternative; solid; Labels and member selection follow the imported productions; generalized formatting is deferred. | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: No standalone view implementation. |

### 8.2.3.11/interconnection-compartment/1

Source: [PDF 242 / printed 210](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=242).

Dependencies: `interconnection-view`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| named-interconnection-compartment | horizontal separator with italic interconnection title and graphical contents; solid; Labels and member selection follow the imported productions; generalized formatting is deferred. | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Compartment asset absent. |

### 8.2.3.11/interconnection-element/1

Source: [PDF 240 / printed 208](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=240).

Dependencies: `part`, `part-ref`.

Source issue: Source prints = followed by spaced |; preserve operator and flag.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| part-in-interconnection | part or part-ref as interconnection element; solid; Labels and member selection follow the imported productions; generalized formatting is deferred. | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: No complete renderer for this imported grammar; explicitly deferred. |

### 8.2.3.11/interconnection-view/1

Source: [PDF 242 / printed 210](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=242).

Dependencies: `dependencies-and-annotations-element`, `ellipsis-at-lower-left-corner`, `interconnection-element`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| interconnection-elements | zero or more interconnection elements and dependencies/annotations with optional lower-left ellipsis; solid; Labels and member selection follow the imported productions; generalized formatting is deferred. | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: No complete composition engine; selected primitives only. |

### 8.2.3.11/part-def-name-compartment/1

Source: [PDF 241 / printed 209](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=241).

Dependencies: `DefinitionPrefix`, `definition-name-with-alias`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| definition-name | keyword line followed by definition declaration and optional alias; solid; DefinitionPrefix plus part def; definition-name-with-alias | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [part-definition](../shapes/svg/part-definition.svg) — Only the minimal geometry and example label described here; each asset retains its own limitations. / Deferred: Only empty-prefix, no-alias name example represented. |

### 8.2.3.11/part-def/1

Source: [PDF 240 / printed 208](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=240), [PDF 241 / printed 209](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=241).

Dependencies: `compartment-stack`, `interconnection-view`, `part-def-name-compartment`, `port-b`, `port-l`, `port-r`, `port-t`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| definition-envelope | sharp rectangle with top/bottom/left/right repeated boundary ports, name region, interconnection view and compartment stack; solid; Labels and member selection follow the imported productions; generalized formatting is deferred. | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [part-definition-parts](../shapes/svg/part-definition-parts.svg) — Only the named component geometry and shown example text; no model or generalized grammar validation. / Deferred: Only the named parts compartment is supplied; arbitrary compartment stacks, boundary ports and interconnection contents remain deferred. |

### 8.2.3.11/part-name-compartment/1

Source: [PDF 241 / printed 209](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=241).

Dependencies: `OccurrenceUsagePrefix`, `usage-name-with-alias`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| usage-name | prefix+part keyword line and name/type declaration with optional alias; solid; OccurrenceUsagePrefix and usage-name-with-alias | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [part-usage](../shapes/svg/part-usage.svg), [part-reference](../shapes/svg/part-reference.svg) — Only the minimal geometry and example label described here; each asset retains its own limitations. / Deferred: Only basic composite/ref labels; other prefixes/aliases deferred. |

### 8.2.3.11/part-ref/1

Source: [PDF 241 / printed 209](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=241).

Dependencies: `compartment-stack`, `interconnection-view`, `part-name-compartment`, `port-b`, `port-l`, `port-r`, `port-t`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| referential-part-envelope | dashed rounded rectangle with repeated ports on four sides, name, interconnection view and compartments; dashed; Labels and member selection follow the imported productions; generalized formatting is deferred. | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [part-reference](../shapes/svg/part-reference.svg) — Only the named component geometry and shown example text; no model or generalized grammar validation. / Deferred: Only the minimal referential envelope is supplied; internal views and compartments remain deferred. |

### 8.2.3.11/part/1

Source: [PDF 241 / printed 209](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=241).

Dependencies: `compartment-stack`, `interconnection-view`, `part-name-compartment`, `port-b`, `port-l`, `port-r`, `port-t`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| composite-part-envelope | solid rounded rectangle with four-side repeated ports, name region, interconnection view and compartment stack; solid; Labels and member selection follow the imported productions; generalized formatting is deferred. | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [part-usage-parts](../shapes/svg/part-usage-parts.svg) — Only the named component geometry and shown example text; no model or generalized grammar validation. / Deferred: Only a two-row parts compartment is supplied; other compartments, nesting and boundary composition remain deferred. |

### 8.2.3.11/parts-compartment-contents/1

Source: [PDF 242 / printed 210](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=242).

Dependencies: `parts-compartment-element`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| parts-rows | zero or more rows followed by optional ellipsis; solid; Labels and member selection follow the imported productions; generalized formatting is deferred. | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [part-definition-parts](../shapes/svg/part-definition-parts.svg), [part-usage-parts](../shapes/svg/part-usage-parts.svg) — Only the named component geometry and shown example text; no model or generalized grammar validation. / Deferred: Two literal rows and an elision marker only; arbitrary member selection, row counts, prefix/alias/value formatting and semantic checks remain deferred. |

### 8.2.3.11/parts-compartment-element/1

Source: [PDF 242 / printed 210](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=242).

Dependencies: `OccurrenceUsagePrefix`, `el-prefix`, `usage-cp`.

Source issue: Imported usage-cp prints usageDeclaration, whereas the textual grammar declares UsageDeclaration; no silent normalization.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| parts-row | optional el-prefix (^ or /; slash meaning not established by this review) then occurrence usage prefix and declaration/value; solid; caret or slash optional; imported prefixes/declaration/value | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [part-definition-parts](../shapes/svg/part-definition-parts.svg), [part-usage-parts](../shapes/svg/part-usage-parts.svg) — Only the named component geometry and shown example text; no model or generalized grammar validation. / Deferred: Two literal rows and an elision marker only; arbitrary member selection, row counts, prefix/alias/value formatting and semantic checks remain deferred. |

### 8.2.3.11/parts-compartment/1

Source: [PDF 242 / printed 210](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=242).

Dependencies: `parts-compartment-contents`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| named-parts-compartment | horizontal separator with italic parts title, then contents; solid; Labels and member selection follow the imported productions; generalized formatting is deferred. | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [part-definition-parts](../shapes/svg/part-definition-parts.svg), [part-usage-parts](../shapes/svg/part-usage-parts.svg) — Only the named component geometry and shown example text; no model or generalized grammar validation. / Deferred: Two literal rows and an elision marker only; arbitrary member selection, row counts, prefix/alias/value formatting and semantic checks remain deferred. |

### 8.2.3.11/usage-node/1

Source: [PDF 241 / printed 209](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=241).

Dependencies: `part`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| part-usage-alternative | partial production contributes part; solid; Labels and member selection follow the imported productions; generalized formatting is deferred. | Minimal example only | [part-usage](../shapes/svg/part-usage.svg) — Only the minimal geometry and example label described here; each asset retains its own limitations. |

## Ports

### table-10/cell-1

Source: [PDF 94 / printed 62](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=94).

Dependencies: `Table examples demonstrate alternatives; not an exhaustive prefix-combination grammar.`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| minimal-port-definition | Sharp-corner rectangular node; Solid unless stated otherwise; Port definition keyword and name | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [port-definition](../shapes/svg/port-definition.svg) — Only the named component geometry and shown example text; no model or generalized grammar validation. |
| port-definition-with-compartments | Sharp-corner rectangle with compartment stack; Solid unless stated otherwise; Definition header plus compartment headings | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [port-definition-ports](../shapes/svg/port-definition-ports.svg) — Only the named component geometry and shown example text; no model or generalized grammar validation. / Deferred: Only a two-row ports compartment is supplied; generalized compartments and nested boundary layout remain deferred. |

### table-10/cell-2

Source: [PDF 94 / printed 62](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=94).

Dependencies: `Table examples demonstrate alternatives; not an exhaustive prefix-combination grammar.`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| minimal-full-port-usage | Rounded rectangular node; Solid unless stated otherwise; «port» and editable name/type | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [port-usage](../shapes/svg/port-usage.svg) — Only the minimal geometry and example label described here; each asset retains its own limitations. |
| full-port-with-compartments | Rounded host and compartment stack; Solid unless stated otherwise; Header and compartment labels | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [port-usage-ports](../shapes/svg/port-usage-ports.svg) — Only the named component geometry and shown example text; no model or generalized grammar validation. / Deferred: Only a two-row ports compartment is supplied; generalized compartments and nested boundary layout remain deferred. |

### table-10/cell-3

Source: [PDF 94 / printed 62](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=94).

Dependencies: `7.12.3`, `Table examples demonstrate alternatives; not an exhaustive prefix-combination grammar.`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| ports-compartment-prefix | Text list; Solid unless stated otherwise; Inherited member prefix ^ | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Requires layout, label parsing or context handling not provided by existing components. |
| ports-compartment-cardinality | Text list; Solid unless stated otherwise; Multiplicity, ordered and nonunique | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Requires layout, label parsing or context handling not provided by existing components. |
| ports-compartment-redefinition | Text list; Solid unless stated otherwise; redefines and :>> forms, including target-only :>> entry | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Requires layout, label parsing or context handling not provided by existing components. |
| ports-compartment-subsetting | Text list; Solid unless stated otherwise; subsets and :> forms | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Requires layout, label parsing or context handling not provided by existing components. |
| ports-compartment-value | Text list; Solid unless stated otherwise; Equals/value example | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Requires layout, label parsing or context handling not provided by existing components. |
| ports-compartment-reference | Text list; Solid unless stated otherwise; ref prefix | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Requires layout, label parsing or context handling not provided by existing components. |
| ports-compartment-name-only | Text list; Solid unless stated otherwise; Untyped name | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Requires layout, label parsing or context handling not provided by existing components. |
| ports-compartment-conjugation | Text list; Solid unless stated otherwise; Type prefixed with ~ | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Requires layout, label parsing or context handling not provided by existing components. |
| ports-compartment-elision | Text list; Solid unless stated otherwise; Trailing ellipsis | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [port-definition-ports](../shapes/svg/port-definition-ports.svg), [port-usage-ports](../shapes/svg/port-usage-ports.svg) — Only the literal trailing elision marker in the selected ports compartment. |

### table-10/cell-4

Source: [PDF 94 / printed 62](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=94).

Dependencies: `8.2.3.11/directed-features-compartment/1`, `Table examples demonstrate alternatives; not an exhaustive prefix-combination grammar.`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| directed-attributes-in-out-inout | Text compartment with horizontal divider; Solid unless stated otherwise; Italic directed features heading and in/out/inout attribute rows | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Requires layout, label parsing or context handling not provided by existing components. |
| directed-items-in-out-inout | Same compartment; Solid unless stated otherwise; in/out/inout item rows and optional ellipsis | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Requires layout, label parsing or context handling not provided by existing components. |

### 8.2.3.12/compartment/1

Source: [PDF 243 / printed 211](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=243).

Dependencies: `8.2.3.12/ports-compartment/1`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| ports-compartment-extension | Adds ports-compartment to compartment; Solid unless stated otherwise; Inherited from ports-compartment | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [port-definition-ports](../shapes/svg/port-definition-ports.svg), [port-usage-ports](../shapes/svg/port-usage-ports.svg) — Only the named component geometry and shown example text; no model or generalized grammar validation. / Deferred: Two literal example rows only; empty/arbitrary-length lists, formatted declarations, nesting and model semantics remain deferred. |

### 8.2.3.12/definition-node/1

Source: [PDF 242 / printed 210](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=242).

Dependencies: `8.2.3.12/port-def/1`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| port-definition-node-extension | Adds port-def to definition-node; Solid unless stated otherwise; Inherited from port-def | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [port-definition](../shapes/svg/port-definition.svg) — Only the named component geometry and shown example text; no model or generalized grammar validation. |

### 8.2.3.12/interconnection-element/1

Source: [PDF 243 / printed 211](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=243).

Dependencies: `port`, `port-def`.

Source issue: Source uses port rather than declared port-usage; resolution not assumed.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| port-interconnection-extension | Adds port-def and source-spelled port to interconnection-element; Solid unless stated otherwise; Dependent node labels | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Preserve source-spelled port; no silent substitution with port-usage. |

### 8.2.3.12/pdh/1

Source: [PDF 243 / printed 211](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=243).

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| horizontal-bidirectional | Horizontal double-headed open arrow; Solid open arrowhead strokes.; No text | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [port-arrow-horizontal-both](../shapes/svg/port-arrow-horizontal-both.svg) — Direction indicator geometry embedded in a boundary glyph; no direction is inferred from model features. |
| horizontal-rightward | Horizontal right-pointing open arrow; Solid open arrowhead strokes.; No text | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [port-arrow-right](../shapes/svg/port-arrow-right.svg) — Direction indicator geometry embedded in a boundary glyph; no direction is inferred from model features. |
| horizontal-leftward | Horizontal left-pointing open arrow; Solid open arrowhead strokes.; No text | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [port-arrow-left](../shapes/svg/port-arrow-left.svg) — Direction indicator geometry embedded in a boundary glyph; no direction is inferred from model features. |

### 8.2.3.12/pdv/1

Source: [PDF 243 / printed 211](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=243).

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| vertical-bidirectional | Vertical double-headed open arrow; Solid open arrowhead strokes.; No text | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [port-arrow-vertical-both](../shapes/svg/port-arrow-vertical-both.svg) — Direction indicator geometry embedded in a boundary glyph; no direction is inferred from model features. |
| vertical-upward | Vertical up-pointing open arrow; Solid open arrowhead strokes.; No text | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [port-arrow-up](../shapes/svg/port-arrow-up.svg) — Direction indicator geometry embedded in a boundary glyph; no direction is inferred from model features. |
| vertical-downward | Vertical down-pointing open arrow; Solid open arrowhead strokes.; No text | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [port-arrow-down](../shapes/svg/port-arrow-down.svg) — Direction indicator geometry embedded in a boundary glyph; no direction is inferred from model features. |

### 8.2.3.12/port-b/1

Source: [PDF 245 / printed 213](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=245).

Dependencies: `pdv`, `port-b`, `port-label`, `proxy-h`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| boundary-b-solid | Small rounded glyph straddling host boundary with pdv; Solid unless stated otherwise; outside lower-right; nested form horizontal label inside, nested ports on bottom | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [port-arrow-up](../shapes/svg/port-arrow-up.svg), [port-arrow-down](../shapes/svg/port-arrow-down.svg), [port-arrow-vertical-both](../shapes/svg/port-arrow-vertical-both.svg) — Only the named component geometry and shown example text; no model or generalized grammar validation. / Deferred: Glyphs are supplied; complete side-specific host boundary, label placement and model-context validation remain host responsibilities. The original four-side composition illustrates placement separately. |
| boundary-b-reference | Dotted/dashed rounded glyph straddling host boundary with pdv; Broken outline (source note calls this dotted); host boundary and direction indication remain solid.; outside lower-right; nested form horizontal label inside, nested ports on bottom | Only nested ports; source note PDF 246 | Deferred: Requires layout, label parsing or context handling not provided by existing components. |
| boundary-b-nested | Elongated rounded glyph straddling host boundary; repeated nested ports on same side; pdv; Solid unless stated otherwise; outside lower-right; nested form horizontal label inside, nested ports on bottom | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Requires layout, label parsing or context handling not provided by existing components. |
| boundary-b-proxy | Delegates to proxy-h; Solid unless stated otherwise; Side-dependent proxy label | Only on part usage within interconnection view | Deferred: Requires layout, label parsing or context handling not provided by existing components. |

### 8.2.3.12/port-def-name-compartment/1

Source: [PDF 242 / printed 210](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=242).

Dependencies: `DefinitionPrefix`, `definition-name-with-alias`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| minimal-definition-name | Header in sharp-corner host; Solid unless stated otherwise; «port def» and editable definition name | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [port-definition](../shapes/svg/port-definition.svg) — Only the named component geometry and shown example text; no model or generalized grammar validation. |
| prefixed-aliased-definition-name | Same header area; Solid unless stated otherwise; DefinitionPrefix and definition-name-with-alias | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Requires layout, label parsing or context handling not provided by existing components. |

### 8.2.3.12/port-def/1

Source: [PDF 242 / printed 210](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=242).

Dependencies: `port-b`, `port-l`, `port-r`, `port-t`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| minimal-port-definition | Sharp-corner rectangular node; Solid unless stated otherwise; Port definition keyword and name | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [port-definition](../shapes/svg/port-definition.svg) — Only the named component geometry and shown example text; no model or generalized grammar validation. |
| port-definition-with-compartments | Sharp-corner rectangle with compartment stack; Solid unless stated otherwise; Definition header plus compartment headings | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [port-definition-ports](../shapes/svg/port-definition-ports.svg) — Only the named component geometry and shown example text; no model or generalized grammar validation. / Deferred: Only a two-row ports compartment is supplied; generalized compartments and nested boundary layout remain deferred. |
| port-definition-with-boundary-ports | Sharp-corner host with zero or more ports on all four sides; Solid unless stated otherwise; Side-specific boundary port labels | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Requires layout, label parsing or context handling not provided by existing components. |

### 8.2.3.12/port-l/1

Source: [PDF 243 / printed 211](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=243), [PDF 244 / printed 212](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=244).

Dependencies: `pdh`, `port-l`, `port-label`, `proxy-v`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| boundary-l-solid | Small rounded glyph straddling host boundary with pdh; Solid unless stated otherwise; outside upper-left; nested form vertical label inside, nested ports on left | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [port-arrow-left](../shapes/svg/port-arrow-left.svg), [port-arrow-right](../shapes/svg/port-arrow-right.svg), [port-arrow-horizontal-both](../shapes/svg/port-arrow-horizontal-both.svg) — Only the named component geometry and shown example text; no model or generalized grammar validation. / Deferred: Glyphs are supplied; complete side-specific host boundary, label placement and model-context validation remain host responsibilities. The original four-side composition illustrates placement separately. |
| boundary-l-reference | Dotted/dashed rounded glyph straddling host boundary with pdh; Broken outline (source note calls this dotted); host boundary and direction indication remain solid.; outside upper-left; nested form vertical label inside, nested ports on left | Only nested ports; source note PDF 246 | Deferred: Requires layout, label parsing or context handling not provided by existing components. |
| boundary-l-nested | Elongated rounded glyph straddling host boundary; repeated nested ports on same side; pdh; Solid unless stated otherwise; outside upper-left; nested form vertical label inside, nested ports on left | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Requires layout, label parsing or context handling not provided by existing components. |
| boundary-l-proxy | Delegates to proxy-v; Solid unless stated otherwise; Side-dependent proxy label | Only on part usage within interconnection view | Deferred: Requires layout, label parsing or context handling not provided by existing components. |

### 8.2.3.12/port-label/1

Source: [PDF 246 / printed 214](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=246).

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| boundary-qualified-name | External or internal label according to side production; Solid unless stated otherwise; QualifiedName | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Requires layout, label parsing or context handling not provided by existing components. |
| boundary-qualified-name-and-type | External or internal label according to side production; Solid unless stated otherwise; QualifiedName : QualifiedName | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Requires layout, label parsing or context handling not provided by existing components. |

### 8.2.3.12/port-name-compartment/1

Source: [PDF 243 / printed 211](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=243).

Dependencies: `OccurrenceUsagePrefix`, `usage-name-with-alias`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| minimal-usage-header | Rounded host header; Solid unless stated otherwise; «port» and name/type | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [port-usage](../shapes/svg/port-usage.svg) — Only the minimal geometry and example label described here; each asset retains its own limitations. |
| prefixed-aliased-usage-header | Rounded host header; Solid unless stated otherwise; OccurrenceUsagePrefix and usage-name-with-alias | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Requires layout, label parsing or context handling not provided by existing components. |

### 8.2.3.12/port-r/1

Source: [PDF 244 / printed 212](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=244), [PDF 245 / printed 213](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=245).

Dependencies: `pdh`, `port-label`, `port-r`, `proxy-v`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| boundary-r-solid | Small rounded glyph straddling host boundary with pdh; Solid unless stated otherwise; outside upper-right; nested form vertical label inside, nested ports on right | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [port-arrow-left](../shapes/svg/port-arrow-left.svg), [port-arrow-right](../shapes/svg/port-arrow-right.svg), [port-arrow-horizontal-both](../shapes/svg/port-arrow-horizontal-both.svg) — Only the named component geometry and shown example text; no model or generalized grammar validation. / Deferred: Glyphs are supplied; complete side-specific host boundary, label placement and model-context validation remain host responsibilities. The original four-side composition illustrates placement separately. |
| boundary-r-reference | Dotted/dashed rounded glyph straddling host boundary with pdh; Broken outline (source note calls this dotted); host boundary and direction indication remain solid.; outside upper-right; nested form vertical label inside, nested ports on right | Only nested ports; source note PDF 246 | Deferred: Requires layout, label parsing or context handling not provided by existing components. |
| boundary-r-nested | Elongated rounded glyph straddling host boundary; repeated nested ports on same side; pdh; Solid unless stated otherwise; outside upper-right; nested form vertical label inside, nested ports on right | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Requires layout, label parsing or context handling not provided by existing components. |
| boundary-r-proxy | Delegates to proxy-v; Solid unless stated otherwise; Side-dependent proxy label | Only on part usage within interconnection view | Deferred: Requires layout, label parsing or context handling not provided by existing components. |

### 8.2.3.12/port-t/1

Source: [PDF 245 / printed 213](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=245).

Dependencies: `pdv`, `port-label`, `port-t`, `proxy-h`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| boundary-t-solid | Small rounded glyph straddling host boundary with pdv; Solid unless stated otherwise; outside upper-left; nested form horizontal label inside, nested ports on top | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [port-arrow-up](../shapes/svg/port-arrow-up.svg), [port-arrow-down](../shapes/svg/port-arrow-down.svg), [port-arrow-vertical-both](../shapes/svg/port-arrow-vertical-both.svg) — Only the named component geometry and shown example text; no model or generalized grammar validation. / Deferred: Glyphs are supplied; complete side-specific host boundary, label placement and model-context validation remain host responsibilities. The original four-side composition illustrates placement separately. |
| boundary-t-reference | Dotted/dashed rounded glyph straddling host boundary with pdv; Broken outline (source note calls this dotted); host boundary and direction indication remain solid.; outside upper-left; nested form horizontal label inside, nested ports on top | Only nested ports; source note PDF 246 | Deferred: Requires layout, label parsing or context handling not provided by existing components. |
| boundary-t-nested | Elongated rounded glyph straddling host boundary; repeated nested ports on same side; pdv; Solid unless stated otherwise; outside upper-left; nested form horizontal label inside, nested ports on top | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Requires layout, label parsing or context handling not provided by existing components. |
| boundary-t-proxy | Delegates to proxy-h; Solid unless stated otherwise; Side-dependent proxy label | Only on part usage within interconnection view | Deferred: Requires layout, label parsing or context handling not provided by existing components. |

### 8.2.3.12/port-usage/1

Source: [PDF 242 / printed 210](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=242), [PDF 243 / printed 211](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=243).

Dependencies: `port-b`, `port-l`, `port-r`, `port-t`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| minimal-full-port-usage | Rounded rectangular node; Solid unless stated otherwise; «port» and editable name/type | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [port-usage](../shapes/svg/port-usage.svg) — Only the minimal geometry and example label described here; each asset retains its own limitations. |
| full-port-with-compartments | Rounded host and compartment stack; Solid unless stated otherwise; Header and compartment labels | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [port-usage-ports](../shapes/svg/port-usage-ports.svg) — Only the named component geometry and shown example text; no model or generalized grammar validation. / Deferred: Only a two-row ports compartment is supplied; generalized compartments and nested boundary layout remain deferred. |
| full-port-with-nested-ports | Rounded host with repeated ports on any side; Solid unless stated otherwise; Side-specific labels | Within the containing part/port production and its declared modeling context; no model validity is inferred. | Deferred: Requires layout, label parsing or context handling not provided by existing components. |

### 8.2.3.12/ports-compartment-contents/1

Source: [PDF 243 / printed 211](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=243).

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| ports-list-empty-or-repeated | Zero or more rows; Solid unless stated otherwise; ports-compartment-element repeated | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [port-definition-ports](../shapes/svg/port-definition-ports.svg), [port-usage-ports](../shapes/svg/port-usage-ports.svg) — Only the named component geometry and shown example text; no model or generalized grammar validation. / Deferred: Two literal example rows only; empty/arbitrary-length lists, formatted declarations, nesting and model semantics remain deferred. |
| ports-list-ellipsis | List with optional trailing ellipsis; Solid unless stated otherwise; … | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [port-definition-ports](../shapes/svg/port-definition-ports.svg), [port-usage-ports](../shapes/svg/port-usage-ports.svg) — Only the literal trailing elision marker in the selected ports compartment. |

### 8.2.3.12/ports-compartment-element/1

Source: [PDF 243 / printed 211](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=243).

Dependencies: `OccurrenceUsagePrefix`, `el-prefix`, `usage-cp`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| ports-list-entry | Text row; Solid unless stated otherwise; Optional el-prefix, OccurrenceUsagePrefix, usage-cp | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [port-definition-ports](../shapes/svg/port-definition-ports.svg), [port-usage-ports](../shapes/svg/port-usage-ports.svg) — Only the named component geometry and shown example text; no model or generalized grammar validation. / Deferred: Two literal example rows only; empty/arbitrary-length lists, formatted declarations, nesting and model semantics remain deferred. |

### 8.2.3.12/ports-compartment/1

Source: [PDF 243 / printed 211](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=243).

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| ports-compartment | Compartment divider and contents region; Solid unless stated otherwise; Italic ports heading and list contents | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [port-definition-ports](../shapes/svg/port-definition-ports.svg), [port-usage-ports](../shapes/svg/port-usage-ports.svg) — Only the named component geometry and shown example text; no model or generalized grammar validation. / Deferred: Two literal example rows only; empty/arbitrary-length lists, formatted declarations, nesting and model semantics remain deferred. |

### 8.2.3.12/proxy-h/1

Source: [PDF 246 / printed 214](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=246).

Dependencies: `8.2.3.9/proxy-label/1`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| horizontal-proxy-label-right | Filled dot crossed by horizontal host boundary; Solid unless stated otherwise; proxy-label to right | Only on a part usage within an interconnection view | Deferred: Requires layout, label parsing or context handling not provided by existing components. |
| horizontal-proxy-label-left | Filled dot crossed by horizontal host boundary; Solid unless stated otherwise; proxy-label to left | Only on a part usage within an interconnection view | Deferred: Requires layout, label parsing or context handling not provided by existing components. |

### 8.2.3.12/proxy-v/1

Source: [PDF 246 / printed 214](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=246).

Dependencies: `8.2.3.9/proxy-label/1`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| vertical-proxy-label-right | Filled dot crossed by vertical host boundary; Solid unless stated otherwise; proxy-label to right | Only on a part usage within an interconnection view | Deferred: Requires layout, label parsing or context handling not provided by existing components. |
| vertical-proxy-label-left | Filled dot crossed by vertical host boundary; Solid unless stated otherwise; proxy-label to left | Only on a part usage within an interconnection view | Deferred: Requires layout, label parsing or context handling not provided by existing components. |

### 8.2.3.12/usage-node/1

Source: [PDF 242 / printed 210](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=242).

Dependencies: `8.2.3.12/port-usage/1`.

| Local alternative | Appearance and labels | Context | Rendering disposition |
|---|---|---|---|
| port-usage-node-extension | Adds port-usage to usage-node; Solid unless stated otherwise; Inherited from port-usage | Within the containing part/port production and its declared modeling context; no model validity is inferred. | [port-usage](../shapes/svg/port-usage.svg) — Only the named component geometry and shown example text; no model or generalized grammar validation. |

## Source and reproducibility

Pinned OMG document `formal/2026-03-02`, SHA-256 `46e6c0476a6f1f34f367d57e039d56659bff75e41d2e4b3d37ca4cadea84a83a`. Original [SysML Language PDF](https://www.omg.org/spec/SysML/2.0/Language/PDF).

Research notes: [Parts](research/parts-notation-audit.md), [ports](research/ports-notation-audit.md), [shared rules](research/parts-ports-shared-rules.md).

Rebuild with `uv run --locked python scripts/build_notation.py`; validate with `uv run --locked python scripts/check_inventory.py`. No SysML parser, OCL evaluator or execution engine was run.
