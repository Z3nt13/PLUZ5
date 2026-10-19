# PLUZ5 Library

_Powered By Z3nT13's PLUZ5. Generated from `PLUZ5-infos.json`; edit it with `web/library.html`._

## Payload Senders / Managers (PC & Web)

### PlayStation Payload Center
- **URL:** https://github.com/Pharaoh2k/PlayStation-Payload-Center
- **Author:** Pharaoh2k
- **Variant:** org
- **Desc:** Cross-platform Avalonia/.NET desktop tool. Discover consoles, browse payload catalogs, SHA-256 verify, queue, and stream payloads to jailbroken PS4/PS5.
- **Tags:** #sender #tool #ps4 #P5U #catalog #queue #sha256 #avalonia
- **Notes:** UDP discovery (PS4:987, PS5:9302). Common send ports 9020/9021.

### ps5-payload-manager
- **URL:** https://github.com/itsPLK/ps5-payload-manager
- **Author:** itsPLK
- **Variant:** org
- **Desc:** Modern web-based dashboard that runs on the PS5 itself. Manage, import, and auto-load payloads. Homescreen shortcut support.
- **Tags:** #payload #manager #webui #P5U #autoload #itsplk
- **Notes:** Can be set as only entry in autoload.txt.

### PKG Sender
- **URL:** https://github.com/Loopayeh/pkg-sender
- **Author:** Loopayeh
- **Variant:** org
- **Desc:** LAN PKG installer for PS4/PS5. Auto-find console, queue installs. No USB needed. Ships `pkg-receiver.elf` for PS5.
- **Tags:** #sender #pkg #tool #ps4 #P5U #port-12800
- **Notes:** PS5 uses pkg-receiver.elf on port 12800. PS4 uses Remote Package Installer or GoldHEN.

### PS5-4-Payload-Sender-Android
- **URL:** https://github.com/PixelPop25/PS5-4-Payload-Sender-Android
- **Author:** PixelPop25
- **Variant:** org
- **Desc:** Simple Android TCP payload injector. Supports .bin / .elf / .lua / .js / .jar.
- **Tags:** #sender #android #P5U #mobile
- **Notes:** Keep mobile data off so traffic stays on LAN.

### PS5AutopayloadHA
- **URL:** https://github.com/cosmicflow2512/PS5AutopayloadHA
- **Author:** cosmicflow2512
- **Variant:** org
- **Desc:** Home Assistant add-on that fully automates the post-exploit payload chain (send / delay / wait-for-port flows).
- **Tags:** #sender #ha #automation #P5U #autoload
- **Notes:** Supports multiple loaders (9021, 9025, 9026, 50000…).

### web-based-ps-package-manager
- **URL:** https://github.com/h-haghpanah/web-based-ps-package-manager
- **Author:** h-haghpanah
- **Variant:** org
- **Desc:** Browser tool for managing and sending packages to PS4 and PS5.
- **Tags:** #sender #pkg #webui #ps4 #P5U
- **Notes:** PS5 side can use ps5_file_downloader (8283) or pkg_receiver (12800).

### Send-Payload-to-PS
- **URL:** https://github.com/Master-s/Send-Payload-to-PS
- **Author:** Master-s
- **Variant:** org
- **Desc:** Multi-platform payload sender including iOS support.
- **Tags:** #sender #ios #android #P5U #ps4
- **Notes:** Has PC and iOS components.

## Core Payload Infrastructure (PS5)

### ps5-payload-dev/sdk
- **URL:** https://github.com/ps5-payload-dev/sdk
- **Author:** ps5-payload-dev
- **Variant:** org
- **Desc:** SDK for developing PS5 payloads using dynamic linking. Works with elfldr, websrv, BD-J, remote_lua_loader, etc.
- **Tags:** #sdk #P5U #ps5-payload-dev #elf
- **Notes:** Install to `/opt/ps5-payload-sdk`. Essential for building native payloads.

