import Kuu.LivingEngi.NativeF55ProofHistoryBoundary

/-!
# LEC-10 — actual north C60 native F55 source-aware two-chart gluing obstruction

LEC-09 proved that two distinct genuinely typed native F55 raw three-cell
histories on the physical north C60 pentagon have the SAME selected E7P4
shadow observation. LEC-10 places those actual SOURCE values into a finite,
ABSTRACT two-chart cover of a singleton base to check the descent levels.
This base is NOT a demonstrated geometric open cover of C60 itself.

The two genuine local raw values live on two charts over a common point.
Their chosen shadows glue, but their actual source proof histories do not.
This is a finite source-aware *nonreflection of gluing*, not a failure of
ordinary quotient gluing or a claim about arbitrary higher stacks.

A proof-carrying trace retains the source and observation together: its
observational readout still glues while its original trace cannot glue.
A separately defined constant-source comparison has the SAME shadow
but a DIFFERENT source; it is NOT an authorized overwrite/repair.

No identification with the frozen historical F55/P77/GK5CG original Type,
no Qi/Gray/legacy KUOS import, no new public root, and no ActOS authority.
-/

namespace Kuu.LivingEngi

open Kuu.F112.Physical

set_option autoImplicit false

universe uLEC10X uLEC10I

/-! The general forward direction is constructive: source gluing
always induces observation gluing, regardless of any injectivity. -/

/-- Any actual source-compatible local atlas stays compatible after the
SPECIFIED native F55 shadow readout. The converse need not hold. -/
theorem nativeF55Observe_preserves_compatible
    {X : Type uLEC10X} {I : Type uLEC10I}
    (U : I → Set X) (s : LocalSections U NorthNativeF55Raw)
    (h : Compatible U s) :
    Compatible U
      (fun i x => northNativeF55Observe (s i x)) := by
  intro i j x hi hj
  exact congrArg northNativeF55Observe (h i j x hi hj)

/-- Any actual global ORIGINAL source defines a global chosen observation.
The reverse is NOT silently asserted. -/
theorem nativeF55Observe_preserves_global
    {X : Type uLEC10X} {I : Type uLEC10I}
    (U : I → Set X) (s : LocalSections U NorthNativeF55Raw)
    (h : HasGlobal U s) :
    HasGlobal U (fun i x => northNativeF55Observe (s i x)) := by
  rcases h with ⟨g, hg⟩
  refine ⟨fun x => northNativeF55Observe (g x), ?_⟩
  intro i x
  exact congrArg northNativeF55Observe (hg i x)

/-- Two abstract overlapping formal charts on a singleton base; only
the local values (not the chart base) come from genuine north C60 F55
source histories. No geometric C60 cover is claimed. -/
def northNativeF55TwoChartCover : Bool → Set Unit :=
  fun _ => Set.univ

/-- Chart true carries the primitive native pentagon 3-cell; chart false
carries the same cell followed by a typed right unit. -/
def northNativeF55TwoChartRaw :
    LocalSections northNativeF55TwoChartCover NorthNativeF55Raw :=
  fun chart _ =>
    if chart then northNativeF55PentagonCell
    else northNativeF55PentagonWithUnit

/-- Observations are computed FROM the retained typed local raw sources. -/
def northNativeF55TwoChartShadow :
    LocalSections northNativeF55TwoChartCover NorthNativeF55Shadow :=
  fun chart x => northNativeF55Observe (northNativeF55TwoChartRaw chart x)

/-- Both local supports really contain the singleton base point. -/
theorem nativeF55_twoChart_cover :
    Covers northNativeF55TwoChartCover := by
  intro x
  exact ⟨true, Set.mem_univ x⟩

/-- The exact source discrepancy at the common overlap is certified by
the independent E7Q3 native C60 raw-term inequality, not inferred from
a quotient statistic. -/
theorem nativeF55_twoChart_raw_overlap_disagrees :
    northNativeF55TwoChartRaw true ⟨(), Set.mem_univ ()⟩ ≠
      northNativeF55TwoChartRaw false ⟨(), Set.mem_univ ()⟩ := by
  simpa [northNativeF55TwoChartRaw] using northNativeF55_raw_distinct

/-- A concrete failure of original Type-valued overlap compatibility. -/
theorem nativeF55_twoChart_raw_incompatible :
    ¬ Compatible northNativeF55TwoChartCover
        northNativeF55TwoChartRaw := by
  intro h
  exact nativeF55_twoChart_raw_overlap_disagrees
    (h true false () (Set.mem_univ ()) (Set.mem_univ ()))

/-- Every overlap agrees AFTER the specified E7P4 shadow observation,
including the collision of the actual two distinct native proof trees. -/
theorem nativeF55_twoChart_shadow_compatible :
    Compatible northNativeF55TwoChartCover
      northNativeF55TwoChartShadow := by
  intro i j x hi hj
  cases i <;> cases j <;>
    simp [northNativeF55TwoChartShadow, northNativeF55TwoChartRaw,
      northNativeF55_observed_equal]

