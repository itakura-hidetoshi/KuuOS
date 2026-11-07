# Living Engi LEC-13B — original swallowtail-certified witness transport (verified)

**Date:** 2026-11-07 JST  
**Author and copyright:** Hidetoshi Itakura / 板倉英俊  
**Repository:** `itakura-hidetoshi/KuuOS`, canonical `main`  
**Theorem PR:** [#3263](https://github.com/itakura-hidetoshi/KuuOS/pull/3263) — **MERGED**  
**Exact-source CI:** [#42366081346](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42366081346) — **completed SUCCESS**  
**Verified PR HEAD:** `26c4a856d415ee03215e0faee4667eb29ef2ad61`  
**Source/test-merge tree:** `b789374a8ad30155ae08fd7e35f660ed9e1e7a7f` — **identical**  
**Test-merge commit:** `ee405af51a63fe3fff44a5a9ab6657b6e9dad649`  
**Merged squash:** `703d5c1aa6d8b7da5f66accaea377d85e84dbff4`  
**Proof-bearing module:** [`SwallowtailWitnessTransportLEC13.lean`](../../formal/KuuOSFormal/SwallowtailWitnessTransportLEC13.lean), 376 physical source lines, 17 theorem declarations and three separately audited constructions, total **20 `#print axioms`**.  
**Public import:** one additive line in `formal/KuuOSFormal.lean`; original independent `KuuOSStrict` and public root 107 are unchanged.

## 1. Exact theorem scope

This result uses the **original** coherent biadjunction actual-lift datum of V5.101, retaining the same `F,G,η,ε`, independently certified forward/reverse swallowtails, original interchangers and strong-transformation modification boundaries. The V5.112 exchange laws have the required **two different whiskering orientations**. No new swallowtail axioms, synthetic interchanger or old/native raw-source equivalence is inserted.

For an actual isomorphism `e : a ≅ b`, the concrete endomorphism witness transport is the genuine equivalence

```lean
witnessConjugation e : (a ⟶ a) ≃ (b ⟶ b)
f ↦ e.inv ≫ f ≫ e.hom
```

with inverse `g ↦ e.hom ≫ g ≫ e.inv`. Lean proves exact reversibility, equality reflection, ordered composition, identities, sequential transport, finite-list history roundtrip and whole-list equality reflection. For ordinary **function-valued local sections**, overlap compatibility and `HasGlobal` are both preserved and reflected, even without an assumed cover, because the receiver-value map itself is an equivalence. This is **not** higher-stack effectivity.

The two normalized original swallowtail defects are identities. More importantly, the forward/reverse **modification exchange** proof establishes the exact transport of each unit/counit modification to its prescribed opposite triangle boundary. Mere invertibility alone would not prove this boundary-coherence equality. Both transports are instantiated from the unmodified `actualLiftCoherentBiadjunctionDatum`.

The genuine retained historical F55 primitive-pentagon and right-unit raw witnesses are **different Type-valued proofs** but have the same specified LEC-12 common readout. For any explicitly supplied shadow-only receiver followed by reversible witness conjugation, a total raw reconstruction remains impossible. The `Factors` no-go is based on the original collision, without asserting an old-to-independent-native faithful source map.

## 2. Lean4 structural repair and CI-unblocking

Initial [run #42363560669](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42363560669) on pre-repair source failed at the original lines 232 and 249 because `rw` could not match the categorical composite under its **actual parenthesization**. The old V5.112 lemmas were correct; outer `Sigma.inv ≫` and inner exchange had to be related by explicitly applying `congrArg (fun z => Sigma.inv ≫ z)`. The forward law requires `.symm`; the reverse law has the direct orientation; `simp` cancels the existing genuine isomorphism. Fix [`1159cd6`](https://github.com/itakura-hidetoshi/KuuOS/commit/1159cd6cb6220c42d3d23377be840cbc65477107) changed proof terms only, with no theorem-statement/assumption weakening.

The subsequent absence of CI was diagnosed separately: direct GitHub API showed `mergeable_state=dirty` from competing **additive import lines** at the same position in `formal/KuuOSFormal.lean`. Current main included `HistoricalNativeF54F47SupportLEC13`; the theorem branch included `SwallowtailWitnessTransportLEC13`. Two-parent merge [`26c4a856`](https://github.com/itakura-hidetoshi/KuuOS/commit/26c4a856d415ee03215e0faee4667eb29ef2ad61) retained both imports; the theorem-module blob was unchanged (`9209f004ebc16b2eef28948a2ed888a423280727`). GitHub then reported `mergeable=true` and automatically registered exact-source checks. A temporary source-identical reentry PR #3265 was closed unmerged after the conflict cause was established.

## 3. Independent verification receipt

| Check | Observed result |
| --- | --- |
| Exact-source [run #42366081346](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42366081346) | **completed SUCCESS** |
| Strict Lean | **10,319 / 10,319 SUCCESS** |
| Governance selected jobs | **30 / 30 SUCCESS** |
| PR-triggered workflows | 10 completed: success or expected skipped |
| Check runs | 42, none failed or pending |
| New theorem declarations | 17 |
| New explicit `#print axioms` | 20 (17 theorems + 3 constructions) |
| New declarations' complete transitive axioms | only `propext`, `Classical.choice`, `Quot.sound` |
| `sorryAx`, new axioms | **none** |
| Changed Lean warnings / errors | **0 / 0** |
| Source/test-merge Git tree | **identical**, `b789374a8ad30155ae08fd7e35f660ed9e1e7a7f` |
| Squash merge main | `703d5c1aa6d8b7da5f66accaea377d85e84dbff4` |

This **LEC-13B module's 20 audited declarations** are standard-axioms-only. A separate verified LEC-13A physical C60 90-edge result (#3262) retains six already-known transitive `native_decide` generated axioms. The two axiom-dependency statements must **not** be conflated.

## 4. Original boundaries, non-claims, next step

- The original historical F54/F55 and independently reconstructed native F54/F55 remain separate source Types, histories and authority scopes. A shared signed/phase shadow is not a faithful equivalence; conjugating a lossy shadow cannot invert its prior loss.
- The original F47 real C60 physical-support boundary and its 90-edge no-decoder result remain intact and separate from the category-level swallowtail transport. The proof does not supply a geometrically supported old-to-native correspondence for every original edge or raw F55 term.
- No fully source/target-indexed historical F54 → independent native F54 functor, all-nine-F55-constructor equivalence, P77/GK5CG high-cell descent, nonzero Čech `H¹`, general gerbe/stack effectivity, external execution authority or clinical/AI-weight change follows.
- The next **LEC-14** target remains an *inhabited* old physical F47 F55 square versus independent real native C60 hexagon F55 square, preserving actual typed endpoints and physical support. The north pentagon with different charge/phase must not be substituted.

Pinned Lean `v4.30.0-rc2`; mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`; original Lean definitions and independent `KuuOSStrict` unchanged; published root 107; protected PR #1558 Draft/Open/unmerged.

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0. Append-only / tighten-only / overwrite-forbidden / same-root.
