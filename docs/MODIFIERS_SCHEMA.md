# Stat-modifier schema (`*_modifiers.xml`) — v1

This document is the authoritative spec for the **declarative stat-modifier**
files a datapack may ship. It lets a pack attach mechanical, stat-changing
effects (Armor TN, Reduction, Initiative, rings/traits, Honor/Glory/Status,
Insight, persistent roll bonuses, …) to the records it already defines
(techniques, kata, kiho, tattoo, merits, flaws, ancestors, paths, mastery
abilities, weapon/armor effects), **without shipping executable code**.

The companion analysis that motivated this schema is
[`contents/stat_modifiers.md`](../contents/stat_modifiers.md) (the full catalog of
stat-changing effects across all packs).

> **Status:** schema **v1, frozen for authoring**. Runtime + lint enforcement
> land with the matching `l5rdal` release (new `ModifierDef` parser +
> `Data.get_modifiers_for`) and a `packlint.py` validator. Until then the
> current loader **silently ignores** a `*_modifiers.xml` file (unknown
> top-level element), so shipping one early is forward-compatible but inert.
> A pack that relies on it MUST bump `min-cm-version` accordingly.

---

## 1. Design principles

1. **Declarative, not code.** Every computed value is an arithmetic expression
   over a read-only character facade, evaluated in a sandbox (AST whitelist).
   No `import`, no Python plugins, no arbitrary execution — datapacks are
   downloaded from third parties, so code execution is out of the question.
2. **Sidecar, id-keyed.** Modifiers live in their own file and attach to a
   record by its `id` (`target`), mirroring the existing `rule=` mechanism and
   the catalog. The host records (`Tech`, `KataDef`, …) are untouched.
3. **Derived, never persisted.** These modifiers are recomputed from what the
   character owns; they are **not** written into the `.l5r` save file.
4. **Auto vs situational.** Effects the app can evaluate (gear, stats,
   prerequisites) apply automatically; effects that depend on combat state the
   app cannot know (stances, maneuvers) surface as **pre-filled manual toggles**.

---

## 2. File location & naming

- One optional file per pack: `xml/<prefix>_modifiers.xml`
  (for `core_pack`: `core/modifiers.xml`).
- Standard datapack XML: `<?xml version="1.0" encoding="utf-8"?>` with a single
  `<L5RCM>` root, UTF-8 without BOM, LF endings, spaces for indentation.
- Absent file ⇒ identical behavior to today. Multiple modifier files per pack
  are allowed (merged by the loader).

A modifier's `target` is resolved against **this pack + `core`** (same rule as
School→clan, Weapon→skill, etc.). A `target` that resolves nowhere is a lint
**error** (dead modifier).

---

## 3. Document structure

```
<L5RCM>
  <ModifierDef target=SLUG kind=KIND [rank=N] [partial=true]>   (1..n)
      <Param   name=ID max=EXPR/>                               (0..n)
      <Mod     .../>                                            (0..n)
      <OneOf>  <Mod .../> <Mod .../> ... </OneOf>               (0..n)
      <Substitute .../>                                         (0..n)
  </ModifierDef>
</L5RCM>
```

A `<ModifierDef>` must contain at least one of `<Mod>`, `<OneOf>` or
`<Substitute>`. Several `<ModifierDef>` may share a `target`; their effects
**stack**.

---

## 4. `<ModifierDef>`

