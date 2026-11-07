# Living Engi Cycle LEC-11 — exact source-aware overlap faithfulness criterion (verified)

**Date:** 2026-11-07 JST  
**Researcher/copyright:** 板倉英俊 / Hidetoshi Itakura  
**Repository:** `itakura-hidetoshi/KuuOS`, canonical `main`  
**Theorem PR:** [#3258](https://github.com/itakura-hidetoshi/KuuOS/pull/3258) — **MERGED**  
**Exact-source CI:** [#42359918998](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42359918998) — **SUCCESS**  
**Verified source HEAD:** `5d4ce63f86cec734b8ccfeeef5557211aede026c`  
**Test-merge SHA:** `f2051f94f4f096cdeb10443fd1f60de776923cf9`  
**Identical source/test-merge Git tree:** `dd47bb12ca9b7c31803925205ca3b8aded9d067e`  
**Theorem squash:** `2d80a2816d529913fc69f1988fde64b93cf9b889`  
**New module:** [`formal/Kuu/LivingEngi/SourceAwareOverlapDescentCriterion.lean`](../../formal/Kuu/LivingEngi/SourceAwareOverlapDescentCriterion.lean) — **353 lines, 23 theorem declarations, 23 explicit `#print axioms`**.  
**Public aggregation:** `KuuOSFormal`, original 107 roots preserved.

## 1. Source-aware necessary-and-sufficient descent condition

The [Living Engi Cycle specification](../LIVING_ENGI_CYCLE_VEDANA_TANHA_UPADANA_BHAVA_v0_1.md) §4/§4.1 distinguished ordinary local overlap defects from higher lifting/cohomology obstructions. LEC-01 proved local compatibility ↔ existence of a global function on a genuine set cover for the **ordinary sheaf of all functions**. LEC-10 supplied a concrete finite negative example: native north C60 F55-shaped source proof trees disagree but their chosen E7P4 shadow observations glue.

LEC-11 identifies exactly the **additional source-aware local proof obligation** needed to turn a global chosen observation into a global original source without altering or identifying the original source proof trees. For `U : I → Set X`, `s : LocalSections U Raw` and `q : Raw → Obs`, define:

```text
OverlapFiberFaithful U q s :=
  ∀ i j x hi hj,
    q (s i ⟨x, hi⟩) = q (s j ⟨x, hj⟩)
      → s i ⟨x, hi⟩ = s j ⟨x, hj⟩
```

On a **genuine cover**, the new principal theorem is:

```text
HasGlobal U s
  ↔ HasGlobal U (shadowSections U q s)
    ∧ OverlapFiberFaithful U q s
```

This condition is **relative to the given local atlas**. It does **not** require the quotient observer `q` to be injective on all conceivable raw proofs. Nor does it infer source equality from equality downstairs without the separate fiber-faithfulness evidence.

The proof proceeds through `Compatible U s ↔ Compatible U (q∘s) ∧ OverlapFiberFaithful U q s` and LEC-01's established full-function-sheaf gluing criterion; it does **not** assume arbitrary higher stack effectivity. Under a known shadow global, the failure of raw global gluing is also equivalent to failure of this exact local certificate.

## 2. Full theorem inventory

23 new declarations and 23 matching `#print axioms` are grouped as follows:

| Group | Names and scope |
| --- | --- |
| Ordinary local descent | `sourceCompatible_implies_shadowCompatible`, `sourceCompatible_implies_overlapFaithful`, `shadowCompatible_and_overlapFaithful_implies_sourceCompatible`, `sourceCompatible_iff_shadowCompatible_and_overlapFaithful` |
| Global necessary/sufficient | `sourceGlobal_implies_shadowGlobal`, `sourceGlobal_implies_overlapFaithful`, `shadowGlobal_and_overlapFaithful_implies_sourceGlobal`, `sourceGlobal_iff_shadowGlobal_and_overlapFaithful`, `no_sourceGlobal_iff_no_overlapFaithful_of_shadowGlobal` |
| Evidence boundary | `admittedShadow_and_overlapFaithful_implies_sourceGlobal`, `no_source_promotion_of_refuted_overlapFaithfulness` |
| Richer receiver | `sourceAwareReadout_source_exact`, `sourceAwareReadout_shadow_exact`, `sourceAwareReadout_injective`, `sourceCompatible_iff_refinedCompatible`, `sourceGlobal_iff_refinedGlobal` |
| Genuine north C60 native F55 instance | `nativeF55_twoChart_not_overlapFiberFaithful`, `nativeF55_constant_twoChart_overlapFiberFaithful`, `nativeF55_source_vs_alternative_overlap_faithfulness`, `nativeF55_sourceAwareReadout_separates_raw`, `nativeF55_twoChart_refined_no_global`, `nativeF55_constant_twoChart_refined_global`, `nativeF55_sourceAwareReadout_no_shadow_factor` |

The original source pair consists of the authentic **independent native F55-shaped** north C60 pentagon three-cell and that cell followed by an actual right unit. Their chosen E7P4 full-shadow observations are equal but their actual source terms differ. Thus the original LEC-10 two-chart atlas **fails** `OverlapFiberFaithful`. A separately constructed constant-source atlas satisfies it, but that is a different original source atlas, not a retrospective history-preserving repair.

## 3. Richer source-aware observation is not a cure for inconsistent evidence

The new source-aware readout is `sourceAwareReadout q r := (q r, r)`. The second projection returns `r` **as stored data**; the first projection exactly returns the original lawful shadow `q r`. It is injective and both preserves and reflects global source gluing:

```text
HasGlobal U s ↔
  HasGlobal U (shadowSections U (sourceAwareReadout q) s)
```

This construction is an intentionally **non-minimal** richer observer carrying the entire source. It does **not** invert the former noninjective shadow quotient, and for the native F55 counterexample its values cannot factor through the old shadow. Adding provenance to an incompatible original two-chart atlas does not magically create a consistent raw global witness.

The LEC-04 promotion gate admits exact shadow global plus *independent source fiber-faithfulness*. If source-faithfulness has been **refuted by a real local witness**, raw-global certification remains inadmissible. Mere absence of proof is still distinct from a proved refutation.

## 4. Lean verification and initial syntax correction

| Check | Verified outcome |
| --- | --- |
| Latest exact source | `5d4ce63f86cec734b8ccfeeef5557211aede026c` |
| Strict Lean | **10,316 / 10,316 SUCCESS** |
| All 23 theorem axiom reports | Only `propext`, `Classical.choice`, `Quot.sound`; many generic theorems use none |
| `sorryAx` | None |
| Governance and exact-head terminal | SUCCESS |
| Independent Kuu public API | SUCCESS |
| Workflow integrity | SUCCESS |
| Git tree (source/test-merge) | `dd47bb12ca9b7c31803925205ca3b8aded9d067e` — identical |

Initial CI [#42359697500](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42359697500) failed at Lean source line 265: the native overlap-faithfulness application had **one missing closing parenthesis**. All 23 `#print axioms` outputs appeared; the syntax issue was repaired with one closing `)` in commit `5d4ce63f86cec734b8ccfeeef5557211aede026c` (no theorem statement, assumption or axiom changes). The latest exact-source CI passed.

The fixed toolchain remains Lean `v4.30.0-rc2` / mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`, and protected validation-only #1558 remains Draft/Open/unmerged.

## 5. Interpretation, limits, and next obligations

The theorem operationalizes the research statement **“the fact that a lawful quotient glues is not sufficient proof that original source proof histories glue.”** The exact extra mathematical witness is now explicit and reusable.

- **取:** certified shadow ≠ certified original raw source; do not promote without the new exact overlap witness.
- **仮有:** a lawful quotient-level WORLD readout can still be maintained without raw-source restoration claims.
- **修復:** an alternate constant atlas and a provenance-enriched readout are *distinct operations*. Neither rewrites old Type-valued histories.
- **空・二諦・中道:** do not equate a quotient, selected presentation or receiver with intrinsic/global Truth; do not reject lawful scoped quotient results either.

This is a theorem for the **ordinary sheaf of all functions** and a concrete independent-native-F55 finite instantiation; it is not a new `H¹` class, actual geometric C60 cover, nontrivial higher-stack descent, or a faithful bridge to the **frozen/historical original F55/P77/GK5CG** Type proof history. No AI weight adjustment, patient outcome, metaphysical equivalence or execution authority follows.

The next separate proof frontier is a genuinely typed original-historical-to-native source comparison and, where warranted, nontrivial transport/higher coherence with original obstructions preserved.

---

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0. Append-only / tighten-only / overwrite-forbidden / same-root.
