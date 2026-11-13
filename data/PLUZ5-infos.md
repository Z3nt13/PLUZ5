# PLUZ5 Library

_Powered By Z3nT13's PLUZ5. Generated from `PLUZ5-infos.json`; edit it with `web/library.html`. Block format: `docs/BLOCK-FORMAT.md`._

## Payload Senders / Managers (PC & Web)

### PlayStation Payload Center
- **URL:** https://github.com/Pharaoh2k/PlayStation-Payload-Center
- **By:** Pharaoh2k
- **Desc:** Cross-platform Avalonia/.NET desktop tool. Discover consoles, browse payload catalogs, SHA-256 verify, queue, and stream payloads to jailbroken PS4/PS5.
- **Tags:** #Network - #tool #catalog #queue #sha256 #avalonia
- **Extras:** P5U | sender
- **Notes:** UDP discovery (PS4:987, PS5:9302). Common send ports 9020/9021.

### ps5-payload-manager
- **URL:** https://github.com/itsPLK/ps5-payload-manager
- **By:** itsPLK
- **Desc:** Modern web-based dashboard that runs on the PS5 itself. Manage, import, and auto-load payloads. Homescreen shortcut support.
- **Tags:** #System-Utility - #manager #webui #autoload #itsplk
- **Extras:** P5U | payload | .elf
- **Notes:** Can be set as only entry in autoload.txt.

### PayLoader / ps5-payloader
- **URL:** https://github.com/Marice/ps5-payloader
- **By:** Marice
- **Desc:** Native PS5 homebrew app (title `PPSA67670`) — controller front-end for Payload Manager (pldmgr). Manage payloads, repositories, autoload/boot chain, and running processes on the TV without a browser. Also covers Signal suite install and USB recovery copy.
- **Tags:** #System-Utility - #manager #autoload #pldmgr
- **Extras:** P5U | app | port:8084,9021
- **Notes:** Needs pldmgr ≥0.6.0 (talks on `127.0.0.1:8084`); ships its own pldmgr copy and can start it via ELF loader 9021. Install folder to `/data/homebrew/PPSA67670`. First release v00.001.000. Build: `PayLoader-Marice_v00.001.000`.

### PKG Sender
- **URL:** https://github.com/Loopayeh/pkg-sender
- **By:** Loopayeh
- **Desc:** LAN PKG installer for PS4/PS5. Auto-find console, queue installs. No USB needed. Ships `pkg-receiver.elf` for PS5.
- **Tags:** #Network - #pkg #tool
- **Extras:** P5U | sender | port:12800
- **Notes:** PS5 uses pkg-receiver.elf on port 12800. PS4 uses Remote Package Installer or GoldHEN.

### PS5-4-Payload-Sender-Android
- **URL:** https://github.com/PixelPop25/PS5-4-Payload-Sender-Android
- **By:** PixelPop25
- **Desc:** Simple Android TCP payload injector. Supports .bin / .elf / .lua / .js / .jar.
- **Tags:** #Network - #mobile
- **Extras:** P5U | sender
- **Notes:** Keep mobile data off so traffic stays on LAN.

### PS5AutopayloadHA
- **URL:** https://github.com/cosmicflow2512/PS5AutopayloadHA
- **By:** cosmicflow2512
- **Desc:** Home Assistant add-on that fully automates the post-exploit payload chain (send / delay / wait-for-port flows).
- **Tags:** #Network - #automation #autoload
- **Extras:** P5U | sender
- **Notes:** Supports multiple loaders (9021, 9025, 9026, 50000…).

### web-based-ps-package-manager
- **URL:** https://github.com/h-haghpanah/web-based-ps-package-manager
- **By:** h-haghpanah
- **Desc:** Browser tool for managing and sending packages to PS4 and PS5.
- **Tags:** #Network - #pkg #webui
- **Extras:** P5U | sender
- **Notes:** PS5 side can use ps5_file_downloader (8283) or pkg_receiver (12800).

### Send-Payload-to-PS
- **URL:** https://github.com/Master-s/Send-Payload-to-PS
- **By:** Master-s
- **Desc:** Multi-platform payload sender including iOS support.
- **Tags:** #Network
- **Extras:** P5U | sender
- **Notes:** Has PC and iOS components.

## Core Payload Infrastructure (PS5)

### ps5-payload-dev/sdk
- **URL:** https://github.com/ps5-payload-dev/sdk
- **By:** ps5-payload-dev
- **Desc:** SDK for developing PS5 payloads using dynamic linking. Works with elfldr, websrv, BD-J, remote_lua_loader, etc.
- **Tags:** #Debug-SDK - #sdk #ps5-payload-dev #elf
- **Extras:** P5U | tool
- **Notes:** Install to `/opt/ps5-payload-sdk`. Essential for building native payloads.

### ps5-payload-dev/websrv
- **URL:** https://github.com/ps5-payload-dev/websrv
- **By:** ps5-payload-dev
- **Desc:** Simple web server payload (port 8080). Launch homebrew and ELF payloads from the PS5 browser or remotely.
- **Tags:** #System-Utility - #webui #ps5-payload-dev
- **Extras:** P5U | payload | .elf | port:8080
- **Notes:** Looks for homebrew under `/data/homebrew`, USB, and external storage.

### ps5-payload-dev/elfldr
- **URL:** https://github.com/ps5-payload-dev/elfldr
- **By:** ps5-payload-dev
- **Desc:** ELF loader for jailbroken PS5s. Accepts payloads on port 9021.
- **Tags:** #System-Utility - #loader #elfdir #ps5-payload-dev
- **Extras:** P5U | payload | .elf | port:9021
- **Notes:** Primary target for ZendRz and most PC senders.

