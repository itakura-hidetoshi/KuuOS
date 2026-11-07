import Kuu.LivingEngi.NativeF55CechSourceGluingObstruction

/-!
# LEC-11 — necessary and sufficient source-aware gluing certificate

LEC-10 supplies a concrete native north C60 F55-shaped source collision:
the chosen E7P4 full shadow glues, but the exact raw Type-valued atlas
does not. This module separates the exact *extra* proof obligation
needed to recover raw gluing from a lawful shadow global readout.

For the ordinary sheaf of ALL functions, on a genuine set cover:
  HasGlobal raw ↔
    HasGlobal (selected observation ∘ raw)
    ∧ overlap-fiber faithfulness of the ORIGINAL raw atlas.

The additional condition is pairwise, source-aware, and relative to the
selected raw atlas; it does NOT assume global injectivity of the quotient.
Thus no historic F55 Type values are reconstructed merely from a shadow.

A refined observer (q(raw), raw) is injective by construction and yields
an exact source-recovering readout, but it does NOT retroactively make an
incompatible local atlas gluable, nor is it a minimal-code receiver.

The north C60 raw witnesses are genuine independent native F55 sources,
but their LEC-10 Bool-indexed Unit chart base is abstract and is NOT a
geometric cover of C60 itself. No H¹, stack/gerbe, external authority,
historic frozen F55/P77/GK5CG equivalence, or runtime AI mutation claim.
-/

namespace Kuu.LivingEngi

open Kuu.F112.Physical

set_option autoImplicit false

universe uLEC11X uLEC11I uLEC11Raw uLEC11Obs

section GeneralFunctionSheaf

variable {X : Type uLEC11X} {I : Type uLEC11I}
variable {Raw : Type uLEC11Raw} {Obs : Type uLEC11Obs}

/-- Explicit chosen observation of the exact original local source atlas. -/
def shadowSections (U : I → Set X) (q : Raw → Obs)
    (s : LocalSections U Raw) : LocalSections U Obs :=
  fun i x => q (s i x)

/-- The exact MISSING premise in general shadow-to-source descent:
two local source values must agree whenever their selected observations
are equal ON THEIR ACTUAL OVERLAP. This is weaker than global injectivity
of q on all raw terms, and relative to the specified source atlas. -/
def OverlapFiberFaithful
    (U : I → Set X) (q : Raw → Obs)
    (s : LocalSections U Raw) : Prop :=
  ∀ (i j : I) (x : X) (hi : x ∈ U i) (hj : x ∈ U j),
    q (s i ⟨x, hi⟩) = q (s j ⟨x, hj⟩) →
      s i ⟨x, hi⟩ = s j ⟨x, hj⟩

/-- Raw compatibility always descends to ANY observation. -/
theorem sourceCompatible_implies_shadowCompatible
    (U : I → Set X) (q : Raw → Obs)
    (s : LocalSections U Raw) (h : Compatible U s) :
    Compatible U (shadowSections U q s) := by
  intro i j x hi hj
  exact congrArg q (h i j x hi hj)

/-- Exact raw compatibility forces relative source equality even if
the quotient observation alone would identify more source histories. -/
theorem sourceCompatible_implies_overlapFaithful
    (U : I → Set X) (q : Raw → Obs)
    (s : LocalSections U Raw) (h : Compatible U s) :
    OverlapFiberFaithful U q s := by
  intro i j x hi hj _
  exact h i j x hi hj

/-- Chosen shadow compatibility plus the missing source-level
faithfulness condition SUFFICES to reconstruct raw compatibility. -/
theorem shadowCompatible_and_overlapFaithful_implies_sourceCompatible
    (U : I → Set X) (q : Raw → Obs)
    (s : LocalSections U Raw)
    (hshadow : Compatible U (shadowSections U q s))
    (hfaith : OverlapFiberFaithful U q s) :
    Compatible U s := by
  intro i j x hi hj
  exact hfaith i j x hi hj (hshadow i j x hi hj)

/-- The exact elementary local descent criterion for this entire
ordinary function-sheaf class. No higher coherence is assumed. -/
theorem sourceCompatible_iff_shadowCompatible_and_overlapFaithful
    (U : I → Set X) (q : Raw → Obs)
    (s : LocalSections U Raw) :
    Compatible U s ↔
      Compatible U (shadowSections U q s) ∧
        OverlapFiberFaithful U q s := by
  constructor
  · intro h
    exact ⟨sourceCompatible_implies_shadowCompatible U q s h,
      sourceCompatible_implies_overlapFaithful U q s h⟩
  · rintro ⟨hshadow, hfaith⟩
    exact shadowCompatible_and_overlapFaithful_implies_sourceCompatible
      U q s hshadow hfaith

