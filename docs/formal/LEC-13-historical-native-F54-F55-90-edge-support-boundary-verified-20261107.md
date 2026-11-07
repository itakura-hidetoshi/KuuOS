# Living Engi Cycle LEC-13 — original F54/F55 proof history does not determine C60 physical support (verified)

**Date:** 2026-11-07 JST  
**Copyright/research:** 板倉英俊 / Hidetoshi Itakura  
**Repository:** `itakura-hidetoshi/KuuOS`; canonical branch `main`  
**Theorem PR:** [#3262](https://github.com/itakura-hidetoshi/KuuOS/pull/3262) — **MERGED**  
**Exact-source CI:** [#42363485222](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42363485222) — **SUCCESS**  
**Verified source HEAD:** `a3da778894da2e136a20fa9d4e9aac2d4d5771d4`  
**Test-merge SHA:** `c152bb74b92aa624a7a5ebfd9c933ca4dceb32c9`  
**Equal Git tree:** `2ef09aab2b5e511d29131d210abcf4334664aea8`  
**Theorem squash:** `ec57d5595ba4c8b80331fbce3c17bb54fb002238`  
**New module:** [`formal/KuuOSFormal/HistoricalNativeF54F47SupportLEC13.lean`](../../formal/KuuOSFormal/HistoricalNativeF54F47SupportLEC13.lean) — **355 lines**, 15 theorem declarations, one explicit supported-comparison constructor with a separate axiom print, **16 `#print axioms`**.  
**Additional import:** a single new `KuuOSFormal.lean` line; original sources and `KuuOSStrict` were not changed; public root 107 unchanged.

## 1. Structural finding: the missing physical C60 support

LEC-12 imported both **genuine historical original F55** raw Type-valued proof trees and the separately reconstructed independent native north C60 F55-shaped proof trees, proving a scoped common `(Int × Int) × ZMod 2` observation with exact Type-separated provenance. It did **not** construct a full original-F54-to-native-F54 boundary/endpoint functor.

LEC-13 takes a distinct step, grounded in the **existing old F47 calibrated four-boundary frame** `C60F47SquareFrame α β r s`. Here `r,s` are correctly dependent **historical original F54 routes** with old `Blocks` and both Nat depths, `α,β` are genuinely typed old F42 face-source comparisons, and the frame stores separately:

- `faceStep`: a genuine original F42/F43 categorical higher arrow, not a numerical substitute;
- `rotationStep`: an original F55 categorical higher arrow at the exact original F54 route endpoints, not a new native raw proof tree;
- a physical C60 edge;
- an existing original calibrated F47 mixed relation.

The retained F112-P39/P40 proofs show that *within this specified existing F47 frame type*, changing the geometric edge while retaining the same two source arrows leaves the calibration valid. The real 90-edge C60 carrier injects into this fixed two-arrow source fiber. This is **not** a theorem saying that arbitrary original F42/F55 raw proofs are already proven to be supported by every such physical edge; an independent source-to-geometry support condition is still needed for that stronger claim.

## 2. Main LEC-13 nonreconstruction theorem

Define, for a genuinely typed original F47 frame `B`:

```text
HistoricalF47F55Shadow(B)
 = ((c60F44OriginalF55Eval B.rotationStep).charge,
    (c60F44OriginalF55Eval B.rotationStep).phase)

HistoricalF47SourceShadow(B)
 = (historicalF47ThreeSourcePair(B), HistoricalF47F55Shadow(B))
```

For any real `e : Edge`, use the already proved genuine `historicalF47AllEdgeFiberMap B e`. LEC-13 proves that **all actual 90 distinct supports** preserve this full original higher-source-and-shadow observer, yet are still distinguished by the actual physical edge:

```text
∀ e : Edge,
  HistoricalF47SourceShadow(B_with_edge(e))
    = HistoricalF47SourceShadow(B)

Fintype.card Edge = 90
Function.Injective (historicalF47AllEdgeFiberMap B)
```

The new noninjectivity and nonfactorization/no-decoder theorems show:

```text
NOT EXISTS decode : (OriginalF42Arrow × OriginalF55Arrow × FullShadow) → Edge,
  FOR ALL e, decode(HistoricalF47SourceShadow(B_with_edge(e))) = e
```

This is a **genuine finite fiber/observable-support obstruction**, not a nonzero Čech `H¹`, a higher-stack effectivity theorem, or a defect of the original F55 category. Merely appending full signed integer charges and braided phase to the old Type-indexed source arrow pair does not supply the separate physical-support witness.

## 3. What extra evidence suffices, and what does not

The richer observer `lec13SupportedSourceShadow B` stores the old two-arrow pair and its chosen complete F55 shadow **alongside** `frameKuuEdge B`. LEC-13 proves this supported observation is injective on the **specified 90-edge family**. This does **not** assert it is globally injective over every possible old F47 frame, or that the old F42/F55 arrows geometrically descend to the selected edge without separate relation proofs.

The additional typed structure `LEC13OriginalNativeCalibration B` requires all of the following independent, caller-supplied evidence:

1. A true retained historical original F55 raw `PresentedCell r s` at the **actual original F54 endpoints**;
2. A proof that its original F55 quotient arrow equals the exact `B.rotationStep`;
3. A truly independent native north C60 F55 raw source term;
4. A proof that their specified LEC-12 common signed/phase readouts agree.

The existence of such a calibration **for arbitrary B is NOT proved or assumed**. Indeed, genuine physical F47 rotation squares normally carry charge `(0,1)` and odd phase, unlike the native north *pentagon* `(1,0)` and phase zero. One must not fabricate a comparison to the wrong native generator. The natural next concrete test uses an **actual native hexagon disjoint-rotation square**, with appropriately typed native endpoints.

**Conditional on a supplied** `LEC13OriginalNativeCalibration B`, Lean constructs a separate `LEC13SupportedOriginalNative B C` packet for each true C60 edge. Every packet retains the old exact raw witness through the calibration index, the old F47 quotient arrow and exact original F54 route endpoints, the selected independent native raw witness, the common-shadow certificate, and a true `Edge`. The 90 supported packets are injectively distinct, while a source+shadow+native-raw-only decoder is still impossible.

These statements prove what survives **when given all specified typed input proofs**. They do not constitute a construction of an unrestricted old/native F54/F55 faithful functor or a universal source-matching existence theorem.

## 4. Exact Lean result and **explicit axiom transparency**

| Verification | Outcome |
| --- | --- |
| Exact-source [CI #42363485222](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42363485222) | **completed SUCCESS** |
| Strict Lean | **10,318 / 10,318 SUCCESS** |
| Added module | 355 source lines, 15 theorem declarations |
| Typed original/native supported constructor | 1, separately audited |
| `#print axioms` | **16** |
| `sorryAx` | **none** |
| New `axiom` declarations | **none** |
| Governance, selected independent public API and structural checks | **SUCCESS** |
| Exact-source / test-merge Git tree | **identical** `2ef09aab2b5e511d29131d210abcf4334664aea8` |
| Change scope | only new mixed public module and one additive import |

**Important difference from LEC-12:** These LEC-13 proof dependencies are **NOT standard-axioms-only**. Their transitive F112 geometric proof dependencies include the standard `propext`, `Classical.choice`, `Quot.sound` **and six pre-existing `native_decide`-generated axioms**:

```text
pentagonalSlotIndex_bijective._native.native_decide.ax_1_1
pentagonalSlotIndex_next._native.native_decide.ax_1_1
pentagonalSlotIndex_next._native.native_decide.ax_1_2
pentagonalSlotIndex_next._native.native_decide.ax_1_3
pentagonalSlotIndex_next._native.native_decide.ax_1_4
pentagonalSlotIndex_next._native.native_decide.ax_1_5
```

No new axiom is introduced in LEC-13; these are inherited from the frozen, previously compiled real-C60 geometry/edge equivalence chain. **Strict Lean success proves compilation with these transitive axioms; it does not prove an axioms-free recreation of all C60 geometric facts.** Discharging these six via fully kernel-reducible combinatorial derivations is an honest separate proof-hardening task, not a reason to silently label this stage “standard-only.”

The initial CI for head `ab581ed6cbb9620d8a05fdc4871f5d28fa6d91b8` failed due to an unapplied-lambda rewrite and `-/` inside a comment. The correction at `a3da778894da2e136a20fa9d4e9aac2d4d5771d4` normalized the exact term with `change`/`simp only` and used an unambiguous comment. No theorem statement, original source datum, or assumption was weakened.

## 5. Living Engi interpretation and next exact frontier

The extra physical support is **provenance/geometry**, orthogonal to the chosen observer's raw-history and full signed-phase information. In the research specification's terms, an observed/valued shadow must not be silently promoted to a global and source-supported physical relation. Legitimate, scoped `ConventionalBhava` can consume a chosen common observation, while missing support or an explicit no-decoder certificate remains visible. A Type-valued historical raw source is neither a physical-edge witness nor execution authority by itself.

**Next LEC-14:** construct at least one **inhabited, appropriately typed** old physical-F47 F55 *square* versus independent native real C60 hexagon-F55 *square* comparison, preserving actual typed old/native endpoints and real support; then test whether full source/target transport can preserve all nine F55 constructors and original P77/GK5CG higher source evidence. Do not infer physical identification from a common `(0,1;1)` value alone. Independently remove the six inherited `native_decide` axioms if a standard-axioms-only geometric proof is required.

No AI weight update, clinical claim, general Čech/stack theorem, geometric equivalence of old/new F54 sources or ActOS execution license has been established.

---

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0. Append-only / tighten-only / overwrite-forbidden / same-root.
