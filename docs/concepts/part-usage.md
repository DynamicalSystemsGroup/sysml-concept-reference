# PartUsage

Status: **draft, source-checked**. Editorial explanation with separately identified source declarations and original illustrative redraws.

Describes a system or system part in a context. A definition describes its kind; multiple usages can share that kind.

[Original XMI declaration](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-Parts-PartUsage). [§7.11 Parts, printed 58 / PDF 90](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=90); [§8.3.11.3 PartUsage, printed 289 / PDF 321](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=321)

## What to understand

- A referential part remains a PartUsage. It is not converted into the metaclass ReferenceUsage just because its declaration contains ref.
- Owning a part declaration, featuring its values, and making those values composite are separate mechanisms.
- The declared partDefinition property has multiplicity 0..*. Class-level constraints still require at least one applicable PartDefinition typing; declaration cardinality alone is not the whole rule.
- The normalized defaults below describe metamodel fields. The multiplicity and composition of a part in a user model follow contextual SysML rules.

## Connected example

wheel is a composite part usage within Assembly. spare is an owned but referential part usage. Both are typed by Wheel; the [0..1] on spare explicitly constrains its modeled values.

```sysml
// Original documentation example. Source-reviewed; not parser-validated.
package AssemblyExample {
    port def Mount;

    part def Wheel {
        port hub : Mount;
    }

    part def Axle {
        port mount : Mount;
    }

    part def Assembly {
        part wheel : Wheel;
        part axle : Axle;
        ref part spare : Wheel[0..1];
        connection link connect axle.mount to wheel.hub;
    }

    part assembly : Assembly;
}
```

Verification: **source-reviewed, not parser-validated or executed**. [§7.6.3 Usages, printed 40 / PDF 72](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=72); [§7.11.2 Part Definitions and Usages, printed 61 / PDF 93](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=93)

## Relationships and composition

### Typing: [PartDefinition](part-definition.md)

A part usage has applicable part-definition typing, explicit or supplied through its semantic specialization.

Condition: Do not restrict every allowed explicit type to PartDefinition; the source also permits qualifying item definitions and kernel structures.

[§7.11.2, printed 61 / PDF 93](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=93)

### Nested declaration: [PartUsage](part-usage.md)

A part usage can declare nested part usages as features in its context.

Condition: Permitted examples do not establish that every nesting is valid; membership, featuring and composition constraints still apply.

[§7.6.3, printed 41 / PDF 73](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=73)

### Nested port: [PortUsage](port-usage.md)

Ports can be declared within a part usage or its defining type.

Condition: The port typing and context-specific referentiality rules apply independently of the enclosing part.

[§7.12.2–3, printed 63 / PDF 95](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=95)

## Graphical notation

These are representative, source-checked variants, not an exhaustive notation grammar. The illustrations are original redraws, not official figures.

### Composite and referential part usages

Context: Usage nodes in structural views.

Rounded rectangle with a part usage label. The referential variant has a dashed outline and the ref prefix. Compartments and side ports are additional variants.

![Composite and referential part usages](../assets/notation/part-usage.svg)

[§8.2.3.11 Parts, printed 209 / PDF 241](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=241)

## Properties

The explicit-redefinition view contains **113 active declarations**, retaining declaration origins and excluding 3 replaced declarations. It deduplicates diamond paths by identity, excludes private inherited fields, and reports unresolved same-name collisions instead of choosing a winner.

**These are metamodel property cardinalities and declared defaults.** They do not determine the multiplicity or runtime values of a part, port or connection in a user model. Derived values still require their derivation rules. See [property rules](../research/property-rules.md).