### ps5-payload-dev/websrv
- **URL:** https://github.com/ps5-payload-dev/websrv
- **Author:** ps5-payload-dev
- **Variant:** org
- **Desc:** Simple web server payload (port 8080). Launch homebrew and ELF payloads from the PS5 browser or remotely.
- **Tags:** #payload #webui #P5U #port-8080 #ps5-payload-dev
- **Notes:** Looks for homebrew under `/data/homebrew`, USB, and external storage.

### ps5-payload-dev/elfldr
- **URL:** https://github.com/ps5-payload-dev/elfldr
- **Author:** ps5-payload-dev
- **Variant:** org
- **Desc:** ELF loader for jailbroken PS5s. Accepts payloads on port 9021.
- **Tags:** #payload #loader #P5U #port-9021 #elfdir #ps5-payload-dev
- **Notes:** Primary target for ZendRz and most PC senders.

### ps5-payload-dev/ftpsrv
- **URL:** https://github.com/ps5-payload-dev/ftpsrv
- **Author:** ps5-payload-dev
- **Variant:** org
- **Desc:** FTP server for jailbroken PS4 and PS5.
- **Tags:** #payload #ftp #P5U #ps4 #ps5-payload-dev #port-2121
- **Notes:** Common companion after HEN.

### ps5-payload-dev/fetchpkg
- **URL:** https://github.com/ps5-payload-dev/fetchpkg
- **Author:** ps5-payload-dev
- **Variant:** org
- **Desc:** Fetch PS4/PS5 package updates referenced by a JSON-formatted manifest URL.
- **Tags:** #payload #pkg #tool #P5U #ps4 #ps5-payload-dev
- **Notes:** Useful for update pipelines.

### etaHEN / forks
- **URL:** https://github.com/MasterPS0/etaHEN-SPayload
- **Author:** MasterPS0
- **Variant:** org
- **Desc:** AIO HEN + toolbox for jailbroken PS5. Debug settings replacement, plugins, rest mode options, etc.
- **Tags:** #hen #payload #P5U #toolbox #etahen
- **Notes:** Many tools assume etaHEN or compatible environment is running.

### onionHEN
- **URL:** (none)
- **Author:** 
- **Variant:** org
- **Desc:** Homebrew enabler and toolbox built on top of etaHEN.
- **Tags:** #hen #payload #P5U #onionhen #toolbox
- **Notes:** Frequently listed in payload mirrors.

### PIZZA-HEN
- **URL:** https://github.com/Michele-M-Media/PIZZA-HEN
- **Author:** Michele-M-Media
- **Variant:** org
- **Desc:** Experimental all-in-one PS5 homebrew environment with its own integration layer, Toolbox, service chain, and branding (builds on upstream open-source projects).
- **Tags:** #hen #payload #P5U #toolbox #aio
- **Notes:** v2.00 public source checkpoint. Maintained by Michele Media.

### ShadowMountPlus
- **URL:** https://github.com/drakmor/ShadowMountPlus
- **Author:** drakmor
- **Variant:** org
- **Desc:** Automated background auto-mounter for jailbroken PS5. Detects, mounts, and installs game backups from internal/external storage. Supports UFS, exFAT, PFS, and nested compressed PFS containers.
- **Tags:** #payload #mount #P5U #shadowmount #automation #drakmor
- **Notes:** Core for game library / KmprZ workflows. Very widely used.

### kstuff-lite
- **URL:** https://github.com/EchoStretch/kstuff-lite
- **Author:** EchoStretch
- **Variant:** EchoStretch
- **Desc:** Lite kstuff build – crypto, FSELF, NPDRM, loader work. Optimized UELF/KELF transitions and diagnostics.
- **Tags:** #payload #kstuff #P5U #echostretch #fself
- **Notes:** Popular base; many forks exist (including drakmor).

### kstuff-lite
- **URL:** https://github.com/drakmor/kstuff-lite
- **Author:** drakmor
- **Variant:** Drakmor
- **Desc:** drakmor fork of kstuff-lite with improved fpkg/FSELF handling, faster startup and internal optimizations.
- **Tags:** #payload #kstuff #P5U #drakmor #fself
- **Notes:** Alternative optimized build.

