# Verified notation evidence for the first four concept pages

## Source and verification

Official source: [OMG SysML 2.0, Part 1: Language](https://www.omg.org/spec/SysML/2.0/Language/PDF), document **formal/2026-03-02**, March 2026. Retrieved 2026-10-21 into ignored `sandbox/official-sources/SysML-Language.pdf`; 3,804,140 bytes; SHA-256 `46e6c0476a6f1f34f367d57e039d56659bff75e41d2e4b3d37ca4cadea84a83a`.

PDF page numbers below are one-based viewer pages. Printed pages have a 32-page offset in the inspected sections. Text was extracted with Poppler; rendered full pages 90, 91, 97, 98 and 241-248 were visually inspected. This is a verified first slice, not a claim of comprehensive notation coverage.

## Shapes and contexts

| Concept / variant | Verified rendering and relevant context | Evidence |
|---|---|---|
| PartDefinition | Sharp-corner rectangle; name area contains `«part def»` and definition name. It can include compartments, an interconnection view and ports on any side. | §7.11.1 Table 9, printed 58 / [PDF 90](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=90); §8.2.3.11, printed 209 / [PDF 241](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=241) |
| PartUsage | Rounded rectangle; `«part»`, followed by usage declaration such as `engine : Engine`. The grammar also draws a dashed-outline rounded `part-ref` variant with the same name-compartment production; a referential usage label is `«ref part»` (prefix resolution below). Compartments/interconnection contents and side ports are supported. Do not make the dashed outline the universal symbol for model references of every kind. | Table 9, printed 59 / [PDF 91](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=91); §8.2.3.11, printed 209 / [PDF 241](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=241) |
| PortUsage, full node | Rounded rectangle with `«port»` and usage declaration; compartment stack and nested side ports are available. | §8.2.3.12, printed 210-211 / [PDF 242](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=242), [PDF 243](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=243) |
| PortUsage, boundary glyph | Small rounded rectangular boundary glyph with adjacent name/type label; can appear at left, right, top or bottom. Larger elongated glyphs allow nested ports. Direction productions include single arrows in either orientation and bidirectional arrows; arrows need not be shown on a minimal undirected example. | §8.2.3.12, printed 211-213 / [PDF 243](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=243), [PDF 244](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=244), [PDF 245](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=245); Table 9 example, printed 59 / [PDF 91](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=91) |
| Port reference / proxy variants | Dotted-outline port productions are restricted to nested ports. The filled-dot proxy option is valid only on a part usage within an interconnection view. These restrictions must accompany examples of those variants. | Explicit notes in §8.2.3.12, printed 214 / [PDF 246](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=246) |
| ConnectionUsage, node | Rounded rectangle containing `«connection»` and usage declaration, with optional compartments. Representative notation includes an `ends` compartment with reference-subsetting declarations. | §7.13.1 Table 11, printed 66 / [PDF 98](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=98); §8.2.3.13, printed 215 / [PDF 247](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=247) |
| ConnectionUsage, binary edge | Solid line between connection ends; optional connection label; end role names, multiplicities and adornments. Grammar includes an open-arrow direction-indication alternative. For a basic example use a plain line and do not imply that every connection is a directed flow. | §8.2.3.13, printed 215-216 / [PDF 247](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=247), [PDF 248](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=248); Table 11, printed 66 / [PDF 98](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=98) |
| ConnectionUsage, n-ary edge | Filled central dot with labeled segments to usage nodes; usage declaration labels the dot. This is an additional representation, not a replacement for the binary line or node. | §8.2.3.13, printed 216 / [PDF 248](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=248) |

Graphical compartments can render selected members textually or graphically; diagram contents depend on the view and its filters. Accordingly, graphical nesting alone should not become a universal RDF assertion of ownership or composition. See §8.2.3.1, printed 193 / [PDF 225](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=225).

## Textual examples and restrictions

- **PartDefinition / PartUsage:** §7.11.1-7.11.2, printed 58-61 / [PDF 90](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=90), [PDF 92](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=92), [PDF 93](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=93). The keyword is `part`. Part usages may be typed by item definitions (including part definitions) or KerML structures. The default multiplicity is conditional under §7.6.3, not universally 1..1. The official Vehicle example distinguishes a referential driver from engine/wheels. Every part usage also has at least one part-definition typing, possibly implicit through the base library usage.
- **PortUsage:** §7.12.2-7.12.3, printed 63 / [PDF 95](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=95). The keyword is `port`; only port definitions may type it. Non-port features inside ports must be referential; nested ports are the exception. Default multiplicity again depends on §7.6.3. A conjugated usage uses `~` before its port-definition name; in/out reverse, inout remains unchanged. An ordinary unqualified port is sufficient for the first illustrative redraw.
- **ConnectionUsage:** §7.13.2, printed 68 / [PDF 100](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=100). The keyword is `connection`; typing is restricted to connection definitions or KerML association structures. Nonabstract connections require at least two end features. Ends are referential and individually have multiplicity 1..1. Reference subsetting (`references` / `::>`) associates ends to connected features. **Cross multiplicity is distinct from end multiplicity**, as clarified on printed 70 / [PDF 102](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=102).

## Suggested original illustrative example

Use a sharp `«part def» Vehicle` box containing rounded `«part» engine : Engine` and `«part» controller : Controller` boxes. Draw small rounded boundary ports with adjacent labels, joined by a plain solid connection line with a usage label. Provide the equivalent textual declaration alongside it. A separate rounded dashed `«ref part» driver : Person` box can demonstrate referential structure, with its own source and explanation.

These would be **original illustrative redraws based on the cited notation**, with new names/layout and no embedded official figure. Label them accordingly. They are documentation examples; they must not be marked parser-validated unless actually run through a SysML implementation. No connection arrow is necessary; the inspected grammar establishes a direction-indication variant, but this slice does not establish every semantic condition for choosing it.

## Prefix resolution and proposed connected example

The exact §8.2.3.11 production on printed 209 / [PDF 241](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=241) is `part-name-compartment = '«' OccurrenceUsagePrefix 'part' '»' usage-name-with-alias`; both solid `part` and dashed `part-ref` use this production. `OccurrenceUsagePrefix` includes `BasicUsagePrefix` (§8.2.2.9.2, printed 174 / [PDF 206](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=206)); that prefix includes optional `ref` (§8.2.2.6.2, printed 169 / [PDF 201](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=201)). Thus the corresponding referential example label is **`«ref part»`**, not unconditionally `«part»`. Table 11 explicitly shows `«ref part»` on printed 68 / [PDF 100](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=100).

The following original example is source-consistent with the binary shorthand in §7.13.2, printed 71 / [PDF 103](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=103), and the part/port declaration forms cited above. It has not been parser-validated:

```sysml
port def Mount;
part def Wheel { port hub : Mount; }
part def Axle { port mount : Mount; }
part def Assembly {
    part wheel : Wheel;
    part axle : Axle;
    connection link connect axle.mount to wheel.hub;
}
```

Label the plain connection edge `link`, with adjacent boundary-port labels `mount : Mount` and `hub : Mount`. The edge label production is `UsageDeclaration`, so the graphical label omits the declaration keywords `connection` and `connect`; see §8.2.3.13, printed 215-216 / [PDF 247](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=247), [PDF 248](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=248). A full connection node instead uses `«connection»` and `link` in its name compartment. Because this example gives no explicit connection type, do not invent `: ConnectionDef` in the edge or node label. Its implicit binary base comes from the library as described on printed 71.
