# PLUZ5 block format (Library)

One block describes one source. It is short on purpose: six lines, one of them a row of typed tokens.
The same block is shown as text (`PLUZ5-infos.md`), stored as json (`PLUZ5-infos.json`) and as one row in `PLUZ5-infos.xlsx`.

## The block

```markdown
### kstuff-lite
- **URL:** https://github.com/drakmor/kstuff-lite
- **By:** drakmor / Drakmor
- **Desc:** Fork of kstuff-lite with faster startup and better fpkg/FSELF handling.
- **Tags:** #Kernel - #kstuff #fself
- **Extras:** P5U | payload | fork:EchoStretch | .elf | stable | fw:760-1200 | !fw:960,1200 | port:9021 | link
- **Notes:** Alternative optimized build.
```

## Lines

| Line | What goes in it | Needed? |
|---|---|---|
| `### Name` | Short name of the tool | **Yes** |
| **URL** | Home of the project (https). `(none)` if there is none | **Yes** |
| **By** | `author / Variant`. Author = repo owner. Variant = who made *this build* (leave out for the original) | No (author is read from the URL) |
| **Desc** | One sentence: what the tool is | Recommended |
| **Tags** | `#Category - #tag #tag`. The word before ` - ` is the category | **Yes** (category) |
| **Extras** | Typed tokens separated by a vertical bar (see below) | Needed for the Store |
| **Notes** | Facts about *this build* only: quirks, paths, versions | No |

Categories (pick one): `Kernel` `Network` `File Management` `Game Tools` `Media` `System Utility` `Debug & SDK` `Linux` `Activation & Spoof` `Unknown`.
Write them with no spaces or `&` in tags: `#Kernel`, `#File-Management`, `#Debug-SDK`, `#Activation-Spoof`, `#System-Utility`, `#Game-Tools`.

## Extras: tokens

Order does not matter. One token = one fact. No spaces inside a token (use `-`). Unknown = leave the token out (never guess).

| Token | Meaning | Values / examples |
|---|---|---|
| Hardware | console model | `P5` regular/slim only, `P5P` PS5 Pro, `P5U` both |
| Type | what it is | `payload` `app` `pkg` `tool` `sender` `exploit` `store` `reference` |
| Format | file type; also decides which registry gets it | `.elf` `.bin` (payload registry), `.pkg` `.lz4` `.ffpfsc` ... |
| Relation | how it relates to another source | `fork:Name` `clone:Name` `template:Name` |
| Channel | release track | `stable` `beta` `alpha` |
| Firmware | works on | `fw:760-1200` range (7.60 to 12.00), `fw:760,900,1200` list. No dots |
| Not firmware | does **not** work on | `!fw:960,1200` (the `!` means "not") |
| Port | ports it uses, one by one | `port:9021` or `port:8000,8001`. No ranges |
| Delivery | where the app/payload is downloaded from | `link` (author's release) or `hosted` (copy in our repo) |
| Keep | never delete old builds | `keep` |
| Needs | requires another tool | `needs:etaHEN` `needs:ShadowMountPlus` |

Firmware numbers are written without the dot: 7.60 = `760`, 12.00 = `1200`.
Anything the page does not recognise is shown with a warning, never dropped.

## What is totally necessary (the minimum)

Three things make a valid Library block:

```markdown
### MyTool
- **URL:** https://github.com/someone/mytool
- **Tags:** #Unknown
```

Everything else is filled in later. The info % in the page shows how complete each block is.

## Store-ready (adds Extras)

To put a source in the Store (what pldmgr serves) it also needs a Type and a Format, so the right registry gets it:

```markdown
### MyTool
- **URL:** https://github.com/someone/mytool
- **Tags:** #Network - #diagnostic
- **Extras:** payload | .elf
```

Defaults when left out: channel `stable`, delivery `link`, hardware not stated.

## Full example

```markdown
### ShadowMountPlus
- **URL:** https://github.com/drakmor/ShadowMountPlus
- **By:** drakmor
- **Desc:** Background auto-mounter: detects, mounts and installs game backups from internal or external storage.
- **Tags:** #Game-Tools - #mount #shadowmount #automation
- **Extras:** P5U | payload | .elf | stable | fw:760-1200 | port:9021 | link | keep
- **Notes:** Original release. Core for the game library workflow.
```

## Where each token goes

| Token | Store json (`payload_registry.json`) |
|---|---|
| Hardware | `hw_target` |
| Format `.elf/.bin` | decides the registry (payload) and the asset search |
| Channel | `channel` |
| `fw:` | `fw_min`, `fw_max` (a list is kept as `fw_list`) |
| `!fw:` | `fw_not` (kept in our json; pldmgr ignores it) |
| `port:` | `port` (first) and `ports` (all) |
| Delivery / Keep | mode per entry / `protected_fallback` |
| Relation / Needs | note text in the Store, full detail in the Library |

Computed values (SHA-256, size, build file name, last-checked date) are never typed. The workflow writes them into the json and the `.xlsx`.

## Icons (pldmgr)

Nothing to type. The workflow draws one icon per payload (category colour + two initials) and writes
`manifests/PLUZ-ps5-Icons.json`; every manifest carries `icons_url` and each payload an `icon_key`
(SHA-256 of the icon, the same scheme as pldmgr's own test files). Turn off with `"icons": false` in `configs/settings.json`.
Custom artwork can be added later by replacing an entry in the icons file with your own `data:image/png;base64,...` string.
