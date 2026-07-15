# ZeroWire

ZeroWire is my personal 0day, CVE, and threat-intel digest. A pipeline pulls
curated RSS feeds every day, enriches anything with a CVE against NVD, EPSS,
and the CISA KEV catalog, triages the results, and opens a pull request where
I check boxes next to what deserves publishing. Merging the PR publishes the
selected items to a static Jekyll site on GitHub Pages.

The whole thing is 100 percent free to run: no paid APIs, no billing, no
credit card. See the Secrets section below.

## Content model

Everything lives in `_posts/YYYY-MM-DD-slug.md`.

1. **Daily Signal**: short feed items. Front matter: `title`, `date`,
   `categories: [Daily Signal]`, `tags`, `severity`
   (`info|low|medium|high|critical`), `must_know` (bool), `sources` (list of
   `{name, url}`), and optional `cve`, `cvss`, `epss`, `kev`.
2. **Must-Know**: not a separate folder. Daily Signal items with
   `must_know: true` surface automatically in the filtered view. The pipeline
   sets the flag when an item is in KEV or has EPSS at or above 0.5.
3. **Threat Research**: longer analysis with `categories: [Threat Research]`.
   Adds a `mitre` list of ATT&CK technique IDs (like `T1190`) and an optional
   `related_detections` list of `{name, url}`.

## Routes

| Route | What it is |
| --- | --- |
| `/` | redirects into the feed |
| `/daily-signal/` | main paginated feed with date dividers |
| `/daily-signal/page/:num/` | older pages (jekyll-paginate-v2) |
| `/must-know/` | filtered high-priority feed |
| `/threat-research/` | analysis list |
| `/tags/<tag>/` | tag archives |

## Local development

Ruby 3.3 and Bundler required.

```sh
bundle install
bundle exec jekyll serve --future
```

Then open `http://127.0.0.1:4000/zerowire/`. The `baseurl` is `/zerowire`
because this deploys as a GitHub Pages project site; clear it in
`_config.yml` if the repo ever becomes a user site.

Search is powered by [Pagefind](https://pagefind.app/), which indexes the
built site at deploy time. During local serve the search box renders as a
placeholder; to test it locally:

```sh
bundle exec jekyll build
npx pagefind --site _site
```

## Pipeline

All stages live in `scripts/` and run on Python 3.11
(`pip install -r scripts/requirements.txt`).

1. `fetch_feeds.py` reads `rss-sources.md`, pulls every feed, canonicalizes
   URLs, collapses duplicate stories with a fuzzy title match (rapidfuzz),
   and stages candidates in `_staging/candidates/`. It never writes to
   `_posts/`.
2. `enrich.py` finds CVE IDs, queries NVD API 2.0 for CVSS, FIRST EPSS for
   exploit probability, and the CISA KEV catalog for known-exploited status,
   with results cached in `.cache/enrichment.json`. It computes `severity`
   and `must_know`: KEV or EPSS >= 0.5 or CVSS >= 9.0 is critical, CVSS >= 7.0
   is high, CVSS >= 4.0 is medium, else low. With `GITHUB_TOKEN` present it
   also cross-checks the GitHub Advisory database.
3. `triage.py` is rules-based by default and needs no key: it trims summaries
   to 2 to 3 sentences, keyword-matches 3 to 5 tags from the controlled
   vocabulary in `vocab.py`, and maps tags to ATT&CK techniques for research
   items. With `--llm` it refines summaries and tags through GitHub Models
   (free tier, authenticated with the same `GITHUB_TOKEN`), falling back to
   rules output on any failure. Triage never touches CVSS, EPSS, KEV,
   severity, or must_know.
4. `promote_drafts.py` and `apply_selections.py` publish. Publishing is
   hybrid: must-know candidates (KEV-listed or EPSS >= 0.5) auto-publish
   during the digest run, so the site refreshes daily without my
   involvement. Everything else lands in a PR whose body is a checkbox
   list; I tick what I want, merge, and the publish workflow promotes
   checked candidates into `_posts/` and discards the rest.

## Automation

| Workflow | Trigger | What it does |
| --- | --- | --- |
| `rss-digest.yml` | daily cron, manual dispatch | fetch, enrich, triage, open the digest PR |
| `publish-drafts.yml` | digest PR merged | promote checked drafts into `_posts/` |
| `pages-deploy.yml` | push to main | Jekyll build, Pagefind index, deploy to Pages |

## Secrets

No paid secrets are required. Ever.

- `NVD_API_KEY` (optional, free): raises the NVD rate limit from 5 to 50
  requests per 30 seconds. Request one at
  <https://nvd.nist.gov/developers/request-an-api-key>. Without it the
  enricher just paces itself slower.
- `GITHUB_TOKEN`: auto-provided by GitHub Actions. It covers GitHub Advisory
  lookups and the optional GitHub Models triage. Nothing to create or rotate.

## License

MIT, see [LICENSE](LICENSE).
