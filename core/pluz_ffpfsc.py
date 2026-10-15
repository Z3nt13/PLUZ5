"""
pluz_ffpfsc.py -- regenerates PLUZ5-ffpfsc.json from whatever is currently
in ffpfsc/, using configs/ffpfsc_registry.json for metadata.

The ffpfsc category covers three subtypes (see ffpfsc_registry.json comment):
  compressor_tool  -- ELF/BIN that runs on the PS5, compresses/decompresses games
  helper_elf       -- supporting ELF utilities for ffpfsc content
  compressed_file  -- actual .ffpfsc/.ffpkg/.fpkg images (metadata only, not hosted)

Supported file extensions in ffpfsc/: .elf, .bin, .ffpfsc, .ffpkg, .fpkg
All must still follow the standard naming convention:
  {identity}[-{variant}]_v{version}[_Expi{YYYYMMDD}].{ext}

No network access.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pluz_common import (  # noqa: E402
    repo_root, load_env, load_config, parse_filename_raw, resolve_identity,
    sha256_file, version_sort_key, FFPFSC_EXTS, BINARY_EXTS, Log,
)

FFPFSC_ALL_EXTS = FFPFSC_EXTS | BINARY_EXTS  # ELF/BIN tools live here too


def build_url(gh_user: str, gh_repo: str, gh_branch: str, filename: str) -> str:
    return f"https://raw.githubusercontent.com/{gh_user}/{gh_repo}/{gh_branch}/ffpfsc/{filename}"


def make_ffpfsc_entry(
    identity: str,
    variant: str,
    artifact: dict,
    reg: dict,
    env: dict,
    retention_tag: str,
) -> dict:
    url = build_url(env["GH_USER"], env["GH_REPO"], env["GH_BRANCH"], artifact["filename"])
    display_name = reg.get(
        "display_name",
        identity if variant == "default" else f"{identity} ({variant})",
    )

    desc_bits = []
    fw_min, fw_max = reg.get("fw_min"), reg.get("fw_max")
    if fw_min or fw_max:
        desc_bits.append(f"FW {fw_min or '?'}-{fw_max or '?'}")
    if artifact.get("expiry"):
        e = artifact["expiry"]
        desc_bits.append(f"expires {e[:4]}-{e[4:6]}-{e[6:]}")
    if reg.get("note") and not desc_bits:
        desc_bits.append(reg["note"])
    description = " -- ".join(desc_bits) if desc_bits else ""

    return {
        "name": display_name,
        "filename": artifact["filename"],
        "url": url,
        "backup_url": reg.get("backup_url"),
        "description": description,
        "version": artifact["version"],
        "ffpfsc_type": reg.get("ffpfsc_type", "helper_elf"),
        "fw_min": fw_min,
        "fw_max": fw_max,
        "platform": reg.get("platform", "ps5"),
        "hw_target": reg.get("hw_target"),
        "category": reg.get("category", "Unknown"),
        "author": reg.get("author"),
        "author_url": reg.get("author_url"),
        "checksum": artifact["sha256"],
        "retention": retention_tag,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(prog="pluz ffpfsc")
    ap.parse_args(argv)

    root = repo_root()
    log = Log(root, "pluz_ffpfsc")
    cfg = load_config(root)
    env = load_env(root)

    missing_env = [k for k in ("GH_USER", "GH_REPO", "GH_BRANCH") if not env.get(k)]
    if missing_env:
        log.line(f"[ERROR] missing required .env values: {', '.join(missing_env)}")
        log.line("Run 'check' and fill in .env before generating manifests.")
        return 1

    ffpfsc_dir = root / cfg["settings"]["paths"].get("ffpfsc", "ffpfsc")
    if not ffpfsc_dir.is_dir():
        log.line(f"ffpfsc/ directory not found at {ffpfsc_dir} -- creating it.")
        ffpfsc_dir.mkdir(parents=True, exist_ok=True)

    registry = cfg["ffpfsc_registry"].get("entries", {})
    if not registry:
        log.line("[WARN] ffpfsc_registry.json has no entries yet -- manifest will be empty.")

    retention = cfg["settings"].get("ffpfsc_retention", {"hosted_keep": 3})
    hosted_keep = retention["hosted_keep"]
    retention_labels = ["current", "previous", "previous-2", "previous-3", "previous-4"]

    files = [
        p for p in ffpfsc_dir.iterdir()
        if p.is_file() and p.suffix.lstrip(".").lower() in FFPFSC_ALL_EXTS
    ]
    log.line(f"Scanning {len(files)} file(s) in {ffpfsc_dir}")

    groups: dict = defaultdict(list)
    unresolved = []

    for f in sorted(files, key=lambda p: p.name):
        parsed = parse_filename_raw(f.name)
        if parsed is None:
            unresolved.append((f.name, "does not match naming convention"))
            continue
        resolved = resolve_identity(parsed["name_part"], registry)
        if resolved is None:
            unresolved.append((
                f.name,
                f"'{parsed['name_part']}' does not resolve to any identity/variant "
                f"in ffpfsc_registry.json",
            ))
            continue
        identity, variant = resolved
        reg_entry = registry[identity]["variants"][variant]
        groups[(identity, variant)].append({
            "filename": f.name,
            "version": parsed["version"],
            "expiry": parsed.get("expiry"),
            "sha256": sha256_file(f),
            "registry": reg_entry,
        })

    if unresolved:
        log.line("")
        log.line(f"{len(unresolved)} file(s) excluded from PLUZ5-ffpfsc.json -- need manual attention:")
        for name, reason in unresolved:
            log.line(f"  [SKIP] {name} -- {reason}")

    all_entries = []

    for (identity, variant), artifacts in groups.items():
        artifacts.sort(key=lambda a: version_sort_key(a["version"]), reverse=True)
        reg = artifacts[0]["registry"]
        is_protected = bool(reg.get("protected_fallback"))

        selected = artifacts[:hosted_keep]
        if is_protected:
            extra = [a for a in artifacts if a not in selected]
            selected = selected + extra

        for i, a in enumerate(selected):
            tag = retention_labels[i] if i < len(retention_labels) else f"previous-{i}"
            all_entries.append(make_ffpfsc_entry(identity, variant, a, reg, env, tag))

    manifest = {
        "name": "Z3nT1's PLUZ5 -- ffpfsc",
        "schema_version": 1,
        "comment": "PS5 ffpfsc/ffpkg/fpkg ecosystem tools and helpers. ffpfsc_type field: compressor_tool | helper_elf | compressed_file.",
        "entries": all_entries,
    }

    manifests_dir = root / cfg["settings"]["paths"]["manifests"]
    manifests_dir.mkdir(parents=True, exist_ok=True)
    out_path = root / cfg["settings"]["manifest_files"]["ffpfsc"]
    out_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    current_count = sum(1 for e in all_entries if e["retention"] == "current")
    log.line("")
    log.line(f"PLUZ5-ffpfsc.json: {len(all_entries)} total entries "
             f"({current_count} current, {len(all_entries) - current_count} fallback)")
    log.close()
    print(f"\nLog written to: {log.path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
