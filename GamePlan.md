# GamePlan.md — Geoz's PS4/PS5 Project Suite

Last updated: 2026-10-13. The single reference document tying together every
project, how they relate, current status, and every external source that
informed them, with full URLs so nothing has to be re-found from memory.
Rule: the game plan comes first, code second.

---

## 1. The universal principles (apply to every project)

1. **Modular by default.** Every feature/option is electively, individually
   downloadable by the user. The only exception is a feature that genuinely
   requires another addon — then the user is told plainly and offered both.
2. **Plugins/addons live in their own project's repo**, never a central addon repo.
3. **Dual-OS, always** (Windows 11, Arch Linux, plus Debian/macOS where a
   project's scope says so). Self-contained and portable: no installs required.
4. **Unknown is better than wrong.** Never guess a source, category, identity,
   firmware range or hardware target — leave it unset and flag it.
5. **Non-destructive by default.** Dry-run unless told to apply; backups first.
6. **Reliability.** Every script is actually run against real-shaped data
   (and edge cases) before being called done.
7. **Hardware-target marking (decided 2026-10-13).** `P5` = optimized only for
   regular/slim PS5; `P5P` = optimized for PS5 Pro; `P5U` = universal (both).
   Used in our projects together with firmware version so everyone can see
   what is optimized for what. In PLUZ5 it is the optional `hw_target` field.
8. **Local paths and secrets live in `.env`, never in committed docs or code.**

---

## 2. Project structure (supersedes the old priority list)

Four projects, each rebuilt fresh on GitHub (old repos erased), private until a
working beta/RC. **Build order: PLUZ5 and ZendRz first, then the other two.**

| # | Project | What it is |
|---|---|---|
| 1 | **PLUZ5** (was PLUZ-ps5) | Personal source-of-truth payload/PKG/ffpfsc registry + mirror + manifest generator; pldmgr auto-update source; backs up the actual files |
| 2 | **ZendRz** (was PSZend + Zendit) | Standalone cross-platform payload sender + PKG/FTP/WebDAV installer; install-tracking log |
| 3 | **ZperoMGR5** (was ZperoMGR+) | Console-side suite: Zpero-Webkit, ProsperoMgr fork, ShrctZ, pldmgr loader, Slopkit; per-addon on/off |
| 4 | **KmprZu** (was KmprZ-Uni) | PC-side compression + game-library engine folding in KmprZ-ps5, KompreZ, GameLibZ, PS5-System-Toolkit |

`PLUZ-ps5-Custom` was **cancelled** (2026-09-23); ideas from nexgen999/evoX-CoreOS are pulled into PLUZ5 instead.

### Landscape changes that affect the plan (Sep–Oct 2026)
- **Relapse** (FW 7.00–13.60, PS5 Pro included) is a public, MIT-licensed chain.
  Open decision for ZperoMGR5: keep its own Zpero-Webkit, or wrap/launch Relapse
  and spend the effort on the console-side suite.
- **FW 14.00 closes it**, so every firmware ceiling in our metadata is 13.60 for now.
- **Three on-console AMPR LZ4 compressors now exist** (see sources). Open
  decision for KmprZu: launch and manage these, or ship its own converter.
  Leaning: orchestrate (library intelligence, vault, shared TOML profiles, install tracking).
- Pro-only gains exist (memory unlock) — first candidate **P5P** feature.

---

## 3. PLUZ5 — status

Pure Python stdlib, zero dependencies, identical on Windows 11 and Arch.

### Locked architecture decisions
- Naming: `pluz_*.py` / `pluz-*.sh` / `pluz-*.bat`
- Layout: see README.md
- `PLUZ.pyz` = single portable executable (stdlib `zipapp` from `core/`)
- **4 manifests**: `PLUZ-ps5-Source.json` (latest, what pldmgr consumes),
  `PLUZ-ps5-Hosted.json` (up to 3 builds), `PLUZ5-PKG.json`, `PLUZ5-ffpfsc.json`;
  plus `manifests/split/` category copies. Manifests carry no timestamps.
- Filename convention: `{payload}[-{variant}]_v{version}[_Expi{YYYYMMDD}].{ext}`;
  FW and hardware target are registry metadata, never filename parts
- Retention: Source = latest 1; hosted = latest 3; `protected_fallback` kept forever
- Categories capped at 10 on purpose
- Optional entry fields: `platform`, `fw_min`/`fw_max` (hand-typed), `hw_target`

### Done
- Core engine: check, merge, update, pkg, ffpfsc, validate, dedupe, cleanup, migrate, backup
- Filename parser fix for multi-hyphen identities (two-stage parse/resolve)
- `PLUZ-AllStar` (.bat + .sh): check, update, pkg, ffpfsc, validate, git push
- `add-source.html` full CRUD (preserves unknown fields on edit)
- `catalog.html` read-only catalog: tabs, tiles/list, search, platform/hardware/category filters, themes
- ffpfsc category + registry; `platform` field; `hw_target` field
- GitHub Actions: manifest regeneration + validation
- Registries now hold: **47 payload identities** (`etaHEN (EchoStretch, Zecoxao)`, `ShadowMountPlus (Beta, Alpha)`, `zftp (itsPLK)`, `zhttp (itsPLK)`, `websrv`, `CheatRunner (default, RDX)`, `elfldr (default, itsPLK)`, `fan-target-70c`, `fan-target-75c`, `fan-target-80c`, `ps5power-notify`, `ps5power-poweroff`, `ps5power-reboot`, `ps5power-suspend`, `poords4-rc`, `poords4-status`, `poords4-stop`, `ps5-self-decrypter-full-system`, `ps5-self-decrypter-game`, `ps5-self-decrypter-shellcore`, `ps5-self-decrypter-system-common-lib`, `ps5-self-pager-full-system`, `ps5-self-pager-game`, `ps5-self-pager-shellcore`, `ps5-self-pager-system-common-lib`, `garlic-savemgr`, `garlic-worker`, `hwinfo-bench`, `hwinfo-sysinfo`, `onionHEN`, `BackPork`, `ftpsrv (default, drakmor, autopause, ps5-payload, install)`, `ProsperoMgr`, `JailbreakStore`, `PIZZA-HEN`, `ChronicLoader-PS5-Payload`, `kstuff-lite (EchoStretch, drakmor)`, `webkit-autoloader (installer, host)`, `ps5-payload-manager`, `ChronicLoader`, `kstuff (EchoStretch, default)`, `ps5-webkit-autoloader`, `ps5library-agent`, `ps5-pkg-manager`, `fgg-unpack`, `elf-launcher`, `wk-autoloader`),
  **2 PKG** (`PS5Webkit`, `PS5Library`), **7 ffpfsc tools** (`ps5-game-compressor`, `ampr-emu`, `dlc-emu`, `lazy-ampr`, `lz4-game-compressor`, `lz4-compression`, `exfat2ampr`)

### Still to build (in order)
1. RSS/Atom export per type from the manifests (pattern confirmed in production by evoX-CoreOS)
2. AIO pack builder: one zip per category + one master zip (mind GitHub's per-file size limits and duplicate storage)
3. Finish the nexgen999 sweep (last 7 repos)
4. Add `ffpfsc_registry.json` to the editor
5. Make `cleanup` and `backup` ffpfsc-aware (`dedupe`, `check`, `validate` already are)
6. Register entries once they ship release artifacts: pLinux5-NG (Linux), PS5-Jailbreak-Doctor (PC tool, probably reference only)

### Known gaps (flagged, not silently fixed)
- `ftpsrv_drakmor_v1.6-ng-test2.elf` uses an underscore before `drakmor` and won't resolve until renamed (`docs/rename-map.md`)
- `zerodaysofficial/ps5-exfat-pkg-builder-v1` is a PC-side tool with no distributable artifact: reference only
- KAR0218 PS4 host: no distributable file names confirmed, so no entries yet
- `exfat2ampr` is registered but its author says it is not console-tested; theghostonline's repo shows no license file — check before mirroring binaries
- `.ffpkg` home-screen apps (exfat2ampr PPSA99272, theghostonline PPSA99420) fit no ffpfsc type yet
- `fw_min`/`fw_max`/`hw_target` are unset on every new entry until set by hand
- Manifest file names are mixed (`PLUZ-ps5-` for Source/Hosted, `PLUZ5-` for PKG/ffpfsc) — decide whether to unify

---

## 4. ZendRz
PSZend (rebuilt six-file layered core) merged with Zendit (plugin architecture,
Y2JB/BD-JB/P2JB loaders kept as fallbacks). Planned: multi-port scan, profiles,
favorite ports, themes, PKG install and FTP/WebDAV clients (reference:
DirectPackageInstaller, ps5upload), self-hosted servers, optional PLUZ5 manifest
catalog, and an install-tracking log (PS5 side and PC side) showing installed vs
server version, release and DLC. No permanent PKG library on the console.

## 5. ZperoMGR5
Custom webkit (Zpero-Webkit) + ProsperoMgr fork + ShrctZ + pldmgr + Slopkit, FW 1.00
to the latest jailbreakable; PLUZ5-backed payload library; cheats (etaHEN/mc4-style,
user-extensible sources); per-addon toggles; stays PS5-only. Console UI options:
ps5-homebrew-ui or ps5-react. ShrctZ's parser and inject are still broken.

## 6. KmprZu
Engine plus modular addons: KmprZ-ps5 (Phase 1 done, Phase 2 next), KompreZ (stages
0–7 done), GameLibZ section, PS5-System-Toolkit. Tree-form sidebar (vendor > system >
version). References: Loopayeh/pkg-viewer, PSVIETHOA-FPKG-Builder (real `.ffpkg`
UFS2 format), Nazky/Lazy_AMPR, NookieAI/kura, the compressors listed in section 8.
Tracking: a not-yet-released compression format teased by x.com/packizard.

## 7. WBrowser
`ps5xploit/WBrowser` — browser-based homebrew launcher UI; candidate delivery
front-end for ShrctZ. PKG confirmed working on the console.

---

## 8. Full source list (every URL checked across this project family)

### PLUZ-ps5 direct references
- https://github.com/itsPLK/ps5-payload-manager (pldmgr itself — the
  manifest schema target)
- https://github.com/itsPLK/ps5-payloads-mirror
- https://github.com/itsPLK/ps5-webkit-autoloader
- https://github.com/itsPLK/ps5-elfldr
- https://github.com/nexgen999/evoX-CoreOS — now on an **hourly automated
  release cycle** (multiple releases/day via GitHub Actions), producing
  `payloads.json`/`pkg.json`/`ffpfsc.json`/`apps.json` + matching RSS
  feeds + an OPML aggregator + AIO zip bundles per type
- https://github.com/nexgen999/evoX-CoreOS-WebUI — the read-only catalog
  browser reference for PLUZ's planned WebUI; static, no build step,
  `config.json` + commented `config.sample.jsonc` pattern
- https://github.com/nexgen999/PS5-Super-PLDMGR-Auto-Updater
- https://github.com/nexgen999/EvoX-Universal.Store — **could not verify
  contents**, doesn't surface in search, flagging honestly rather than
  guessing
- https://github.com/nexgen999/evoX-CoreOS_AutoInstaller — not yet checked
- https://github.com/nexgen999/evoX-RSS — the RSS/CORS-proxy technique
  (`api.rss2json.com`) used to read GitHub Atom feeds client-side without
  hitting the 60/hr unauthenticated API limit
- https://github.com/nexgen999/PS5-Repository-List — curated PS5 scene
  dev/link directory; worth linking to rather than duplicating
- https://x.com/nexgen999 — confirmed in his own words: "evoX-CoreOS is
  Store for PLDMGR (payloads only) + others download + rss feed...
  evoX-CoreOS WebUI is the web interface." The specific status ID given
  this round (`2100660763895398741`) didn't surface in search and
  couldn't be fetched directly; a closely related post from the same
  account (`2097849680877011361`, same WebUI-demo content) was found
  instead.
- https://github.com/notmaj0r/ProsperoMgr
- https://github.com/notmaj0r/CheatRunner
- https://github.com/notmaj0r/JailbreakStore
- https://github.com/aydencharles/onionHEN
- https://github.com/StonedModder/ChronicLoader-PS5-Payload
- https://github.com/Michele-M-Media/PIZZA-HEN
- https://github.com/drakmor/ShadowMountPlus
- https://github.com/zecoxao/zecoxao.github.io (real etaHEN-Zecoxao
  source, confirmed by direct file path, correcting an earlier guess)
