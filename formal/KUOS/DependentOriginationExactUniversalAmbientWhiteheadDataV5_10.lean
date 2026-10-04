import KUOS.DependentOriginationExactUniversalAmbientP4ClosureV5_09

namespace KUOS.DependentOriginationExactUniversalAmbientWhiteheadDataV5_10

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationExactUniversalAmbientCoverageReductionV4_90
open KUOS.DependentOriginationExactUniversalAmbientP4ClosureV5_09

set_option autoImplicit false

noncomputable section

/-!
# Canonical ambient Whitehead data v5.10

v5.09 closes the current ambient P4 route by proving ambient object coverage
and Whitehead existence for the exact-universal realization.  This file exposes
the resulting Whitehead datum itself as a canonical theorem-bearing object,
rather than leaving the endpoint only in existential form.

No new mathematical hypothesis is introduced.  The forward pseudofunctor is
definitionally the exact-universal realization, the local hom equivalences are
the already-proved exact-universal hom equivalences, and ambient essential
surjectivity is supplied by the v5.09 canonical object-coverage theorem.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Canonical ambient Whitehead biequivalence data for the exact-universal
realization. -/
noncomputable def exactUniversalAmbientCanonicalWhiteheadBiequivalenceData
    (A : RefinementAtlas (LocalizedContext W)) :
    WhiteheadBiequivalenceData
      (ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
      (DependentOriginationCompletion2.{u, v, uH, uH, vH}
        (W := W) A) :=
  exactUniversalAmbientWhiteheadBiequivalenceOfCoverage.{u, v, uH, vH}
    (W := W) A
    (exactUniversalAmbientObjectCoverage_canonical
      (W := W) A)

/-- The forward pseudofunctor of the canonical ambient Whitehead datum is
literally the exact-universal realization. -/
@[simp] theorem exactUniversalAmbientCanonicalWhiteheadBiequivalenceData_forward
    (A : RefinementAtlas (LocalizedContext W)) :
    (exactUniversalAmbientCanonicalWhiteheadBiequivalenceData
      (W := W) A).forward =
      (exactUniversalRealization (W := W) A).toPseudofunctor := by
  rfl

/-- The local hom equivalence carried by the canonical Whitehead datum is the
already validated exact-universal ambient hom equivalence. -/
theorem exactUniversalAmbientCanonicalWhiteheadBiequivalenceData_homEquiv
    (A : RefinementAtlas (LocalizedContext W))
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A) :
    (exactUniversalAmbientCanonicalWhiteheadBiequivalenceData
      (W := W) A).homEquiv X Y =
      exactUniversalAmbientHomEquivalence (W := W) A X Y := by
  rfl

/-- The canonical Whitehead datum supplies an explicit essentially-surjective
object witness for every ambient completion object. -/
theorem exactUniversalAmbientCanonicalWhitehead_object_essentially_surjective
    (A : RefinementAtlas (LocalizedContext W))
    (Z :
      DependentOriginationCompletion2.{u, v, uH, uH, vH}
        (W := W) A) :
    ∃ X : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A,
      Nonempty (Bicategory.Equivalence X.carrier Z) := by
  exact
    (exactUniversalAmbientCanonicalWhiteheadBiequivalenceData
      (W := W) A).object_essentially_surjective Z

/-- The v5.09 existential endpoint is witnessed by the canonical Whitehead
datum above. -/
theorem exactUniversalAmbientCanonicalWhiteheadExistence_via_data
    (A : RefinementAtlas (LocalizedContext W)) :
    ExactUniversalAmbientWhiteheadExistence.{u, v, uH, vH}
      (W := W) A := by
  exact
    ⟨exactUniversalAmbientCanonicalWhiteheadBiequivalenceData
        (W := W) A,
      exactUniversalAmbientCanonicalWhiteheadBiequivalenceData_forward
        (W := W) A⟩

/-! ## Regression checks -/

#print axioms exactUniversalAmbientCanonicalWhiteheadBiequivalenceData
#print axioms exactUniversalAmbientCanonicalWhiteheadBiequivalenceData_forward
#print axioms exactUniversalAmbientCanonicalWhiteheadBiequivalenceData_homEquiv
#print axioms exactUniversalAmbientCanonicalWhitehead_object_essentially_surjective
#print axioms exactUniversalAmbientCanonicalWhiteheadExistence_via_data

end

end KUOS.DependentOriginationExactUniversalAmbientWhiteheadDataV5_10
