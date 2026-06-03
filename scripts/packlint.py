#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
packlint.py - Lint L5RCM datapacks.

Checks manifest validity, XML well-formedness/formatting, schema and
referential integrity (via l5rdal, the app's own parser) and package hygiene.

Examples:
  python scripts/packlint.py --all
  python scripts/packlint.py packs/lbs_pack
  python scripts/packlint.py great_clan_pack --with-core packs/core_pack
  python scripts/packlint.py --all --fix          # auto-format XML hygiene
  python scripts/packlint.py --all --strict        # warnings fail too
  python scripts/packlint.py --all --json

Exit codes: 0 = clean, 1 = errors (or warnings under --strict/over threshold),
2 = usage error.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

import packlib
from packlib import (DEFAULT_CORE_DIR, DEFAULT_PACKS_DIR, SEV_ERROR, SEV_WARNING,
                     discover_packs, format_finding, lint_pack, load_pack_info,
                     summarize)


def resolve_targets(args) -> list:
    if args.all:
        packs = discover_packs(args.packs_dir)
        if not packs:
            sys.stderr.write("No packs found under {0}\n".format(args.packs_dir))
            raise SystemExit(2)
        return packs

    if not args.packs:
        sys.stderr.write("Specify one or more packs, or use --all.\n")
        raise SystemExit(2)

    out = []
    for token in args.packs:
        if os.path.isdir(token) and os.path.isfile(os.path.join(token, "manifest")):
            out.append(load_pack_info(token))
            continue
        candidate = os.path.join(args.packs_dir, token)
        if os.path.isfile(os.path.join(candidate, "manifest")):
            out.append(load_pack_info(candidate))
            continue
        sys.stderr.write("Not a pack (no manifest): {0}\n".format(token))
        raise SystemExit(2)
    return out


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Lint L5RCM datapacks (manifest, XML, schema, references, hygiene).")
    parser.add_argument("packs", nargs="*",
                        help="pack directories or names under --packs-dir")
    parser.add_argument("--all", action="store_true",
                        help="lint every pack under --packs-dir")
    parser.add_argument("--packs-dir", default=DEFAULT_PACKS_DIR,
                        help="root containing the packs (default: %(default)s)")
    parser.add_argument("--with-core", default=DEFAULT_CORE_DIR, metavar="PATH",
                        help="core pack used to resolve cross-references "
                             "(default: %(default)s)")
    parser.add_argument("--no-core", action="store_true",
                        help="skip cross-reference resolution entirely")
    parser.add_argument("--fix", action="store_true",
                        help="auto-fix safe XML formatting (EOL, trailing ws, "
                             "tabs, declaration, final newline)")
    parser.add_argument("--strict", action="store_true",
                        help="treat warnings as failures")
    parser.add_argument("--max-warnings", type=int, default=None, metavar="N",
                        help="fail if warnings exceed N")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="machine-readable output")
    args = parser.parse_args(argv)

    targets = resolve_targets(args)
    core_dir = None if args.no_core else args.with_core
    with_core = not args.no_core

    all_findings = []
    per_pack = []
    for pack in targets:
        findings = lint_pack(pack, core_dir=core_dir, fix=args.fix, with_core=with_core)
        findings.sort(key=lambda f: (f.severity != SEV_ERROR, f.file or "", f.line or 0, f.code))
        per_pack.append((pack, findings))
        all_findings += findings

    errors, warnings = summarize(all_findings)
    failed = errors > 0 or (args.strict and warnings > 0) or \
        (args.max_warnings is not None and warnings > args.max_warnings)

    if args.as_json:
        print(json.dumps({
            "packs": [
                {"pack": p.name, "id": p.id,
                 "findings": [f.to_dict() for f in fs]}
                for p, fs in per_pack
            ],
            "summary": {"errors": errors, "warnings": warnings,
                        "exit_code": 1 if failed else 0},
        }, indent=2))
        return 1 if failed else 0

    for pack, findings in per_pack:
        e, w = summarize(findings)
        status = "OK" if e == 0 else "FAIL"
        header = "== {0} (id={1}) : {2}".format(pack.name, pack.id, status)
        if e or w:
            header += "  [{0} error(s), {1} warning(s)]".format(e, w)
        print(header)
        for f in findings:
            print(format_finding(f))
        if not findings:
            print("  (no findings)")
        print()

    print("Total: {0} error(s), {1} warning(s) across {2} pack(s).".format(
        errors, warnings, len(targets)))
    if args.fix:
        print("XML hygiene auto-fix applied where needed (--fix).")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
