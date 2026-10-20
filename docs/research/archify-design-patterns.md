# Archify design patterns for the concept reference

Reviewed 2026-10-21 against upstream commit [`25cf37080fc8b1dbe758a4efc3935b55f3327083`](https://github.com/tt-a1i/archify/tree/25cf37080fc8b1dbe758a4efc3935b55f3327083). This combines a source-code review with a desktop visual inspection of the pinned upstream HTTPS explainer example. We did not run Archify's own browser gates. No upstream implementation was copied into this project.

## What the source actually does

Archify has two presentation systems. Its diagram Viewer is a dense technical canvas with a semantic palette and mono typography; its explainer reader is a quieter document with prose, panels and supporting diagrams. The reader is the closer reference for our catalogue. These are explicit design choices, rather than a single effect or CSS library. [Design system](https://github.com/tt-a1i/archify/blob/25cf37080fc8b1dbe758a4efc3935b55f3327083/DESIGN.md), [reader stylesheet](https://github.com/tt-a1i/archify/blob/25cf37080fc8b1dbe758a4efc3935b55f3327083/archify/explainer/reader.css).

| Observed pattern | Why it helps our catalogue (recommendation) |
|---|---|
| Reader roles distinguish paper, panel, recessed surface, ink, secondary text, muted text, rules and accents. The same roles have light/dark values. | Keep DSG navy, paper and brass, but use separate preview, metadata and control surfaces. Avoid giving every block equal visual weight. |
| The reader uses a consistent control height, radius and text size, restrained shadows, a 16px board gap and a bounded page width. | Normalize search, filters, copy and download controls. Use one spacing rhythm instead of individually tuned card margins. |
| A conclusion panel leads, followed by more detailed panels; IDs and headings create scanning landmarks. | Lead with what the library provides and its limits, then distinguish asset browsing from the selected asset's specification. |
| Panel spans depend on content type. Wide code, comparisons and diagrams get more columns; narrow screens collapse to source order. | Give a selected SVG a large preview and metadata column. Keep the grid for discovery rather than squeezing every detail into each tile. |
| Source references open structured cards containing title, location, optional pinned excerpt/revision and an original-source link. | Put document version, table/row, page and review status together beside the selected shape. Preserve the original OMG link and separate it from our download. |
| The Viewer can dock, collapse or overlay its reader rail to preserve canvas readability. | Keep visual inspection and evidence adjacent on desktop, then stack them on mobile. A simple in-page inspector is sufficient; a drawer is optional. |
| Reduced-motion, print and no-JavaScript reading are explicit. Native controls have focus styling; dialog closure restores focus. | Keep downloads and source links usable without JavaScript. Filters and selection should enhance a complete static catalogue. |

The surface and control observations above come from the [reader CSS](https://github.com/tt-a1i/archify/blob/25cf37080fc8b1dbe758a4efc3935b55f3327083/archify/explainer/reader.css#L1-L94). Content-aware spans are implemented in [layout.mjs](https://github.com/tt-a1i/archify/blob/25cf37080fc8b1dbe758a4efc3935b55f3327083/archify/explainer/layout.mjs). Source cards and keyboard handling are in [reader.js](https://github.com/tt-a1i/archify/blob/25cf37080fc8b1dbe758a4efc3935b55f3327083/archify/explainer/reader.js#L592-L640). The Viewer rail is in [template.html](https://github.com/tt-a1i/archify/blob/25cf37080fc8b1dbe758a4efc3935b55f3327083/archify/assets/template.html#L2600-L2712).

## What we should borrow across the site first

Our shared `site/style.css` already has DSG typography, a bounded reading column and sidebar navigation. The biggest opportunity is to make each page's primary question, current state and evidence easier to scan, while using the same surfaces, controls and spacing across the separate concept browser and gallery templates.

| Page family | Recommended adaptation |
|---|---|
| Homepage | Lead with purpose, current verified scope and three routes: explore concepts, inspect notation coverage, borrow SVGs. Put detailed methodology further down. |
| Concept profiles and browser | Start with purpose and applicability, then notation and relationships. Keep source/review status near the claims it qualifies. Use section navigation and disclosures for raw inheritance/default evidence; bound wide property tables. |
| Research and RDF documentation | Preserve prose measure. Use consistent provenance blocks, quiet uncertainty callouts, and distinct code/query/download surfaces. Avoid turning every paragraph into a card. |
| Notation coverage and register | Show the denominator, counting unit and review state before the table. Group family summaries and support source-row drill-down. Status colors need visible labels: indexed, illustrated and checked are different claims. |
| SVG gallery | Separate compact browse tiles from a large selected preview with applicability, source, limits and download/copy actions. Preserve stable fragments and static access. |

Prioritize shared foundations before page-specific interactions:

1. Define surface, text, rule and status roles using the DSG palette, a short spacing scale and consistent controls. Share them between site CSS, the browser template and gallery.
2. Establish page anatomy: title/lead, scope/status summary, primary content, then deeper evidence. Keep research pages as prose; use panels where they create useful hierarchy or comparison.
3. Reuse evidence/status treatments with original-source links and readable conditions. Source location, review state and semantic limitations remain distinct fields.
4. Improve responsive hierarchy and navigation: section anchors, current-section indication, wrapping controls, bounded tables/code and stacked inspection layouts.
5. Add the selected-shape inspector after these foundations. The gallery's fixed 180px previews constrain detailed inspection; its JavaScript currently only filters and copies files.

Preserve Source Serif headings, Plex body/technical type and DSG identity. Archify's dark-first Viewer, fullscreen canvas, pan/zoom, animation and complex reader rail solve diagram exploration problems; they should not become default chrome for research pages. An optional dark SVG preview can inspect contrast without requiring a whole-site theme system.

These are recommendations inferred from the upstream patterns and our current source. They are not upstream features promised by this catalogue.

## The less visible contribution: quality gates

Archify's `finalize` pipeline runs validation, delivery, strict artifact checks and a real-browser check. Its explainer browser checks inspect horizontal overflow, clipped content, minimum text size, unresolved references, duplicate IDs, keyboard traversal, occluded controls, console errors, no-JavaScript reading and print content. The code explicitly limits what geometry measurements prove: they do not establish visual quality. [Finalize stages](https://github.com/tt-a1i/archify/blob/25cf37080fc8b1dbe758a4efc3935b55f3327083/archify/bin/finalize.mjs#L22), [browser checks](https://github.com/tt-a1i/archify/blob/25cf37080fc8b1dbe758a4efc3935b55f3327083/archify/explainer/browser-check.mjs#L29-L64), [failure criteria](https://github.com/tt-a1i/archify/blob/25cf37080fc8b1dbe758a4efc3935b55f3327083/archify/explainer/browser-check.mjs#L188-L208).

For this project, add browser checks for desktop/mobile overflow, selecting and deep-linking a shape, filtering to zero results, keyboard operation, copy failure fallback, downloadable SVG metadata and static access with JavaScript disabled. Review screenshots after automated checks; passing layout measurements alone is insufficient. Do not adopt Archify's diagram-specific tiny-text failure floors as our page typography target.

## Reuse and licensing

The pinned upstream root license is MIT and names tt-a1i (2026) and Cocoon AI (2025). It requires its copyright and permission notice in copies or substantial portions of the software. Its repository also has third-party notices, so copying bundled fonts or vendor code would require checking those specific notices. Our recommendations reuse design ideas and contain no copied implementation. Our Apache-2.0 license does not replace notices required for any future upstream code we might incorporate. [Upstream license](https://github.com/tt-a1i/archify/blob/25cf37080fc8b1dbe758a4efc3935b55f3327083/LICENSE), [third-party notices](https://github.com/tt-a1i/archify/blob/25cf37080fc8b1dbe758a4efc3935b55f3327083/THIRD_PARTY_NOTICES.md).
