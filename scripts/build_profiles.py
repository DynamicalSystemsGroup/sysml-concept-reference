"""Generate source-backed concept profiles, original-example records and seed reconciliation."""
import json
import re
from pathlib import Path

from rdflib import Graph, Literal, RDF, RDFS, URIRef
from rdflib.namespace import DCTERMS

from build_inventory import ID, INV, ROOT, write_turtle
from check_inventory import load_graph
from property_resolution import resolve_properties


def by_source(graph, source):
    matches = [n for n in graph.subjects(DCTERMS.source, URIRef(source)) if (n, RDF.type, INV.MetaclassRecord) in graph]
    if len(matches) != 1:
        raise ValueError("Profile concept must resolve uniquely: " + source)
    return matches[0]


def add_evidence(graph, entries, source_artifact):
    result = []
    for entry in entries:
        url = URIRef(entry["url"])
        if str(url) != f"https://www.omg.org/spec/SysML/2.0/Language/PDF#page={entry['pdf_page']}":
            raise ValueError("Inconsistent PDF evidence location")
        graph.add((url, RDF.type, INV.EvidenceLocation))
        graph.add((url, INV.sourceArtifact, source_artifact))
        graph.add((url, INV.sourceLocator, Literal(entry["locator"])))
        graph.add((url, INV.pdfPage, Literal(entry["pdf_page"])))
        graph.add((url, INV.printedPage, Literal(entry["printed_page"])))
        result.append(url)
    return result


def reconcile(graph, profiles, seed):
    entries = {e["name"]: e for e in seed["entries"]}
    report = []
    for profile in profiles:
        concept = by_source(graph, profile["concept_source"])
        entry = entries[profile["name"]]
        bases = sorted(str(graph.value(b, RDFS.label)) for b in graph.objects(concept, INV.specializes))
        constraints = sorted(str(graph.value(r, RDFS.label)) for r in graph.objects(concept, INV.declaresConstraint))
        props = {str(graph.value(p, RDFS.label)): p for p in graph.objects(concept, INV.declaresProperty)}
        differences = []
        if bases != sorted(entry["general_classes"]):
            differences.append("Direct general classes differ")
        if constraints != sorted(entry["named_constraints"]):
            differences.append("Declared constraint names differ")
        if sorted(props) != sorted(a["name"] for a in entry["attributes"]):
            differences.append("Declared property names differ")
        for attr in entry["attributes"]:
            if attr["name"] not in props:
                continue
            prop = props[attr["name"]]
            normal = json.loads(str(graph.value(prop, INV.normalizationDetail)))
            declaration = attr["declaration"]
            match = re.search(r":\s*(\w+)\s*\[(\d+)\.\.(\d+|\*)\]", declaration)
            if not match:
                differences.append("Unparsed seed signature: " + attr["name"])
                continue
            type_name = str(graph.value(graph.value(prop, INV.valueType), RDFS.label))
            if (match[1], int(match[2]), match[3]) != (type_name, normal["lower"]["value"], str(normal["upper"]["value"])):
                differences.append("Type/bounds differ: " + attr["name"])
            if attr["derived"] != normal["qualifiers"]["isDerived"]["value"]:
                differences.append("Derived flag differs: " + attr["name"])
            if ("ordered" in declaration) != normal["qualifiers"]["isOrdered"]["value"]:
                differences.append("Ordering differs: " + attr["name"])
            for marker, pred in (("subsets", INV.subsets), ("redefines", INV.redefines)):
                names = sorted(str(graph.value(p, RDFS.label)) for p in graph.objects(prop, pred))
                # The selected seed signatures have at most one role after each marker.
                expected = re.findall(r"\b" + marker + r"\s+(\w+)", declaration)
                if names != sorted(expected):
                    differences.append(marker + " differs: " + attr["name"])
        report.append({"concept": profile["name"], "seed_section": entry["section"],
                       "status": "SelectedFieldsMatch" if not differences else "DifferencesFound",
                       "checked": ["direct bases", "declared property names/types/bounds/derivation/ordering/subsets/redefinitions", "constraint names"],
                       "differences": differences})
    return {"scope": "Four selected class declarations; not a complete PDF or seed reconciliation", "concepts": report}


def meaning_value(normal):
    default = normal["default"]
    if default["status"] == "NoDeclaredDefault":
        return "No declared default"
    if default["status"] != "DecodedLiteral":
        return default["status"]
    return json.dumps(default["value"], ensure_ascii=False) + " (" + default["type"].split(":")[-1] + ")"


