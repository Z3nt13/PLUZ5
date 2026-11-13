"""pluz pack -- build the PLUZ5-Cust download pack from this (the main PLUZ5) repo.

  python pluz.py pack                 writes dist/PLUZ5-Cust/ and dist/PLUZ5-Cust-<version>.zip
  python pluz.py pack --version v8.0  name the zip

The pack is this repo with: no payloads, no manifests, an empty Library, an empty Store,
mode "source", and the Cust README. The full list and the sources list stay in examples/.
The workflow .github/workflows/pack.yml runs this on every release.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pluz_common import repo_root  # noqa: E402

SKIP_DIRS = {".git", "__pycache__", "dist", "logs", "_backups", "payloads", "manifests", "pack", "data"}
SKIP_FILES = {".env"}
DOCS_DROP = {"GUIDE-PLUZ5.md"}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="pluz pack")
    ap.add_argument("--version", default="v8.0")
    a = ap.parse_args(argv)
    root = repo_root()
    if not (root / "pack" / "README-Cust.md").exists():
        print("This is not the main PLUZ5 repo (pack/README-Cust.md missing).")
        return 1
    dist = root / "dist"
    out = dist / "PLUZ5-Cust"
    if dist.exists():
        shutil.rmtree(dist)
    out.mkdir(parents=True)

    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts) or p.is_dir() or rel.name in SKIP_FILES:
            continue
        if rel.parts[0] == "docs" and rel.name in DOCS_DROP:
            continue
        if rel.suffix == ".pyc":
            continue
        dst = out / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dst)

    # empty working folders
    for d in ("payloads", "manifests", "logs", "data"):
        (out / d).mkdir(exist_ok=True)
        (out / d / ".gitkeep").write_text("", encoding="utf-8")

    # examples: the full list and the sources list
    ex = out / "examples"
    ex.mkdir(exist_ok=True)
    shutil.copy2(root / "configs" / "payload_registry.json", ex / "example-full.json")
    if (root / "data" / "PLUZ5-infos.md").exists():
        shutil.copy2(root / "data" / "PLUZ5-infos.md", ex / "PS5-SOURCES-library.md")
    if (root / "data" / "PLUZ5-infos.json").exists():
        shutil.copy2(root / "data" / "PLUZ5-infos.json", ex / "PS5-SOURCES-library.json")

    # empty Store, source mode
    reg = {"schema_version": 6, "store_name": "My PLUZ5 store",
           "comment": "YOUR list. Build it with web/library.html or web/builder.html, or load examples/example-full.json.",
           "payloads": {}}
    (out / "configs" / "payload_registry.json").write_text(json.dumps(reg, indent=2) + "\n", encoding="utf-8")
    st = json.loads((out / "configs" / "settings.json").read_text(encoding="utf-8"))
    st["mode"], st["project"] = "source", "PLUZ5-Cust"
    (out / "configs" / "settings.json").write_text(json.dumps(st, indent=2) + "\n", encoding="utf-8")
    (out / "data" / "PLUZ5-infos.json").write_text(json.dumps(
        {"schema_version": 8, "comment": "Your Library. Edit with web/library.html.", "entries": [],
         "powered_by": "Powered By Z3nT13's PLUZ5"}, indent=2) + "\n", encoding="utf-8")

    # env: blank, ready to fill; mode source
    env = (root / ".env.example").read_text(encoding="utf-8")
    env = re.sub(r"(?m)^GH_USER=.*$", "GH_USER=your-github-name", env)
    env = re.sub(r"(?m)^GH_REPO=.*$", "GH_REPO=your-repo-name", env)
    env = re.sub(r"(?m)^# PLUZ_MODE=.*$", "# PLUZ_MODE=source", env)
    (out / ".env").write_text(env, encoding="utf-8")
    (out / ".env.example").write_text(env, encoding="utf-8")

    # texts: Cust README, names
    shutil.copy2(root / "pack" / "README-Cust.md", out / "README.md")
    for f in ("web/builder.html", "web/catalog.html", "web/library.html", "web/start.html", "web/pldmgr.html", "pluz.py", "core/pluz_cli.py"):
        p = out / f
        if p.exists():
            t = p.read_text(encoding="utf-8")
            t = t.replace("PLUZ5-Cust", "PLUZ5-Cust").replace("<title>PLUZ5 -", "<title>PLUZ5-Cust -")
            p.write_text(t, encoding="utf-8")
    cli = out / "core" / "pluz_cli.py"
    t = cli.read_text(encoding="utf-8")
    cli.write_text(re.sub(r'\s*"pack": "pluz_pack",?', "", t), encoding="utf-8")
    (out / "core" / "pluz_pack.py").unlink(missing_ok=True)

    zp = dist / f"PLUZ5-Cust-{a.version}-FULL.zip"
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(out.rglob("*")):
            if p.is_file():
                z.write(p, Path("PLUZ5-Cust") / p.relative_to(out))
    n = sum(1 for p in out.rglob("*") if p.is_file())
    print(f"pack: {n} files -> {zp}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