### ps5-payload-dev/ftpsrv
- **URL:** https://github.com/ps5-payload-dev/ftpsrv
- **By:** ps5-payload-dev
- **Desc:** FTP server for jailbroken PS4 and PS5.
- **Tags:** #Network - #ftp #ps5-payload-dev
- **Extras:** P5U | payload | .elf | port:2121
- **Notes:** Common companion after HEN.

### zftpd
- **URL:** https://github.com/seregonwar/zftpd
- **By:** seregonwar
- **Desc:** Zero-copy high-performance FTP/HTTP daemon (C11). Saturates Gigabit (~117 MB/s). Linux/macOS/Windows + **PS4/PS5 payloads**; optional ZHTTP browser file explorer. On-screen IP/port notification on console.
- **Tags:** #File-Management - #ftp #http #file-manager #webui #tool
- **Extras:** P5U | payload | .elf | port:2121,8888
- **Notes:** Default FTP **-p 2121** (fallback range 2120–2129 if busy). ZHTTP often **8888**. Control/teardown `127.0.0.1:28888`. Latest **v1.7.0**. Binary: `zftpd-seregonwar` / `zftpd-ps5[-zhttp]-v1.7.0.elf`.

### ps5-payload-dev/fetchpkg
- **URL:** https://github.com/ps5-payload-dev/fetchpkg
- **By:** ps5-payload-dev
- **Desc:** Fetch PS4/PS5 package updates referenced by a JSON-formatted manifest URL.
- **Tags:** #System-Utility - #pkg #tool #ps5-payload-dev
- **Extras:** P5U | payload | .elf
- **Notes:** Useful for update pipelines.

### etaHEN / forks
- **URL:** (none)
- **By:** MasterPS0
- **Desc:** AIO HEN + toolbox for jailbroken PS5. Debug settings replacement, plugins, rest mode options, etc.
- **Tags:** #Kernel - #hen #toolbox #etahen
- **Extras:** P5U | payload | .elf
- **Notes:** Many tools assume etaHEN or compatible environment is running.

### onionHEN / OnionBuddies
- **URL:** https://github.com/orgs/OnionBuddies/repositories
- **By:** OnionBuddies
- **Desc:** Modular HEN ecosystem (plugins, WebUI, external plugin support) — successor/modular direction beyond classic single-blob HENs.
- **Tags:** #Kernel - #hen #onionhen #toolbox #modular
- **Extras:** P5U | payload | .elf
- **Notes:** Org hosts plugin SDK, DPI plugin, boilerplate, etc. Classic onionHEN builds still mirrored in itsPLK payloads-mirror.

### onionHEN DPI v2 plugin
- **URL:** https://github.com/OnionBuddies/onionHEN-dpiv2-plugin
- **By:** OnionBuddies
- **Desc:** OnionHEN plugin: receives PS4/PS5 `.pkg` over LAN, stages on console, submits to system installer. Embedded WebUI; browser is primary installer UI. XML page limited to start/stop and ports.
- **Tags:** #Kernel - #hen #pkg #dpi #plugin #webui
- **Extras:** P5U | tool | .elf | port:9090,12800
- **Notes:** Install as `/data/OnionHEN/plugins/DPIV00001.elf`. Default WebUI `http://<ps5-ip>:12800`, API TCP 9090. No separate runtime assets. Binary: `dpiv2-OnionBuddies.elf`.

### PIZZA-HEN
- **URL:** https://github.com/Michele-M-Media/PIZZA-HEN
- **By:** Michele-M-Media
- **Desc:** Experimental all-in-one PS5 homebrew environment with its own integration layer, Toolbox, service chain, and branding (builds on upstream open-source projects).
- **Tags:** #Kernel - #hen #toolbox #aio
- **Extras:** P5U | payload | .elf
- **Notes:** v2.00 public source checkpoint. Maintained by Michele Media.

### ShadowMountPlus
- **URL:** https://github.com/drakmor/ShadowMountPlus
- **By:** drakmor
- **Desc:** Automated background auto-mounter for jailbroken PS5. Detects, mounts, and installs game backups from internal/external storage. Supports UFS, exFAT, PFS, and nested compressed PFS containers.
- **Tags:** #Game-Tools - #mount #shadowmount #automation #drakmor
- **Extras:** P5U | payload | .elf
- **Notes:** Core for game library / KmprZ workflows. Very widely used.

### kstuff-lite
- **URL:** https://github.com/EchoStretch/kstuff-lite
- **By:** EchoStretch
- **Desc:** Lite kstuff build – crypto, FSELF, NPDRM, loader work. Optimized UELF/KELF transitions and diagnostics.
- **Tags:** #Kernel - #kstuff #echostretch #fself
- **Extras:** P5U | payload | .elf
- **Notes:** Popular base; many forks exist (including drakmor).

### kstuff-lite
- **URL:** https://github.com/drakmor/kstuff-lite
- **By:** drakmor
- **Desc:** drakmor fork of kstuff-lite with improved fpkg/FSELF handling, faster startup and internal optimizations.
- **Tags:** #Kernel - #kstuff #drakmor #fself
- **Extras:** P5U | payload | fork:EchoStretch | .elf
- **Notes:** Alternative optimized build.

### nanoDNS
- **URL:** https://github.com/drakmor/nanoDNS
- **By:** drakmor
- **Desc:** PlayStation 4/5 DNS proxy server.
- **Tags:** #Network - #dns #tool #drakmor
- **Extras:** P5U | payload | .elf
- **Notes:** Local DNS proxy useful for blocking/redirecting Sony endpoints.

### ampr_emu
- **URL:** https://github.com/drakmor/ampr_emu
- **By:** drakmor
- **Desc:** AMPR userland emulation.
- **Tags:** #Game-Tools - #emu #drakmor
- **Extras:** P5U | payload | .elf
- **Notes:** Public beta; Discord linked from repo.

