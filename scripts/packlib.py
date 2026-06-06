#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
packlib.py - Shared library for the L5RCM datapack tooling.

Backs two CLIs:
  * packlint.py  - lints a pack (manifest, XML, schema/referential integrity, hygiene)
  * packbuild.py - builds a deterministic <id>-<version>.l5rcmpack archive

The schema "source of truth" is the ``l5rdal`` package shipped as the
``scripts/dal`` git submodule (tag v1.3.1). We reuse its parser
(``l5rdal.Data(..., exception=True)``) instead of reimplementing it, and we
mirror the cross-reference checks historically done by ``dal_check.py``.

No third-party dependency beyond what ``l5rdal`` itself needs (``lxml``).
"""

from __future__ import annotations

import json
import os
import re
import sys
import zipfile
from dataclasses import dataclass, field
from typing import Iterable, Optional

# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #

HERE = os.path.dirname(os.path.abspath(__file__))          # .../scripts
REPO_ROOT = os.path.dirname(HERE)                          # repo root
DAL_DIR = os.path.join(HERE, "dal")                        # l5rdal submodule root
DEFAULT_PACKS_DIR = os.path.join(REPO_ROOT, "packs")
DEFAULT_CORE_DIR = os.path.join(DEFAULT_PACKS_DIR, "core_pack")

# --------------------------------------------------------------------------- #
# Format constants (verified against l5rdal v1.3.1 build_from_xml methods)
# --------------------------------------------------------------------------- #

# Child tags recognised by the loader (l5rdal.Data.__load_xml). Anything else
# under <L5RCM> is silently ignored by the app == dead data.
RECOGNIZED_TAGS = (
    "Clan", "Family", "School", "SkillDef", "SpellDef", "Merit", "Flaw",
    "SkillCateg", "KataDef", "KihoDef", "PerkCateg", "EffectDef", "Weapon",
    "Armor", "RingDef", "TraitDef",
    # ModifierDef is recognised by l5rdal >= 1.4.0. The generic structural loop
    # does nothing for it (no required attrs / id); its schema is validated by
    # check_modifiers(). Listed here so it is not flagged as an unknown tag.
    "ModifierDef",
)

# Attributes that build_from_xml reads via elem.attrib[...] (raise if missing).
REQUIRED_ATTRS = {
    "Clan": ("id", "name"),
    "Family": ("id", "name", "clanid"),
    "School": ("id", "name", "clanid"),          # read_attribute -> None, but semantically required
    "SkillDef": ("id", "name", "trait", "type"),
    "SpellDef": ("id",),
    "Merit": ("id", "name", "type"),
    "Flaw": ("id", "name", "type"),
    "SkillCateg": ("id",),
    "KataDef": ("id",),
    "KihoDef": ("id",),
    "PerkCateg": ("id",),
    "EffectDef": ("id",),
    "Weapon": ("name",),
    "Armor": ("name", "tn", "rd", "cost"),
    "RingDef": ("id",),
    "TraitDef": ("id",),
}

# Sub-elements whose absence makes build_from_xml crash (elem.find(x).iter()/.text).
REQUIRED_SUBELEMENTS = {
    "Family": ("Trait",),
    "School": ("Tags", "Skills", "Techs", "Spells"),
    "Weapon": ("Tags",),
}

# Integer-typed attributes (int(elem.attrib[...]) at load time).
INT_ATTRS = {
    "Armor": ("tn", "rd"),
    "Weapon": ("strength", "min_strength"),
}

# Loader collection each tag feeds into (used for per-type id uniqueness).
TAG_COLLECTION = {
    "Clan": "clans", "Family": "families", "School": "schools",
    "SkillDef": "skills", "SpellDef": "spells", "Merit": "merits",
    "Flaw": "flaws", "SkillCateg": "skcategs", "KataDef": "katas",
    "KihoDef": "kihos", "PerkCateg": "perktypes", "EffectDef": "weapon_effects",
    "Weapon": "weapons", "Armor": "armors", "RingDef": "rings",
    "TraitDef": "traits",
}

# Identity field per type (everything is keyed by id except Weapon/Armor, which
# l5rdal keys by name for idempotent loading).
IDENTITY_ATTR = {"Weapon": "name", "Armor": "name"}

# Manifest keys
MANIFEST_KNOWN_KEYS = (
    "id", "display_name", "language", "authors", "version",
    "update-uri", "download-uri", "min-cm-version",
)
MANIFEST_REQUIRED = ("id", "version", "display_name")

# Regexes
SLUG_RE = re.compile(r"^[a-z0-9_]+$")
VERSION_RE = re.compile(r"^\d{1,2}\.\d{1,2}(\.\d{1,2})?$")
LOCALE_RE = re.compile(r"^[a-z]{2}_[A-Z]{2}$")
XML_DECL_RE = re.compile(r"^<\?xml[^>]*\bencoding=[\"']([^\"']+)[\"']", re.IGNORECASE)
CANONICAL_DECL = '<?xml version="1.0" encoding="utf-8"?>'

# Hygiene
JUNK_DIR_NAMES = {".git", ".svn", ".hg", "__pycache__", ".idea", ".vs"}
JUNK_FILE_NAMES = {".DS_Store", "Thumbs.db"}

# Special non-ring element keywords tolerated on spells.
SPELL_ELEMENT_EXTRA = {"multi", "all", "none", "void"}

# Sentinel skill trait used by "Craft" skills whose trait varies by craft type.
# It is a deliberate convention in core data, not an unresolved reference.
SKILL_TRAIT_EXTRA = {"varies"}

# --------------------------------------------------------------------------- #
# Stat-modifier schema (docs/MODIFIERS_SCHEMA.md v1) constants
# --------------------------------------------------------------------------- #

MOD_KINDS = {
    "tech", "kata", "kiho", "tattoo", "merit", "flaw", "ancestor", "path",
    "mastery", "weapon_effect", "armor",
}

# affects that carry a roll/keep/bonus triple ...
MOD_ROLL_AFFECTS = {
    "any_roll", "skill_roll", "attack_roll", "damage_roll", "trait_roll", "ring_roll",
}
# ... and those that carry a single scalar `value`.
MOD_SCALAR_AFFECTS = {
    "armor_tn", "reduction", "wound_penalty", "health_rank", "insight",
    "honor", "glory", "status", "void_max", "trait_rank", "ring_rank",
    "spell_tn_self",
}
# initiative accepts either shape.
MOD_BOTH_AFFECTS = {"initiative"}
MOD_ALL_AFFECTS = MOD_ROLL_AFFECTS | MOD_SCALAR_AFFECTS | MOD_BOTH_AFFECTS

MOD_OPS = {"add", "set", "min", "max"}

MOD_WHEN_VOCAB = {
    "auto",
    # generic player-controlled on/off for effects that are switched on rather
    # than tied to a specific stance (e.g. an activated Kiho/Kata).
    "activated",
    "defense_stance", "full_defense_stance", "attack_stance",
    "full_attack_stance", "center_stance",
    "mounted", "vs_lower_initiative", "first_round", "grappling",
    "maneuver_increased_damage", "maneuver_called_shot", "maneuver_knockdown",
    "maneuver_feint", "maneuver_disarm",
}

MOD_DETAIL_PREFIXES = {"skill", "weapon", "trait", "ring", "tag"}

# affects that *require* a `detail` selector (meaningless without a target).
# skill_roll / attack_roll / damage_roll take an OPTIONAL detail: omitting it
# means "applies to all skills / attacks / weapons" (a general bonus); a detail
# only narrows the scope.
MOD_DETAIL_REQUIRED = {"trait_roll", "ring_roll", "trait_rank", "ring_rank"}

# affects a <Substitute> may target.
MOD_SUBSTITUTABLE = {
    "initiative", "attack_roll", "damage_roll", "trait_roll", "skill_roll",
}

# Value-DSL facade (see docs/MODIFIERS_SCHEMA.md §9). rings/traits are small and
# stable, so we validate their members; skills.* / skill('id') are lenient.
MOD_RINGS = {"air", "earth", "fire", "water", "void"}
MOD_TRAITS = {
    "agility", "awareness", "intelligence", "perception",
    "reflexes", "stamina", "strength", "willpower",
}
MOD_VALUE_BARE = {"school_rank", "insight_rank", "honor", "glory", "status", "taint"}
MOD_VALUE_ATTR_ROOTS = {"rings", "traits", "skills"}
MOD_VALUE_FUNCS = {"min", "max", "floor", "ceil", "abs", "round",
                   "skill", "merit_rank", "flaw_rank"}

# requires-predicate facade (see docs/MODIFIERS_SCHEMA.md §10). has_kiho /
# has_tattoo may appear either bare ("not has_kiho" = owns any) or as a call
# ("has_kiho('slug')" = owns that one), so they are in both sets.
MOD_PRED_BARE = ({"unarmored", "in_light_armor", "in_heavy_armor",
                  "has_kiho", "has_tattoo"} | MOD_VALUE_BARE)
MOD_PRED_FUNCS = {"wielding", "has_kiho", "has_tattoo"} | MOD_VALUE_FUNCS

MOD_PARAM_NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")

# --------------------------------------------------------------------------- #
# Findings
# --------------------------------------------------------------------------- #

SEV_ERROR = "error"
SEV_WARNING = "warning"


@dataclass
class Finding:
    severity: str
    code: str
    pack: str
    message: str
    file: Optional[str] = None      # path relative to repo root
    line: Optional[int] = None

    def to_dict(self) -> dict:
        return {
            "severity": self.severity, "code": self.code, "pack": self.pack,
            "message": self.message, "file": self.file, "line": self.line,
        }


def _err(pack, code, msg, file=None, line=None):
    return Finding(SEV_ERROR, code, pack, msg, file, line)


def _warn(pack, code, msg, file=None, line=None):
    return Finding(SEV_WARNING, code, pack, msg, file, line)


# --------------------------------------------------------------------------- #
# l5rdal bootstrap
# --------------------------------------------------------------------------- #

_L5RDAL = None


def import_l5rdal():
    """Import and return the l5rdal module from the scripts/dal submodule."""
    global _L5RDAL
    if _L5RDAL is not None:
        return _L5RDAL
    if DAL_DIR not in sys.path:
        sys.path.insert(0, DAL_DIR)
    try:
        import l5rdal  # type: ignore
    except ImportError as exc:
        raise SystemExit(
            "ERROR: cannot import 'l5rdal' from {dal}.\n"
            "  - run: git submodule update --init\n"
            "  - ensure lxml is installed: pip install lxml\n"
            "  detail: {exc}".format(dal=DAL_DIR, exc=exc)
        )
    # silence the noisy 'data' logger l5rdal uses
    import logging
    log = logging.getLogger("data")
    log.addHandler(logging.NullHandler())
    log.propagate = False
    _L5RDAL = l5rdal
    return l5rdal


# --------------------------------------------------------------------------- #
# Pack discovery / manifest
# --------------------------------------------------------------------------- #

@dataclass
class PackInfo:
    name: str                       # source directory name
    path: str                       # absolute path to the pack directory
    raw: Optional[dict] = None      # parsed manifest JSON
    manifest_error: Optional[str] = None

    @property
    def manifest_path(self) -> str:
        return os.path.join(self.path, "manifest")

    @property
    def id(self) -> Optional[str]:
        return self.raw.get("id") if isinstance(self.raw, dict) else None

    @property
    def version(self) -> Optional[str]:
        return self.raw.get("version") if isinstance(self.raw, dict) else None

    @property
    def language(self) -> Optional[str]:
        return self.raw.get("language") if isinstance(self.raw, dict) else None


def load_pack_info(pack_dir: str) -> PackInfo:
    pack_dir = os.path.abspath(pack_dir)
    info = PackInfo(name=os.path.basename(pack_dir.rstrip(os.sep)), path=pack_dir)
    mpath = os.path.join(pack_dir, "manifest")
    if not os.path.isfile(mpath):
        info.manifest_error = "manifest file not found at pack root"
        return info
    try:
        with open(mpath, "r", encoding="utf-8") as fp:
            info.raw = json.load(fp)
    except Exception as exc:
        info.manifest_error = "invalid JSON: {0}".format(exc)
    return info


def discover_packs(packs_dir: str = DEFAULT_PACKS_DIR) -> list[PackInfo]:
    out = []
    if not os.path.isdir(packs_dir):
        return out
    for name in sorted(os.listdir(packs_dir)):
        d = os.path.join(packs_dir, name)
        if os.path.isdir(d) and os.path.isfile(os.path.join(d, "manifest")):
            out.append(load_pack_info(d))
    return out


def output_filename(manifest: dict) -> str:
    """Deterministic artifact name: <id>-<version>[-<language>].l5rcmpack."""
    pid = manifest["id"]
    ver = manifest["version"]
    lang = manifest.get("language")
    stem = "{0}-{1}".format(pid, ver)
    if lang:
        stem = "{0}-{1}".format(stem, lang)
    return stem + ".l5rcmpack"


def rel_to_repo(path: str) -> str:
    try:
        return os.path.relpath(path, REPO_ROOT).replace(os.sep, "/")
    except ValueError:
        return path


# --------------------------------------------------------------------------- #
# File walking
# --------------------------------------------------------------------------- #

def _walk_files(pack_dir: str):
    """Yield (abspath, relpath_posix) for files, skipping junk directories."""
    for root, dirs, files in os.walk(pack_dir):
        dirs[:] = [d for d in dirs if d not in JUNK_DIR_NAMES]
        for f in files:
            ap = os.path.join(root, f)
            rp = os.path.relpath(ap, pack_dir).replace(os.sep, "/")
            yield ap, rp


def iter_payload_files(pack_dir: str) -> list[tuple[str, str]]:
    """Files that go into the .l5rcmpack: the manifest plus every .xml file.

    Returns a list of (abspath, arcname) sorted by arcname for reproducibility.
    """
    payload = []
    for ap, rp in _walk_files(pack_dir):
        base = os.path.basename(rp)
        if base.startswith(".") or base.endswith("~"):
            continue
        if rp == "manifest" or rp.lower().endswith(".xml"):
            payload.append((ap, rp))
    payload.sort(key=lambda t: t[1])
    return payload


# --------------------------------------------------------------------------- #
# XML hygiene (text-level) + --fix
# --------------------------------------------------------------------------- #

def _read_text_utf8(abs_path: str):
    raw = open(abs_path, "rb").read()
    try:
        return raw, raw.decode("utf-8"), None
    except UnicodeDecodeError as exc:
        return raw, None, str(exc)


def check_xml_hygiene(pack_name: str, abs_path: str, fix: bool = False) -> tuple[list[Finding], bool]:
    """Encoding/whitespace/EOL hygiene. With fix=True rewrites the file in a
    *non-destructive* way (declaration, EOL->LF, trailing ws, leading tabs,
    final newline). Never reflows element text content."""
    rel = rel_to_repo(abs_path)
    findings: list[Finding] = []
    raw, text, decode_err = _read_text_utf8(abs_path)

    if decode_err is not None:
        findings.append(_err(pack_name, "xml-not-utf8",
                             "file is not valid UTF-8: {0}".format(decode_err), rel))
        return findings, False

    had_bom = text.startswith("﻿")
    body = text[1:] if had_bom else text
    if had_bom:
        findings.append(_warn(pack_name, "xml-bom", "file starts with a UTF-8 BOM", rel))

    first_line = body.split("\n", 1)[0].lstrip("\r")
    m = XML_DECL_RE.match(first_line)
    if not first_line.startswith("<?xml"):
        findings.append(_warn(pack_name, "xml-no-declaration",
                              "missing <?xml ... ?> declaration", rel, 1))
    elif m and m.group(1).lower() not in ("utf-8", "utf8"):
        findings.append(_warn(pack_name, "xml-encoding",
                              "declared encoding is '{0}', expected utf-8".format(m.group(1)),
                              rel, 1))

    if "\r" in body:
        findings.append(_warn(pack_name, "xml-eol",
                              "non-LF line endings (CR/CRLF) present", rel))

    lines = body.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    trailing = [i + 1 for i, ln in enumerate(lines) if ln != ln.rstrip()]
    if trailing:
        findings.append(_warn(pack_name, "xml-trailing-ws",
                              "trailing whitespace on {0} line(s)".format(len(trailing)),
                              rel, trailing[0]))
    tabs = [i + 1 for i, ln in enumerate(lines)
            if ln[:len(ln) - len(ln.lstrip())].count("\t")]
    if tabs:
        findings.append(_warn(pack_name, "xml-tabs",
                              "tab characters used for indentation on {0} line(s)".format(len(tabs)),
                              rel, tabs[0]))
    if body and not body.endswith("\n"):
        findings.append(_warn(pack_name, "xml-final-newline",
                              "missing final newline", rel))

    changed = False
    if fix:
        new_text = _fix_xml_text(body)
        if new_text != text:
            with open(abs_path, "w", encoding="utf-8", newline="") as fp:
                fp.write(new_text)
            changed = True
    return findings, changed


def _fix_xml_text(body: str) -> str:
    body = body.replace("\r\n", "\n").replace("\r", "\n")
    out_lines = []
    for ln in body.split("\n"):
        # expand only *leading* tabs (2 spaces each), strip trailing whitespace
        stripped = ln.lstrip("\t")
        n_tabs = len(ln) - len(stripped)
        if n_tabs:
            ln = ("  " * n_tabs) + stripped
        out_lines.append(ln.rstrip())
    text = "\n".join(out_lines)
    # declaration
    first = text.split("\n", 1)[0]
    if not first.startswith("<?xml"):
        text = CANONICAL_DECL + "\n" + text
    else:
        m = XML_DECL_RE.match(first)
        if m and m.group(1).lower() not in ("utf-8", "utf8"):
            rest = text.split("\n", 1)[1] if "\n" in text else ""
            text = CANONICAL_DECL + ("\n" + rest if rest else "")
    if not text.endswith("\n"):
        text += "\n"
    return text


# --------------------------------------------------------------------------- #
# XML structural checks (element-level, with line numbers via lxml)
# --------------------------------------------------------------------------- #

def _is_int(val) -> bool:
    try:
        int(val)
        return True
    except (TypeError, ValueError):
        return False


def check_xml_structure(pack_name: str, abs_path: str):
    """Parse one XML file and validate structure.

    Returns (findings, identities) where identities is a list of
    (collection, identity_value, rel, line) for cross-file uniqueness.
    A leading well-formedness/root error returns ([...], []) and signals the
    caller that the pack cannot be loaded.
    """
    from lxml import etree
    rel = rel_to_repo(abs_path)
    findings: list[Finding] = []
    identities: list[tuple] = []

    try:
        tree = etree.parse(abs_path)
    except etree.XMLSyntaxError as exc:
        line = getattr(exc, "lineno", None) or (exc.position[0] if getattr(exc, "position", None) else None)
        findings.append(_err(pack_name, "xml-not-well-formed", str(exc), rel, line))
        return findings, identities, True  # fatal for this file
    except Exception as exc:
        findings.append(_err(pack_name, "xml-parse-error", str(exc), rel))
        return findings, identities, True

    root = tree.getroot()
    if root is None or root.tag != "L5RCM":
        findings.append(_err(pack_name, "xml-bad-root",
                             "root element is '{0}', expected 'L5RCM'".format(
                                 getattr(root, "tag", None)), rel,
                             getattr(root, "sourceline", None)))
        return findings, identities, True

    for elem in root:
        tag = elem.tag
        if not isinstance(tag, str):      # comment / PI
            continue
        line = elem.sourceline
        if tag not in RECOGNIZED_TAGS:
            findings.append(_warn(pack_name, "xml-unknown-tag",
                                  "unrecognised element <{0}> is ignored by the loader".format(tag),
                                  rel, line))
            continue

        # required attributes
        for attr in REQUIRED_ATTRS.get(tag, ()):  # type: ignore[arg-type]
            val = elem.attrib.get(attr)
            if val is None or val == "":
                findings.append(_err(pack_name, "missing-required-attr",
                                     "<{0}> missing required attribute '{1}'".format(tag, attr),
                                     rel, line))

        # integer attributes
        for attr in INT_ATTRS.get(tag, ()):  # type: ignore[arg-type]
            if attr in elem.attrib and not _is_int(elem.attrib[attr]):
                findings.append(_err(pack_name, "bad-int-attr",
                                     "<{0}> attribute '{1}'='{2}' is not an integer".format(
                                         tag, attr, elem.attrib[attr]), rel, line))

        # 'page' must be an int if present (read by the loader as book_page)
        if "page" in elem.attrib and not _is_int(elem.attrib["page"]):
            findings.append(_warn(pack_name, "bad-page",
                                  "<{0}> attribute 'page'='{1}' is not an integer".format(
                                      tag, elem.attrib["page"]), rel, line))

        # required sub-elements (their absence crashes build_from_xml)
        for sub in REQUIRED_SUBELEMENTS.get(tag, ()):  # type: ignore[arg-type]
            if elem.find(sub) is None:
                findings.append(_err(pack_name, "missing-required-subelement",
                                     "<{0}> missing required child <{1}>".format(tag, sub),
                                     rel, line))

        # collect identity for uniqueness
        id_attr = IDENTITY_ATTR.get(tag, "id")
        id_val = elem.attrib.get(id_attr)
        if id_val:
            identities.append((TAG_COLLECTION[tag], id_val, rel, line))

    return findings, identities, False


# --------------------------------------------------------------------------- #
# Manifest checks
# --------------------------------------------------------------------------- #

def check_manifest(pack: PackInfo) -> list[Finding]:
    rel = rel_to_repo(pack.manifest_path)
    findings: list[Finding] = []

    if pack.raw is None:
        findings.append(_err(pack.name, "manifest-invalid",
                             pack.manifest_error or "manifest missing or invalid", rel))
        return findings
    if not isinstance(pack.raw, dict):
        findings.append(_err(pack.name, "manifest-invalid",
                             "manifest is not a JSON object", rel))
        return findings

    raw = pack.raw

    for key in MANIFEST_REQUIRED:
        if key not in raw:
            findings.append(_err(pack.name, "manifest-missing-field",
                                 "missing required field '{0}'".format(key), rel))
        elif not isinstance(raw[key], str) or not raw[key].strip():
            findings.append(_err(pack.name, "manifest-bad-type",
                                 "field '{0}' must be a non-empty string".format(key), rel))

    pid = raw.get("id")
    if isinstance(pid, str) and pid:
        if not SLUG_RE.match(pid):
            findings.append(_warn(pack.name, "id-not-slug",
                                  "id '{0}' is not a clean slug [a-z0-9_]+ "
                                  "(filename/install-dir match relies on it)".format(pid), rel))
        if pid.endswith("_pack"):
            findings.append(_warn(pack.name, "id-redundant-suffix",
                                  "id '{0}' carries the redundant '_pack' suffix".format(pid), rel))
        if pid != pack.name:
            findings.append(_warn(pack.name, "id-dir-mismatch",
                                  "manifest id '{0}' != source directory '{1}'".format(pid, pack.name),
                                  rel))

    ver = raw.get("version")
    if isinstance(ver, str) and ver and not VERSION_RE.match(ver):
        findings.append(_err(pack.name, "bad-version",
                             "version '{0}' must match N.N[.N]".format(ver), rel))

    mcv = raw.get("min-cm-version")
    if mcv is not None:
        if not isinstance(mcv, str) or not VERSION_RE.match(mcv):
            findings.append(_err(pack.name, "bad-min-cm-version",
                                 "min-cm-version '{0}' must match N.N[.N]".format(mcv), rel))

    lang = raw.get("language")
    if lang is not None and (not isinstance(lang, str) or not LOCALE_RE.match(lang)):
        findings.append(_warn(pack.name, "bad-language",
                              "language '{0}' is not a plausible locale (e.g. en_US)".format(lang), rel))

    authors = raw.get("authors")
    if authors is None or (isinstance(authors, list) and not authors):
        findings.append(_warn(pack.name, "no-authors", "no 'authors' listed", rel))
    elif not (isinstance(authors, list) and all(isinstance(a, str) for a in authors)):
        findings.append(_warn(pack.name, "bad-authors", "'authors' must be a list of strings", rel))

    for key in raw:
        if key not in MANIFEST_KNOWN_KEYS:
            findings.append(_warn(pack.name, "manifest-unknown-key",
                                  "unknown manifest key '{0}' (typo?)".format(key), rel))

    return findings


# --------------------------------------------------------------------------- #
# Package hygiene (file inventory)
# --------------------------------------------------------------------------- #

def check_package_hygiene(pack: PackInfo) -> list[Finding]:
    findings: list[Finding] = []
    seen_junk_dirs = set()

    for root, dirs, files in os.walk(pack.path):
        for d in list(dirs):
            if d in JUNK_DIR_NAMES:
                rp = os.path.relpath(os.path.join(root, d), pack.path).replace(os.sep, "/")
                if rp not in seen_junk_dirs:
                    seen_junk_dirs.add(rp)
                    findings.append(_warn(pack.name, "junk-dir",
                                          "VCS/build directory '{0}' should not be in the pack".format(rp),
                                          rel_to_repo(os.path.join(root, d))))
        dirs[:] = [d for d in dirs if d not in JUNK_DIR_NAMES]

        for f in files:
            ap = os.path.join(root, f)
            rp = os.path.relpath(ap, pack.path).replace(os.sep, "/")
            relrepo = rel_to_repo(ap)

            # zip-slip / unsafe arcname guard
            if rp.startswith("/") or os.path.isabs(rp) or "\\" in rp or \
                    any(part == ".." for part in rp.split("/")):
                findings.append(_err(pack.name, "unsafe-name",
                                     "unsafe entry name '{0}' (path traversal/absolute)".format(rp),
                                     relrepo))
                continue

            if f in JUNK_FILE_NAMES or f.endswith("~") or f.startswith("."):
                findings.append(_warn(pack.name, "junk-file",
                                      "OS/editor junk file '{0}'".format(rp), relrepo))
            elif rp == "manifest" or rp.lower().endswith(".xml"):
                pass  # shipped
            elif rp.lower().endswith(".l5rcmpack"):
                findings.append(_warn(pack.name, "stray-artifact",
                                      "built artifact '{0}' should not live in the source tree".format(rp),
                                      relrepo))
            else:
                findings.append(_warn(pack.name, "stray-file",
                                      "file '{0}' is neither manifest nor .xml; the loader ignores it".format(rp),
                                      relrepo))
    return findings


# --------------------------------------------------------------------------- #
# Semantic load (l5rdal as source of truth) + referential integrity
# --------------------------------------------------------------------------- #

def semantic_load_error(pack: PackInfo, l5rdal) -> list[Finding]:
    """Load the pack alone through l5rdal with exception=True. Any failure is a
    real, app-visible loading error."""
    try:
        l5rdal.Data([pack.path], exception=True)
        return []
    except l5rdal.DataPackLoadingError as exc:
        return [_err(pack.name, "load-error", str(exc.error_str),
                     rel_to_repo(os.path.join(pack.path, exc.file_path)) if exc.file_path else None)]
    except Exception as exc:  # noqa: BLE001
        return [_err(pack.name, "load-error", "{0}: {1}".format(type(exc).__name__, exc))]


def _pack_records(data, pack_id, attr):
    return [x for x in getattr(data, attr)
            if getattr(x, "source_pack", None) is not None and x.source_pack.id == pack_id]


def check_references(pack: PackInfo, l5rdal, core_dir: Optional[str]) -> list[Finding]:
    """Resolve cross-references against the core+pack reference graph.

    Mirrors and extends dal_check.py. Returns ERROR for unresolved references
    that the app needs, WARNING for loose/optional ones (school
    affinity/deficiency, spell element)."""
    findings: list[Finding] = []
    pack_id = pack.id
    if not pack_id:
        return findings

    dirs = [pack.path]
    if pack_id != "core":
        if core_dir and os.path.isdir(core_dir):
            dirs = [core_dir, pack.path]
        else:
            return [_warn(pack.name, "ref-skipped",
                          "referential checks skipped (no core pack available; "
                          "pass --with-core or place packs/core_pack)")]

    try:
        ref = l5rdal.Data(dirs, exception=True)
    except Exception as exc:  # noqa: BLE001
        return [_warn(pack.name, "ref-skipped",
                      "referential checks skipped (reference load failed: {0})".format(exc))]

    clan_ids = {c.id for c in ref.clans}
    skcat_ids = {x.id for x in ref.skcategs}
    trait_ids = {x.id for x in ref.traits} | {x.id for x in ref.rings}
    ring_ids = {x.id for x in ref.rings}
    perktype_ids = {x.id for x in ref.perktypes}
    skill_ids = {x.id for x in ref.skills}
    spell_ids = {x.id for x in ref.spells}
    effect_ids = {x.id for x in ref.weapon_effects}
    perk_ids = {x.id for x in ref.merits} | {x.id for x in ref.flaws}
    tag_universe = clan_ids | {f.id for f in ref.families} | {t for s in ref.schools for t in s.tags}

    def ref_err(code, msg):
        findings.append(_err(pack.name, code, msg))

    # Skills
    for sk in _pack_records(ref, pack_id, "skills"):
        if sk.type not in skcat_ids:
            ref_err("ref-skill-category", "skill '{0}' -> unknown category '{1}'".format(sk.id, sk.type))
        if sk.trait not in (trait_ids | SKILL_TRAIT_EXTRA):
            ref_err("ref-skill-trait", "skill '{0}' -> unknown trait/ring '{1}'".format(sk.id, sk.trait))

    # Perks (merits + flaws)
    for kind in ("merits", "flaws"):
        for p in _pack_records(ref, pack_id, kind):
            if p.type not in perktype_ids:
                ref_err("ref-perk-category", "{0} '{1}' -> unknown category '{2}'".format(kind[:-1], p.id, p.type))
            for r in p.ranks:
                for e in r.exceptions:
                    if e.tag not in tag_universe:
                        # Perk exception tags are school tags that may be
                        # provided by *any* pack (not just core), so an
                        # unresolved one against core+pack is advisory, not fatal.
                        findings.append(_warn(pack.name, "ref-perk-exception-tag",
                                              "{0} '{1}' rank {2} -> tag '{3}' not found in core+pack "
                                              "(may be provided by another pack)".format(
                                                  kind[:-1], p.id, r.id, e.tag)))

    # Families
    for fam in _pack_records(ref, pack_id, "families"):
        if fam.clanid not in clan_ids:
            ref_err("ref-family-clan", "family '{0}' -> unknown clan '{1}'".format(fam.id, fam.clanid))
        if fam.trait and fam.trait not in trait_ids:
            ref_err("ref-family-trait", "family '{0}' -> unknown trait/ring '{1}'".format(fam.id, fam.trait))

    # Schools
    for sch in _pack_records(ref, pack_id, "schools"):
        if sch.clanid not in clan_ids:
            ref_err("ref-school-clan", "school '{0}' -> unknown clan '{1}'".format(sch.id, sch.clanid))
        if sch.trait and sch.trait not in (trait_ids | {"void"}):
            findings.append(_warn(pack.name, "ref-school-trait",
                                  "school '{0}' -> unknown trait/ring '{1}'".format(sch.id, sch.trait)))
        for which, val in (("affinity", sch.affinity), ("deficiency", sch.deficiency)):
            if val and val not in (ring_ids | {"void"}):
                findings.append(_warn(pack.name, "ref-school-element",
                                      "school '{0}' {1} '{2}' is not a known ring".format(sch.id, which, val)))
        for s in sch.skills:
            if s.id and s.id not in skill_ids:
                ref_err("ref-school-skill", "school '{0}' -> unknown skill '{1}'".format(sch.id, s.id))
        for sp in sch.spells:
            if sp.id and sp.id not in spell_ids:
                ref_err("ref-school-spell", "school '{0}' -> unknown spell '{1}'".format(sch.id, sp.id))
        for pk in sch.perks:
            if pk.id and pk.id not in perk_ids:
                ref_err("ref-school-perk", "school '{0}' -> unknown merit/flaw '{1}'".format(sch.id, pk.id))

    # Weapons / Armors
    for w in _pack_records(ref, pack_id, "weapons"):
        if w.skill and w.skill not in skill_ids:
            ref_err("ref-weapon-skill", "weapon '{0}' -> unknown skill '{1}'".format(w.name, w.skill))
        if w.effectid and w.effectid not in effect_ids:
            ref_err("ref-weapon-effect", "weapon '{0}' -> unknown effect '{1}'".format(w.name, w.effectid))
    for a in _pack_records(ref, pack_id, "armors"):
        if a.effectid and a.effectid not in effect_ids:
            ref_err("ref-armor-effect", "armor '{0}' -> unknown effect '{1}'".format(a.name, a.effectid))

    # Spells (lenient: element is free-ish text)
    for sp in _pack_records(ref, pack_id, "spells"):
        if sp.element and sp.element not in (ring_ids | SPELL_ELEMENT_EXTRA):
            findings.append(_warn(pack.name, "ref-spell-element",
                                  "spell '{0}' element '{1}' is not a known ring".format(sp.id, sp.element)))

    return findings


# --------------------------------------------------------------------------- #
# Stat-modifier validation (docs/MODIFIERS_SCHEMA.md)
# --------------------------------------------------------------------------- #

def _validate_expr(expr: str, params: Iterable[str], predicate: bool = False):
    """Validate a value-DSL expression (or a requires predicate) against the
    sandbox whitelist. Returns None on success, or a short error string.

    Mirrors what the app's evaluator will accept: arithmetic over a fixed
    facade, a whitelist of functions, no attribute access outside
    rings/traits/skills, no dunder, no arbitrary calls.
    """
    import ast

    if expr is None or expr.strip() == "":
        return "empty expression"
    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError as exc:
        return "not parseable ({0})".format(exc.msg)

    bare = (MOD_PRED_BARE if predicate else MOD_VALUE_BARE) | set(params)
    funcs = MOD_PRED_FUNCS if predicate else MOD_VALUE_FUNCS

    err = []

    def fail(msg):
        err.append(msg)

    def visit(node):
        if err:
            return
        if isinstance(node, ast.Expression):
            visit(node.body)
        elif isinstance(node, ast.BinOp):
            if not isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv)):
                fail("operator {0} not allowed".format(type(node.op).__name__))
            visit(node.left); visit(node.right)
        elif isinstance(node, ast.UnaryOp):
            if not isinstance(node.op, (ast.UAdd, ast.USub, ast.Not)):
                fail("unary {0} not allowed".format(type(node.op).__name__))
            if isinstance(node.op, ast.Not) and not predicate:
                fail("'not' is only allowed in requires predicates")
            visit(node.operand)
        elif predicate and isinstance(node, ast.BoolOp):
            for v in node.values:
                visit(v)
        elif predicate and isinstance(node, ast.Compare):
            if any(not isinstance(o, (ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE))
                   for o in node.ops):
                fail("comparison operator not allowed")
            visit(node.left)
            for c in node.comparators:
                visit(c)
        elif isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                fail("only simple function calls are allowed")
            elif node.func.id not in funcs:
                fail("unknown function '{0}'".format(node.func.id))
            if node.keywords:
                fail("keyword arguments are not allowed")
            for a in node.args:
                visit(a)
        elif isinstance(node, ast.Attribute):
            base = node.value
            if not isinstance(base, ast.Name) or base.id not in MOD_VALUE_ATTR_ROOTS:
                fail("attribute access only on rings/traits/skills")
            elif base.id == "rings" and node.attr not in MOD_RINGS:
                fail("unknown ring '{0}'".format(node.attr))
            elif base.id == "traits" and node.attr not in MOD_TRAITS:
                fail("unknown trait '{0}'".format(node.attr))
            # skills.<id> is lenient (skill ids are pack-defined)
        elif isinstance(node, ast.Name):
            if node.id not in bare and node.id not in funcs and node.id not in MOD_VALUE_ATTR_ROOTS:
                fail("unknown name '{0}'".format(node.id))
        elif isinstance(node, ast.Constant):
            # numbers, plus string literals (only meaningful as call args, e.g.
            # skill('kenjutsu'), wielding('daisho')); other literal types are out.
            if not isinstance(node.value, (int, float, str)):
                fail("constant of type {0} not allowed".format(type(node.value).__name__))
        else:
            fail("syntax element {0} not allowed".format(type(node).__name__))

    visit(tree)
    return err[0] if err else None


def _check_mod_element(pack_name, rel, mod, params, in_oneof=False):
    """Validate a single <Mod>. Returns (findings, set_targets) where
    set_targets is the (affects, detail) keys this Mod marks with op=set."""
    findings = []
    line = mod.sourceline
    affects = mod.attrib.get("affects")
    op = mod.attrib.get("op", "add")
    when = mod.attrib.get("when", "auto")
    detail = mod.attrib.get("detail")
    value = mod.attrib.get("value")
    roll, keep, bonus = mod.attrib.get("roll"), mod.attrib.get("keep"), mod.attrib.get("bonus")
    has_triple = any(x is not None for x in (roll, keep, bonus))
    set_targets = []

    def e(code, msg):
        findings.append(_err(pack_name, code, msg, rel, line))

    if not affects:
        e("modifier-missing-affects", "<Mod> missing required attribute 'affects'")
    elif affects not in MOD_ALL_AFFECTS:
        e("modifier-bad-affects", "<Mod> unknown affects '{0}'".format(affects))

    if op not in MOD_OPS:
        e("modifier-bad-op", "<Mod> invalid op '{0}'".format(op))
    if when not in MOD_WHEN_VOCAB:
        e("modifier-bad-when", "<Mod> unknown when '{0}'".format(when))

    # value xor roll/keep/bonus
    if value is not None and has_triple:
        e("modifier-value-conflict",
          "<Mod> has both 'value' and roll/keep/bonus (use one)")
    elif value is None and not has_triple:
        e("modifier-missing-value",
          "<Mod affects='{0}'> has neither 'value' nor roll/keep/bonus".format(affects))

    # roll/scalar consistency vs affects
    if affects in MOD_ROLL_AFFECTS and value is not None:
        e("modifier-shape", "roll affects '{0}' must use roll/keep/bonus, not value".format(affects))
    if affects in MOD_SCALAR_AFFECTS and has_triple:
        e("modifier-shape", "scalar affects '{0}' must use value, not roll/keep/bonus".format(affects))

    # detail
    if detail is not None:
        prefix = detail.split(":", 1)[0] if ":" in detail else None
        if prefix not in MOD_DETAIL_PREFIXES:
            e("modifier-bad-detail",
              "<Mod> detail '{0}' must be one of {1} prefixed (e.g. 'skill:kenjutsu')".format(
                  detail, sorted(MOD_DETAIL_PREFIXES)))
    elif affects in MOD_DETAIL_REQUIRED:
        e("modifier-missing-detail",
          "<Mod affects='{0}'> requires a 'detail' selector".format(affects))

    # expressions
    for label, ex in (("value", value), ("roll", roll), ("keep", keep), ("bonus", bonus)):
        if ex is not None:
            msg = _validate_expr(ex, params)
            if msg:
                e("modifier-bad-expr", "<Mod> {0}='{1}': {2}".format(label, ex, msg))
    if mod.attrib.get("requires"):
        msg = _validate_expr(mod.attrib["requires"], params, predicate=True)
        if msg:
            e("modifier-bad-expr", "<Mod> requires='{0}': {1}".format(mod.attrib["requires"], msg))

    if op == "set" and affects:
        set_targets.append((affects, detail))

    return findings, set_targets


def check_modifiers(pack: PackInfo, l5rdal, core_dir: Optional[str],
                    with_core: bool) -> list[Finding]:
    """Validate every <ModifierDef> in the pack (schema + target resolution)."""
    from lxml import etree
    findings: list[Finding] = []

    # Build the per-kind id universe from core+pack, when available.
    universe = None
    if with_core:
        dirs = [pack.path]
        pack_id = pack.id
        if pack_id and pack_id != "core" and core_dir and os.path.isdir(core_dir):
            dirs = [core_dir, pack.path]
        try:
            ref = l5rdal.Data(dirs, exception=True)
            tech_ids = {t.id for s in ref.schools for t in getattr(s, "techs", [])}
            universe = {
                "tech": tech_ids, "path": tech_ids,
                "kata": {x.id for x in ref.katas},
                "kiho": {x.id for x in ref.kihos},
                "tattoo": {x.id for x in ref.kihos},
                "merit": {x.id for x in ref.merits},
                "ancestor": {x.id for x in ref.merits},
                "flaw": {x.id for x in ref.flaws},
                "mastery": {x.id for x in ref.skills},
                "weapon_effect": {x.id for x in ref.weapon_effects},
                "armor": {a.name for a in ref.armors} | {x.id for x in ref.weapon_effects},
            }
        except Exception:
            universe = None  # resolution skipped, schema checks still run

    for ap, rp in iter_payload_files(pack.path):
        if rp == "manifest":
            continue
        try:
            root = etree.parse(ap).getroot()
        except Exception:
            continue  # well-formedness already reported by check_xml_structure
        if root is None or root.tag != "L5RCM":
            continue
        rel = rel_to_repo(ap)

        for md in root:
            if md.tag != "ModifierDef":
                continue
            line = md.sourceline
            target = md.attrib.get("target")
            kind = md.attrib.get("kind")

            def e(code, msg, ln=line):
                findings.append(_err(pack.name, code, msg, rel, ln))

            if not target:
                e("modifier-missing-target", "<ModifierDef> missing required attribute 'target'")
            if not kind:
                e("modifier-missing-kind", "<ModifierDef> missing required attribute 'kind'")
            elif kind not in MOD_KINDS:
                e("modifier-bad-kind", "<ModifierDef> unknown kind '{0}'".format(kind))

            # declared params (names + max expression)
            params = []
            for p in md.findall("Param"):
                name = p.attrib.get("name")
                if not name or not MOD_PARAM_NAME_RE.match(name):
                    e("modifier-bad-param-name",
                      "<Param> name '{0}' must match [a-z][a-z0-9_]*".format(name),
                      p.sourceline)
                else:
                    params.append(name)
                if p.attrib.get("max") is None:
                    e("modifier-missing-param-max", "<Param name='{0}'> missing 'max'".format(name),
                      p.sourceline)
                else:
                    msg = _validate_expr(p.attrib["max"], params)
                    if msg:
                        e("modifier-bad-expr", "<Param max='{0}'>: {1}".format(p.attrib["max"], msg),
                          p.sourceline)

            mods = md.findall("Mod")
            groups = md.findall("OneOf")
            subs = md.findall("Substitute")
            if not (mods or groups or subs):
                e("modifier-empty",
                  "<ModifierDef target='{0}'> has no <Mod>/<OneOf>/<Substitute>".format(target))

            set_keys = {}

            def record_set(set_targets, ln):
                for key in set_targets:
                    if key in set_keys:
                        findings.append(_err(pack.name, "modifier-set-conflict",
                                             "two op='set' on affects='{0}' detail='{1}'".format(
                                                 key[0], key[1]), rel, ln))
                    else:
                        set_keys[key] = ln

            for mod in mods:
                f, st = _check_mod_element(pack.name, rel, mod, params)
                findings += f
                record_set(st, mod.sourceline)

            for g in groups:
                opts = g.findall("Mod")
                if len(opts) < 2:
                    findings.append(_warn(pack.name, "modifier-oneof-too-few",
                                          "<OneOf> should offer at least two <Mod> options",
                                          rel, g.sourceline))
                for mod in opts:
                    f, st = _check_mod_element(pack.name, rel, mod, params, in_oneof=True)
                    findings += f
                    record_set(st, mod.sourceline)

            for s in subs:
                sl = s.sourceline
                s_aff = s.attrib.get("affects")
                if not (s_aff and s.attrib.get("use") and s.attrib.get("instead_of")):
                    e("modifier-sub-missing",
                      "<Substitute> requires affects/use/instead_of", sl)
                elif s_aff not in MOD_SUBSTITUTABLE:
                    e("modifier-sub-bad-affects",
                      "<Substitute> affects '{0}' is not substitutable".format(s_aff), sl)
                if s.attrib.get("requires"):
                    msg = _validate_expr(s.attrib["requires"], params, predicate=True)
                    if msg:
                        e("modifier-bad-expr",
                          "<Substitute> requires='{0}': {1}".format(s.attrib["requires"], msg), sl)
                if s.attrib.get("when", "auto") not in MOD_WHEN_VOCAB:
                    e("modifier-bad-when",
                      "<Substitute> unknown when '{0}'".format(s.attrib.get("when")), sl)

            # target resolution (only when the reference graph is available)
            if universe is not None and target and kind in universe:
                if target not in universe[kind]:
                    e("modifier-target-unresolved",
                      "<ModifierDef> target '{0}' (kind={1}) not found in core+pack".format(
                          target, kind))

    return findings


# --------------------------------------------------------------------------- #
# Orchestration: lint one pack
# --------------------------------------------------------------------------- #

def lint_pack(pack: PackInfo, core_dir: Optional[str] = DEFAULT_CORE_DIR,
              fix: bool = False, with_core: bool = True) -> list[Finding]:
    findings: list[Finding] = []

    # 1. manifest
    findings += check_manifest(pack)

    # 2. XML structure + hygiene per file; collect identities for uniqueness
    identities: list[tuple] = []
    any_parse_fatal = False
    for ap, rp in iter_payload_files(pack.path):
        if rp == "manifest":
            continue
        struct, ids, fatal = check_xml_structure(pack.name, ap)
        findings += struct
        identities += ids
        any_parse_fatal = any_parse_fatal or fatal
        hyg, _changed = check_xml_hygiene(pack.name, ap, fix=fix)
        findings += hyg

    # 3. per-type id uniqueness within the pack (l5rdal silently overwrites dups)
    seen: dict[tuple, tuple] = {}
    for coll, val, rp, line in identities:
        key = (coll, val)
        if key in seen:
            prev_rp, prev_line = seen[key]
            findings.append(_err(pack.name, "duplicate-id",
                                 "duplicate {0} id/name '{1}' (also at {2}:{3})".format(
                                     coll, val, prev_rp, prev_line), rp, line))
        else:
            seen[key] = (rp, line)

    # 4. hygiene: file inventory
    findings += check_package_hygiene(pack)

    # If structurally broken or manifest invalid, don't attempt semantic load.
    has_error = any(f.severity == SEV_ERROR for f in findings)

    l5rdal = import_l5rdal()
    if not has_error:
        load_errs = semantic_load_error(pack, l5rdal)
        findings += load_errs
        if not load_errs and with_core:
            findings += check_references(pack, l5rdal, core_dir)
    # Stat-modifier schema validation is independent of the (older) submodule
    # DAL: it reads <ModifierDef> directly and resolves targets against the
    # core+pack record graph. Run it whenever the pack parsed cleanly.
    if not any_parse_fatal:
        findings += check_modifiers(pack, l5rdal, core_dir, with_core)
    return findings


# --------------------------------------------------------------------------- #
# Build (deterministic .l5rcmpack)
# --------------------------------------------------------------------------- #

# Fixed metadata for byte-reproducible archives.
_ZIP_DATE = (1980, 1, 1, 0, 0, 0)
_ZIP_EXTERNAL_ATTR = (0o644 & 0xFFFF) << 16
_ZIP_CREATE_SYSTEM = 3  # unix


def build_pack(pack: PackInfo, out_dir: str) -> str:
    """Create a deterministic <id>-<version>[-<language>].l5rcmpack archive.

    Reproducibility: sorted entries, fixed timestamp/permissions/create-system,
    constant DEFLATE level. Repeated builds are byte-identical on a given zlib.
    """
    if not isinstance(pack.raw, dict) or not pack.id or not pack.version:
        raise ValueError("pack {0} has an invalid manifest; cannot build".format(pack.name))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, output_filename(pack.raw))

    payload = iter_payload_files(pack.path)  # already sorted by arcname
    if not any(arc == "manifest" for _, arc in payload):
        raise ValueError("pack {0} has no manifest to package".format(pack.name))

    with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for abs_path, arcname in payload:
            zi = zipfile.ZipInfo(arcname, date_time=_ZIP_DATE)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = _ZIP_EXTERNAL_ATTR
            zi.create_system = _ZIP_CREATE_SYSTEM
            with open(abs_path, "rb") as fp:
                zf.writestr(zi, fp.read())
    return out_path


def validate_built_pack(out_path: str, l5rdal) -> list[Finding]:
    """Extract the produced archive to a temp dir and load it with
    exception=True to confirm it is installable."""
    import tempfile
    import shutil
    name = os.path.basename(out_path)
    tmp = tempfile.mkdtemp(prefix="l5rcmpack_")
    try:
        with zipfile.ZipFile(out_path, "r") as zf:
            zf.extractall(tmp)
        try:
            data = l5rdal.Data([tmp], exception=True)
        except Exception as exc:  # noqa: BLE001
            return [_err(name, "validate-load", "built pack failed to load: {0}".format(exc))]
        if len(data.packs) != 1:
            return [_err(name, "validate-manifest",
                         "built pack exposes {0} manifests (expected 1)".format(len(data.packs)))]
        return []
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --------------------------------------------------------------------------- #
# Reporting helpers (shared by both CLIs)
# --------------------------------------------------------------------------- #

def resolve_packs(tokens, all_flag: bool, packs_dir: str = DEFAULT_PACKS_DIR) -> list[PackInfo]:
    """Resolve CLI pack arguments to PackInfo objects (shared by both CLIs).

    Each token may be a path to a pack directory or a bare directory name under
    ``packs_dir``. Raises ValueError on a bad token / empty selection."""
    if all_flag:
        packs = discover_packs(packs_dir)
        if not packs:
            raise ValueError("no packs found under {0}".format(packs_dir))
        return packs
    if not tokens:
        raise ValueError("specify one or more packs, or use --all")
    out = []
    for token in tokens:
        if os.path.isdir(token) and os.path.isfile(os.path.join(token, "manifest")):
            out.append(load_pack_info(token))
            continue
        candidate = os.path.join(packs_dir, token)
        if os.path.isfile(os.path.join(candidate, "manifest")):
            out.append(load_pack_info(candidate))
            continue
        raise ValueError("not a pack (no manifest): {0}".format(token))
    return out


def sha256_of(path: str) -> str:
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as fp:
        for chunk in iter(lambda: fp.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def summarize(findings: Iterable[Finding]) -> tuple[int, int]:
    errors = sum(1 for f in findings if f.severity == SEV_ERROR)
    warnings = sum(1 for f in findings if f.severity == SEV_WARNING)
    return errors, warnings


def format_finding(f: Finding) -> str:
    loc = ""
    if f.file:
        loc = " {0}".format(f.file)
        if f.line:
            loc += ":{0}".format(f.line)
    tag = "E" if f.severity == SEV_ERROR else "W"
    return "  [{0}] {1}{2}: {3}".format(tag, f.code, loc, f.message)
