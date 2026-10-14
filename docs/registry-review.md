# Registry review (2026-10-13)

Two different `payload_registry.json` snapshots were uploaded: an older one (42 identities, matching the 2026-09-18 GamePlan) and a
newer 'session3' one (32 identities). They are different lineages, not old/new versions of each other. The live registry is the
**older one** (vetted, follows the documented stable+fast pattern) plus 5 additions that earlier sessions documented.
Nothing was deleted: everything left out is preserved below for you to accept or reject.

## Added to the live registry from session3

- `ps5library-agent`
- `ps5-pkg-manager`
- `fgg-unpack`
- `elf-launcher`
- `wk-autoloader`

## Conflicts on the same (identity, variant) -- old value kept

### CheatRunner / RDX
VERIFIED: github.com/notmaj0r/CheatRunner exists (not a fork, 115 stars). github.com/LightningMods/CheatRunner could not be found. Kept the old values.

| field | old (kept) | session3 |
|---|---|---|
| author | notmaj0r | LightningMods |
| author_url | https://github.com/notmaj0r | https://github.com/LightningMods |
| display_name | CheatRunner (RDX fork) | CheatRunner (RDX) |
| note | unset -- fill in from release notes | In-game cheat trainer / code injector. |
| source_repo | https://github.com/notmaj0r/CheatRunner | https://github.com/LightningMods/CheatRunner |

### ShadowMountPlus / Beta
VERIFIED: github.com/drakmor/ShadowMountPlus exists (726 stars, GPL-3.0). github.com/shadermount/ShadowMountPlus could not be found. Kept the old values, including protected_fallback=true (the documented stable+fast pattern).

| field | old (kept) | session3 |
|---|---|---|
| author | drakmor | shadermount |
| author_url | https://github.com/drakmor | https://github.com/shadermount |
| category | Game Tools | File Management |
| note | Slower-moving, more-tested track. Always kept regardless of retention count. | USB/BD ISO mount helper. |
| protected_fallback | True | False |
| source_repo | https://github.com/drakmor/ShadowMountPlus | https://github.com/shadermount/ShadowMountPlus |

### etaHEN / Zecoxao
Not verified. Old value kept.

| field | old (kept) | session3 |
|---|---|---|
| note | No expiry timer. More stable on FW 11.40 than current EchoStretch beta. Permanen | No expiry timer. More stable on FW 11.40 than current EchoStretch beta. Permanen |

### kstuff / default
PARTLY CHECKED: github.com/ps5-payload-dev/kstuff exists but is archived (2025-04-07) with no description or releases, so it is NOT confirmed to be the vanilla build the old note refers to. Kept 'unset'.

| field | old (kept) | session3 |
|---|---|---|
| author | unset | ps5-payload-dev |
| author_url | None | https://github.com/ps5-payload-dev |
| note | Vanilla/original kstuff build referenced by kstuff_v1.09.elf -- source not confi | Kernel stuff payload for PS5 jailbreak. |
| source_repo | unset -- not yet confirmed | https://github.com/ps5-payload-dev/kstuff |

### websrv / default
Not verified. Old value kept.

| field | old (kept) | session3 |
|---|---|---|
| display_name | websrv | Web Server (ps5-payload-dev) |
| note | Confirm websrv_v0.34.elf and webSRV-ps5_v0.34.elf via dedupe before keeping both | Simple HTTP server payload for PS5. Serves files from /data/ over HTTP. |

### zftp / itsPLK
COULD NOT VERIFY: github.com/itsPLK/zftp could not be fetched. Old entry says attribution unconfirmed, so it stays unset (also port 21 vs 2121 unresolved).

| field | old (kept) | session3 |
|---|---|---|
| author | unset -- attribution unconfirmed, do not guess | itsPLK |
| author_url | None | https://github.com/itsPLK |
| display_name | zftp | zftp (itsPLK) |
| note | Naming/attribution not yet verified -- leave for the future scraper/discovery en | FTP server payload. Serves the PS5 filesystem over FTP on port 2121. |
| port | 21 | 2121 |
| source_repo | unset -- attribution unconfirmed, do not guess (see docs/rename-map.md) | https://github.com/itsPLK/zftp |

## Session3-only entries NOT added to the live registry

Full JSON for each is in the block at the end of this file.

