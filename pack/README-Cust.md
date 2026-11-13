# PLUZ5-Cust

Your own PS5 payload store, kept fresh by GitHub. **No payloads are shipped:** you pick the sources, GitHub checks them
daily and writes a list that [pldmgr](https://github.com/itsPLK/ps5-payload-manager) on your PS5 reads.

```
Library (notes) ─► Store (picks) ─► GitHub Actions (daily) ─► manifests/PLUZ-ps5-Source.json ─► pldmgr on the PS5
```

## Fast path (browser only, about 10 minutes)

1. Open **`web/start.html`** from this folder (double-click it). It walks you through every step and builds your links.
2. Or follow [docs/GUIDE-PLUZ5-Cust.md](docs/GUIDE-PLUZ5-Cust.md), the same steps with all the detail.

## The short version

| # | Do this |
|---|---|
| 1 | GitHub → **New repository** (Public). Upload this folder's contents (see the guide, step 2: web or PC). |
| 2 | Repo **Settings → Actions → General → Workflow permissions: Read and write**. **Settings → Pages → `main` / root**. |
| 3 | Make a **fine-grained token** (Contents + Workflows: read/write). The guide shows where. |
| 4 | Open `web/library.html` → add sources → drag to **Store** → download the json files → upload to `configs/` and `data/`. |
| 5 | **Actions → PLUZ5 Update → Run workflow.** |
| 6 | pldmgr → **Settings → Manage Sources → Add Source** → paste `https://raw.githubusercontent.com/<you>/<repo>/main/manifests/PLUZ-ps5-Source.json` |

## What is in the pack

| Path | What |
|---|---|
| `web/start.html` | step-by-step wizard: paste your repo link, get every link and your `.env` |
| `web/library.html` | Library + Store editor (drag and drop, copy blocks, edit) |
| `web/builder.html` | fine-tune Store cards (FW, ports, patterns) |
| `web/pldmgr.html` | your pldmgr link, Copy, Check |
| `examples/example-full.json` | a ready Store of 42+ payloads: load it in the Builder or Library |
| `examples/PS5-SOURCES-library.json` (+ `.md`) | 97 sources with notes: open the json in the Library |
| `docs/` | guide and block format |
| `.env` | your settings (never uploaded). The only file with paths and the token |
| `PLUZ-AllStar.bat` / `pluz-allstar.sh` | one click: build and upload from a PC, Linux or Mac (portable Python + Git) |
| `PLUZ-GHclean.bat` / `pluz-ghclean.sh` | fixes stuck GitHub sign-ins and wrong repo links |

## Credits

Built on the work of the PS5 scene. Thank you to **itsPLK**, **notmaj0r**, **nexgen999**, **ps5-payload-dev**, **earthonion**,
**drakmor**, **Nazky**, **zecoxao**, the etaHEN and kstuff developers, and every author whose payloads these lists point to.

Designed by **Z3nT13**, built together with **Sparkz** (Claude, Anthropic).

*Powered By Z3nT13's PLUZ5*