/-- Exact raw global values can be observed globally without
reconstructing the raw values from observations. -/
theorem sourceGlobal_implies_shadowGlobal
    (U : I → Set X) (q : Raw → Obs)
    (s : LocalSections U Raw) :
    HasGlobal U s → HasGlobal U (shadowSections U q s) := by
  rintro ⟨g, hg⟩
  refine ⟨fun x => q (g x), ?_⟩
  intro i x
  exact congrArg q (hg i x)

/-- An actual global source entails the missing relative overlap witness. -/
theorem sourceGlobal_implies_overlapFaithful
    (U : I → Set X) (q : Raw → Obs)
    (s : LocalSections U Raw) (h : HasGlobal U s) :
    OverlapFiberFaithful U q s :=
  sourceCompatible_implies_overlapFaithful U q s
    (global_implies_compatible U s h)

/-- Given a genuine covering family, the gluable shadow plus exact
overlap fiber information reconstructs the ORIGINAL local source gluing. -/
theorem shadowGlobal_and_overlapFaithful_implies_sourceGlobal
    (U : I → Set X) (q : Raw → Obs)
    (s : LocalSections U Raw) (hcover : Covers U)
    (hshadow : HasGlobal U (shadowSections U q s))
    (hfaith : OverlapFiberFaithful U q s) :
    HasGlobal U s := by
  have hsc : Compatible U (shadowSections U q s) :=
    global_implies_compatible U (shadowSections U q s) hshadow
  have hraw : Compatible U s :=
    shadowCompatible_and_overlapFaithful_implies_sourceCompatible
      U q s hsc hfaith
  exact (compatible_iff_hasGlobal U s hcover).1 hraw

/-- MAIN LEC-11: source global existence iff (lawful chosen quotient
global existence AND the additional exact local source-fiber witness). -/
theorem sourceGlobal_iff_shadowGlobal_and_overlapFaithful
    (U : I → Set X) (q : Raw → Obs)
    (s : LocalSections U Raw) (hcover : Covers U) :
    HasGlobal U s ↔
      HasGlobal U (shadowSections U q s) ∧
        OverlapFiberFaithful U q s := by
  constructor
  · intro h
    exact ⟨sourceGlobal_implies_shadowGlobal U q s h,
      sourceGlobal_implies_overlapFaithful U q s h⟩
  · rintro ⟨hshadow, hfaith⟩
    exact shadowGlobal_and_overlapFaithful_implies_sourceGlobal
      U q s hcover hshadow hfaith

/-- Once the selected shadow global exists, the precise remaining
obstruction to raw global gluing is failure of overlap faithfulness.
No assertion is made that the obstruction is a cohomology class. -/
theorem no_sourceGlobal_iff_no_overlapFaithful_of_shadowGlobal
    (U : I → Set X) (q : Raw → Obs)
    (s : LocalSections U Raw) (hcover : Covers U)
    (hshadow : HasGlobal U (shadowSections U q s)) :
    (¬ HasGlobal U s) ↔ (¬ OverlapFiberFaithful U q s) := by
  constructor
  · intro hno hfaith
    exact hno
      (shadowGlobal_and_overlapFaithful_implies_sourceGlobal
        U q s hcover hshadow hfaith)
  · intro hno hsource
    exact hno (sourceGlobal_implies_overlapFaithful U q s hsource)

/-- LEC-04: a certified SHADOW global does not alone promote the raw
global. The explicitly independent overlap source proof is required. -/
theorem admittedShadow_and_overlapFaithful_implies_sourceGlobal
    (U : I → Set X) (q : Raw → Obs)
    (s : LocalSections U Raw) (hcover : Covers U)
    (ev : PromotionEvidence (HasGlobal U (shadowSections U q s)))
    (hadmit : Admissible ev)
    (hfaith : OverlapFiberFaithful U q s) :
    HasGlobal U s :=
  shadowGlobal_and_overlapFaithful_implies_sourceGlobal
    U q s hcover (admitted_sound ev hadmit) hfaith

