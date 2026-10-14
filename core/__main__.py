"""
__main__.py -- entry point for PLUZ.pyz (built via `python3 -m zipapp`).

Pure stdlib dispatcher. No network access, no third-party imports. Maps a
subcommand name to the matching pluz_<name> module's main(argv) function.
"""
from __future__ import annotations

import sys

COMMANDS = {
    "check": "pluz_check",
    "merge": "pluz_merge",
    "fetch": "pluz_fetch",
    "update": "pluz_update",
    "pkg": "pluz_pkg",
    "ffpfsc": "pluz_ffpfsc",
    "cleanup": "pluz_cleanup",
    "migrate": "pluz_migrate",
    "validate": "pluz_validate",
    "dedupe": "pluz_dedupe",
    "backup": "pluz_backup",
    "ghclean": "pluz_ghclean",
    "debug": "pluz_debug",
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("PLUZ-ps5 -- usage: PLUZ.pyz <command> [args]")
        print("")
        print("Commands:")
        for name in COMMANDS:
            print(f"  {name}")
        print("")
        print("Run 'PLUZ.pyz <command> --help' for a command's own options.")
        return 0

    command = sys.argv[1]
    if command not in COMMANDS:
        print(f"[ERROR] unknown command '{command}'. Run with --help to see the list.", file=sys.stderr)
        return 1

    module = __import__(COMMANDS[command])
    return module.main(sys.argv[2:])


if __name__ == "__main__":
    sys.exit(main())
