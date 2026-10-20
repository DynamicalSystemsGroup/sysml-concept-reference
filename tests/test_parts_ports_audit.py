"""Audit closure, explicit deferrals and component contracts must agree."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest
import xml.etree.ElementTree as ET
from rdflib import RDF
from pyshacl import validate

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from parts_ports_audit import validate_audit, audit_counts
from check_inventory import load_graph, INV

class PartsPortsAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit=json.loads((ROOT/'data/parts-ports-audit.json').read_text())
        cls.index=json.loads((ROOT/'data/notation-source-index.json').read_text())
        cls.assets=json.loads((ROOT/'data/svg-shapes.json').read_text())

    def test_selected_source_units_and_query_rows_are_independent_of_asset_counts(self):
        validate_audit(self.index,self.audit,self.assets)
        counts=audit_counts(self.audit)
        self.assertEqual(counts['audited_source_cells'],12)
        self.assertEqual(counts['audited_production_occurrences'],38)
        self.assertEqual(counts['alternative_records'],106)
        self.assertGreater(counts['deferred_records'],0)
        g=load_graph()
        self.assertEqual(len(set(g.subjects(RDF.type,INV.SourceUnitAudit))),50)
        self.assertEqual(len(list(g.query((ROOT/'queries/notation-alternatives.rq').read_text()))),106)

    def test_omitted_unit_or_unexplained_alternative_cannot_pass_as_a_complete_audit(self):
        bad=deepcopy(self.audit);bad['units'].pop()
        with self.assertRaisesRegex(ValueError,'exactly the selected'):validate_audit(self.index,bad,self.assets)
        bad=deepcopy(self.audit)
        alt=next(a for u in bad['units'] for a in u['alternatives'] if not a['represented_by']);alt['deferred_reason']=None
        with self.assertRaisesRegex(ValueError,'neither asset nor deferral'):validate_audit(self.index,bad,self.assets)
        bad=deepcopy(self.audit);bad['units'][0]['alternatives'][0]['represented_by']=['invented']
        with self.assertRaisesRegex(ValueError,'unknown asset'):validate_audit(self.index,bad,self.assets)

    def test_source_identity_and_page_numbers_are_not_interchangeable(self):
        bad=deepcopy(self.audit);bad['source']['sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'identity mismatch'):validate_audit(self.index,bad,self.assets)
        bad=deepcopy(self.audit);bad['units'][0]['printed_pages']=bad['units'][0]['source_pages']
        with self.assertRaisesRegex(ValueError,'printed pages mismatch'):validate_audit(self.index,bad,self.assets)

    def test_shacl_rejects_lost_deferrals_and_dangling_component_claims(self):
        g=load_graph();alt=next(g.subjects(INV.renderingStatus,INV.DeferredRendering));g.remove((alt,INV.deferredReason,None))
        self.assertFalse(validate(g,shacl_graph=str(ROOT/'data/rdf/shapes.ttl'),inference='none')[0])
        g=load_graph();asset=next(g.objects(None,INV.representedByAsset));g.remove((asset,RDF.type,INV.SVGShapeAsset))
        self.assertFalse(validate(g,shacl_graph=str(ROOT/'data/rdf/shapes.ttl'),inference='none')[0])

    def test_compartment_slots_and_direction_geometry_are_distinct(self):
        catalog=json.loads((ROOT/'shapes/catalog.json').read_text());assets={a['id']:a for a in catalog['shapes']}
        self.assertEqual(set(assets['part-definition-parts']['labelSlots']),{'label','row1','row2'})
        self.assertGreater(assets['part-definition-parts']['viewBox'][3],assets['part-definition']['viewBox'][3])
        ns={'s':'http://www.w3.org/2000/svg'}
        paths=[]
        for direction in ['left','right','up','down','horizontal-both','vertical-both']:
            root=ET.parse(ROOT/'shapes/svg'/('port-arrow-'+direction+'.svg'))
            paths.append(root.find('.//s:path',ns).get('d'))
        self.assertEqual(len(set(paths)),6)
        root=ET.parse(ROOT/'shapes/svg/port-definition.svg')
        self.assertIsNone(root.find('.//s:rect',ns).get('rx'))
        self.assertIn('«port def»',[n.text for n in root.findall('.//s:text',ns)])

if __name__=='__main__':unittest.main()
