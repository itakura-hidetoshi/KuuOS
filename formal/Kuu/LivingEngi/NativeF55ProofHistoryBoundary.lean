import Kuu.LivingEngi.HistoryFeedbackRepair
import Kuu.F112.PolygonNativeF55ChargeRigidity

/-!
# LEC-09 — actual independent C60 F55 Type-valued source vs chosen shadow

This is a NEW result on the genuinely typed, nine-constructor NATIVE F55
free three-cell source over ACTUAL north C60 pentagon F54 raw routes.

Already-proven E7Q3 inputs:
* a raw pentagon three-cell and the same raw cell with a pasted unit are
  syntactically different Type-valued source histories;
* their images in the chosen E7P4 full-shadow quotient are equal.

This module derives source-recovery nonfactorization, nonfaithfulness of
all observers that descend through this quotient, and proof-gated rejection
of any claim that quotient equality establishes original source equality.

The quotient is a lawful observer for its declared charges. Failure to
recover additional source syntax is NOT a failure of the quotient.

No equivalence with the FROZEN original F55/P77/GK5CG source,
no high-dimensional global filler, no historical phase transfer and no
unlicensed declaration of true/false WORLD or actual ActOS authorization.
The independent Kuu file uses no KUOS, Gray or Qi imports.
-/

namespace Kuu.LivingEngi

open Kuu.F112.Physical

set_option autoImplicit false

universe uObs

/-- Genuine native F55 three-cell proof-tree type on actual north C60
pentagon's two authentic parallel F54 routes. No arbitrary proxy site. -/
abbrev NorthNativeF55Raw :=
  KuuNativeF45Tree.DepthRotationRoute.PresentedCell
    (.pentagon .north)
    northNativeF45PentagonLong northNativeF45PentagonShort

/-- The specific chosen E7P4 observational quotient of that raw Type. -/
abbrev NorthNativeF55Shadow :=
  NativeF55ThreeHom northNativeF45PentagonLong
    northNativeF45PentagonShort

/-- Quotient observation: source raw proof history is retained in the
domain, but its selected full-shadow value is the observable. -/
def northNativeF55Observe : NorthNativeF55Raw → NorthNativeF55Shadow :=
  fun c => nativeF55ThreeOf c

/-- The source terms differ IN THE ORIGINAL NATIVE FREE PROOF TYPE. -/
theorem northNativeF55_raw_distinct :
    northNativeF55PentagonCell ≠
      northNativeF55PentagonWithUnit :=
  northNativeF55PentagonWithUnit_raw_ne

/-- The same two raw Type values have equal genuine chosen quotient
images. The old E7Q3 proof is reused with no extra quotient axioms. -/
theorem northNativeF55_observed_equal :
    northNativeF55Observe northNativeF55PentagonCell =
      northNativeF55Observe northNativeF55PentagonWithUnit :=
  northNativeF55Pentagon_quotient_eq_withUnit

/-- Exact formal source-vs-observed dichotomy: equality below
does not establish equality upstairs. -/
theorem nativeF55_same_observation_distinct_raw :
    (northNativeF55Observe northNativeF55PentagonCell =
      northNativeF55Observe northNativeF55PentagonWithUnit) ∧
    (northNativeF55PentagonCell ≠
      northNativeF55PentagonWithUnit) :=
  ⟨northNativeF55_observed_equal, northNativeF55_raw_distinct⟩

/-- An actual quotient collision proves noninjectivity of the
SPECIFIED raw-to-shadow map. No theorem about arbitrary observations. -/
theorem nativeF55_raw_observer_not_injective :
    ¬ Function.Injective northNativeF55Observe := by
  intro hInjective
  exact northNativeF55_raw_distinct
    (hInjective northNativeF55_observed_equal)

/-- LEC-02 on the actual nine-constructor F55 source: no function
from its chosen quotient can reconstruct EVERY original raw proof-tree
as an exact left inverse to this observation map. -/
theorem nativeF55_no_total_raw_reconstruction :
    ¬ Factors northNativeF55Observe
      (fun c : NorthNativeF55Raw => c) :=
  no_factor_of_collision
    northNativeF55Observe (fun c : NorthNativeF55Raw => c)
    northNativeF55PentagonCell northNativeF55PentagonWithUnit
    northNativeF55_observed_equal northNativeF55_raw_distinct

/-- A source-recovery function with the indicated section law is
impossible. The law concerns ALL original source values, not merely a
chosen representative of each quotient class. -/
theorem nativeF55_no_shadow_left_inverse :
    ¬ ∃ recover : NorthNativeF55Shadow → NorthNativeF55Raw,
        ∀ raw : NorthNativeF55Raw,
          recover (northNativeF55Observe raw) = raw :=
  nativeF55_no_total_raw_reconstruction

/-- Every observer that ONLY reads this quotient necessarily
identifies the two actually different raw histories. -/
theorem nativeF55_downstream_observer_collapses_source
    {Obs : Type uObs} (read : NorthNativeF55Shadow → Obs) :
    read (northNativeF55Observe northNativeF55PentagonCell) =
      read (northNativeF55Observe northNativeF55PentagonWithUnit) :=
  congrArg read northNativeF55_observed_equal

