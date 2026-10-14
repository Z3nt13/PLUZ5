# Rename Map

PLUZ never renames binaries automatically ("unknown is better than wrong").
Do these by hand on disk before running `pluz-merge --apply` if you want
these files recognized cleanly. Every new name below has a matching entry
in `configs/payload_registry.json`.

## Explicit dual-track variants

| Current filename | New filename |
|---|---|
| `etaHEN_v2.6B.elf` (or similar bare EchoStretch build) | `etaHEN-EchoStretch_v2.6B.elf` |
| `etaHEN-Zecoxao_v2.6B.elf` | *(already correct)* |
| `ShadowMountPlus_v1.6beta16.elf` | `ShadowMountPlus-Beta_v1.6beta16.elf` |
| `ShadowMountPlus_v1.7alpha6.elf` (or newer alpha you grab) | `ShadowMountPlus-Alpha_v1.7alpha9.elf` (use whatever alpha you actually have) |

## Sibling-tool families (were wrongly shaped like versions/variants)

| Current filename | Recommended new filename |
|---|---|
| `fan_target_70c_v0.1.elf` | `fan-target-70c_v0.1.elf` |
| `fan_target_75c_v0.1.elf` | `fan-target-75c_v0.1.elf` |
| `fan_target_80c_v0.1.elf` | `fan-target-80c_v0.1.elf` |
| `ps5power-notify_test_v1.0.elf` | `ps5power-notify_v1.0.elf` |
| `PoorDS4rc38_v0.1.0-rc38.elf` | `poords4-rc_v0.1.0-rc38.elf` |
| `PoorDS4-status_v0.1.0-rc38.elf` | `poords4-status_v0.1.0-rc38.elf` |
| `PoorDS4-stop_v0.1.0-rc38.elf` | `poords4-stop_v0.1.0-rc38.elf` |
| `hwinfo_bench_v0.1.elf` | `hwinfo-bench_v0.1.elf` |
| `hwinfo_sysinfo_v0.1.elf` | `hwinfo-sysinfo_v0.1.elf` |

Already-fine as-is (registry matches): `ps5power-poweroff/reboot/suspend`,
all 4 `ps5-self-decrypter-*`, all 4 `ps5-self-pager-*`, `garlic-savemgr`,
`garlic-worker`.

## Malformed filenames (won't parse at all as-is)

| Current filename | Problem | Recommended new filename |
|---|---|---|
| `ftpsrv_v1.15-ng (stable.elf` | stray space + unmatched `(` | `ftpsrv_v1.15-ng.elf` (put "stable" in the registry `channel` field, not the filename) |
| `ftpsrv_drakmor_v1.6-ng-test2.elf` | underscore before `drakmor` instead of a hyphen -- reads as one unbroken name segment, won't resolve to the `ftpsrv` payload + `drakmor` variant | `ftpsrv-drakmor_v1.6-ng-test2.elf` |

## Not a distributable payload -- don't force it into the registry

`zerodaysofficial/ps5-exfat-pkg-builder-v1` is a PC-side PKG-building toolkit (like `mkpfs` for `.ffpfsc`), not something that ships an `.elf`/`.bin`/`.pkg` release of its own to catalog. Worth linking from docs as a reference tool, but it doesn't belong in `payload_registry.json` or `pkg_registry.json` -- there's no artifact for `pluz-merge` to actually pick up.

| `kylin-core-comm.-lite_vv131-global-release.elf` | double "v", periods in name | `kylin-core-comm-lite_v131.elf` (note "global-release" in registry `note`) |
| `PS5-File-Explorer_vfile-explorer-v0.2.1.elf` | version string duplicated | `PS5-File-Explorer_v0.2.1.elf` |
| `PS5-Custom-Tool-Manager-_vCustom.elf` | "Custom" isn't a version | rename once you know the real version, or use `v0.0.0` + a note explaining there's no versioned release |
| `ps5-fw-spoof_v26616621599.elf` | looks like a Unix timestamp | confirm the real version from the source repo, keep the number as a build-id note instead |

## Possible true duplicates (confirm with `pluz-dedupe` before deleting anything)

| Files | What to check |
|---|---|
| `websrv_v0.34.elf` vs `webSRV-ps5_v0.34.elf` | Run `pluz-dedupe` — matching SHA-256 means identical, keep one. |
| `zftp_v1.5.0.bin` vs `zftp_v1.5.0.elf` | Same check — could be two formats of one release (keep both) or coincidentally identical. |
| `zhttp_v1.5.0.bin` vs `zhttp_v1.5.0.elf` | Same as above. |

## PKG filenames

Official Sony-style PKGs (content-id filenames like
`UP6312-PPSA18654_00-0220083948426038_sc.pkg`) don't follow the scene
`{payload}-{variant}_v{version}.ext` convention and the parser won't
match them. For those, you'll need a future manual-lookup path keyed by
exact filename rather than a rename — not built yet, flagged in
`pluz_pkg.py`'s unresolved list if you drop one in `pkgs/` as-is.