def render_markdown(profile, graph, concept, reconciliation):
    def refs(entries):
        return "; ".join(f"[{e['locator']}, printed {e['printed_page']} / PDF {e['pdf_page']}]({e['url']})" for e in entries)
    code = (ROOT / profile["example_file"]).read_text()
    result = resolve_properties(graph, concept)
    lines = [f"# {profile['name']}", "", "Status: **draft, source-checked**. Editorial explanation with separately identified source declarations and original illustrative redraws.", "", profile["purpose"], "", f"[Original XMI declaration]({profile['concept_source']}). " + refs(profile["evidence"]), "", "## What to understand", ""]
    lines.extend("- " + p for p in profile["learning_points"])
    lines += ["", "## Connected example", "", profile["example_focus"], "", "```sysml", code.rstrip(), "```", "", "Verification: **source-reviewed, not parser-validated or executed**. " + refs(profile["example_evidence"]), "", "## Relationships and composition", ""]
    for r in profile["relationships"]:
        target = next(p for p in json.loads((ROOT / "data/concept-profiles.json").read_text())["profiles"] if p["concept_source"] == r["target_source"])
        lines += [f"### {r['kind'].capitalize()}: [{target['name']}]({target['slug']}.md)", "", r["description"], "", "Condition: " + r["condition"], "", refs(r["evidence"]), ""]
    lines += ["## Graphical notation", "", "These are representative, source-checked variants, not an exhaustive notation grammar. The illustrations are original redraws, not official figures.", ""]
    for n in profile["notations"]:
        lines += ["### " + n["title"], "", "Context: " + n["context"] + ".", "", n["description"], ""]
        if n.get("asset"):
            lines += [f"![{n['title']}](../assets/notation/{n['asset']})", ""]
        lines += [refs(n["evidence"]), ""]
    lines += ["## Properties", "", f"The explicit-redefinition view contains **{len(result['active'])} active declarations**, retaining declaration origins and excluding {len(result['replaced'])} replaced declarations. It deduplicates diamond paths by identity, excludes private inherited fields, and reports unresolved same-name collisions instead of choosing a winner.", "", "**These are metamodel property cardinalities and declared defaults.** They do not determine the multiplicity or runtime values of a part, port or connection in a user model. Derived values still require their derivation rules. See [property rules](../research/property-rules.md).", "", "| Property | Meaning | Type | Bounds | Declared on | Declared default |", "|---|---|---|---|---|---|"]
    def cell(value):
        return str(value).replace("|", "\\|").replace("\n", " ")
    for prop in sorted(result["active"], key=lambda p: (str(graph.value(p, RDFS.label)), str(p))):
        n = json.loads(str(graph.value(prop, INV.normalizationDetail)))
        owner = graph.value(prop, INV.declaredOn)
        values = [f"[{graph.value(prop, RDFS.label)}]({graph.value(prop, DCTERMS.source)})", graph.value(prop, DCTERMS.description) or "Explanation not yet reviewed", graph.value(graph.value(prop, INV.valueType), RDFS.label), f"{n['lower']['value']}..{n['upper']['value']}", graph.value(owner, RDFS.label), meaning_value(n)]
        lines.append("| " + " | ".join(cell(v) for v in values) + " |")
    if result["replaced"]:
        lines += ["", "### Replaced declarations", ""]
        for old, replacements in sorted(result["replaced"].items(), key=lambda p: str(p[0])):
            lines.append(f"- `{graph.value(old, INV.qualifiedName)}` → " + ", ".join(f"`{graph.value(p, INV.qualifiedName)}`" for p in replacements))
    if result["conflicts"]:
        lines += ["", "Unresolved same-name declarations: " + ", ".join(sorted(result["conflicts"]))]
    lines += ["", "## Reconciliation and limits", "", f"Seed reconciliation: **{reconciliation['status']}** for {', '.join(reconciliation['checked'])}. This checks selected structural fields only; it does not approve the entire seed or all semantics.", ""]
    lines.extend("- " + c for c in profile["caveats"])
    lines += ["- Effective property resolution covers explicit inheritance and redefinition identities; it does not evaluate constraint consistency, OCL derivations or executable behavior.", "", "[Browse interactive properties](../concept-browser.html#" + str(concept) + ") · [Concept-page contract](../concept-page-contract.md)", ""]
    return "\n".join(lines)


