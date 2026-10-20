"""Validate the catalogue and run checked-in SPARQL queries, or execute one query."""
import argparse
import json
from pathlib import Path

from pyshacl import validate
from rdflib import Graph, Namespace, RDF

ROOT = Path(__file__).resolve().parents[1]
INV = Namespace("https://github.com/rororowyourboat/sysmlv2_inventory/vocab#")


def load_graph():
    g = Graph()
    for name in ("vocabulary", "metamodel", "mechanisms"):
        g.parse(ROOT / f"data/rdf/{name}.ttl")
    return g


def check(g):
    conforms, _, report = validate(g, shacl_graph=str(ROOT / "data/rdf/shapes.ttl"), inference="none")
    if not conforms:
        raise ValueError(report)
    for node in g.subjects(RDF.type, INV.ExtractedPropertyRecord):
        for predicate in (INV.xmiAttributes, INV.lowerEncoding, INV.upperEncoding, INV.defaultEncoding):
            json.loads(str(g.value(node, predicate)))
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
    if counts["concepts.rq"] != 15 or counts["source-gaps.rq"] != 0:
        raise ValueError(f"Unexpected query results: {counts}")
    if not all(counts[name] > 0 for name in ("part-properties.rq", "mechanisms.rq", "reference-gaps.rq")):
        raise ValueError(f"Expected nonempty query results: {counts}")
    print(json.dumps({"triples": len(g), "query_rows": counts}, indent=2))


if __name__ == "__main__":
    main()
