import KUOS.DependentOriginationExactUniversalAmbientStrongTransCoherentExtensionV5_08

namespace KUOS.DependentOriginationExactUniversalAmbientP4ClosureV5_09

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationExactUniversalAmbientCoverageReductionV4_90
open KUOS.DependentOriginationExactUniversalAmbientRestrictionFaithfulSplitV4_93
open KUOS.DependentOriginationExactUniversalAmbientRestrictionFullV4_94
open KUOS.DependentOriginationExactUniversalAmbientStrongTransExtensionV4_95
open KUOS.DependentOriginationExactUniversalAmbientStrongTransCoherentExtensionV5_08

set_option autoImplicit false

noncomputable section

/-!
# Ambient P4 route closure v5.09

v5.08 constructs a coherent localized StrongTrans extension for every raw
StrongTrans between every pair of localized higher systems.  Applying that
uniform theorem to the localized values of arbitrary ambient completion objects
discharges the exact v4.95 ambient StrongTrans-extension hypothesis.

The existing v4.95 theorem then supplies restriction-hom essential
surjectivity, and the already closed v4.94/v4.92/v4.91/v4.90 chain yields the
ambient Whitehead existence conclusion.

This file only composes already validated theorem-level interfaces.  It adds no
new choice of representative, no new localization relation witness, and no new
coherence axiom.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- The v4.95 ambient StrongTrans-extension hypothesis is now unconditional:
v5.08 supplies the required coherent extension for every pair of ambient
localized higher systems. -/
theorem exactUniversalAmbientRestrictionStrongTransExtension_canonical
    (A : RefinementAtlas (LocalizedContext W)) :
    ExactUniversalAmbientRestrictionStrongTransExtension.{u, v, uH, vH}
      (W := W) A := by
  intro X Y
  exact
    higherLocalizedCanonicalStrongTransExtensionExists
      (W := W)
      (higherStackObjectVal (W := W) A X)
      (higherStackObjectVal (W := W) A Y)

/-- Consequently restriction is essentially surjective on every ambient
StrongTrans hom category. -/
theorem exactUniversalAmbientRestrictionHomEssSurj_canonical
    (A : RefinementAtlas (LocalizedContext W)) :
    ExactUniversalAmbientRestrictionHomEssSurj.{u, v, uH, vH}
      (W := W) A :=
  exactUniversalAmbientRestrictionHomEssSurj_of_strongTransExtension
    (W := W) A
    (exactUniversalAmbientRestrictionStrongTransExtension_canonical
      (W := W) A)

/-- The current sufficient ambient P4 route is closed: the exact-universal
realization admits the ambient Whitehead data of v4.90 for every refinement
atlas. -/
theorem exactUniversalAmbientWhiteheadExistence_canonical
    (A : RefinementAtlas (LocalizedContext W)) :
    ExactUniversalAmbientWhiteheadExistence.{u, v, uH, vH}
      (W := W) A :=
  exactUniversalAmbientWhiteheadExistence_of_strongTransExtension
    (W := W) A
    (exactUniversalAmbientRestrictionStrongTransExtension_canonical
      (W := W) A)

/-- Equivalently, the ambient object-coverage condition of v4.90 now follows
for the exact-universal realization. -/
theorem exactUniversalAmbientObjectCoverage_canonical
    (A : RefinementAtlas (LocalizedContext W)) :
    ExactUniversalAmbientObjectCoverage.{u, v, uH, vH}
      (W := W) A :=
  (exactUniversalAmbientWhiteheadExistence_iff_objectCoverage
    (W := W) A).mp
    (exactUniversalAmbientWhiteheadExistence_canonical
      (W := W) A)

/-! ## Regression checks -/

#print axioms exactUniversalAmbientRestrictionStrongTransExtension_canonical
#print axioms exactUniversalAmbientRestrictionHomEssSurj_canonical
#print axioms exactUniversalAmbientWhiteheadExistence_canonical
#print axioms exactUniversalAmbientObjectCoverage_canonical

end

end KUOS.DependentOriginationExactUniversalAmbientP4ClosureV5_09
