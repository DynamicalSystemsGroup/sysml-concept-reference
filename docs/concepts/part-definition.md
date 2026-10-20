# PartDefinition

Status: **draft, source-checked**. Editorial explanation with separately identified source declarations and original illustrative redraws.

Defines a reusable kind of system or system part, including features that usages of that kind can have.

[Original XMI declaration](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-Parts-PartDefinition). [§7.11.1 Parts Overview, printed 58 / PDF 90](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=90); [§8.3.11.2 PartDefinition, printed 289 / PDF 321](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=321)

## What to understand

- A definition is a classifier; a part usage is a feature in context. They retain different metaclass identities.
- Declaring a nested definition introduces a scoped kind. It does not by itself declare a part usage.
- Properties of this metaclass describe the language definition, rather than arbitrary attributes such as a modeled wheel diameter.

## Connected example

Wheel, Axle and Assembly are part definitions. Their port and part declarations specify features; assembly : Assembly is a separate usage of the defined kind.

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

Verification: **source-reviewed, not parser-validated or executed**. [§7.11.2 Part Definitions and Usages, printed 61 / PDF 93](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=93)

## Relationships and composition

### Usage of a kind: [PartUsage](part-usage.md)

Part usages can use the kind introduced by a part definition.

Condition: Typing is distinct from model ownership; many usages can share the same definition.

[§7.11.2, printed 61 / PDF 93](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=93)

### Declared feature: [PortUsage](port-usage.md)

A part definition can declare port usages as features.

Condition: Port definitions determine permitted port typing; the enclosing declaration is not a substitute for that type.

[§7.12.2–3, printed 63 / PDF 95](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=95)

## Graphical notation

These are representative, source-checked variants, not an exhaustive notation grammar. The illustrations are original redraws, not official figures.

### Part definition node

Context: Definition node in a structural view.

Sharp-corner rectangle with the part def keyword and definition name. Compartment and interconnection contents may extend the basic node.

![Part definition node](../assets/notation/part-definition.svg)

