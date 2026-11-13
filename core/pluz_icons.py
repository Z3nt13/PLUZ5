"""pluz_icons -- generated icons for the pldmgr list.

pldmgr's own format (seen in its tools/test_repo.json + test_icons.json):
  manifest: top-level "icons_url", and "icon_key" on each payload
  icons file: {"icons": {"<key>": "data:image/svg+xml;base64,..."}}
  key = SHA-256 (hex) of the data-URI string, so equal icons share one key.

We draw the same style: 128x128 rounded square, category colour, two initials.
Standard library only; no network.
"""
from __future__ import annotations

import base64
import hashlib
import re

COLORS = {  # category -> (light, dark)
    "Kernel": ("#ef4444", "#b91c1c"), "Network": ("#3b82f6", "#1d4ed8"),
    "File Management": ("#f59e0b", "#b45309"), "Game Tools": ("#10b981", "#047857"),
    "Media": ("#ec4899", "#be185d"), "System Utility": ("#8b5cf6", "#6d28d9"),
    "Debug & SDK": ("#06b6d4", "#0e7490"), "Linux": ("#64748b", "#334155"),
    "Activation & Spoof": ("#f97316", "#c2410c"), "Unknown": ("#6b7280", "#374151"),
}


def initials(name: str) -> str:
    toks = [t for t in re.split(r"[^A-Za-z0-9]+", re.sub(r"\s*\([^)]*\)\s*$", "", name)) if t]
    if not toks:
        return "?"
    first = toks[0][0].upper()
    if len(toks) > 1:
        return first + toks[1][0].upper()
    caps = [c for c in toks[0][1:] if c.isupper()]
    return first + (caps[0] if caps else "")


def icon_for(name: str, category: str) -> tuple[str, str]:
    """Return (key, data_uri)."""
    a, b = COLORS.get(category, COLORS["Unknown"])
    txt = initials(name).replace("&", "&amp;").replace("<", "&lt;")
    svg = ("<svg xmlns='http://www.w3.org/2000/svg' width='128' height='128'><defs>"
           "<linearGradient id='g' x1='0' y1='0' x2='1' y2='1'>"
           f"<stop offset='0' stop-color='{a}'/><stop offset='1' stop-color='{b}'/></linearGradient></defs>"
           "<rect width='128' height='128' rx='24' fill='url(#g)'/>"
           "<text x='64' y='82' font-family='Arial,sans-serif' font-size='44' font-weight='bold' fill='#fff' "
           f"text-anchor='middle'>{txt}</text></svg>")
    uri = "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()
    return hashlib.sha256(uri.encode()).hexdigest(), uri
