"""Inheritance edge cases that a simple name-based flattening gets wrong."""
import json
from pathlib import Path
import sys
import unittest

from rdflib import Graph, Literal, Namespace, RDFS

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from property_resolution import INV, inheritance_paths, resolve_properties

N = Namespace("urn:inventory-test:")


class PropertyResolutionTests(unittest.TestCase):
    def setUp(self):
        self.g = Graph()

    def cls(self, name, bases=()):
        c = N[name]
        self.g.add((c, INV.coverage, INV.DeclaredPropertiesExtracted))
        for base in bases:self.g.add((c, INV.specializes, base))
        return c

    def prop(self, owner, key, name="field", visibility=None, redefines=()):
        p = N[key]
        attrs = {"visibility": visibility} if visibility else {}
        self.g.add((owner, INV.declaresProperty, p))
        self.g.add((p, INV.declaredOn, owner));self.g.add((p, RDFS.label, Literal(name)))
        self.g.add((p, INV.xmiAttributes, Literal(json.dumps(attrs))))
        for target in redefines:self.g.add((p, INV.redefines, target))
        return p

    def test_diamond_preserves_one_identity_and_both_paths(self):
        a = self.cls("A");p = self.prop(a,"a-field")
        b = self.cls("B",[a]);c = self.cls("C",[a]);d = self.cls("D",[b,c])
        result=resolve_properties(self.g,d)
        self.assertEqual(result["active"],[p])
        self.assertEqual(len(inheritance_paths(self.g,d,a)),2)

    def test_transitive_redefinition_hides_ancestors_and_retains_history(self):
        a=self.cls("A");p=self.prop(a,"original")
        b=self.cls("B",[a]);q=self.prop(b,"replacement",redefines=[p])
        c=self.cls("C",[b]);r=self.prop(c,"latest",redefines=[q])
        result=resolve_properties(self.g,c)
        self.assertEqual(result["active"],[r])
        self.assertEqual(result["replaced"][p],[r]);self.assertEqual(result["replaced"][q],[r])

    def test_redefinition_on_one_diamond_branch_does_not_resurrect_original(self):
        a=self.cls("A");p=self.prop(a,"original")
        b=self.cls("B",[a]);q=self.prop(b,"replacement",redefines=[p])
        c=self.cls("C",[a]);d=self.cls("D",[b,c])
        self.assertEqual(resolve_properties(self.g,d)["active"],[q])

    def test_same_name_without_redefinition_remains_a_conflict(self):
        a=self.cls("A");p=self.prop(a,"one")
        b=self.cls("B");q=self.prop(b,"two")
        c=self.cls("C",[a,b]);r=resolve_properties(self.g,c)
        self.assertEqual(set(r["active"]),{p,q});self.assertEqual(set(r["conflicts"]["field"]),{p,q})

    def test_private_member_is_local_but_not_inherited(self):
        a=self.cls("A");p=self.prop(a,"private-field",visibility="private")
        b=self.cls("B",[a])
        self.assertIn(p,resolve_properties(self.g,a)["active"])
        self.assertNotIn(p,resolve_properties(self.g,b)["active"])
        self.assertIn(p,resolve_properties(self.g,b)["excluded_private"])

    def test_cycles_and_unextracted_bases_are_explicit_failures(self):
        a=self.cls("A");b=self.cls("B",[a]);self.g.add((a,INV.specializes,b))
        with self.assertRaisesRegex(ValueError,"Generalization cycle"):resolve_properties(self.g,a)
        self.g.remove((a,INV.specializes,b));self.g.add((a,INV.specializes,N.Missing))
        with self.assertRaisesRegex(ValueError,"unextracted superclass"):resolve_properties(self.g,a)

    def test_redefinition_cycle_is_an_explicit_failure(self):
        a=self.cls("A");p=self.prop(a,"one");q=self.prop(a,"two",redefines=[p]);self.g.add((p,INV.redefines,q))
        with self.assertRaisesRegex(ValueError,"Redefinition cycle"):resolve_properties(self.g,a)


if __name__ == "__main__":unittest.main()
