# PLUZ5 (formerly PLUZ-ps5 / PayLoadUpdaterZ-PS5)

A personal, pldmgr-compatible payload, PKG and ffpfsc-tool mirror and manifest
generator for PS5 homebrew (PS4 payloads can be included too). Free for anyone
to use. Cross-platform (Windows + Arch Linux), dependency-free (Python stdlib
only: no pip installs, no 7-Zip binary, no third-party packages of any kind).

## Security note (read this first)

Every script in `core/` is plain, readable Python standard library code. There is:
- no `eval`/`exec` of remote or dynamic content
- no network call from any `core/` script
- no obfuscation, no base64-encoded payloads, no bundled binaries
- nothing that shells out to `curl`/`wget`/`iwr` or similar

The only places this repo touches the network:
- `web/add-source.html` -- only when you click "Fetch from GitHub" / "Scrape All", never on load
- `web/catalog.html` -- on load it fetches this repo's own manifest JSON files (nothing else)

Verify yourself in about two minutes:
`grep -rn "eval(\|exec(\|urllib\|requests\|socket\|subprocess" core/`
The only `subprocess` usage is local `git` commands in `pluz_update.py`
(add/commit/push) -- `pluz_check.py` only looks for `git` on PATH.

## Layout

```
PLUZ5/
├── PLUZ.pyz                  # portable single-file executor (see below)
├── PLUZ-AllStar.bat / pluz-allstar.sh   # one-shot pipeline (see below)
├── pluz-*.sh / pluz-*.bat    # thin per-command launchers
├── README.md / GamePlan.md
├── .env.example               # copy to .env (gitignored) and fill in
├── .github/workflows/         # update.yml (regenerate manifests), validate.yml
├── core/                      # the actual engine -- everything lives here
│   ├── __main__.py            # dispatcher (used by PLUZ.pyz)
│   ├── pluz_common.py         # shared helpers -- no network calls, ever
│   ├── pluz_check.py          # health check (read-only)
│   ├── pluz_merge.py          # import payloads/pkgs from any directory
│   ├── pluz_update.py         # ELF/BIN manifests (Source, Hosted, category splits)
│   ├── pluz_pkg.py            # PKG manifest
│   ├── pluz_ffpfsc.py         # ffpfsc-tool manifest
│   ├── pluz_validate.py       # schema + filename + dupe checks
│   ├── pluz_dedupe.py         # SHA-256 collision report
│   ├── pluz_cleanup.py        # backup + wipe for a clean rebuild
│   ├── pluz_migrate.py        # one-time old-repo retirement
│   └── pluz_backup.py         # on-demand backup
├── configs/
│   ├── settings.json          # paths, manifest names, retention, hw_targets
│   ├── categories.json
│   ├── sources.json           # documentation-only reference list
│   ├── payload_registry.json  # ELF/BIN identity -> metadata
│   ├── pkg_registry.json      # PKG identity -> metadata
│   └── ffpfsc_registry.json   # ffpfsc-ecosystem tool identity -> metadata
├── data/                      # placeholder for the future source/override database
├── web/
│   ├── catalog.html           # read-only browser: tabs, search, filters, themes
│   └── add-source.html        # registry editor (add / edit / delete), human review
├── payloads/  pkgs/  ffpfsc/  # flat artifact storage (.elf/.bin, .pkg, ffpfsc tools)
├── manifests/                 # generated -- see "The 4 manifests"
│   └── split/                 # category-split ELF/BIN manifests
├── docs/rename-map.md
└── logs/
```

## GitHub-first (the default way to work)

Everything runs on GitHub; your PC, Arch, Debian or Mac is only needed for a first upload or an emergency.

1. **Edit in the web UI.** Change `configs/*.json` (registries, settings) with GitHub's editor, or use `web/add-source.html`. Commit.
2. **The `PLUZ5 Update` workflow does the rest.** Daily at 03:17 UTC, on every push to `configs/ payloads/ pkgs/ ffpfsc/`, and on demand (Actions tab, Run workflow). It runs `fetch` (downloads new upstream releases into `payloads/` and `pkgs/`), then `update`, `pkg`, `ffpfsc`, then `validate`, and commits the result. A failing validate stops the job before anything is committed.
3. **`fetch` never guesses.** It only downloads when a release channel matches and exactly one asset fits. Everything else is listed as `[SKIP]` in the Actions log. Fix a skipped entry by adding `asset_pattern` (asset name, e.g. `*.elf`) or `tag_pattern` (release tag) to its registry variant. Set `"fetch": false` to exclude a variant. It is add-only: it never deletes or overwrites a file.
4. **No secrets needed.** The workflow uses GitHub's built-in token.