/-- No injective observation of the genuine raw proof language can
factor through this selected shadow quotient. A richer source-aware
observer would have to retain more information. -/
theorem nativeF55_no_faithful_observer_via_shadow
    {Obs : Type uObs} (readRaw : NorthNativeF55Raw → Obs)
    (hFaithful : Function.Injective readRaw) :
    ¬ Factors northNativeF55Observe readRaw := by
  intro hFactor
  have hEqual : readRaw northNativeF55PentagonCell =
      readRaw northNativeF55PentagonWithUnit :=
    factors_constant_on_fibers northNativeF55Observe readRaw
      hFactor _ _ northNativeF55_observed_equal
  exact northNativeF55_raw_distinct (hFaithful hEqual)

/-- An arbitrary explicitly declared raw-data observer with equal
outputs on the two witnesses is not injective. No information from
the current history is silently reconstructed from this equality. -/
theorem nativeF55_identifying_observer_not_injective
    {Obs : Type uObs} (readRaw : NorthNativeF55Raw → Obs)
    (hEqual : readRaw northNativeF55PentagonCell =
      readRaw northNativeF55PentagonWithUnit) :
    ¬ Function.Injective readRaw := by
  intro hFaithful
  exact northNativeF55_raw_distinct (hFaithful hEqual)

/-- LEC-04 proof gate: the ACTUAL source equality cannot be certified,
even though the chosen quotient images are equal. Missing evidence alone
would be a different, unchecked state; here we have a genuine raw
counterexample, so the proposition is refuted. -/
theorem nativeF55_source_equality_not_admissible
    (ev : PromotionEvidence
      (northNativeF55PentagonCell = northNativeF55PentagonWithUnit)) :
    ¬ Admissible ev := by
  intro hAccept
  exact northNativeF55_raw_distinct (admitted_sound ev hAccept)

/-- Quotient equality AND the independent mathematical obstruction
to illicitly promoting the original Type-valued equality both hold. -/
theorem nativeF55_quotient_equal_but_source_promotion_blocked :
    (northNativeF55Observe northNativeF55PentagonCell =
      northNativeF55Observe northNativeF55PentagonWithUnit) ∧
    (∀ ev : PromotionEvidence
        (northNativeF55PentagonCell = northNativeF55PentagonWithUnit),
      ¬ Admissible ev) :=
  ⟨northNativeF55_observed_equal,
    nativeF55_source_equality_not_admissible⟩

/-- Proof-carrying source+observation packet: the original raw witness is
DATA, not reconstructed from a chosen quotient value. This is a
reusable LEC-09 certificate shape for future source-history comparisons. -/
structure NativeF55Trace where
  raw : NorthNativeF55Raw
  observation : NorthNativeF55Shadow
  sourceEq : observation = northNativeF55Observe raw

/-- Construct a packet directly from its actual raw source history. -/
def nativeF55Trace (raw : NorthNativeF55Raw) : NativeF55Trace where
  raw := raw
  observation := northNativeF55Observe raw
  sourceEq := rfl

/-- Reading a trace preserves its actual selected quotient value. -/
def nativeF55TraceReadout (trace : NativeF55Trace) :
    NorthNativeF55Shadow := trace.observation

theorem nativeF55TraceReadout_eq_observe
    (raw : NorthNativeF55Raw) :
    nativeF55TraceReadout (nativeF55Trace raw) =
      northNativeF55Observe raw := rfl

/-- Even after the quotient observation is stored alongside the original
proof, distinct raw history packets may share its readout. -/
theorem nativeF55Trace_witnesses_distinct :
    nativeF55Trace northNativeF55PentagonCell ≠
      nativeF55Trace northNativeF55PentagonWithUnit := by
  intro h
  exact northNativeF55_raw_distinct
    (congrArg NativeF55Trace.raw h)

/-- The two distinct proof-carrying trace packets have equal
readout despite keeping their raw data as separate typed fields. -/
theorem nativeF55Trace_readout_collision :
    nativeF55TraceReadout
        (nativeF55Trace northNativeF55PentagonCell) =
      nativeF55TraceReadout
        (nativeF55Trace northNativeF55PentagonWithUnit) :=
  northNativeF55_observed_equal

/-- The readout projection on proof-carrying traces is itself
noninjective: adding source provenance is useful precisely because
the projected observational value does not determine that provenance. -/
theorem nativeF55TraceReadout_not_injective :
    ¬ Function.Injective nativeF55TraceReadout := by
  intro hInjective
  exact nativeF55Trace_witnesses_distinct
    (hInjective nativeF55Trace_readout_collision)

#print axioms nativeF55_same_observation_distinct_raw
#print axioms nativeF55_raw_observer_not_injective
#print axioms nativeF55_no_total_raw_reconstruction
#print axioms nativeF55_no_shadow_left_inverse
#print axioms nativeF55_downstream_observer_collapses_source
#print axioms nativeF55_no_faithful_observer_via_shadow
#print axioms nativeF55_identifying_observer_not_injective
#print axioms nativeF55_source_equality_not_admissible
#print axioms nativeF55_quotient_equal_but_source_promotion_blocked
#print axioms nativeF55TraceReadout_eq_observe
#print axioms nativeF55Trace_witnesses_distinct
#print axioms nativeF55Trace_readout_collision
#print axioms nativeF55TraceReadout_not_injective

end Kuu.LivingEngi
