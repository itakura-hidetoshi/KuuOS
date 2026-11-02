# F112-P94D3GK5AN / Qi v4.7 — unconditional original P89 structural 4-cell repair into the EXISTING P94A

**Date:** 2026-11-03 JST. **Canonical theorem repository:** `itakura-hidetoshi/KuuOS`, branch `main`. Independent Kuu owns theorem authority; Qi imports it one-way. Strict 空 authority remains independent. Public aggregate `KuuOSFormal`, **107 public roots preserved**.

**Pins:** Lean `v4.30.0-rc2`; mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`. Append-only / tighten-only / same-root; protected PR #1558 stays Draft/OPEN/unmerged. Neither historical original-F55 nor historical P93C/P94A source files are replaced. No new logical axioms, sorry, native_decide, Gray reconstruction or unrestricted higher descent.

## 1. Exact-source merged proofs and independent audit

| Evidence | Independent GK5AN | Qi v4.7 |
| --- | --- | --- |
| Formal PR | [#2989](https://github.com/itakura-hidetoshi/KuuOS/pull/2989) **MERGED** | [#2990](https://github.com/itakura-hidetoshi/KuuOS/pull/2990) **MERGED** |
| Final exact-source HEAD | `8b9d76c9dd68efd3f7b3fc6483dbb20b2ae82fca` | `de80062e2dcdee7369b0da60e07655728f4f5917` |
| Squash SHA | `d7b6f00ffb14add6bd3b115c1ca80fc7090567f4` | `f42892267735287a243f103c6d3268a853fb671d` |
| Exact source/test-merge/squash Git tree | `802633ba63dcd2ddc714362afecddaef274558fd` | `184e6306a8bee3da8ba01ddf9cdf03748771b307` |
| PR Governance CI | [#41530901808](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41530901808) **terminal SUCCESS** | [#41531748938](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41531748938) attempt 2 **terminal SUCCESS** |
| Strict Lean / `KuuOSFormal` | **9232/9232 SUCCESS** | **10159/10159 SUCCESS** |
| New axiom audit | **15/15**, all within allowed standard set; core source-lift recursors & existence **8 axiom-free** | **8/8**, all subsets of `{propext, Classical.choice, Quot.sound}` |
| New Lean error/warning/sorryAx | **0/0/0** | **0/0/0** |
| Governance | **30/30 SUCCESS** | **30/30 SUCCESS** |
| Source changes | New independent GK5AN Lean module + one public import | New Qi v4.7 Lean module + one public import |

The initial Qi governance attempt had a **transient GitHub Actions artifact download `ECONNRESET`** in `KuuOS repository revision DAG v0.85`, not a Lean elaboration or theorem error. Re-running only that failed job on attempt 2 yielded 30/30 terminal SUCCESS. Do not present transient transfer failure as a theorem failure.

## 2. Crucial reused construction — P94A existed before GK5AN

The earlier historical file [P94A independently declared unit-four-cell presentation](../../formal/Kuu/F112/PolygonNativeF55P94UnitFourCellPresentation.lean) **already provided** `NativeF55P94UnitFourCell`: a separately selected Type-valued presentation containing all P93C evidence by an honest `.old` generator; it also explicitly adjoins three new higher generators `horizontalUnit`, `leftContextUnit`, `rightContextUnit`, and recursively closes under real P93-like typed operations. It preserves the entire chosen signed pentagon/square/odd C60 shadow by an actual constructor induction. **GK5AN did not invent, replace, or duplicate P94A**.

Previous [GK5AL/Qi v4.5](GK5AL-Qi-v4_5-primitive-P80-unit-structural-boundary.md) reduced the original P87/P89 full structural lift into the then-chosen P93C target to exactly the three original P80 primitive unit families. [GK5AM](GK5AM-context-parity-original-P80-unit-no-P93-structural-lift.md) proved that the structural `φ`-images of original left/right context units have unequal `ZMod 2` context parity, which all 16 actual P93C four-cell constructors preserve. Hence complete original P87/P89 structural lifting into **P93C** does NOT exist wherever genuine typed contexts occur. Qi v4.6 instantiated this no-go on true north C60.

GK5AN changes **the target**, not the original source or its theorem history. Write `φ` for GK5AI's complete constructor-recursive original F55 3-cell→selected P92B 3-cell map. Crucially `φ(f)` and `.original(f)` are different actual terms in general.

## 3. Genuine unconditional source P89→P94A lift

New independent Lean: [GK5AN structural P89→P94A](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5ANStructuralP89ToP94A.lean).

The function `nativeGK5ANPrimitiveToP94` constructs actual selected P94A four-cells for **all three original P80 primitive generator families** with their exact source types. The recursors
```text
nativeGK5ANP80P94_of_primitive
nativeGK5ANP85P94_of_P80
nativeGK5ANP86P94_of_P85
nativeGK5ANP87P94_of_P86
nativeGK5ANP87ToP94
nativeGK5ANP89ToP94
```
prove actual original P77→P80→P85→P86→P87→P89 generator compatibility without forgetting the true original F54 double-Nat histories or F55 proof terms. The old P77 witness uses the independently proven GK5AJ map and P94A's `.old` inclusion; the original P89 interchange uses the independently proven GK5AK actual P93 higher witness, again included via P94A `.old`. **All thirteen original P89 four-cell constructors are covered.**

`nativeGK5ANP87P89ToP94_unconditional` proves the source-independent existence of both complete P87 and complete P89 *P94A-target* structural Type-valued lifting families **without a P87/P93 premise**. Their unqualified existence is a DIFFERENT theorem from GK5AM's P93C nonexistence, so there is no contradiction.

`nativeGK5ANP89ToP94FourClassMap` gives an UNCONDITIONAL, actual witness-respecting quotient map from the genuine original P89 4-cell existence quotient to the chosen P94A 4-cell existence quotient. The representative formula is `nativeGK5ANP89ToP94FourClassMap_spec` and full C60 signed/odd shadow preservation is `nativeGK5ANP89ToP94Shadow_commutes`.

**Faithfulness remains exactly conditional:**

```text
Injective(original-P89 four-witness quotient -> P94A quotient)
  ↔ (for all original 3-proofs f,g,
      genuine P94A 4-cell(phi f,phi g)
        => genuine original P89 4-cell(f,g)).
