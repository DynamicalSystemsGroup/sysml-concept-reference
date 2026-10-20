# Publishing with GitHub Pages

The site combines the interactive concept browser, rendered research notes, downloadable RDF/JSON data and saved SPARQL queries. It is generated from this repository; there is no separately maintained wiki or backend.

The intended address is [dynamicalsystemsgroup.github.io/sysml-concept-reference](https://dynamicalsystemsgroup.github.io/sysml-concept-reference/). That address is a deployment target, not evidence that publication has completed. Check the repository's [Pages workflow](https://github.com/DynamicalSystemsGroup/sysml-concept-reference/actions/workflows/pages.yml) for the actual deployment result.

## Build and preview locally

Use the appropriate development context before installing development tools or contacting GitHub. For this workspace:

```bash
source ~/.config/direnv/direnvrc
use_dsg
ctxcheck
git status --short
uv sync --locked
uv run --locked python scripts/build_profiles.py
uv run --locked python scripts/build_notation.py
uv run --locked python scripts/check_inventory.py
uv run --locked python scripts/build_browser.py
uv run --locked python scripts/build_site.py
uv run --locked python -m http.server 8000 --bind 127.0.0.1 --directory _site
```

Open `http://127.0.0.1:8000/`. Stop the preview server with Ctrl-C. `_site/` is generated and ignored by Git. The site builder checks internal links and fragments and uses relative URLs so the same site works beneath the GitHub Pages repository path.

The builder publishes an explicit set of inputs: the homepage, research Markdown, generated browser, selected inventory data, RDF files and queries. It does not publish `sandbox/`, environments, credentials or arbitrary repository files. Links to source scripts open those files in the GitHub repository. Raw OMG downloads remain ignored.

## First publication

After the user explicitly authorizes committing and pushing:

1. Review the diff and stage explicit paths. Commit the inventory and Pages setup, then push `main` through the context-specific SSH remote.
2. In GitHub repository **Settings → Pages**, choose **GitHub Actions** as the build source. An administrator can also create the Pages site through the [GitHub Pages REST API](https://docs.github.com/en/rest/pages/pages#create-a-apiname-pages-site) using `build_type: workflow`.
3. Run **Deploy GitHub Pages** from the Actions tab if the initial push happened before Pages was enabled.
4. Wait for the deployment to finish, then verify the public homepage, browser, documentation and downloadable data at the Pages URL.

The project declares its seven-day package release cutoff in `pyproject.toml`, so the lockfile does not depend on a contributor’s global `uv` configuration.

The workflow runs on pushes to `main`, pull requests to `main`, and manual dispatch. Pull requests build and validate only; deployment is restricted to `main` outside pull requests. The build job has read-only repository access. The deploy job has Pages deployment and identity-token permissions and uses the `github-pages` environment. Action references are pinned to reviewed commit SHAs.

## Updating the site

Edit research notes in `docs/`, the homepage in `site/index.md`, and the documentation style in `site/style.css`. Update the browser template and regenerate it when changing its presentation. For data changes, follow the [RDF reproduction guide](rdf-inventory.md), including pinned-source checks where applicable.

Run:

```bash
uv run --locked python scripts/build_profiles.py
uv run --locked python scripts/build_notation.py
uv run --locked python scripts/check_inventory.py
uv run --locked python scripts/build_browser.py
uv run --locked python -m unittest discover -s tests -v
uv run --locked python scripts/build_site.py
```

Commit and push only when explicitly authorized. A successful deployment publishes the new site automatically. CI uses checked-in RDF and does not fetch OMG originals on each deployment; source-dependent tests report skips when the ignored originals are unavailable. Run the source audit locally with the pinned downloads before publishing source-derived changes.

## Hosting choice

GitHub Pages supports the existing interactive HTML browser and publishes the notes and data from a single Git history. A GitHub wiki would add a second repository and would not serve that browser as a website. This setup follows GitHub's [custom Pages workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

## DSG identity

Shared colors and locally hosted fonts live in `site/brand.css`; layout rules live in `site/style.css`. Official logo assets, original URLs, hashes and font licenses are recorded in `site/assets/provenance.json`. The browser receives the same assets for offline use. Preserve formal notation geometry when applying presentation colors.