- `AnyPS5` -- contradicts an earlier decision: PC-side relinker (runs PS5 executables on Linux/Windows), not a console payload; flagged as a reference, unassigned
- `BinLoader` -- not verified in this review (fields may be guesses) -- confirm source/author/category before adding
- `etaHEN-cheat` -- contradicts an earlier decision: PS5_etaHEN_Cheat_Repository was checked earlier and ruled NOT registry material (per-game cheat content, not a homebrew tool)
- `fan-target` -- overlaps existing identity 'fan-target-70c/75c/80c' -- decide which naming to keep
- `mira` -- not verified in this review (fields may be guesses) -- confirm source/author/category before adding
- `ps5-dumper` -- not verified in this review (fields may be guesses) -- confirm source/author/category before adding
- `ps5-elfldr` -- overlaps existing identity 'elfldr' -- decide which naming to keep
- `ps5-fw-spoof` -- not verified in this review (fields may be guesses) -- confirm source/author/category before adding
- `ps5-gdbstub` -- not verified in this review (fields may be guesses) -- confirm source/author/category before adding
- `ps5-hen` -- not verified in this review (fields may be guesses) -- confirm source/author/category before adding
- `ps5-klog` -- not verified in this review (fields may be guesses) -- confirm source/author/category before adding
- `ps5-linux` -- not verified in this review (fields may be guesses) -- confirm source/author/category before adding
- `ps5-mtrr` -- not verified in this review (fields may be guesses) -- confirm source/author/category before adding
- `ps5-notify` -- not verified in this review (fields may be guesses) -- confirm source/author/category before adding
- `ps5-payload-dl` -- not verified in this review (fields may be guesses) -- confirm source/author/category before adding
- `ps5-reboot` -- not verified in this review (fields may be guesses) -- confirm source/author/category before adding
- `ps5-self-decrypter` -- overlaps existing identity 'ps5-self-decrypter-full-system/-game/-shellcore/-system-common-lib' -- decide which naming to keep
- `ps5-shutdown` -- not verified in this review (fields may be guesses) -- confirm source/author/category before adding
- `ps5-sysex` -- not verified in this review (fields may be guesses) -- confirm source/author/category before adding
- `ps5-uart` -- not verified in this review (fields may be guesses) -- confirm source/author/category before adding
- `zftpd` -- not verified in this review (fields may be guesses) -- confirm source/author/category before adding

## PKG registry

Union of both: PS5Webkit, PS5Library.

## Full JSON of the entries held back

