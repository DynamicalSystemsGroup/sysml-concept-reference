"""Publishing checks for project-path navigation and the static artifact boundary."""
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_site import build, check_links


class SiteTests(unittest.TestCase):
    def test_site_includes_browser_notes_and_exact_downloads(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "sysml-concept-reference"
            pages, links = build(output)
            self.assertGreaterEqual(pages, 10)
            self.assertGreater(links, 100)
            for path in ("index.html", "docs/concept-browser.html", "docs/rdf-inventory.html",
                         "data/index.html", "queries/index.html", "assets/style.css",
                         "assets/brand/dsg-wordmark.png", "assets/brand/fonts/ibm-plex-sans.woff2",
                         "docs/concepts/part-usage.html", "docs/concepts/port-usage.html",
                         "docs/assets/notation/connection-usage.svg", "data/rdf/profiles.ttl",
                         "docs/notation-coverage.html", "docs/notation-register.html",
                         "data/notation-source-index.json", "data/notation-coverage.json",
                         "data/rdf/notation-register.ttl"):
                self.assertTrue((output / path).is_file(), path)
            self.assertEqual((output / "data/rdf/metamodel.ttl").read_bytes(), (ROOT / "data/rdf/metamodel.ttl").read_bytes())
            self.assertFalse((output / "sandbox").exists())
            self.assertFalse((output / ".venv").exists())
            self.assertFalse((output / "scripts").exists())
            self.assertIn('href="notation-coverage.html"', (output / "docs/concept-browser.html").read_text())
            self.assertIn('href="../index.html"', (output / "docs/concept-browser.html").read_text())
            self.assertIn('/blob/main/scripts/build_browser.py', (output / "docs/rdf-inventory.html").read_text())

    def test_broken_published_link_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            (output / "index.html").write_text('<a href="missing.html">Broken</a>')
            with self.assertRaisesRegex(ValueError, "Broken site link"):
                check_links(output)

    def test_root_relative_link_fails_for_project_pages(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            (output / "index.html").write_text('<a href="/index.html">Wrong root</a>')
            with self.assertRaisesRegex(ValueError, "Root-relative link"):
                check_links(output)

    def test_build_preserves_unrecognized_output_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "existing"
            output.mkdir()
            keep = output / "keep.txt"
            keep.write_text("User content")
            with self.assertRaisesRegex(ValueError, "without the site build marker"):
                build(output)
            self.assertEqual(keep.read_text(), "User content")


if __name__ == "__main__":
    unittest.main()