### BackPork
- **URL:** https://github.com/BestPig/BackPork
- **By:** BestPig
- **Desc:** Lets you sideload system libraries into PS5 games.
- **Tags:** #System-Utility - #sideload #library #bestpig
- **Extras:** P5U | payload | .elf
- **Notes:** Useful for advanced game patching / library injection.

### ps5debug-NG
- **URL:** https://github.com/EchoStretch/ps5debug-NG
- **By:** EchoStretch
- **Desc:** PS5 debugger payload – userland TCP wire-protocol server hosted inside SceShellCore.
- **Tags:** #Debug-SDK - #debug #echostretch
- **Extras:** P5U | payload | .elf
- **Notes:** GPL-3. For development / reverse engineering.

### PS5 Account Activator
- **URL:** https://github.com/Epinorr/ps5-account-activator
- **By:** Epinorr
- **Desc:** All-in-one ELF that combines offline account activation + NP Fake Signin in a single execution. Idempotent, region-aware, clean on-screen notifications.
- **Tags:** #Activation-Spoof - #activator #account #np
- **Extras:** P5U | payload | .elf | port:9021
- **Notes:** Send to the foreground user on port 9021. Binary: `AIO-Activator-Epinorr_v2.1.0.elf` (upstream ships as `AIO-Activator.elf`). Skips steps already done. Latest v2.1.0.

### np-fake-signin
- **URL:** https://github.com/earthonion/np-fake-signin
- **By:** earthonion
- **Desc:** Sets PSN state to "signed in" on PS4/PS5. Standalone NP fake sign-in (also folded into Account Activator AIO builds).
- **Tags:** #Activation-Spoof - #np #account
- **Extras:** P5U | payload | .elf
- **Notes:** Primary GitHub home for the payload.

### ps5-account-tools
- **URL:** https://github.com/MangoScango/ps5-account-tools
- **By:** MangoScango
- **Desc:** Web UI (port 6769) to manage local PS5 accounts — offline activation + fake PSN sign-in in one place, plus local profile avatar change. Enables Remote Play pairing (Chiaki / Px Play).
- **Tags:** #Activation-Spoof - #account #activator #np #webui #remote-play
- **Extras:** P5U | payload | .elf | port:6769
- **Notes:** After activation, note Account IDs, reboot, then pair remote play. Pair with nanoDNS to keep PSN blocked.

### ps5-fw-spoof
- **URL:** https://github.com/illusionyy/ps5-fw-spoof
- **By:** illusionyy
- **Desc:** Patch PS4 SDK + PS5 Update version in kernel data to `99.99` without hardcoded offsets.
- **Tags:** #Activation-Spoof - #spoof #firmware
- **Extras:** P5U | payload | .elf
- **Notes:** Version spoof helper for tools that gate on FW/SDK version. Binary: `ps5-fw-spoof-illusionyy.elf`.

