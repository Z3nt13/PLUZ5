# PLUZ5-Cust: step by step

Goal: your own payload store that pldmgr can read, updated by GitHub every day.
You need: a free GitHub account, a browser. A PC is optional (it makes uploads one click).

## 1. Create your repository

1. Go to github.com → sign in → **+ → New repository**.
2. Name: anything (example `PLUZ5-Cust-mine`). **Public**. Leave "Add a README" off. **Create**.
   (If the project offers **Use this template**, use that instead and skip step 2.)

## 2. Put the pack into it

**Option A: browser.**
1. Unzip `PLUZ5-Cust-v8.0-FULL.zip`.
2. In your new repo click **uploading an existing file**, drag in the folders `configs`, `core`, `data`, `docs`, `examples`, `web`, `payloads`, `manifests` and the root files (`pluz.py`, `.gitignore`, `.gitattributes`, `README.md`).
3. The hidden **`.github`** folder is dropped by the web uploader. Create it by hand: **Add file → Create new file**, name it `.github/workflows/update.yml`, paste the content of that file from the pack, **Commit**.
4. Do **not** upload `.env`.

**Option B: PC (recommended, no manual hidden-file step).** See section 8.

## 3. Switch on the two settings (once)

1. **Settings → Actions → General → Workflow permissions → Read and write → Save.**
2. **Settings → Pages → Source: Deploy from a branch → Branch `main`, folder `/ (root)` → Save.** Wait 1-3 minutes for "Your site is live".

## 4. Make a GitHub token (strongly recommended)

A token lets the PC scripts push without passwords, and lets the web pages save to your repo.

1. GitHub → your photo → **Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token**.
2. Name `PLUZ5`, expiration 90 days, **Only select repositories** → your repo.
3. Repository permissions: **Contents: Read and write**, **Workflows: Read and write**. Generate.
4. Copy it immediately (shown once). Store it only in `.env` (`GH_TOKEN=`). Never share or upload it.

## 5. Open the start page

Open `web/start.html` from the unzipped folder (or from your Pages site `https://<you>.github.io/<repo>/web/start.html`).
Paste your repo link. It fills your user, repo, branch, builds every link, and shows your `.env` text.

## 6. Choose your payloads

How the pages work:

| Page | Use it for |
|---|---|
| **Library** (`web/library.html`) | your list of every source, with notes. Add a repo link, edit a block, drag blocks to the Store |
| **Store** (right side of the Library) | only what pldmgr will download |
| **Builder** (`web/builder.html`) | fine-tune Store cards: category, firmware, ports, file patterns, personal files |

Steps:
1. Open the Library → **Open Library json…** → pick `examples/PS5-SOURCES-library.json` (97 sources), or start empty and paste your own repo links under **Add to Library**. (PC users can also import a markdown list: `python pluz.py infos --import file.md`.)
2. Tick the sources you want → **drag to Store** (or the **→ Store** button).
3. Optional: open the Builder, set your **store name** (shown in pldmgr), tidy cards. **Load example list** gives a ready 42+ start.
4. **Download** `payload_registry.json` (Store) and `PLUZ5-infos.json` (Library).

Block format (how a source is written): `docs/BLOCK-FORMAT.md`. Minimum: URL + `#Unknown`.

## 7. Publish

1. Repo → `configs/` → **Add file → Upload files** → `payload_registry.json` → **Commit**.
2. Repo → `data/` → upload `PLUZ5-infos.json` → **Commit**.
3. **Actions → PLUZ5 Update → Run workflow**. Green tick in about a minute. It then runs every day and on every change.
4. Open `https://raw.githubusercontent.com/<you>/<repo>/main/manifests/PLUZ-ps5-Source.json`. JSON = ready.

## 8. From a PC (portable apps preferred)

Handy for uploading everything in one go and for adding many files.

**Windows (portable, nothing installed):**
1. Get portable **WinPython** (python.org-free), **PortableGit**, **7-Zip portable**. Put them in one folder, e.g. `D:\portaz\`.
2. Open `.env`: set `PLUZ_PY_DIR`, `PLUZ_GIT_DIR`, `PLUZ_7ZIP_DIR` to those folders. Set `GH_USER`, `GH_REPO`, `GH_TOKEN`.
3. Double-click **`PLUZ-AllStar.bat`**. It links the folder to your repo, fetches, builds, checks and pushes.

**Linux / Arch / Mac:**
1. Have `python3` and `git` (system, or a portable build; set `PLUZ_PYTHON` / `PLUZ_GIT` in `.env` to use specific ones).
2. Fill `GH_USER`, `GH_REPO`, `GH_TOKEN` in `.env`.
3. `chmod +x pluz-allstar.sh && ./pluz-allstar.sh`

**Updating later (same script):** edit `configs/payload_registry.json`, `data/PLUZ5-infos.json` or drop files into `payloads/`, then run AllStar again. It pushes only what changed.

**Cleaning up GitHub (scripts included):**

| Problem | Run |
|---|---|
| Git asks for a password again and again, or uses the wrong account | `PLUZ-GHclean.bat` (Linux/Mac: `./pluz-ghclean.sh`), then AllStar again |
| `Repository not found` / wrong remote | fix `GH_USER` / `GH_REPO` in `.env`, run AllStar (it re-links the folder) |
| Need a log | `PLUZ-AllStar.bat debug` → `logs/allstar_debug_<time>.log` (token hidden) |

## 9. Add it in pldmgr on the PS5

1. **pldmgr → Settings (gear) → Manage Sources → Add Source.**
2. Paste your link (`web/pldmgr.html` makes it for you, with a Check button) → **Add**.
3. Your store name appears with the payloads. Pick, download, send.

## 10. Keep it going

| Task | Steps |
|---|---|
| Add a source | Library → paste repo link → drag to Store → download → upload to `configs/` and `data/` → run the workflow |
| Add your own `.elf` / `.bin` | name it `Name_v1.0.elf` → put in `payloads/` → run the workflow. Yours beats an upstream copy of the same name |
| Host the files yourself | `configs/settings.json` → `"mode": "hosted"` (or `PLUZ_MODE=hosted` in `.env`). Only share files you may redistribute |
| Remove a source | Library → select → **Mark removed** (restorable), or remove from Store |
| Stopped updating | GitHub pauses idle repos after 60 days: press **Run workflow** once |

## Troubleshooting

| You see | Do this |
|---|---|
| Workflow red, push `403` | Step 3.1, re-run |
| Workflow does not exist | `.github/workflows/update.yml` missing: step 2.3 |
| Page 404 | Pages not live: branch `main`, root, repo Public. Or open the page from the unzipped folder |
| `[SKIP] N candidate assets` | Set **Asset pattern** on the card (Builder) |
| `[SKIP] no 'beta' release` | Set **Tag pattern** or Channel |
| `[SKIP] only a .zip asset` | Pick another asset, use hosted mode, or unzip and add it as your own file |
| `could not read releases (403)` | GitHub rate limit; run again later |
| Manifest has 0 entries | Store is still empty: upload `payload_registry.json` |
| AllStar: `Repository not found` | Fix `GH_USER` / `GH_REPO` in `.env` |
| pldmgr shows nothing | Open the link in a browser first: 404 = wrong name/branch; repo must be Public |
