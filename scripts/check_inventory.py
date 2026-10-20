"""Validate the catalogue and run checked-in SPARQL queries, or execute one query."""
import argparse
import json
from pathlib import Path

from pyshacl import validate
from rdflib import Graph, Namespace, RDF
from rdflib.namespace import DCTERMS

from property_resolution import resolve_properties

ROOT = Path(__file__).resolve().parents[1]
INV = Namespace("https://github.com/DynamicalSystemsGroup/sysml-concept-reference/vocab#")


def load_graph(include_profiles=True):
    g = Graph()
    for name in ("vocabulary", "metamodel", "mechanisms"):
        g.parse(ROOT / f"data/rdf/{name}.ttl")
    if include_profiles and (ROOT / "data/rdf/profiles.ttl").exists():
        g.parse(ROOT / "data/rdf/profiles.ttl")
    return g


def check(g):
    conforms, _, report = validate(g, shacl_graph=str(ROOT / "data/rdf/shapes.ttl"), inference="none")
    if not conforms:
        raise ValueError(report)
    for node in g.subjects(RDF.type, INV.ExtractedPropertyRecord):
        for predicate in (INV.xmiAttributes, INV.lowerEncoding, INV.upperEncoding, INV.defaultEncoding):
            json.loads(str(g.value(node, predicate)))
        normal = json.loads(str(g.value(node, INV.normalizationDetail)))
        for field, predicate in (("lower", INV.lowerBound), ("upper", INV.upperBound)):
            term = g.value(node, predicate)
            expected = normal[field]["value"]
            actual = term.toPython() if term is not None else None
            if (str(actual) if field == "upper" and actual is not None else actual) != (str(expected) if field == "upper" and expected is not None else expected):
                raise ValueError("Normalized bounds disagree with provenance: " + str(node))
    for concept in g.subjects(INV.isFocus, None):
        resolution = resolve_properties(g, concept)
        if set(g.objects(concept, INV.effectiveProperty)) != set(resolution["active"]):
            raise ValueError("Materialized effective properties are stale")
    for profile in g.subjects(RDF.type, INV.ConceptProfile):
        concept = g.value(profile, INV.concept)
        for prop in g.objects(concept, INV.effectiveProperty):
            if not g.value(prop, DCTERMS.description):
                raise ValueError("Profile property lacks a reviewed explanation: " + str(prop))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", type=Path, help="Print a query's result rows as JSON")
    args = parser.parse_args()
    g = load_graph()
    if args.query:
        result = g.query(args.query.read_text())
        rows = [{str(k): str(v) for k, v in row.asdict().items()} for row in result]
        print(json.dumps(rows, indent=2))
        return
    print(check(g).strip())
    counts = {}
    for path in sorted((ROOT / "queries").glob("*.rq")):
        counts[path.name] = len(list(g.query(path.read_text())))
    if counts["concepts.rq"] != json.loads((ROOT / "data/rdf/extraction-report.json").read_text())["focus_metaclasses"] or counts["source-gaps.rq"] != 0:
        raise ValueError(f"Unexpected query results: {counts}")
    if not all(counts[name] > 0 for name in ("part-properties.rq", "mechanisms.rq", "reference-gaps.rq")):
        raise ValueError(f"Expected nonempty query results: {counts}")
    for name in ("effective-properties.rq", "replaced-properties.rq", "concept-relations.rq", "notation.rq", "examples.rq"):
        if counts.get(name, 0) == 0:
            raise ValueError("Expected nonempty profile query: " + name)
    print(json.dumps({"triples": len(g), "query_rows": counts}, indent=2))


if __name__ == "__main__":
    main()