/-- A PROVED counterexample to source-faithfulness excludes ANY
admitted certificate for exact global raw gluing (even if shadow glues).
Unchecked evidence is a different state, not a proof of failure. -/
theorem no_source_promotion_of_refuted_overlapFaithfulness
    (U : I → Set X) (q : Raw → Obs)
    (s : LocalSections U Raw)
    (hbad : ¬ OverlapFiberFaithful U q s)
    (ev : PromotionEvidence (HasGlobal U s)) :
    ¬ Admissible ev := by
  intro hadmit
  exact hbad
    (sourceGlobal_implies_overlapFaithful U q s (admitted_sound ev hadmit))

/-- A provenance-refined observation stores both the exact chosen
shadow and the genuine original source. This is a new richer observation,
NOT a claim that the old quotient was raw-faithful. -/
def sourceAwareReadout (q : Raw → Obs) (r : Raw) : Obs × Raw :=
  (q r, r)

/-- Exact raw source can be retrieved from the refined observation. -/
theorem sourceAwareReadout_source_exact
    (q : Raw → Obs) (r : Raw) :
    (sourceAwareReadout q r).2 = r := rfl

/-- The previous lawful quotient remains exactly the first projection. -/
theorem sourceAwareReadout_shadow_exact
    (q : Raw → Obs) (r : Raw) :
    (sourceAwareReadout q r).1 = q r := rfl

/-- The richer source-aware receiver is faithful by containing raw data;
this is not an inverse to the OLD chosen shadow quotient. -/
theorem sourceAwareReadout_injective
    (q : Raw → Obs) :
    Function.Injective (sourceAwareReadout q) := by
  intro r₁ r₂ h
  exact congrArg (fun p : Obs × Raw => p.2) h

/-- A gluable refined atlas and a gluable original raw atlas have
exactly the same compatibility status, without requiring a cover. -/
theorem sourceCompatible_iff_refinedCompatible
    (U : I → Set X) (q : Raw → Obs)
    (s : LocalSections U Raw) :
    Compatible U s ↔
      Compatible U (shadowSections U (sourceAwareReadout q) s) := by
  constructor
  · exact sourceCompatible_implies_shadowCompatible
      U (sourceAwareReadout q) s
  · intro h i j x hi hj
    exact congrArg (fun p : Obs × Raw => p.2) (h i j x hi hj)

/-- A refined observation preserves AND reflects global gluing because
the original raw Type-valued witness is retained as an explicit field. -/
theorem sourceGlobal_iff_refinedGlobal
    (U : I → Set X) (q : Raw → Obs)
    (s : LocalSections U Raw) :
    HasGlobal U s ↔
      HasGlobal U (shadowSections U (sourceAwareReadout q) s) := by
  constructor
  · exact sourceGlobal_implies_shadowGlobal
      U (sourceAwareReadout q) s
  · rintro ⟨g, hg⟩
    refine ⟨fun x => (g x).2, ?_⟩
    intro i x
    exact congrArg (fun p : Obs × Raw => p.2) (hg i x)

end GeneralFunctionSheaf

/-! Instantiation to the *actual independent native north C60 F55 source*
values of LEC-09, placed in LEC-10's abstract two-chart model. -/

