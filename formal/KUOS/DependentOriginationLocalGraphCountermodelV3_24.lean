import KUOS.DependentOriginationCylinderLocalityCountermodelV3_21

namespace KUOS.DependentOriginationLocalGraphCountermodelV3_24

open KUOS.DependentOriginationPairwiseCorrelationCountermodelV3_17
open KUOS.DependentOriginationCylinderLocalityCountermodelV3_21
open KUOS.DependentOriginationOverlapStarTransitivityV3_20

/-!
# Local graph rigidity still does not close correlation v3.24

v3.22 and v3.23 investigate graph-like behavior of the actual unitor and
associator correction equations.  This finite truth-test records an important
logical boundary before those local theorems are used globally.

The Boolean parity countermodel of v3.17 is not only footprint-local.  Each of
its three local correction loci is itself graph-like over one chosen coordinate:

* state a: fixing ab fixes ac;
* state b: fixing ab fixes bc;
* state c: fixing ac fixes bc.

Thus two correcting sections at the same state which agree on the chosen base
coordinate agree on the full declared footprint.

Nevertheless the model still has nested pairwise-compatible local witnesses,
no globally compatible family, and failure of overlap-star transitivity.

Therefore local functional dependence inside each correction locus is still
not enough to eliminate the global witness-correlation obstruction.  A genuine
cross-route cocycle/triangle law remains necessary.
-/

/-- One chosen base coordinate for each local parity constraint. -/
def graphBaseCoord : CorrelationState → CorrelationCoord
  | .a => .ab
  | .b => .ab
  | .c => .ac

/-- Abstract local graph rigidity: among corrected sections at one state,
agreement at the chosen base coordinate forces agreement on the whole
footprint. -/
def AbstractLocalGraphRigidity : Prop :=
  ∀ s : CorrelationState,
    ∀ q q' : CorrelationCoord → Bool,
      LocalCorrected s q →
      LocalCorrected s q' →
      q (graphBaseCoord s) = q' (graphBaseCoord s) →
      ∀ k : CorrelationCoord,
        footprint s k →
          q k = q' k

/-- The v3.17 parity model satisfies local graph rigidity at every state. -/
theorem abstractLocalGraphRigidity :
    AbstractLocalGraphRigidity := by
  intro s q q' hq hq' hbase k hk
  cases s with
  | a =>
      change q .ab = q .ac at hq
      change q' .ab = q' .ac at hq'
      change q .ab = q' .ab at hbase
      cases k with
      | ab =>
          exact hbase
      | ac =>
          exact hq.symm.trans (hbase.trans hq')
      | bc =>
          simp [footprint] at hk
  | b =>
      change q .ab = q .bc at hq
      change q' .ab = q' .bc at hq'
      change q .ab = q' .ab at hbase
      cases k with
      | ab =>
          exact hbase
      | ac =>
          simp [footprint] at hk
      | bc =>
          exact hq.symm.trans (hbase.trans hq')
  | c =>
      change q .ac ≠ q .bc at hq
      change q' .ac ≠ q' .bc at hq'
      change q .ac = q' .ac at hbase
      cases k with
      | ab =>
          simp [footprint] at hk
      | ac =>
          exact hbase
      | bc =>
          cases hca : q .ac <;>
            cases hcb : q .bc <;>
            cases hca' : q' .ac <;>
            cases hcb' : q' .bc <;>
            simp [hca, hcb, hca', hcb'] at hq hq' hbase ⊢

/-- Cylinder locality, local graph rigidity, and nested pairwise compatibility
can all coexist with failure of global correlation. -/
def AbstractCylinderGraphCorrelationGap : Prop :=
  AbstractFootprintCylinderLocality ∧
    AbstractLocalGraphRigidity ∧
      NestedPairwiseCompatible ∧
        ¬ GloballyCompatibleFamily

theorem abstractCylinderGraphCorrelationGap :
    AbstractCylinderGraphCorrelationGap := by
  exact
    ⟨abstractFootprintCylinderLocality,
      abstractLocalGraphRigidity,
      nestedPairwiseCompatible,
      not_globallyCompatibleFamily⟩

/-- Even after adding local graph rigidity to cylinder locality, the same
finite model still violates the v3.20 triangle-closing condition. -/
theorem cylinderGraphRigidity_with_failure_of_starTransitivity :
    AbstractFootprintCylinderLocality ∧
      AbstractLocalGraphRigidity ∧
      NestedPairwiseCompatible ∧
      ¬ GloballyCompatibleFamily ∧
      ¬ AbstractOverlapStarTransitive := by
  exact
    ⟨abstractFootprintCylinderLocality,
      abstractLocalGraphRigidity,
      nestedPairwiseCompatible,
      not_globallyCompatibleFamily,
      not_abstractOverlapStarTransitive⟩

/-- Pure locality plus same-state graph rigidity still does not logically imply
one globally compatible correction family. -/
theorem not_cylinder_graph_and_nested_imply_global :
    ¬ ((AbstractFootprintCylinderLocality ∧
        AbstractLocalGraphRigidity ∧
        NestedPairwiseCompatible) →
      GloballyCompatibleFamily) := by
  intro h
  exact not_globallyCompatibleFamily
    (h
      ⟨abstractFootprintCylinderLocality,
        abstractLocalGraphRigidity,
        nestedPairwiseCompatible⟩)

/-!
## Factorization frontier after v3.24

The remaining obstruction is now known not to be removed by either:

* finite footprint locality; or
* routewise functional/graph rigidity.

Those are local properties.  The missing information is genuinely relational
between different correction loci.

Accordingly, the next positive theorem must use a cross-route law: an actual
triangle/cocycle identity, overlap-star transitivity derived from the concrete
equations, or an equivalent coherence relation linking associator and unitor
constraints.
-/

end KUOS.DependentOriginationLocalGraphCountermodelV3_24