```json
{
  "AnyPS5": {
    "variants": {
      "boykopovar": {
        "display_name": "AnyPS5 (boykopovar)",
        "source_repo": "https://github.com/boykopovar/AnyPS5",
        "author": "boykopovar",
        "author_url": "https://github.com/boykopovar",
        "backup_url": null,
        "category": "Network",
        "channel": "stable",
        "fw_min": null,
        "fw_max": null,
        "port": null,
        "protected_fallback": false,
        "note": "Cross-platform payload sender and exploit helper."
      }
    }
  },
  "BinLoader": {
    "variants": {
      "default": {
        "display_name": "BinLoader",
        "source_repo": "https://github.com/ps5-payload-dev/binloader",
        "author": "ps5-payload-dev",
        "author_url": "https://github.com/ps5-payload-dev",
        "backup_url": null,
        "category": "Network",
        "channel": "stable",
        "fw_min": null,
        "fw_max": null,
        "port": 9021,
        "protected_fallback": false,
        "note": "ELF/BIN loader, listens on port 9021 for incoming payloads."
      }
    }
  },
  "etaHEN-cheat": {
    "variants": {
      "default": {
        "display_name": "etaHEN Cheat Loader",
        "source_repo": "https://github.com/spfi970/PS5_etaHEN_Cheat_Repository",
        "author": "spfi970",
        "author_url": "https://github.com/spfi970",
        "backup_url": null,
        "category": "Game Tools",
        "channel": "stable",
        "fw_min": null,
        "fw_max": null,
        "port": null,
        "protected_fallback": false,
        "note": "Cheat/trainer repository companion to etaHEN."
      }
    }
  },
  "fan-target": {
    "variants": {
      "70c": {
        "display_name": "Fan Target 70\u00b0C",
        "source_repo": "https://github.com/ps5-payload-dev/fan-target",
        "author": "ps5-payload-dev",
        "author_url": "https://github.com/ps5-payload-dev",
        "backup_url": null,
        "category": "System Utility",
        "channel": "stable",
        "fw_min": null,
        "fw_max": null,
        "port": null,
        "protected_fallback": false,
        "note": "Sets fan target temperature to 70\u00b0C."
      }
    }
  },
  "mira": {
    "variants": {
      "default": {
        "display_name": "Mira",
        "source_repo": "https://github.com/OpenOrbis/mira-project",
        "author": "OpenOrbis",
        "author_url": "https://github.com/OpenOrbis",
        "backup_url": null,
        "category": "Kernel",
        "channel": "stable",
        "fw_min": "5.05",
        "fw_max": "9.00",
        "port": null,
        "protected_fallback": false,
        "note": "OpenOrbis kernel framework."
      }
    }
  },
  "ps5-dumper": {
    "variants": {
      "default": {
        "display_name": "PS5 Dumper",
        "source_repo": "https://github.com/ps5-payload-dev/dumper",
        "author": "ps5-payload-dev",
        "author_url": "https://github.com/ps5-payload-dev",
        "backup_url": null,
        "category": "Debug & SDK",
        "channel": "stable",
        "fw_min": null,
        "fw_max": null,
        "port": null,
        "protected_fallback": false,
        "note": "Process/memory dumper."
      }
    }
  },
  "ps5-elfldr": {
    "variants": {
      "default": {
        "display_name": "elfldr (ps5-payload-dev)",
        "source_repo": "https://github.com/ps5-payload-dev/elfldr",
        "author": "ps5-payload-dev",
        "author_url": "https://github.com/ps5-payload-dev",
        "backup_url": null,
        "category": "Debug & SDK",
        "channel": "stable",
        "fw_min": null,
        "fw_max": null,
        "port": 9021,
        "protected_fallback": false,
        "note": "Minimal ELF loader. Replaces pwnldr. Listens on port 9021."
      }
    }
  },
  "ps5-fw-spoof": {
    "variants": {
      "default": {
        "display_name": "PS5 FW Spoof",
        "source_repo": "https://github.com/LightningMods/ps5-fw-spoof",
        "author": "LightningMods",
        "author_url": "https://github.com/LightningMods",
        "backup_url": null,
        "category": "Activation & Spoof",
        "channel": "stable",
        "fw_min": null,
        "fw_max": null,
        "port": null,
        "protected_fallback": false,
        "note": "Firmware version spoofer payload."
      }
    }
  },
  "ps5-gdbstub": {
    "variants": {
      "default": {
        "display_name": "PS5 GDB Stub",
        "source_repo": "https://github.com/ps5-payload-dev/gdbstub",
        "author": "ps5-payload-dev",
        "author_url": "https://github.com/ps5-payload-dev",
        "backup_url": null,
        "category": "Debug & SDK",
        "channel": "stable",
        "fw_min": null,
        "fw_max": null,
        "port": 2159,
        "protected_fallback": false,
        "note": "GDB remote stub for PS5. Connects on port 2159."
      }
    }
  },
  "ps5-hen": {
    "variants": {
      "default": {
        "display_name": "PS5 HEN",
        "source_repo": "https://github.com/sleirsgoevy/ps4jb",
        "author": "sleirsgoevy",
        "author_url": "https://github.com/sleirsgoevy",
        "backup_url": null,
        "category": "Kernel",
        "channel": "stable",
        "fw_min": "4.03",
        "fw_max": "9.60",
        "port": null,
        "protected_fallback": false,
        "note": "Homebrew enabler for PS5."
      }
    }
  },
  "ps5-klog": {
    "variants": {
      "default": {
        "display_name": "PS5 Kernel Logger",
        "source_repo": "https://github.com/ps5-payload-dev/klog",
        "author": "ps5-payload-dev",
        "author_url": "https://github.com/ps5-payload-dev",
        "backup_url": null,
        "category": "System Utility",
        "channel": "stable",
        "fw_min": null,
        "fw_max": null,
        "port": null,
        "protected_fallback": false,
        "note": "Kernel log forwarder."
      }
    }
  },
  "ps5-linux": {
    "variants": {
      "default": {
        "display_name": "PS5 Linux Loader",
        "source_repo": "https://github.com/ps5-payload-dev/linuxloader",
        "author": "ps5-payload-dev",
        "author_url": "https://github.com/ps5-payload-dev",
        "backup_url": null,
        "category": "Linux",
        "channel": "stable",
        "fw_min": null,
        "fw_max": null,
        "port": null,
        "protected_fallback": false,
        "note": "Boots a Linux kernel on the PS5."
      }
    }
  },
  "ps5-mtrr": {
    "variants": {
      "default": {
        "display_name": "PS5 MTRR Fixer",
        "source_repo": "https://github.com/ps5-payload-dev/mtrr",
        "author": "ps5-payload-dev",
        "author_url": "https://github.com/ps5-payload-dev",
        "backup_url": null,
        "category": "System Utility",
        "channel": "stable",
        "fw_min": null,
        "fw_max": null,
        "port": null,
        "protected_fallback": false,
        "note": "Memory Type Range Register fixer."
      }
    }
  },
  "ps5-notify": {
    "variants": {
      "default": {
        "display_name": "PS5 Notify",
        "source_repo": "https://github.com/ps5-payload-dev/notify",
        "author": "ps5-payload-dev",
        "author_url": "https://github.com/ps5-payload-dev",
        "backup_url": null,
        "category": "System Utility",
        "channel": "stable",
        "fw_min": null,
        "fw_max": null,
        "port": null,
        "protected_fallback": false,
        "note": "Sends a notification message to the PS5 screen."
      }
    }
  },
  "ps5-payload-dl": {
    "variants": {
      "default": {
        "display_name": "PS5 Payload Downloader",
        "source_repo": "https://github.com/ps5-payload-dev/dl",
        "author": "ps5-payload-dev",
        "author_url": "https://github.com/ps5-payload-dev",
        "backup_url": null,
        "category": "File Management",
        "channel": "stable",
        "fw_min": null,
        "fw_max": null,
        "port": null,
        "protected_fallback": false,
        "note": "Payload downloader / file fetch helper."
      }
    }
  },
  "ps5-reboot": {
    "variants": {
      "default": {
        "display_name": "PS5 Reboot Payload",
        "source_repo": "https://github.com/ps5-payload-dev/reboot",
        "author": "ps5-payload-dev",
        "author_url": "https://github.com/ps5-payload-dev",
        "backup_url": null,
        "category": "System Utility",
        "channel": "stable",
        "fw_min": null,
        "fw_max": null,
        "port": null,
        "protected_fallback": false,
        "note": "Reboots the PS5."
      }
    }
  },
  "ps5-self-decrypter": {
    "variants": {
      "full-system": {
        "display_name": "PS5 SELF Decrypter (Full System)",
        "source_repo": "https://github.com/ps5-payload-dev/selfdecrypter",
        "author": "ps5-payload-dev",
        "author_url": "https://github.com/ps5-payload-dev",
        "backup_url": null,
        "category": "Debug & SDK",
        "channel": "stable",
        "fw_min": null,
        "fw_max": null,
        "port": null,
        "protected_fallback": false,
        "note": "Decrypts SELF files from the PS5 system partition."
      }
    }
  },
  "ps5-shutdown": {
    "variants": {
      "default": {
        "display_name": "PS5 Shutdown Payload",
        "source_repo": "https://github.com/ps5-payload-dev/shutdown",
        "author": "ps5-payload-dev",
        "author_url": "https://github.com/ps5-payload-dev",
        "backup_url": null,
        "category": "System Utility",
        "channel": "stable",
        "fw_min": null,
        "fw_max": null,
        "port": null,
        "protected_fallback": false,
        "note": "Shuts down the PS5."
      }
    }
  },
  "ps5-sysex": {
    "variants": {
      "default": {
        "display_name": "PS5 sysex",
        "source_repo": "https://github.com/ps5-payload-dev/sysex",
        "author": "ps5-payload-dev",
        "author_url": "https://github.com/ps5-payload-dev",
        "backup_url": null,
        "category": "Debug & SDK",
        "channel": "stable",
        "fw_min": null,
        "fw_max": null,
        "port": null,
        "protected_fallback": false,
        "note": "System exception handler / crash reporter."
      }
    }
  },
  "ps5-uart": {
    "variants": {
      "default": {
        "display_name": "PS5 UART Logger",
        "source_repo": "https://github.com/ps5-payload-dev/uart",
        "author": "ps5-payload-dev",
        "author_url": "https://github.com/ps5-payload-dev",
        "backup_url": null,
        "category": "System Utility",
        "channel": "stable",
        "fw_min": null,
        "fw_max": null,
        "port": null,
        "protected_fallback": false,
        "note": "UART debug logger."
      }
    }
  },
  "zftpd": {
    "variants": {
      "seregonwar": {
        "display_name": "zftpd (seregonwar)",
        "source_repo": "https://github.com/seregonwar/zftpd",
        "author": "seregonwar",
        "author_url": "https://github.com/seregonwar",
        "backup_url": null,
        "category": "Network",
        "channel": "stable",
        "fw_min": null,
        "fw_max": null,
        "port": 2121,
        "protected_fallback": false,
        "note": "FTP daemon payload for PS5."
      }
    }
  }
}
```