- https://github.com/BestPig/BackPork
- https://github.com/EchoStretch/kstuff-lite
- https://github.com/ps5-payload-dev/ftpsrv
- https://github.com/ps5-payload-dev/websrv
- https://github.com/ps5-payload-dev/elfldr
- https://github.com/zerodaysofficial/ps5-exfat-pkg-builder-v1 (PC-side
  dev tool, not a cataloged payload)
- https://github.com/McCaulay/mast1c0re — real, mature SDK for
  game-save-exploit-delivered payloads; different delivery mechanism
  (PS2 save injection, not FTP/ELF sideload), doesn't fit the current
  elf/bin/pkg model as-is
- https://cturt.github.io/mast1c0re.html

### KmprZ-ps5 / compression-format references
- https://github.com/thanhsondev/PSVIETHOA-FPKG-Builder
- https://github.com/thanhsondev/PSVIETHOA-FPKG-Builder/releases
- https://github.com/Loopayeh/pkg-viewer
- https://github.com/Loopayeh/game-list
- https://github.com/SvenGDK/PS5PKGReader
- https://github.com/SvenGDK (LibProsperoPKG — real PS5 PKG metadata
  field shapes: `ContentId`, `TitleId`, `Title`, `Version`,
  `ApplicationType`)
- https://github.com/zerodaysofficial/ps5-exfat-pkg-builder-v1/releases
- https://github.com/Nazky/Lazy_AMPR

