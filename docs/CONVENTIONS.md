# Datapack conventions

This document defines the rules enforced by the tooling in `scripts/`
(`packlint.py` and `packbuild.py`). The schema "source of truth" is the
`l5rdal` package (the `scripts/dal` submodule, tag `v1.3.1`) — the very parser
the L5RCM app uses to load packs.

## Why the naming rule matters (the catalog ↔ install invariant)

A `.l5rcmpack` is a ZIP whose **root** holds a JSON file named exactly
`manifest`. When the app installs a pack it creates a directory named after the
manifest **`id`** and matches the online catalog entry by that same `id`.

Historically the published asset name was derived from the *source directory*
(`make_pack_ci.sh`) while the manifest `id` could differ (e.g. directory
`community_data_pack` vs id `community`, `lbs_pack` vs id `LBS`). The asset name
and the install directory then disagreed and the catalog ↔ installed match
broke.

**Rule:** the artifact name is always derived from the manifest:

```
<id>-<version>.l5rcmpack
<id>-<version>-<language>.l5rcmpack     # when a language is declared
```

`packbuild.py` derives the name from the manifest only — never from arguments
or the directory name — so the asset always matches what the app installs.

## Manifest

Required keys (errors if missing/wrong type):

| key            | type   | notes                                              |
|----------------|--------|----------------------------------------------------|
| `id`           | string | install-dir / catalog key; keep it stable          |
| `version`      | string | dotted-numeric `N.N[.N]` (e.g. `5.1`, `1.6.0`)     |
| `display_name` | string | human-readable name                                |

Optional keys: `language` (locale like `en_US`; absent = culture-invariant),
`authors` (list of strings), `update-uri`, `download-uri`,
`min-cm-version` (dotted-numeric). Unknown keys are flagged as warnings (typo
guard).

### id / slug rules

- The `id` should be a clean slug matching `^[a-z0-9_]+$`.
- It should **not** carry the redundant `_pack` suffix.
- Ideally the source directory name equals the `id`.

These are **warnings**, not errors: existing ids are kept stable on purpose
(changing an `id` changes the install directory and would orphan users'
already-installed data). The build still derives the filename from `id`, so the
catalog ↔ install match is correct regardless. (`core` is a special id: the app
routes `id == "core"` to its own data root, so it legitimately differs from the
`core_pack` directory.)

## XML content

- Every data file is `<?xml version="1.0" encoding="utf-8"?>` with a single
  `<L5RCM>` root.
- Recognised child elements: `Clan`, `Family`, `School`, `SkillDef`, `SpellDef`,
  `Merit`, `Flaw`, `SkillCateg`, `KataDef`, `KihoDef`, `PerkCateg`, `EffectDef`,
  `Weapon`, `Armor`, `RingDef`, `TraitDef`. Any other top-level element is
  silently ignored by the loader (flagged as a warning = dead data).
- Each record needs the required attributes for its type (e.g. `id`/`name`,
  `clanid`, `trait`, `type`); `page` must be an integer when present.
- **ids are unique per type within a pack.** `l5rdal` silently overwrites a
  record with a duplicate id (Weapon/Armor are keyed by `name`), so a duplicate
  is a hidden data-loss bug and is reported as an error.
- Cross-references must resolve against `core` + the pack (School → clan / skill
  / spell / starting merit-flaw; Family → clan / trait; Skill → category /
  trait; Perk → category; Weapon/Armor → skill / effect). `varies` is an
  accepted sentinel for Craft-skill traits.
- Formatting hygiene (warnings, auto-fixable with `--fix`): UTF-8 without BOM,
  LF line endings, no trailing whitespace, spaces (not tabs) for indentation, a
  final newline.

## Stat modifiers (`*_modifiers.xml`)

A pack may ship declarative, stat-changing effects (Armor TN, Reduction,
Initiative, rings/traits, Honor/Glory/Status, Insight, persistent roll bonuses,
formula substitutions) that attach to its existing records (techniques, kata,
kiho, tattoo, merits, flaws, ancestors, paths, mastery abilities, weapon/armor
effects) by `id`. The schema (`<ModifierDef>` and friends) is specified in
[`MODIFIERS_SCHEMA.md`](MODIFIERS_SCHEMA.md); `packs/core_pack/core/modifiers.xml`
is the reference example.

**Status:** schema frozen for authoring; `ModifierDef` is **not yet** in the
recognised-elements list above because runtime + lint enforcement land with the
matching `l5rdal` release. Until then the loader ignores a `*_modifiers.xml`
file harmlessly (unknown top-level element), so authoring one early is
forward-compatible but inert — a pack relying on it MUST bump `min-cm-version`.

## Package hygiene

A pack ships only its `manifest` and `.xml` files. VCS/OS/editor junk
(`.git`, `__pycache__`, `.DS_Store`, `Thumbs.db`, `*~`, dotfiles) and stray
files (e.g. `Missing.txt`, `manifest.bak`, committed `.l5rcmpack`) are flagged.
Entry names with path traversal (`..`), absolute paths or backslashes are
rejected (anti ZIP-slip, since the app extracts with `extractall`).

## Severity & exit codes

- **error** → blocks (`packlint` exits non-zero; `packbuild` refuses to build).
- **warning** → advisory; non-blocking unless `--strict` or `--max-warnings N`.
- `packlint` exit codes: `0` clean, `1` errors (or warnings under `--strict` /
  over threshold), `2` usage error.

## Commands

```bash
# lint
python scripts/packlint.py --all                  # every pack
python scripts/packlint.py packs/lbs_pack          # one pack
python scripts/packlint.py --all --fix             # auto-format XML hygiene
python scripts/packlint.py --all --strict --json   # CI-friendly

# build (deterministic; runs the linter first)
python scripts/packbuild.py --all --validate       # build + confirm installable
python scripts/packbuild.py core_pack              # one pack
```

Both tools need the `l5rdal` submodule and `lxml`:

```bash
git submodule update --init
pip install lxml
```
