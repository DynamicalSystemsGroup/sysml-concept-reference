"""Resolve declaration identities through UML-style explicit inheritance and redefinition.

This computes a metamodel declaration view, not execution of SysML derivations.
"""
from collections import defaultdict
import json
from rdflib import Namespace, RDFS

INV = Namespace("https://github.com/DynamicalSystemsGroup/sysml-concept-reference/vocab#")


def resolve_properties(graph, concept):
    memo, visiting = {}, set()

    def redefined_by(prop, seen=None):
        seen = set() if seen is None else seen
        if prop in seen:
            raise ValueError(f"Redefinition cycle at {prop}")
        result = set()
        for target in graph.objects(prop, INV.redefines):
            result.add(target)
            result.update(redefined_by(target, seen | {prop}))
        return result

    def resolve(node):
        if node in visiting:
            raise ValueError(f"Generalization cycle at {node}")
        if node in memo:
            return memo[node]
        if graph.value(node, INV.coverage) != INV.DeclaredPropertiesExtracted:
            raise ValueError(f"Cannot resolve an unextracted superclass: {node}")
        visiting.add(node)
        ancestors, inherited, history, excluded = {node}, set(), set(), set()
        for base in graph.objects(node, INV.specializes):
            parent = resolve(base)
            ancestors.update(parent["ancestors"])
            history.update(parent["all_declarations"])
            excluded.update(parent["excluded_private"])
            for prop in parent["active"]:
                attrs = json.loads(str(graph.value(prop, INV.xmiAttributes) or "{}"))
                if attrs.get("visibility") == "private":
                    excluded.add(prop)
                else:
                    inherited.add(prop)
        declared = set(graph.objects(node, INV.declaresProperty))
        candidates = inherited | declared
        all_declarations = history | declared
        suppressed = set().union(*(redefined_by(p) for p in candidates)) if candidates else set()
        active = candidates - suppressed
        replaced = {p: sorted((q for q in active if p in redefined_by(q)), key=str)
                    for p in all_declarations - active if p in suppressed}
        # Keep competing declarations visible; names do not establish redefinition.
        names = defaultdict(list)
        for prop in active:
            names[str(graph.value(prop, RDFS.label))].append(prop)
        conflicts = {name: sorted(props, key=str) for name, props in names.items() if len(props) > 1}
        result = {"active": sorted(active, key=str), "replaced": replaced,
                  "excluded_private": sorted(excluded, key=str), "conflicts": conflicts,
                  "ancestors": ancestors, "all_declarations": all_declarations}
        visiting.remove(node)
        memo[node] = result
        return result

    return resolve(concept)


def inheritance_paths(graph, concept, owner):
    """Retain alternative paths through diamonds without duplicating declarations."""
    def visit(node, path):
        if node in path:
            raise ValueError("Generalization cycle")
        if node == owner:
            return [path + [node]]
        paths = []
        for base in sorted(graph.objects(node, INV.specializes), key=str):
            paths.extend(visit(base, path + [node]))
        return paths
    return visit(concept, [])
