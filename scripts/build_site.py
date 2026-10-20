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
from page_layout import REPO, NAV, relative, layout


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
    mapping[ROOT / "LICENSE"] = "LICENSE"
    mapping[ROOT / "docs/svg-shapes.html"] = "docs/svg-shapes.html"
    # Publish only the declared library files, never arbitrary working files.
    import json
    shape_catalog = json.loads((ROOT / "shapes/catalog.json").read_text())
    shape_files = ["README.md", "LICENSE", "catalog.json", "catalog.zip", "shapes.svg", "renderer.mjs",
                   "examples/composition.svg", "examples/parts-ports.svg", "examples/renderer.html"]
    shape_files += [shape["file"] for shape in shape_catalog["shapes"]]
    for name in shape_files:
        path = (ROOT / "shapes" / name).resolve()
        if not path.is_relative_to(ROOT / "shapes"):
            raise ValueError("Shape download escapes the library directory")
        mapping[path] = path.relative_to(ROOT).as_posix()
    downloads = [ROOT / "data/language-inventory.json", ROOT / "data/source-manifest.json",
                 ROOT / "data/notation-source-index.json", ROOT / "data/notation-reviews.json", ROOT / "data/notation-coverage.json",
                 ROOT / "data/svg-shapes.json", ROOT / "data/parts-ports-audit.json",
                 ROOT / "data/namespace-migration.json", ROOT / "data/concept-profiles.json", ROOT / "data/property-explanations.json", ROOT / "data/profile-reconciliation.json",
                 ROOT / "data/examples/assembly.sysml",
                 *sorted((ROOT / "data/rdf").glob("*.ttl")), ROOT / "data/rdf/extraction-report.json",
                 *sorted((ROOT / "queries").glob("*.rq"))]
    mapping.update({p: p.relative_to(ROOT).as_posix() for p in downloads})
    mapping.update({p: p.relative_to(ROOT).as_posix() for p in sorted((ROOT / "docs/assets/notation").glob("*.svg"))})
    css = output / "assets/style.css"
    css.parent.mkdir(parents=True)
    shutil.copyfile(ROOT / "site/style.css", css)
    shutil.copyfile(ROOT / "site/site.js", output / "assets/site.js")
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
        if source.suffix != ".md" or source.is_relative_to(ROOT / "shapes"):
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
        md.renderer.rules["table_open"] = lambda tokens, idx, options, env: '<div class="table-scroll" role="region" tabindex="0" aria-label="Reference table"><table>'
        md.renderer.rules["table_close"] = lambda tokens, idx, options, env: '</table></div>'
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