### Local (optional)

Copy `.env.example` to `.env` and edit only that file: `PLUZ_PY_DIR`, `PLUZ_GIT_DIR` (portable tool folders on Windows) or `PLUZ_PYTHON`, `PLUZ_GIT` (exact paths), plus `GH_USER`, `GH_REPO`, `GH_BRANCH`. Every launcher (`pluz-*.bat`, `pluz-*.sh`) reads those through `pluz-env.bat` / `pluz-env.sh`, so no path lives in the source. Blank values fall back to `python` / `git` on PATH. `PLUZ-AllStar.bat` / `pluz-allstar.sh` run the whole pipeline (check, fetch, update, pkg, ffpfsc, validate, git push) in one go. `pluz-fetch` is a dry run unless you pass `--apply`.

## Two ways to run this

**1. `PLUZ.pyz`** -- portable single file (built with Python's stdlib `zipapp`,
not a third-party packer). Inspect it yourself: `unzip -l PLUZ.pyz` shows plain
`.py` files. Run it from inside the repo folder:
```
python3 PLUZ.pyz check
python3 PLUZ.pyz merge --source /path/to/payloads --apply
python3 PLUZ.pyz update --push
python3 PLUZ.pyz pkg
python3 PLUZ.pyz ffpfsc
python3 PLUZ.pyz validate
python3 PLUZ.pyz dedupe
python3 PLUZ.pyz backup
python3 PLUZ.pyz cleanup --apply
python3 PLUZ.pyz migrate --old /path/to/old/repo --apply
```
Rebuild it anytime: `python3 -m zipapp core -o PLUZ.pyz -p "/usr/bin/env python3"`

**2. Individual `pluz-*.sh` / `pluz-*.bat` launchers** -- same commands, one file
per command. Both call the same `core/pluz_*.py` code; `core/` is the source of truth.

**One-shot:** `PLUZ-AllStar.bat` (Windows) / `pluz-allstar.sh` (Arch/Linux) run
check -> update -> pkg -> ffpfsc -> validate -> git add/commit/push, stopping at the
first failing step. `.github/workflows/update.yml` regenerates all manifests on
GitHub when `payloads/`, `pkgs/`, `ffpfsc/` or `configs/` change.

## Design principles (do not violate these)

1. **Unknown is better than wrong.** Unparseable filenames, unclear categories,
   ambiguous zip contents, firmware ranges, hardware targets -- all left unset or
   flagged for manual review, never guessed. Human review is the final authority.
2. **Never delete on ambiguity.** Retention only removes a file when PLUZ is certain
   it is superseded. `protected_fallback: true` entries are never auto-deleted.
3. **Non-destructive by default.** Every script defaults to dry-run; `--apply` (or
   `--push` for update) is required to actually change anything.
4. **Secrets and local paths never touch git.** `.env` only, gitignored.
5. **Backups before anything destructive.** `cleanup` and `migrate` always zip a backup first.
6. **Never assume `.bin` and `.elf` are duplicates.** Investigate (or run `dedupe`) first.

## The "stable + fast" variant pattern

Some tools ship two tracks you want to keep at once. Model both as **variants of
the same payload name**, with the stable one `protected_fallback: true` and the
fast one on normal retention:

```json
"ShadowMountPlus": {
  "variants": {
    "Beta":  { "channel": "beta",  "protected_fallback": true  },
    "Alpha": { "channel": "alpha", "protected_fallback": false }
  }
}
```
Filenames: `ShadowMountPlus-Beta_v1.6beta16.elf`, `ShadowMountPlus-Alpha_v1.7alpha9.elf`.
Same pattern for `etaHEN-EchoStretch` (fast) vs `etaHEN-Zecoxao` (protected).

## The 4 manifests

