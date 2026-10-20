"""Build an allowlisted GitHub Pages site and check every internal link."""
from __future__ import annotations

import argparse
from html import escape
from html.parser import HTMLParser
import os
from pathlib import Path
import re
import shutil
from urllib.parse import quote, unquote, urlsplit, urlunsplit

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
REPO = "https://github.com/DynamicalSystemsGroup/sysml-concept-reference"
NAV = [
    ("Home", "index.html"),
    ("Concept browser", "docs/concept-browser.html"),
    ("Notation coverage", "docs/notation-coverage.html"),
    ("Notation source register", "docs/notation-register.html"),
    ("Concept-page contract", "docs/concept-page-contract.html"),
    ("Part usage", "docs/concepts/part-usage.html"),
    ("Part definition", "docs/concepts/part-definition.html"),
    ("Port usage", "docs/concepts/port-usage.html"),
    ("Connection usage", "docs/concepts/connection-usage.html"),
    ("RDF inventory", "docs/rdf-inventory.html"),
    ("Official sources", "docs/official-machine-readable-specs.html"),
    ("Language research", "docs/language-research.html"),
    ("Roadmap", "docs/roadmap.html"),
    ("Data downloads", "data/index.html"),
    ("SPARQL queries", "queries/index.html"),
    ("Publishing", "docs/publishing.html"),
]


def relative(destination: str, current: str) -> str:
    return Path(os.path.relpath(destination, Path(current).parent)).as_posix()