### nanoDNS
- **URL:** https://github.com/drakmor/nanoDNS
- **Author:** drakmor
- **Variant:** org
- **Desc:** PlayStation 4/5 DNS proxy server.
- **Tags:** #payload #dns #tool #P5U #ps4 #drakmor
- **Notes:** Local DNS proxy useful for blocking/redirecting Sony endpoints.

### ampr_emu
- **URL:** https://github.com/drakmor/ampr_emu
- **Author:** drakmor
- **Variant:** org
- **Desc:** AMPR userland emulation.
- **Tags:** #payload #emu #P5U #drakmor
- **Notes:** Public beta; Discord linked from repo.

### BackPork
- **URL:** https://github.com/BestPig/BackPork
- **Author:** BestPig
- **Variant:** org
- **Desc:** Lets you sideload system libraries into PS5 games.
- **Tags:** #payload #sideload #P5U #library #bestpig
- **Notes:** Useful for advanced game patching / library injection.

### ps5debug-NG
- **URL:** https://github.com/EchoStretch/ps5debug-NG
- **Author:** EchoStretch
- **Variant:** org
- **Desc:** PS5 debugger payload – userland TCP wire-protocol server hosted inside SceShellCore.
- **Tags:** #payload #debug #P5U #echostretch
- **Notes:** GPL-3. For development / reverse engineering.

### PS5 Account Activator
- **URL:** https://github.com/Epinorr/ps5-account-activator
- **Author:** Epinorr
- **Variant:** org
- **Desc:** All-in-one ELF that combines offline account activation + NP Fake Signin in a single execution. Idempotent, region-aware, clean on-screen notifications.
- **Tags:** #payload #activator #account #np #P5U #port-9021
- **Notes:** Send `AIO-Activator.elf` to the foreground user (port 9021). ~v2.1.0.

### np-fake-signin
- **URL:** https://github.com/earthonion/np-fake-signin
- **Author:** earthonion
- **Variant:** org
- **Desc:** Sets PSN state to "signed in" on PS4/PS5. Standalone NP fake sign-in (also folded into Account Activator AIO builds).
- **Tags:** #payload #np #account #P5U #ps4
- **Notes:** Primary GitHub home for the payload.

### ps5-account-tools
- **URL:** https://github.com/MangoScango/ps5-account-tools
- **Author:** MangoScango
- **Variant:** org
- **Desc:** Web UI (port 6769) to manage local PS5 accounts — offline activation + fake PSN sign-in in one place, plus local profile avatar change. Enables Remote Play pairing (Chiaki / Px Play).
- **Tags:** #payload #account #activator #np #webui #P5U #port-6769 #remote-play
- **Notes:** After activation, note Account IDs, reboot, then pair remote play. Pair with nanoDNS to keep PSN blocked.

### ps5-fw-spoof
- **URL:** https://github.com/illusionyy/ps5-fw-spoof
- **Author:** illusionyy
- **Variant:** org
- **Desc:** Patch PS4 SDK + PS5 Update version in kernel data to `99.99` without hardcoded offsets.
- **Tags:** #payload #spoof #firmware #P5U #ps4
- **Notes:** Version spoof helper for tools that gate on FW/SDK version.

### ps5-self-pager
- **URL:** https://github.com/idlesauce/ps5-self-pager
- **Author:** idlesauce
- **Variant:** org
- **Desc:** PS5 SELF decryptor (“yet another PS5 SELF decryptor”).
- **Tags:** #tool #decrypt #self #P5U #dev
- **Notes:** Development / reverse-engineering utility.

### WelcomeHubActivator
- **URL:** https://github.com/ghost1372/WelcomeHubActivator
- **Author:** ghost1372
- **Variant:** org
- **Desc:** PS5 ELF payload that enables the Welcome Hub (FW 10.00–13.60). Requires prior fake account activation + fake sign-in (e.g. ProsperoManager / Account Activator).
- **Tags:** #payload #activator #welcome-hub #account #P5U #port-9021
- **Notes:** One-shot; persists across reboots. Binary: `WelcomeHubActivator-org_v1.0.0.elf`. Backs up `app.db` → `app.bckdb` before edit. If activation fails, may need System *Feature* Update (not full System Software Update). Sign out/in after success.

