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
  Iso.refl _

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

/-- The canonical evaluator on the identity free path is exactly the
v5.01 canonical identity naturality.  Unlike the ordinary presentation edge
corresponding to an identity morphism, the identity in `LocalizationPaths W`
is literally the empty path, so no presentation `mapId` transport is needed. -/
theorem higherLocalizedStrongTransPathNaturality_id
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    (X : LocalizationPaths W) :
    higherLocalizedStrongTransPathNaturality
        (W := W) gamma (𝟙 X) =
      higherLocalizedStrongTransNaturality_id
        (W := W) gamma (higherLocalizedPathObject W X) := by
  change
    higherLocalizedStrongTransPathNaturality
        (W := W) gamma (Quiver.Path.nil : X ⟶ X) =
      higherLocalizedStrongTransNaturality_id
        (W := W) gamma (higherLocalizedPathObject W X)
  rfl

/-- Left-unit normalization in the only form needed by the path recursion:
the right factor is a single localization-quiver edge.  For a singleton path,
`nil.comp e.toPath` reduces definitionally, avoiding the dependent transport
that appears for an arbitrary right-hand path. -/
theorem higherLocalizedStrongTransPathNaturality_comp_id_left_edge
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X : LocalizationPaths W}
    {a b : Localization.Construction.LocQuiver W}
    (e : a ⟶ b)
    (hX : X = (Paths.of (Localization.Construction.LocQuiver W)).obj a) :
    higherLocalizedStrongTransNaturality_comp
        (W := W) gamma
        (higherLocalizedPathArrow W (𝟙 X))
        (higherLocalizedPathArrow W
          ((Paths.of (Localization.Construction.LocQuiver W)).map e))
        (higherLocalizedStrongTransPathNaturality (W := W) gamma (𝟙 X))
        (higherLocalizedStrongTransPathNaturality
          (W := W) gamma
          ((Paths.of (Localization.Construction.LocQuiver W)).map e)) =
      higherLocalizedStrongTransNaturalityTransport
        (W := W) gamma
        (higherLocalizedPathArrowCompIso W (𝟙 X)
          ((Paths.of (Localization.Construction.LocQuiver W)).map e))
        (higherLocalizedStrongTransPathNaturality
          (W := W) gamma
          ((𝟙 X) ≫
            (Paths.of (Localization.Construction.LocQuiver W)).map e)) := by
  subst X
  rw [higherLocalizedStrongTransPathNaturality_id]
  set_option backward.isDefEq.respectTransparency false in
    simpa
      [higherLocalizedPathArrow, higherLocalizedPathObject,
        higherLocalizedPathQuotientFunctor,
        Strict.leftUnitor_eqToIso,
        PrelaxFunctor.map₂_eqToHom] using
      (higherLocalizedStrongTransNaturality_comp_id_left
        (W := W) gamma
        (higherLocalizedPathArrow W
          ((Paths.of (Localization.Construction.LocQuiver W)).map e))
        (higherLocalizedStrongTransPathNaturality
          (W := W) gamma
          ((Paths.of (Localization.Construction.LocQuiver W)).map e)))

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
  rw [higherLocalizedStrongTransPathNaturality_id]
  set_option backward.isDefEq.respectTransparency false in
    simpa
      [higherLocalizedPathArrowCompIso,
        higherLocalizedPathArrow, higherLocalizedPathObject,
        higherLocalizedPathQuotientFunctor,
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

/-- Transporting back along the inverse source isomorphism cancels the
original transport. -/
theorem higherLocalizedStrongTransNaturalityTransport_symm_left
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {a b : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)}
    {f g : a ⟶ b}
    (eta : f ≅ g)
    (naturality_g :
      F.map g ≫ higherLocalizedStrongTransExtensionApp (W := W) gamma b ≅
        higherLocalizedStrongTransExtensionApp (W := W) gamma a ≫ G.map g) :
    higherLocalizedStrongTransNaturalityTransport
        (W := W) gamma eta.symm
        (higherLocalizedStrongTransNaturalityTransport
          (W := W) gamma eta naturality_g) =
      naturality_g := by
  rw [higherLocalizedStrongTransNaturalityTransport_trans]
  have hIso : eta.symm ≪≫ eta = Iso.refl g := by
    apply Iso.ext
    exact Subsingleton.elim _ _
  rw [hIso]
  exact
    higherLocalizedStrongTransNaturalityTransport_refl
      (W := W) gamma g naturality_g

