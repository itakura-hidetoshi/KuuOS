# Living Engi Cycle LEC-10 — north C60 native F55 source/shadow gluing nonreflection (verified)

**Date:** 2026-11-07 JST  
**Researcher/copyright:** 板倉英俊 / Hidetoshi Itakura  
**Canonical repository:** \`itakura-hidetoshi/KuuOS\`, \`main\`  
**Theorem PR:** [#3256](https://github.com/itakura-hidetoshi/KuuOS/pull/3256) — **MERGED**  
**Exact-source CI:** [#42358724142](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42358724142) — **SUCCESS**  
**Verified source HEAD:** \`001c26e45fb72b39744309475cc2c35ca7b1f13f\`  
**Test-merge SHA:** \`09d2c79e171e0dca4ba42063f08f39293271052f\`  
**Source/test-merge tree:** \`a131d2354c62aa4f4305a8901b3254fb35b97a1d\` — **identical**  
**Merged theorem squash:** \`f58c4b8babb7f42578d2a6e6caaad5f4a56f9c49\`  
**New Lean source:** [\`formal/Kuu/LivingEngi/NativeF55CechSourceGluingObstruction.lean\`](../../formal/Kuu/LivingEngi/NativeF55CechSourceGluingObstruction.lean) — **297 lines; 21 theorems, 21 \`#print axioms\`**.  
**Public root:** \`KuuOSFormal\`, root 107 unchanged.

## 1. Problem — lawfully gluable shadow does not imply source gluing

The [Living Engi research specification](../LIVING_ENGI_CYCLE_VEDANA_TANHA_UPADANA_BHAVA_v0_1.md) §4 distinguishes a **specified local compatibility defect** from a **higher/global lifting obstruction**. LEC-01 already proves compatibility iff global gluing for the ordinary sheaf of all functions on a set cover. LEC-09 supplies the authentic independent native north C60 F55-shaped **raw Type-valued** witness pair:

- \`r₁ = northNativeF55PentagonCell\`: a native pentagon three-cell over the real north C60 F54 routes;
- \`r₂ = northNativeF55PentagonWithUnit\`: that raw three-cell followed by an actual right unit.

Their *raw proof trees differ*: \`r₁ ≠ r₂\`. Yet the exact **chosen** E7P4 full-shadow quotient \`q = northNativeF55Observe\` identifies them: \`q(r₁)=q(r₂)\`. The source is genuine, but the following **chart base is only an abstract two-chart singleton model**, *not* a demonstrated geometric open cover of C60.

Declare a cover \`U : Bool → Set Unit\` with \`U(true)=U(false)=univ\`. The original local source atlas \`s\` takes value \`r₁\` on the true chart and \`r₂\` on the false chart; the selected shadow atlas is \`q ∘ s\`. The exact result is:

\`\`\`text
HasGlobal U (q ∘ s)
AND
NOT HasGlobal U s
\`\`\`

The proof is concrete: all observed values agree, so LEC-01 glues them downstairs, but the raw witnesses disagree on their common overlap, so no *source-preserving* global function matches both upstairs.

In notation inspired by §4.1, there is a **nonzero raw overlap discrepancy** while the corresponding chosen shadow discrepancy is zero. Since the raw Type is not supplied with an additive group structure, **no numeric subtraction, universal norm, nonzero cohomology class or H¹ computation is asserted.** The Čech-language comparison is an ordinary overlap-equality test, not a theorem about a nontrivial higher lifting class.

## 2. Formal theorem families

| Family | Lean4 statements and proof scope |
| --- | --- |
| Positive direction | \`nativeF55Observe_preserves_compatible\`, \`nativeF55Observe_preserves_global\`: exact source gluing implies chosen observational gluing |
| Cover/source witness | \`nativeF55_twoChart_cover\`, \`nativeF55_twoChart_raw_overlap_disagrees\`, \`nativeF55_twoChart_raw_incompatible\`: genuine north C60 values are different on the model overlap |
| Lawful quotient gluing | \`nativeF55_twoChart_shadow_compatible\`, \`nativeF55_twoChart_shadow_global\`, \`nativeF55_twoChart_explicit_shadow_global\`: explicit observational compatibility and global readout |
| Nonreflection | \`nativeF55_twoChart_raw_no_global\`, \`nativeF55_twoChart_shadow_glues_not_raw\`, \`nativeF55_twoChart_finite_nonreflection\`: gluing downstairs does not reflect to the exact original local source atlas |
| Mathematical admission | \`nativeF55_twoChart_shadow_certificate_admitted\`, \`nativeF55_twoChart_raw_global_not_admissible\`, \`nativeF55_twoChart_promotion_levels_separate\`: LEC-04 admits the genuine shadow theorem and rejects the *refuted* raw-global claim |
| Source provenance | \`nativeF55_twoChart_trace_readout_exact\`, \`nativeF55_twoChart_trace_global_implies_raw_global\`, \`nativeF55_twoChart_trace_no_global\`: LEC-09 proof-carrying trace stores actual raw values; retaining them does not make incompatible sources gluable |
| Alternative, not repair | \`nativeF55_twoChart_constant_raw_global\`, \`nativeF55_twoChart_constant_shadow_equal\`, \`nativeF55_twoChart_constant_raw_changed\`, \`nativeF55_twoChart_no_exact_source_preserving_replacement\`: an alternative constant raw atlas glues and has the *same shadow* but **changes a source value** |

Each of the **21 theorem declarations** has a separate \`#print axioms\`. The source additionally defines the actual cover, the raw/shadow/trace atlases and the two evidence levels.

## 3. Exact-source verification

| Verification | Result |
| --- | --- |
| New source | 297 lines; one new independent Lean module |
| Integration | One new import in \`formal/KuuOSStrict.lean\`; old sources not edited |
| Strict Lean | **10,315 / 10,315 SUCCESS** |
| Governance Gate | **SUCCESS**; terminal exact-head receipt SUCCESS |
| Independent Kuu core/public API | **SUCCESS** |
| Workflow consolidation integrity | **SUCCESS** |
| 21 \`#print axioms\` | Only \`propext\`, \`Classical.choice\`, \`Quot.sound\` (one declaration uses none) |
| \`sorryAx\` | **none** |
| Source/test-merge Git tree | \`a131d2354c62aa4f4305a8901b3254fb35b97a1d\` — identical |
| Protected validation-only #1558 | Draft / OPEN / unmerged |

Completed exact-source workflow \`42358724142\` compiled \`Kuu.LivingEngi.NativeF55CechSourceGluingObstruction\`, \`KuuOSStrict\` and the retained public \`KuuOSFormal\`. Pinned Lean \`v4.30.0-rc2\` / mathlib \`5450b53e5ddc75d46418fabb605edbf36bd0beb6\` unchanged. Strict Lean ran with warning/sorry-as-error; new module built successfully.

## 4. Interpretation under the original Living Engi specification

- **受 (vedanā):** chosen observational quotient reports exactly what it preserves; it is not equivalent to the raw witness.
- **愛 (taṇhā):** preference for the shadow may be lawful, but preference never proves source gluing.
- **取 (upādāna):** claiming that the *original raw atlas* glues merely because its quotient atlas does is an explicitly refuted proof promotion for this witness.
- **有 (bhava):** a *conventional* globally gluable shadow can be retained within its scope. It must not overwrite the source evidence or masquerade as a fully reconstructing WORLD.
- **修復・還滅:** keeping the original source/trace and exhibiting the obstruction differs from replacing a conflicting source to get agreement. The alternate constant atlas is an **alternate model**, not a certified original-source-preserving repair.

These are scoped research correspondences, **not** claims about the psychological or clinical occurrence of suffering, Buddhist doctrine equivalence, AI learning or external action authorization.

## 5. Remaining frontier and explicit nonclaims

1. No faithful typed equivalence or source/target comparison with the **frozen historical original F55/P77/GK5CG** Type evidence has yet been proved. Independent native F55-shaped source ≠ historical original by declaration.
2. No actual geometric C60 open cover, nontrivial Čech \`H¹\`, gerbe/stack effectivity, higher holonomy obstruction, or universal descent failure has been constructed by this two-chart singleton example.
3. No runtime memory/weight update, physical operation, Truth/WORLD authority, governance or ActOS authorization follows from the Lean result.
4. Subsequent work may construct a **source-aware exact transport criterion** or an independently verified historic-to-native typed bridge, preserving provenance and nontrivial obstructions.

This is an append-only research/proof record. It **does not** revise the historic specification snapshots §0–18 or any prior original proof history.

---

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0. Append-only / tighten-only / overwrite-forbidden / same-root.
