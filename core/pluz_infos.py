"""pluz infos -- the Library (every source you know about) and its readable copies.

data/PLUZ5-infos.json   master (edited with web/library.html)
data/PLUZ5-infos.md     generated, same blocks as a readable list (see docs/BLOCK-FORMAT.md)
data/PLUZ5-infos.xlsx   generated, one row per entry

  python pluz.py infos                  rebuild the .md and .xlsx from the json
  python pluz.py infos --import f.md    add blocks (new block format, or the old tracker format)
  python pluz.py infos --sync-store     add a Library entry for every Store entry that has none
  python pluz.py infos --to-store       add Store entries for Library blocks that are Store-ready
  python pluz.py infos --check          validate only

The Library is never read by pldmgr. Only configs/payload_registry.json (the Store) is.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pluz_common import repo_root, load_config, Log  # noqa: E402

POWERED = "Powered By Z3nT13's PLUZ5"
SCHEMA = 8
CATS = ["Kernel", "Network", "File Management", "Game Tools", "Media", "System Utility",
        "Debug & SDK", "Linux", "Activation & Spoof", "Unknown"]
HW = ("P5", "P5P", "P5U")
TYPES = ("payload", "app", "pkg", "tool", "sender", "exploit", "store", "reference")
CHANNELS = ("stable", "beta", "alpha")
RELS = ("fork", "clone", "template")
FMT_PAYLOAD = (".elf", ".bin")


def cat_tag(c: str) -> str:
    return re.sub(r"[ &]+", "-", c.replace(" & ", "-")).strip("-")


TAG2CAT = {cat_tag(c).lower(): c for c in CATS}
TAG2CAT.update({"debug-sdk": "Debug & SDK", "activation-spoof": "Activation & Spoof"})


def slug(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-") or "entry"


def norm_url(u: str) -> str:
    return re.sub(r"(\.git)?/*$", "", str(u or "").strip().lower())


def owner_of(url: str) -> str:
    m = re.match(r"https?://github\.com/([^/]+)/?", str(url or ""), re.I)
    return m.group(1) if m else ""


def is_repo(url: str) -> bool:
    return bool(re.match(r"https?://github\.com/[^/]+/[^/]+/?$", str(url or ""), re.I))


def make_id(name: str, variant: str) -> str:
    return f"{slug(name)}-{slug(variant or 'org')}"


def fw_fmt(n: str) -> str:
    """'760' -> '7.60', '1200' -> '12.00' (the registry still uses dotted strings)."""
    n = str(n)
    return f"{n[:-2]}.{n[-2:]}" if len(n) >= 3 else n


def fw_num(s: str) -> str:
    return re.sub(r"\D", "", str(s or ""))


def load_infos(path: Path) -> dict:
    if path.exists():
        d = json.loads(path.read_text(encoding="utf-8"))
        d.setdefault("entries", [])
        return d
    return {"schema_version": SCHEMA, "comment": "Your Library. Edit with web/library.html.", "entries": []}


def save_infos(path: Path, d: dict) -> None:
    out = {k: v for k, v in d.items() if k not in ("entries", "powered_by")}
    out["schema_version"] = SCHEMA
    out["entries"] = d["entries"]
    out["powered_by"] = POWERED
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def new_entry(**kw) -> dict:
    e = {"id": "", "name": "", "url": "", "author": "", "variant": "", "section": "General", "desc": "",
         "category": "Unknown", "tags": [], "type": "", "formats": [], "hw": "", "relation": "",
         "channel": "", "fw": "", "fw_list": [], "fw_not": [], "ports": [], "delivery": "", "keep": False,
         "needs": [], "notes": "", "extras_unknown": [], "flags": [], "removed": False, "hidden": False}
    e.update(kw)
    return e


# ---------- Extras tokens ----------
def parse_extras(text: str, e: dict) -> None:
    for raw in re.split(r"\s*\|\s*", text.strip()):
        t = raw.strip()
        if not t or t == "-":
            continue
        low = t.lower()
        if t in HW:
            e["hw"] = t
        elif low in TYPES:
            e["type"] = low
        elif re.fullmatch(r"\.[a-z0-9]{2,8}", low):
            if low not in e["formats"]:
                e["formats"].append(low)
        elif low in CHANNELS:
            e["channel"] = low
        elif low in ("link", "hosted"):
            e["delivery"] = low
        elif low == "keep":
            e["keep"] = True
        elif re.match(r"(fork|clone|template):.+", t, re.I):
            e["relation"] = t.split(":", 1)[0].lower() + ":" + t.split(":", 1)[1].strip()
        elif re.fullmatch(r"fw:\d{3,4}-\d{3,4}", low):
            e["fw"] = low[3:]
        elif re.fullmatch(r"fw:\d{3,4}(,\d{3,4})+", low) or re.fullmatch(r"fw:\d{3,4}", low):
            e["fw_list"] = low[3:].split(",")
        elif re.fullmatch(r"!fw:\d{3,4}(,\d{3,4})*", low):
            e["fw_not"] = low[4:].split(",")
        elif re.fullmatch(r"port:\d{2,5}(,\d{2,5})*", low):
            e["ports"] = low[5:].split(",")
        elif low.startswith("needs:") and len(t) > 6:
            e["needs"] += [x.strip() for x in t[6:].split(",") if x.strip()]
        else:
            e["extras_unknown"].append(t)


def extras_line(e: dict) -> str:
    p = []
    if e.get("hw"):
        p.append(e["hw"])
    if e.get("type"):
        p.append(e["type"])
    if e.get("relation"):
        p.append(e["relation"])
    p += e.get("formats", [])
    if e.get("channel"):
        p.append(e["channel"])
    if e.get("fw"):
        p.append("fw:" + e["fw"])
    if e.get("fw_list"):
        p.append("fw:" + ",".join(e["fw_list"]))
    if e.get("fw_not"):
        p.append("!fw:" + ",".join(e["fw_not"]))
    if e.get("ports"):
        p.append("port:" + ",".join(e["ports"]))
    if e.get("delivery"):
        p.append(e["delivery"])
    if e.get("keep"):
        p.append("keep")
    for n in e.get("needs", []):
        p.append("needs:" + n)
    p += e.get("extras_unknown", [])
    return " | ".join(p)


def tags_line(e: dict) -> str:
    tags = " ".join("#" + t for t in e.get("tags", []))
    return f"#{cat_tag(e.get('category') or 'Unknown')}" + (f" - {tags}" if tags else "")


# ---------- markdown (new block format) ----------
FIELD_RE = re.compile(r"^-\s+\*\*(\w+):\*\*\s*(.*)$")


def split_blocks(text: str):
    section, cur, fence = "General", None, False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        if line.startswith("## "):
            section, cur = line[3:].strip(), None
        elif line.startswith("### "):
            cur = {"head": line[4:].strip(), "section": section, "f": {}}
            yield cur
        elif cur is not None:
            m = FIELD_RE.match(line)
            if m:
                cur["f"][m.group(1)] = m.group(2).strip()


def parse_md(text: str) -> list[dict]:
    """New block format. Old tracker blocks are detected (Author/Variant lines) and converted."""
    out = []
    for b in list(split_blocks(text)):
        f = b["f"]
        if not f.get("URL") and not f.get("Tags"):
            continue  # prose heading, not a block
        if "Variant" in f or ("Author" in f and "By" not in f) or "Extras" not in f and re.search(r"#P5U|#payload", f.get("Tags", "")):
            out.append(convert_legacy(b))
            continue
        name = re.sub(r"\s+\([^()]*\)$", "", b["head"]) or b["head"]
        url = f.get("URL", "")
        url = url if url.startswith("http") else ""
        by = f.get("By", "")
        author, _, variant = [x.strip() for x in by.partition("/")]
        author = author or owner_of(url)
        variant = variant or author
        e = new_entry(name=name, url=url, author=author, variant=variant, section=b["section"],
                      desc=f.get("Desc", ""), notes=f.get("Notes", ""),
                      removed=f.get("Status", "").lower() == "removed")
        tl = f.get("Tags", "")
        head, sep, rest = tl.partition(" - ")
        first = head.strip().lstrip("#")
        if sep or first.lower() in TAG2CAT:
            e["category"] = TAG2CAT.get(first.lower(), "Unknown")
            if first.lower() not in TAG2CAT:
                e["flags"].append(f"category '{first}' not recognised")
            tl = rest
        else:
            e["flags"].append("no category")
        e["tags"] = [t.lstrip("#") for t in tl.split() if t.startswith("#")]
        parse_extras(f.get("Extras", ""), e)
        e["id"] = make_id(name, variant)
        out.append(e)
    return out


def to_md(d: dict) -> str:
    lines = ["# PLUZ5 Library", "", f"_{POWERED}. Generated from `PLUZ5-infos.json`; edit it with `web/library.html`. Block format: `docs/BLOCK-FORMAT.md`._", ""]
    sections: dict[str, list] = {}
    for e in d["entries"]:
        sections.setdefault(e.get("section") or "General", []).append(e)
    for sec, items in sections.items():
        lines += [f"## {sec}", ""]
        for e in items:
            lines.append(f"### {e['name']}")
            lines.append(f"- **URL:** {e.get('url') or '(none)'}")
            by = e.get("author") or ""
            if e.get("variant") and e["variant"] != e.get("author"):
                by += f" / {e['variant']}"
            if by:
                lines.append(f"- **By:** {by}")
            if e.get("desc"):
                lines.append(f"- **Desc:** {e['desc']}")
            lines.append(f"- **Tags:** {tags_line(e)}")
            x = extras_line(e)
            if x:
                lines.append(f"- **Extras:** {x}")
            if e.get("notes"):
                lines.append(f"- **Notes:** {e['notes']}")
            if e.get("removed"):
                lines.append("- **Status:** removed")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


# ---------- legacy tracker -> new block ----------
TAGCAT = [  # first match wins
    ("Activation & Spoof", {"activator", "account", "spoof", "np"}),
    ("Kernel", {"hen", "kstuff", "onionhen", "etahen", "fself", "jailbreak"}),
    ("Linux", {"linux"}),
    ("Debug & SDK", {"sdk", "dumper", "kdump", "debug", "dev", "diagnostic"}),
    ("Media", {"media", "video", "player", "stremio", "iptv", "nuvio", "wallpaper", "theme", "homescreen", "visual", "boot-anim"}),
    ("Game Tools", {"shadowmount", "mount", "ffpkg", "cheats", "patches", "patch", "trainer", "saves", "save", "emu", "emulator", "recomp", "eden", "games", "updater"}),
    ("File Management", {"file-manager", "pfs", "exfat", "ffpfsc", "compression", "lz4", "zstd", "archive", "usb", "conversion", "backup"}),
    ("Network", {"ftp", "network", "dns", "smb", "dlna", "sender", "http", "transfer", "dpi", "nas"}),
    ("System Utility", {"manager", "autoload", "fan-control", "power", "led", "reboot", "menu", "welcome-hub", "toolbox", "pldmgr", "overlay", "tesla", "plugin"}),
]
SECCAT = {"Payload Senders": "Network", "Autoloaders": "Kernel", "File Managers": "File Management",
          "Overlays": "System Utility", "Themes": "Media", "Media": "Media", "Linux": "Linux",
          "Emulators": "Game Tools", "Stores": "Game Tools", "Payload Mirrors": "System Utility",
          "Game / Library": "File Management", "WebKit": "Kernel", "Core Payload": "System Utility"}
KNOWN_REL = {"https://github.com/drakmor/kstuff-lite": "fork:EchoStretch"}
NON_TAG = {"p5", "p5p", "p5u", "ps4", "android", "ios", "ha", "pc", "port"}


def convert_legacy(b: dict) -> dict:
    f, flags = b["f"], []
    name = re.sub(r"\s+\([^()]*\)$", "", b["head"]) or b["head"]
    url = f.get("URL", "")
    url_ok = url.startswith("http")
    url = url if url_ok else ""
    author = f.get("Author") or owner_of(url)
    variant = f.get("Variant") or author
    tags = [t.lstrip("#") for t in f.get("Tags", "").split() if t.startswith("#")]
    low = [t.lower() for t in tags]
    notes = f.get("Notes", "")
    desc = f.get("Desc", "")
    e = new_entry(name=name, url=url, author=author, variant=variant, section=b["section"], desc=desc)
    # hardware
    for h in ("P5P", "P5U", "P5"):
        if h.lower() in low:
            e["hw"] = h
            break
    # ports
    e["ports"] = sorted({t[5:] for t in low if re.fullmatch(r"port-\d{2,5}", t)}, key=int)
    # type
    s = set(low)
    if "exploit" in s or "mast1c0re" in s or "y2jb" in s or b["section"].startswith(("Autoloaders", "WebKit")) and "payload" not in s and "autoload" not in s:
        e["type"] = "exploit"
    elif "sender" in s:
        e["type"] = "sender"
    elif "store" in s:
        e["type"] = "store"
    elif "native-app" in s:
        e["type"] = "app"
    elif "payload" in s:
        e["type"] = "payload"
    elif "tool" in s:
        e["type"] = "tool"
    elif s & {"mirror", "hub", "catalog", "links", "releases", "collection"}:
        e["type"] = "reference"
    else:
        e["type"] = "tool"
        flags.append("type guessed (tool)")
    # formats from notes: Binary: `x.ext`
    fm = re.findall(r"Binary[^`]*`[^`]*?(\.(?:elf|bin|pkg|lz4|ffpfsc|sprx))(?:\]|`)", notes)
    fm += re.findall(r"`[^`\s]*?(\.(?:elf|bin|sprx))`", notes)
    for x in fm:
        if x not in e["formats"]:
            e["formats"].append(x)
    if "sprx" in s or "sprx" in notes.lower() and ".sprx" in e["formats"]:
        pass
    if e["type"] == "payload" and not e["formats"]:
        e["formats"] = [".elf"]
        flags.append("format .elf assumed")
    if e["type"] == "payload" and not url_ok:
        flags.append("no url")
    # category
    cat = None
    for c, ts in TAGCAT:
        if s & ts:
            cat = c
            break
    if not cat:
        for k, c in SECCAT.items():
            if b["section"].startswith(k):
                cat = c
                flags.append("category from section")
                break
    if not cat:
        cat = "Unknown"
        flags.append("category unknown")
    e["category"] = cat
    # firmware
    fwt = sorted({t[3:] for t in low if re.fullmatch(r"fw-\d{3,4}", t)})
    m = re.search(r"FW\s*(\d+)\.(\d\d)\s*[–-]\s*(\d+)\.(\d\d)", desc + " " + notes)
    if m:
        e["fw"] = f"{m.group(1)}{m.group(2)}-{m.group(3)}{m.group(4)}"
        flags.append("firmware read from text")
    elif fwt:
        e["fw_list"] = fwt
        flags.append("firmware from #fw tag")
    # relation / needs
    if norm_url(url) in KNOWN_REL:
        e["relation"] = KNOWN_REL[norm_url(url)]
    if "etaHEN" in desc + notes and e["type"] == "payload" and re.search(r"needs?|requires?", desc + notes, re.I):
        pass
    # related line
    rel = f.get("Related", "")
    if rel:
        notes = (notes + " Related: " + re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", rel)).strip()
    e["notes"] = notes
    # remaining tags
    drop = NON_TAG | {t for c, ts in TAGCAT for t in ts if False}
    e["tags"] = [t for t in tags if t.lower() not in drop and not re.fullmatch(r"(?i)port-\w+|fw-\d+|payload|sender|store|native-app|exploit", t)]
    if not url_ok and url:
        flags.append("url not https")
    if url and not is_repo(url):
        flags.append("not a repo url: Library only")
    e["flags"] = flags
    e["id"] = make_id(name, variant)
    return e


# ---------- xlsx (stdlib only) ----------
HEAD = ["Name", "Variant", "Author", "Category", "Type", "HW", "Formats", "Relation", "Channel", "FW", "Not FW", "Ports",
        "Delivery", "Keep", "Needs", "Section", "URL", "Tags", "Desc", "Notes", "Flags", "Status", "Id"]
WIDTH = [28, 12, 16, 18, 10, 6, 10, 18, 8, 12, 12, 12, 9, 6, 16, 24, 46, 36, 58, 58, 30, 9, 30]


def _col(i: int) -> str:
    s = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def _esc(s) -> str:
    s = str(s if s is not None else "")
    s = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", s)
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def row_of(e: dict) -> list:
    return [e.get("name"), e.get("variant"), e.get("author"), e.get("category"), e.get("type"), e.get("hw"),
            " ".join(e.get("formats", [])), e.get("relation"), e.get("channel"),
            e.get("fw") or ",".join(e.get("fw_list", [])), ",".join(e.get("fw_not", [])), ",".join(e.get("ports", [])),
            e.get("delivery"), "keep" if e.get("keep") else "", ",".join(e.get("needs", [])), e.get("section"),
            e.get("url"), " ".join("#" + t for t in e.get("tags", [])), e.get("desc"), e.get("notes"),
            "; ".join(e.get("flags", []) + e.get("extras_unknown", [])), "removed" if e.get("removed") else "", e.get("id")]


def to_xlsx(d: dict, path: Path) -> None:
    rows = [HEAD] + [row_of(e) for e in d["entries"]]
    last = _col(len(HEAD) - 1)
    sheet = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
             '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">',
             '<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>',
             '<cols>' + "".join(f'<col min="{i+1}" max="{i+1}" width="{w}" customWidth="1"/>' for i, w in enumerate(WIDTH)) + '</cols>',
             '<sheetData>']
    for r, row in enumerate(rows, 1):
        st = ' s="1"' if r == 1 else ""
        cells = "".join(f'<c r="{_col(c)}{r}" t="inlineStr"{st}><is><t xml:space="preserve">{_esc(v)}</t></is></c>' for c, v in enumerate(row))
        sheet.append(f'<row r="{r}">{cells}</row>')
    sheet.append('</sheetData>')
    sheet.append(f'<autoFilter ref="A1:{last}{len(rows)}"/></worksheet>')
    styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
              '<fonts count="2"><font><sz val="11"/><name val="Calibri"/></font><font><b/><sz val="11"/><name val="Calibri"/></font></fonts>'
              '<fills count="2"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill></fills>'
              '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
              '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
              '<cellXfs count="2"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'
              '<xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/></cellXfs></styleSheet>')
    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
          '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
          '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/></Types>')
    rel = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
           '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')
    wb = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
          'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Library" sheetId="1" r:id="rId1"/></sheets></workbook>')
    wbr = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
           '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
           '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>')
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", rel)
        z.writestr("xl/workbook.xml", wb)
        z.writestr("xl/_rels/workbook.xml.rels", wbr)
        z.writestr("xl/styles.xml", styles)
        z.writestr("xl/worksheets/sheet1.xml", "".join(sheet))


# ---------- library <-> store ----------
def merge_entries(d: dict, new: list[dict]) -> int:
    have = {e["id"] for e in d["entries"]}
    n = 0
    for e in new:
        base, k = e["id"], 2
        if e["id"] in have:
            dup = next(x for x in d["entries"] if x["id"] == e["id"])
            if norm_url(dup.get("url")) == norm_url(e.get("url")):
                continue
            while e["id"] in have:
                e["id"], k = f"{base}-{k}", k + 1
        d["entries"].append(e)
        have.add(e["id"])
        n += 1
    return n


def store_ready(e: dict) -> bool:
    return (e.get("type") == "payload" and any(f in FMT_PAYLOAD for f in e.get("formats", []))
            and is_repo(e.get("url")) and not e.get("removed"))


def to_store_entry(e: dict) -> dict:
    fw_min = fw_max = None
    if e.get("fw"):
        a, b = e["fw"].split("-")
        fw_min, fw_max = fw_fmt(a), fw_fmt(b)
    elif e.get("fw_list"):
        fw_min, fw_max = fw_fmt(min(e["fw_list"], key=int)), fw_fmt(max(e["fw_list"], key=int))
    note = e.get("notes") or ""
    if e.get("relation"):
        note = (f"{e['relation'].replace(':', ' of ')}. " + note).strip()
    if e.get("needs"):
        note = (note + " Needs: " + ", ".join(e["needs"]) + ".").strip()
    r = {"display_name": e["name"] if e["variant"] == e["author"] else f"{e['name']} ({e['variant']})",
         "source_repo": e["url"], "author": e.get("author") or owner_of(e["url"]),
         "author_url": f"https://github.com/{owner_of(e['url'])}", "backup_url": None,
         "category": e.get("category") or "Unknown", "channel": e.get("channel") or "stable",
         "fw_min": fw_min, "fw_max": fw_max, "port": int(e["ports"][0]) if e.get("ports") else None,
         "protected_fallback": bool(e.get("keep")), "note": note}
    if e.get("hw"):
        r["hw_target"] = e["hw"]
    if len(e.get("ports", [])) > 1:
        r["ports"] = [int(p) for p in e["ports"]]
    if e.get("fw_list") and len(e["fw_list"]) > 1:
        r["fw_list"] = e["fw_list"]
    if e.get("fw_not"):
        r["fw_not"] = e["fw_not"]
    if e.get("delivery") == "hosted":
        r["delivery"] = "hosted"
    if e["formats"] and e["formats"][0] == ".bin" and ".elf" not in e["formats"]:
        r["asset_pattern"] = "*.bin"
    return r


def store_key(e: dict) -> tuple[str, str]:
    return slug(e["name"]), ("default" if e["variant"] == e["author"] else slug(e["variant"]))


def sync_store(d: dict, registry: dict) -> int:
    urls = {norm_url(e.get("url")) for e in d["entries"] if e.get("url")}
    new = []
    for ident, ent in registry.get("payloads", {}).items():
        for var, r in ent.get("variants", {}).items():
            u = r.get("source_repo") or ""
            if not str(u).startswith("http") or norm_url(u) in urls:
                continue
            urls.add(norm_url(u))
            variant = (r.get("author") or owner_of(u) or "org") if var == "default" else var
            name = re.sub(r"\s+\([^()]*\)$", "", r.get("display_name") or ident) or ident
            fw = ""
            if r.get("fw_min") and r.get("fw_max"):
                fw = f"{fw_num(r['fw_min'])}-{fw_num(r['fw_max'])}"
            e = new_entry(id=make_id(name, variant), name=name, url=u, author=r.get("author") or owner_of(u),
                          variant=variant, section="From the Store", category=r.get("category") or "Unknown",
                          type="payload", formats=[".elf"], hw=r.get("hw_target") or "", channel=r.get("channel") or "",
                          fw=fw, ports=[str(r["port"])] if r.get("port") else [], keep=bool(r.get("protected_fallback")),
                          notes=r.get("note") or "", flags=["from the Store: format .elf assumed"])
            new.append(e)
    return merge_entries(d, new)


def add_to_store(d: dict, registry: dict) -> tuple[int, list[str]]:
    reg = registry.setdefault("payloads", {})
    have = {norm_url(r.get("source_repo")) for ent in reg.values() for r in ent.get("variants", {}).values()}
    n, skipped = 0, []
    for e in d["entries"]:
        if not store_ready(e):
            continue
        if norm_url(e["url"]) in have:
            skipped.append(e["name"])
            continue
        ident, var = store_key(e)
        ent = reg.setdefault(ident, {"variants": {}})
        k = var
        while k in ent["variants"]:
            k += "2"
        ent["variants"][k] = to_store_entry(e)
        have.add(norm_url(e["url"]))
        n += 1
    return n, skipped


def check(d: dict, log: Log) -> bool:
    ok, seen = True, set()
    for e in d["entries"]:
        if e.get("id") in seen:
            log.line(f"[FAIL] duplicate library id {e.get('id')}")
            ok = False
        seen.add(e.get("id"))
        if not e.get("name"):
            log.line(f"[FAIL] entry {e.get('id')} has no name")
            ok = False
        if e.get("url") and not str(e["url"]).startswith("https://"):
            log.line(f"[FAIL] {e['id']}: url must start with https://")
            ok = False
        if e.get("category") and e["category"] not in CATS:
            log.line(f"[FAIL] {e['id']}: category '{e['category']}' is not one of the 10")
            ok = False
        for x in e.get("extras_unknown", []):
            log.line(f"[WARN] {e['id']}: unknown Extras token '{x}' (kept, not used)")
    if ok:
        log.line(f"[OK  ] library: {len(d['entries'])} entries, ids unique")
    return ok


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="pluz infos")
    ap.add_argument("--import", dest="imp", help="markdown file with ### blocks to add")
    ap.add_argument("--sync-store", action="store_true", help="add Library entries for Store entries that have none")
    ap.add_argument("--to-store", action="store_true", help="add Store entries for Store-ready Library blocks")
    ap.add_argument("--check", action="store_true", help="validate only, write nothing")
    a = ap.parse_args(argv)
    root = repo_root()
    cfg = load_config(root)
    dp = root / "data" / "PLUZ5-infos.json"
    d = load_infos(dp)
    with Log(root, "pluz_infos") as log:
        if a.check:
            return 0 if check(d, log) else 1
        if a.imp:
            n = merge_entries(d, parse_md(Path(a.imp).read_text(encoding="utf-8")))
            log.line(f"imported {n} new entr{'y' if n == 1 else 'ies'} from {a.imp}")
        if a.sync_store:
            n = sync_store(d, cfg["registry"])
            log.line(f"added {n} Library entr{'y' if n == 1 else 'ies'} from the Store")
        if a.to_store:
            n, sk = add_to_store(d, cfg["registry"])
            (root / "configs" / "payload_registry.json").write_text(
                json.dumps(cfg["registry"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            log.line(f"added {n} Store entr{'y' if n == 1 else 'ies'}; {len(sk)} already in the Store")
        if not check(d, log):
            return 1
        save_infos(dp, d)
        (root / "data" / "PLUZ5-infos.md").write_text(to_md(d), encoding="utf-8")
        to_xlsx(d, root / "data" / "PLUZ5-infos.xlsx")
        log.line("wrote data/PLUZ5-infos.json, .md, .xlsx")
    return 0


if __name__ == "__main__":
    sys.exit(main())
