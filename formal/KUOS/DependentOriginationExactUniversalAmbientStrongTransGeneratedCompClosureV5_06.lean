import KUOS.DependentOriginationExactUniversalAmbientStrongTransCompositionCoherenceV5_06

namespace KUOS.DependentOriginationExactUniversalAmbientStrongTransGeneratedCompClosureV5_06

open CategoryTheory
open CategoryTheory.Bicategory
open CategoryTheory.Functor
open Opposite
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68
open KUOS.DependentOriginationExactUniversalAmbientStrongTransExtensionV4_95
open KUOS.DependentOriginationExactUniversalAmbientStrongTransCompositionNaturalityV4_99
open KUOS.DependentOriginationExactUniversalAmbientStrongTransIdentityNaturalityV5_01
open KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationTransportV5_03
open KUOS.DependentOriginationExactUniversalAmbientStrongTransGeneratedRelationV5_06
open KUOS.DependentOriginationExactUniversalAmbientStrongTransGeneratorInvarianceV5_06
open KUOS.DependentOriginationExactUniversalAmbientStrongTransWhiskerCompatibilityV5_06
open KUOS.DependentOriginationExactUniversalAmbientStrongTransCompositionCoherenceV5_06

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory
open scoped Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Generated composition-closure invariance v5.06

This file begins the structural extension from the four retained localization
generators to `GeneratedCompClosure2Cell`.

The source bicategory is locally discrete.  Consequently, once the endpoints
of a source-arrow comparison are fixed, the comparison 2-isomorphism is unique.
We exploit that thinness explicitly: generator invariance may be used with any
comparison isomorphism having the same endpoints, while path-composition
comparisons are retained as concrete equality-induced isomorphisms.

The remaining step in this file is to combine these comparisons with the v5.06
unit/associativity and whisker-transport theorems to perform structural
induction on `GeneratedCompClosure2Cell`.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Canonical comparison from the composite of the two localized source arrows
to the localized source arrow of the concatenated free path. -/
noncomputable def higherLocalizedPathArrowCompIso
    {X Y Z : LocalizationPaths W}
    (p : X ⟶ Y) (q : Y ⟶ Z) :
    higherLocalizedPathArrow W p ≫ higherLocalizedPathArrow W q ≅
      higherLocalizedPathArrow W (p ≫ q) :=
  eqToIso (by
    simp
      [higherLocalizedPathArrow, higherLocalizedPathQuotientFunctor,
        Functor.map_comp, op_comp, Quiver.Hom.comp_toLoc])

/-- In a locally discrete source hom-category, parallel source-arrow
isomorphisms are equal.  Keeping this as a named lemma prevents later proofs
from depending on the presentation chosen for equality transports. -/
theorem higherLocalizedPathArrowIso_ext
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (eta theta :
      higherLocalizedPathArrow W p ≅ higherLocalizedPathArrow W q) :
    eta = theta := by
  apply Iso.ext
  exact Subsingleton.elim _ _

/-- Generator invariance is independent of the presentation of the parallel
source-arrow comparison. -/
theorem higherLocalizedStrongTransPathNaturality_generating_invariant_of_iso
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (alpha : LocalizationGenerating2Cell W p q)
    (eta :
      higherLocalizedPathArrow W p ≅ higherLocalizedPathArrow W q) :
    higherLocalizedStrongTransPathNaturality
        (W := W) gamma p =
      higherLocalizedStrongTransNaturalityTransport
        (W := W) gamma eta
        (higherLocalizedStrongTransPathNaturality
          (W := W) gamma q) := by
  have heta :
      eta = higherLocalizedGeneratingPathArrowIso (W := W) alpha :=
    higherLocalizedPathArrowIso_ext W _ _
  rw [heta]
  exact
    higherLocalizedStrongTransPathNaturality_generating_invariant
      (W := W) gamma alpha

