"""Notation source counting, traceability, and honest coverage claims."""
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import sys
import shutil
import unittest

from rdflib import RDF
from pyshacl import validate

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_notation import validate_index, validate_reviews, coverage, grammar_index, pdf_source
from check_inventory import load_graph, INV


class NotationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index=json.loads((ROOT/'data/notation-source-index.json').read_text())
        cls.reviews=json.loads((ROOT/'data/notation-reviews.json').read_text())
        cls.profiles=json.loads((ROOT/'data/concept-profiles.json').read_text())
        cls.graph=load_graph()

    def test_index_retains_repeated_cells_and_nonstandard_source_operators(self):
        validate_index(self.index)
        self.assertEqual(Counter(p['operator'] for p in self.index['productions']),{'=':523,'=|':97,'|=':19})
        matrix=[r for r in self.index['table_cells'] if r['table']==25 and r['label']=='Matrix View']
        self.assertEqual(len(matrix),2)
        self.assertNotEqual(matrix[0]['id'],matrix[1]['id'])
        self.assertEqual(len(self.index['table_cells']),192)
        self.assertEqual(len(set(p['name'] for p in self.index['productions'])),523)

    def test_generated_counts_match_graph_without_join_inflation(self):
        existing=validate_reviews(self.index,self.reviews,self.profiles)
        report=coverage(self.index,self.reviews,existing)
        self.assertEqual(report,json.loads((ROOT/'data/notation-coverage.json').read_text()))
        g=self.graph
        self.assertEqual(len(set(g.subjects(RDF.type,INV.GraphicalProductionOccurrence))),639)
        self.assertEqual(len(set(g.subjects(RDF.type,INV.NotationSourceCell))),192)
        self.assertEqual(len(set(g.subjects(RDF.type,INV.Notation))),6)
        self.assertEqual(len(list(g.query((ROOT/'queries/notation-records.rq').read_text()))),6)
        rows=list(g.query((ROOT/'queries/notation-coverage.rq').read_text()))
        self.assertEqual(sum(int(r.indexedProductions) for r in rows),639)
        self.assertEqual(sum(int(r.indexedCells) for r in rows),192)
        self.assertEqual(sum(int(r.mappedProductions) for r in rows),23)
        self.assertEqual(sum(int(r.mappedCells) for r in rows),7)
        self.assertEqual(len(list(g.query((ROOT/'queries/notation-gaps.rq').read_text()))),801)
        self.assertEqual(report['counts']['fully_audited_production_occurrences'],0)

    def test_unknown_source_and_exhaustive_claims_are_rejected(self):
        bad=deepcopy(self.reviews);bad['notations'][0]['production_ids']=['invented']
        with self.assertRaisesRegex(ValueError,'production mapping'):validate_reviews(self.index,bad,self.profiles)
        bad=deepcopy(self.reviews);bad['notations'][0]['coverage_claim']='Complete'
        with self.assertRaisesRegex(ValueError,'exhaustive'):validate_reviews(self.index,bad,self.profiles)
        bad=deepcopy(self.index);bad['source']['sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'source identity'):validate_index(bad)

    def test_missing_visual_conditions_and_dangling_mapping_fail_shacl(self):
        g=load_graph()
        record=next(g.subjects(INV.coverageClaim,None))
        g.remove((record,INV.condition,None))
        self.assertFalse(validate(g,shacl_graph=str(ROOT/'data/rdf/shapes.ttl'),inference='none')[0])
        g=load_graph()
        node=next(g.objects(record,INV.supportingProduction))
        g.remove((node,RDF.type,INV.GraphicalProductionOccurrence))
        self.assertFalse(validate(g,shacl_graph=str(ROOT/'data/rdf/shapes.ttl'),inference='none')[0])

    @unittest.skipUnless((ROOT/'sandbox/official-sources/SysML-Language.pdf').is_file() and shutil.which('pdftotext'),'Pinned PDF or Poppler unavailable')
    def test_pdf_hash_and_independent_text_modes_match_committed_index(self):
        import hashlib
        from build_notation import text_pages
        pdf=ROOT/'sandbox/official-sources/SysML-Language.pdf'
        self.assertEqual(hashlib.sha256(pdf.read_bytes()).hexdigest(),pdf_source()['sha256'])
        sections,layout=grammar_index(text_pages(pdf))
        _,raw=grammar_index(text_pages(pdf,raw=True))
        self.assertEqual(sections,self.index['sections'])
        self.assertEqual(layout,self.index['productions'])
        key=lambda p:(p['section'],p['name'],p['operator'],p['pdf_page'])
        self.assertEqual(Counter(map(key,layout)),Counter(map(key,raw)))


if __name__=='__main__':unittest.main()
