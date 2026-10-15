"""
pluz_pkg.py -- regenerates PLUZ5-PKG.json from whatever is currently in
pkgs/, using configs/pkg_registry.json for metadata.

PKGs are NOT pldmgr's domain (pldmgr's autoloader consumes .elf/.bin).
PKGs are typically installed via a package installer or a fetchpkg-style
tool that reads a JSON manifest of its own -- so this writes a dedicated
manifest rather than mixing into the pldmgr manifests. Fields (title_id,
content_id, pkg_type, required_system_version) are modeled on real PS5 PKG
param.json metadata, not invented.

Per the "3 manifests total" decision (Source/Hosted for ELF+BIN, one PKG
file), current + fallback PKG builds live together in ONE file, each entry
tagged with a "retention" field ("current"/"previous"/"previous-2") rather
than splitting into a separate PKG-Hosted.json. Same retention rule as
ELF/BIN: 1 current + up to hosted_keep-1 additional fallbacks per
(identity, variant), protected_fallback entries always kept.

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
    repo_root, load_env, load_config, parse_filename_raw, resolve_identity, sha256_file,
    version_sort_key, Log,
)


def build_url(gh_user: str, gh_repo: str, gh_branch: str, filename: str) -> str:
    return f"https://raw.githubusercontent.com/{gh_user}/{gh_repo}/{gh_branch}/pkgs/{filename}"


def make_pkg_entry(identity: str, variant: str, artifact: dict, reg: dict, env: dict, retention_tag: str) -> dict:
    url = build_url(env["GH_USER"], env["GH_REPO"], env["GH_BRANCH"], artifact["filename"])
    display_name = reg.get("display_name", identity if variant == "default" else f"{identity} ({variant})")

    return {
        "name": display_name,
        "filename": artifact["filename"],
        "url": url,
        "backup_url": reg.get("backup_url"),
        "title_id": reg.get("title_id"),
        "content_id": reg.get("content_id"),
        "pkg_type": reg.get("pkg_type", "homebrew"),
        "version": artifact["version"],
        "required_system_version": reg.get("required_system_version"),
        "platform": reg.get("platform", "ps5"),
        "hw_target": reg.get("hw_target"),
        "category": reg.get("category", "Unknown"),
        "author": reg.get("author"),
        "author_url": reg.get("author_url"),
        "checksum": artifact["sha256"],
        "retention": retention_tag,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(prog="pluz pkg")
    ap.parse_args(argv)  # no options yet -- kept for a consistent CLI shape

    root = repo_root()
    log = Log(root, "pluz_pkg")
    cfg = load_config(root)
    env = load_env(root)

    missing_env = [k for k in ("GH_USER", "GH_REPO", "GH_BRANCH") if not env.get(k)]
    if missing_env:
        log.line(f"[ERROR] missing required .env values: {', '.join(missing_env)}")
        log.line("Run 'check' and fill in .env before generating manifests.")
        return 1

    pkgs_dir = root / cfg["settings"]["paths"]["pkgs"]
    registry = cfg["pkg_registry"]["packages"]
    retention = cfg["settings"].get("pkg_retention", cfg["settings"]["retention"])
    hosted_keep = retention["hosted_keep"]

    files = [p for p in pkgs_dir.iterdir() if p.is_file() and p.suffix.lstrip(".").lower() == "pkg"] \
        if pkgs_dir.is_dir() else []
    log.line(f"Scanning {len(files)} files in {pkgs_dir}")

    groups = defaultdict(list)
    unresolved = []

    for f in sorted(files, key=lambda p: p.name):
        parsed = parse_filename_raw(f.name)
        if parsed is None:
            unresolved.append((f.name, "does not match naming convention -- "
                               "official Sony PKGs with content-id filenames need a manual "
                               "pkg_registry.json entry keyed by exact filename (not yet supported "
                               "by this parser -- flagged, not guessed)"))
            continue
        resolved = resolve_identity(parsed["name_part"], registry)
        if resolved is None:
            unresolved.append((f.name, f"'{parsed['name_part']}' does not resolve to any "
                               f"registered identity/variant in pkg_registry.json"))
            continue
        identity, variant = resolved
        reg_entry = registry[identity]["variants"][variant]
        groups[(identity, variant)].append({
            "filename": f.name,
            "version": parsed["version"],
            "sha256": sha256_file(f),
            "registry": reg_entry,
        })

    if unresolved:
        log.line("")
        log.line(f"{len(unresolved)} file(s) excluded from PLUZ5-PKG.json -- need manual attention:")
        for name, reason in unresolved:
            log.line(f"  [SKIP] {name} -- {reason}")

    all_pkgs = []
    retention_labels = ["current", "previous", "previous-2", "previous-3", "previous-4"]

    for (identity, variant), artifacts in groups.items():
        artifacts.sort(key=lambda a: version_sort_key(a["version"]), reverse=True)
        reg_entry = artifacts[0]["registry"]
        is_protected = reg_entry.get("protected_fallback", False)
        effective_keep = max(hosted_keep, len(artifacts)) if is_protected else hosted_keep

        for i, artifact in enumerate(artifacts[:effective_keep]):
            tag = retention_labels[i] if i < len(retention_labels) else f"previous-{i}"
            entry = make_pkg_entry(identity, variant, artifact, reg_entry, env, tag)
            all_pkgs.append(entry)

    manifest = {"name": "Z3nT1's PLUZ5 -- PKG", "packages": all_pkgs}

    out_path = root / cfg["settings"]["manifest_files"]["pkg"]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    log.line(f"Wrote {len(all_pkgs)} entries to {out_path}")

    if unresolved:
        log.line(f"[WARN] {len(unresolved)} files skipped -- see log for details")

    log.close()
    return 0 if not unresolved else 1


if __name__ == "__main__":
    sys.exit(main())