### ps-patch-system
- **URL:** https://github.com/illusionyy/ps-patch-system
- **By:** illusionyy
- **Desc:** App patching system for PS4/PS5. Local HTTP UI on port **23900**; applies user XML patches (PS-Game-Patch format) to eboot/(s)elf; can patch shellcore to mount `/data` in sandbox. PS5 Media-tab “Keep in Home” shortcut.
- **Tags:** #Game-Tools - #patches #cheats #webui #illusionyy
- **Extras:** P5U | payload | .elf | port:23900
- **Notes:** Send `patch-bundle-loader-prospero.elf` (PS5) or `…-orbis.elf` (PS4) to elfldr :9021. XMLs from [PS-Game-Patch](https://github.com/illusionyy/PS-Game-Patch) → `/data/user/patches` (`xml_prospero` / `xml_orbis`). Pairs with CheatRunner. Binary: `ps-patch-system-illusionyy`. Web: `http://<ps5-ip>:23900`. Related: NeoEnabler (https://github.com/gasb07/NeoEnabler) depends on this (load order: patch-system first).

### NeoEnabler
- **URL:** https://github.com/gasb07/NeoEnabler
- **By:** gasb07
- **Desc:** Run PS4 games on PS5 in **PS4 Pro mode** at higher resolutions (up to native 4K). Requires **ps-patch-system** loaded first. Auto Pro mode / optional 8 GiB memory budget for patched titles; GPU clock boost (1800–2200 MHz) on FW 13.20/13.60. Web panel + Media shortcut.
- **Tags:** #Game-Tools - #patches #webui #neo #resolution #gpu
- **Extras:** P5U | payload | .elf | port:8765
- **Notes:** Load order every boot: **ps-patch-system → neo-manager.elf** (9021). Panel `http://<ps5-ip>:8765`. Patches synced into `/data/user/patches/xml_orbis/`. 8 GiB without HV on 13.20/13.60 (validated paths). Logs `/data/neo-enabler/`. Latest **~0.5.0**. Binary: `NeoEnabler-gasb07` / `neo-manager.elf`.

### ps5-self-pager
- **URL:** https://github.com/idlesauce/ps5-self-pager
- **By:** idlesauce
- **Desc:** PS5 SELF decryptor (“yet another PS5 SELF decryptor”).
- **Tags:** #Debug-SDK - #tool #decrypt #self #dev
- **Extras:** P5U | tool
- **Notes:** Development / reverse-engineering utility.

### WelcomeHubActivator
- **URL:** https://github.com/ghost1372/WelcomeHubActivator
- **By:** ghost1372
- **Desc:** Activates the PS5 Welcome Hub / first-party tile path for homebrew-friendly setups.
- **Tags:** #Activation-Spoof - #activator #welcome-hub
- **Extras:** P5U | payload | .elf
- **Notes:** One-shot; persists across reboots. Binary: `WelcomeHubActivator-ghost1372_v1.0.0.elf`. Backs up `app.db` → `app.bckdb` before edit.

### ddd_status
- **URL:** https://github.com/earthonion/ddd_status
- **By:** earthonion
- **Desc:** PS5 status / diagnostic helper in the earthonion toolkit family.
- **Tags:** #Debug-SDK - #diagnostic #earthonion
- **Extras:** P5U | payload | .elf

### kdump_ps5
- **URL:** https://github.com/earthonion/kdump_ps5
- **By:** earthonion
- **Desc:** Kernel dump utility for jailbroken PS5.
- **Tags:** #Debug-SDK - #debug #kdump #earthonion
- **Extras:** P5U | payload | .elf

### garlic-savemgr
- **URL:** https://github.com/earthonion/garlic-savemgr
- **By:** earthonion
- **Desc:** Local PS5 save manager — decrypt/encrypt/browse with embedded web UI.
- **Tags:** #Game-Tools - #saves #webui #earthonion
- **Extras:** P5U | payload | .elf | port:8082
- **Notes:** Send to elfldr; open `http://<ps5-ip>:8082`. Binary: `garlic-savemgr-earthonion_v1.7.elf`.

### PS5-Power-Payloads-Project
- **URL:** https://github.com/MasterPS0/PS5-Power-Payloads-Project
- **By:** MasterPS0
- **Desc:** Reboot / power-off / suspend payloads for PS5.
- **Tags:** #System-Utility - #power #reboot
- **Extras:** P5U | payload | .elf
- **Notes:** Binaries: `reboot-MasterPS0.elf`, `poweroff-MasterPS0.elf`, `suspend-MasterPS0.elf`.

### ps5upload
- **URL:** https://github.com/phantomptr/ps5upload
- **By:** phantomptr
- **Desc:** Fast resumable transfer of games, apps, homebrew, folders, disk images, and archives to a jailbroken PS5 over AVA1 (port 9120). Installs PS4/PS5 packages; file browser and console management from desktop, Android, or browser. FW 1.00–13.60.
- **Tags:** #Network - #tool #transfer #upload #pkg #webui
- **Extras:** P5U | tool | fw:100-1360 | port:9120
- **Notes:** Client on macOS/Linux/Windows/Android + web. Latest **v7.1.9**. Binary/app: `PS5Upload-phantomptr_v7.1.9`.

### ProsperoMgr
- **URL:** https://github.com/notmaj0r/ProsperoMgr
- **By:** notmaj0r
- **Desc:** Web-based all-in-one PS5 manager (single ELF). File manager, ZIP/RAR, payload library, PKG queue, saves, autoloader, thermal/fan. Dashboard port 7070.
- **Tags:** #Game-Tools - #manager #webui #file-manager #pkg #saves #autoload #notmaj0r
- **Extras:** P5U | payload | .elf | port:7070
- **Notes:** `http://<ps5-ip>:7070`. Binary: `ProsperoMgr-notmaj0r.elf`.

### CheatRunner
- **URL:** https://github.com/notmaj0r/CheatRunner
- **By:** notmaj0r
- **Desc:** Web-based PS5 cheat trainer. Games library, .mc4/.shn/.json, PS-Game-Patch XML, autoload profiles. Dashboard port 9999.
- **Tags:** #Game-Tools - #cheats #trainer #webui #notmaj0r
- **Extras:** P5U | payload | .elf | port:9999
- **Notes:** Related: https://github.com/notmaj0r/CheatRunner_Patches. Binary: `CheatRunner-notmaj0r.elf`.

### CheatRunner_Patches
- **URL:** https://github.com/notmaj0r/CheatRunner_Patches
- **By:** notmaj0r
- **Desc:** Patch collections for CheatRunner (xml / xml_prospero).
- **Tags:** #Game-Tools - #cheats #patches #notmaj0r
- **Extras:** P5U | tool

### PatchDL / ps5-patchdl
- **URL:** https://github.com/knutwurst/ps5-patchdl
- **By:** knutwurst
- **Desc:** PS5 payload that lists installed disc/PSN games and downloads official game **updates** from Sony (multi-connection, resume, optional checksum). FW 1.00–13.60. Web UI; optional home-screen tile. Does not download full games or system software.
- **Tags:** #Game-Tools - #pkg #updater #patch #webui
- **Extras:** P5U | payload | .elf | fw:100-1360 | port:12880
- **Notes:** Open `http://<ps5-ip>:12880/`. Version history via prosperopatches.com / orbispatches.com. Latest **v0.3.12**. Binary: `patchdl-knutwurst_v0.3.12.elf`.

### ps5-pkg-manager
- **URL:** https://github.com/itsPLK/ps5-pkg-manager
- **By:** itsPLK
- **Desc:** Package manager for PS5 — USB or Samba/SMB, multi-part packages, direct install from PC. Web UI port 8844.
- **Tags:** #File-Management - #pkg #manager #webui #smb #usb #itsplk
- **Extras:** P5U | payload | .elf | port:8844
- **Notes:** Binary: `ps5-pkg-manager-itsPLK.elf`.

### JailbreakStore
- **URL:** https://github.com/notmaj0r/JailbreakStore
- **By:** notmaj0r
- **Desc:** Payload that rebrands the PlayStation Store tile (NPXS40047) into a custom launcher.
- **Tags:** #Media - #homescreen #notmaj0r
- **Extras:** P5U | store | .elf
- **Notes:** ⚠ DB edits can corrupt PS4 FPKGs. Binary: `JailbreakStore-notmaj0r.elf`.

### ps5-firmware-pin
- **URL:** https://github.com/lvndry/ps5-firmware-pin
- **By:** lvndry
- **Desc:** PC Python tools to pin/unpin PS5 firmware and USB downgrade helper. Tested on 13.60 (Relapse).
- **Tags:** #System-Utility - #tool #firmware #pin #shsrv
- **Extras:** P5U | tool
- **Notes:** Pin needs jailbreak + shsrv on 2323.

### PS5-NetDis
- **URL:** https://github.com/eladharels/PS5-NetDis
- **By:** eladharels
- **Desc:** Network diagnostics / port-availability helper for jailbroken PS5.
- **Tags:** #Debug-SDK - #network #diagnostic #webui
- **Extras:** P5U | payload | .elf | port:8070,9021
- **Notes:** UI at `http://<ps5-ip>:8070`. Binary: `NetDis-eladharels_v1.0.0.elf`.

### App Title
- **URL:** https://github.com/porhe911/App-Title
- **By:** porhe911
- **Desc:** Standalone ELF that shows game/app title IDs on the home screen. Media → App Title settings.
- **Tags:** #Media - #homescreen #visual #title-id #media
- **Extras:** P5U | payload | .elf
- **Notes:** Config `/data/AppTitle/`. Latest **v0.2.8**. Binary: `App_Title-porhe911_v0.2.8.elf`.

## Autoloaders / Exploit Loaders

### ps5-webkit-autoloader
- **URL:** https://github.com/itsPLK/ps5-webkit-autoloader
- **By:** itsPLK
- **Desc:** Automated WebKit-path payload loader. Supports FW 7.00–13.60.
- **Tags:** #System-Utility - #autoload #loader #webkit #itsplk
- **Extras:** P5U | tool | fw:700-1360
- **Notes:** Community note: v0.5.0 can feel faster than v0.6.1 on some FW (e.g. PS5 Pro 11.40).

### ps5-bdjb-autoloader
- **URL:** https://github.com/itsPLK/ps5-bdjb-autoloader
- **By:** itsPLK
- **Desc:** Automated BD-J path payload loader.
- **Tags:** #System-Utility - #autoload #loader #bdj #itsplk
- **Extras:** P5U | tool

### ps5-lua-autoloader
- **URL:** https://github.com/itsPLK/ps5-lua-autoloader
- **By:** itsPLK
- **Desc:** Automated payload and Lua script loader.
- **Tags:** #System-Utility - #autoload #loader #lua #itsplk
- **Extras:** P5U | tool

### ps5-y2jb-autoloader
- **URL:** https://github.com/itsPLK/ps5-y2jb-autoloader
- **By:** itsPLK
- **Desc:** Automated Y2JB-path payload loader.
- **Tags:** #System-Utility - #autoload #loader #y2jb #itsplk
- **Extras:** P5U | exploit

### P2JB-Y2JB-Porting
- **URL:** https://github.com/matem6/P2JB-Y2JB-Porting
- **By:** matem6
- **Desc:** PS5 jailbreak via Y2JB; ports Gezine’s p2jb kqueueex work.
- **Tags:** #Kernel - #y2jb #jailbreak
- **Extras:** P5U | exploit

### Luac0re
- **URL:** https://github.com/Gezine/Luac0re
- **By:** Gezine
- **Desc:** mast1c0re variation using Lua scripting.
- **Tags:** #Debug-SDK - #lua #mast1c0re #dev
- **Extras:** P5U | exploit

### mast1c0re
- **URL:** https://github.com/McCaulay/mast1c0re
- **By:** McCaulay
- **Desc:** Payloads via game save file on PS4/PS5.
- **Tags:** #Debug-SDK - #mast1c0re #save #dev
- **Extras:** P5U | exploit
- **Notes:** Docs: https://cturt.github.io/mast1c0re.html

### Y2JB-installer
- **URL:** https://github.com/dakotadawolfe/Y2JB-installer
- **By:** dakotadawolfe
- **Desc:** Standalone ELF that installs YouTube + official Y2JB Autoloader image on **PS5 FW 13.60**. Writes/verifies `download0.dat`, completion notification. Targets US YouTube `PPSA01650` v01.000.030.
- **Tags:** #System-Utility - #autoload #y2jb #installer
- **Extras:** P5U | exploit | .elf | fw:1360
- **Notes:** Privileged session required; ≥2 GiB free; close YouTube first. Backups under `/data/y2jb-installer/`. Credits Gezine Y2JB, itsPLK autoloader, jamesst20 installer bits. Latest **v2.0.0** (console validation pending). Binary: `Y2JB-installer-dakotadawolfe_v2.0.0.elf`.

### PS5-Super-PLDMGR-Auto-Updater
- **URL:** https://github.com/nexgen999/PS5-Super-PLDMGR-Auto-Updater
- **By:** nexgen999
- **Desc:** Auto-updater focused on the PS5 Payload Manager ecosystem.
- **Tags:** #Game-Tools - #tool #autoload #updater #pldmgr
- **Extras:** P5U | tool

## File Managers / Web UIs

### ps5-web-file-manager
- **URL:** https://github.com/owendswang/ps5-web-file-manager
- **By:** owendswang
- **Desc:** File manager for PS5 with a web UI.
- **Tags:** #File-Management - #file-manager #webui
- **Extras:** P5U | payload | .elf

### BFpilot
- **URL:** https://github.com/ItsBlurf/BFpilot
- **By:** ItsBlurf
- **Desc:** Lightweight browser-based PS5 file manager.
- **Tags:** #File-Management - #file-manager #webui
- **Extras:** P5U | payload | .elf

## Overlays / Menus / System UI

### Prospero-Menu
- **URL:** https://github.com/StonedModder/Prospero-Menu
- **By:** StonedModder
- **Desc:** Expandable Tesla-style overlay system for jailbroken PS5. Drop-in `.ovl` or JSON menus.
- **Tags:** #Debug-SDK - #overlay #menu #tesla #fan-control #boot-anim #elfdir #games #dumper #stonedmodder
- **Extras:** P5U | tool
- **Notes:** Overlays in `/data/ProsperoMenu/overlays/`.

## Themes / Home Screen / Visual

### LiveShell
- **URL:** https://github.com/ZiZc3/LiveShell
- **By:** ZiZc3
- **Desc:** Animated video wallpapers for the PS5 home screen (LiveShell Engine). Discover catalog, per-game/app videos, PS Store-only mode, playlists, sound, Dim/Vignette/Haze, parallax, rest-mode resume, home-screen app + phone/PC control. H.264/HEVC up to 4K.
- **Tags:** #Media - #theme #wallpaper #homescreen #video #visual #webui #media
- **Extras:** P5U | app | .elf
- **Notes:** Load `liveshell.elf`. Videos `/data/LiveShell/video` or USB `liveshell/`. Pause while games run (decoder). Latest **v1.7.0**. Binary: `LiveShell-ZiZc3_v1.7.0` / `liveshell.elf`.

### ThemeChanger
- **URL:** https://github.com/Yahballon/ThemeChanger
- **By:** Yahballon
- **Desc:** Native wallpaper manager (`PPSA99891`). MotionBGS / LiveShell; Signal Companion for LED colours/effects.
- **Tags:** #Media - #theme #wallpaper #homescreen #video #liveshell #signal #led
- **Extras:** P5U | app
- **Notes:** Latest **v0.3.24**. Build: `ThemeChanger-Yahballon_v0.3.24`.

## Media / Players

### PS-Play
- **URL:** https://github.com/MounirHero/PS-Play
- **By:** MounirHero
- **Desc:** All-in-one media hub — DLNA, Stremio, IPTV, USB playback. AMOLED-black UI.
- **Tags:** #Media - #media #player #dlna #stremio #iptv
- **Extras:** P5U | app

## Linux / Dual-boot

### ps5-linux-1240-build
- **URL:** https://github.com/Wigglez-sudo/ps5-linux-1240-build
- **By:** Wigglez-sudo
- **Desc:** Linux loader for **PS5 firmware 12.40** with GPU/display up. Ubuntu image on USB/SSD; one arm per boot.
- **Tags:** #Linux - #linux #loader
- **Extras:** P5 | payload | .elf | fw:1240
- **Notes:** `loader-1240-7ed8615b.elf`. Image: ps5-ubuntu2604.img.xz.

## Emulators / Ports

### EglantinePS5
- **URL:** https://github.com/heydemoura/EglantinePS5
- **By:** heydemoura
- **Desc:** Unofficial PS5 homebrew port of **Eglantine** (Switch 2–capable Eden fork). Early alpha — video/audio/controller/saves working; experimental local multiplayer. Same native stack as ProsperoEden (boilerplate + ps5-opengl / Mesa Vulkan).
- **Tags:** #Game-Tools - #emulator #eden #eglantine
- **Extras:** P5U | app
- **Notes:** Not affiliated with Eglantine/Eden/Sony. Related to ProsperoEden lineage. Current release **v1.000.000**. Build: `EglantinePS5-heydemoura_v1.000.000`.

### ProsperoEden
- **URL:** https://github.com/Swordpdf/ProsperoEden
- **By:** Swordpdf
- **Desc:** Unofficial PS5 port of the Eden emulator. Early alpha; per-game folders (roms/DLC/mods/cheats).
- **Tags:** #Game-Tools - #emulator #eden
- **Extras:** P5U | app
- **Notes:** Latest alpha **v1.005.000**. Build: `ProsperoEden-Swordpdf_v1.005.000`.

### ampr-emu-ng
- **URL:** https://github.com/quer3q/ampr-emu-ng
- **By:** quer3q
- **Desc:** AMPR emulation sprx, fork of drakmor/ampr_emu, for use with ShadowMountPlus.
- **Tags:** #Game-Tools - #tool #ampr
- **Extras:** P5U | tool | .sprx | port:9090
- **Notes:** Binary: `ampr_emu.sprx`. Needs ShadowMountPlus. Port 9090 is debug only.

## Stores / Download Managers

### ProsperoStore
- **URL:** https://github.com/darkxex/ProsperoStore
- **By:** darkxex
- **Desc:** Native PS5 app store (title `PPSA99000`) for prosperostore.net / homebrew.page catalog.
- **Tags:** #Game-Tools - #shadowmount #catalog
- **Extras:** P5U | store | port:9021
- **Notes:** Needs ShadowMountPlus ≥1.7beta4. Build: `ProsperoStore-darkxex_v1.000.100`.

### ps5shopappkg
- **URL:** https://github.com/ps5xploit/ps5shopappkg
- **By:** ps5xploit
- **Desc:** Browser-based PS5 homebrew/APPKG shop (ps5shopappkg.pages.dev). DPI v2 port 12800. Max FW 13.60.
- **Tags:** #Game-Tools - #webui #pkg
- **Extras:** P5U | store | port:12800

### Orbit Store
- **URL:** https://github.com/saawant12/orbit-store-ps5
- **By:** saawant12
- **Desc:** Modern PS5 download manager (~1600 games). Native TV app + Orbit Zero (desktop). Archive.org / Vikingfile / AkiraBox.
- **Tags:** #Game-Tools - #download-manager #webui #shadowmount
- **Extras:** P5U | store
- **Notes:** Latest beta ~v1.3.5. Build: `OrbitStore-saawant12_v1.3.5`.

### Jobee'sLair / JobeesLair
- **URL:** https://github.com/JVK3R/JobeesLair
- **By:** JVK3R
- **Desc:** PS5 homebrew game store. ShadowMount+ required.
- **Tags:** #Game-Tools - #download-manager #shadowmount
- **Extras:** P5U | store
- **Notes:** Latest v0.4.1. Build: `JobeesLair-JVK3R_v0.4.1`.

### Overdrive
- **URL:** https://github.com/MyLuxy/overdrive
- **By:** MyLuxy
- **Desc:** Open rebuild of the Overdrive game store (~1800+ games); also installs prosperostore.net homebrew.
- **Tags:** #Game-Tools - #download-manager #shadowmount #catalog
- **Extras:** P5U | store
- **Notes:** Related: https://github.com/overdriveps5/overdrive-releases (`PPSA99058`). Build: `Overdrive-MyLuxy_v1.0.7`.

### overdrive-releases
- **URL:** https://github.com/overdriveps5/overdrive-releases
- **By:** overdriveps5
- **Desc:** Official binary release channel for Overdrive (`Overdrive-PPSA99058.exfat.zip`).
- **Tags:** #Game-Tools - #releases #mirror
- **Extras:** P5U | store

### BlackBox
- **URL:** https://github.com/D3ATHLY/blackbox
- **By:** D3ATHLY
- **Desc:** PS5 homebrew storefront / download manager. Install via `PPSA01453.ffpkg` + ShadowMount.
- **Tags:** #Game-Tools - #download-manager #shadowmount #catalog
- **Extras:** P5U | store | .elf
- **Notes:** ⚠ Do not load `blackbox.elf` via Payload Manager. ~1.12.0.

### RecompStore
- **URL:** https://github.com/elripalda/RecompStore
- **By:** elripalda
- **Desc:** Store for native ports of recompiled games. Bring your own disc.
- **Tags:** #Game-Tools - #recomp
- **Extras:** P5U | store
- **Notes:** Build: `RecompStore-elripalda`.

### Spela
- **URL:** https://github.com/ensamvarg360/spela
- **By:** ensamvarg360
- **Desc:** Self-hosted storefront for **your own** PS5 backups. PC catalog + LAN install via ShadowMount+; optional home-screen app.
- **Tags:** #Game-Tools - #download-manager #shadowmount #backup
- **Extras:** P5U | store
- **Notes:** Latest **v0.7.3**. Build: `Spela-ensamvarg360_v0.7.3`.

### RemotePFS
- **URL:** https://github.com/PSBrew/RemotePFS
- **By:** PSBrew
- **Desc:** Linux SBC service emulating exFAT USB OTG from a remote NAS for ShadowMountPlus.
- **Tags:** #Game-Tools - #tool #mount #pfs #shadowmount #nas #psbrew
- **Extras:** P5U | tool

## Payload Mirrors & Catalogs

### theghostonline.dev
- **URL:** https://theghostonline.dev
- **By:** theghostonline
- **Desc:** Homebrew hub — apps, PSVR2, on-console HITMAN/007 servers, Nuvio PS5.
- **Tags:** #Media - #hub #homebrew #media #psvr2 #nuvio
- **Extras:** P5U | reference

### ps5-payloads-mirror
- **URL:** https://github.com/itsPLK/ps5-payloads-mirror
- **By:** itsPLK
- **Desc:** Automated mirror of useful PS5 payloads with version tracking.
- **Tags:** #System-Utility - #mirror #catalog #itsplk
- **Extras:** P5U | payload | .elf

### PS5LinkCentalizer
- **URL:** https://github.com/pedrohti/PS5LinkCentalizer
- **By:** pedrohti
- **Desc:** Community link hub; auto-updates project data from GitHub.
- **Tags:** #System-Utility - #mirror #catalog #links
- **Extras:** P5U | reference

### zecoxao.github.io
- **URL:** https://github.com/zecoxao/zecoxao.github.io
- **By:** zecoxao
- **Desc:** Historical PS scene sites and tools archive.
- **Tags:** #File-Management - #mirror #archive #historical
- **Extras:** P5 | reference

### PS5-Repository-List
- **URL:** https://github.com/nexgen999/PS5-Repository-List
- **By:** nexgen999
- **Desc:** Curated list of PS5 repositories / scene resources.
- **Tags:** #System-Utility - #mirror #catalog #links
- **Extras:** P5U | reference

### PS5-Stuff
- **URL:** https://github.com/TheWizWikii/PS5-Stuff
- **By:** TheWizWikii
- **Desc:** Collection of BD-JB ISOs, payloads and related tools.
- **Tags:** #System-Utility - #mirror #bdj #collection
- **Extras:** P5U | payload | .elf

### ps5-custom-payloads
- **URL:** https://github.com/TheWizWikii/ps5-custom-payloads
- **By:** TheWizWikii
- **Desc:** Custom payload sources for PS5 Payload Manager.
- **Tags:** #System-Utility - #mirror #catalog #pldmgr
- **Extras:** P5U | payload | .elf

## Game / Library / Compression (KmprZ relevance)

### Alembic
- **URL:** https://github.com/fthdgn-gh/Alembic
- **By:** fthdgn-gh
- **Desc:** Convert PS5/PS4 games between debug FPKG, fake PKG, dump folders, exFAT, FFPKG (UFS2), FFPFS (PFS), FFPFSC (compressed PFS). Console **home-screen app** (from 0.3.0) or payload web UI + PC CLI/engine. Network pairing (convert on PC → write to console); SMB/NFS/WebDAV/FTP; AMPR/LZ4 for PS5; streaming, no temp copies.
- **Tags:** #Game-Tools - #tool #compression #pfs #pkg #exfat #ffpkg #kmprz #webui #ampr #shadowmount
- **Extras:** P5U | app
- **Notes:** Highly relevant to KmprZ. Byte-identical refs: PS5PKGTool / MkPFS / LibOrbisPkg. Self-updates via Payload Manager. WIP — back up before converting. Latest **v0.5.1**. Binary/app: `Alembic-fthdgn-gh_v0.5.1`.

### ps5-dump-forge
- **URL:** https://github.com/quer3q/ps5-dump-forge
- **By:** quer3q
- **Desc:** Cross-platform PS5 dump toolkit (PS5 payload + Win/macOS/Linux app/CLI). Convert/edit folders, exFAT, FFPKG, FFPFS, FFPFSC, FPKG; read zip/7z/rar; pack assets to **zstd** or LZ4; library + file explorer; on-the-fly convert between devices (SMB/FTP/NFS); PKG install on paired console.
- **Tags:** #Game-Tools - #tool #compression #pkg #exfat #ffpkg #ffpfsc #zstd #lz4 #kmprz #webui #transfer
- **Extras:** P5U | tool | .elf
- **Notes:** Strong KmprZ-adjacent peer to Alembic / Dump-Image-Converter. UI in 11 languages. Payload `ps5-dump-forge-<ver>-ps5.elf` → 9021. Latest **v0.5.4**. Scene note: ZSTD packs discussed e.g. [Techjunkie_Aman](https://x.com/Techjunkie_Aman/status/2118918691228426752) (with ampr-emu-ng).

### ps5-zstd-toml-generator
- **URL:** https://github.com/giusepper11/ps5-zstd-toml-generator
- **By:** giusepper11
- **Desc:** PC tool that builds a custom **Zstd** compression profile (`profile.toml`) from an extracted PS5 game dump. Intended for use with **ps5-dump-forge** Pack → Custom rules (TOML).
- **Tags:** #File-Management - #tool #compression #zstd #kmprz #toml #profile
- **Extras:** tool
- **Notes:** Windows x64 portable ZIP (`Start-Generator.cmd`). Outputs `profile.toml`, `report.txt`, `decisions.tsv`. Pairs with dump-forge / ampr-style asset packs. Latest prerelease **v0.3.2**. Build: `ps5-zstd-toml-generator-giusepper11_v0.3.2`.

### PS5 Dump & Image Converter
- **URL:** https://github.com/strongt1me/PS5-Dump-Image-Converter
- **By:** strongt1me
- **Desc:** Desktop suite (Win/Linux/macOS) — convert/validate dumps, PKG/FPKG, AMPR EMU & BACKPORT, console helpers.
- **Tags:** #Game-Tools - #tool #compression #pkg #exfat #ffpkg #ffpfsc #ampr #kmprz
- **Extras:** P5U | sender
- **Notes:** Latest **v1.9.84**.

### MkPFS
- **URL:** https://github.com/PSBrew/MkPFS
- **By:** PSBrew
- **Desc:** Build PFS images from loose game files (`sce_sys/param.json`).
- **Tags:** #File-Management - #tool #pfs #compression #kmprz #param-json
- **Extras:** P5U | tool

### PS5-Game-Compressor
- **URL:** https://github.com/juma-sayeh/PS5-Game-Compressor
- **By:** juma-sayeh
- **Desc:** Payload for compressing/unpacking/validating/repairing ShadowMountPlus-mounted games.
- **Tags:** #Game-Tools - #compression #shadowmount #kmprz #tool
- **Extras:** P5U | payload | .elf

### Lazy_AMPR
- **URL:** https://github.com/Nazky/Lazy_AMPR
- **By:** Nazky
- **Desc:** Desktop GUI to build/extract AMPR LZ4 asset packs (Win/Linux/macOS).
- **Tags:** #File-Management - #tool #compression #ampr #lz4 #kmprz
- **Extras:** P5U | tool

### pkg-viewer
- **URL:** https://github.com/Loopayeh/pkg-viewer
- **By:** Loopayeh
- **Desc:** PC tool to inspect PS2–PS5 / Switch packages and images without extracting.
- **Tags:** #File-Management - #tool #pkg #viewer #kmprz #loopayeh
- **Extras:** P5U | tool
- **Notes:** Supports `.pkg`, `.exfat`, `.ffpfsc`, `.ffpkg`. ~v1.7.5.

### Convertidor-Pro
- **URL:** https://github.com/TheWizWikii/Convertidor-Pro
- **By:** TheWizWikii
- **Desc:** PC suite for decrypting, converting, compressing game backups.
- **Tags:** #File-Management - #tool #compression #conversion #redump
- **Extras:** tool

### ps5-app-dumper
- **URL:** https://github.com/EchoStretch/ps5-app-dumper
- **By:** EchoStretch
- **Desc:** Dump application files from pfsmnt to USB.
- **Tags:** #Debug-SDK - #dumper #usb #echostretch
- **Extras:** P5U | payload | .elf

### apr-emu-updater
- **URL:** https://github.com/tsuramatsu1/apr-emu-updater
- **By:** tsuramatsu1
- **Desc:** Keeps APR Emu up to date on installed titles via console web UI.
- **Tags:** #Game-Tools - #emu #updater #webui
- **Extras:** P5U | payload | .elf

### packizard
- **URL:** https://x.com/packizard
- **By:** packizard
- **Desc:** Announced new compression format for PS5 dumps (not fully released yet).
- **Tags:** #File-Management - #compression #wip #kmprz
- **Extras:** P5U | tool

## WebKit / Exploit Hosts

### nexgen999 ps5webkit host
- **URL:** https://nexgen999.github.io/ps5webkit/
- **By:** nexgen999
- **Desc:** Self-hosted WebKit exploit / payload loading page.
- **Tags:** #System-Utility - #webkit #host #autoload
- **Extras:** P5U | exploit

### ps4macedo ps51360 host
- **URL:** https://ps4macedo.github.io/ps51360/
- **By:** ps4macedo
- **Desc:** WebKit/host page oriented at PS5 firmware 13.60.
- **Tags:** #Kernel - #webkit #host
- **Extras:** P5U | exploit | fw:1360
