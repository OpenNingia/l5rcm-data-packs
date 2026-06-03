#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
packbuild.py - Build deterministic L5RCM .l5rcmpack archives.

Replaces makepack.bat / makepack.sh / make_pack_ci.sh with a single
cross-platform builder. The output name is derived from the manifest as
``<id>-<version>[-<language>].l5rcmpack`` so the published asset always matches
the directory the app installs into (keyed by the manifest id). Archives are
byte-reproducible (sorted entries, fixed timestamp/permissions, constant
DEFLATE level).

The linter runs as a pre-step; the build aborts on errors (use --no-lint to
skip, --strict to also abort on warnings).

Examples:
  python scripts/packbuild.py --all
  python scripts/packbuild.py core_pack --validate
  python scripts/packbuild.py --all --out-dir dist --validate

Exit codes: 0 = all built, 1 = a build/lint/validation failed, 2 = usage error.
"""

from __future__ import annotations

import argparse
import os
import sys

import packlib
from packlib import (DEFAULT_CORE_DIR, DEFAULT_PACKS_DIR, build_pack,
                     format_finding, import_l5rdal, lint_pack, resolve_packs,
                     sha256_of, summarize, validate_built_pack)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Build deterministic .l5rcmpack archives from pack sources.")
    parser.add_argument("packs", nargs="*",
                        help="pack directories or names under --packs-dir")
    parser.add_argument("--all", action="store_true",
                        help="build every pack under --packs-dir")
    parser.add_argument("--packs-dir", default=DEFAULT_PACKS_DIR,
                        help="root containing the packs (default: %(default)s)")
    parser.add_argument("--out-dir", default=DEFAULT_PACKS_DIR,
                        help="where to write the .l5rcmpack files (default: %(default)s)")
    parser.add_argument("--with-core", default=DEFAULT_CORE_DIR, metavar="PATH",
                        help="core pack used by the lint pre-step (default: %(default)s)")
    parser.add_argument("--no-core", action="store_true",
                        help="skip cross-reference resolution in the lint pre-step")
    parser.add_argument("--no-lint", action="store_true",
                        help="skip the lint pre-step (not recommended)")
    parser.add_argument("--strict", action="store_true",
                        help="abort the build on warnings too")
    parser.add_argument("--validate", action="store_true",
                        help="load the produced archive with l5rdal to confirm it installs")
    args = parser.parse_args(argv)

    try:
        targets = resolve_packs(args.packs, args.all, args.packs_dir)
    except ValueError as exc:
        sys.stderr.write("{0}\n".format(exc))
        return 2

    l5rdal = import_l5rdal()
    core_dir = None if args.no_core else args.with_core
    out_dir = os.path.abspath(args.out_dir)

    failures = 0
    for pack in targets:
        print("== {0} (id={1})".format(pack.name, pack.id))

        if pack.raw is None or not pack.id or not pack.version:
            print("  SKIP: invalid manifest ({0})".format(pack.manifest_error or "missing id/version"))
            failures += 1
            continue

        # lint pre-step
        if not args.no_lint:
            findings = lint_pack(pack, core_dir=core_dir, fix=False,
                                 with_core=not args.no_core)
            errors, warnings = summarize(findings)
            blocking = errors > 0 or (args.strict and warnings > 0)
            if blocking:
                print("  LINT FAILED [{0} error(s), {1} warning(s)] -- not building:".format(
                    errors, warnings))
                for f in findings:
                    if f.severity == packlib.SEV_ERROR or args.strict:
                        print(format_finding(f))
                failures += 1
                continue
            elif warnings:
                print("  lint ok ({0} warning(s))".format(warnings))

        # build
        try:
            out_path = build_pack(pack, out_dir)
        except Exception as exc:  # noqa: BLE001
            print("  BUILD FAILED: {0}".format(exc))
            failures += 1
            continue
        print("  built {0}".format(os.path.relpath(out_path, os.getcwd())))
        print("  sha256 {0}".format(sha256_of(out_path)))

        # validate
        if args.validate:
            verrs = validate_built_pack(out_path, l5rdal)
            if verrs:
                for f in verrs:
                    print(format_finding(f))
                failures += 1
            else:
                print("  validated: loads cleanly via l5rdal")
        print()

    built = len(targets) - failures
    print("Built {0}/{1} pack(s); {2} failure(s).".format(built, len(targets), failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
