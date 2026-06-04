# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A collection of game-data packs for **L5RCM** (Legend of the Five Rings Character Manager). The "code" is mostly XML game data (clans, families, schools, skills, merits, flaws, spells, katas, kihos, weapons, etc.). Python scripts validate and zip each pack into a distributable `.l5rcmpack` file (a renamed ZIP).

## Repository layout

- `packs/<pack_name>/` — one directory per pack. Always contains a `manifest` (JSON) plus XML data, either under a subfolder matching the manifest `id` (e.g. `core_pack/core/`) or under `xml/`. Both layouts are supported by the loader.
- `scripts/` — Python build/validation tooling.
- `scripts/dal/` — **git submodule** pointing at [`OpenNingia/l5rcm-data-access`](https://github.com/OpenNingia/l5rcm-data-access) (tag `v1.3.1`). Provides the **`l5rdal`** Python 3 package (the parser the app itself uses) for loading and validating pack content. Run `git submodule update --init` after cloning; the tooling also needs `lxml` (`pip install lxml`).
- `scripts/packlib.py`, `scripts/packlint.py`, `scripts/packbuild.py` — the linter + deterministic builder. See `docs/CONVENTIONS.md`.
- `contents/*.md` — human-readable summaries of each pack. Historically auto-generated via `l5rdal`'s `report.ContentToMarkDown` (needs `jinja2` + the app's `l5rcm` templates); the build tooling here does **not** regenerate them.
- `.github/workflows/main.yml` — CI: builds every pack on push to `master`; on tags matching `v*` it creates a draft GitHub Release and uploads each `.l5rcmpack` as an asset.

## Common commands

A single cross-platform Python builder + linter replaces the old
`makepack.bat`/`makepack.sh`/`make_pack_ci.sh`/`dal_check.py` scripts. Both run
under Python 3 and use the `l5rdal` submodule as the schema source of truth.

Lint (manifest, XML, schema/referential integrity, hygiene):
```
python scripts/packlint.py --all                 # every pack
python scripts/packlint.py packs/<pack_name>      # one pack
python scripts/packlint.py --all --fix            # auto-format XML hygiene
python scripts/packlint.py --all --strict --json  # CI-friendly machine output
```

Build deterministic `.l5rcmpack` files (the linter runs first; errors block):
```
python scripts/packbuild.py --all --validate      # build all + confirm installable
python scripts/packbuild.py <pack_name>           # one pack
```

The output name is derived from the manifest (`<id>-<version>[-<language>].l5rcmpack`)
so the published asset matches the directory the app installs into. Cross-pack
references are resolved against `core_pack` automatically (`--with-core PATH` to
override, `--no-core` to skip). The output `.l5rcmpack` files land in `packs/`
(override with `--out-dir`) and are gitignored. Conventions & severity model:
see `docs/CONVENTIONS.md`.

## Pack architecture

### Manifest (`packs/<pack>/manifest`)
JSON with required fields enforced by `packlint.py`:
- `id` — short slug (`[a-z0-9_]+`, no `_pack` suffix); the install-dir / catalog key — keep it stable.
- `version` — must match `^\d{1,2}\.\d{1,2}(\.\d{1,2})?$` (e.g. `5.1`, `1.6.0`).
- `display_name` — required.
- `authors`, `min-cm-version` — warnings if missing/malformed.
- Optional `language` (e.g. `en_US`) — when present, gets appended to the built filename: `<id>-<version>-<language>.l5rcmpack`.

### XML data
Every data file is `<?xml version="1.0" encoding="utf-8"?>` with a single `<L5RCM>` root. The loader recognises these child elements: `Clan`, `Family`, `School`, `SkillDef`, `SpellDef`, `Merit`, `Flaw`, `SkillCateg`, `KataDef`, `KihoDef`, `PerkCateg`, `EffectDef`, `Weapon`, `Armor`, `RingDef`, `TraitDef` (anything else is silently ignored). Records reference each other by `id` strings (e.g. a School's `clanid` must match a `<Clan id="...">` in the loaded pack set). ids are unique per type within a pack — duplicates are silently overwritten by `l5rdal`, so `packlint.py` reports them as errors.

### Cross-pack references
Most non-core packs reference `core_pack` definitions (clans, traits, rings, base skills). `packlint.py`/`packbuild.py` resolve references against `core_pack` automatically; use `--with-core PATH` to point at a different core (or `--no-core` to skip). `l5rdal.Data` takes a list of paths and loads them together as a unified reference graph.

## Editing conventions

- Keep IDs lowercase snake_case and stable — they're foreign keys across many files (and the install-dir / catalog key).
- When adding a new school, family, kata, etc., grep an existing equivalent in `packs/core_pack/` first to match the exact XML shape (attributes vs child elements vary by record type).
- After non-trivial changes, run `python scripts/packlint.py packs/<pack_name>` before committing (errors must be clean; review warnings).
- Release flow: tag the commit `vX.Y` on `master` — CI lints, builds every pack deterministically and attaches them to a draft release. Don't manually upload pack files.
