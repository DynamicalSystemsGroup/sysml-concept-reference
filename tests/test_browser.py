"""The real browser application can render without runtime exceptions."""
from pathlib import Path
import shutil
import subprocess
import unittest

ROOT=Path(__file__).resolve().parents[1]


class BrowserApplicationTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which("node"), "Node is required for the generated-application smoke check")
    def test_generated_application_and_handlers(self):
        subprocess.run(["node",str(ROOT/"tests/browser-smoke.cjs"),str(ROOT/"docs/concept-browser.html")],check=True,capture_output=True,text=True)


if __name__=="__main__":unittest.main()
