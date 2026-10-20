"""Portable SVG contract, provenance and distributable integrity."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from zipfile import ZipFile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_shapes import validate_definitions
from build_site import build
from check_inventory import load_graph, INV
from rdflib import RDF

NS={'s':'http://www.w3.org/2000/svg'}


class ShapeLibraryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog=json.loads((ROOT/'shapes/catalog.json').read_text())
        cls.index=json.loads((ROOT/'data/notation-source-index.json').read_text())

    def test_svg_metadata_hashes_geometry_and_scope_are_consistent(self):
        self.assertEqual(len(self.catalog['shapes']),20)
        symbols=ET.parse(ROOT/'shapes/shapes.svg').getroot()
        for shape in self.catalog['shapes']:
            path=ROOT/'shapes'/shape['file'];raw=path.read_bytes();svg=ET.fromstring(raw)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),shape['sha256'])
            metadata=json.loads(svg.find('s:metadata',NS).text)
            self.assertEqual(metadata['license'],'Apache-2.0')
            self.assertEqual(metadata['source_sha256'],self.index['source']['sha256'])
            self.assertEqual(metadata['production_ids'],shape['production_ids'])
            self.assertTrue(shape['limits']);self.assertTrue(shape['source_urls'])
            self.assertEqual(svg.get('viewBox'),' '.join(map(str,shape['viewBox'])))
            self.assertEqual(svg.get('role'),'img');self.assertTrue(svg.get('aria-label'))
            self.assertTrue(svg.find('s:title',NS).text)
            symbol=next(s for s in symbols if s.get('id')==shape['symbolId'])
            canonical=lambda node: ET.canonicalize(ET.tostring(node,encoding="unicode"),strip_text=True)
            self.assertEqual([canonical(c) for c in svg],[canonical(c) for c in symbol])
            for x,y in shape['anchors'].values():
                self.assertTrue(0<=x<=shape['viewBox'][2] and 0<=y<=shape['viewBox'][3])
            slots={n.get('data-slot') for n in svg.iter() if n.get('data-slot')}
            self.assertEqual(slots,set(shape['labelSlots']))
            # Standalone components can be safely cloned; no global styles or ID dependencies.
            for node in svg.iter():
                self.assertNotIn(node.tag.split('}')[-1],('script','foreignObject','image','style','use'))
                self.assertNotIn('id',node.attrib)
                self.assertFalse(any(k.lower().startswith('on') for k in node.attrib))
                self.assertFalse(any(k.endswith('href') for k in node.attrib))
        reference=ET.parse(ROOT/'shapes/svg/part-reference.svg')
        self.assertEqual(reference.find('.//s:rect',NS).get('stroke-dasharray'),'8 5')
        binding=ET.parse(ROOT/'shapes/svg/binding-connection.svg')
        self.assertEqual(binding.find('.//s:text',NS).text,'=')
        self.assertFalse(any(n.get('data-slot') for n in binding.iter()))

    def test_bundle_has_exact_files_and_preserves_license(self):
        expected={'LICENSE','README.md','catalog.json','shapes.svg','renderer.mjs',
                  'examples/composition.svg','examples/parts-ports.svg','examples/renderer.html'}
        expected.update(s['file'] for s in self.catalog['shapes'])
        with ZipFile(ROOT/'shapes/catalog.zip') as bundle:
            self.assertEqual(set(bundle.namelist()),expected)
            self.assertIsNone(bundle.testzip())
            for name in expected:self.assertEqual(bundle.read(name),(ROOT/'shapes'/name).read_bytes())
            self.assertEqual(bundle.read('LICENSE'),(ROOT/'LICENSE').read_bytes())
            self.assertNotIn('dsg-logo.png',bundle.namelist())

    def test_site_serves_exact_module_and_svg_bytes(self):
        with tempfile.TemporaryDirectory() as temp:
            output=Path(temp)/'site';build(output)
            for name in ('renderer.mjs','README.md','LICENSE','catalog.zip','catalog.json','svg/port-glyph.svg'):
                self.assertEqual((output/'shapes'/name).read_bytes(),(ROOT/'shapes'/name).read_bytes())
            gallery=(output/'docs/svg-shapes.html').read_text()
            self.assertEqual(gallery.count('class="shape-card"'),20)
            self.assertIn('href="../shapes/catalog.zip"',gallery)
            self.assertIn('href="svg-shapes-guide.html"',gallery)
            self.assertTrue((output/'docs/svg-shapes-guide.html').is_file())

    def test_catalog_requires_source_evidence_and_safe_ids(self):
        config=json.loads((ROOT/'data/svg-shapes.json').read_text())
        config['shapes'][0]['production_ids']=['nonexistent']
        with self.assertRaisesRegex(ValueError,'production evidence'):validate_definitions(config,self.index)
        config=json.loads((ROOT/'data/svg-shapes.json').read_text())
        config['shapes'][0]['id']='../bad'
        with self.assertRaisesRegex(ValueError,'SVG ID'):validate_definitions(config,self.index)
        config=json.loads((ROOT/'data/svg-shapes.json').read_text())
        next(s for s in config['shapes'] if s['id']=='part-definition-parts')['rows'].append('unsupported third row')
        with self.assertRaisesRegex(ValueError,'exactly two literal rows'):validate_definitions(config,self.index)
        config=json.loads((ROOT/'data/svg-shapes.json').read_text())
        next(s for s in config['shapes'] if s['id']=='port-arrow-up')['direction_indicator']='diagonal'
        with self.assertRaisesRegex(ValueError,'direction indicator'):validate_definitions(config,self.index)
        graph=load_graph()
        self.assertEqual(len(set(graph.subjects(RDF.type,INV.SVGShapeAsset))),20)
        self.assertEqual(len(list(graph.query((ROOT/'queries/svg-shapes.rq').read_text()))),20)

    @unittest.skipUnless(shutil.which('node'),'Node unavailable')
    def test_renderer_anchor_math_includes_letterboxing_and_rejects_bad_sizes(self):
        module=(ROOT/'shapes/renderer.mjs').as_uri()
        shape=next(s for s in self.catalog['shapes'] if s['id']=='part-usage')
        code=f"""
import assert from 'node:assert/strict';
import {{anchorPositions}} from {json.dumps(module)};
const shape={json.dumps(shape)};
assert.deepEqual(anchorPositions(shape,{{x:20,y:50}}).east,{{x:252,y:120}});
assert.deepEqual(anchorPositions(shape,{{width:480,height:140}}).east,{{x:352,y:70}});
assert.deepEqual(anchorPositions(shape,{{width:480,height:280,x:10,y:20}}).north,{{x:250,y:36}});
for (const value of [0,-1,Infinity,NaN,'240']) assert.throws(()=>anchorPositions(shape,{{width:value}}));
assert.throws(()=>anchorPositions(shape,{{x:'20'}}));
"""
        subprocess.run(['node','--input-type=module','-e',code],check=True,capture_output=True,text=True)


if __name__=='__main__':unittest.main()