/-- Right-unit normalization of the free-path evaluator, expressed using
the canonical path-composition comparison. -/
theorem higherLocalizedStrongTransPathNaturality_comp_id_right
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : LocalizationPaths W}
    (p : X ⟶ Y) :
    higherLocalizedStrongTransNaturality_comp
        (W := W) gamma
        (higherLocalizedPathArrow W p)
        (higherLocalizedPathArrow W (𝟙 Y))
        (higherLocalizedStrongTransPathNaturality (W := W) gamma p)
        (higherLocalizedStrongTransPathNaturality (W := W) gamma (𝟙 Y)) =
      higherLocalizedStrongTransNaturalityTransport
        (W := W) gamma
        (higherLocalizedPathArrowCompIso W p (𝟙 Y))
        (higherLocalizedStrongTransPathNaturality
          (W := W) gamma (p ≫ 𝟙 Y)) := by
  simpa
    [higherLocalizedPathArrowCompIso,
      higherLocalizedStrongTransPathNaturality,
      higherLocalizedPathArrow, higherLocalizedPathObject,
      higherLocalizedPathQuotientFunctor,
      Functor.map_comp, op_comp, Quiver.Hom.comp_toLoc,
      Strict.rightUnitor_eqToIso,
      PrelaxFunctor.map₂_eqToHom] using
    (higherLocalizedStrongTransNaturality_comp_id_right
      (W := W) gamma
      (higherLocalizedPathArrow W p)
      (higherLocalizedStrongTransPathNaturality (W := W) gamma p))

/-- Transport along parallel source 2-isomorphisms is independent of
which presentation of that 2-isomorphism is chosen.  This is the thinness
principle used below to forget equality-proof presentation details. -/
theorem higherLocalizedStrongTransNaturalityTransport_eq_of_parallel_iso
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {a b : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)}
    {f g : a ⟶ b}
    (eta theta : f ≅ g)
    (naturality_g :
      F.map g ≫ higherLocalizedStrongTransExtensionApp (W := W) gamma b ≅
        higherLocalizedStrongTransExtensionApp (W := W) gamma a ≫ G.map g) :
    higherLocalizedStrongTransNaturalityTransport
        (W := W) gamma eta naturality_g =
      higherLocalizedStrongTransNaturalityTransport
        (W := W) gamma theta naturality_g := by
  have h : eta = theta := by
    apply Iso.ext
    exact Subsingleton.elim _ _
  subst theta
  rfl

/-- The identity free path carries the canonical v5.01 identity
naturality after transport along the quotient functor's map-id comparison.

The equality proof is named locally and eliminated before simplification.  This
avoids asking `simp` to normalize a dependent `eqToHom` whose source type
still contains `Q.map (𝟙 X)`. -/
theorem higherLocalizedStrongTransPathNaturality_id_transport
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    (X : LocalizationPaths W) :
    let hId :
        higherLocalizedPathArrow W (𝟙 X) =
          𝟙 (higherLocalizedPathObject W X) := by
      change
        ((higherLocalizedPathQuotientFunctor W).map (𝟙 X)).op.op.toLoc =
          𝟙 (higherLocalizedPathObject W X)
      rw [(higherLocalizedPathQuotientFunctor W).map_id X]
      rfl
    higherLocalizedStrongTransPathNaturality
        (W := W) gamma (𝟙 X) =
      higherLocalizedStrongTransNaturalityTransport
        (W := W) gamma (eqToIso hId)
        (higherLocalizedStrongTransNaturality_id
          (W := W) gamma (higherLocalizedPathObject W X)) := by
  dsimp only
  let hId :
      higherLocalizedPathArrow W (𝟙 X) =
        𝟙 (higherLocalizedPathObject W X) := by
    change
      ((higherLocalizedPathQuotientFunctor W).map (𝟙 X)).op.op.toLoc =
        𝟙 (higherLocalizedPathObject W X)
    rw [(higherLocalizedPathQuotientFunctor W).map_id X]
    rfl
  change
    higherLocalizedStrongTransPathNaturality
        (W := W) gamma (𝟙 X) =
      higherLocalizedStrongTransNaturalityTransport
        (W := W) gamma (eqToIso hId)
        (higherLocalizedStrongTransNaturality_id
          (W := W) gamma (higherLocalizedPathObject W X))
  cases hId
  change
    higherLocalizedStrongTransPathNaturality
        (W := W) gamma (Quiver.Path.nil : X ⟶ X) =
      _
  apply Iso.ext
  simp
    [higherLocalizedStrongTransPathNaturality,
      higherLocalizedStrongTransNaturalityTransport_hom,
      PrelaxFunctor.map₂_eqToHom]