| Property | Meaning | Type | Bounds | Declared on | Declared default |
|---|---|---|---|---|---|
| [aliasIds](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-aliasIds) | Alternative identifiers for this element, typically supplied by tools. | String | 0..* | Element | No declared default |
| [chainingFeature](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Features-Feature-chainingFeature) | The ordered features whose successive navigation determines this feature’s modeled values. | Feature | 0..* | Feature | No declared default |
| [crossFeature](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Features-Feature-crossFeature) | The navigational feature constraining collections reached across the other ends of the same owning type. | Feature | 0..1 | Feature | No declared default |
| [declaredName](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-declaredName) | The primary name explicitly supplied for this element. | String | 0..1 | Element | No declared default |
| [declaredShortName](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-declaredShortName) | An explicitly supplied compact alternative name whose contextual uniqueness is the modeler’s responsibility. | String | 0..1 | Element | No declared default |
| [differencingType](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-differencingType) | The ordered types defining this type as the first type’s interpretations minus those of subsequent types. | Type | 0..* | Type | No declared default |
| [directedFeature](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-directedFeature) | The features of this type with an explicit direction. | Feature | 0..* | Type | No declared default |
| [directedUsage](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-directedUsage) | The usage features in this context that have an explicit direction. | Usage | 0..* | Usage | No declared default |
| [direction](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Features-Feature-direction) | Describes whether modeled feature values serve as inputs, outputs, or both. | FeatureDirectionKind | 0..1 | Feature | No declared default |
| [documentation](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-documentation) | The documentation elements owned by this element. | Documentation | 0..* | Element | No declared default |
| [elementId](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-elementId) | The tooling-assigned global identifier intended to remain stable for this element’s lifetime. | String | 1..1 | Element | No declared default |
| [endFeature](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-endFeature) | The features of this type marked as ends. | Feature | 0..* | Type | No declared default |
| [endOwningType](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Features-Feature-endOwningType) | The type owning this feature through an end-feature membership. | Type | 0..1 | Feature | No declared default |
| [feature](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-feature) | The features available through this type’s feature memberships, including inherited features. | Feature | 0..* | Type | No declared default |
| [featureMembership](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-featureMembership) | The owned and inherited feature memberships of this type, excluding imported memberships. | FeatureMembership | 0..* | Type | No declared default |
| [featureTarget](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Features-Feature-featureTarget) | The final feature in this feature’s navigation chain, or this feature when no chain exists. | Feature | 1..1 | Feature | No declared default |
| [featuringType](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Features-Feature-featuringType) | The types that every domain instance from which this feature is evaluated must satisfy. | Type | 0..* | Feature | No declared default |
| [importedMembership](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Namespaces-Namespace-importedMembership) | The memberships made available by imports owned by this namespace. | Membership | 0..* | Namespace | No declared default |
| [individualDefinition](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-Occurrences-OccurrenceUsage-individualDefinition) | The optional occurrence definition typing this usage that is marked individual. | OccurrenceDefinition | 0..1 | OccurrenceUsage | No declared default |
| [inheritedFeature](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-inheritedFeature) | The features obtained through inherited feature memberships. | Feature | 0..* | Type | No declared default |
| [inheritedMembership](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-inheritedMembership) | The memberships made available to this type by specialization or conjugation. | Membership | 0..* | Type | No declared default |
| [input](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-input) | The features of this type directed into the type, including bidirectional features. | Feature | 0..* | Type | No declared default |
| [intersectingType](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-intersectingType) | The types whose shared interpretations define this type. | Type | 0..* | Type | No declared default |
| [isAbstract](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-isAbstract) | Requires every instance of this type to also instantiate a more specialized type. | Boolean | 1..1 | Type | false (LiteralBoolean) |
| [isComposite](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Features-Feature-isComposite) | Makes modeled values dependent on their featuring instance for continued existence and exclusive to that instance across composite features. | Boolean | 1..1 | Feature | false (LiteralBoolean) |
| [isConjugated](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-isConjugated) | Records whether this type owns a conjugation as its conjugator. | Boolean | 1..1 | Type | No declared default |
| [isConstant](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Features-Feature-isConstant) | Keeps the modeled value unchanged across snapshots even when the feature is variable. | Boolean | 1..1 | Feature | false (LiteralBoolean) |
| [isDerived](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Features-Feature-isDerived) | Indicates that modeled values of this feature are always computable from other feature values. | Boolean | 1..1 | Feature | false (LiteralBoolean) |
| [isEnd](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Features-Feature-isEnd) | Marks a feature as an end, mapping each domain instance to one value; navigation cardinality can additionally be constrained through its cross feature. | Boolean | 1..1 | Feature | false (LiteralBoolean) |
| [isImpliedIncluded](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-isImpliedIncluded) | Records that all required implied owned relationships are included; false requires that none be included. | Boolean | 1..1 | Element | false (LiteralBoolean) |
| [isIndividual](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-Occurrences-OccurrenceUsage-isIndividual) | Identifies a usage of the specific individual designated by its individual definition. | Boolean | 1..1 | OccurrenceUsage | false (LiteralBoolean) |
| [isLibraryElement](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-isLibraryElement) | Indicates that this element lies within the ownership tree of a library model. | Boolean | 1..1 | Element | No declared default |
| [isOrdered](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Features-Feature-isOrdered) | Records whether the modeled feature values have a meaningful sequence. | Boolean | 1..1 | Feature | false (LiteralBoolean) |
| [isPortion](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Features-Feature-isPortion) | Indicates that modeled values are spatial or temporal portions of their domain instance and represent that same thing. | Boolean | 1..1 | Feature | false (LiteralBoolean) |
| [isReference](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-isReference) | The derived opposite of isComposite, identifying usage values without composite lifetime dependence. | Boolean | 1..1 | Usage | No declared default |
| [isSufficient](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-isSufficient) | Makes satisfying this type’s classification conditions sufficient for classification by the type. | Boolean | 1..1 | Type | false (LiteralBoolean) |
| [isUnique](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Features-Feature-isUnique) | Requires the modeled collection of feature values to contain no repeated values when true. | Boolean | 1..1 | Feature | true (LiteralBoolean) |
| [isVariation](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-isVariation) | Marks a variation point and requires its relevant memberships to be variant memberships. | Boolean | 1..1 | Usage | No declared default |
| [itemDefinition](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-Items-ItemUsage-itemDefinition) | The structures typing this item usage, including compatible KerML library structures. | Structure | 0..* | ItemUsage | No declared default |
| [mayTimeVary](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-mayTimeVary) | The derived replacement for Feature.isVariable indicating snapshot-based featuring; isConstant can still require the same value throughout an occurrence. | Boolean | 1..1 | Usage | No declared default |
| [member](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Namespaces-Namespace-member) | The elements available as members through this namespace’s memberships. | Element | 0..* | Namespace | No declared default |
| [membership](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Namespaces-Namespace-membership) | The memberships available in this namespace, including owned and imported memberships. | Membership | 0..* | Namespace | No declared default |
| [multiplicity](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-multiplicity) | The owned multiplicity constraining this type’s modeled cardinality; without one, applicable supertype multiplicities still constrain it. | Multiplicity | 0..1 | Type | No declared default |
| [name](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-name) | The effective name used for namespace lookup, which some element kinds compute rather than declare. | String | 0..1 | Element | No declared default |
| [nestedAction](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-nestedAction) | The action usages owned as features by this usage. | ActionUsage | 0..* | Usage | No declared default |
| [nestedAllocation](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-nestedAllocation) | The allocation usages owned as features by this usage. | AllocationUsage | 0..* | Usage | No declared default |
| [nestedAnalysisCase](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-nestedAnalysisCase) | The analysis case usages owned as features by this usage. | AnalysisCaseUsage | 0..* | Usage | No declared default |
| [nestedAttribute](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-nestedAttribute) | The attribute usages owned as features by this usage. | AttributeUsage | 0..* | Usage | No declared default |
| [nestedCalculation](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-nestedCalculation) | The calculation usages owned as features by this usage. | CalculationUsage | 0..* | Usage | No declared default |
| [nestedCase](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-nestedCase) | The case usages owned as features by this usage. | CaseUsage | 0..* | Usage | No declared default |
| [nestedConcern](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-nestedConcern) | The concern usages owned as features by this usage. | ConcernUsage | 0..* | Usage | No declared default |
| [nestedConnection](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-nestedConnection) | The connector-as-usages, including binding, succession and flow usages owned as features by this usage. | ConnectorAsUsage | 0..* | Usage | No declared default |
| [nestedConstraint](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-nestedConstraint) | The constraint usages owned as features by this usage. | ConstraintUsage | 0..* | Usage | No declared default |
| [nestedEnumeration](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-nestedEnumeration) | The enumeration usages owned as features by this usage. | EnumerationUsage | 0..* | Usage | No declared default |
| [nestedFlow](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-nestedFlow) | The flow usages owned as features by this usage. | FlowUsage | 0..* | Usage | No declared default |
| [nestedInterface](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-nestedInterface) | The interface usages owned as features by this usage. | InterfaceUsage | 0..* | Usage | No declared default |
| [nestedItem](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-nestedItem) | The item usages owned as features by this usage. | ItemUsage | 0..* | Usage | No declared default |
| [nestedMetadata](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-nestedMetadata) | The metadata usages owned as features by this usage. | MetadataUsage | 0..* | Usage | No declared default |
| [nestedOccurrence](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-nestedOccurrence) | The occurrence usages owned as features by this usage. | OccurrenceUsage | 0..* | Usage | No declared default |
| [nestedPart](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-nestedPart) | The part usages owned as features by this usage. | PartUsage | 0..* | Usage | No declared default |
| [nestedPort](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-nestedPort) | The port usages owned as features by this usage. | PortUsage | 0..* | Usage | No declared default |
| [nestedReference](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-nestedReference) | The reference usages owned as features by this usage. | ReferenceUsage | 0..* | Usage | No declared default |
| [nestedRendering](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-nestedRendering) | The rendering usages owned as features by this usage. | RenderingUsage | 0..* | Usage | No declared default |
| [nestedRequirement](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-nestedRequirement) | The requirement usages owned as features by this usage. | RequirementUsage | 0..* | Usage | No declared default |
| [nestedState](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-nestedState) | The state usages owned as features by this usage. | StateUsage | 0..* | Usage | No declared default |
| [nestedTransition](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-nestedTransition) | The transition usages owned as features by this usage. | TransitionUsage | 0..* | Usage | No declared default |
| [nestedUsage](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-nestedUsage) | The usage features owned by this usage. | Usage | 0..* | Usage | No declared default |
| [nestedUseCase](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-nestedUseCase) | The use case usages owned as features by this usage. | UseCaseUsage | 0..* | Usage | No declared default |
| [nestedVerificationCase](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-nestedVerificationCase) | The verification case usages owned as features by this usage. | VerificationCaseUsage | 0..* | Usage | No declared default |
| [nestedView](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-nestedView) | The view usages owned as features by this usage. | ViewUsage | 0..* | Usage | No declared default |
| [nestedViewpoint](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-nestedViewpoint) | The viewpoint usages owned as features by this usage. | ViewpointUsage | 0..* | Usage | No declared default |
| [occurrenceDefinition](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-Occurrences-OccurrenceUsage-occurrenceDefinition) | The classes typing this occurrence usage, including compatible KerML library classes. | Class | 0..* | OccurrenceUsage | No declared default |
| [output](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-output) | The features of this type directed out of the type, including bidirectional features. | Feature | 0..* | Type | No declared default |
| [ownedAnnotation](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-ownedAnnotation) | The annotation relationships owned here that annotate this element. | Annotation | 0..* | Element | No declared default |
| [ownedConjugator](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-ownedConjugator) | The optional conjugation owned here that treats this type as the original type. | Conjugation | 0..1 | Type | No declared default |
| [ownedCrossSubsetting](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Features-Feature-ownedCrossSubsetting) | The optional owned cross-subsetting relationship specifying this feature’s cross-navigation constraint. | CrossSubsetting | 0..1 | Feature | No declared default |
| [ownedDifferencing](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-ownedDifferencing) | The owned difference relationships defining this type as their difference result. | Differencing | 0..* | Type | No declared default |
| [ownedDisjoining](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-ownedDisjoining) | The owned disjointness relationships constraining this type against other types. | Disjoining | 0..* | Type | No declared default |
| [ownedElement](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-ownedElement) | The elements reached as owned related elements through this element’s owned relationships. | Element | 0..* | Element | No declared default |
| [ownedEndFeature](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-ownedEndFeature) | The end features introduced through memberships owned by this type. | Feature | 0..* | Type | No declared default |
| [ownedFeature](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-ownedFeature) | The features introduced through feature memberships owned by this type. | Feature | 0..* | Type | No declared default |
| [ownedFeatureChaining](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Features-Feature-ownedFeatureChaining) | The owned relationships specifying the ordered steps used to navigate this feature. | FeatureChaining | 0..* | Feature | No declared default |
| [ownedFeatureInverting](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Features-Feature-ownedFeatureInverting) | The owned relationships that give this feature an inverse navigation interpretation. | FeatureInverting | 0..* | Feature | No declared default |
| [ownedFeatureMembership](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-ownedFeatureMembership) | The memberships owned here that introduce owned features of this type. | FeatureMembership | 0..* | Type | No declared default |
| [ownedImport](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Namespaces-Namespace-ownedImport) | The import relationships owned by this namespace. | Import | 0..* | Namespace | No declared default |
| [ownedIntersecting](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-ownedIntersecting) | The owned intersection relationships defining this type as their intersection result. | Intersecting | 0..* | Type | No declared default |
| [ownedMember](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Namespaces-Namespace-ownedMember) | The member elements owned through this namespace’s owned memberships. | Element | 0..* | Namespace | No declared default |
| [ownedMembership](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Namespaces-Namespace-ownedMembership) | The memberships owned by this namespace. | Membership | 0..* | Namespace | No declared default |
| [ownedRedefinition](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Features-Feature-ownedRedefinition) | The owned subsetting relationships that replace inherited features with this redefining feature. | Redefinition | 0..* | Feature | No declared default |
| [ownedReferenceSubsetting](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Features-Feature-ownedReferenceSubsetting) | The optional owned reference-subsetting relationship identifying the feature referenced by this feature. | ReferenceSubsetting | 0..1 | Feature | No declared default |
| [ownedRelationship](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-ownedRelationship) | The relationships owned by this element as their owning related element. | Relationship | 0..* | Element | No declared default |
| [ownedSpecialization](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-ownedSpecialization) | The owned specialization relationships in which this type is the more specific type. | Specialization | 0..* | Type | No declared default |
| [ownedSubsetting](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Features-Feature-ownedSubsetting) | The owned specializations that constrain this feature to select values from another feature. | Subsetting | 0..* | Feature | No declared default |
| [ownedTypeFeaturing](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Features-Feature-ownedTypeFeaturing) | The owned type-featuring relationships that explicitly identify contexts featuring this feature. | TypeFeaturing | 0..* | Feature | No declared default |
| [ownedTyping](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Features-Feature-ownedTyping) | The owned feature-typing relationships that constrain the types of this feature’s modeled values. | FeatureTyping | 0..* | Feature | No declared default |
| [ownedUnioning](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-ownedUnioning) | The owned union relationships defining this type as their union result. | Unioning | 0..* | Type | No declared default |
| [owner](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-owner) | The owning related element reached through this element’s owning relationship, which need not be a namespace. | Element | 0..1 | Element | No declared default |
| [owningDefinition](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-owningDefinition) | The definition that directly owns this usage, when present. | Definition | 0..1 | Usage | No declared default |
| [owningFeatureMembership](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Features-Feature-owningFeatureMembership) | The membership that owns this feature as a feature of its owning type. | FeatureMembership | 0..1 | Feature | No declared default |
| [owningMembership](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-owningMembership) | The relationship owning this element when that relationship is a membership. | OwningMembership | 0..1 | Element | No declared default |
| [owningNamespace](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-owningNamespace) | The namespace obtained through this element’s owning membership, when that ownership route exists. | Namespace | 0..1 | Element | No declared default |
| [owningRelationship](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-owningRelationship) | The relationship that directly owns this element as a related element, if one exists. | Relationship | 0..1 | Element | No declared default |
| [owningType](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Features-Feature-owningType) | The type that owns this feature through its owning feature membership. | Type | 0..1 | Feature | No declared default |
| [owningUsage](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-owningUsage) | The enclosing usage that directly owns this nested usage, when present. | Usage | 0..1 | Usage | No declared default |
| [partDefinition](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-Parts-PartUsage-partDefinition) | The part definitions among this part usage’s item-definition types. | PartDefinition | 0..* | PartUsage | No declared default |
| [portionKind](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-Occurrences-OccurrenceUsage-portionKind) | Distinguishes a snapshot from a time slice of the featuring instance and requires an owning type when specified. | PortionKind | 0..1 | OccurrenceUsage | No declared default |
| [qualifiedName](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-qualifiedName) | The ownership-path name in KerML syntax, absent when the named ownership path or disambiguation conditions are not met. | String | 0..1 | Element | No declared default |
| [shortName](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-shortName) | The effective compact name used for namespace lookup, which some element kinds compute rather than declare. | String | 0..1 | Element | No declared default |
| [textualRepresentation](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-textualRepresentation) | The textual-representation annotations attached to this element. | TextualRepresentation | 0..* | Element | No declared default |
| [unioningType](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-unioningType) | The types whose combined interpretations equal this type’s interpretation. | Type | 0..* | Type | No declared default |
| [usage](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-usage) | The usage features available in this context, including usages not owned here. | Usage | 0..* | Usage | No declared default |
| [variant](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-variant) | The usages offered as alternatives at this variation point; absent when it is not a variation point. | Usage | 0..* | Usage | No declared default |
| [variantMembership](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Usage-variantMembership) | The owned memberships introducing variants, required to be empty outside a variation point. | VariantMembership | 0..* | Usage | No declared default |

### Replaced declarations

- `KerML::Core::Features::Feature::isVariable` → `SysML::Systems::DefinitionAndUsage::Usage::mayTimeVary`
- `KerML::Core::Features::Feature::type` → `SysML::Systems::Occurrences::OccurrenceUsage::occurrenceDefinition`
- `SysML::Systems::DefinitionAndUsage::Usage::definition` → `SysML::Systems::Occurrences::OccurrenceUsage::occurrenceDefinition`

## Reconciliation and limits

Seed reconciliation: **SelectedFieldsMatch** for direct bases, declared property names/types/bounds/derivation/ordering/subsets/redefinitions, constraint names. This checks selected structural fields only; it does not approve the entire seed or all semantics.

- The examples have been checked against source notation, but no SysML parser or semantic engine was run.
- No exhaustive permission matrix or complete notation grammar is claimed.
- Effective property resolution covers explicit inheritance and redefinition identities; it does not evaluate constraint consistency, OCL derivations or executable behavior.

[Browse interactive properties](../concept-browser.html#https://github.com/DynamicalSystemsGroup/sysml-concept-reference/id/SysML/20250201/Systems-Parts-PartUsage) · [Concept-page contract](../concept-page-contract.md)