| attr      | required        | value                                                                 |
|-----------|-----------------|-----------------------------------------------------------------------|
| `target`  | yes             | slug of the source record (resolved against pack + `core`)            |
| `kind`    | yes             | `tech kata kiho tattoo merit flaw ancestor path mastery weapon_effect armor` |
| `rank`    | `mastery` only  | integer — the skill rank at which the mastery ability triggers        |
| `partial` | no (default no) | `true` ⇒ this record has stat clauses **not** modeled here (honesty flag; the full text stays in the source record's `<Description>`) |

`kind` tells the recompute step which pool of *owned* things to scan
(school techs, perks, reached masteries, …) before applying the modifier.

---

## 5. `<Mod>` — additive / overriding modifier

| attr                     | required                         | notes                                                                 |
|--------------------------|----------------------------------|-----------------------------------------------------------------------|
| `affects`                | yes                              | target statistic — see [§8](#8-affects-taxonomy)                       |
| `value`                  | for **scalar** affects           | expression — see [§9](#9-value-dsl)                                    |
| `roll` / `keep` / `bonus`| for **roll** affects             | expressions, each default `0`; map to the `(r, k, b)` tuple           |
| `op`                     | no (default `add`)               | `add` \| `set` \| `min` \| `max` — see [§11](#11-op-semantics)         |
| `detail`                 | when the affects is scoped       | qualified selector: `skill:`, `weapon:`, `trait:`, `ring:`, `tag:`    |
| `requires`               | no (default none = always)       | **auto-evaluable predicate** over character/equipment state — [§10](#10-requires-predicates) |
| `when`                   | no (default `auto`)              | situational **combat** flag (manual toggle) — [§12](#12-when-vocabulary) |
| `default`                | no                               | `on`/`off`; implicit: `auto`/`requires`-only ⇒ `on`, `when` set ⇒ `off` |
| `reason`                 | no                               | display label; default = the source record's name                     |

Rule: `value` **xor** (`roll`/`keep`/`bonus`). Supplying both is a lint error.

`requires` and `when` are orthogonal and may coexist: `requires` gates whether
the modifier is *applicable at all* (auto), `when` gates whether the applicable
modifier is *currently switched on* (manual).

---

## 6. `<OneOf>` — mutually exclusive choice

Wraps two or more `<Mod>` of which the player picks exactly one (UI: radio).
Use for the catalog's "X **OR** Y" effects (e.g. `tattoo_bear`: +Stamina **or**
+½ Strength).

```xml
<OneOf>
  <Mod affects="trait_rank" detail="trait:stamina"  value="school_rank"/>
  <Mod affects="trait_rank" detail="trait:strength" value="ceil(school_rank/2)"/>
</OneOf>
```

`<OneOf>` inherits the host `<ModifierDef>` context; its children take the same
attributes as a standalone `<Mod>`.

---

## 7. `<Param>` — player-chosen coupled magnitude

Declares a single value the player chooses once (0..`max`), referenced by name
inside sibling `<Mod>` expressions. Use for "shift up to N from A to B" effects
where the **same** amount feeds two stats (e.g. BoE `the_power_of_the_mountain`:
−X Armor TN / +X to all damage, X ≤ Earth).

```xml
<ModifierDef target="the_power_of_the_mountain" kind="kata">
  <Param name="x" max="rings.earth"/>
  <Mod affects="armor_tn"    value="-x"/>
  <Mod affects="damage_roll" bonus="x"/>
</ModifierDef>
```

`name` matches `^[a-z][a-z0-9_]*$`; `max` is an expression. The UI renders a
0..max stepper; the chosen value is **not** persisted (it is session/combat
state).

---

## 8. `affects` taxonomy

**Roll-typed** (use `roll`/`keep`/`bonus`):

| `affects`     | internal | detail                              |
|---------------|----------|-------------------------------------|
| `any_roll`    | `anyr`   | —                                   |
| `skill_roll`  | `skir`   | *optional* `skill:` or `tag:`       |
| `attack_roll` | `atkr`   | *optional* `weapon:` or `tag:`      |
| `damage_roll` | `wdmg`   | *optional* `weapon:` or `tag:`      |
| `trait_roll`  | `trat`   | **required** `trait:`               |
| `ring_roll`   | `ring`   | **required** `ring:`                |

For `skill_roll`/`attack_roll`/`damage_roll` the `detail` is *optional*:
omitting it means the modifier applies to **all** skills / attacks / weapons (a
general bonus, e.g. "+1k0 to all attacks"); a `detail` only narrows the scope.
`trait_roll`/`ring_roll` (and the `trait_rank`/`ring_rank` scalars) **require**
a `detail` — they are meaningless without a target.

**Scalar** (use `value`):

| `affects`        | internal     | status   | detail            |
|------------------|--------------|----------|-------------------|
| `armor_tn`       | `artn`       | existing | —                 |
| `reduction`      | `arrd`       | existing | —                 |
| `initiative`     | `init`       | existing | — (scalar or roll)|
| `wound_penalty`  | `wpen`       | existing | —                 |
| `health_rank`    | `hrnk`       | existing | —                 |
| `insight`        | **new**      | add      | —                 |
| `honor`          | **new**      | add      | —                 |
| `glory`          | **new**      | add      | —                 |
| `status`         | **new**      | add      | —                 |
| `void_max`       | **new**      | add      | —                 |
| `trait_rank`     | **new** *(cascade)* | add | `trait:`        |
| `ring_rank`      | **new** *(cascade)* | add | `ring:`         |
| `spell_tn_self`  | **new**      | add      | — (TN of spells targeting you) |

"new" entries must be added to the app's `MOD_TYPES` (in `l5r/api/rules`) when
the runtime lands. `trait_rank`/`ring_rank` **cascade**: raising the rank feeds
every derived stat (rings from traits, wounds, etc.).

---

## 9. `value` DSL

A pure arithmetic expression, evaluated read-only in a sandbox.

- **Operators:** `+ - * / // ( )`
- **Functions:** `min max floor ceil abs round`
- **Numeric facade (read-only):**
  - `rings.air | rings.earth | rings.fire | rings.water | rings.void`
  - `traits.<name>` — `agility perception reflexes awareness intelligence stamina strength willpower`
  - `skills.<id>` or `skill('<id>')` → that skill's rank (0 if untrained)
  - `school_rank`, `insight_rank`
  - `honor`, `glory`, `status` (rank values)
  - `taint` (Shadowlands Taint rank, 0 if none)
  - `merit_rank('<slug>')`, `flaw_rank('<slug>')`
  - `<Param>` names declared in the same `<ModifierDef>`

Anything else (attribute access, `__dunder__`, calls outside the function list,
names not in the facade) is a **hard parse error** in lint and at load.

---

## 10. `requires` predicates

A boolean expression over an auto-evaluable state facade. When it evaluates
false the modifier is inert (not shown as available). Distinct from `when`:
`requires` is **machine-checked**, `when` is a human toggle.

- **Boolean operators:** `and or not ( )`, comparisons `== != < <= > >=`
- **Predicate facade (read-only):**
  - `wielding('<weapon-or-category>')` — e.g. `wielding('daisho')`, `wielding('katana')`, `wielding('polearm')`
  - `unarmored`, `in_light_armor`, `in_heavy_armor`
  - `has_kiho`, `has_tattoo`, `has_kiho('<slug>')`
  - everything in the numeric facade (so `taint > 0`, `school_rank >= 3`, …)

```xml
<!-- only while wielding both katana and wakizashi -->
<Mod affects="armor_tn" value="school_rank" requires="wielding('daisho')"/>
<!-- only when unarmored and not channeling kiho/tattoo -->
<Mod affects="reduction" value="3 + rings.void"
     requires="unarmored and not has_kiho and not has_tattoo"/>
```

---

## 11. `op` semantics

| `op`  | meaning                                              | example                                   |
|-------|-----------------------------------------------------|-------------------------------------------|
| `add` | add to the running total (default)                  | `armor_tn +X`                             |
| `set` | force an absolute value                             | `Lame`: `ring_rank ring:water set 1`      |
| `min` | floor — raise to at least the value                 | (rare)                                    |
| `max` | cap — lower to at most the value                    | (rare)                                    |

`set`/`min`/`max` apply after all `add` of the same `affects`+`detail` are
summed; multiple `set` on the same target is a lint error (ambiguous).

---

## 12. Sign convention

Values add in the **natural direction of the affects**:

- `wound_penalty`: positive = *more* penalty. A reduction is a **negative**
  value (e.g. `indomitable_warrior_style`: `wound_penalty value="-rings.earth"`).
- `armor_tn`, `reduction`, `initiative`, `insight`, `honor`, … positive = the
  stat goes up. Penalties are negative.
- Roll modifiers: `roll`/`keep`/`bonus` add to the pool; negatives subtract.

---

## 13. `when` vocabulary (closed set)

Situational combat flags. A `when` other than `auto` makes the modifier start
**inactive**; the user flips it on when the situation applies. The set is closed
(the UI must label each toggle); new values are added by PR (lint enum + app
registry).

```
auto
defense_stance  full_defense_stance  attack_stance  full_attack_stance  center_stance
mounted  vs_lower_initiative  first_round  grappling
maneuver_increased_damage  maneuver_called_shot  maneuver_knockdown
maneuver_feint  maneuver_disarm
```

---

## 14. `<Substitute>` — formula substitution

For "use trait/ring A instead of B in calculation C" effects (e.g. Iron Forest
Style, Balance the Elements, the Kitsuki ancestor).

| attr         | required | value                                                       |
|--------------|----------|-------------------------------------------------------------|
| `affects`    | yes      | `initiative attack_roll damage_roll trait_roll skill_roll`  |
| `use`        | yes      | substitute trait/ring                                       |
| `instead_of` | yes      | replaced trait/ring                                         |
| `requires`   | no       | predicate ([§10](#10-requires-predicates))                  |
| `when`       | no       | combat flag ([§13](#13-when-vocabulary))                    |

```xml
<Substitute affects="initiative" use="void" instead_of="reflexes"/>
```

---

## 15. Runtime contract (informative)

The app loads these via `Data.get_modifiers_for(slug)`. During recompute it
scans owned tech/perk/mastery ids (`api.character.get_rules()` / `get_tags()` /
reached masteries) and materializes a separate, **non-serialized**
`runtime_modifiers` list. Each entry exposes `value` as a computed property
(so `x.value[0]` keeps working in `l5r/api/rules`), `active=False` when a
non-`auto` `when` is present, and is filtered out entirely when `requires` is
false. None of this touches the `.l5r` file.

---

## 16. Validation (implemented in `packlint.py`)

`check_modifiers()` in `scripts/packlib.py` reads every `<ModifierDef>` directly
(independent of the submodule DAL version) and emits these findings. Multiple
`ModifierDef` sharing a `target` are **allowed** (they stack) — there is no
duplicate-target check.

Errors (block build):
- `modifier-missing-target` / `modifier-missing-kind` / `modifier-bad-kind`.
- `modifier-empty` — no `<Mod>`/`<OneOf>`/`<Substitute>`.
- `modifier-bad-affects` / `modifier-bad-op` / `modifier-bad-when`.
- `modifier-value-conflict` — both `value` and `roll/keep/bonus`;
  `modifier-missing-value` — neither; `modifier-shape` — wrong shape for the
  affects (scalar vs roll).
- `modifier-missing-detail` — `trait_roll`/`ring_roll`/`trait_rank`/`ring_rank`
  without a `detail`; `modifier-bad-detail` — unrecognised `detail` prefix.
- `modifier-bad-expr` — a `value`/`roll`/`keep`/`bonus`/`requires`/`max`
  expression that fails the sandbox whitelist (syntax error, disallowed
  operator/node, unknown function, attribute access outside rings/traits/skills,
  unknown ring/trait, or a name/param that is not in the facade). This is what
  rejects e.g. `__import__('os').system(...)`.
- `modifier-set-conflict` — two `op="set"` on the same `affects`+`detail`.
- `modifier-sub-missing` / `modifier-sub-bad-affects` — malformed `<Substitute>`.
- `modifier-target-unresolved` — `target` not found in the core+pack record
  graph for its `kind` (only when a reference graph is available;
  `kind=ancestor`→merits, `kind=path`→school techs, `kind=mastery`→skills, etc.).

Warnings:
- `modifier-oneof-too-few` — a `<OneOf>` with fewer than two `<Mod>` options.
- `partial="true"` missing on a record whose catalog row has unmodeled clauses
  (best-effort cross-check against `contents/*.md`) — *planned*.
- XML hygiene (BOM, CRLF, trailing whitespace, tabs, final newline).

---

## 17. Coexistence & migration of the legacy `rule=` engine

A handful of stat effects are already **hardcoded in the app** and tagged with
`rule=` in the packs (`crab_the_mountain_does_not_move`, `strength_of_earth`,
`monkey_tokus_lesson`, `crane_the_force_of_honor`, `ma_insight_plus_3/7`, …).
For example:

```python
def get_base_rd():
    if has_rule('crab_the_mountain_does_not_move'):
        return ring_rank('earth')
    return 0
```

(Note: many `has_rule`/`cnt_rule` checks gate **availability/legality/options**,
not stat values — those are out of scope and stay hardcoded forever. Only the
~6-8 calls that compute a stat value are migration targets; see
`contents/stat_modifiers.md`, `rule=` column.)

### The cross-artifact hazard

The hardcode lives in the **app**; the `ModifierDef` lives in the **datapack**.
The two ship and update independently, so a naive migration breaks one of these
combinations:

|                                   | datapack *without* ModifierDef | datapack *with* ModifierDef |
|-----------------------------------|--------------------------------|-----------------------------|
| **old app** (hardcode, no engine) | ✅ ok                          | ✅ ok (ignores ModifierDef) |
| **new app**, hardcode removed     | ❌ effect **LOST**             | ✅ ok                       |
| **new app**, hardcode present     | ✅ ok                          | ❌ **DOUBLE-counted**       |

You can neither drop the hardcode cold (loses the effect on old datapacks) nor
add the `ModifierDef` while the hardcode stays (doubles it).

### Resolution: hardcode becomes a self-disabling fallback

When the runtime engine lands, wrap each migratable stat hardcode in a gate that
yields to the datapack:

```python
def get_base_rd():
    # legacy fallback: fires only if the datapack hasn't taken over this effect
    if not api.data.get_modifiers_for('crab_the_mountain_does_not_move'):
        if has_rule('crab_the_mountain_does_not_move'):
            return ring_rank('earth')
    return 0
```

This makes every cell of the table correct: old datapack → no `ModifierDef` →
fallback fires (effect preserved); new datapack → `ModifierDef` present →
fallback yields, the engine applies it (no double, no loss); old app → has no
engine and ignores `ModifierDef`, so its hardcode still fires. No hard version
cut, datapacks can be rolled out gradually.

### Migration phasing

1. **Engine phase** — build the runtime; wrap the ~6-8 stat hardcodes in the
   `if not get_modifiers_for(slug):` gate. Computed numbers are unchanged
   whether or not a datapack provides the `ModifierDef`.
2. **Per-effect migration** — for each effect: author its `ModifierDef` in the
   core pack **and** add a golden regression test asserting the computed value
   (e.g. a PC with Mountain Does Not Move shows the *same* RD before/after). The
   gate auto-disables the hardcode. Do it in small batches.
3. **Cleanup** — once the core pack's `min-cm-version` guarantees the
   `ModifierDef`s exist, delete the dead hardcode fallbacks.

**Never** double-encode: an effect is either hardcoded (gated) or in a modifiers
file, and the gate guarantees exactly one path is live at runtime.

---

## 18. Out of scope (v1)

- **Enemy/target-side effects** ("target suffers −X TN", "ignore enemy armor").
  Model only your own clauses; flag the record `partial="true"`.
- **Action economy / re-rolls / Free Raises / die-explosion changes.** Not stat
  values.
- **Spells.** Magical, temporary, out of scope (the catalog excludes them too).
- **Meta-multipliers on facade variables** (e.g. "Honor counts double for
  techniques") — not expressible as a stat modifier; stays a special rule.
