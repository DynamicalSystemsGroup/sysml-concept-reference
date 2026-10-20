# Property normalization rules from official UML and SysML sources

Research date: 2026-10-21. Scope: decoding UML-serialized metamodel declarations and explaining SysML usages. These are distinct levels: the UML multiplicity of a metamodel property is not the multiplicity of a usage in a user model.

## Pinned sources

OMG lists the following normative machine-readable documents on its [UML 2.5.1 publication page](https://www.omg.org/spec/UML/2.5.1). Local copies are in ignored `sandbox/official-sources/`.

| Artifact | Official URL / document ID | Bytes | SHA-256 |
|---|---|---:|---|
| UML abstract syntax | https://www.omg.org/spec/UML/20161101/UML.xmi — ptc/18-01-01 | 1901856 | `e8166c91f51b8a0c015a90101b83d2249d03252e9f9a500a6511654347804f21` |
| Primitive types | https://www.omg.org/spec/UML/20161101/PrimitiveTypes.xmi — ptc/18-01-02 | 2880 | `62d12217fcd26037fc917709e2a896600af574efd6412c110e2a711395a69849` |
| UML 2.5.1 specification | https://www.omg.org/spec/UML/2.5.1/PDF — formal/17-12-05 | 18069510 | `416b57e1933780eb48bd60fe513e031da220c28a521bdd334a366bebc78a463e` |
| SysML 2.0 Part 1 | https://www.omg.org/spec/SysML/2.0/Language/PDF | See shared source manifest | See shared source manifest |

Page references below are printed specification pages, not PDF viewer page numbers. XMI fragment identifiers are exact `xmi:id` values.

## Decode declarations before interpreting values

1. **Absent bound specification:** UML `MultiplicityElement::lowerBound()` and `upperBound()` yield 1 when their respective value specification is absent (or its value query yields null). Thus an `ownedAttribute` with neither bound node has effective UML multiplicity `[1..1]`. Evidence: UML §7.8.8.7, pp. 46–47; XMI fragments [MultiplicityElement-lowerBound](https://www.omg.org/spec/UML/20161101/UML.xmi#MultiplicityElement-lowerBound), [MultiplicityElement-upperBound](https://www.omg.org/spec/UML/20161101/UML.xmi#MultiplicityElement-upperBound).
2. **Present literal with omitted `value`:** resolve the literal metaclass's value-property default. `LiteralInteger` defaults to 0; `LiteralUnlimitedNatural` defaults to 0; `LiteralBoolean` defaults to false. A present `<lowerValue xmi:type="uml:LiteralInteger"/>` therefore means lower 0, not lower 1. Evidence: UML §8.6.8.4 and §8.6.9.4, p. 83; §8.6.14.4, p. 86; XMI fragments [LiteralBoolean-value](https://www.omg.org/spec/UML/20161101/UML.xmi#LiteralBoolean-value), [LiteralInteger-value](https://www.omg.org/spec/UML/20161101/UML.xmi#LiteralInteger-value), [LiteralUnlimitedNatural-value](https://www.omg.org/spec/UML/20161101/UML.xmi#LiteralUnlimitedNatural-value).
3. **String exception:** `LiteralString::value` has multiplicity `[0..1]` and no declared default. A missing `value` must be recorded as absent/unresolved rather than invented as an empty string. Explicit `value=""` is a different serialization state. Evidence: UML §8.6.13.4–5, p. 85; [LiteralString-value](https://www.omg.org/spec/UML/20161101/UML.xmi#LiteralString-value).
4. **No declared property default:** absent `defaultValue` means no default specification is declared on that property. Do not fabricate zero or false merely because its type is Integer or Boolean. A *present* Boolean literal default node lacking `value` does declare false by rule 2. `Property::defaultValue` is optional `[0..1]`. Evidence: UML §9.9.17.6, p. 150; [Property-defaultValue](https://www.omg.org/spec/UML/20161101/UML.xmi#Property-defaultValue).
5. **Preserve provenance:** retain raw serialization presence, normalized value and the UML rule used to supply a missing serialized attribute. A normalized default is not an explicit serialized value. This is an inventory design recommendation derived from the distinctions above.

## UML property-qualifier defaults

| Omitted qualifier | Normalized value | Evidence |
|---|---|---|
| `isOrdered` | false | UML §7.8.8.5, p. 45; `MultiplicityElement-isOrdered` |
| `isUnique` | true | UML §7.8.8.5, p. 45; `MultiplicityElement-isUnique` |
| `isDerived` | false | UML §9.9.17.5, p. 149; `Property-isDerived` |
| `isDerivedUnion` | false | UML §9.9.17.5, p. 149; `Property-isDerivedUnion` |
| `isReadOnly` | false | UML §9.9.21.5, p. 156; `StructuralFeature-isReadOnly` |
| `aggregation` | none | UML §9.9.17.5, p. 149; `Property-aggregation` |

All identifiers in this table resolve against the [official UML XMI](https://www.omg.org/spec/UML/20161101/UML.xmi). `isComposite` is derived from `aggregation = composite` (§9.9.17.7, p. 151; `Property-isComposite.1`); it must not be inferred merely from the declaring class or from a nested XML element. A derived property is not automatically read-only: preserve the independent qualifiers.

## Effective inherited properties and collisions

UML §9.2.3.2–3, p. 100, explains that non-private members are inherited unless a particular kind specifies otherwise. Redefining members contribute in place of their redefined members; a member may redefine multiple elements and an element may be redefined several times only when the applicable definition remains unambiguous. This is identity-based replacement, not name-based deduplication. See [UML PDF](https://www.omg.org/spec/UML/2.5.1/PDF).

The executable-shape evidence is in `Classifier::hasVisibilityOf`, `inherit`, `inheritableMembers` and `inheritedMember`, UML §9.9.4.7, pp. 133–134, with exact XMI fragments [Classifier-hasVisibilityOf](https://www.omg.org/spec/UML/20161101/UML.xmi#Classifier-hasVisibilityOf), [Classifier-inherit](https://www.omg.org/spec/UML/20161101/UML.xmi#Classifier-inherit), [Classifier-inheritableMembers](https://www.omg.org/spec/UML/20161101/UML.xmi#Classifier-inheritableMembers), [Classifier-inheritedMember.1](https://www.omg.org/spec/UML/20161101/UML.xmi#Classifier-inheritedMember.1).

Actionable inventory algorithm:

- Traverse immediate generalizations recursively; retain declaration identities and all inheritance paths.
- Deduplicate the same declaration identity reached through diamonds.
- Exclude private inherited members and explicitly redefined inherited identities in the relevant class context.
- Retain replaced declarations in a separate provenance/history view.
- Do not treat same-name properties as replacements without redefinition evidence. Report unresolved competing declarations for review; never choose whichever traversal encounters last.

Namespace members must be distinguishable (UML §7.8.10.7, p. 51; `Namespace-members_distinguishable`). Imported-member collision exclusion is a separate operation and must not be mistaken for inherited-property replacement.

`Property::isConsistentWith`, UML §9.9.17.7, p. 151 ([XMI](https://www.omg.org/spec/UML/20161101/UML.xmi#Property-isConsistentWith)), says in prose that the redefining type conforms to the redefined type, and its specified multiplicity is contained in the original multiplicity. The OCL in both PDF and XMI contains an apparent defect: the upper-bound conditional compares lower bounds (`prop.lowerBound() <= self.lowerBound()`) rather than upper bounds. Preserve this discrepancy in evidence; do not silently claim faithful execution of the normative OCL or use it as an unquestioned validation oracle. The stated containment intent implies the narrower interval, but adopting a corrected condition is an explicit implementation interpretation.

## SysML usage semantics: separate from UML serialization defaults

SysML §7.6.3, pp. 40–42, provides these textual/modeling rules ([official PDF](https://www.omg.org/spec/SysML/2.0/Language/PDF)):

- Usage typing, subsetting and redefinition are distinct specializations. Redefinition is a kind of subsetting.
- Missing usage multiplicity inherits constraints from subsetted/redefined usages. Without tighter inherited constraints, its effective default is `[0..*]`.
- An implicit tighter `[1..1]` applies only when all three conditions hold: it is an attribute, item (including part, excluding connection) or port usage; it is owned by a definition or usage rather than a package; and it has no explicit owned subsettings or redefinitions.
- `nonunique` and `ordered` override the default unique/unordered usage semantics.
- `ref` indicates referential rather than composite usage. Composite values cannot outlive their featuring occurrence and cannot simultaneously belong to a different composite usage unless the featuring instance is the same. A composite usage must be featured by an occurrence.
- Directed usages are always referential, even without explicit `ref`.
- Nested usages in a usage body are owned usages and features of the owning usage. This ownership statement does not imply composition of the modeled values.

A `ReferenceUsage` (the concept used without a kind keyword) is always referential, with or without explicit `ref`; a referential `PartUsage` remains a `PartUsage`. Evidence: §7.6.4, p. 42.

`Usage` may own nested definitions; the specification assigns them namespace scoping significance rather than feature semantics. `Usage::isReference = not isComposite`. Evidence: §8.3.6.4, pp. 269–273, especially Usage description and `deriveUsageIsReference` ([official PDF](https://www.omg.org/spec/SysML/2.0/Language/PDF)).

`PartUsage` specializes `ItemUsage`, must have at least one item definition that is a `PartDefinition`, and must directly or indirectly specialize `Parts::parts`. The declaration of `partDefinition` is `[0..*]` even though the class-level constraints demand at least one suitable definition; do not overwrite declaration multiplicity to hide that distinction. Actor/stakeholder contexts add specialization requirements. Evidence: §8.3.11.3, pp. 290–291 ([official PDF](https://www.omg.org/spec/SysML/2.0/Language/PDF)).

## Limits

These rules support declaration normalization and an evidence-backed browser; they do not constitute a complete UML interpreter, SysML compiler or semantic conformance checker. Unsupported expressions and unresolved external references should remain explicit rather than receiving guessed values.
