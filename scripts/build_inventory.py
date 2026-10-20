"""Build the focused RDF slice from hash-pinned official XMI; no network by default."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen
import xml.etree.ElementTree as ET

from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef
from itertools import groupby
from rdflib.namespace import DCTERMS, XSD

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://github.com/rororowyourboat/sysmlv2_inventory/"
INV = Namespace(BASE + "vocab#")
ID = Namespace(BASE + "id/")
XMI = "{http://www.omg.org/spec/XMI/20161101}"
FOCUS = {
    "KerML": {"Element", "Relationship", "Namespace", "Membership", "OwningMembership",
              "Type", "Classifier", "FeatureMembership", "Feature", "TypeFeaturing"},
    "SysML": {"Definition", "Usage", "ReferenceUsage", "PartDefinition", "PartUsage"},
}
# Editorial summaries, kept separate from extracted declarations and source text.
SUMMARIES = {
    "Element": "The common foundation for things recorded in a KerML model, including relationships.",
    "Relationship": "A model element that relates other model elements and can participate in ownership.",
    "Namespace": "A context in which model elements are made available as named members.",
    "Membership": "Relates a namespace to a member without necessarily transferring ownership.",
    "OwningMembership": "A membership through which a namespace owns its member element.",
    "Type": "Describes a set of modeled things and can specify features and specialization relationships.",
    "Class": "A classifier for individually distinguishable things, even when their relationships are otherwise identical.",
    "Structure": "A KerML class for structurally described objects, underlying SysML item definitions.",
    "Classifier": "A type used to classify things in the modeled system.",
    "Feature": "A type that describes a relation from a featuring context to its values.",
    "FeatureMembership": "An owning membership connecting a type to an owned feature; featuring semantics also depend on whether the feature varies with time.",
    "TypeFeaturing": "Relates a feature to a type providing its featuring context; this is distinct from owning the feature declaration.",
    "Definition": "A SysML classifier that defines a reusable kind of modeled entity.",
    "Usage": "A SysML feature describing use of a kind of entity in a modeling context.",
    "ReferenceUsage": "A usage constrained to be referential rather than composite.",
    "PartDefinition": "Defines a kind of system or system part.",
    "PartUsage": "Describes a system or system part in context, with part-definition typing requirements.",
    "ItemDefinition": "Defines a kind of item, forming a foundation for part definitions.",
    "ItemUsage": "Describes an item in context, forming a foundation for part usages.",
    "OccurrenceDefinition": "Defines a kind of occurrence, including entities with temporal extent.",
    "OccurrenceUsage": "Describes occurrences in context, including temporal portions and individual occurrences.",
}


def fetch(manifest: dict, directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    for source in manifest["artifacts"]:
        path = directory / (source["language"] + ".xmi")
        data = path.read_bytes() if path.exists() else urlopen(source["url"], timeout=60).read()
        if hashlib.sha256(data).hexdigest() != source["sha256"] or len(data) != source["bytes"]:
            raise ValueError(f"Pinned content mismatch for {source['language']}; do not update the manifest silently")
        if not path.exists():
            path.write_bytes(data)


class Extractor:
    def __init__(self, manifest: dict, directory: Path):
        self.manifest = manifest
        self.sources = {s["url"]: s for s in manifest["artifacts"]}
        self.nodes = {}
        self.parents = {}
        self.g = Graph()
        for prefix, ns in (("inv", INV), ("id", ID), ("dct", DCTERMS)):
            self.g.bind(prefix, ns)
        self.created = set()
        self.external = set()
        for url, source in self.sources.items():
            data = (directory / (source["language"] + ".xmi")).read_bytes()
            if len(data) != source["bytes"] or hashlib.sha256(data).hexdigest() != source["sha256"]:
                raise ValueError(f"Pinned content mismatch: {source['language']}")
            root = ET.fromstring(data)
            package = next(n for n in root if n.get("name") == source["language"])
            if package.get("URI") != source["embedded_package_uri"]:
                raise ValueError("Unexpected package namespace")
            for parent in root.iter():
                for child in parent:
                    if child.get(XMI + "id"):
                        self.parents[(url, child.get(XMI + "id"))] = parent
                node_id = parent.get(XMI + "id")
                if node_id:
                    key = (url, node_id)
                    if key in self.nodes:
                        raise ValueError(f"Duplicate XMI ID: {key}")
                    self.nodes[key] = parent
            artifact = self.artifact(url)
            self.g.add((artifact, RDF.type, INV.SourceArtifact))
            for pred, value in ((DCTERMS.source, URIRef(url)), (INV.sha256, Literal(source["sha256"])),
                                (INV.language, Literal(source["language"])), (INV.version, Literal(source["version"])),
                                (INV.omgFileId, Literal(source["omg_file_id"])),
                                (INV.embeddedPackageURI, Literal(source["embedded_package_uri"])),
                                (INV.retrievedOn, Literal(manifest["retrieved_on"], datatype=XSD.date))):
                self.g.add((artifact, pred, value))

    def artifact(self, url):
        return ID["source/sha256/" + self.sources[url]["sha256"]]

    def refkey(self, url, node):
        if node is None:
            raise ValueError("Missing required XMI reference")
        if node.get(XMI + "idref"):
            return url, node.get(XMI + "idref")
        if node.get("href") and "#" in node.get("href"):
            return tuple(node.get("href").split("#", 1))
        raise ValueError(f"Unsupported reference: {node.attrib}")

    def qualified(self, key):
        names = []
        node = self.nodes[key]
        while node is not None:
            if node.get("name"):
                names.append(node.get("name"))
            node = self.parents.get((key[0], node.get(XMI + "id")))
        return "::".join(reversed(names))

    def uri(self, key):
        url, node_id = key
        if url not in self.sources:
            if url != "https://www.omg.org/spec/UML/20161101/PrimitiveTypes.xmi":
                raise ValueError(f"Unpinned external reference: {key}")
            self.external.add(url + "#" + node_id)
            u = URIRef(url + "#" + node_id)
            self.g.add((u, RDF.type, INV.ExternalTypeReference))
            self.g.add((u, RDFS.label, Literal(node_id)))
            self.g.add((u, INV.coverage, INV.ExternalUnverified))
            return u
        if key not in self.nodes:
            raise ValueError(f"Unresolved reference: {key}")
        return ID[self.sources[url]["language"] + "/20250201/" + quote(node_id, safe="-._~")]

    def record(self, key):
        u = self.uri(key)
        if key[0] not in self.sources or key in self.created:
            return u
        self.created.add(key)
        node = self.nodes[key]
        kind = node.get(XMI + "type", "")
        cls = {"uml:Class": INV.MetaclassRecord, "uml:Enumeration": INV.EnumerationRecord,
               "uml:Property": INV.PropertyRecord, "uml:Constraint": INV.ConstraintRecord,
               "uml:Association": INV.AssociationRecord}.get(kind, INV.SourceElementRecord)
        g = self.g
        for pred, value in ((RDF.type, INV.Record), (RDF.type, cls),
                            (RDFS.label, Literal(node.get("name", key[1]))),
                            (INV.qualifiedName, Literal(self.qualified(key))),
                            (INV.language, Literal(self.sources[key[0]]["language"])),
                            (INV.sourceArtifact, self.artifact(key[0])),
                            (DCTERMS.source, URIRef(key[0] + "#" + key[1])),
                            (INV.sourceLocator, Literal("xmi:id=" + key[1])),
                            (INV.coverage, INV.ReferenceOnly),
                            (INV.evidenceStatus, INV.Extracted)):
            g.add((u, pred, value))
        return u

    def bases(self, key):
        return [self.refkey(key[0], n.find("general")) for n in self.nodes[key].findall("generalization")]

    def details(self, key, focus):
        g = self.g
        n = self.nodes[key]
        u = self.record(key)
        g.set((u, INV.coverage, INV.DeclaredPropertiesExtracted))
        g.add((u, INV.isFocus, Literal(focus)))
        g.add((u, INV.notationStatus, INV.NotYetVerified))
        g.add((u, INV.xmiAttributes, Literal(json.dumps({k: v for k, v in n.attrib.items() if not k.startswith(XMI)}, sort_keys=True))))
        summary = SUMMARIES.get(n.get("name"))
        if summary:
            g.add((u, DCTERMS.description, Literal(summary)))
            g.add((u, INV.descriptionStatus, INV.EditorialSummary))
        for base in self.bases(key):
            g.add((u, INV.specializes, self.record(base)))
        for prop in n.findall("ownedAttribute"):
            pk = (key[0], prop.get(XMI + "id"))
            p = self.record(pk)
            g.set((p, INV.coverage, INV.ExtractedDeclaration))
            g.add((p, RDF.type, INV.ExtractedPropertyRecord))
            g.add((p, INV.declaredOn, u))
            g.add((u, INV.declaresProperty, p))
            g.add((p, INV.xmiAttributes, Literal(json.dumps({k: v for k, v in prop.attrib.items() if not k.startswith(XMI)}, sort_keys=True))))
            for attr in ("isDerived", "isReadOnly", "isOrdered", "isUnique", "isDerivedUnion"):
                if attr in prop.attrib:
                    if prop.get(attr) not in ("true", "false"):
                        raise ValueError(f"Invalid Boolean {attr}")
                    g.add((p, INV[attr], Literal(prop.get(attr) == "true")))
            if prop.get("aggregation"):
                g.add((p, INV.aggregation, Literal(prop.get("aggregation"))))
            for tag, predicate in (("type", INV.valueType), ("association", INV.association),
                                   ("subsettedProperty", INV.subsets), ("redefinedProperty", INV.redefines)):
                for ref in prop.findall(tag):
                    g.add((p, predicate, self.record(self.refkey(key[0], ref))))
            # Preserve lexical XMI encodings. UML defaults are deliberately not expanded.
            for tag, predicate in (("lowerValue", INV.lowerEncoding), ("upperValue", INV.upperEncoding),
                                   ("defaultValue", INV.defaultEncoding)):
                val = prop.find(tag)
                encoding = {"present": val is not None}
                if val is not None:
                    encoding.update({"type": val.get(XMI + "type"), "value": val.get("value")})
                g.add((p, predicate, Literal(json.dumps(encoding, sort_keys=True))))
        for rule in n.findall("ownedRule"):
            r = self.record((key[0], rule.get(XMI + "id")))
            g.set((r, INV.coverage, INV.NameOnly))
            g.add((r, INV.declaredOn, u))
            g.add((u, INV.declaresConstraint, r))
            g.add((r, INV.executionStatus, INV.NotImplemented))

    def build(self):
        selected = {k for k, n in self.nodes.items() if n.get(XMI + "type") == "uml:Class"
                    and n.get("name") in FOCUS[self.sources[k[0]]["language"]]}
        if len(selected) != sum(map(len, FOCUS.values())):
            raise ValueError("Focus selection did not uniquely match")
        detailed = set(selected)
        pending = list(selected)
        while pending:
            for base in self.bases(pending.pop()):
                if base not in detailed:
                    detailed.add(base)
                    pending.append(base)
        for key in sorted(detailed):
            self.details(key, key in selected)
        return {"focus_metaclasses": len(selected), "detailed_metaclasses": len(detailed),
                "declared_properties": len(set(self.g.subjects(RDF.type, INV.ExtractedPropertyRecord))),
                "constraint_names": len(set(self.g.subjects(RDF.type, INV.ConstraintRecord))),
                "source_reference_records": len(self.created),
                "external_type_references": sorted(self.external),
                "scope": "Focus metaclasses plus all ancestors; declared properties, not a computed effective schema",
                "limitations": ["UML defaults not expanded", "Reference-only records not fully inventoried",
                                "Constraint bodies and operations not extracted", "Notation not yet verified",
                                "No library, full metamodel, or SysML conformance claim"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch", action="store_true", help="Download missing sources and enforce manifest hashes")
    parser.add_argument("--source-dir", type=Path, default=ROOT / "sandbox/official-sources")
    args = parser.parse_args()
    manifest = json.loads((ROOT / "data/source-manifest.json").read_text())
    if args.fetch:
        fetch(manifest, args.source_dir)
    extractor = Extractor(manifest, args.source_dir)
    report = extractor.build()
    # Stable, readable Turtle; no blank nodes or serializer-generated identifiers.
    g = extractor.g
    for prefix, ns in (("rdf", RDF), ("rdfs", RDFS), ("xsd", XSD)):
        g.bind(prefix, ns)
    term = lambda value: value.n3(namespace_manager=g.namespace_manager)
    blocks = []
    for subject in sorted(set(g.subjects()), key=str):
        pairs = sorted(g.predicate_objects(subject), key=lambda pair: (str(pair[0]), pair[1].n3()))
        fields = [f"    {term(predicate)} " + ", ".join(term(obj) for _, obj in values)
                  for predicate, values in groupby(pairs, key=lambda pair: pair[0])]
        blocks.append(term(subject) + "\n" + " ;\n".join(fields) + " .\n")
    prefixes = "".join(f"@prefix {prefix}: <{ns}> .\n" for prefix, ns in sorted(g.namespaces()))
    (ROOT / "data/rdf/metamodel.ttl").write_text("# Generated by scripts/build_inventory.py; do not edit.\n" + prefixes + "\n" + "\n".join(blocks))
    (ROOT / "data/rdf/extraction-report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
