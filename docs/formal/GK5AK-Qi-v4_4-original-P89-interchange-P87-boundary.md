# F112-P94D3GK5AK / Qi v4.4 — original P89 horizontal interchange, P87 lift obstruction, genuine north C60 physical four-cell comparison

**Date:** 2026-11-03 JST.
**Canonical theorem branch:** `itakura-hidetoshi/KuuOS` / `main`; independent Kuu supplies theorem authority, Qi consumes Kuu in ONE direction. Strict 空 authority stays independent. Public aggregate `KuuOSFormal`, retained root107.
**Pins:** Lean `v4.30.0-rc2`, mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`.
**Protected branch:** PR #1558 Draft/OPEN/unmerged; append-only/tighten-only, no removal or weakening of previous theorems.

## Exact-source, merged and audited provenance

| Evidence | Independent F112 GK5AK | Qi v4.4 |
| --- | --- | --- |
| Formal PR | [#2979](https://github.com/itakura-hidetoshi/KuuOS/pull/2979) MERGED | [#2980](https://github.com/itakura-hidetoshi/KuuOS/pull/2980) MERGED |
| Final exact-source HEAD | `955707fdf4e2e2b930aec7eca3e8929949515c78` | `d448e511a5562b4cf4ad868f21a7cb1243e48eb8` |
| Squash SHA | `ceb8714d6edfa994028ba716e0960a8fda8ab653` | `f55b7582b0642c76a6e5a214b1426bf11a79eb52` |
| Exact-source/squash Git tree | `6d521231819df52cef3f7dc828378bc530fc6f6c` | `5819a56c80b6f4603f4c3c1680fe498f4d95c987` |
| Exact-source CI | [#41515336483](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41515336483) SUCCESS | [#41516371268](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41516371268) SUCCESS |
| Strict Lean | **9226/9226**, `KuuOSFormal` SUCCESS | `KuuOSFormal` and Qi v4.4 changed target SUCCESS (10153-target graph) |
| New source `#print axioms` outputs | **8/8**, within permitted set | **7/7**, within permitted set |
| New Lean errors / warnings / sorryAx | **0 / 0 / 0** | **0 / 0 / 0** |
| Independent Kuu / PR Governance | SUCCESS / SUCCESS | SUCCESS / SUCCESS |
| Changed files | New independent Lean module + 1 aggregate import | New Qi Lean module + 1 aggregate import |

All 15 new source `#print axioms` outputs were read in the exact-head Lean CI logs. Dependencies are subsets of `{propext, Classical.choice, Quot.sound}`; the true interchange constructor map, all-thirteen P89 lift from P87, restriction, and the iff of Type-valued lifting existence were each reported to use **NO axioms**. The ordinary quotient maps use the existing `Quot.sound` and, as applicable, `propext` / `Classical.choice`. No inference is made that historical Qi v2.5/v3.7 `native_decide` axioms disappeared globally.

## 1. Independent GK5AK: actual original P89 interchange and source P87 frontier

New Lean: [GK5AK original P89-to-P93 structural four-cell bridge](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5AKInterchangeFourCellBoundary.lean).

GK5AI proved a structural, Type-valued map `φ` on all nine original F55 3-cell constructors into selected P92B. GK5AJ proved the true P77 **eight** vertical 4-cell generators transport into selected P93. But the source P89 four-cell syntax has **thirteen** constructors, including an inherited `P87` generator and a genuine new *horizontal interchange*. The P93 `.old` generator only certifies four-cells between `.original f` and `.original g`, not automatically between the distinct **structural images** `φ f` and `φ g`. This typing boundary is genuine.

**Unconditional construction:** `nativeGK5AKInterchangeStructural` constructs an ACTUAL P93C Type-valued four-cell between the structural images of the left and right sides of the original P89 horizontal interchange:

```text
P89 original source:
  horizontal(trans(f₁,f₂), trans(g₁,g₂))
      ⇝ trans(horizontal(f₁,g₁),horizontal(f₂,g₂))

P93 selected:
  horizontal(trans(φ f₁,φ f₂),trans(φ g₁,φ g₂))
      ⇝ trans(horizontal(φ f₁,φ g₁),horizontal(φ f₂,φ g₂))
```

It is a true target `NativeF55P93AssocFourCell.interchange`, using GK5AJ's definitional horizontal compatibility; no P87 premise or signed-shadow equality is needed to construct it.

**Exact higher obstruction:** define the explicitly supplied `NativeGK5AKP87StructuralBoundary` as a family of genuine P93 four-cell certificates connecting structural images of every inherited original P87 four-cell. Define `NativeGK5AKP89StructuralBoundary` as the corresponding family for all thirteen source P89 4-cell constructors. By original constructor recursion and exact restriction:

