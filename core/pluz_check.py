"""
plz_check.py -- full PLUZ-ps5 health check. Reads only, never writes
(except its own log file). No network access.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pluz_common import (  # noqa: E402
    repo_root, load_env, require_env, load_config, parse_filename_raw, resolve_identity, Log,
)


def check(log: Log, label: str, ok: bool, detail: str = "") -> bool:
    status = "OK" if ok else "FAIL"
    line = f"[{status:4}] {label}"
    if detail:
        line += f" -- {detail}"
    log.line(line)
    return ok


def check_dir_coverage(log: Log, dir_path: Path, registry: dict, label: str):
    unresolved = []
    if dir_path.is_dir():
        for f in dir_path.iterdir():
            if not f.is_file() or f.name == ".gitkeep":
                continue
            parsed = parse_filename_raw(f.name)
            if parsed is None:
                unresolved.append((f.name, "unparseable filename"))
                continue
            resolved = resolve_identity(parsed["name_part"], registry)
            if resolved is None:
                unresolved.append((f.name, f"no registry entry resolves '{parsed['name_part']}'"))
    if unresolved:
        log.line(f"[WARN] {len(unresolved)} file(s) in {label}/ won't appear in manifests:")
        for name, reason in unresolved:
            log.line(f"    {name} -- {reason}")
    else:
        check(log, f"every {label}/ file resolves against its registry", True)


def main(argv=None):
    root = repo_root()
    log = Log(root, "pluz_check")
    log.line("PLUZ-ps5 health check")
    log.line("=" * 50)

    all_ok = True

    for d in ["configs", "data", "payloads", "pkgs", "ffpfsc", "manifests", "manifests/split", "core", "web", "logs"]:
        all_ok &= check(log, f"directory: {d}", (root / d).is_dir())

    try:
        cfg = load_config(root)
        all_ok &= check(log, "config files parse", True)
    except Exception as e:
        cfg = None
        all_ok &= check(log, "config files parse", False, str(e))

    env = load_env(root)
    env_file_exists = (root / ".env").exists()
    all_ok &= check(log, ".env file present", env_file_exists,
                     "run: cp .env.example .env  (then fill it in)" if not env_file_exists else "")
    if env_file_exists:
        missing = require_env(env, ["GH_TOKEN", "GH_USER", "GH_REPO", "GH_BRANCH"])
        all_ok &= check(log, ".env has required keys", not missing,
                         f"missing: {', '.join(missing)}" if missing else "")

    gi = root / ".gitignore"
    gi_ok = gi.exists() and ".env" in gi.read_text(encoding="utf-8")
    all_ok &= check(log, ".gitignore excludes .env", gi_ok)

    git_path = shutil.which("git")
    check(log, "git on PATH", git_path is not None, git_path or "not found (ok if configured via portable_tools)")
    check(log, f"python version: {sys.version.split()[0]}", sys.version_info >= (3, 9))

    if cfg:
        pt = cfg["settings"].get("portable_tools", {})
        for name, path_str in pt.items():
            if name == "comment" or not path_str:
                continue
            p = Path(path_str)
            check(log, f"portable tool '{name}' path exists", p.exists(), str(p))

    leftovers = list(root.glob("*.tmp")) + list(root.glob("pluz_extract_*")) + list(root.glob("pluz_backup_tmp_*"))
    if leftovers:
        log.line(f"[WARN] {len(leftovers)} leftover tmp/extraction item(s) found -- "
                 f"run cleanup to sweep them: {', '.join(p.name for p in leftovers[:10])}")
    else:
        check(log, "no leftover tmp/extraction items", True)

    if cfg:
        check_dir_coverage(log, root / cfg["settings"]["paths"]["payloads"], cfg["registry"]["payloads"], "payloads")
        check_dir_coverage(log, root / cfg["settings"]["paths"]["pkgs"], cfg["pkg_registry"]["packages"], "pkgs")
        check_dir_coverage(log, root / cfg["settings"]["paths"].get("ffpfsc", "ffpfsc"), cfg["ffpfsc_registry"].get("entries", {}), "ffpfsc")

    log.line("=" * 50)
    log.line("PLUZ environment is READY." if all_ok else "PLUZ environment has issues -- see FAIL lines above.")
    log.close()
    print(f"\nLog written to: {log.path}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