/-- The exact extra LEC-11 certificate FAILS on the LEC-10 original
native raw source atlas. Its selected quotient really does glue. -/
theorem nativeF55_twoChart_not_overlapFiberFaithful :
    ¬ OverlapFiberFaithful northNativeF55TwoChartCover
      northNativeF55Observe northNativeF55TwoChartRaw := by
  intro hfaith
  have hshadow :
      northNativeF55Observe
          (northNativeF55TwoChartRaw true ⟨(), Set.mem_univ ()⟩) =
        northNativeF55Observe
          (northNativeF55TwoChartRaw false ⟨(), Set.mem_univ ()⟩) := by
    simpa [northNativeF55TwoChartRaw] using
      northNativeF55_observed_equal
  exact nativeF55_twoChart_raw_overlap_disagrees
    (hfaith true false () (Set.mem_univ ()) (Set.mem_univ ()) hshadow

/-- The separate ALTERNATIVE constant source atlas IS faithful on
the same abstract overlaps because it uses one actual raw source. -/
theorem nativeF55_constant_twoChart_overlapFiberFaithful :
    OverlapFiberFaithful northNativeF55TwoChartCover
      northNativeF55Observe northNativeF55TwoChartConstantRaw := by
  intro i j x hi hj _
  rfl

/-- Same lawful shadow gluing, distinct exact source-faithfulness statuses:
a source substitution cannot be called a proof of old-source repair. -/
theorem nativeF55_source_vs_alternative_overlap_faithfulness :
    (¬ OverlapFiberFaithful northNativeF55TwoChartCover
        northNativeF55Observe northNativeF55TwoChartRaw) ∧
      OverlapFiberFaithful northNativeF55TwoChartCover
        northNativeF55Observe northNativeF55TwoChartConstantRaw :=
  ⟨nativeF55_twoChart_not_overlapFiberFaithful,
    nativeF55_constant_twoChart_overlapFiberFaithful⟩

/-- The genuine pair remains distinct under the source-refined receiver
even though the old E7P4 shadow quotient identified it. -/
theorem nativeF55_sourceAwareReadout_separates_raw :
    sourceAwareReadout northNativeF55Observe
        northNativeF55PentagonCell ≠
      sourceAwareReadout northNativeF55Observe
        northNativeF55PentagonWithUnit := by
  intro h
  exact northNativeF55_raw_distinct
    (congrArg (fun p : NorthNativeF55Shadow × NorthNativeF55Raw => p.2) h)

/-- The refined atlas cannot magically glue the originally conflicting
actual proof trees; their raw projection witnesses the obstruction. -/
theorem nativeF55_twoChart_refined_no_global :
    ¬ HasGlobal northNativeF55TwoChartCover
      (shadowSections northNativeF55TwoChartCover
        (sourceAwareReadout northNativeF55Observe)
        northNativeF55TwoChartRaw) := by
  intro h
  exact nativeF55_twoChart_raw_no_global
    ((sourceGlobal_iff_refinedGlobal northNativeF55TwoChartCover
      northNativeF55Observe northNativeF55TwoChartRaw).2 h)

/-- The alternative constant-source atlas (different raw source!) has
a global refined readout, consistent with full source retention. -/
theorem nativeF55_constant_twoChart_refined_global :
    HasGlobal northNativeF55TwoChartCover
      (shadowSections northNativeF55TwoChartCover
        (sourceAwareReadout northNativeF55Observe)
        northNativeF55TwoChartConstantRaw) :=
  (sourceGlobal_iff_refinedGlobal northNativeF55TwoChartCover
    northNativeF55Observe northNativeF55TwoChartConstantRaw).1
    nativeF55_twoChart_constant_raw_global

/-- A faithful source-aware observer CANNOT factor through the original
chosen shadow quotient on all actual native F55 raw proof-tree values. -/
theorem nativeF55_sourceAwareReadout_no_shadow_factor :
    ¬ Factors northNativeF55Observe
      (sourceAwareReadout northNativeF55Observe) :=
  nativeF55_no_faithful_observer_via_shadow
    (sourceAwareReadout northNativeF55Observe)
    (sourceAwareReadout_injective northNativeF55Observe)

#print axioms sourceCompatible_implies_shadowCompatible
#print axioms sourceCompatible_implies_overlapFaithful
#print axioms shadowCompatible_and_overlapFaithful_implies_sourceCompatible
#print axioms sourceCompatible_iff_shadowCompatible_and_overlapFaithful
#print axioms sourceGlobal_implies_shadowGlobal
#print axioms sourceGlobal_implies_overlapFaithful
#print axioms shadowGlobal_and_overlapFaithful_implies_sourceGlobal
#print axioms sourceGlobal_iff_shadowGlobal_and_overlapFaithful
#print axioms no_sourceGlobal_iff_no_overlapFaithful_of_shadowGlobal
#print axioms admittedShadow_and_overlapFaithful_implies_sourceGlobal
#print axioms no_source_promotion_of_refuted_overlapFaithfulness
#print axioms sourceAwareReadout_source_exact
#print axioms sourceAwareReadout_shadow_exact
#print axioms sourceAwareReadout_injective
#print axioms sourceCompatible_iff_refinedCompatible
#print axioms sourceGlobal_iff_refinedGlobal
#print axioms nativeF55_twoChart_not_overlapFiberFaithful
#print axioms nativeF55_constant_twoChart_overlapFiberFaithful
#print axioms nativeF55_source_vs_alternative_overlap_faithfulness
#print axioms nativeF55_sourceAwareReadout_separates_raw
#print axioms nativeF55_twoChart_refined_no_global
#print axioms nativeF55_constant_twoChart_refined_global
#print axioms nativeF55_sourceAwareReadout_no_shadow_factor

end Kuu.LivingEngi