### KmprZ-Universal references
- https://github.com/NookieAI/kura

### ShrctZ references
- https://github.com/ps5xploit/WBrowser

### General scene research / people to follow
- https://psx-place.com/
- https://psx-place.com/resources/categories/playstation-5-ps5.49/
- https://ps5exploit.com/
- https://gbatemp.net/forums/sony-playstation-5.298/
- https://x.com/nexgen999
- https://github.com/Gezine
- https://x.com/TeRex777_
- https://x.com/calmboy2019
- https://x.com/LightningMods_
- https://x.com/gezine_dev
- https://x.com/theflow0
- https://x.com/master_s9
- https://x.com/NanospeedGamer
- https://x.com/TheWizWiki
- https://x.com/StretchEcho
- https://x.com/frwololo
- https://x.com/Sonic_Iso
- https://github.com/flaviopenas-ps
- https://github.com/DrYenyen

### Not yet checked (carried forward)
- https://github.com/nexgen999?tab=repositories (last 7 repos — general
  sweep, not yet done)

---

### Added 2026-10 (this round)

**Exploit / firmware landscape**
- PS5 "Relapse" by ntfargo (GitHub, published 2026-09-29, MIT) — public
  WebKit + kernel-race chain for FW 7.00–13.60 incl. PS5 Pro, in-memory only
  (repo URL not captured in this session)
