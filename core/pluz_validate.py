"""
pluz_validate.py -- checks manifest JSON schema (ELF/BIN pldmgr shape, PKG
shape AND ffpfsc shape), scans payloads/ + pkgs/ for filenames that won't parse, and
reports SHA-256 collisions. Read-only. No network access.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pluz_common import repo_root, load_config, parse_filename_raw, sha256_file, Log  # noqa: E402


HW_TARGETS = {None, "P5", "P5P", "P5U"}


def check_hw(entry, path: Path, log: Log) -> bool:
    if entry.get("hw_target") not in HW_TARGETS:
        log.line(f"[FAIL] {path.name} -- '{entry.get('filename', '?')}' has invalid hw_target '{entry.get('hw_target')}' (use P5, P5P, P5U or leave unset)")
        return False
    return True


def validate_pldmgr_manifest(path: Path, log: Log) -> bool:
    if not path.exists():
        log.line(f"[FAIL] {path.name} -- file does not exist (run 'update' first)")
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        log.line(f"[FAIL] {path.name} -- invalid JSON: {e}")
        return False

    ok = True
    keys = list(data.keys())
    if keys[:2] != ["name", "payloads"]:
        log.line(f"[FAIL] {path.name} -- top-level keys must be ['name','payloads'] in that order, got {keys}")
        ok = False

    for entry in data.get("payloads", []):
        fn = entry.get("filename", "?")
        if not isinstance(entry.get("url"), str):
            log.line(f"[FAIL] {path.name} -- '{fn}' has non-string url (pldmgr requires a single string)")
            ok = False
        bu = entry.get("backup_url")
        if bu is not None and not isinstance(bu, str):
            log.line(f"[FAIL] {path.name} -- '{fn}' has non-string backup_url (must be a string or null)")
            ok = False
        if not entry.get("checksum"):
            log.line(f"[FAIL] {path.name} -- '{fn}' missing checksum")
            ok = False
        ok &= check_hw(entry, path, log)
        if entry.get("category") == "Unknown":
            log.line(f"[WARN] {path.name} -- '{fn}' still has category Unknown")

    if ok:
        log.line(f"[OK  ] {path.name} -- schema valid ({len(data.get('payloads', []))} entries)")
    return ok


def validate_pkg_manifest(path: Path, log: Log) -> bool:
    if not path.exists():
        log.line(f"[FAIL] {path.name} -- file does not exist (run 'pkg' first)")
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        log.line(f"[FAIL] {path.name} -- invalid JSON: {e}")
        return False

    ok = True
    keys = list(data.keys())
    if keys[:2] != ["name", "packages"]:
        log.line(f"[FAIL] {path.name} -- top-level keys must be ['name','packages'] in that order, got {keys}")
        ok = False

    valid_tags = {"current", "previous", "previous-2", "previous-3", "previous-4"}
    for entry in data.get("packages", []):
        fn = entry.get("filename", "?")
        if not isinstance(entry.get("url"), str):
            log.line(f"[FAIL] {path.name} -- '{fn}' has non-string url")
            ok = False
        bu = entry.get("backup_url")
        if bu is not None and not isinstance(bu, str):
            log.line(f"[FAIL] {path.name} -- '{fn}' has non-string backup_url (must be a string or null)")
            ok = False
        if not entry.get("checksum"):
            log.line(f"[FAIL] {path.name} -- '{fn}' missing checksum")
            ok = False
        ok &= check_hw(entry, path, log)
        tag = entry.get("retention")
        if tag not in valid_tags and not (isinstance(tag, str) and tag.startswith("previous-")):
            log.line(f"[WARN] {path.name} -- '{fn}' has unexpected retention tag '{tag}'")

    if ok:
        log.line(f"[OK  ] {path.name} -- schema valid ({len(data.get('packages', []))} entries)")
    return ok


def validate_ffpfsc_manifest(path: Path, log: Log) -> bool:
    if not path.exists():
        log.line(f"[SKIP] {path.name} not found yet (run 'ffpfsc' if you host ffpfsc/ files)")
        return True
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        log.line(f"[FAIL] {path.name} -- invalid JSON: {e}")
        return False

    ok = True
    if not isinstance(data.get("entries"), list):
        log.line(f"[FAIL] {path.name} -- top-level key 'entries' (list) is required, got {list(data.keys())}")
        return False
    valid_types = {"compressor_tool", "helper_elf", "compressed_file"}
    for entry in data["entries"]:
        fn = entry.get("filename", "?")
        if not isinstance(entry.get("url"), str):
            log.line(f"[FAIL] {path.name} -- '{fn}' has non-string url")
            ok = False
        bu = entry.get("backup_url")
        if bu is not None and not isinstance(bu, str):
            log.line(f"[FAIL] {path.name} -- '{fn}' has non-string backup_url (must be a string or null)")
            ok = False
        if not entry.get("checksum"):
            log.line(f"[FAIL] {path.name} -- '{fn}' missing checksum")
            ok = False
        ok &= check_hw(entry, path, log)
        if entry.get("ffpfsc_type") not in valid_types:
            log.line(f"[FAIL] {path.name} -- '{fn}' has invalid ffpfsc_type '{entry.get('ffpfsc_type')}'")
            ok = False
    if ok:
        log.line(f"[OK  ] {path.name} -- schema valid ({len(data['entries'])} entries)")
    return ok


def scan_dir_for_issues(payloads_dir: Path, label: str, log: Log):
    files = [p for p in payloads_dir.iterdir() if p.is_file() and p.name != ".gitkeep"] \
        if payloads_dir.is_dir() else []
    unparseable = [f.name for f in files if parse_filename_raw(f.name) is None]
    if unparseable:
        log.line(f"[WARN] {len(unparseable)} filename(s) in {label}/ won't parse -- see docs/rename-map.md:")
        for n in unparseable:
            log.line(f"    {n}")
    else:
        log.line(f"[OK  ] every filename in {label}/ parses cleanly")

    by_hash = defaultdict(list)
    for f in files:
        by_hash[sha256_file(f)].append(f.name)
    collisions = {h: names for h, names in by_hash.items() if len(names) > 1}
    if collisions:
        log.line(f"[WARN] {len(collisions)} SHA-256 collision group(s) in {label}/ -- run 'dedupe' for detail")
    else:
        log.line(f"[OK  ] no SHA-256 collisions in {label}/")


def main(argv=None):
    root = repo_root()
    log = Log(root, "pluz_validate")
    cfg = load_config(root)

    log.line("PLUZ validate")
    log.line("=" * 60)

    all_ok = True
    all_ok &= validate_pldmgr_manifest(root / cfg["settings"]["manifest_files"]["main"], log)
    all_ok &= validate_pldmgr_manifest(root / cfg["settings"]["manifest_files"]["hosted"], log)

    split_dir = root / cfg["settings"]["paths"]["split_manifests"]
    if split_dir.is_dir():
        for p in sorted(split_dir.glob("*.json")):
            all_ok &= validate_pldmgr_manifest(p, log)

    mf = cfg["settings"]["manifest_files"]
    pkg_file = root / mf.get("pkg", "manifests/PLUZ5-PKG.json")
    if pkg_file.exists():
        all_ok &= validate_pkg_manifest(pkg_file, log)
    else:
        log.line(f"[SKIP] no {pkg_file.name} found yet (run 'pkg' if you have .pkg files)")

    all_ok &= validate_ffpfsc_manifest(root / mf.get("ffpfsc", "manifests/PLUZ5-ffpfsc.json"), log)

    log.line("")
    log.line("Scanning payloads/, pkgs/ and ffpfsc/ for issues...")
    scan_dir_for_issues(root / cfg["settings"]["paths"]["payloads"], "payloads", log)
    scan_dir_for_issues(root / cfg["settings"]["paths"]["pkgs"], "pkgs", log)
    scan_dir_for_issues(root / cfg["settings"]["paths"].get("ffpfsc", "ffpfsc"), "ffpfsc", log)

    log.line("=" * 60)
    log.line("VALIDATION PASSED." if all_ok else "VALIDATION FAILED -- see FAIL lines above.")
    log.close()
    print(f"\nLog written to: {log.path}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
