"""
pluz_ghauth.py -- prints the HTTP header git needs to sign in to GitHub with
GH_USER + GH_TOKEN from .env, or nothing if either is unset. Used by the
AllStar scripts as `git -c "http.extraheader=<this output>" push`, so the
token is never written into the remote URL or git's config on disk.
"""
import base64
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pluz_common import load_env  # noqa: E402


def main():
    env = load_env()
    user, token = env.get("GH_USER", ""), env.get("GH_TOKEN", "")
    if user and token:
        pair = base64.b64encode(f"{user}:{token}".encode()).decode()
        print(f"AUTHORIZATION: basic {pair}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