def main():
    source_graph = load_graph(include_profiles=False)
    config = json.loads((ROOT / "data/concept-profiles.json").read_text())
    profiles = config["profiles"]
    report = reconcile(source_graph, profiles, json.loads((ROOT / "data/language-inventory.json").read_text()))
    (ROOT / "data/profile-reconciliation.json").write_text(json.dumps(report, indent=2) + "\n")
    g = Graph()
    g.bind("inv", INV); g.bind("id", ID); g.bind("dct", DCTERMS)
    manifest = json.loads((ROOT / "data/source-manifest.json").read_text())
    pdf = next(a for a in manifest["supporting_artifacts"] if a["id"] == "SysMLLanguage")
    pdf_source = ID["source/sha256/" + pdf["sha256"]]
    for profile, reconciled in zip(profiles, report["concepts"]):
        concept = by_source(source_graph, profile["concept_source"])
        p = ID["profile/" + profile["slug"]]
        g.add((p, RDF.type, INV.ConceptProfile));g.add((p, INV.concept, concept))
        g.add((concept, INV.hasProfile, p));g.add((p, INV.profileStatus, INV.DraftSourceChecked))
        g.add((p, DCTERMS.description, Literal(profile["purpose"])));g.add((p, INV.evidenceStatus, INV.EditorialSummary))
        g.add((p, INV.profilePage, Literal("concepts/" + profile["slug"] + ".md")))
        for point in profile["learning_points"]:g.add((p, INV.learningPoint, Literal(point)))
        for caveat in profile["caveats"]:g.add((p, INV.caveat, Literal(caveat)))
        for evidence in add_evidence(g, profile["evidence"], pdf_source):g.add((p, INV.evidence, evidence))
        example = ID["example/" + profile["slug"]]
        g.add((example, RDF.type, INV.Example));g.add((p, INV.hasExample, example))
        g.add((example, INV.code, Literal((ROOT / profile["example_file"]).read_text())))
        g.add((example, DCTERMS.description, Literal(profile["example_focus"])))
        g.add((example, INV.verificationStatus, INV.SourceReviewedNotExecuted))
        for evidence in add_evidence(g, profile["example_evidence"], pdf_source):g.add((example, INV.evidence, evidence))
        for i, relationship in enumerate(profile["relationships"]):
            r = ID[f"profile/{profile['slug']}/relationship/{i+1}"]
            g.add((r, RDF.type, INV.ConceptRelationship));g.add((p, INV.hasRelationship, r))
            g.add((r, INV.fromConcept, concept));g.add((r, INV.toConcept, by_source(source_graph, relationship["target_source"])))
            g.add((r, INV.relationKind, Literal(relationship["kind"])));g.add((r, DCTERMS.description, Literal(relationship["description"])))
            g.add((r, INV.condition, Literal(relationship["condition"])));g.add((r, INV.evidenceStatus, INV.EditorialSummary))
            for evidence in add_evidence(g, relationship["evidence"], pdf_source):g.add((r, INV.evidence, evidence))
        for notation in profile["notations"]:
            n = ID["notation/" + notation["id"]]
            g.add((n, RDF.type, INV.Notation));g.add((p, INV.hasNotation, n));g.add((n, INV.concept, concept))
            g.add((n, RDFS.label, Literal(notation["title"])));g.add((n, INV.context, Literal(notation["context"])))
            g.add((n, DCTERMS.description, Literal(notation["description"])));g.add((n, INV.verificationStatus, INV.RepresentativeNotationVisuallyChecked))
            if notation.get("asset"):
                asset = ROOT / "docs/assets/notation" / notation["asset"]
                if not asset.is_file():raise ValueError("Missing notation illustration")
                g.add((n, INV.asset, Literal("assets/notation/" + notation["asset"])))
                g.add((n, INV.depictionStatus, INV.OriginalRedraw))
            else:g.add((n, INV.depictionStatus, INV.SourceDescriptionOnly))
            for evidence in add_evidence(g, notation["evidence"], pdf_source):g.add((n, INV.evidence, evidence))
        (ROOT / "docs/concepts" / (profile["slug"] + ".md")).write_text(render_markdown(profile, source_graph, concept, reconciled))
    write_turtle(g, ROOT / "data/rdf/profiles.ttl")
    print(f"Built {len(profiles)} concept profiles, notation/example records and selected seed reconciliation")


if __name__ == "__main__":
    main()
