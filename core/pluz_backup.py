"""
plz_backup.py -- zips the whole repo to <backups>/, on demand. Same logic
used internally by plz_cleanup.py and plz_migrate.py. No network access.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pluz_common import repo_root, load_config, create_backup_zip, timestamp, Log  # noqa: E402


def main(argv=None):
    root = repo_root()
    log = Log(root, "pluz_backup")
    cfg = load_config(root)

    backups_dir = root / cfg["settings"]["paths"].get("backups", "_backups")
    backups_dir.mkdir(parents=True, exist_ok=True)
    target = backups_dir / f"PLUZ-ps5_BACKUP_{timestamp()}"

    log.line(f"Backing up {root} -> {target}.zip")
    written = create_backup_zip(root, target)
    log.line(f"[DONE] {written}")
    log.close()
    print(f"\nBackup: {written}")
    print(f"Log written to: {log.path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
