"""Checks for decoded defaults, source-backed profiles and unresolved claims."""
import json
from pathlib import Path
import sys
import unittest

from rdflib import Literal, RDF, RDFS
from rdflib.namespace import DCTERMS
from pyshacl import validate

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from normalize_xmi import decode_bound, decode_literal, normalize_declaration
from check_inventory import INV, check, load_graph
from build_profiles import reconcile

ABSENT={"present":False}


class NormalizationTests(unittest.TestCase):
    def test_absent_bound_is_one_but_omitted_numeric_literal_is_zero(self):
        self.assertEqual(decode_bound(ABSENT,True)["value"],1)
        self.assertEqual(decode_bound({"present":True,"type":"uml:LiteralInteger","value":None},True)["value"],0)
        self.assertEqual(decode_bound({"present":True,"type":"uml:LiteralUnlimitedNatural","value":"-1"},False)["value"],"*")

    def test_no_default_is_not_false_and_absent_string_is_not_empty(self):
        self.assertEqual(decode_literal(ABSENT)["status"],"NoDeclaredDefault")
        self.assertIsNone(decode_literal(ABSENT)["value"])
        self.assertIs(decode_literal({"present":True,"type":"uml:LiteralBoolean","value":None})["value"],False)
        missing=decode_literal({"present":True,"type":"uml:LiteralString","value":None})
        empty=decode_literal({"present":True,"type":"uml:LiteralString","value":""})
        self.assertEqual(missing["status"],"UnspecifiedLiteralValue");self.assertEqual(empty["value"],"")

    def test_independent_qualifiers_and_literal_kind_are_retained(self):
        result=normalize_declaration({"isDerived":"true"},ABSENT,ABSENT,ABSENT)
        self.assertTrue(result["qualifiers"]["isDerived"]["value"])
        self.assertFalse(result["qualifiers"]["isReadOnly"]["value"])
        self.assertTrue(result["qualifiers"]["isUnique"]["value"])
        self.assertEqual(decode_literal({"present":True,"type":"uml:LiteralString","value":"true"})["value"],"true")

    def test_unsupported_expressions_and_invalid_booleans_are_not_guessed(self):
        self.assertEqual(decode_literal({"present":True,"type":"uml:OpaqueExpression","value":None})["status"],"UnsupportedExpression")
        with self.assertRaisesRegex(ValueError,"Invalid Boolean"):decode_literal({"present":True,"type":"uml:LiteralBoolean","value":"maybe"})


class ProfileTests(unittest.TestCase):
    def setUp(self):self.g=load_graph()

    def conforms(self):return validate(self.g,shacl_graph=str(ROOT/"data/rdf/shapes.ttl"),inference="none")[0]

    def test_four_profiles_have_explanations_for_every_active_property(self):
        profiles=list(self.g.subjects(RDF.type,INV.ConceptProfile));self.assertEqual(len(profiles),4)
        for profile in profiles:
            concept=self.g.value(profile,INV.concept)
            for prop in self.g.objects(concept,INV.effectiveProperty):
                self.assertTrue(self.g.value(prop,DCTERMS.description),str(prop))
                self.assertEqual(self.g.value(prop,INV.descriptionStatus),INV.EditorialSummary)
        self.assertTrue(check(self.g))

    def test_missing_relationship_condition_and_notation_evidence_fail_shapes(self):
        relation=next(self.g.subjects(RDF.type,INV.ConceptRelationship))
        self.g.remove((relation,INV.condition,None));self.assertFalse(self.conforms())
        self.g=load_graph();notation=next(self.g.subjects(RDF.type,INV.Notation))
        self.g.remove((notation,INV.evidence,None));self.assertFalse(self.conforms())

    def test_fabricated_default_and_parser_verified_status_are_rejected(self):
        prop=next(self.g.subjects(INV.defaultStatus,INV.NoDeclaredDefault))
        self.g.add((prop,INV.declaredDefault,Literal(False)));self.assertFalse(self.conforms())
        self.g=load_graph();example=next(self.g.subjects(RDF.type,INV.Example))
        self.g.set((example,INV.verificationStatus,INV.ParserValidated));self.assertFalse(self.conforms())

    def test_stale_materialized_property_view_is_detected(self):
        concept=next(self.g.subjects(INV.effectiveProperty,None));prop=next(self.g.objects(concept,INV.effectiveProperty))
        self.g.remove((concept,INV.effectiveProperty,prop))
        with self.assertRaisesRegex(ValueError,"stale"):check(self.g)

    def test_seed_reconciliation_reports_real_differences(self):
        profiles=json.loads((ROOT/"data/concept-profiles.json").read_text())["profiles"]
        seed=json.loads((ROOT/"data/language-inventory.json").read_text())
        original=reconcile(self.g,profiles,seed)
        self.assertTrue(all(c["status"]=="SelectedFieldsMatch" for c in original["concepts"]))
        part=next(e for e in seed["entries"] if e["name"]=="PartUsage")
        part["attributes"][0]["derived"]=False
        changed=reconcile(self.g,profiles,seed)
        self.assertTrue(any("Derived flag differs" in diff for c in changed["concepts"] for diff in c["differences"]))


if __name__=="__main__":unittest.main()