### ps5upload
- **URL:** (none)
- **Author:** 
- **Variant:** org
- **Desc:** Fast, reliable file transfer between PC and PS5 (requires companion PC app).
- **Tags:** #tool #transfer #P5U #upload
- **Notes:** Useful for pushing large game dumps or packages.

## Autoloaders / Exploit Loaders

### ps5-webkit-autoloader
- **URL:** https://github.com/itsPLK/ps5-webkit-autoloader
- **Author:** itsPLK
- **Variant:** org
- **Desc:** Automated payload loader for exploited PS5 consoles (WebKit path).
- **Tags:** #autoload #loader #P5U #webkit #itsplk
- **Notes:** Very popular (1k+ stars).

### ps5-bdjb-autoloader
- **URL:** https://github.com/itsPLK/ps5-bdjb-autoloader
- **Author:** itsPLK
- **Variant:** org
- **Desc:** Automated payload loader for exploited PS5 consoles (BD-J path).
- **Tags:** #autoload #loader #P5U #bdj #itsplk
- **Notes:** BD-J entry point automation.

### ps5-lua-autoloader
- **URL:** https://github.com/itsPLK/ps5-lua-autoloader
- **Author:** itsPLK
- **Variant:** org
- **Desc:** Automated payload and Lua script loader for exploited PS5 consoles.
- **Tags:** #autoload #loader #P5U #lua #itsplk
- **Notes:** For Lua-based exploit chains.

### ps5-y2jb-autoloader
- **URL:** https://github.com/itsPLK/ps5-y2jb-autoloader
- **Author:** itsPLK
- **Variant:** org
- **Desc:** Automated payload loader for exploited PS5 consoles (Y2JB path).
- **Tags:** #autoload #loader #P5U #y2jb #itsplk
- **Notes:** Very popular Y2JB automation (~900 stars).

### P2JB-Y2JB-Porting
- **URL:** https://github.com/matem6/P2JB-Y2JB-Porting
- **Author:** matem6
- **Variant:** org
- **Desc:** PS5 jailbreak via Y2JB. Ports Gezine’s p2jb kqueueex cr_ref overflow.
- **Tags:** #exploit #y2jb #P5U #jailbreak #port
- **Notes:** Exploit porting work around Y2JB / p2jb.

### Luac0re
- **URL:** https://github.com/Gezine/Luac0re
- **Author:** Gezine
- **Variant:** org
- **Desc:** mast1c0re variation that uses Lua scripting for easier exploit development.
- **Tags:** #exploit #lua #mast1c0re #P5U #ps4 #dev
- **Notes:** Scriptable save-game exploit framework variant.

### mast1c0re
- **URL:** https://github.com/McCaulay/mast1c0re
- **Author:** McCaulay
- **Variant:** org
- **Desc:** Develop payloads that can be executed on PS4 or PS5 through a game save file.
- **Tags:** #exploit #mast1c0re #P5U #ps4 #save #dev
- **Notes:** Classic save-file payload framework. Docs: https://cturt.github.io/mast1c0re.html

### PS5-Super-PLDMGR-Auto-Updater
- **URL:** https://github.com/nexgen999/PS5-Super-PLDMGR-Auto-Updater
- **Author:** nexgen999
- **Variant:** org
- **Desc:** Auto-updater focused on the PS5 Payload Manager (PLDMGR) ecosystem.
- **Tags:** #tool #autoload #updater #P5U #pldmgr
- **Notes:** Keeps payload manager related components current.

## File Managers / Web UIs

### ps5-web-file-manager
- **URL:** https://github.com/owendswang/ps5-web-file-manager
- **Author:** owendswang
- **Variant:** org
- **Desc:** File manager for PS5 with a web UI.
- **Tags:** #file-manager #webui #payload #P5U
- **Notes:** Browse/manage files from browser.

