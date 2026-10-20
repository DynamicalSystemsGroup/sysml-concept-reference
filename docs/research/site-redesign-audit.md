# Site redesign audit and acceptance criteria

Baseline: commit `05c167d`. This is a preservation redesign of the DSG technical reference. The original page paths, concept IRIs, section anchors, source data, legal terms, logos and typography remain the baseline.

## Design read

A public technical reference for modelers and renderer authors, using an editorial reading surface and focused reference tools. Native HTML/CSS and the existing file-based Python generators remain the implementation. Design variance 3, motion intensity 1, visual density 5: predictable reading order, no automatic animation, compact metadata with comfortable prose.

The DSG identity uses navy `#11113a`, paper `#ebe6d6`, brass `#d4b478` and darker brass links `#7f601b`; Source Serif 4 headings, IBM Plex Sans body and Plex Mono technical text. The page presentation stays light and paper-based. Shape previews may offer an explicit dark inspection surface. This is an established brand treatment, not a new palette or framework.

## Baseline findings

- The static builder shares a header/sidebar/footer, but the concept browser and gallery embed separate styling and navigation. The published browser receives an extra navigation bar.
- The sidebar exposes every page at once, including on mobile. Long navigation precedes the content on small screens.
- Most content has the same paper surface. Purpose, scope, status, narrative and raw reference material have little visual separation.
- Property and source-register tables are long. Source links retain provenance, but the document version and interpretation status are spread across separate text fragments.
- The gallery provides nine portable components and working filters/copy/downloads. Each tile carries its full description, and there is no large selected-shape inspection area.
- Existing wins include local fonts, relative project-path URLs, safe DOM text, explicit evidence/coverage limits, keyboard focus styles, static documents and downloads, and an offline concept browser.
- The baseline is 24 generated HTML pages. Titles and descriptive metadata exist; no analytics events or structured search metadata are present in the current templates.

## Intended shared components

1. One page frame, semantic surface/spacing/type/control tokens, grouped reference navigation and compact native mobile navigation.
2. A title/lead/scope summary with the relevant counting unit or review status, followed by readable content sections. Prose is bounded; tables and visual workspaces can use more width.
3. Local section navigation with stable anchors and current-section indication. It remains useful without JavaScript.
4. Contextual evidence panels containing the source document, version/file identity, exact location and original link. Raw data remains accessible through disclosures.
5. A concept workspace using the same frame and component vocabulary, with notation and relationships before deep property evidence.
6. A source register grouped into family disclosures, and a gallery with compact discovery tiles plus a selected preview, metadata and copy/download actions.

These adapt the design ideas documented in [Archify research](archify-design-patterns.md). No upstream implementation is copied.

## Completion checks

- Exercise homepage, four concept profiles, concept browser, research/RDF documents, coverage/register and SVG gallery on desktop and mobile.
- Preserve existing routes, source links, section anchors, property modes, concept navigation, downloads, Apache licensing, file bytes and offline browsing.
- Verify narrow-screen overflow, focus/keyboard behavior, section navigation, deep links, empty/error states, copy fallback, static access and print/reduced-motion behavior.
- Keep asset and source-unit counts separate. Never present indexing, representative source checks or SHACL results as language conformance.
- Run relevant unit/RDF/link checks and retained real-browser checks. Inspect rendered captures; automated geometry checks alone do not establish visual quality.
- Record Lighthouse results if the tool can run; do not invent performance or accessibility scores.
- Build deterministically, commit focused changes under DSG context, then verify the deployed artifacts.

## Implemented result and local verification

The shared frame is in `scripts/page_layout.py`, with semantic roles in `site/brand.css`, layout in `site/style.css` and progressive reading aids in `site/site.js`. Both portable tools embed these shared inputs. The browser adds `site/browser.css`; the gallery adds its existing dedicated CSS/JS files. No production dependency or Archify implementation was added.

- Homepage: purpose, actual catalogue scope and three entry routes. Static concept pages: purpose/status, learning points, notation and relationships before the example and deep property evidence.
- Documents: bounded prose, keyboard-scrollable tables, contextual original-source panels and local navigation. Register families retain their section IDs, display their source titles, and report source cells separately from grammar occurrences.
- Browser: shared frame, compact mobile concept selection, preserved concept-IRI fragments and property modes. Section navigation scrolls and focuses without overwriting the selected concept fragment; unavailable profile sections are hidden.
- Gallery: compact discovery tiles and a selected inspector with editable labels, optional dark preview, original-file downloads, preview copy, source identity and attachment coordinates. Original files remain distinct from customized previews. Module/clipboard failures retain usable downloads; no-JavaScript reading retains all nine static cards.
- Native navigation/disclosures remain usable without JavaScript. Print opens evidence/property disclosures and restores their prior state afterward; repeated print events are guarded. Print removes navigation and includes page margins. No automatic motion is introduced.

Local checks on 2026-10-21:

- All 40 Python/Node application tests passed, with the cached originals available. The profile, notation, SVG, browser and site generators ran successfully. SHACL and the saved SPARQL queries passed for catalogue integrity; these results make no language-conformance claim.
- The retained site browser check passed on all 24 shared-frame routes at 1440, 390 and 320px, checking document overflow, title/ID integrity and logos. Its interaction checks covered concept/property empty states and navigation, concept history, local-section focus/fragments, gallery deep links, literal labels, preview copy, a blocked renderer module, keyboard entry, reduced motion and print state. Static reading/navigation was exercised without JavaScript on six page families. The renderer example is covered separately by the retained shape browser check.
- The shape browser check passed for all nine cards, family/search/empty states, copy success/failure, composition, external sprite use, safe labels, theme overrides, clone identities, rejected invalid options and static downloads.
- Desktop/mobile captures were visually reviewed for the homepage, concept browser/profile, research/RDF pages, coverage/register and gallery. A generated profile print PDF was inspected for readable source evidence and property tables. Captures, reports and the PDF stay in ignored `sandbox/`.
- A build of baseline commit `05c167d` was compared with the redesign: no published heading/asset IDs were removed, and the embedded browser inventory JSON is unchanged. Catalogue data, SVG geometry, sprite, renderer and ZIP bytes are unchanged in Git.
- Lighthouse local simulated-mobile results: homepage performance 99/accessibility 100; gallery 98/100; concept browser 58/100. The baseline browser also scored 58 for performance (97 accessibility). The self-contained browser transfers about 1.29 MB uncompressed on the local Python server, versus 1.27 MB before the redesign. Its slow simulated-network loading remains a limitation; scores are individual tool runs, not a performance guarantee or a complete accessibility audit.
- The Playwright CLI rejected direct `file:` navigation. A standalone headless Chromium run instead loaded `docs/concept-browser.html` through the file protocol and confirmed the rendered PartUsage profile, all 113 active property rows and the offline navigation rewrites. Its retained DOM is in `sandbox/redesign-offline-dom.html`. The existing Node DOM smoke check also executes the generated application with `location.protocol = 'file:'`, covering four profiles, modes, filtering and concept navigation. Inventory, application, CSS and reading aids remain embedded, with local font/logo paths.

The retained commands and component locations are documented in [Publishing](../publishing.md). Local verification and a later deployed result are separate states; consult the Pages workflow for publication.
