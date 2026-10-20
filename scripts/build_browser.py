"""Generate a self-contained, offline concept browser from the RDF catalogue."""
import json
from html import escape
import shutil

from rdflib import RDF, RDFS
from rdflib.namespace import DCTERMS

from check_inventory import INV, ROOT, check, load_graph
from property_resolution import inheritance_paths, resolve_properties


def payload(g):
    def val(s, p):
        value = g.value(s, p)
        return str(value) if value is not None else None

    def linked(u):
        return {"id": str(u), "name": val(u, RDFS.label) or str(u),
                "qualifiedName": val(u, INV.qualifiedName), "source": val(u, DCTERMS.source) or str(u)}

    def evidence(node):
        result = []
        for e in sorted(g.objects(node, INV.evidence), key=str):
            locators = sorted(map(str, g.objects(e, INV.sourceLocator)))
            page = val(e, INV.pdfPage)
            result.append({"url": str(e), "label": "; ".join(locators) + (f" · PDF {page}" if page else "")})
        return result

    properties = {}
    for p in g.subjects(RDF.type, INV.ExtractedPropertyRecord):
        properties[str(p)] = {**linked(p), "meaning": val(p, DCTERMS.description),
                              "owner": str(g.value(p, INV.declaredOn)),
                              "normalization": json.loads(val(p, INV.normalizationDetail)),
                              "raw": {"attributes": json.loads(val(p, INV.xmiAttributes)),
                                      "lower": json.loads(val(p, INV.lowerEncoding)),
                                      "upper": json.loads(val(p, INV.upperEncoding)),
                                      "default": json.loads(val(p, INV.defaultEncoding))},
                              "type": linked(g.value(p, INV.valueType)),
                              "subsets": sorted((linked(x) for x in g.objects(p, INV.subsets)), key=lambda x: x["id"]),
                              "redefines": sorted((linked(x) for x in g.objects(p, INV.redefines)), key=lambda x: x["id"])}
    concepts = {}
    for c in g.subjects(INV.isFocus, None):
        resolution = resolve_properties(g, c)
        owners = {g.value(p, INV.declaredOn) for p in resolution["all_declarations"]}
        concepts[str(c)] = {**linked(c), "meaning": val(c, DCTERMS.description),
                            "language": val(c, INV.language), "focus": bool(g.value(c, INV.isFocus).toPython()),
                            "bases": sorted(map(str, g.objects(c, INV.specializes))),
                            "properties": sorted(map(str, g.objects(c, INV.declaresProperty))),
                            "effective": sorted(map(str, resolution["active"])),
                            "allDeclarations": sorted(map(str, resolution["all_declarations"])),
                            "replaced": {str(k): sorted(map(str, v)) for k, v in resolution["replaced"].items()},
                            "excludedPrivate": sorted(map(str, resolution["excluded_private"])),
                            "conflicts": {k: sorted(map(str, v)) for k, v in resolution["conflicts"].items()},
                            "paths": {str(owner): [[str(n) for n in path] for path in inheritance_paths(g, c, owner)] for owner in owners},
                            "rules": sorted((linked(r) for r in g.objects(c, INV.declaresConstraint)), key=lambda x: x["id"])}
    mechanisms = [{"id": str(m), "name": val(m, RDFS.label), "meaning": val(m, DCTERMS.description)}
                  for m in sorted(g.subjects(RDF.type, INV.Mechanism), key=str)]
    applications = [{"concept": val(a, INV.concept), "mechanism": val(a, INV.mechanism),
                     "explanation": val(a, DCTERMS.description), "status": val(g.value(a, INV.applicability), RDFS.label),
                     "sources": sorted(map(str, g.objects(a, INV.evidence)))}
                    for a in sorted(g.subjects(RDF.type, INV.MechanismApplication), key=str)]
    profiles = {}
    for p in g.subjects(RDF.type, INV.ConceptProfile):
        profiles[val(p, INV.concept)] = {
            "purpose": val(p, DCTERMS.description), "evidence": evidence(p),
            "profilePage": val(p, INV.profilePage),
            "learningPoints": sorted(map(str, g.objects(p, INV.learningPoint))),
            "caveats": sorted(map(str, g.objects(p, INV.caveat))),
            "examples": [{"code": val(e, INV.code), "explanation": val(e, DCTERMS.description), "evidence": evidence(e)}
                         for e in sorted(g.objects(p, INV.hasExample), key=str)],
            "relationships": [{"kind": val(r, INV.relationKind), "target": val(r, INV.toConcept),
                               "meaning": val(r, DCTERMS.description), "condition": val(r, INV.condition), "evidence": evidence(r)}
                              for r in sorted(g.objects(p, INV.hasRelationship), key=str)],
            "notations": [{"name": val(n, RDFS.label), "context": val(n, INV.context),
                           "meaning": val(n, DCTERMS.description), "asset": val(n, INV.asset), "evidence": evidence(n)}
                          for n in sorted(g.objects(p, INV.hasNotation), key=str)]}
    manifest = json.loads((ROOT / "data/source-manifest.json").read_text())
    return {"concepts": concepts, "properties": properties, "profiles": profiles,
            "mechanisms": mechanisms, "applications": applications,
            "sources": manifest["artifacts"] + manifest["supporting_artifacts"],
            "counts": json.loads((ROOT / "data/rdf/extraction-report.json").read_text())}


def main():
    g = load_graph()
    check(g)
    browser_data = payload(g)
    data = json.dumps(browser_data, sort_keys=True, ensure_ascii=True).replace("<", "\\u003c")
    template = (ROOT / "scripts/browser-template.html").read_text()
    brand = (ROOT / "site/brand.css").read_text().replace('url("fonts/', 'url("assets/brand/fonts/')
    template = template.replace("__BRAND_STYLES__", brand)
    destination = ROOT / "docs/assets/brand"
    destination.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT / "site/assets", destination, dirs_exist_ok=True)
    (ROOT / "docs/concept-browser.html").write_text(template.replace("__INVENTORY_DATA__", data).replace("__CONCEPT_ANCHORS__", "".join(f'<span id="{escape(uri, quote=True)}"></span>' for uri in sorted(browser_data["concepts"]))))
    print("Built docs/concept-browser.html")


if __name__ == "__main__":
    main()