### BFpilot
- **URL:** https://github.com/ItsBlurf/BFpilot
- **Author:** ItsBlurf
- **Variant:** org
- **Desc:** Lightweight PS5 file manager – browser based.
- **Tags:** #file-manager #webui #payload #P5U
- **Notes:** Minimal alternative to heavier managers.

### NetDis / PS5-NetDis
- **URL:** https://github.com/eladharels/PS5-NetDis
- **Author:** eladharels
- **Variant:** org
- **Desc:** Network diagnostic payload — lists every TCP/UDP socket on a jailbroken PS5 (listening ports, connections, owner process + title ID, reachable from network vs localhost only). Live page in console browser or phone.
- **Tags:** #payload #network #diagnostic #webui #P5U #port-8070 #port-9021
- **Notes:** Send `NetDis.elf` to 9021; UI at `http://<ps5-ip>:8070`. Homescreen Media tile. Binary: `NetDis-org_v1.0.0.elf`. Useful before starting tools that need a free port.

## Overlays / Menus / System UI

### Prospero-Menu
- **URL:** https://github.com/StonedModder/Prospero-Menu
- **Author:** StonedModder
- **Variant:** org
- **Desc:** Community expandable overlay system for jailbroken PS5 (Tesla Menu style). Drop-in overlays (program `.ovl` or pure JSON menus). Accessible at any time without web UIs.
- **Tags:** #overlay #menu #tesla #P5U #fan-control #boot-anim #elfdir #games #dumper #stonedmodder
- **Notes:** Overlays live in `/data/ProsperoMenu/overlays/`. Bundled: Fan Control, Console Tools, Games, App Dumper, Elf-Updater, Quick Launch. Supports boot animation / splash via elfdir addon.

## Themes / Home Screen / Visual

### LiveShell
- **URL:** https://github.com/ZiZc3/LiveShell
- **Author:** ZiZc3
- **Variant:** org
- **Desc:** Animated video wallpapers for the PS5 home screen (LiveShell Engine). Discover tab with hundreds of wallpapers, per-game/app videos (experimental), PS Store-only mode, sound support, look effects (Dim/Vignette/Haze), parallax, rest-mode resume, phone/PC remote control.
- **Tags:** #theme #wallpaper #homescreen #video #P5U #visual #webui #media
- **Notes:** Load `liveshell.elf`. Videos go in `/data/LiveShell/video` or USB `liveshell/` folder. H.264/HEVC ≤1080p only (4K not yet). Pause while games run so they keep the video decoder. Current version ~v1.3.

## Media / Players

### PS-Play
- **URL:** https://github.com/MounirHero/PS-Play
- **Author:** MounirHero
- **Variant:** org
- **Desc:** All-in-one media hub for jailbroken PS5 — DLNA receiver, DLNA/UPnP browser, native Stremio client, IPTV/Live TV and USB playback. Minimal AMOLED-black UI.
- **Tags:** #media #player #dlna #stremio #iptv #P5U #native-app
- **Notes:** Based on Prospero Player; Stremio integration from Nuvio Portable.

## Stores / Download Managers

### ProsperoStore
- **URL:** https://github.com/darkxex/ProsperoStore
- **Author:** darkxex
- **Variant:** org
- **Desc:** Native PS5 homebrew app store (title `PPSA99000`) for the catalog at prosperostore.net / homebrew.page. Browse, install, update, uninstall from the couch; signed catalog with download verification.
- **Tags:** #store #native-app #P5U #shadowmount #port-9021 #catalog
- **Notes:** Aggregator only — apps belong to their own devs. Needs ShadowMountPlus (≥1.7beta4) + ELF loader on 9021; ships a one-shot Lapy helper if no resident Lapy is running. Previous folders kept under `/data/prosperostore/previous/<TITLE ID>` on update. Catalog fallback mirror: darkxex.github.io (signature-checked). Alpha ~v1.000.100. Binary: `ProsperoStore-org_v1.000.100` (native app / FFPKG style, not a single ELF).

