"""Generate a self-contained, offline concept browser from the RDF catalogue."""
import json

from rdflib import RDF, RDFS
from rdflib.namespace import DCTERMS

from check_inventory import INV, ROOT, check, load_graph


def payload(g):
    def val(s, p):
        v = g.value(s, p)
        return str(v) if v is not None else None

    def linked(u):
        return {"id": str(u), "name": val(u, INV.qualifiedName) or val(u, RDFS.label) or str(u),
                "source": val(u, DCTERMS.source) or str(u)}

    concepts = {}
    for c in g.subjects(INV.isFocus, None):
        props = []
        for p in g.objects(c, INV.declaresProperty):
            attrs = json.loads(val(p, INV.xmiAttributes))
            props.append({"name": val(p, RDFS.label), "id": str(p), "source": val(p, DCTERMS.source),
                          "type": linked(g.value(p, INV.valueType)), "attributes": attrs,
                          "lower": json.loads(val(p, INV.lowerEncoding)),
                          "upper": json.loads(val(p, INV.upperEncoding)),
                          "default": json.loads(val(p, INV.defaultEncoding)),
                          "subsets": sorted((linked(x) for x in g.objects(p, INV.subsets)), key=lambda x: x["id"]),
                          "redefines": sorted((linked(x) for x in g.objects(p, INV.redefines)), key=lambda x: x["id"])})
        rules = sorted((linked(r) for r in g.objects(c, INV.declaresConstraint)), key=lambda x: x["id"])
        concepts[str(c)] = {"name": val(c, RDFS.label), "qualifiedName": val(c, INV.qualifiedName),
                            "meaning": val(c, DCTERMS.description), "source": val(c, DCTERMS.source),
                            "language": val(c, INV.language), "focus": bool(g.value(c, INV.isFocus).toPython()),
                            "bases": sorted(map(str, g.objects(c, INV.specializes))),
                            "properties": sorted(props, key=lambda x: x["name"]), "rules": rules}
    mechanisms = []
    for m in sorted(g.subjects(RDF.type, INV.Mechanism), key=str):
        mechanisms.append({"id": str(m), "name": val(m, RDFS.label), "meaning": val(m, DCTERMS.description)})
    applications = []
    for a in sorted(g.subjects(RDF.type, INV.MechanismApplication), key=str):
        applications.append({"concept": val(a, INV.concept), "mechanism": val(a, INV.mechanism),
                             "explanation": val(a, DCTERMS.description),
                             "status": val(g.value(a, INV.applicability), RDFS.label),
                             "sources": sorted(map(str, g.objects(a, INV.evidence)))})
    return {"concepts": concepts, "mechanisms": mechanisms, "applications": applications,
            "sources": json.loads((ROOT / "data/source-manifest.json").read_text())["artifacts"],
            "counts": json.loads((ROOT / "data/rdf/extraction-report.json").read_text())}


def main():
    g = load_graph()
    check(g)
    data = json.dumps(payload(g), sort_keys=True, ensure_ascii=True).replace("<", "\\u003c")
    template = (ROOT / "scripts/browser-template.html").read_text()
    (ROOT / "docs/concept-browser.html").write_text(template.replace("__INVENTORY_DATA__", data))
    print("Built docs/concept-browser.html")


if __name__ == "__main__":
    main()