- https://github.com/PS5Dev/Byepervisor-Reborn — hypervisor exploit base,
  FW 13.60/13.20 supported; developer-only, ships no patches
- https://github.com/pLabs5/pLinux5-NG — Linux boot on FW 8.xx–13.60; early,
  no releases listed, license wording inconsistent (README vs repo)
- https://github.com/boykopovar/AnyPS5 — relinker + PRX reimplementations
- Sony firmware 14.00 (2026-09-16) closes the Relapse hole; no public 14.00
  kernel exploit as of this writing

**On-console compression (AMPR LZ4)**
- https://github.com/theghostonline/PS5-LZ4-Compression — most complete;
  native app PPSA99420 + engine, port 5920, console-tested on FW 13.60
- https://github.com/gameboy829/PS5-LZ4-Game-Compressor — port 5911, beta.1
- https://github.com/ViiNCENZO10/exfat2ampr — port 6972, queue + pause/resume;
  author states not yet console-tested
- https://github.com/juma-sayeh/PS5-Game-Compressor
- https://github.com/drakmor/ampr_emu and https://github.com/drakmor/dlc_emu
- https://pippo26442999.github.io/.exFAT/ampr-emu-drakmor/manifest.json —
  hosted APR-EMU build manifest

**Native PS5 app / UI building blocks**
- https://github.com/blackbearreloaded/ps5-homebrew-ui (+ ps5-native-app-boilerplate, ps5-opengl)
- https://github.com/half144/ps5-react
- https://github.com/Phoenixx1202/Spectrum-Library — library-manager UI reference

