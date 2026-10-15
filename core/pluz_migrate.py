"""
plz_migrate.py -- retires an OLD, separate PLUZ repo into this clean one.

Safety contract:
  - The OLD repo is NEVER modified or deleted. Only read.
  - A full zip backup of the old repo is made before anything else (on --apply).
  - Old payload binaries are copied (not moved) into the new payloads/.
  - Old manifest JSON is read best-effort to pre-seed payload_registry.json.
    Uncertain fields become "Unknown"/"unset" -- never fabricated.

No network access. Dry-run by default.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pluz_common import (  # noqa: E402
    repo_root, parse_filename_raw, split_name_best_effort, sha256_file, create_backup_zip, timestamp, Log, BINARY_EXTS,
)


def find_old_manifests(old_root: Path) -> list[Path]:
    candidates = []
    for pattern in ("*PLUZ*.json", "payloads*.json", "Z3nT1s*.json"):
        candidates.extend(old_root.glob(pattern))
    seen, out = set(), []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out


def extract_registry_hints(manifest_json: dict) -> dict:
    hints = {}
    for entry in manifest_json.get("payloads", []):
        parsed = parse_filename_raw(entry.get("filename", ""))
        if not parsed:
            continue
        payload, variant = split_name_best_effort(parsed["name_part"])
        source = entry.get("source")
        if isinstance(source, list):
            source = next((s for s in source if "raw.githubusercontent" not in s), source[0] if source else None)
        hints.setdefault(payload, {}).setdefault("variants", {})[variant] = {
            "display_name": entry.get("name", payload),
            "source_repo": source or "unset -- fill in",
            "category": entry.get("category", "Unknown"),
            "channel": "stable",
            "fw_min": None,
            "fw_max": None,
            "port": None,
            "protected_fallback": False,
            "note": "imported from old repo -- review",
        }
    return hints


def main(argv=None):
    ap = argparse.ArgumentParser(prog="plz migrate")
    ap.add_argument("--old", required=True, help="Path to the OLD PLUZ repo (read-only)")
    ap.add_argument("--apply", action="store_true", help="Actually write files (default: dry-run)")
    args = ap.parse_args(argv)

    old_root = Path(args.old)
    new_root = repo_root()

    if not old_root.is_dir():
        print(f"[ERROR] old repo path does not exist: {old_root}", file=sys.stderr)
        return 1

    log = Log(new_root, "pluz_migrate")
    mode = "APPLY" if args.apply else "DRY-RUN"
    log.line(f"PLUZ migrate -- mode: {mode}")
    log.line(f"old (read-only): {old_root}")
    log.line(f"new (target):    {new_root}")
    log.line("=" * 60)

    backup_target = old_root.parent / f"{old_root.name}_BACKUP_{timestamp()}"
    log.line(f"[PLAN] backup old repo -> {backup_target}.zip")
    if args.apply:
        written = create_backup_zip(old_root, backup_target)
        log.line(f"[DONE] backup written: {written}")

    old_payloads_dir = old_root / "payloads"
    old_files = [p for p in old_payloads_dir.iterdir() if p.is_file() and p.suffix.lstrip(".").lower() in BINARY_EXTS] \
        if old_payloads_dir.is_dir() else []
    log.line(f"[FOUND] {len(old_files)} binaries in {old_payloads_dir}")

    new_payloads_dir = new_root / "payloads"
    new_payloads_dir.mkdir(parents=True, exist_ok=True)

    copied, dupe, conflict = 0, 0, 0
    for f in sorted(old_files, key=lambda p: p.name):
        dest = new_payloads_dir / f.name
        if dest.exists():
            if sha256_file(dest) == sha256_file(f):
                dupe += 1
                continue
            log.line(f"[CONFLICT] {f.name} exists with different hash -- not overwritten")
            conflict += 1
            continue
        log.line(f"[PLAN] copy {f.name}")
        if args.apply:
            shutil.copy2(f, dest)
        copied += 1

    log.line(f"[SUMMARY] {copied} to copy, {dupe} already identical, {conflict} conflicts")

    old_manifests = find_old_manifests(old_root)
    log.line(f"[FOUND] {len(old_manifests)} candidate old manifest file(s): "
             f"{', '.join(p.name for p in old_manifests) or '(none)'}")

    merged_hints = {}
    for mf in old_manifests:
        try:
            data = json.loads(mf.read_text(encoding="utf-8"))
        except Exception as e:
            log.line(f"[SKIP] {mf.name} -- could not parse JSON: {e}")
            continue
        for payload, body in extract_registry_hints(data).items():
            merged_hints.setdefault(payload, {"variants": {}})
            merged_hints[payload]["variants"].update(body["variants"])

    if merged_hints:
        registry_path = new_root / "configs" / "payload_registry.json"
        existing = json.loads(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {
            "schema_version": 3, "payloads": {}
        }
        added = 0
        for payload, body in merged_hints.items():
            existing["payloads"].setdefault(payload, {"variants": {}})
            for variant, meta in body["variants"].items():
                if variant not in existing["payloads"][payload]["variants"]:
                    existing["payloads"][payload]["variants"][variant] = meta
                    added += 1
        log.line(f"[PLAN] merge {added} new payload/variant entries into payload_registry.json "
                 f"(existing entries never overwritten)")
        if args.apply:
            registry_path.write_text(json.dumps(existing, indent=2), encoding="utf-8")
            log.line("[DONE] payload_registry.json updated -- review 'Unknown'/'unset' fields by hand")

    log.line("=" * 60)
    if not args.apply:
        log.line("This was a DRY RUN. Nothing was written. Re-run with --apply to execute this plan.")
    log.line("The OLD repo was never modified.")
    log.close()
    print(f"\nLog written to: {log.path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
