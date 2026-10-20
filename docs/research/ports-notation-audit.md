# Ports notation: selected source-unit audit

This note records the source-review baseline; current implementation dispositions are in the [published ledger](../parts-ports-notation-audit.md).

This audit inspects all four labeled cells of Table 10 and all 20 declaration occurrences in §8.2.3.12. It identifies displayed alternatives and their restrictions; an audited source unit may still have every rendering alternative deferred. It is not a claim of complete SysML graphical coverage, parser acceptance, model validity or renderer conformance.

The pinned source is OMG SysML 2.0 Language, `formal/2026-03-02`, SHA-256 `46e6c0476a6f1f34f367d57e039d56659bff75e41d2e4b3d37ca4cadea84a83a`, verified against `data/source-manifest.json`. PDF pages 94, 95, 239 and 242–246 were rendered and visually inspected; extracted text was used to locate declarations. The section continues through **PDF 246 / printed 214**, not merely PDF 245.

## What the source actually permits

A port definition has a sharp-corner rectangular full-node form; a port usage has a rounded rectangular full-node form. Both can carry a compartment stack and repeated boundary ports on all four sides. Their respective headers use `DefinitionPrefix` with the port-definition keyword and `definition-name-with-alias`, or `OccurrenceUsagePrefix` with the port keyword and `usage-name-with-alias`. These dependencies require more than substituting an arbitrary label into a rectangle. [Table 10, PDF 94 / printed 62](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=94), [§8.2.3.12, PDF 242–243 / printed 210–211](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=242).

Each left, right, top and bottom boundary production shows four alternatives: a solid small rounded glyph; a reference glyph with a broken outline; an elongated rounded glyph carrying nested ports on its corresponding side; and a proxy alternative. Left/right forms contain a horizontal direction indication (`pdh`), and top/bottom forms contain a vertical indication (`pdv`). Those direction productions each show three alternatives: both directions and either individual direction. The current undirected `port-glyph` component supplies reusable geometry, but does **not** alone instantiate any complete displayed boundary production. [PDF 243–245 / printed 211–213](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=243).

The small left/right forms position their labels outside and above, toward the corresponding side. The top form puts its external label above-left; the bottom form puts it below-right. Elongated left/right forms carry vertical labels inside and their repeated nested ports on the corresponding edge. Elongated top/bottom forms carry horizontal labels inside and nested ports on the corresponding top/bottom edge. Position is a layout responsibility; rotating a whole SVG also rotates its text and does not reproduce these alternatives. [PDF 244–245 / printed 212–213](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=244).

The source explicitly restricts broken-outline reference ports to **nested ports**. It restricts the proxy option to a **part usage within an interconnection view**. Vertical proxies show a filled dot across a vertical boundary and a label on either side; horizontal proxies show a dot across a horizontal boundary and a label on either side. These are context restrictions, not assumptions that screen nesting automatically establishes model ownership. [PDF 246 / printed 214](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=246).

`proxy-label` is resolved outside the selected ports section: §8.2.3.9 defines it as an optional leading dot followed by `FeatureChainMember`. It is **not undefined** merely because no declaration occurs in §8.2.3.12. The selected ports source refers to that name without a separate cross-reference. Existing research descriptions that call this dependency unresolved should be updated. [PDF 239 / printed 207](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=239).

## Compartments and conjugation

The ports compartment comprises a heading, repeated entries and optional trailing ellipsis. Its entry rule composes optional `el-prefix`, `OccurrenceUsagePrefix` and `usage-cp`. Table 10 illustrates inherited-member marking; multiplicity and ordered/nonunique modifiers; word and symbolic redefinition/subsetting forms; value notation; a referential entry; a name-only entry; a conjugated type; and elision. These examples do not establish an exhaustive cross-product of all prefix combinations. [Table 10, PDF 94 / printed 62](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=94), [grammar PDF 243 / printed 211](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=243).

The directed-features cell demonstrates `in`, `out` and `inout` for both attribute and item entries, with an optional ellipsis. Its graphical productions are in the preceding **parts** section, not among the 20 ports declarations. Their contents use repeated elements and optional elision; the element references `el-prefix`, `FeatureDirection` and `Definition-Body-Item`. [Table 10, PDF 94 / printed 62](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=94), [§8.2.3.11, PDF 242 / printed 210](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=242).

Conjugation reverses `in` and `out`, leaving `inout` unchanged. A conjugated port-usage type can use the original type name preceded by `~`; this denotes the corresponding nested conjugated definition. Table 10 shows that shorthand in a compartment entry. A boundary `port-label`, however, is printed as a qualified name with an optional colon and qualified type name; this audit does not silently extend that production to accept every compartment syntax. Likewise, a direction glyph alone is insufficient evidence for choosing an arrow from an arbitrary set of exchanged features. [§7.12.3, PDF 95 / printed 63](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=95), [boundary label PDF 246 / printed 214](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=246).

Ports are occurrences and can themselves contain nested ports. Other features of a port definition or usage must be referential rather than composite. This semantic restriction matters when explaining a port's nested contents; it does not mean every item exchanged through the port is a composed child of it. [§7.12.1, PDF 93 / printed 61](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=93), [§7.12.2, PDF 95 / printed 63](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=95).

