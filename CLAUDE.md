# CLAUDE.md

Editing rules for AI sessions working on ZeroWire.

## Ground rules

- No em dashes anywhere: not in code, not in content, not in docs. Use
  commas, colons, or plain hyphens instead.
- Prose is written in first person; this is a personal digest.
- Keep the project 100 percent free to run. Never introduce a dependency,
  API, or service that needs billing or a credit card.

## Site

- The Chirpy theme is only a base. Every layout in `_layouts/` and include in
  `_includes/` is a custom override. Preserve them; do not swap back to theme
  layouts or regenerate them from the theme.
- ALL CSS lives in `assets/css/jekyll-theme-chirpy.scss`. Extend that one
  file. No inline style tags, no extra stylesheets.
- Before changing routing, pagination, or permalinks, verify `/daily-signal/`
  still renders and paginates (`bundle exec jekyll build` and check
  `_site/daily-signal/index.html` plus `_site/daily-signal/page/2/` when
  there are enough posts). The root URL must keep redirecting into it.
- Posts carry the data model in front matter (`severity`, `must_know`,
  `sources`, optional `cve`, `cvss`, `epss`, `kev`, `mitre`,
  `related_detections`). Layouts and includes depend on those exact keys.

## Pipeline

- `_staging/candidates/` is the only place fetch/enrich/triage may write.
  Only `promote_drafts.py` (and `apply_selections.py` through it) writes to
  `_posts/`.
- Keep the LLM out of enrichment math. CVSS, EPSS, KEV, severity, and
  must_know come only from `enrich.py`. Triage (including `--llm` mode) may
  touch summaries, tags, and MITRE mappings, nothing else.
- The LLM path must stay optional and fail-open: if GitHub Models errors or
  the flag is off, rules-based output ships and the run succeeds.
- Enrichment results are cached in `.cache/`; do not remove the caching or
  the NVD backoff, they keep the free-tier rate limits comfortable.

## Workflow

- Local dev: `bundle exec jekyll serve --future`.
- Keep commits small and logical.