### Orbit Store
- **URL:** https://github.com/saawant12/orbit-store-ps5
- **Author:** saawant12
- **Variant:** org
- **Desc:** Modern PS5 download manager with native TV app, phone controls, and Orbit Zero (Mac/Windows/Linux). Browse ~1600 games (PS5 + PS4), compare sources/formats, single-file downloads to console or attached drive. Catalogue updates automatically.
- **Tags:** #store #download-manager #P5U #ps4 #webui #native-app #shadowmount
- **Notes:** Sources include Archive.org, Vikingfile, AkiraBox. Optional TorBox + Archive.org sign-in. Library integrates with ShadowMount. Always free. Latest beta ~v1.3.5.

### RecompStore
- **URL:** https://github.com/elripalda/RecompStore
- **Author:** elripalda
- **Variant:** org
- **Desc:** Homebrew app store for jailbroken PS5 that installs and updates native ports of recompiled games. Bring your own disc.
- **Tags:** #store #recomp #P5U #native-app
- **Notes:** Focused on recompiled / ported titles rather than dumps.

### RemotePFS
- **URL:** https://github.com/PSBrew/RemotePFS
- **Author:** PSBrew
- **Variant:** org
- **Desc:** Linux SBC service that emulates an exFAT USB mass storage device via USB OTG, presenting files from a remote Synology NAS to a jailbroken PS5 via ShadowMountPlus.
- **Tags:** #tool #mount #pfs #shadowmount #P5U #nas #psbrew
- **Notes:** Hardware bridge: NAS → SBC → fake USB → PS5. Pairs with ShadowMountPlus.

## Payload Mirrors & Catalogs

### ps5-payloads-mirror
- **URL:** https://github.com/itsPLK/ps5-payloads-mirror
- **Author:** itsPLK
- **Variant:** org
- **Desc:** Automated mirror of useful PS5 payloads with version tracking, source links, and direct downloads. Excellent living reference list.
- **Tags:** #mirror #catalog #P5U #itsplk #payload
- **Notes:** Keep an eye on this for new releases.

### PS5LinkCentalizer
- **URL:** https://github.com/pedrohti/PS5LinkCentalizer
- **Author:** pedrohti
- **Variant:** org
- **Desc:** Community link hub for the PS5 jailbreak scene. Auto-updates project data from GitHub.
- **Tags:** #mirror #catalog #links #P5U
- **Notes:** Good discovery source.

### zecoxao.github.io
- **URL:** https://github.com/zecoxao/zecoxao.github.io
- **Author:** zecoxao
- **Variant:** org
- **Desc:** Host of many historical PS scene sites and tools.
- **Tags:** #mirror #archive #ps4 #P5 #historical
- **Notes:** Useful for older payloads and documentation.

## Game / Library / Compression (KmprZ relevance)

### MkPFS
- **URL:** https://github.com/PSBrew/MkPFS
- **Author:** PSBrew
- **Variant:** org
- **Desc:** Tool for building PFS images from loose game files. Reads `sce_sys/param.json`. Core building block for future KmprZ compression stage.
- **Tags:** #tool #pfs #compression #P5U #kmprz #param-json
- **Notes:** Directly relevant to Stage 1 of KmprZ.

### PS5-Game-Compressor
- **URL:** https://github.com/juma-sayeh/PS5-Game-Compressor
- **Author:** juma-sayeh
- **Variant:** org
- **Desc:** Standalone PS5 payload for compressing, unpacking, validating, and repairing ShadowMountPlus-mounted games.
- **Tags:** #payload #compression #P5U #shadowmount #kmprz #tool
- **Notes:** Directly relevant to KmprZ Stage 1. Works on games already mounted via ShadowMountPlus.

