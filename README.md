# PLUZ5

A PS5 payload store that keeps itself fresh. GitHub checks the sources every day and writes a list that
[pldmgr](https://github.com/itsPLK/ps5-payload-manager) on your PS5 reads.

## Add it to pldmgr (30 seconds)

```
https://raw.githubusercontent.com/Z3nt13/PLUZ5/main/manifests/PLUZ-ps5-Source.json
```

1. Open **pldmgr** on the PS5 → **Settings (gear) → Manage Sources → Add Source**.
2. Paste the link above → **Add**.
3. Your store appears: pick a payload → download → send.

Other links (same place, `manifests/`): **Hosted** (files served from this repo) `PLUZ-ps5-Hosted.json`, and one list per category in `split/`.
Check a link: open it in a browser, you should see JSON. Page with a Copy and Check button: `web/pldmgr.html`.

## What is in here

| Folder | What |
|---|---|
| `manifests/` | generated lists pldmgr reads |
| `payloads/` | hosted copies of the payloads |
| `configs/payload_registry.json` | the **Store**: what gets published |
| `data/PLUZ5-infos.json` (+ `.md`, `.xlsx`) | the **Library**: every source known, with notes |
| `web/` | Start, Library, Builder, Catalog, pldmgr pages |
| `docs/` | step-by-step guides and the block format |
| `core/`, `.github/` | engine and daily workflow |

## Make your own store

Download **PLUZ5-Cust** from the [Releases](../../releases) page. It is this project without the payloads, with a step-by-step guide.

## Guides

- [docs/GUIDE-PLUZ5.md](docs/GUIDE-PLUZ5.md): use it, run it, update it (owner steps)
- [docs/BLOCK-FORMAT.md](docs/BLOCK-FORMAT.md): how a Library block is written

## Credits

Built on the work of the PS5 scene. Thank you to **itsPLK** (pldmgr, webkit autoloader), **notmaj0r**, **nexgen999**,
**ps5-payload-dev**, **earthonion**, **drakmor**, **Nazky**, **zecoxao**, the etaHEN and kstuff developers, and every author
the lists point to. Payload files belong to their authors; hosted copies keep their original names and source links.

Designed by **Z3nT13**, built together with **Sparkz** (Claude, Anthropic).

*Powered By Z3nT13's PLUZ5*