/-- Transport along the identity source 2-isomorphism is the identity
operation on StrongTrans naturality data. -/
theorem higherLocalizedStrongTransNaturalityTransport_refl
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {a b : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)}
    (f : a ⟶ b)
    (naturality_f :
      F.map f ≫ higherLocalizedStrongTransExtensionApp (W := W) gamma b ≅
        higherLocalizedStrongTransExtensionApp (W := W) gamma a ≫ G.map f) :
    higherLocalizedStrongTransNaturalityTransport
        (W := W) gamma (Iso.refl f) naturality_f =
      naturality_f := by
  apply Iso.ext
  simp [higherLocalizedStrongTransNaturalityTransport_hom]

/-- Successive source transports compose.  This is the vertical transport law
needed both for path-composition normalization and for the later
`GeneratedLocalization2Cell.trans` case. -/
theorem higherLocalizedStrongTransNaturalityTransport_trans
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {a b : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)}
    {f g h : a ⟶ b}
    (eta : f ≅ g) (theta : g ≅ h)
    (naturality_h :
      F.map h ≫ higherLocalizedStrongTransExtensionApp (W := W) gamma b ≅
        higherLocalizedStrongTransExtensionApp (W := W) gamma a ≫ G.map h) :
    higherLocalizedStrongTransNaturalityTransport
        (W := W) gamma eta
        (higherLocalizedStrongTransNaturalityTransport
          (W := W) gamma theta naturality_h) =
      higherLocalizedStrongTransNaturalityTransport
        (W := W) gamma (eta ≪≫ theta) naturality_h := by
  apply Iso.ext
  simp
    [higherLocalizedStrongTransNaturalityTransport_hom,
      Iso.trans_hom, Iso.trans_inv, PrelaxFunctor.map₂_comp]

/-- Equality-induced source-arrow comparison attached to a retained generated
composition-closure derivation.  The derivation itself supplies the quotient
equality; no choice of relation witness is introduced. -/
noncomputable def higherLocalizedGeneratedCompClosurePathArrowIso
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (alpha : GeneratedCompClosure2Cell W p q) :
    higherLocalizedPathArrow W p ≅ higherLocalizedPathArrow W q :=
  eqToIso (by
    change
      ((higherLocalizedPathQuotientFunctor W).map p).op.op.toLoc =
        ((higherLocalizedPathQuotientFunctor W).map q).op.op.toLoc
    exact
      congrArg (fun k => k.op.op.toLoc)
        (generatedLocalization2Cell_equalInLocalization W
          (GeneratedLocalization2Cell.ofCompClosure alpha)))

/-! ## Regression checks -/

#print axioms higherLocalizedPathArrowCompIso
#print axioms higherLocalizedPathArrowIso_ext
#print axioms higherLocalizedStrongTransPathNaturality_generating_invariant_of_iso
#print axioms higherLocalizedStrongTransPathNaturality_comp_id_right
#print axioms higherLocalizedStrongTransNaturalityTransport_eq_of_parallel_iso
#print axioms higherLocalizedStrongTransPathNaturality_id_transport
#print axioms higherLocalizedStrongTransNaturalityTransport_refl
#print axioms higherLocalizedStrongTransNaturalityTransport_trans
#print axioms higherLocalizedGeneratedCompClosurePathArrowIso

end

end KUOS.DependentOriginationExactUniversalAmbientStrongTransGeneratedCompClosureV5_06
