#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests for the stat-modifier validation in packlib (docs/MODIFIERS_SCHEMA.md).

Run:  python scripts/test_packlib.py        (or: python -m unittest scripts.test_packlib)
"""

import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import packlib  # noqa: E402
from packlib import _validate_expr, lint_pack, load_pack_info, DEFAULT_CORE_DIR  # noqa: E402


class TestValidateExpr(unittest.TestCase):

    def ok(self, expr, **kw):
        self.assertIsNone(_validate_expr(expr, kw.pop("params", ()), **kw),
                          "expected {0!r} to be valid".format(expr))

    def bad(self, expr, **kw):
        self.assertIsNotNone(_validate_expr(expr, kw.pop("params", ()), **kw),
                             "expected {0!r} to be rejected".format(expr))

    def test_valid_values(self):
        self.ok("traits.perception")
        self.ok("rings.earth")
        self.ok("2 * school_rank + 5")
        self.ok("ceil(honor / 2)")
        self.ok("max(honor - 3, 1)")
        self.ok("insight_rank + rings.air")
        self.ok("skills.iaijutsu")
        self.ok("skill('kenjutsu')")
        self.ok("-x", params=("x",))

    def test_reject_dangerous(self):
        self.bad("__import__('os').system('x')")
        self.bad("().__class__")
        self.bad("open('f')")

    def test_reject_typos_and_unknowns(self):
        self.bad("traits.perceptron")     # unknown trait
        self.bad("rings.metal")           # unknown ring
        self.bad("undeclared + 1")        # unknown name
        self.bad("frobnicate(1)")         # unknown function
        self.bad("not honor")             # 'not' only in predicates

    def test_predicates(self):
        self.ok("wielding('daisho')", predicate=True)
        self.ok("unarmored and not has_kiho", predicate=True)
        self.ok("taint > 0", predicate=True)
        self.ok("school_rank >= 3 or has_tattoo", predicate=True)
        self.bad("wielding('daisho')")    # call ok only because wielding is a func;
        # 'not' / boolean ops rejected outside predicate:
        self.bad("a and b", predicate=False)


def _lint_temp_modifiers(xml_body, with_core=False):
    """Write a one-file pack with the given modifiers XML and lint it.
    Returns the set of finding codes."""
    tmp = tempfile.mkdtemp(prefix="modlint_")
    with open(os.path.join(tmp, "manifest"), "w", encoding="utf-8") as fp:
        fp.write('{"id": "tmp", "version": "1.0", "display_name": "Tmp"}')
    with open(os.path.join(tmp, "mods.xml"), "w", encoding="utf-8") as fp:
        fp.write('<?xml version="1.0" encoding="utf-8"?>\n<L5RCM>\n')
        fp.write(xml_body)
        fp.write('\n</L5RCM>\n')
    pack = load_pack_info(tmp)
    core = DEFAULT_CORE_DIR if with_core else None
    findings = lint_pack(pack, core_dir=core, with_core=with_core)
    import shutil
    shutil.rmtree(tmp, ignore_errors=True)
    return {f.code for f in findings}


class TestCheckModifiers(unittest.TestCase):

    def codes(self, body, with_core=False):
        return _lint_temp_modifiers(body, with_core=with_core)

    def test_clean_passes(self):
        codes = self.codes(
            '<ModifierDef target="x" kind="tech">'
            '<Mod affects="armor_tn" value="traits.perception"/></ModifierDef>')
        self.assertFalse({c for c in codes if c.startswith("modifier-")})

    def test_bad_kind_and_missing_target(self):
        codes = self.codes('<ModifierDef kind="bogus">'
                           '<Mod affects="armor_tn" value="1"/></ModifierDef>')
        self.assertIn("modifier-bad-kind", codes)
        self.assertIn("modifier-missing-target", codes)

    def test_bad_affects_and_shape(self):
        codes = self.codes(
            '<ModifierDef target="x" kind="tech">'
            '<Mod affects="nope" value="1"/>'
            '<Mod affects="armor_tn" roll="1"/></ModifierDef>')
        self.assertIn("modifier-bad-affects", codes)
        self.assertIn("modifier-shape", codes)

    def test_value_conflict_and_missing(self):
        codes = self.codes(
            '<ModifierDef target="x" kind="tech">'
            '<Mod affects="armor_tn" value="1" bonus="1"/>'
            '<Mod affects="armor_tn"/></ModifierDef>')
        self.assertIn("modifier-value-conflict", codes)
        self.assertIn("modifier-missing-value", codes)

    def test_detail_rules(self):
        codes = self.codes(
            '<ModifierDef target="x" kind="tech">'
            '<Mod affects="trait_roll" roll="1"/>'              # missing detail
            '<Mod affects="armor_tn" value="1" detail="oops"/>'  # bad prefix
            '</ModifierDef>')
        self.assertIn("modifier-missing-detail", codes)
        self.assertIn("modifier-bad-detail", codes)

    def test_attack_roll_detail_optional(self):
        # a general attack bonus needs no detail
        codes = self.codes(
            '<ModifierDef target="x" kind="tech">'
            '<Mod affects="attack_roll" roll="1" keep="0"/></ModifierDef>')
        self.assertNotIn("modifier-missing-detail", codes)

    def test_set_conflict(self):
        codes = self.codes(
            '<ModifierDef target="x" kind="tech">'
            '<Mod affects="armor_tn" op="set" value="1"/>'
            '<Mod affects="armor_tn" op="set" value="2"/></ModifierDef>')
        self.assertIn("modifier-set-conflict", codes)

    def test_bad_expr_blocks_code(self):
        codes = self.codes(
            '<ModifierDef target="x" kind="tech">'
            '<Mod affects="armor_tn" value="__import__(\'os\')"/></ModifierDef>')
        self.assertIn("modifier-bad-expr", codes)

    def test_substitute_and_param_and_oneof(self):
        codes = self.codes(
            '<ModifierDef target="x" kind="kata">'
            '<Substitute affects="armor_tn" use="void"/>'       # missing instead_of + bad affects
            '<OneOf><Mod affects="armor_tn" value="1"/></OneOf>'  # too few
            '</ModifierDef>')
        self.assertIn("modifier-sub-missing", codes)
        self.assertIn("modifier-oneof-too-few", codes)

    def test_empty_def(self):
        codes = self.codes('<ModifierDef target="x" kind="tech"/>')
        self.assertIn("modifier-empty", codes)

    def test_target_resolution_with_core(self):
        if not os.path.isdir(DEFAULT_CORE_DIR):
            self.skipTest("core_pack not available")
        good = self.codes(
            '<ModifierDef target="dragon_kitsukis_method" kind="tech">'
            '<Mod affects="armor_tn" value="1"/></ModifierDef>', with_core=True)
        self.assertNotIn("modifier-target-unresolved", good)
        bad = self.codes(
            '<ModifierDef target="totally_made_up_slug" kind="tech">'
            '<Mod affects="armor_tn" value="1"/></ModifierDef>', with_core=True)
        self.assertIn("modifier-target-unresolved", bad)


if __name__ == "__main__":
    unittest.main()
