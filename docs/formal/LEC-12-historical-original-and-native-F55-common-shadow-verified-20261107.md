# Living Engi Cycle LEC-12 — genuine original F55 ↔ independent native F55 common-shadow comparison (verified)

**Date:** 2026-11-07 JST  
**Research/copyright:** 板倉英俊 / Hidetoshi Itakura  
**Canonical repo:** `itakura-hidetoshi/KuuOS`, `main`  
**Theorem PR:** [#3260](https://github.com/itakura-hidetoshi/KuuOS/pull/3260) — **MERGED**  
**Latest exact-source CI:** [#42361244071](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42361244071) — **SUCCESS**  
**Verified source HEAD:** `e292a775639e72ec62111db963783e4f2785204c`  
**Test-merge:** `c89233767cec73b312dca0aa97acd5902a35a8d8`  
**Source/test-merge Git tree:** `d999152254a878df75fade0fe70082765bb0a1e2` — equal  
**Merged theorem squash/main:** `f700f0d680865301d6872c5e25b7d2541ad591b6`  
**New module:** [`formal/KuuOSFormal/HistoricalNativeF55CommonShadowLEC12.lean`](../../formal/KuuOSFormal/HistoricalNativeF55CommonShadowLEC12.lean) — 306 lines, **14 theorem declarations and 2 typed proof-carrying data constructors**, 16 explicit `#print axioms` calls.  
**Integration:** one additive `KuuOSFormal` import; existing public root 107 unchanged. **No independent `KuuOSStrict` / `Kuu/` source changed.**

## 1. Why an explicitly mixed original/native module is necessary

Earlier LEC-09/10/11 showed that **independently reconstructed** native north C60 F55-shaped raw terms cannot be faithfully recovered from one chosen E7P4 full-shadow quotient and established a precise overlap-fiber-faithful gluing criterion. These results deliberately did **not** import the **historical original** F55 Type source.

The new LEC-12 module is a **first actual mixed-typed comparison**. It imports two already established, *different* raw source grammars:

1. **Historical ORIGINAL:** `KUOS...` `OriginalF45BracketTree.DepthRotationRoute.PresentedCell`. Its original categorical `Blocks`, both independent Nat depths, original F54 source/target routes, and nine F55 constructors remain preserved. The existing original F59/F58 braided Gray interpretation `c60F55SourceNative` is used, not reconstructed from the native quotient.
2. **Independent native:** `Kuu.F112.Physical.KuuNativeF45Tree.DepthRotationRoute.PresentedCell`; the actual **north C60** pentagon witnesses are `northNativeF55PentagonCell` and `northNativeF55PentagonWithUnit`.

These **different Type carriers are never treated as definitionally equal**, and a full original-to-native source functor or equivalence has **not** been constructed. The old pentagon side has genuine arbitrary typed four-stage `t₁,...,t₄` inputs; it is NOT claimed that these input objects geometrically coincide with the selected native north C60 stages.

For preservation of the independent authority boundary, LEC-12 lives in `formal/KuuOSFormal/`, in the retained/mixed public aggregate, NOT in `formal/Kuu/` or `KuuOSStrict`. Existing higher F55/P77/GK5CG sources are not edited.

## 2. Precise comparison theorem: same numeric receiver, distinct raw witnesses

Define the **common observation carrier**:

```text
HistoricalNativeF55CommonShadow = (Int × Int) × ZMod 2
```

The two readings are separately constructed:

```text
historicalF55CommonReadout oldRaw
  = ((c60F55SourceNative oldRaw).charge,
     (c60F55SourceNative oldRaw).phase)

nativeNorthF55CommonReadout nativeRaw
  = nativeRaw.nativeShadow
```

The existing independently proved nine-constructor results imply, **for every original raw F55 term** and every selected independent native north C60 raw F55 term:

```text
phase = (second_signed_charge : ZMod 2)
```

Using a true old `PresentedCell.pentagon t₁ t₂ t₃ t₄`, its old source history followed by a genuine right identity, and the corresponding *distinct* new native north C60 pentagon and right-unit history, LEC-12 proves:

```text
old_pentagon ≠ old_pentagon_withUnit
native_pentagon ≠ native_pentagon_withUnit

oldShadow(old_pentagon)       = nativeShadow(native_pentagon)
oldShadow(old_pentagon+unit)  = nativeShadow(native_pentagon+unit)
oldShadow(old_pentagon)       = oldShadow(old_pentagon+unit)
```

The calibrated common value for both original generators is `((1,0),0)`. A right unit has neutral Gray/charge-phase evaluation, **but does not make the raw original terms equal**.

Hence the chosen common numeric observation is **not injective on either specified raw source family**. That loss of information is proved, not inferred from a plausible-looking numeric equality.

## 3. Typed pairwise proof-carrying comparison receipts

`HistoricalNativeF55Aligned Hist oldRead` is a Type-valued record storing **three independent facts**:

- `historical : Hist`: full historical raw witness;
- `independent : NorthNativeF55Raw`: full independent native raw witness;
- `shadowAgreement`: a proved equality of the exact common numeric readouts.

LEC-12 constructs `historicalNativePentagonAligned` and `historicalNativeWithUnitAligned` from the genuine source terms, not from a fabricated map. It proves those packets are **distinct** because their stored original raw histories differ even though their common readouts coincide.

This is a **faithful retention of a selected pair of real histories as data**, not a faithful functor from the entire historical F55 source category to the new native F55 source category. An equality downstairs is never promoted to raw equality upstairs.

## 4. Exact-source Lean4 audit

| Verification | Result |
| --- | --- |
| Strict Lean | **10,317 / 10,317 SUCCESS** |
| New theorem declarations | **14** |
| New proof-carrying constructors `historicalNativePentagonAligned` / `historicalNativeWithUnitAligned` | **2** |
| Explicit `#print axioms` | **16**; standard `propext`, `Classical.choice`, `Quot.sound` only (old raw inequality uses none) |
| `sorryAx` | **none** |
| Governance / exact-head terminal | **SUCCESS** |
| Independent Kuu retained public API | **SUCCESS** |
| Public proof roots restoration and relevant selected integrity jobs | **SUCCESS** |
| Source/test-merge Git tree | **identical** — `d999152254a878df75fade0fe70082765bb0a1e2` |
| Changed Lean source | New 306-line mixed public-layer module only; one additional `KuuOSFormal` import |

No Lean v4.30.0-rc2 or pinned mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` change. The separately protected #1558 remains Draft/Open/unmerged.

## 5. Relationship to the original Living Engi Cycle

- **受:** the common signed/phase shadow is a lawful *selected evaluation* of two DIFFERENT source types, not an intrinsic identification of source proof histories.
- **愛:** ranking or reuse of compatible observational values does not establish a source functor, higher coherence or original-type equality.
- **取:** asserting that the old raw F55 proof equals the independent native raw F55 proof just because the two have value `((1,0),0)` would be a promotion across an unproved boundary.
- **仮有:** a scoped WORLD model may use the common calibrated receiver while separately retaining its actual historical and native Type-valued provenance.
- **修復:** a richer proof-carrying representation retains both histories; it does not overwrite either old F55/P77/GK5CG source or claim a completed historical-to-native migration.

**Limits:** No full faithful old-original ↔ native F54/F55 equivalence; no literal identity of old four-stage t_i and native north geometry; no transfer of original P77/GK5CG 4- to 8-cell witnesses or their obstruction; no nonzero H¹, gerbe/stack effectivity, universal higher descent, AI weight update, clinical proof or ActOS authorization. This is a **real but scoped first cross-authority comparison**.

## 6. Next research frontier

LEC-13 should attempt a *boundary-indexed* old F54 → independent native F54 comparison with explicit original `Blocks`/two Nat depths and physical C60 endpoints, then prove which F55 constructors it transports while checking all required source/target equalities and the original P77/GK5CG higher witness types. Where a faithful map fails, retain a concrete obstruction and source-history packets rather than inferring source equality from calibrated charges.

---

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0. Append-only / tighten-only / overwrite-forbidden / same-root.
