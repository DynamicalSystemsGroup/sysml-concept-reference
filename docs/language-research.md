# SysML v2 language inventory and research findings

## Purpose and evidence

Research date: 2026-10-20. This note inventories language entities, relationships, properties, constraints and behavior. It does not establish implementation support or conformance.

The user-provided [NotebookLM notebook](https://notebooklm.google.com/notebook/68f78add-cb6f-42cf-9e2e-cb1b1ce42511) is titled **SysML 2.0 Language Specification**. `nlm notebook get` reported one source, ID `c83ee3d3-22d7-4c7c-97f5-196a6fe0c27d`, titled with the [official OMG Language PDF URL](https://www.omg.org/spec/SysML/2.0/Language/PDF). The retrieved source identifies **SysML 2.0, Part 1, formal/2026-03-02, March 2026**.

Seven notebook queries covered scope, structure, behavior, requirements/cases/views, shared properties, coverage and disputed details. Answers were reviewed alongside the source text fetched through `nlm source content`. Generated answers are research leads; the specification clauses take precedence. Some answers contained incorrect section numbers, inheritance labels and ownership explanations. Those mistakes are not accepted as facts here.

The companion [language inventory JSON](../data/language-inventory.json) records:

- 98 named subsection entries in **§§8.3.6–8.3.27**: 93 metaclasses and 5 enumerations.
- 218 extracted declared property signatures, preserving types, multiplicities, slash notation and qualifiers as present on matching source lines.
- 365 named constraints, plus general classes and per-entry section references.
- Source metadata and content hash, notebook query topics, conversation IDs, question/answer hashes and coverage limitations.

These counts describe this extraction, not the entire SysML/KerML metamodel. It does not expand inherited properties, operation definitions, complete OCL bodies, every grammar rule or every library member. A missing extracted property does not establish that a metaclass lacks that property. Full implementation requires checking the official machine-readable metamodel and referenced KerML specification.

## Specification layers

| Specification layer | Evidence | Inventory scope |
|---|---|---|
| User-facing language concepts | Clause 7 | Useful discovery guide; not a complete data schema |
| Textual and graphical syntax | §8.2 | Textual grammar and graphical notation are separate coverage dimensions |
| Abstract syntax | §8.3 | Metaclasses, properties, inheritance and well-formedness rules inform the semantic model |
| Semantics | §8.4 | Resolve implied relationships and library specialization; labels alone are insufficient |
| Standard libraries | Clause 9 | Load compatible library models and resolve their members |
| Referenced specifications | Normative references and interchange clauses | KerML and Systems Modeling API/Services are separate sources; this notebook does not replace them |

The specification describes language meaning. It does not prescribe our palette, storage engine, undo stack or layout algorithm. Proposed engineering choices below must remain distinguishable from language requirements.

## Entity and relationship inventory

The following list is generated from dedicated subsection headings in the notebook source. Foundation concepts preceding §8.3.6 are recorded separately below. Each row links back to the [OMG source](https://www.omg.org/spec/SysML/2.0/Language/PDF); exact subsection IDs and declarations are in the JSON.

| Section | Family | Named entries |
|---|---|---|
| 8.3.6 | Definition and usage | `Definition`, `ReferenceUsage`, `Usage`, `VariantMembership` |
| 8.3.7 | Attributes | `AttributeDefinition`, `AttributeUsage` |
| 8.3.8 | Enumerations | `EnumerationDefinition`, `EnumerationUsage` |
| 8.3.9 | Occurrences | `EventOccurrenceUsage`, `OccurrenceDefinition`, `OccurrenceUsage`, `PortionKind` (enum) |
| 8.3.10 | Items | `ItemDefinition`, `ItemUsage` |
| 8.3.11 | Parts | `PartDefinition`, `PartUsage` |
| 8.3.12 | Ports | `ConjugatedPortDefinition`, `ConjugatedPortTyping`, `PortConjugation`, `PortDefinition`, `PortUsage` |
| 8.3.13 | Connections | `BindingConnectorAsUsage`, `ConnectionDefinition`, `ConnectionUsage`, `ConnectorAsUsage`, `SuccessionAsUsage` |
| 8.3.14 | Interfaces | `InterfaceDefinition`, `InterfaceUsage` |
| 8.3.15 | Allocations | `AllocationDefinition`, `AllocationUsage` |
| 8.3.16 | Flows | `FlowDefinition`, `FlowUsage`, `SuccessionFlowUsage` |
| 8.3.17 | Actions | `AcceptActionUsage`, `ActionDefinition`, `ActionUsage`, `AssignmentActionUsage`, `ControlNode`, `DecisionNode`, `ForkNode`, `ForLoopActionUsage`, `IfActionUsage`, `JoinNode`, `LoopActionUsage`, `MergeNode`, `PerformActionUsage`, `SendActionUsage`, `TerminateActionUsage`, `TriggerInvocationExpression`, `TriggerKind` (enum), `WhileLoopActionUsage` |
| 8.3.18 | States | `ExhibitStateUsage`, `StateSubactionKind` (enum), `StateSubactionMembership`, `StateDefinition`, `StateUsage`, `TransitionFeatureKind` (enum), `TransitionFeatureMembership`, `TransitionUsage` |
| 8.3.19 | Calculations | `CalculationDefinition`, `CalculationUsage` |
| 8.3.20 | Constraints | `AssertConstraintUsage`, `ConstraintDefinition`, `ConstraintUsage` |
| 8.3.21 | Requirements and concerns | `ActorMembership`, `ConcernDefinition`, `ConcernUsage`, `FramedConcernMembership`, `RequirementConstraintKind` (enum), `RequirementConstraintMembership`, `RequirementDefinition`, `RequirementUsage`, `SatisfyRequirementUsage`, `SubjectMembership`, `StakeholderMembership` |
| 8.3.22 | Cases | `CaseDefinition`, `CaseUsage`, `ObjectiveMembership` |
| 8.3.23 | Analysis cases | `AnalysisCaseDefinition`, `AnalysisCaseUsage` |
| 8.3.24 | Verification cases | `RequirementVerificationMembership`, `VerificationCaseDefinition`, `VerificationCaseUsage` |
| 8.3.25 | Use cases | `IncludeUseCaseUsage`, `UseCaseDefinition`, `UseCaseUsage` |
| 8.3.26 | Views and viewpoints | `Expose`, `MembershipExpose`, `NamespaceExpose`, `RenderingDefinition`, `RenderingUsage`, `ViewDefinition`, `ViewpointDefinition`, `ViewpointUsage`, `ViewRenderingMembership`, `ViewUsage` |
| 8.3.27 | Metadata | `MetadataDefinition`, `MetadataUsage` |

### Foundations inherited or referenced from KerML

These must be part of the implementation coverage checklist even though they do not have dedicated class-detail entries in the extracted §§8.3.6–8.3.27 index. The Language PDF discusses foundations in §§8.3.2–8.3.5 and uses additional KerML classes throughout its grammar, generalizations and constraints. Exact inherited declarations need verification against KerML.

| Foundation | Concepts to preserve | Evidence in the SysML source |
|---|---|---|
| Graph identity | `Element`, `Relationship`, declared/effective names, IDs, owned relationships and implied elements | §§7.2, 8.3.2 |
| Dependencies | `Dependency`, client/supplier references | §§7.3, 8.3.3 |
| Annotations | `AnnotatingElement`, `Annotation`, `Comment`, `Documentation`, `TextualRepresentation` | §§7.4, 8.3.4 |
| Namespaces | `Namespace`, `Package`, `LibraryPackage`, `Membership`, `OwningMembership`, visibility | §§7.5, 8.3.5 |
| Imports and aliases | `Import`, `MembershipImport`, `NamespaceImport`, filtering and alias memberships | §§7.5, 8.3.5 |
| Classification and featuring | `Type`, `Classifier`, `Feature`, `FeatureMembership`, `FeatureTyping` | §§7.6, 8.2.2.6, 8.3.6 |
| Specialization | `Subclassification`, `Subsetting`, `Redefinition`, reference/cross subsetting and feature chaining | §§7.6, 7.13, 8.2.2.6 |
| Expressions and execution foundations | Expressions, invocations, functions, predicates, behaviors, steps, connectors and successions | §§7.13, 7.17–7.20; imported KerML classes in §8.3 |

Distinguish grammar productions, library definitions and metaclasses. A relationship is itself a model element; its graphical representation does not replace its semantic structure.

## The most important semantic distinctions

### Ownership, featuring, composition and diagram nesting

These are four different mechanisms:

1. **Owning membership** owns a declaration in a namespace/model structure.
2. **Feature membership** establishes a feature of a type/context.
3. **Composite feature semantics** concerns dependence of modeled instances; `Usage::isReference` is derived from the complement of `isComposite`.
4. **Diagram nesting** is a presentation choice that can show ownership, features, imports or grouping according to the selected notation/view.

For example, a `ref part` declaration can be owned in the source model while its referenced instances are non-composite. A definition nested in another definition creates a scoped declaration; that does not itself create an owned part instance. See §§7.5–7.6, 8.3.6.2–8.3.6.4.


### Definitions, usages and occurrences

A definition is a classifier; a usage is a feature in context. Do not represent them as one node type with a decorative label. Keep explicit typing/specialization references and preserve multiple usages of the same definition. Do not equate a usage declaration with a single runtime instance. See §8.3.6 and the type-specific families.


### Ports, connections, interfaces, bindings and flows

These are separate semantic kinds. Record feature paths, end features, port typing and conjugation. A connection can require a presentation richer than one binary line. Bindings assert equality; successions express temporal ordering; flows model transfers. See §§8.3.12–8.3.16 and their corresponding semantics.

Port feature direction, flow direction, connection-end ordering and graphical arrow direction must remain separate fields/concepts.

### Requirements and verification

`SatisfyRequirementUsage` is a usage with requirement/constraint semantics, not simply a colored edge. `RequirementVerificationMembership` is a specialized membership associated with verified requirements. A link to evidence and an executed verification result are different concepts. See §§8.3.21, 8.3.24, 8.4.17 and 8.4.20.

### Metamodel properties, modeled attributes and notation

| Category | Example | Handling |
|---|---|---|
| Metamodel property | `Definition::isVariation` | Use the metamodel declaration and constraints |
| Derived metamodel property | `/ownedPart`, `/isReference` | Compute/obtain from the semantic engine; avoid independent writable copies |
| Model feature | A user-declared `AttributeUsage` such as mass | Resolve its type, value expression and units |
| Notation | A label or compartment in graphical syntax | Record its syntax-to-semantics mapping; it is not an extra metamodel attribute |

A leading slash in §8.3 declarations indicates derivation. This is distinct from a modeler's `derived` feature modifier. Stored, inherited, derived and implied information must be distinguishable in inventory records. See §8.3.1 and §8.3.6.

## Property and relationship coverage checklist

The JSON retains declaration signatures rather than inventing a flattened database schema. Examples directly extracted from the source:

| Metaclass | Declared properties to inspect | Section |
|---|---|---|
| `Definition` | `isVariation`; derived owned-usage collections and variant information | 8.3.6.2 |
| `Usage` | Derived `definition`, `isReference`, `mayTimeVary`, nested-usage collections; `isVariation` | 8.3.6.4 |
| `OccurrenceUsage` | `isIndividual`, `portionKind`, derived `individualDefinition` and `occurrenceDefinition` | 8.3.9.4 |
| `PortUsage` | Derived `portDefinition` with `[0..*]` multiplicity | 8.3.12.6 |
| `AssignmentActionUsage` | Derived `referent`, `targetArgument`, `valueExpression` | 8.3.17.5 |
| `IfActionUsage` | Derived `ifArgument`, `thenAction`, optional `elseAction` | 8.3.17.10 |
| `StateUsage` | `isParallel`; derived entry/do/exit actions and state definitions | 8.3.18.6 |
| `TransitionUsage` | Derived source, target, succession, trigger actions, guard expressions and effect actions | 8.3.18.9 |
| `SatisfyRequirementUsage` | Derived `satisfiedRequirement`, `satisfyingFeature` | 8.3.21.10 |
| `ViewUsage` | Derived exposed elements, satisfied viewpoints, conditions, view definition and rendering | 8.3.26.11 |

For every supported kind, inspect applicable inherited properties too: identity, names, visibility, owning relationships, typing, abstractness, direction, multiplicity bounds, ordering, uniqueness, composition/reference, specialization, value expressions, initial/default values, variation and temporal portions. Applicability and defaults depend on kind/context; do not expose every modifier on every element or assume a universal default multiplicity.

A relationship record needs more than source/target strings: preserve its own ID/kind, role-specific references, owning context, explicit/implied status and constraints. The renderer may choose a simpler edge representation without discarding the semantic record.

## Behavioral coverage and runtime boundary

All families below belong in the language inventory.

| Behavior family | Capture in the semantic model | Execution work beyond rendering | Source |
|---|---|---|---|
| Occurrences/events | Temporal portions, identity and event references | Lifetimes and temporal interpretation | §8.3.9 |
| Actions/performances | Definitions, usages, parameters, performed-action references | Invocation and parameter binding | §8.3.17 |
| Branching and concurrency | Decisions, merges, forks, joins and successions | Scheduling and synchronization | §8.3.17.6–8.3.17.13 |
| Structured control | If/for/while forms, test/sequence/body/variable references | Evaluate conditions and iterate | §8.3.17 |
| Communication/triggers | Send/accept payloads and endpoint/trigger expressions | Transfer handling, matching and time/change triggers | §8.3.17 |
| Assignment/termination | Target/referent/value and terminated-occurrence references | Mutate time-varying values and end lifetimes | §8.3.17.5, §8.3.17.16 |
| States | Parallel/exclusive structure, exhibited states, entry/do/exit memberships | Active-state and subaction lifecycle | §8.3.18 |
| Transitions | Source/target, trigger/guard/effect memberships | Trigger eligibility, guard evaluation and transition effects | §8.3.18.8–8.3.18.9 |
| Calculations/constraints | Parameters, expressions, assertions and dependencies | Expression evaluation and constraint checking | §§8.3.19–8.3.20 |
| Analysis/verification cases | Objectives, subjects, results and verified requirements | Execute analysis or verification with a declared evaluator | §§8.3.22–8.3.24 |

Behavioral declarations, semantic validity, expression evaluation and execution semantics are separate inventory dimensions. Detailed behavior comes from §8.4 and model libraries, including referenced KerML foundations; this inventory records their scope without implementing an execution engine.

## Views, variability, metadata and libraries

Views/viewpoints/renderings/exposure/filtering are model concepts (§8.3.26), distinct from arbitrary diagram presentation. Metadata definitions/usages (§8.3.27) and semantic extensions differ from untyped custom properties. Variation points and `VariantMembership` (§8.3.6) must not be treated as simultaneous owned features.

Library coverage must remain a separate workstream from metaclass enumeration:

| Library group | Reference | Required investigation |
|---|---|---|
| Systems Model Library | §9.2 | Base definitions/usages and implicit specialization targets |
| Standard views and reflection | §§9.2.20, 9.2.22 | Standard view definitions and the reflective SysML model |
| Metadata | §9.3 | Structured annotations and domain metadata |
| Analysis | §9.4 | Tool execution and analysis/trade-study models |
| Cause and effect | §9.5 | Causation-related modeling |
| Requirement derivation | §9.6 | Derivation models and metadata |
| Geometry | §9.7 | Spatial/shape types and operations |
| Quantities and units | §9.8 | Quantity values, measurement references, units and conversions |

These are coverage pointers, not an enumeration of every library element. Library symbols such as a verdict enumeration must not be mistaken for new §8.3 metaclasses. A library-aware parser/resolver is required before accurate inherited-feature and typing displays can be promised.

## Source discrepancies and generated-answer corrections

| Finding | Evidence/check | Treatment |
|---|---|---|
| Port referentiality is overgeneralized in prose | §8.3.12.6 description versus `validatePortUsageIsReference`, `validatePortUsageNestedUsagesNotComposite` and `checkPortUsageSubportSpecialization` | Preserve the discrepancy. Constraints distinguish nested port contexts; do not implement an unconditional ban on composite ports from the overview alone |
| Transition fields are collections in abstract syntax | §8.3.18.9 declares trigger, guard and effect collections with `[0..*]` | Keep the declared shape; investigate constraints/library restrictions before interpreting them as singular properties |
| A notebook answer conflated ownership and composition | Its structural summary treated `OwningMembership` and `isComposite` together; the source separates membership and usage semantics | Use the four-way distinction above |
| Several SysML classes were mislabeled as KerML classes | Requirement/case answer labeled `ConstraintDefinition`, `CalculationDefinition` and others as KerML classes | Verify against each class's General Classes declaration; do not copy generated inheritance tables |
| Some class section numbers were wrong | Behavior answer assigned wrong subsection IDs to `StateDefinition`, `TransitionUsage` and `SuccessionAsUsage` | Use extracted index: 8.3.18.5, 8.3.18.9 and 8.3.13.6 respectively |
| Generated cardinalities were polluted by citation markers | Structural answer included declarations such as `[5]` alongside citations | Use source declaration strings, not the generated table |
| API protocol lists varied between answers | Generated scope answers listed unsupported mixes of protocols | Do not repeat them; the separate API specification was not researched here |

These findings demonstrate why notebook answers cannot substitute for an official metamodel and clause-by-clause validation. No erratum was filed and no standard interpretation is claimed as approved.

## Acceptance cases and open coverage

Use these examples to audit inventory coverage:

1. Inherited and redefined features remain distinguishable from directly declared ones.
2. Multiplicity, units, expressions and default/initial values survive inspection without flattening their meaning.
3. A conjugated port retains its typing and direction semantics.
4. A branching/concurrent action model displays control kinds without claiming simulation.
5. A guarded state transition retains triggers/effects and its exact memberships.
6. Satisfaction and verification retain their distinct semantic structures.
7. Metadata application and a filtered view reference existing elements without duplicating ownership.
8. Unsupported library features and unresolved references are retained and diagnosed rather than dropped.

Still open: complete inherited KerML schema, official metamodel validation, all library declarations, grammar/graphical-notation coverage, full OCL and derivation evaluation, source-preserving parser behavior, API/interchange scope and execution conformance. These acceptance cases are proposed, not run.

## Reproduction and verification

The installed `nlm` CLI was used directly. The normal authenticated profile worked; no credentials were read or printed, and no notebook sources, notes, sharing settings or artifacts were changed. Queries may remain in notebook chat history.

```bash
nlm notebook get 68f78add-cb6f-42cf-9e2e-cb1b1ce42511
nlm source content c83ee3d3-22d7-4c7c-97f5-196a6fe0c27d \
  --output sandbox/sysml-notebook/source.txt
nlm notebook query 68f78add-cb6f-42cf-9e2e-cb1b1ce42511 \
  '<targeted language-inventory question>' \
  --json --new-conversation
```

The catalogue was extracted by reading unique named subsection headings in §§8.3.6–8.3.27, selecting their body occurrences, and collecting General Classes, one-line property declarations between Attributes and Operations, and constraint identifiers. It is sensitive to source-text layout; its raw declaration strings intentionally remain visible for review.

Raw retrieved text and generated answers are not included in this public repository. The catalogue retains query topics, conversation IDs and question/answer hashes. Original question wording included project-specific context and is omitted rather than rewritten as if different questions had been asked. Seven queries returned successfully, with the expected source ID. Verification checked JSON parsing, unique entry names/sections, counts, representative source declarations and local documentation links. The catalogue and documentation checks do not establish language conformance.

## Research repository scope

This repository owns the ongoing SysML v2 inventory. Its records describe language constructs, source evidence and unresolved coverage. Notebook access may require authorization; no public sharing was enabled. Query topic summaries are descriptive labels, not verbatim historical prompts.