## Source-unit disposition

The working ledger [the published ledger](../../data/parts-ports-audit.json) contains 24 units and 61 descriptive alternative records, with geometry, labels, context, source pages, dependencies and either a limited asset match or explicit deferral. These are audit bookkeeping counts, not 61 unique symbols or a total number of required SVGs. The following index makes every selected source unit explicit.

| Source-unit ID | PDF / printed pages | Disposition |
|---|---|---|
| `table-10/cell-1` | 94 / 62 | Minimal definition and compartment form considered; new definition asset is safe; compartment form deferred. |
| `table-10/cell-2` | 94 / 62 | Minimal full usage matched by `port-usage`; compartment form deferred. |
| `table-10/cell-3` | 94 / 62 | Nine entry families listed above; compartment rendering deferred. |
| `table-10/cell-4` | 94 / 62 | Directed attribute/item families; compartment rendering deferred. |
| `8.2.3.12/definition-node/1` | 242 / 210 | Extension dependency on `port-def`; no separate SVG required. |
| `8.2.3.12/port-def/1` | 242 / 210 | Minimal definition safe to add; compartments and boundary composition deferred. |
| `8.2.3.12/port-def-name-compartment/1` | 242 / 210 | Minimal header safe to add; generalized prefix/alias parsing deferred. |
| `8.2.3.12/usage-node/1` | 242 / 210 | Extension dependency on `port-usage`; no separate SVG required. |
| `8.2.3.12/port-usage/1` | 242–243 / 210–211 | Minimal full node matched; compartments and nested ports deferred. |
| `8.2.3.12/port-name-compartment/1` | 243 / 211 | Minimal header matched; generalized prefix/alias parsing deferred. |
| `8.2.3.12/compartment/1` | 243 / 211 | Extension dependency on ports compartment. |
| `8.2.3.12/ports-compartment/1` | 243 / 211 | Heading and list layout deferred. |
| `8.2.3.12/ports-compartment-contents/1` | 243 / 211 | Repeated/empty rows and optional elision deferred. |
| `8.2.3.12/ports-compartment-element/1` | 243 / 211 | Prefix and usage declaration dependency deferred. |
| `8.2.3.12/interconnection-element/1` | 243 / 211 | Source prints `port-def` or `port`; preserve spelling and flag mismatch. |
| `8.2.3.12/pdh/1` | 243 / 211 | Horizontal bidirectional/rightward/leftward indications deferred. |
| `8.2.3.12/pdv/1` | 243 / 211 | Vertical bidirectional/upward/downward indications deferred. |
| `8.2.3.12/port-l/1` | 243–244 / 211–212 | Solid/reference/nested/proxy alternatives deferred; generic geometry only exists. |
| `8.2.3.12/port-r/1` | 244–245 / 212–213 | Same four alternatives; position-specific labels deferred. |
| `8.2.3.12/port-t/1` | 245 / 213 | Same four alternatives; horizontal nested layout deferred. |
| `8.2.3.12/port-b/1` | 245 / 213 | Same four alternatives; lower label layout deferred. |
| `8.2.3.12/port-label/1` | 246 / 214 | Name-only/name-and-type parsing and placement deferred. |
| `8.2.3.12/proxy-v/1` | 246 / 214 | Two label positions; context-restricted layout deferred. |
| `8.2.3.12/proxy-h/1` | 246 / 214 | Two label positions; context-restricted layout deferred. |

Each row's original source is [the pinned OMG PDF](https://www.omg.org/spec/SysML/2.0/Language/PDF); use its PDF page number in `#page=` links. Units remain distinct even where a table and production describe related alternatives.

## Safe asset additions and remaining ambiguity

The immediate safe gap is a **minimal `port-definition` SVG**: reuse the established sharp-corner definition template with the port-definition keyword, editable name, original metadata and anchors. It should explicitly exclude compartments, aliases, prefix combinations and boundary/nested ports. A conjugated full-usage example can use the existing editable label slot as a demonstrator; that does not add parsing support for conjugated types.

Direction-arrow primitives could be added without asserting model semantics, but complete boundary-port components also require side-specific labels, containment restrictions, nested layout and direction-selection rules. Reference/proxy drawing should remain deferred until those responsibilities have an explicit interface. A compartment renderer needs its own row/layout contract rather than a flattened text field.

The original §8.2.3.12 extension says `interconnection-element =| port-def | port`, while the full usage production in this section is named `port-usage`. This audit records the mismatch and does not substitute one identifier for the other. The extension operator `=|` is also preserved as printed; it must not be normalized to ordinary `=` in extraction. [PDF 243 / printed 211](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=243).

## Implementation reconciliation

The descriptions above record the initial source-review findings. The current [per-alternative ledger](../parts-ports-notation-audit.md) is authoritative for asset/deferral status after implementation: it includes minimal PortDefinition, selected two-row compartment nodes and direction-bearing boundary glyphs. Broader layouts and imported grammar are still deferred as recorded there. See the [connected reference](../parts-and-ports.md) and [SVG library](../svg-shapes.html).