/-- An actual global conventional/shadow readout exists on this cover.
It glues exactly the selected quotient information, not source history. -/
theorem nativeF55_twoChart_shadow_global :
    HasGlobal northNativeF55TwoChartCover
      northNativeF55TwoChartShadow :=
  (compatible_iff_hasGlobal
    northNativeF55TwoChartCover northNativeF55TwoChartShadow
    nativeF55_twoChart_cover).1 nativeF55_twoChart_shadow_compatible

/-- A second explicit global witness, independent of the gluing choice:
both quotient values coincide with the same right-unit shadow. -/
theorem nativeF55_twoChart_explicit_shadow_global :
    ∃ g : Unit → NorthNativeF55Shadow,
      ∀ (i : Bool) (x : {y : Unit // y ∈ northNativeF55TwoChartCover i}),
        g x.1 = northNativeF55TwoChartShadow i x := by
  refine ⟨fun _ => northNativeF55Observe northNativeF55PentagonWithUnit, ?_⟩
  intro i x
  cases i <;>
    simp [northNativeF55TwoChartShadow, northNativeF55TwoChartRaw,
      northNativeF55_observed_equal]

/-- No global raw Type-valued F55 history can agree with both local
sources. This does not forbid a global chosen quotient readout. -/
theorem nativeF55_twoChart_raw_no_global :
    ¬ HasGlobal northNativeF55TwoChartCover
        northNativeF55TwoChartRaw := by
  intro hglobal
  exact nativeF55_twoChart_raw_incompatible
    (global_implies_compatible
      northNativeF55TwoChartCover northNativeF55TwoChartRaw hglobal)

/-- Certified nonreflection: ordinary gluing exists downstairs, but
EXACT source-preserving gluing of the selected original local atlas fails. -/
theorem nativeF55_twoChart_shadow_glues_not_raw :
    HasGlobal northNativeF55TwoChartCover
        northNativeF55TwoChartShadow ∧
      ¬ HasGlobal northNativeF55TwoChartCover
        northNativeF55TwoChartRaw :=
  ⟨nativeF55_twoChart_shadow_global, nativeF55_twoChart_raw_no_global⟩

/-- The example exists inside the ACTUAL native F55 source type, without
postulating any arbitrary collision or new quotient axiom. -/
theorem nativeF55_twoChart_finite_nonreflection :
    ∃ s : LocalSections northNativeF55TwoChartCover NorthNativeF55Raw,
      HasGlobal northNativeF55TwoChartCover
        (fun i x => northNativeF55Observe (s i x)) ∧
      ¬ HasGlobal northNativeF55TwoChartCover s := by
  exact ⟨northNativeF55TwoChartRaw,
    nativeF55_twoChart_shadow_global, nativeF55_twoChart_raw_no_global⟩

/-- An LEC-04 certificate for the lawful chosen shadow gluing. This
mathematical admission is neither a WORLD truth declaration nor ActOS. -/
def nativeF55TwoChartShadowCertificate :
    PromotionEvidence
      (HasGlobal northNativeF55TwoChartCover
        northNativeF55TwoChartShadow) :=
  PromotionEvidence.certified nativeF55_twoChart_shadow_global

theorem nativeF55_twoChart_shadow_certificate_admitted :
    Admissible nativeF55TwoChartShadowCertificate :=
  certified_admitted nativeF55_twoChart_shadow_global

/-- No proposed evidence state may certify a FALSE global original-source
claim for the actual two-chart raw atlas. Unchecked is not a refutation:
the independent raw discrepancy supplies the negative proof here. -/
theorem nativeF55_twoChart_raw_global_not_admissible
    (ev : PromotionEvidence
      (HasGlobal northNativeF55TwoChartCover northNativeF55TwoChartRaw)) :
    ¬ Admissible ev := by
  intro hadmit
  exact nativeF55_twoChart_raw_no_global (admitted_sound ev hadmit)

/-- Two distinct kinds of mathematical admission remain separate. -/
theorem nativeF55_twoChart_promotion_levels_separate :
    Admissible nativeF55TwoChartShadowCertificate ∧
      (∀ ev : PromotionEvidence
        (HasGlobal northNativeF55TwoChartCover northNativeF55TwoChartRaw),
        ¬ Admissible ev) :=
  ⟨nativeF55_twoChart_shadow_certificate_admitted,
    nativeF55_twoChart_raw_global_not_admissible⟩

/-- Every original local proof is kept in a typed LEC-09 trace packet,
rather than fabricated from the chosen shadow readout. -/
def northNativeF55TwoChartTrace :
    LocalSections northNativeF55TwoChartCover NativeF55Trace :=
  fun i x => nativeF55Trace (northNativeF55TwoChartRaw i x)

/-- Projection of the proof-carrying trace agrees exactly with the
previous selected shadow atlas. -/
theorem nativeF55_twoChart_trace_readout_exact :
    (fun i x => nativeF55TraceReadout
      (northNativeF55TwoChartTrace i x)) =
      northNativeF55TwoChartShadow := rfl

/-- Any global trace, if it existed, would project to a global genuine
source raw proof tree, because the trace stores that tree as data. -/
theorem nativeF55_twoChart_trace_global_implies_raw_global
    (h : HasGlobal northNativeF55TwoChartCover
      northNativeF55TwoChartTrace) :
    HasGlobal northNativeF55TwoChartCover
      northNativeF55TwoChartRaw := by
  rcases h with ⟨g, hg⟩
  refine ⟨fun x => (g x).raw, ?_⟩
  intro i x
  exact congrArg NativeF55Trace.raw (hg i x)

/-- Retaining provenance in proof-carrying traces does not
magically make the actually distinct traces source-gluable. -/
theorem nativeF55_twoChart_trace_no_global :
    ¬ HasGlobal northNativeF55TwoChartCover
      northNativeF55TwoChartTrace := by
  intro h
  exact nativeF55_twoChart_raw_no_global
    (nativeF55_twoChart_trace_global_implies_raw_global h)

/-- There exists an alternative constant source atlas that REALLY glues.
It is not the original source atlas and cannot be called its exact repair. -/
def northNativeF55TwoChartConstantRaw :
    LocalSections northNativeF55TwoChartCover NorthNativeF55Raw :=
  fun _ _ => northNativeF55PentagonCell

def northNativeF55TwoChartConstantShadow :
    LocalSections northNativeF55TwoChartCover NorthNativeF55Shadow :=
  fun i x => northNativeF55Observe (northNativeF55TwoChartConstantRaw i x)

theorem nativeF55_twoChart_constant_raw_global :
    HasGlobal northNativeF55TwoChartCover
      northNativeF55TwoChartConstantRaw := by
  refine ⟨fun _ => northNativeF55PentagonCell, ?_⟩
  intro i x
  rfl

/-- BOTH atlases have the same global conventional observations. -/
theorem nativeF55_twoChart_constant_shadow_equal :
    northNativeF55TwoChartConstantShadow =
      northNativeF55TwoChartShadow := by
  funext i x
  cases i <;>
    simp [northNativeF55TwoChartConstantShadow,
      northNativeF55TwoChartConstantRaw, northNativeF55TwoChartShadow,
      northNativeF55TwoChartRaw, northNativeF55_observed_equal]

/-- The alternative changed one ORIGINAL proof-relevant local value.
Shadow invariance cannot be used as permission to overwrite history. -/
theorem nativeF55_twoChart_constant_raw_changed :
    northNativeF55TwoChartConstantRaw false ⟨(), Set.mem_univ ()⟩ ≠
      northNativeF55TwoChartRaw false ⟨(), Set.mem_univ ()⟩ := by
  simpa [northNativeF55TwoChartConstantRaw, northNativeF55TwoChartRaw]
    using northNativeF55_raw_distinct

/-- A purported globally gluable exact replacement agreeing with ALL
original local sources is impossible. A different source is a new atlas. -/
theorem nativeF55_twoChart_no_exact_source_preserving_replacement :
    ¬ ∃ alt : LocalSections northNativeF55TwoChartCover NorthNativeF55Raw,
      HasGlobal northNativeF55TwoChartCover alt ∧
        (∀ i x, alt i x = northNativeF55TwoChartRaw i x) := by
  rintro ⟨alt, hglobal, hsource⟩
  have heq : alt = northNativeF55TwoChartRaw := by
    funext i x
    exact hsource i x
  rw [heq] at hglobal
  exact nativeF55_twoChart_raw_no_global hglobal

#print axioms nativeF55Observe_preserves_compatible
#print axioms nativeF55Observe_preserves_global
#print axioms nativeF55_twoChart_cover
#print axioms nativeF55_twoChart_raw_overlap_disagrees
#print axioms nativeF55_twoChart_raw_incompatible
#print axioms nativeF55_twoChart_shadow_compatible
#print axioms nativeF55_twoChart_shadow_global
#print axioms nativeF55_twoChart_explicit_shadow_global
#print axioms nativeF55_twoChart_raw_no_global
#print axioms nativeF55_twoChart_shadow_glues_not_raw
#print axioms nativeF55_twoChart_finite_nonreflection
#print axioms nativeF55_twoChart_shadow_certificate_admitted
#print axioms nativeF55_twoChart_raw_global_not_admissible
#print axioms nativeF55_twoChart_promotion_levels_separate
#print axioms nativeF55_twoChart_trace_readout_exact
#print axioms nativeF55_twoChart_trace_global_implies_raw_global
#print axioms nativeF55_twoChart_trace_no_global
#print axioms nativeF55_twoChart_constant_raw_global
#print axioms nativeF55_twoChart_constant_shadow_equal
#print axioms nativeF55_twoChart_constant_raw_changed
#print axioms nativeF55_twoChart_no_exact_source_preserving_replacement

end Kuu.LivingEngi
