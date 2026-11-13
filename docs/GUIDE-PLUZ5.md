# PLUZ5: step by step (owner guide)

## A. Use the store on the PS5

1. pldmgr → **Settings (gear) → Manage Sources → Add Source**.
2. Paste `https://raw.githubusercontent.com/Z3nt13/PLUZ5/main/manifests/PLUZ-ps5-Source.json` → **Add**.
3. Not showing? Open the link in a browser. JSON = fine, re-add it. 404 = the workflow has not run yet (section B step 9).

## B. Fresh start of the repo (do this once)

You have the full zip. Nothing from the old repo is needed.

| # | Do this |
|---|---|
| 1 | **Backup:** on the old repo, **Code → Download ZIP**. Keep it somewhere safe. |
| 2 | **Delete the old repo:** repo → **Settings → General → Danger Zone → Delete this repository**. |
| 3 | **Create the new one:** github.com → **New repository** → name `PLUZ5`, **Public**, no README, no .gitignore → Create. |
| 4 | **Token** (fine-grained, this repo only): Settings (your photo) → Developer settings → Fine-grained tokens → New. Permissions: **Contents: Read and write** and **Workflows: Read and write**. Copy it. |
| 5 | **Unzip** `PLUZ5-v8.0-FULL.zip` to a folder (portable drive is fine). |
| 6 | **Edit `.env`**: `GH_USER=Z3nt13`, `GH_REPO=PLUZ5`, `GH_TOKEN=` your token. Windows: set the portable tool folders (`PLUZ_PY_DIR`, `PLUZ_GIT_DIR`, `PLUZ_7ZIP_DIR`). Linux/Mac: leave `PLUZ_*` blank. |
| 7 | **Run** `PLUZ-AllStar.bat` (Linux/Mac: `./pluz-allstar.sh`). It links the folder to the repo, builds, validates and pushes. |
| 8 | **Repo settings:** Settings → Actions → General → Workflow permissions → **Read and write** → Save. Settings → Pages → Deploy from a branch → `main` / `(root)` → Save. |
| 9 | **First run:** Actions → **PLUZ5 Update** → **Run workflow**. Wait for the green tick (1-3 min). |
| 10 | **Check:** open the link in section A. JSON with `"name": "Z3nT13's PLUZ5"` = done. |

Why not the web uploader: it drops hidden files (`.github`) and big batches. AllStar pushes everything.

## C. Keep it updated

| Task | Steps |
|---|---|
| Daily updates | Automatic (03:17 UTC). If GitHub pauses them after 60 idle days, press **Run workflow** once. |
| Add a source | Open `web/library.html` on your Pages site (or the unzipped folder) → paste the repo link → drag it to **Store** → download both json files → put them in `configs/` and `data/` (web upload or AllStar) → run the workflow. |
| Add your own `.elf` / `.bin` | Name it `Name_v1.0.elf` → drop it into `payloads/` → run the workflow. A file in `payloads/` beats the upstream copy. |
| Change a field (FW, category, port) | Library or Builder → edit the card → download → upload → run. |
| Look at the notes | `data/PLUZ5-infos.xlsx` (filter by category, type, hardware) or `.md`. |
| Something skipped | Actions → latest run → find `[SKIP]` lines. Fix list is in the README of the Cust pack (Troubleshooting). |

## D. Publish the Cust pack

`pack.yml` builds **PLUZ5-Cust-<version>-FULL.zip** from this repo and attaches it to a Release.

1. Releases → **Draft a new release** → tag `v8.0` → **Publish**. The zip appears on the release in about a minute.
2. Optional template mirror (so people can click **Use this template**): create an empty public repo `PLUZ5-Cust`, tick **Template repository** in its settings, add a repo secret `PACK_TOKEN` (token with Contents + Workflows write on `PLUZ5-Cust`) in **PLUZ5 → Settings → Secrets → Actions**. Each release then pushes the pack there.

## E. Check yourself

| Test | Expected |
|---|---|
| Section A link in a browser | JSON, store name, many payloads |
| Actions tab | green |
| `data/PLUZ5-infos.xlsx` | 97 rows, filter on top |
| `web/pldmgr.html` → Check | "OK: ... with N payloads" |

## F. Clean up GitHub sign-in and old repos (scripts included)

| Problem | Run | What it does |
|---|---|---|
| Git keeps asking for a password, or uses the wrong account | `PLUZ-GHclean.bat` (Linux/Mac: `./pluz-ghclean.sh`) | removes stored GitHub credentials and stale git settings for this folder, then you run AllStar again |
| Push refused / "not a git repository" / wrong remote | same script, then AllStar | AllStar re-links the folder to `GH_USER/GH_REPO` from `.env` |
| Need a log to ask for help | `PLUZ-AllStar.bat debug` | writes `logs/allstar_debug_<time>.log` (token hidden) |

Both scripts read the portable tool folders from `.env`, so nothing has to be installed.

## G. Two ways to update (pick any)

| Way | When | How |
|---|---|---|
| **Web GUI** | quick edits from any device | Library/Builder page → edit → download json → upload to `configs/` / `data/` in the repo → Run workflow |
| **PC / Linux / Mac, portable apps** | many changes, own payload files | edit files in the folder → run `PLUZ-AllStar.bat` / `./pluz-allstar.sh` (needs only portable Python + Git from `.env`) |