[§8.2.3.11 Parts, printed 209 / PDF 241](https://www.omg.org/spec/SysML/2.0/Language/PDF#page=241)

## Properties

The explicit-redefinition view contains **82 active declarations**, retaining declaration origins and excluding 0 replaced declarations. It deduplicates diamond paths by identity, excludes private inherited fields, and reports unresolved same-name collisions instead of choosing a winner.

**These are metamodel property cardinalities and declared defaults.** They do not determine the multiplicity or runtime values of a part, port or connection in a user model. Derived values still require their derivation rules. See [property rules](../research/property-rules.md).

| Property | Meaning | Type | Bounds | Declared on | Declared default |
|---|---|---|---|---|---|
| [aliasIds](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-aliasIds) | Alternative identifiers for this element, typically supplied by tools. | String | 0..* | Element | No declared default |
| [declaredName](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-declaredName) | The primary name explicitly supplied for this element. | String | 0..1 | Element | No declared default |
| [declaredShortName](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-declaredShortName) | An explicitly supplied compact alternative name whose contextual uniqueness is the modeler’s responsibility. | String | 0..1 | Element | No declared default |
| [differencingType](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-differencingType) | The ordered types defining this type as the first type’s interpretations minus those of subsequent types. | Type | 0..* | Type | No declared default |
| [directedFeature](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-directedFeature) | The features of this type with an explicit direction. | Feature | 0..* | Type | No declared default |
| [directedUsage](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Definition-directedUsage) | The usage features in this context that have an explicit direction. | Usage | 0..* | Definition | No declared default |
| [documentation](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-documentation) | The documentation elements owned by this element. | Documentation | 0..* | Element | No declared default |
| [elementId](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-elementId) | The tooling-assigned global identifier intended to remain stable for this element’s lifetime. | String | 1..1 | Element | No declared default |
| [endFeature](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-endFeature) | The features of this type marked as ends. | Feature | 0..* | Type | No declared default |
| [feature](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-feature) | The features available through this type’s feature memberships, including inherited features. | Feature | 0..* | Type | No declared default |
| [featureMembership](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-featureMembership) | The owned and inherited feature memberships of this type, excluding imported memberships. | FeatureMembership | 0..* | Type | No declared default |
| [importedMembership](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Namespaces-Namespace-importedMembership) | The memberships made available by imports owned by this namespace. | Membership | 0..* | Namespace | No declared default |
| [inheritedFeature](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-inheritedFeature) | The features obtained through inherited feature memberships. | Feature | 0..* | Type | No declared default |
| [inheritedMembership](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-inheritedMembership) | The memberships made available to this type by specialization or conjugation. | Membership | 0..* | Type | No declared default |
| [input](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-input) | The features of this type directed into the type, including bidirectional features. | Feature | 0..* | Type | No declared default |
| [intersectingType](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-intersectingType) | The types whose shared interpretations define this type. | Type | 0..* | Type | No declared default |
| [isAbstract](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-isAbstract) | Requires every instance of this type to also instantiate a more specialized type. | Boolean | 1..1 | Type | false (LiteralBoolean) |
| [isConjugated](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-isConjugated) | Records whether this type owns a conjugation as its conjugator. | Boolean | 1..1 | Type | No declared default |
| [isImpliedIncluded](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-isImpliedIncluded) | Records that all required implied owned relationships are included; false requires that none be included. | Boolean | 1..1 | Element | false (LiteralBoolean) |
| [isIndividual](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-Occurrences-OccurrenceDefinition-isIndividual) | Restricts this occurrence definition to classify at most one modeled thing. | Boolean | 1..1 | OccurrenceDefinition | false (LiteralBoolean) |
| [isLibraryElement](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-isLibraryElement) | Indicates that this element lies within the ownership tree of a library model. | Boolean | 1..1 | Element | No declared default |
| [isSufficient](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-isSufficient) | Makes satisfying this type’s classification conditions sufficient for classification by the type. | Boolean | 1..1 | Type | false (LiteralBoolean) |
| [isVariation](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Definition-isVariation) | Marks a variation point and requires its relevant memberships to be variant memberships. | Boolean | 1..1 | Definition | No declared default |
| [member](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Namespaces-Namespace-member) | The elements available as members through this namespace’s memberships. | Element | 0..* | Namespace | No declared default |
| [membership](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Namespaces-Namespace-membership) | The memberships available in this namespace, including owned and imported memberships. | Membership | 0..* | Namespace | No declared default |
| [multiplicity](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-multiplicity) | The owned multiplicity constraining this type’s modeled cardinality; without one, applicable supertype multiplicities still constrain it. | Multiplicity | 0..1 | Type | No declared default |
| [name](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-name) | The effective name used for namespace lookup, which some element kinds compute rather than declare. | String | 0..1 | Element | No declared default |
| [output](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-output) | The features of this type directed out of the type, including bidirectional features. | Feature | 0..* | Type | No declared default |
| [ownedAction](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Definition-ownedAction) | The action usages owned as features by this definition. | ActionUsage | 0..* | Definition | No declared default |
| [ownedAllocation](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Definition-ownedAllocation) | The allocation usages owned as features by this definition. | AllocationUsage | 0..* | Definition | No declared default |
| [ownedAnalysisCase](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Definition-ownedAnalysisCase) | The analysis case usages owned as features by this definition. | AnalysisCaseUsage | 0..* | Definition | No declared default |
| [ownedAnnotation](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-ownedAnnotation) | The annotation relationships owned here that annotate this element. | Annotation | 0..* | Element | No declared default |
| [ownedAttribute](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Definition-ownedAttribute) | The attribute usages owned as features by this definition. | AttributeUsage | 0..* | Definition | No declared default |
| [ownedCalculation](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Definition-ownedCalculation) | The calculation usages owned as features by this definition. | CalculationUsage | 0..* | Definition | No declared default |
| [ownedCase](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Definition-ownedCase) | The case usages owned as features by this definition. | CaseUsage | 0..* | Definition | No declared default |
| [ownedConcern](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Definition-ownedConcern) | The concern usages owned as features by this definition. | ConcernUsage | 0..* | Definition | No declared default |
| [ownedConjugator](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-ownedConjugator) | The optional conjugation owned here that treats this type as the original type. | Conjugation | 0..1 | Type | No declared default |
| [ownedConnection](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Definition-ownedConnection) | The connector-as-usages, including binding, succession and flow usages owned as features by this definition. | ConnectorAsUsage | 0..* | Definition | No declared default |
| [ownedConstraint](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Definition-ownedConstraint) | The constraint usages owned as features by this definition. | ConstraintUsage | 0..* | Definition | No declared default |
| [ownedDifferencing](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-ownedDifferencing) | The owned difference relationships defining this type as their difference result. | Differencing | 0..* | Type | No declared default |
| [ownedDisjoining](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-ownedDisjoining) | The owned disjointness relationships constraining this type against other types. | Disjoining | 0..* | Type | No declared default |
| [ownedElement](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-ownedElement) | The elements reached as owned related elements through this element’s owned relationships. | Element | 0..* | Element | No declared default |
| [ownedEndFeature](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-ownedEndFeature) | The end features introduced through memberships owned by this type. | Feature | 0..* | Type | No declared default |
| [ownedEnumeration](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Definition-ownedEnumeration) | The enumeration usages owned as features by this definition. | EnumerationUsage | 0..* | Definition | No declared default |
| [ownedFeature](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-ownedFeature) | The features introduced through feature memberships owned by this type. | Feature | 0..* | Type | No declared default |
| [ownedFeatureMembership](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-ownedFeatureMembership) | The memberships owned here that introduce owned features of this type. | FeatureMembership | 0..* | Type | No declared default |
| [ownedFlow](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Definition-ownedFlow) | The flow usages owned as features by this definition. | FlowUsage | 0..* | Definition | No declared default |
| [ownedImport](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Namespaces-Namespace-ownedImport) | The import relationships owned by this namespace. | Import | 0..* | Namespace | No declared default |
| [ownedInterface](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Definition-ownedInterface) | The interface usages owned as features by this definition. | InterfaceUsage | 0..* | Definition | No declared default |
| [ownedIntersecting](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-ownedIntersecting) | The owned intersection relationships defining this type as their intersection result. | Intersecting | 0..* | Type | No declared default |
| [ownedItem](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Definition-ownedItem) | The item usages owned as features by this definition. | ItemUsage | 0..* | Definition | No declared default |
| [ownedMember](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Namespaces-Namespace-ownedMember) | The member elements owned through this namespace’s owned memberships. | Element | 0..* | Namespace | No declared default |
| [ownedMembership](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Namespaces-Namespace-ownedMembership) | The memberships owned by this namespace. | Membership | 0..* | Namespace | No declared default |
| [ownedMetadata](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Definition-ownedMetadata) | The metadata usages owned as features by this definition. | MetadataUsage | 0..* | Definition | No declared default |
| [ownedOccurrence](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Definition-ownedOccurrence) | The occurrence usages owned as features by this definition. | OccurrenceUsage | 0..* | Definition | No declared default |
| [ownedPart](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Definition-ownedPart) | The part usages owned as features by this definition. | PartUsage | 0..* | Definition | No declared default |
| [ownedPort](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Definition-ownedPort) | The port usages owned as features by this definition. | PortUsage | 0..* | Definition | No declared default |
| [ownedReference](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Definition-ownedReference) | The reference usages owned as features by this definition. | ReferenceUsage | 0..* | Definition | No declared default |
| [ownedRelationship](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-ownedRelationship) | The relationships owned by this element as their owning related element. | Relationship | 0..* | Element | No declared default |
| [ownedRendering](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Definition-ownedRendering) | The rendering usages owned as features by this definition. | RenderingUsage | 0..* | Definition | No declared default |
| [ownedRequirement](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Definition-ownedRequirement) | The requirement usages owned as features by this definition. | RequirementUsage | 0..* | Definition | No declared default |
| [ownedSpecialization](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-ownedSpecialization) | The owned specialization relationships in which this type is the more specific type. | Specialization | 0..* | Type | No declared default |
| [ownedState](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Definition-ownedState) | The state usages owned as features by this definition. | StateUsage | 0..* | Definition | No declared default |
| [ownedSubclassification](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Classifiers-Classifier-ownedSubclassification) | The subclassification relationships owned here that identify this classifier as the more specific classifier. | Subclassification | 0..* | Classifier | No declared default |
| [ownedTransition](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Definition-ownedTransition) | The transition usages owned as features by this definition. | TransitionUsage | 0..* | Definition | No declared default |
| [ownedUnioning](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-ownedUnioning) | The owned union relationships defining this type as their union result. | Unioning | 0..* | Type | No declared default |
| [ownedUsage](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Definition-ownedUsage) | The usage features owned by this definition. | Usage | 0..* | Definition | No declared default |
| [ownedUseCase](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Definition-ownedUseCase) | The use case usages owned as features by this definition. | UseCaseUsage | 0..* | Definition | No declared default |
| [ownedVerificationCase](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Definition-ownedVerificationCase) | The verification case usages owned as features by this definition. | VerificationCaseUsage | 0..* | Definition | No declared default |
| [ownedView](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Definition-ownedView) | The view usages owned as features by this definition. | ViewUsage | 0..* | Definition | No declared default |
| [ownedViewpoint](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Definition-ownedViewpoint) | The viewpoint usages owned as features by this definition. | ViewpointUsage | 0..* | Definition | No declared default |
| [owner](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-owner) | The owning related element reached through this element’s owning relationship, which need not be a namespace. | Element | 0..1 | Element | No declared default |
| [owningMembership](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-owningMembership) | The relationship owning this element when that relationship is a membership. | OwningMembership | 0..1 | Element | No declared default |
| [owningNamespace](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-owningNamespace) | The namespace obtained through this element’s owning membership, when that ownership route exists. | Namespace | 0..1 | Element | No declared default |
| [owningRelationship](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-owningRelationship) | The relationship that directly owns this element as a related element, if one exists. | Relationship | 0..1 | Element | No declared default |
| [qualifiedName](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-qualifiedName) | The ownership-path name in KerML syntax, absent when the named ownership path or disambiguation conditions are not met. | String | 0..1 | Element | No declared default |
| [shortName](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-shortName) | The effective compact name used for namespace lookup, which some element kinds compute rather than declare. | String | 0..1 | Element | No declared default |
| [textualRepresentation](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Root-Elements-Element-textualRepresentation) | The textual-representation annotations attached to this element. | TextualRepresentation | 0..* | Element | No declared default |
| [unioningType](https://www.omg.org/spec/KerML/20250201/KerML.xmi#Core-Types-Type-unioningType) | The types whose combined interpretations equal this type’s interpretation. | Type | 0..* | Type | No declared default |
| [usage](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Definition-usage) | The usage features available in this context, including usages not owned here. | Usage | 0..* | Definition | No declared default |
| [variant](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Definition-variant) | The usages offered as alternatives at this variation point; absent when it is not a variation point. | Usage | 0..* | Definition | No declared default |
| [variantMembership](https://www.omg.org/spec/SysML/20250201/SysML.xmi#Systems-DefinitionAndUsage-Definition-variantMembership) | The owned memberships introducing variants, required to be empty outside a variation point. | VariantMembership | 0..* | Definition | No declared default |

## Reconciliation and limits

Seed reconciliation: **SelectedFieldsMatch** for direct bases, declared property names/types/bounds/derivation/ordering/subsets/redefinitions, constraint names. This checks selected structural fields only; it does not approve the entire seed or all semantics.

- Instance-level composition is governed by usages and their context, rather than by the outline of the definition box.
- Effective property resolution covers explicit inheritance and redefinition identities; it does not evaluate constraint consistency, OCL derivations or executable behavior.

[Browse interactive properties](../concept-browser.html#https://github.com/DynamicalSystemsGroup/sysml-concept-reference/id/SysML/20250201/Systems-Parts-PartDefinition) · [Concept-page contract](../concept-page-contract.md)