**Tools, diagnostics and PS5 Pro**
- https://github.com/obl1vn/Unlock-ps5-pro-memory — one `param.json` flag, ~1.2 GiB more GPU memory on PS5 Pro (one console, FW 13.60)
- https://github.com/asomimlrxd/PS5-Jailbreak-Doctor — Windows log-diagnosis app (MIT)
- https://github.com/leolobato/playden-ps5 — alpha Steam-library client, FW 13.60 only
- https://github.com/rdiol12/PS5Library and https://github.com/itsPLK/ps5-pkg-manager (now in the registries)
- https://github.com/seregonwar/zftpd
- https://github.com/KAR0218/KAR0218.github.io — PS4 FW-branched exploit host; no distributable artifact names visible, so not registered

---

### Added 2026-10 (this round)

**Exploit / firmware landscape**
- PS5 "Relapse" by ntfargo (GitHub, published 2026-09-29, MIT) — public
  WebKit + kernel-race chain for FW 7.00–13.60 incl. PS5 Pro, in-memory only
  (repo URL not captured in this session)
- https://github.com/PS5Dev/Byepervisor-Reborn — hypervisor exploit base,
  FW 13.60/13.20 supported; developer-only, ships no patches
- https://github.com/pLabs5/pLinux5-NG — Linux boot on FW 8.xx–13.60; early,
  no releases listed, license wording inconsistent (README vs repo)
- https://github.com/boykopovar/AnyPS5 — relinker + PRX reimplementations
- Sony firmware 14.00 (2026-09-16) closes the Relapse hole; no public 14.00
  kernel exploit as of this writing

**On-console compression (AMPR LZ4)**
- https://github.com/theghostonline/PS5-LZ4-Compression — most complete;
  native app PPSA99420 + engine, port 5920, console-tested on FW 13.60
- https://github.com/gameboy829/PS5-LZ4-Game-Compressor — port 5911, beta.1
- https://github.com/ViiNCENZO10/exfat2ampr — port 6972, queue + pause/resume;
  author states not yet console-tested
- https://github.com/juma-sayeh/PS5-Game-Compressor
- https://github.com/drakmor/ampr_emu and https://github.com/drakmor/dlc_emu
- https://pippo26442999.github.io/.exFAT/ampr-emu-drakmor/manifest.json —
  hosted APR-EMU build manifest

**Native PS5 app / UI building blocks**
- https://github.com/blackbearreloaded/ps5-homebrew-ui (+ ps5-native-app-boilerplate, ps5-opengl)
- https://github.com/half144/ps5-react
- https://github.com/Phoenixx1202/Spectrum-Library — library-manager UI reference

**Tools, diagnostics and PS5 Pro**
- https://github.com/obl1vn/Unlock-ps5-pro-memory — one `param.json` flag, ~1.2 GiB more GPU memory on PS5 Pro (one console, FW 13.60)
- https://github.com/asomimlrxd/PS5-Jailbreak-Doctor — Windows log-diagnosis app (MIT)
- https://github.com/leolobato/playden-ps5 — alpha Steam-library client, FW 13.60 only
- https://github.com/rdiol12/PS5Library and https://github.com/itsPLK/ps5-pkg-manager (now in the registries)
- https://github.com/seregonwar/zftpd
- https://github.com/KAR0218/KAR0218.github.io — PS4 FW-branched exploit host; no distributable artifact names visible, so not registered

---

## 9. Working directories
Local paths for each machine (Arch Linux project root, Windows portable tools)
are kept in each machine's local configuration and `.env` — not recorded in
this committed document.

## 10. Immediate next steps (in order)
1. Decisions: ZperoMGR5 vs Relapse; KmprZu orchestrate vs own converter
2. PLUZ5: RSS export, then AIO pack builder
3. ZendRz rebuild (second in build order)
4. nexgen999 sweep; editor and cleanup/backup ffpfsc support
5. Tag `hw_target` / firmware on registry entries as they are verified
