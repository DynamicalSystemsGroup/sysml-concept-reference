"""Checks for provenance loss, broken links and unsafe source changes."""
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

from pyshacl import validate
from rdflib import Literal, RDF, URIRef
from rdflib.namespace import DCTERMS

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_inventory import Extractor, INV, XMI, fetch
from check_inventory import load_graph


class CatalogueTests(unittest.TestCase):
    def setUp(self):
        self.g = load_graph()

    def conforms(self):
        return validate(self.g, shacl_graph=str(ROOT / "data/rdf/shapes.ttl"), inference="none")[0]

    def test_current_catalogue_validates(self):
        self.assertTrue(self.conforms())

    def test_missing_source_is_rejected(self):
        prop = next(self.g.subjects(RDF.type, INV.ExtractedPropertyRecord))
        self.g.remove((prop, DCTERMS.source, None))
        self.assertFalse(self.conforms())

    def test_dangling_value_type_is_rejected(self):
        prop = next(self.g.subjects(RDF.type, INV.ExtractedPropertyRecord))
        self.g.set((prop, INV.valueType, URIRef("urn:missing:type")))
        self.assertFalse(self.conforms())

    def test_unsupported_applicability_is_rejected(self):
        app = next(self.g.subjects(RDF.type, INV.MechanismApplication))
        self.g.set((app, INV.applicability, Literal("certainly always allowed")))
        self.assertFalse(self.conforms())

    def test_part_ancestry_retains_declaration_origin(self):
        rows = list(self.g.query((ROOT / "queries/part-properties.rq").read_text()))
        composite = [row for row in rows if str(row.property).endswith("Core-Features-Feature-isComposite")]
        self.assertEqual(len(composite), 1)
        self.assertTrue(str(composite[0].owner).endswith("Core-Features-Feature"))
        self.assertTrue(str(composite[0].source).endswith("#Core-Features-Feature-isComposite"))
        self.assertTrue(any(row.redefines is not None for row in rows))


class SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((ROOT / "data/source-manifest.json").read_text())
        cls.directory = ROOT / "sandbox/official-sources"

    def setUp(self):
        if not all((self.directory / (s["language"] + ".xmi")).exists() for s in self.manifest["artifacts"]):
            self.skipTest("Pinned originals absent: run build_inventory.py --fetch for source checks")
        self.extractor = Extractor(self.manifest, self.directory)

    def test_all_curated_evidence_locations_exist_in_pinned_sources(self):
        g = load_graph()
        for url in g.objects(None, INV.evidence):
            base, fragment = str(url).split("#", 1)
            if base in self.extractor.sources:
                self.assertIn((base, fragment), self.extractor.nodes)
            else:
                self.assertTrue(fragment.startswith("page="))
                self.assertIn(base, {a["url"] for a in self.manifest["supporting_artifacts"]})
                self.assertEqual(int(fragment[5:]), int(g.value(url, INV.pdfPage)))

    def test_changed_source_is_rejected_without_overwriting(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            for source in self.manifest["artifacts"]:
                shutil.copyfile(self.directory / (source["language"] + ".xmi"), directory / (source["language"] + ".xmi"))
            path = directory / "KerML.xmi"
            path.write_bytes(path.read_bytes() + b"\n")
            changed = path.read_bytes()
            with self.assertRaisesRegex(ValueError, "Pinned content mismatch"):
                fetch(self.manifest, directory)
            self.assertEqual(path.read_bytes(), changed)

    def test_unresolved_reference_fails(self):
        with self.assertRaisesRegex(ValueError, "Unresolved reference"):
            self.extractor.record((self.manifest["artifacts"][0]["url"], "missing-id"))

    def test_ambiguous_focus_selection_fails(self):
        node = next(n for n in self.extractor.nodes.values() if n.get(XMI + "type") == "uml:Class" and n.get("name") == "Element")
        node.set("name", "MissingElement")
        with self.assertRaisesRegex(ValueError, "Focus selection"):
            self.extractor.build()


if __name__ == "__main__":
    unittest.main()
