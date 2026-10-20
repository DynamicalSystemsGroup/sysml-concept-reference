"""Decode explicit XMI values and documented UML omissions without inventing defaults."""
import hashlib
import json
import xml.etree.ElementTree as ET

from rdflib import Literal, Namespace, RDF, URIRef
from rdflib.namespace import DCTERMS

BASE = "https://github.com/DynamicalSystemsGroup/sysml-concept-reference/"
INV = Namespace(BASE + "vocab#")
ID = Namespace(BASE + "id/")
UML = "https://www.omg.org/spec/UML/20161101/UML.xmi#"
QUALIFIERS = {
    "isDerived": (False, "Property-isDerived"),
    "isDerivedUnion": (False, "Property-isDerivedUnion"),
    "isReadOnly": (False, "StructuralFeature-isReadOnly"),
    "isOrdered": (False, "MultiplicityElement-isOrdered"),
    "isUnique": (True, "MultiplicityElement-isUnique"),
    "aggregation": ("none", "Property-aggregation"),
}


def decode_literal(encoding):
    """No default specification is different from a literal with omitted value."""
    if not encoding["present"]:
        return {"status": "NoDeclaredDefault", "value": None, "evidence": UML + "Property-defaultValue"}
    kind, raw = encoding.get("type"), encoding.get("value")
    if kind in ("uml:LiteralInteger", "uml:LiteralUnlimitedNatural"):
        value = int(raw) if raw is not None else 0
    elif kind == "uml:LiteralBoolean":
        if raw not in (None, "true", "false"):
            raise ValueError(f"Invalid Boolean literal: {raw}")
        value = raw == "true"
    elif kind == "uml:LiteralString":
        if raw is None:
            return {"status": "UnspecifiedLiteralValue", "value": None, "type": kind}
        value = raw
    else:
        return {"status": "UnsupportedExpression", "value": None, "type": kind}
    return {"status": "DecodedLiteral", "value": value, "type": kind,
            "basis": "ExplicitValue" if raw is not None else "UMLLiteralDefault",
            "evidence": UML + kind.split(":")[1] + "-value"}


def decode_bound(encoding, lower):
    field = "lower" if lower else "upper"
    if not encoding["present"]:
        return {"value": 1, "basis": "AbsentBoundSpecification", "evidence": UML + f"MultiplicityElement-{field}Bound"}
    decoded = decode_literal(encoding)
    if decoded["status"] != "DecodedLiteral" or type(decoded["value"]) is not int:
        return {"value": None, "basis": "UnsupportedBoundExpression", "evidence": UML + f"MultiplicityElement-{field}Bound"}
    value = decoded["value"]
    if value == -1 and not lower and encoding.get("type") == "uml:LiteralUnlimitedNatural":
        value = "*"
    elif value < 0:
        raise ValueError("Negative finite multiplicity bound")
    return {"value": value, "basis": decoded["basis"], "evidence": decoded["evidence"]}


def normalize_declaration(attributes, lower, upper, default):
    flags = {}
    for name, (fallback, source) in QUALIFIERS.items():
        value = attributes.get(name, fallback)
        if isinstance(fallback, bool) and name in attributes:
            if value not in ("true", "false"):
                raise ValueError(f"Invalid qualifier {name}")
            value = value == "true"
        flags[name] = {"value": value, "basis": "ExplicitXMI" if name in attributes else "UMLPropertyDefault", "evidence": UML + source}
    return {"lower": decode_bound(lower, True), "upper": decode_bound(upper, False),
            "default": decode_literal(default), "qualifiers": flags}


def add_normalization(graph, manifest, directory):
    supporting = {a["id"]: a for a in manifest["supporting_artifacts"]}
    for artifact in supporting.values():
        path = directory / artifact["file"]
        data = path.read_bytes()
        if len(data) != artifact["bytes"] or hashlib.sha256(data).hexdigest() != artifact["sha256"]:
            raise ValueError("Pinned supporting artifact mismatch: " + artifact["id"])
        node = ID["source/sha256/" + artifact["sha256"]]
        graph.add((node, RDF.type, INV.SourceArtifact))
        graph.add((node, DCTERMS.source, URIRef(artifact["url"])))
        graph.add((node, INV.sha256, Literal(artifact["sha256"])))
        graph.add((node, INV.language, Literal(artifact["language"])))
        graph.add((node, INV.version, Literal(artifact["version"])))
        graph.add((node, INV.retrievedOn, Literal(artifact["retrieved_on"], datatype=URIRef("http://www.w3.org/2001/XMLSchema#date"))))
    uml_root = ET.parse(directory / supporting["UMLMetamodel"]["file"]).getroot()
    uml_ids = {v for n in uml_root.iter() for k, v in n.attrib.items() if k.endswith("}id")}
    primitive_root = ET.parse(directory / supporting["UMLPrimitiveTypes"]["file"]).getroot()
    primitive_ids = {v for n in primitive_root.iter() for k, v in n.attrib.items() if k.endswith("}id")}
    for node in list(graph.subjects(RDF.type, INV.ExternalTypeReference)):
        if str(node).split("#")[-1] not in primitive_ids:
            raise ValueError("Missing primitive type definition")
        graph.set((node, INV.coverage, INV.ExternalIdentityVerified))
        graph.add((node, INV.sourceArtifact, ID["source/sha256/" + supporting["UMLPrimitiveTypes"]["sha256"]]))
        graph.add((node, DCTERMS.source, node))
    for prop in list(graph.subjects(RDF.type, INV.ExtractedPropertyRecord)):
        attrs = json.loads(str(graph.value(prop, INV.xmiAttributes)))
        normalized = normalize_declaration(attrs, *(json.loads(str(graph.value(prop, pred))) for pred in (INV.lowerEncoding, INV.upperEncoding, INV.defaultEncoding)))
        graph.set((prop, INV.normalizationDetail, Literal(json.dumps(normalized, sort_keys=True))))
        for name in ("lower", "upper"):
            item = normalized[name]
            if item["value"] is not None:
                val = Literal(item["value"] if name == "lower" else str(item["value"]))
                graph.add((prop, INV.lowerBound if name == "lower" else INV.upperBound, val))
        default = normalized["default"]
        graph.add((prop, INV.defaultStatus, INV[default["status"]]))
        if default["value"] is not None:
            graph.add((prop, INV.declaredDefault, Literal(default["value"])))
        for name, item in normalized["qualifiers"].items():
            graph.add((prop, INV["normalized" + name[0].upper() + name[1:]], Literal(item["value"])))
        evidence = {item["evidence"] for item in [normalized["lower"], normalized["upper"], *normalized["qualifiers"].values()]}
        if default.get("evidence"):
            evidence.add(default["evidence"])
        for url in evidence:
            if url.split("#")[-1] not in uml_ids:
                raise ValueError("Unknown UML normalization rule: " + url)
            graph.add((prop, INV.normalizationSource, URIRef(url)))
    return len(uml_ids)