```text
Nonempty(P89 structural 4-cell lift family)
    ↔ Nonempty(P87 structural 4-cell lift family).
```

This is `nativeGK5AKP89Structural_nonempty_iff_P87`, a theorem about the presence of **typed witness-producing functions** for fixed original source categories and polygon, not a declaration that either family exists unconditionally. All thirteen closure steps other than the inherited `P87` source generator have actual corresponding P93 Type-valued constructors.

Conditional on an actual `P87` structural lift, `nativeGK5AKFourClassMap` descends the genuine original `P89` four-cell **witness quotient** to the separately selected `P93` four-cell witness quotient. The source-preserving statement `nativeGK5AKFourClassInjective_iff_reflect` proves:

```text
Injective(F)
  ↔ (∀ original f,g,
       Nonempty(P93FourCell(φ f, φ g))
           → Nonempty(P89FourCell(f,g))).
```

This is an **iff**, NOT a proof that reflection is globally available. `nativeGK5AKFourClassShadow_commutes` derives preservation of the whole signed pentagon/square/odd-ZMod2 C60 shadow from ACTUAL original witness soundness and GK5AJ's full structural shadow theorem; numerical equality alone never constructs a four-cell.

## 2. Qi v4.4: real north-C60 F45 stage witnesses and physical direction

New Lean: [Qi v4.4 real C60 interchange and conditional reflection](../../formal/KUOS/Architecture/QiWuxingGK5AKNorthPhysicalInterchangeV4_4.lean).

For the first two **existing, genuinely adjacent** north-C60 F45 stages, retain independent doubly Nat-dependent F54 unit routes and genuine original F55 identity three-cells. Use them as four inputs to the **ACTUAL original P89 Type-valued horizontal interchange constructor**. In `fivefoldGK5AKNorthSelectedInterchange`, construct the corresponding genuine selected P93 four-cell by independent GK5AK's structural interchange map.

`fivefoldGK5AKNorthSelectedInterchange_class_eq` shows that the two selected three-cell comparison terms have equal P93 four-cell quotient classes because the ACTUAL higher witness exists. It does NOT claim the original raw F55 proof terms are equal.

For the separate actual north-C60 original four-sector long/short F54 pentagon histories, define `FivefoldGK5AKNorthP87Boundary` over the real `Site` source and target and keep it **explicitly as data, not an inhabitance theorem**. Given this interface, the real physical north-C60 fifth around-edge `Dart×Dart` endpoints pair with the original P89→selected P93 four-cell quotient map. Theorem `fivefoldGK5AKNorthPhysicalFourClass_injective_iff_reflect` proves its injectivity **iff** the exact original P89 comparison-reflection condition; the true physical Dart coordinates add no new source 4-cell authority. The signed/odd phase observer remains compatible with the physical/selected map.

`fivefoldGK5AKNorthPhysicalInterchangeAndOrientation` simultaneously carries the genuine north fifth-around-edge closure, ACTUAL original P89 and selected P93 Type-valued 4-cell proof terms, and both **physically reversed** categorical edges 04 and 43 as separately typed evidence. No physical Edge is equated to any Mathlib whole NatIso.

## 3. Proven scope and remaining obstruction

**Constructed:** an unconditional horizontal interchange P89→P93 Type-valued 4-cell for all correct original typed inputs; the complete P89 structural lift *from* specified P87 base data; precise iff for existence of the lift families; conditional genuine quotient map with exact reflectivity iff; real first/second north-C60 instance and correctly reversed physical orientations.

**Not proven:** unconditionally inhabited original P87→structural-P93 base comparison; global injectivity or reflection of the P89→P93 quotient; derivation of P92B's additional `assocNaturality` from original nine-constructor F55; frozen historical KUOS F54/F55 equivalence; a global original raw F54→Mathlib whole NatIso pseudofunctor; arbitrary physical Edge-to-NatIso higher fillers; Gray reconstruction, global descent, gluing or unrestricted hyperdescent. P77/P87/P89 and P92B/P93 are distinct presentations with separate actual Type-valued proof histories.

## 4. Next frontier: GK5AL (working title)

Investigate the **precise old P87 structural boundary** instead of merely adding more quotient observations. Characterize which P87 generators admit a P93 four-cell between **GK5AI structural φ-images**, while explicitly distinguishing `.original f` from `φ f`. Prove an actual lift on supported generators and a rigorous obstruction on unsupported ones. Keep real north-C60 physical fifth around-edge and both 04/43 reversed orientations; preserve independent Kuu→Qi, strict 空 authority, fixed pins, same-root107, append-only and draft #1558 untouched.
