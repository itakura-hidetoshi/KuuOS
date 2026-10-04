import KUOS.DependentOriginationExactUniversalAmbientWhiteheadDataV5_10
import KUOS.DependentOriginationExactUniversalAmbientRestrictionUniversalityV4_91
import KUOS.DependentOriginationExactUniversalAmbientRestrictionHomEquivalenceV4_92
import KUOS.DependentOriginationExactUniversalAmbientRestrictionFullV4_94

namespace KUOS.DependentOriginationExactUniversalAmbientCanonicalSourceV5_11

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationExactHigherPresentationSectorV4_50
open KUOS.DependentOriginationExactPresentationEssentialUniquenessV4_53
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalHomEquivalenceV4_83
open KUOS.DependentOriginationExactUniversalAmbientCoverageReductionV4_90
open KUOS.DependentOriginationExactUniversalAmbientRestrictionUniversalityV4_91
open KUOS.DependentOriginationExactUniversalAmbientRestrictionHomEquivalenceV4_92
open KUOS.DependentOriginationExactUniversalAmbientRestrictionFaithfulSplitV4_93
open KUOS.DependentOriginationExactUniversalAmbientRestrictionFullV4_94
open KUOS.DependentOriginationExactUniversalAmbientP4ClosureV5_09
open KUOS.DependentOriginationExactUniversalAmbientWhiteheadDataV5_10

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory
open scoped Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Canonical ambient source section v5.11

v5.09 proves the StrongTrans-extension route and hence ambient restriction-hom
essential surjectivity.  v4.94 identifies that condition with local
restriction-hom equivalence, and v4.92 turns local hom equivalence into
restriction universality.

The important consequence is stronger than mere Whitehead object coverage:
for every ambient DO₂ object `Z`, its tautological restriction presentation
has carrier definitionally equal to `Z`.  Choosing its now-proved universal
target witness therefore gives an exact-universal source object whose carrier
is literally `Z`, not merely equivalent to it.

This supplies the object map and local hom-section functors needed for an
ambient quasi-inverse pseudofunctor.  It does not yet assemble their
pseudofunctor identity/composition coherence.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

abbrev Source :=
  ExactUniversalRawObject.{u, v, uH, vH} (W := W) A

abbrev Ambient :=
  DependentOriginationCompletion2.{u, v, uH, uH, vH} (W := W) A

/-- v5.09's canonical StrongTrans extension closes the v4.94 local
restriction-hom equivalence condition. -/
theorem exactUniversalAmbientRestrictionHomEquivalence_canonical :
    ExactUniversalAmbientRestrictionHomEquivalence.{u, v, uH, vH}
      (W := W) A := by
  exact
    (exactUniversalAmbientRestrictionHomEquivalence_iff_essSurj
      (W := W) A).2
      (exactUniversalAmbientRestrictionHomEssSurj_canonical
        (W := W) A)

/-- Consequently every ambient object's tautological restriction presentation
is a coherent universal target. -/
theorem exactUniversalAmbientRestrictionUniversality_canonical :
    ExactUniversalAmbientRestrictionUniversality.{u, v, uH, vH}
      (W := W) A :=
  exactUniversalAmbientRestrictionUniversality_of_homEquivalence
    (W := W) A
    (exactUniversalAmbientRestrictionHomEquivalence_canonical
      (W := W) A)

/-- Canonically choose the universal-target witness for the tautological
restriction presentation of one ambient object.  The only choice is the proof
of universality; the carrier itself remains definitionally the prescribed
ambient object. -/
noncomputable def exactUniversalAmbientCanonicalRestrictionUniversalTarget
    (Z : Ambient (W := W) A) :
    ExactPresentationCoherentUniversalTarget
      (W := W) A
      (exactUniversalAmbientRestrictionPresentation
        (W := W) A Z) :=
  Classical.choice
    (exactUniversalAmbientRestrictionUniversality_canonical
      (W := W) A Z)

/-- Canonical exact-universal source label attached to an ambient DO₂ object. -/
noncomputable def exactUniversalAmbientCanonicalSource
    (Z : Ambient (W := W) A) :
    Source (W := W) A :=
  exactUniversalAmbientSourceOfRestrictionUniversalTarget
    (W := W) A Z
    (exactUniversalAmbientCanonicalRestrictionUniversalTarget
      (W := W) A Z)

/-- The selected source object realizes to the prescribed ambient object
definitionally. -/
@[simp] theorem exactUniversalAmbientCanonicalSource_carrier
    (Z : Ambient (W := W) A) :
    (exactUniversalAmbientCanonicalSource (W := W) A Z).carrier = Z :=
  rfl

/-- The strict exact-universal realization sends the selected source label
back to the original ambient object. -/
@[simp] theorem exactUniversalAmbientCanonicalSource_realization_obj
    (Z : Ambient (W := W) A) :
    (exactUniversalRealization (W := W) A).obj
        (exactUniversalAmbientCanonicalSource (W := W) A Z) = Z :=
  rfl

/-- Local inverse functor on one ambient hom category, using the v4.83 exact
hom section for the canonical source labels. -/
noncomputable def exactUniversalAmbientCanonicalHomSection
    (Z T : Ambient (W := W) A) :
    (Z ⟶ T) ⥤
      (exactUniversalAmbientCanonicalSource (W := W) A Z ⟶
        exactUniversalAmbientCanonicalSource (W := W) A T) :=
  exactUniversalHomSection
    (W := W) A
    (exactUniversalAmbientCanonicalSource (W := W) A Z)
    (exactUniversalAmbientCanonicalSource (W := W) A T)

/-- The local hom section preserves the chosen ambient one-cell exactly under
the realization projection. -/
@[simp] theorem exactUniversalAmbientCanonicalHomSection_obj_lift
    {Z T : Ambient (W := W) A}
    (f : Z ⟶ T) :
    ((exactUniversalAmbientCanonicalHomSection
      (W := W) A Z T).obj f).lift = f := by
  exact
    exactUniversalHomSection_obj_lift_exact
      (W := W) A
      (exactUniversalAmbientCanonicalSource (W := W) A Z)
      (exactUniversalAmbientCanonicalSource (W := W) A T)
      f

/-- Likewise the local section preserves ambient two-cells exactly under the
realization projection. -/
@[simp] theorem exactUniversalAmbientCanonicalHomSection_map_lift
    {Z T : Ambient (W := W) A}
    {f g : Z ⟶ T}
    (eta : f ⟶ g) :
    ((exactUniversalAmbientCanonicalHomSection
      (W := W) A Z T).map eta).lift = eta := by
  rfl

/-! ## Regression checks -/

#print axioms exactUniversalAmbientRestrictionHomEquivalence_canonical
#print axioms exactUniversalAmbientRestrictionUniversality_canonical
#print axioms exactUniversalAmbientCanonicalRestrictionUniversalTarget
#print axioms exactUniversalAmbientCanonicalSource
#print axioms exactUniversalAmbientCanonicalSource_carrier
#print axioms exactUniversalAmbientCanonicalSource_realization_obj
#print axioms exactUniversalAmbientCanonicalHomSection
#print axioms exactUniversalAmbientCanonicalHomSection_obj_lift
#print axioms exactUniversalAmbientCanonicalHomSection_map_lift

end

end KUOS.DependentOriginationExactUniversalAmbientCanonicalSourceV5_11
