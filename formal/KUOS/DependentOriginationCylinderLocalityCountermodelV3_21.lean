import KUOS.DependentOriginationOverlapStarTransitivityV3_20

namespace KUOS.DependentOriginationCylinderLocalityCountermodelV3_21

open KUOS.DependentOriginationPairwiseCorrelationCountermodelV3_17
open KUOS.DependentOriginationOverlapStarTransitivityV3_20

/-!
# Cylinder locality does not close witness correlation v3.21

Canonical v3.12 proves an important locality theorem for the actual quotient
correction loci: correctness at one route state depends only on the finite
gauge-coordinate footprint of that state.  Equivalently, changing all gauge
coordinates outside the footprint preserves membership in the correction
locus.

v3.17 shows that nested pairwise-compatible local witnesses need not correlate
into one globally compatible family.  v3.20 isolates overlap-star transitivity
as one sufficient condition that would close this gap.

The present file truth-tests whether footprint locality alone can supply that
missing correlation.  The answer is negative already in the finite Boolean
parity model of v3.17.

The abstract correction predicates in that model are cylinders with respect to
their declared footprints: if two sections agree on the footprint of a state,
then either both satisfy that state's correction equation or neither does.
Nevertheless the same model has nested pairwise-compatible witnesses and no
globally compatible family, and it fails star transitivity.

Therefore the canonical v3.12 cylinder theorem is structurally important but
cannot, by itself, justify the v3.16 witness-correlation upgrade.
-/

/-- Abstract analogue of the v3.12 cylinder property: local correctness
depends only on the coordinates listed in the state's footprint. -/
def AbstractFootprintCylinderLocality : Prop :=
  ∀ s : CorrelationState,
    ∀ q q' : CorrelationCoord → Bool,
      LocalCorrected s q →
      (∀ k : CorrelationCoord, footprint s k → q k = q' k) →
        LocalCorrected s q'

/-- The v3.17 parity correction predicates really are footprint cylinders. -/
theorem abstractFootprintCylinderLocality :
    AbstractFootprintCylinderLocality := by
  intro s q q' hq hAgree
  cases s with
  | a =>
      change q .ab = q .ac at hq
      change q' .ab = q' .ac
      have hab : q .ab = q' .ab :=
        hAgree .ab (by simp [footprint])
      have hac : q .ac = q' .ac :=
        hAgree .ac (by simp [footprint])
      exact hab.symm.trans (hq.trans hac)
  | b =>
      change q .ab = q .bc at hq
      change q' .ab = q' .bc
      have hab : q .ab = q' .ab :=
        hAgree .ab (by simp [footprint])
      have hbc : q .bc = q' .bc :=
        hAgree .bc (by simp [footprint])
      exact hab.symm.trans (hq.trans hbc)
  | c =>
      change q .ac ≠ q .bc at hq
      change q' .ac ≠ q' .bc
      have hac : q .ac = q' .ac :=
        hAgree .ac (by simp [footprint])
      have hbc : q .bc = q' .bc :=
        hAgree .bc (by simp [footprint])
      intro hEq
      apply hq
      exact hac.trans (hEq.trans hbc.symm)

/-- Named abstract obstruction package: cylinder locality and nested pairwise
compatibility coexist with failure of global correlation. -/
def AbstractCylinderPairwiseCorrelationGap : Prop :=
  AbstractFootprintCylinderLocality ∧
    NestedPairwiseCompatible ∧
      ¬ GloballyCompatibleFamily

/-- Explicit witness that cylinder locality does not eliminate the correlation
obstruction. -/
theorem abstractCylinderPairwiseCorrelationGap :
    AbstractCylinderPairwiseCorrelationGap := by
  exact
    ⟨abstractFootprintCylinderLocality,
      nestedPairwiseCompatible,
      not_globallyCompatibleFamily⟩

/-- Even after adding the v3.12-style cylinder property, the parity model still
fails the v3.20 triangle-closing condition. -/
theorem cylinderLocality_with_failure_of_starTransitivity :
    AbstractFootprintCylinderLocality ∧
      NestedPairwiseCompatible ∧
      ¬ GloballyCompatibleFamily ∧
      ¬ AbstractOverlapStarTransitive := by
  exact
    ⟨abstractFootprintCylinderLocality,
      nestedPairwiseCompatible,
      not_globallyCompatibleFamily,
      not_abstractOverlapStarTransitive⟩

/-- Pure footprint-cylinder locality plus nested pairwise compatibility does not
logically imply existence of a globally compatible local family. -/
theorem not_cylinder_and_nested_imply_global :
    ¬ ((AbstractFootprintCylinderLocality ∧ NestedPairwiseCompatible) →
      GloballyCompatibleFamily) := by
  intro h
  exact not_globallyCompatibleFamily
    (h ⟨abstractFootprintCylinderLocality, nestedPairwiseCompatible⟩)

/-!
## Factorization frontier after v3.21

The logical boundary is now sharper.

The actual quotient correction loci have the v3.12 cylinder property:

  correction at state s depends only on footprint(s).

But v3.21 proves that the conjunction

  footprint-cylinder locality
  + nested pairwise-compatible local witnesses

still does not force one globally compatible family.

Thus the remaining positive route must use information stronger than finite
support/locality.  Candidate sources are now specifically higher compatibility
properties of the concrete associator and unitor equations:

1. overlap-star transitivity or a weaker triangle-filling law;
2. an overlap-preserving gauge-fixing normalizer;
3. a higher cocycle identity tying different route equations together.

The next theorem unit should therefore study concrete mixed triangles of route
states, rather than only the support of each individual equation.
-/

end KUOS.DependentOriginationCylinderLocalityCountermodelV3_21