```

This is `nativeGK5ANP89ToP94_injective_iff_reflect`, NOT an unconditional assertion that all P94A comparisons reflect to old source P89.

## 4. Exact old-P93 obstruction and new-P94A repair coexist

`nativeGK5ANP93NoButP94Yes_leftContext` and `nativeGK5ANP93NoButP94Yes_rightContext` prove for **any genuinely typed original context** that the SAME structural endpoints of the original P80 unit have `¬Nonempty(P93FourCell(phi f,phi g))` and `Nonempty(P94AFourCell(phi f,phi g))`.

`nativeGK5ANP93ToP94Class_not_injective` proves the existing canonical P93C→P94A four-class quotient map is **not injective** on genuine typed left-context 3-cell proofs. This is a precise historical nonfaithfulness statement: the extended P94A relation *necessarily collapses at least one pair* that present P93C distinguishes. It does not mean P94A destroys original raw Type-valued proof terms; they remain distinct until quotienting.

P94A is an **explicit selected enlargement**, not a deduction that historical P93C contained the missing coherence all along, nor a uniqueness/minimality theorem among all possible extensions.

## 5. Qi v4.7 — actual north C60 repaired physical comparison

New Qi Lean: [Qi v4.7 genuine north C60 P94A repair](../../formal/KUOS/Architecture/QiWuxingGK5ANP94NorthPhysicalRepairV4_7.lean).

At the real north C60 four-sector original F54 long3/short2 histories, with all independent two-Nat F45 stages and dual Site-category Blocks still typed, `fivefoldGK5ANP94NorthBoundary_repaired` proves the conjunction:
```text
¬Nonempty(old-north-P93C primitive compatibility)
¬Nonempty(old-north-P87→P93C full lift)
 Nonempty(true-north-P89→P94A full structural lift).
```
The actual physical map `fivefoldGK5ANP94NorthPhysicalFourClassMap` is **unconditional**:
```text
Original north P89 four-witness quotient
 -> (physical fifth-around Dart×Dart) × selected P94A four-witness quotient.
```
Its real representative specification, precise injectivity/reflection iff and complete original pentagon/square/odd-ZMod2 shadow factorization have all been Lean-checked.

`fivefoldGK5ANP94NorthLeftRepair` and `NorthRightRepair` keep the concrete original two adjacent F45 stage unit sources and prove P93C nonexistence versus P94A genuine repair on exactly these typed witnesses. `fivefoldGK5ANP94NorthPhysicalRepairAndOrientation` preserves the real physical fifth-around Dart closure and both **physically reversed 04/43 categorical Edge orientations** in conjunction with the repaired P94A higher family.

The physical Edge/Dart data are not identified with whole Mathlib NatIso, and physical geometry alone did not create the new P94A generators.

## 6. Remaining frontier

**GK5AO (candidate):** determine whether all three P80 primitive unit generators are *individually* necessary for every conservative selected higher extension, or whether the horizontal unit becomes derivable from already-present P93C constraints and newly adjoined context units. Independently analyze the exact reflection condition for the original P89→P94A quotient, perhaps using Type-valued noncommutative witness invariants. Do not conflate the source-specific P93C parity obstruction with a universal no-go for all targets.

All previous C60/五行, independent Kuu and prior GK5AK/GK5AL/GK5AM/Qi v4.5/v4.6 records remain intact.