### Convertidor-Pro
- **URL:** https://github.com/TheWizWikii/Convertidor-Pro
- **Author:** TheWizWikii
- **Variant:** org
- **Desc:** PC automation suite (RedumpScraper ecosystem) for decrypting, converting, compressing and optimizing game backups — aimed at both emulation and real hardware.
- **Tags:** #tool #compression #conversion #pc #redump
- **Notes:** Spanish-language project; useful offline prep pipeline before pushing dumps to PS5.

### ps5-custom-payloads
- **URL:** https://github.com/TheWizWikii/ps5-custom-payloads
- **Author:** TheWizWikii
- **Variant:** org
- **Desc:** Custom payload source repo intended for PS5 Payload Manager (multiple sources support).
- **Tags:** #mirror #catalog #payload #P5U #pldmgr
- **Notes:** Add via Payload Manager → Manage Sources (QR / URL).

### PS5-Repository-List
- **URL:** https://github.com/nexgen999/PS5-Repository-List
- **Author:** nexgen999
- **Variant:** org
- **Desc:** Curated list of PS5 repositories / scene resources.
- **Tags:** #mirror #catalog #links #P5U
- **Notes:** Good discovery index alongside PS5LinkCentalizer.

### ps5-app-dumper
- **URL:** https://github.com/EchoStretch/ps5-app-dumper
- **Author:** EchoStretch
- **Variant:** org
- **Desc:** Utility to dump application files from the console’s pfsmnt to a connected USB device.
- **Tags:** #dumper #payload #P5U #usb #echostretch
- **Notes:** Also available as built-in overlay inside Prospero-Menu.

### apr-emu-updater
- **URL:** https://github.com/tsuramatsu1/apr-emu-updater
- **Author:** tsuramatsu1
- **Variant:** org
- **Desc:** PS5 payload that keeps APR Emu up to date on installed titles, managed from a web interface on the console.
- **Tags:** #emu #updater #webui #payload #P5U
- **Notes:** Targets APR emulator patches on installed games.

### PS5-Stuff
- **URL:** https://github.com/TheWizWikii/PS5-Stuff
- **Author:** TheWizWikii
- **Variant:** org
- **Desc:** Collection of BD-JB ISOs, payloads and related PS5 tools/releases.
- **Tags:** #mirror #payload #bdj #P5U #collection
- **Notes:** Useful grab-bag of scene releases.

### phantomptr/ps5upload
- **URL:** (none)
- **Author:** 
- **Variant:** org
- **Desc:** Upload tooling referenced in KmprZ credits.
- **Tags:** #transfer #tool #P5U
- **Notes:** Related to the ps5upload entry.

## From the Store

### etaHEN
- **URL:** https://github.com/etaHEN/etaHEN
- **Author:** EchoStretch / LightningMods
- **Variant:** EchoStretch
- **Desc:** 
- **Tags:** #payload
- **Notes:** Fast-moving mainline. Normal retention -- newer builds may carry an expiry timestamp (_ExpiYYYYMMDD).

### CheatRunner
- **URL:** https://github.com/notmaj0r/CheatRunner
- **Author:** notmaj0r
- **Variant:** org
- **Desc:** 
- **Tags:** #payload
- **Notes:** unset -- fill in from release notes

### elfldr
- **URL:** https://github.com/itsPLK/ps5-elfldr
- **Author:** itsPLK
- **Variant:** itsPLK
- **Desc:** 
- **Tags:** #payload
- **Notes:** unset -- fill in from release notes

### PoorDS4
- **URL:** https://github.com/ItsBlurf/PoorDS4
- **Author:** ItsBlurf
- **Variant:** org
- **Desc:** 
- **Tags:** #payload
- **Notes:** sibling tool -- see docs/rename-map.md

### Self Decrypter: Full System
- **URL:** https://github.com/idlesauce/PS5-SELF-Decrypter
- **Author:** idlesauce
- **Variant:** org
- **Desc:** 
- **Tags:** #payload
- **Notes:** sibling tool -- see docs/rename-map.md

