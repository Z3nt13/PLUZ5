# data/

This directory is a placeholder for the fuller SOURCE → PROJECT → ARTIFACT
database described in the PLUZ-PS5 v2 master plan (Phases 7-9): a proper
source registry with per-field discovery timestamps, and a human-override
layer that survives re-scrapes even when upstream metadata changes back.

**Not built yet, on purpose.** Per the plan's own commandment #18
("plan first, code second... build one small component at a time"),
this round only shipped:

- The directory reorg (`core/`, `configs/`, `data/`, `web/`)
- `web/add-source.html` — a standalone review/entry tool (see that file)
- PKG support (`configs/pkg_registry.json`, `core/plz_pkg.py`)

What's still missing before this becomes the real Phase 7-9 system:
- `sources.json` here (not the documentation-only one in `configs/`) with
  per-source discovery state: last checked, enabled, discovery settings
- `overrides.json` — a place for human corrections keyed by field, so a
  future re-scrape can propose new data without silently clobbering a
  correction you already made
- The actual sync engine that reads a source, proposes data, and merges
  it against `overrides.json` with human corrections always winning

`web/add-source.html` currently writes directly into `configs/payload_registry.json`
or `configs/pkg_registry.json` (via the File System Access API, or a
downloadable JSON snippet as a fallback) — which is fine for now, but
once the override-survives-rescrape system exists, that's where corrections
should live instead so re-running discovery doesn't require re-doing them.