/-- The opposite cancellation order for source transport. -/
theorem higherLocalizedStrongTransNaturalityTransport_symm_right
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {a b : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)}
    {f g : a ⟶ b}
    (eta : f ≅ g)
    (naturality_f :
      F.map f ≫ higherLocalizedStrongTransExtensionApp (W := W) gamma b ≅
        higherLocalizedStrongTransExtensionApp (W := W) gamma a ≫ G.map f) :
    higherLocalizedStrongTransNaturalityTransport
        (W := W) gamma eta
        (higherLocalizedStrongTransNaturalityTransport
          (W := W) gamma eta.symm naturality_f) =
      naturality_f := by
  rw [higherLocalizedStrongTransNaturalityTransport_trans]
  have hIso : eta ≪≫ eta.symm = Iso.refl f := by
    apply Iso.ext
    exact Subsingleton.elim _ _
  rw [hIso]
  exact
    higherLocalizedStrongTransNaturalityTransport_refl
      (W := W) gamma f naturality_f

/-- Appending one localization-quiver edge to a nonempty path is
exactly the v4.99 composition constructor.  After the definitional
normalization of `higherLocalizedPathArrowCompIso`, no endpoint transport is
present in this recursion equation. -/
theorem higherLocalizedStrongTransPathNaturality_comp_edge_of_nonempty
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X : LocalizationPaths W}
    {a b : Localization.Construction.LocQuiver W}
    (p : X ⟶ (Paths.of (Localization.Construction.LocQuiver W)).obj a)
    (e : a ⟶ b)
    (hp : p.length ≠ 0) :
    higherLocalizedStrongTransNaturality_comp
        (W := W) gamma
        (higherLocalizedPathArrow W p)
        (higherLocalizedPathArrow W
          ((Paths.of (Localization.Construction.LocQuiver W)).map e))
        (higherLocalizedStrongTransPathNaturality (W := W) gamma p)
        (higherLocalizedStrongTransPathNaturality
          (W := W) gamma
          ((Paths.of (Localization.Construction.LocQuiver W)).map e)) =
      higherLocalizedStrongTransPathNaturality
        (W := W) gamma
        (p ≫ (Paths.of (Localization.Construction.LocQuiver W)).map e) := by
  obtain ⟨c, p', e₀, rfl⟩ :=
    (Quiver.Path.length_ne_zero_iff_eq_cons (p := p)).1 hp
  rfl

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
#print axioms higherLocalizedStrongTransPathNaturality_id
#print axioms higherLocalizedStrongTransPathNaturality_comp_id_left_edge
#print axioms higherLocalizedStrongTransPathNaturality_comp_id_right
#print axioms higherLocalizedStrongTransNaturalityTransport_eq_of_parallel_iso
#print axioms higherLocalizedStrongTransNaturalityTransport_refl
#print axioms higherLocalizedStrongTransNaturalityTransport_trans
#print axioms higherLocalizedStrongTransNaturalityTransport_symm_left
#print axioms higherLocalizedStrongTransNaturalityTransport_symm_right
#print axioms higherLocalizedStrongTransPathNaturality_comp_edge_of_nonempty
#print axioms higherLocalizedGeneratedCompClosurePathArrowIso

end

end KUOS.DependentOriginationExactUniversalAmbientStrongTransGeneratedCompClosureV5_06