def layout(body: str, title: str, current: str, source: str | None = None) -> str:
    def a(label, path):
        active = ' aria-current="page"' if path == current else ""
        return f'<a href="{escape(relative(path, current))}"{active}>{escape(label)}</a>'
    navigation = "".join(a(label, path) for label, path in NAV)
    edit = f'<p class="edit"><a href="{REPO}/blob/main/{quote(source)}">View this page’s source on GitHub</a></p>' if source else ""
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} | SysML Concept Reference</title><meta name="description" content="Source-backed KerML and SysML v2 concepts, properties, relationships and research.">
<link rel="stylesheet" href="{escape(relative('assets/brand/brand.css', current))}"><link rel="stylesheet" href="{escape(relative('assets/style.css', current))}"><link rel="icon" href="{escape(relative('assets/brand/dsg-logo.png', current))}" type="image/png"></head>
<body><a class="skip" href="#main">Skip to content</a>
<header class="site-nav"><a class="dsg-logo" href="https://www.dynamicalsystemsgroup.com/" aria-label="Dynamical Systems Group website"><img src="{escape(relative('assets/brand/dsg-wordmark.png', current))}" alt="Dynamical Systems Group" width="185" height="48"></a><a class="brand" href="{escape(relative('index.html', current))}">SysML Concept Reference</a>
<nav aria-label="Primary">{a('Explore concepts', 'docs/concept-browser.html')}{a('Research', 'docs/rdf-inventory.html')}<a href="{REPO}">GitHub</a></nav></header>
<div class="shell"><aside class="sidebar"><details open><summary>Contents</summary><nav aria-label="Research guides">{navigation}</nav></details></aside>
<main id="main"><article>{body}{edit}</article></main></div>
<footer class="site-footer"><strong>A Dynamical Systems Group project</strong><nav aria-label="DSG links"><a href="https://www.dynamicalsystemsgroup.com/">DSG website</a><a href="https://github.com/DynamicalSystemsGroup">DSG on GitHub</a><a href="{REPO}">Source repository</a></nav><p>Research based on official OMG sources. Editorial interpretations and coverage limits are recorded with the evidence.</p></footer>
</body></html>'''


class SiteLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            self.ids.add(values["id"])
        for attr in ("href", "src"):
            if attr in values:
                self.links.append(values[attr])


def check_links(directory: Path) -> tuple[int, int]:
    pages = {}
    for file in directory.rglob("*.html"):
        parser = SiteLinks()
        parser.feed(file.read_text())
        pages[file] = parser
    sources = {file: parser.links + re.findall(r'url\([\'"]?([^\)\'"\s]+)', file.read_text()) for file, parser in pages.items()}
    sources.update({file: re.findall(r'url\([\'"]?([^\)\'"\s]+)', file.read_text()) for file in directory.rglob("*.css")})
    count = 0
    for file, links in sources.items():
        for link in links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            if url.path.startswith("/"):
                raise ValueError(f"Root-relative link breaks project Pages paths: {file}: {link}")
            target = (file.parent / unquote(url.path)).resolve() if url.path else file
            if not target.is_relative_to(directory.resolve()):
                raise ValueError(f"Link escapes published site: {file}: {link}")
            if target.is_dir():
                target /= "index.html"
            if not target.is_file():
                raise ValueError(f"Broken site link: {file}: {link}")
            if url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                raise ValueError(f"Missing HTML fragment: {file}: {link}")
            count += 1
    return len(pages), count


def build(output: Path) -> tuple[int, int]:
    output = output.resolve()
    if output == ROOT or ROOT.is_relative_to(output):
        raise ValueError("Output must not be the repository or its parent")
    marker = output / ".inventory-site-build"
    if output.exists():
        if not marker.is_file():
            raise ValueError("Refusing to replace an output directory without the site build marker")
        shutil.rmtree(output)
    output.mkdir(parents=True)
    marker.write_text("Generated site; safe to rebuild.\n")
    (output / ".nojekyll").touch()
    mapping = {ROOT / "site/index.md": "index.html", ROOT / "README.md": "docs/repository.html"}
    mapping.update({p: "docs/" + p.relative_to(ROOT / "docs").with_suffix(".html").as_posix() for p in sorted((ROOT / "docs").rglob("*.md"))})
    browser = ROOT / "docs/concept-browser.html"
    mapping[browser] = "docs/concept-browser.html"
    downloads = [ROOT / "data/language-inventory.json", ROOT / "data/source-manifest.json",
                 ROOT / "data/notation-source-index.json", ROOT / "data/notation-reviews.json", ROOT / "data/notation-coverage.json",
                 ROOT / "data/namespace-migration.json", ROOT / "data/concept-profiles.json", ROOT / "data/property-explanations.json", ROOT / "data/profile-reconciliation.json",
                 ROOT / "data/examples/assembly.sysml",
                 *sorted((ROOT / "data/rdf").glob("*.ttl")), ROOT / "data/rdf/extraction-report.json",
                 *sorted((ROOT / "queries").glob("*.rq"))]
    mapping.update({p: p.relative_to(ROOT).as_posix() for p in downloads})
    mapping.update({p: p.relative_to(ROOT).as_posix() for p in sorted((ROOT / "docs/assets/notation").glob("*.svg"))})
    css = output / "assets/style.css"
    css.parent.mkdir(parents=True)
    shutil.copyfile(ROOT / "site/style.css", css)
    brand_dir = output / "assets/brand"
    brand_dir.mkdir(parents=True)
    shutil.copyfile(ROOT / "site/brand.css", brand_dir / "brand.css")
    for asset in (ROOT / "site/assets").rglob("*"):
        if asset.is_file():
            destination = brand_dir / asset.relative_to(ROOT / "site/assets")
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(asset, destination)
    # Offline browser assets use the same relative paths as docs/concept-browser.html.
    shutil.copytree(brand_dir, output / "docs/assets/brand", dirs_exist_ok=True)

    def rewrite(href: str, source: Path, destination: str):
        parsed = urlsplit(href)
        if parsed.scheme or parsed.netloc or not parsed.path:
            return href
        if parsed.path.startswith("/"):
            raise ValueError(f"Unexpected absolute local link: {source}: {href}")
        target = (source.parent / unquote(parsed.path)).resolve()
        if not target.is_relative_to(ROOT) or not target.exists():
            raise ValueError(f"Missing or out-of-repository source link: {source}: {href}")
        if target in mapping:
            path = relative(mapping[target], destination)
        elif target.is_dir() and target.relative_to(ROOT).as_posix() in ("data", "data/rdf", "queries"):
            directory = target.relative_to(ROOT).as_posix()
            path = relative("queries/index.html" if directory == "queries" else "data/index.html", destination)
        else:
            kind = "tree" if target.is_dir() else "blob"
            return f"{REPO}/{kind}/main/{quote(target.relative_to(ROOT).as_posix())}" + ("#" + parsed.fragment if parsed.fragment else "")
        return urlunsplit(("", "", path, parsed.query, parsed.fragment))

    for source, destination in mapping.items():
        if source.is_symlink():
            raise ValueError(f"Refusing to publish a symbolic link: {source}")
        target = output / destination
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.suffix != ".md":
            if source == browser:
                html = source.read_text().replace('href="notation-coverage.md"', 'href="notation-coverage.html"')
                navbar = '<nav class="browser-nav" aria-label="Research site"><strong>SysML Concept Reference</strong><a href="../index.html">Home</a><a href="rdf-inventory.html">Research guide</a><a href="../data/index.html">Download data</a></nav>'
                html = html.replace("</head>", '<link rel="stylesheet" href="../assets/style.css"></head>', 1)
                # Only browser-nav styles should affect the existing standalone browser.
                html = html.replace('<link rel="stylesheet" href="../assets/style.css">', '<style>.browser-nav{display:flex;gap:22px;flex-wrap:wrap;align-items:center;padding:14px 5vw;background:var(--wash);border-bottom:1px solid var(--line);font:14px/1.5 var(--font-body)}.browser-nav strong{margin-right:auto}</style>')
                target.write_text(html.replace("<body>", "<body>\n" + navbar, 1))
            else:
                shutil.copyfile(source, target)
            continue
        md = MarkdownIt("commonmark", {"html": False}).enable("table")
        tokens = md.parse(source.read_text())
        headings = set()
        for i, token in enumerate(tokens):
            if token.type == "heading_open":
                text = tokens[i + 1].content
                slug = re.sub(r"[^\w\s-]", "", text.lower()).strip().replace(" ", "-")
                unique = slug
                n = 1
                while unique in headings:
                    unique = f"{slug}-{n}"
                    n += 1
                headings.add(unique)
                token.attrSet("id", unique)
            for child in token.children or []:
                if child.type == "link_open":
                    child.attrSet("href", rewrite(child.attrGet("href"), source, destination))
                elif child.type == "image":
                    child.attrSet("src", rewrite(child.attrGet("src"), source, destination))
        title = next((tokens[i + 1].content for i, t in enumerate(tokens) if t.type == "heading_open"), source.stem)
        body = md.renderer.render(tokens, md.options, {})
        target.write_text(layout(body, title, destination, source.relative_to(ROOT).as_posix()))
    for directory, title, paths in (("data", "Download inventory data", [p for p in downloads if p.parent.name != "queries"]),
                                    ("queries", "Saved SPARQL queries", [p for p in downloads if p.suffix == ".rq"])):
        current = f"{directory}/index.html"
        rows = "".join(f'<li><a href="{escape(relative(mapping[p], current))}">{escape(p.relative_to(ROOT).as_posix())}</a></li>' for p in paths)
        body = f'<h1>{escape(title)}</h1><p>These files are the same reviewed sources used by the concept catalogue. Download them for local inspection and queries.</p><ul>{rows}</ul>'
        (output / current).parent.mkdir(parents=True, exist_ok=True)
        (output / current).write_text(layout(body, title, current))
    return check_links(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "_site")
    args = parser.parse_args()
    pages, links = build(args.output)
    print(f"Built {pages} HTML pages; checked {links} internal links in {args.output}")


if __name__ == "__main__":
    main()