| File | Contents |
|---|---|
| `PLUZ-ps5-Source.json` | Latest/current ELF+BIN, one entry per (payload, variant). **This is what pldmgr consumes.** |
| `PLUZ-ps5-Hosted.json` | ELF+BIN fallbacks, up to 3 retained builds (`retention` tag: current / previous / previous-2). `protected_fallback` entries always included. |
| `PLUZ5-PKG.json` | All PKG entries in one file, each tagged with `retention`. PKGs use a different consumption model than pldmgr's autoloader. |
| `PLUZ5-ffpfsc.json` | ffpfsc-ecosystem tools: `compressor_tool`, `helper_elf`, `compressed_file` (metadata only -- PLUZ5 never hosts full game images). |

`manifests/split/*.json` are per-category copies of the Source manifest. All
manifests are deterministic (no per-run timestamps), so re-running changes nothing
unless an input changed. Source and Hosted keep their original `PLUZ-ps5-` file
names; PKG and ffpfsc use the `PLUZ5-` prefix.

## Filename convention

```
{payload}[-{variant}]_v{version}[_Expi{YYYYMMDD}].{ext}
```
`ext` is `elf`, `bin`, `pkg`, `ffpfsc`, `ffpkg` or `fpkg`. Firmware compatibility and
hardware target are **registry metadata, never part of the filename**. Official Sony
content-id PKG filenames do not match this and need manual handling -- see
`docs/rename-map.md`.

## Registry fields

All three registries share: `display_name`, `source_repo` (the project's primary
URL), `author`, `author_url`, `backup_url` (optional mirror -- if you hold files from
both sources, run `dedupe`; matching SHA-256 means the same artifact),
`category`, `protected_fallback`, `note`, and the optional fields below.

- `payload_registry.json` (ELF/BIN) adds `channel`, `port`.
- `pkg_registry.json` (PKG) adds `pkg_type`, `title_id`, `content_id`, `required_system_version`.
- `ffpfsc_registry.json` adds `ffpfsc_type` (`compressor_tool` | `helper_elf` | `compressed_file`).

Optional on any entry (absent or `null` means "not stated", never guessed):

| Field | Values |
|---|---|
| `platform` | `ps5` (default) \| `ps4` \| `ps4/ps5` |
| `fw_min` / `fw_max` | firmware strings, **hand-typed**, never auto-parsed (e.g. `"3.00"`, `"13.60"`) |
| `hw_target` | `P5` = regular/slim PS5 only \| `P5P` = optimized for PS5 Pro \| `P5U` = universal, optimized for both |

Categories (capped at 10 on purpose): Kernel, Network, File Management, Game
Tools, Media, System Utility, Debug & SDK, Linux, Activation & Spoof, Unknown.
A longer list does not scale without an automated review workflow.

## `web/catalog.html` -- read-only catalog

Static page (works on GitHub Pages or any static host). Tabs for payloads, PKGs
and ffpfsc tools; tile and list views; search; filters for platform, hardware
target (P5 / P5P / P5U) and category; per-entry detail with firmware range and
checksum; selectable themes. It only reads the manifest JSON files above.

## `web/add-source.html` -- registry editor

Offline-first: every field is editable by hand. Load a real `payload_registry.json`
or `pkg_registry.json` through the browser's File System Access API, browse and
filter entries, edit or delete one in place, then Save. Fields the form has no
input for (for example `platform`) are preserved when you edit. GitHub discovery
is on-demand only: a single "Fetch from GitHub", or a multi-link batch scrape that
shows one result card per repo with a "Load into form" button, so you review each
before anything is saved. Firefox lacks the File System Access API; use
Copy/Download there. The editor does not cover `ffpfsc_registry.json` yet.

## First-time order of operations

1. `pluz-check`
2. `pluz-merge --source /path/to/your/payloads` (dry-run), review the log
3. Check `docs/rename-map.md` for anything flagged, rename on disk if wanted
4. `pluz-merge --source /path/to/your/payloads --apply`
5. Fill registry gaps flagged in the registries (new entries default to `Unknown`)
6. `pluz-validate`
7. `pluz-update`, `pluz-pkg` and `pluz-ffpfsc`, review the manifests, then
   `pluz-update --push` (or `PLUZ-AllStar`) when ready

## What's deferred (on purpose)

The full SOURCE -> PROJECT -> ARTIFACT database with rescrape-proof human overrides
isn't built (see `data/README.md`). Also open: RSS/Atom export, per-type AIO zip
bundles. See `GamePlan.md` section 3.