### GarlicSaves
- **URL:** https://git.etawen.dev/earthonion/garlic-savemgr
- **Author:** earthonion
- **Variant:** org
- **Desc:** 
- **Tags:** #payload
- **Notes:** separate tool from garlic-worker, shared prefix only | Not on GitHub (Forgejo host): listed only. Add direct_url + version once you have a file link, then remove fetch:false.

### Garlic Worker
- **URL:** https://git.etawen.dev/earthonion/garlic-worker
- **Author:** earthonion
- **Variant:** org
- **Desc:** 
- **Tags:** #payload
- **Notes:** separate tool from garlic-savemgr, shared prefix only | Not on GitHub (Forgejo host): listed only. Add direct_url + version once you have a file link, then remove fetch:false.

### HWInfo Bench
- **URL:** https://github.com/drakmor/ps5-hwinfo
- **Author:** drakmor
- **Variant:** org
- **Desc:** 
- **Tags:** #payload
- **Notes:** separate tool from hwinfo-sysinfo, shared prefix only

### onionHEN
- **URL:** https://github.com/aydencharles/onionHEN
- **Author:** aydencharles
- **Variant:** org
- **Desc:** 
- **Tags:** #payload
- **Notes:** unset -- fill in from release notes

### ProsperoMgr
- **URL:** https://github.com/notmaj0r/ProsperoMgr
- **Author:** notmaj0r
- **Variant:** org
- **Desc:** 
- **Tags:** #payload
- **Notes:** All-in-one PS5 manager -- files, transfers, PKG installer, save backups, payload autoloader.

### JailbreakStore
- **URL:** https://github.com/notmaj0r/JailbreakStore
- **Author:** notmaj0r
- **Variant:** org
- **Desc:** 
- **Tags:** #payload
- **Notes:** unset -- fill in from release notes

### ChronicLoader
- **URL:** https://github.com/StonedModder/ChronicLoader-PS5-Payload
- **Author:** StonedModder
- **Variant:** org
- **Desc:** 
- **Tags:** #payload
- **Notes:** PS5 payload updater/autoloader -- downloads from configured GitHub releases and writes autoload.txt. Same repo as the ChronicLoader entry; kept for old file names.

### PS5Library Agent
- **URL:** https://github.com/rdiol12/PS5Library
- **Author:** rdiol12
- **Variant:** org
- **Desc:** 
- **Tags:** #payload
- **Notes:** Console-side agent ELF for the PS5Library native storefront. Pairs with PS5Library.pkg. Provides the on-console backend that the storefront UI talks to. GPL-3.0.

### PS5 PKG Manager
- **URL:** https://github.com/itsPLK/ps5-pkg-manager
- **Author:** itsPLK
- **Variant:** org
- **Desc:** 
- **Tags:** #payload
- **Notes:** Console-side PKG browser and installer (pkgmgr.elf). Scans USB and SMB shares for PKG files and installs them directly on the PS5. GPL-3.0.

### FGG Unpack
- **URL:** https://github.com/FGGstore/FGG-Unpack
- **Author:** FGGstore
- **Variant:** org
- **Desc:** 
- **Tags:** #payload
- **Notes:** Background watcher ELF that auto-extracts .zip and .7z archives uploaded via FTP, in-place. Great for uploading compressed game folders. Ships with .elf.json for pldmgr. GPL-3.0.

### ELF Launcher
- **URL:** https://github.com/X-F1REBALL-X/elf-launcher
- **Author:** X-F1REBALL-X
- **Variant:** org
- **Desc:** 
- **Tags:** #payload
- **Notes:** Home screen tile + browser UI for sending ELF payloads to the PS5 (elfldr on port 9021). Serves launcher at port 1000. Companion to wk-autoloader. FOSS.

### WK-AutoLoader
- **URL:** https://github.com/X-F1REBALL-X/WK-AutoLoader
- **Author:** X-F1REBALL-X
- **Variant:** org
- **Desc:** 
- **Tags:** #payload
- **Notes:** WebKit-based jailbreak loader UI on port 1022. Supports FW 1.xx-5.xx, 7.00-12.00, 12.02-12.70. installer.elf. GPL-3.0.
