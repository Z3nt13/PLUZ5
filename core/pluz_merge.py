"""
plz_merge.py -- scans ANY directory you point it at (your own local payload
dump, or a clone of someone else's payload repo) and copies in whatever
isn't already present. .elf/.bin go to payloads/, .pkg go to pkgs/ --
routed automatically by extension since they're different consumption
models (pldmgr autoloader vs package installer). Extracts zips using the
stdlib zipfile module (no external unzip/7z binary), parses filenames,
hashes everything, and flags anything ambiguous for manual review instead
of guessing.

No network access. Dry-run by default.
"""
from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pluz_common import (  # noqa: E402
    repo_root, load_config, parse_filename_raw, resolve_identity, split_name_best_effort,
    sha256_file, Log, BINARY_EXTS, PKG_EXTS,
)

ALL_ROUTABLE_EXTS = BINARY_EXTS | PKG_EXTS


def find_candidates_in_zip(zip_path: Path, extract_dir: Path) -> list[Path]:
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(extract_dir)
    return [p for p in extract_dir.rglob("*")
            if p.is_file() and p.suffix.lstrip(".").lower() in ALL_ROUTABLE_EXTS]


def plan_for_file(src_file: Path, log: Log, tmp_root: Path, elf_bin_registry: dict, pkg_registry: dict) -> dict | None:
    ext = src_file.suffix.lstrip(".").lower()

    if ext in ALL_ROUTABLE_EXTS:
        working_file, working_name = src_file, src_file.name
    elif ext == "zip":
        extract_dir = tmp_root / src_file.stem
        extract_dir.mkdir(parents=True, exist_ok=True)
        try:
            candidates = find_candidates_in_zip(src_file, extract_dir)
        except Exception as e:
            log.line(f"[SKIP] {src_file.name} -- could not extract zip: {e}")
            return None
        if len(candidates) == 0:
            log.line(f"[SKIP] {src_file.name} -- zip contained no .elf/.bin/.pkg -- manual review needed")
            return None
        if len(candidates) > 1:
            names = ", ".join(c.name for c in candidates)
            log.line(f"[SKIP] {src_file.name} -- zip contained multiple candidate files "
                      f"({names}) -- ambiguous, manual review needed")
            return None
        working_file = candidates[0]
        working_name = src_file.stem + working_file.suffix
    else:
        return None

    working_ext = working_file.suffix.lstrip(".").lower()
    parsed = parse_filename_raw(working_name)
    if parsed is None:
        log.line(f"[SKIP] {working_name} -- does not match "
                 f"{{name}}_v{{version}}[_Expi{{YYYYMMDD}}].{{ext}} "
                 f"-- see docs/rename-map.md, manual review needed")
        return None
    # honest log line: try a real registry match first (correct split even
    # for multi-hyphen compound names); only fall back to a labeled guess
    # when nothing in either registry matches yet (e.g. a brand new payload)
    registry = pkg_registry if working_ext in PKG_EXTS else elf_bin_registry
    resolved = resolve_identity(parsed["name_part"], registry)
    if resolved:
        parsed["payload"], parsed["variant"] = resolved
        parsed["guessed"] = False
    else:
        parsed["payload"], parsed["variant"] = split_name_best_effort(parsed["name_part"])
        parsed["guessed"] = True

    return {
        "src": working_file,
        "filename": working_name,
        "ext": working_ext,
        "parsed": parsed,
        "sha256": sha256_file(working_file),
    }


def main(argv=None):
    ap = argparse.ArgumentParser(prog="plz merge")
    ap.add_argument("--source", required=True, help="Directory to scan (local dump, or another repo's payloads/ dir)")
    ap.add_argument("--apply", action="store_true", help="Actually copy files (default: dry-run only)")
    args = ap.parse_args(argv)

    root = repo_root()
    log = Log(root, "pluz_merge")
    cfg = load_config(root)
    payloads_dir = root / cfg["settings"]["paths"]["payloads"]
    pkgs_dir = root / cfg["settings"]["paths"]["pkgs"]
    payloads_dir.mkdir(parents=True, exist_ok=True)
    pkgs_dir.mkdir(parents=True, exist_ok=True)

    source_dir = Path(args.source)
    if not source_dir.is_dir():
        log.line(f"[ERROR] source directory does not exist: {source_dir}")
        return 1

    mode = "APPLY" if args.apply else "DRY-RUN"
    log.line(f"PLUZ merge -- mode: {mode}")
    log.line(f"source: {source_dir}")
    log.line(f"targets: {payloads_dir} (elf/bin), {pkgs_dir} (pkg)")
    log.line("=" * 60)

    to_copy = []
    skipped = 0
    already_present = 0

    with tempfile.TemporaryDirectory(prefix="pluz_extract_") as tmp:
        tmp_root = Path(tmp)
        candidates = [p for p in source_dir.iterdir() if p.is_file()]
        for src_file in sorted(candidates, key=lambda p: p.name):
            plan = plan_for_file(src_file, log, tmp_root, cfg["registry"]["payloads"], cfg["pkg_registry"]["packages"])
            if plan is None:
                skipped += 1
                continue

            dest_dir = pkgs_dir if plan["ext"] in PKG_EXTS else payloads_dir
            dest = dest_dir / plan["filename"]
            if dest.exists():
                if sha256_file(dest) == plan["sha256"]:
                    already_present += 1
                    continue
                else:
                    log.line(f"[CONFLICT] {plan['filename']} already exists with a DIFFERENT hash "
                              f"-- not overwriting. Manual review needed.")
                    skipped += 1
                    continue

            to_copy.append((plan, dest))

        log.line("")
        log.line(f"Plan: {len(to_copy)} to copy, {already_present} already present, {skipped} need manual review")
        log.line("=" * 60)

        for plan, dest in to_copy:
            p = plan["parsed"]
            guess_tag = " (guess -- not yet registered)" if p.get("guessed") else ""
            log.line(f"  {plan['filename']} -> {dest.parent.name}/  "
                      f"payload={p['payload']} variant={p['variant']}{guess_tag} "
                      f"version={p['version']} sha256={plan['sha256'][:12]}...")
            if args.apply:
                shutil.copy2(plan["src"], dest)

    if args.apply:
        log.line("")
        log.line(f"Applied: copied {len(to_copy)} files.")
        log.line("Reminder: new payload/variant combos not yet in payload_registry.json or "
                 "pkg_registry.json won't show up in manifests until you add them "
                 "('check' will list what's missing).")
    else:
        log.line("")
        log.line("This was a DRY RUN. Re-run with --apply to actually copy files.")

    log.close()
    print(f"\nLog written to: {log.path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
