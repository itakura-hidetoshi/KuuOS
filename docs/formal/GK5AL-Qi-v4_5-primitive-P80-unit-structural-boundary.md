# F112-P94D3GK5AL / Qi v4.5 — three primitive P80 unit boundaries for actual structural P87/P89 transport

**Date:** 2026-11-03 JST. Canonical theorem repository: `itakura-hidetoshi/KuuOS`, branch `main`. Independent Kuu formalization provides mathematical authority; Qi imports it one way only. Strict 空 remains independent. Public aggregate `KuuOSFormal`; root107 preserved.

**Environment:** Lean `v4.30.0-rc2`; mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`; append-only/tighten-only; protected PR #1558 remains Draft/OPEN/unmerged. No sorry, admit, new axioms, frozen KUOS rewrite, Gray restoration or global hyperdescent.

## 1. Exact-source audit and merge provenance

| Evidence | Independent GK5AL | Qi v4.5 |
| --- | --- | --- |
| Theorem/integration PR | [#2982](https://github.com/itakura-hidetoshi/KuuOS/pull/2982) MERGED | [#2983](https://github.com/itakura-hidetoshi/KuuOS/pull/2983) MERGED |
| Exact source HEAD | `a76c8fc621cbf40d2c1a3a1e6ccdc3c2400b8579` | `7c191d704f84e03ae4fb30d927a657b7d1908dbd` |
| Squash SHA | `b253d1541b8bf0f57f3fbaebcf331791e57bbb59` | `c454fbb05dde2bd48a2c53a33f0420dc118ed34e` |
| Exact source/test-merge Git tree | `741829612feb09947d1b415a0e6428939f7ed7bb` | `a64ee043f21125a98d014f7a76782abfa10667a3` |
| Exact-source CI | [#41521504514](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41521504514) SUCCESS | [#41522484049](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41522484049) SUCCESS |
| Strict Lean / KuuOSFormal | **9228 / 9228 SUCCESS** | **10155 / 10155 SUCCESS** |
| New axiom prints | **10/10**, none depends on any axioms | **9/9**, subsets of `propext`, `Classical.choice`, `Quot.sound` |
| Lean diagnostics | error/warning 0/0 | error/warning 0/0 |
| Gate | Governance 30/30 SUCCESS, independent Kuu/Workflow integrity SUCCESS | Governance and required targeted validation SUCCESS |

No transfer of historical `native_decide` assumptions from earlier Qi modules is ruled out by these *new-source* axiom audits; each claim is scoped to the printed declarations.

## 2. True old P87 primitive boundary is entirely at P80 units

Original four-cell sources remain genuinely typed along this historical inclusion:

```text
P77: eight vertical original F55 source four-cell rules
  ↳ P80: nine constructor presentation, with three new units
     [horizontalUnit | leftContextUnit | rightContextUnit]
    ↳ P85: eight constructor horizontal closure
      ↳ P86: twelve constructor context/route closure
        ↳ P87: twelve constructor self-recursive closure
          ↳ P89: thirteen constructor interchange closure
```

The GK5AI structural map `φ` translates the original F55 3-cell syntax recursively into selected P92B and is not identical to P92B's whole-term `.original` inclusion. P93's inherited `.old` generator compares `.original(f)` to `.original(g)`, so it does *not* license an unproved comparison between `φ(f)` and `φ(g)`.

GK5AJ unconditionally translates the original eight P77 vertical four-cell rules. Every additional P80/P85/P86/P87 *closure* rule is handled by a corresponding actual P93 selected four-cell constructor. The residual unknown basis consists of exactly the three originally adjoined P80 unit generators, kept as the new Type-valued dependent source `NativeGK5ALPrimitiveUnitFourCell`.

The proof-bearing additive module [GK5AL Lean source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5ALPrimitiveUnitObstruction.lean) constructs typed `.toP87` inclusions, complete recursors `nativeGK5ALP80_of_primitive`, `nativeGK5ALP85_of_P80`, `nativeGK5ALP86_of_P85`, `nativeGK5ALP87_of_P86`, and the exact converse restriction `nativeGK5ALPrimitive_of_P87`.

For each fixed polygon and original two-category source:

```text
Nonempty(NativeGK5AKP89StructuralBoundary)
 ↔ Nonempty(NativeGK5AKP87StructuralBoundary)
 ↔ Nonempty(NativeGK5ALPrimitiveBoundary).
```

Theorems `nativeGK5ALP87Structural_nonempty_iff_primitive` and `nativeGK5ALP89Structural_nonempty_iff_primitive` are constructive and **axiom-free** in the Lean `#print axioms` sense. If any *actual* primitive has no selected P93 four-cell joining its two structural images, `nativeGK5ALP87_obstruction_of_primitive_missing` and `nativeGK5ALP89_obstruction_of_primitive_missing` exclude the corresponding global lift. **GK5AL itself does not prove that such a primitive counterexample exists.** The independent structural P89 interchange already constructed by GK5AK remains unconditional.

## 3. Qi v4.5 genuinely physical north-C60 instance

[Qi v4.5 Lean source](../../formal/KUOS/Architecture/QiWuxingGK5ALNorthPrimitiveObstructionV4_5.lean) imports only earlier Qi v4.4 and independent Kuu GK5AL. On the original adjacent north C60 F45 first and second stages it constructs all three `NativeGK5ALPrimitiveUnitFourCell` witnesses, retaining original doubly Nat-indexed F54 unit routes. `fivefoldGK5ALNorthThreeOriginalP87Witnesses` proves all three have genuinely old P87 four-cell witnesses — **not** their selected P93 structural images.

Over the real `Site.vertex` → `Site.face` two-category source, `fivefoldGK5ALNorthP87_iff_threePrimitive` and `fivefoldGK5ALNorthP89_iff_threePrimitive` make the exact structural transport dependency explicit.

Under an explicitly supplied `FivefoldGK5ALNorthPrimitiveBoundary`, `fivefoldGK5ALNorthPhysicalFourClassMap` builds a physical fifth Edge/Dart pair coupled to the original-P89/selected-P93 four-cell quotient map. `fivefoldGK5ALNorthPhysicalInjective_iff_reflect` restates the true P93→P89 comparison reflection gate, and `fivefoldGK5ALNorthPhysicalShadow_commutes` preserves the original signed pentagon/square/odd ZMod2 phase. Actual physical 04/43 reversed Dart orientations remain those established in Qi v4.4; no equality between physical Edge and Mathlib whole NatIso has been added.

## 4. Interpretation, strict authority and next frontier

**Proven:** a complete and exact minimal generator-family reduction of the old P87/P89 structural 4-cell transport, P77 source lift, original typed P80 primitive witnesses, genuine north C60 instantiations, conditional four-cell quotient map and preservation of all chosen original C60 shadows.

**Not proven in GK5AL/Qi v4.5:** unconditional selected P93 higher-cell certificates for the three P80 primitive units, global faithfulness of the quotient map, P92B extra associator naturality inside original nine-constructor F55, an unrestricted whole-NatIso/physical-Edge comparison or general higher descent. None is silently supplied by local physical C60 data.

**Next F112-P94D3GK5AM:** analyze selected P92B context-constructor parity and whether actual P93 four-cell rules preserve it. A genuine mismatch for the P80 context-unit structural images would constitute a concrete obstruction, strictly stronger than GK5AL's conditional if-and-only-if theorem. A proposed invariant is not itself an accepted proof until a separate pinned Lean CI validates it. Maintain original raw proof histories, independent Kuu authority, root107 and protected PR #1558.

Historical GK5AK and Qi v4.4 formal sources and previous README/ROADMAP records remain intact.
