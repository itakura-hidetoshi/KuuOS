import Mathlib.CategoryTheory.Equivalence
import KUOS.DependentOriginationHigherLocalizationNecessityV2_16
import KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationNaturalityV4_97

namespace KUOS.DependentOriginationExactUniversalAmbientStrongTransWInverseNaturalityV4_98

open CategoryTheory
open CategoryTheory.Functor
open Opposite
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationHigherLocalizationNecessityV2_16
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationExactUniversalAmbientStrongTransExtensionV4_95
open KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationNaturalityV4_97

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory
open scoped Bicategory

set_option autoImplicit false

noncomputable section

/-!
# W-inverse StrongTrans naturality v4.98

v4.97 constructs the StrongTrans naturality isomorphism on every arrow in the
image of the presentation unit.  The next generator of Mathlib's constructed
localization is the formal inverse of a declared W-arrow.

At the pinned Mathlib revision there is no dedicated
`Pseudofunctor.mapAdjunction` helper.  We therefore stay on the already
validated KuuOS route:

* an isomorphism in the localized base is sent by a Cat-valued pseudofunctor to
  an equivalence of categories (v2.16);
* precomposition by that equivalence is fully faithful;
* the known naturality square on the forward isomorphism is conjugated with the
  pseudofunctor `mapComp`/`mapId` coherence;
* `Functor.preimageIso` then gives the unique naturality square on the inverse.

This is the StrongTrans analogue of the inverse-stability argument used in
v4.94 for modifications and of the fully-faithful preimage construction used
in v4.81 for pointwise inverse naturality.

This theorem unit constructs naturality on inverse generators.  It does not yet
close arbitrary path composition, quotient-relation independence, or the final
identity/composition coherence of the global StrongTrans extension.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- After left whiskering by the forward image of an isomorphism, the desired
inverse-arrow naturality square is canonically determined by the known forward
naturality square and pseudofunctor coherence. -/
noncomputable def higherLocalizedStrongTransInverseWhiskeredSquare
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : LocalizedContext W} (e : X ≅ Y)
    (hp :
      F.map e.hom.op.op.toLoc ≫
            higherLocalizedStrongTransExtensionApp (W := W) gamma
              (.mk (op (op Y))) ≅
        higherLocalizedStrongTransExtensionApp (W := W) gamma
              (.mk (op (op X))) ≫
          G.map e.hom.op.op.toLoc) :
    (F.map e.hom.op.op.toLoc).toFunctor ⋙
          ((F.map e.inv.op.op.toLoc).toFunctor ⋙
            (higherLocalizedStrongTransExtensionApp (W := W) gamma
              (.mk (op (op X)))).toFunctor) ≅
      (F.map e.hom.op.op.toLoc).toFunctor ⋙
          ((higherLocalizedStrongTransExtensionApp (W := W) gamma
              (.mk (op (op Y)))).toFunctor ⋙
            (G.map e.inv.op.op.toLoc).toFunctor) := by
  let p := e.hom.op.op.toLoc
  let q := e.inv.op.op.toLoc
  let aX :=
    higherLocalizedStrongTransExtensionApp (W := W) gamma
      (.mk (op (op X)))
  let aY :=
    higherLocalizedStrongTransExtensionApp (W := W) gamma
      (.mk (op (op Y)))
  let hpNat :
      (F.map p).toFunctor ⋙ aY.toFunctor ≅
        aX.toFunctor ⋙ (G.map p).toFunctor := by
    simpa only [p, aX, aY] using Cat.Hom.toNatIso hp
  let unitF :
      𝟭 (F.obj (.mk (op (op X)))) ≅
        (F.map p).toFunctor ⋙ (F.map q).toFunctor := by
    simpa only [Cat.Hom.id_toFunctor, Cat.Hom.comp_toFunctor] using
      Cat.Hom.toNatIso
        ((F.mapId (.mk (op (op X)))).symm ≪≫
          F.mapComp' p q (𝟙 _) (by
            apply Discrete.ext
            dsimp [p, q]
            simp))
  let unitG :
      𝟭 (G.obj (.mk (op (op X)))) ≅
        (G.map p).toFunctor ⋙ (G.map q).toFunctor := by
    simpa only [Cat.Hom.id_toFunctor, Cat.Hom.comp_toFunctor] using
      Cat.Hom.toNatIso
        ((G.mapId (.mk (op (op X)))).symm ≪≫
          G.mapComp' p q (𝟙 _) (by
            apply Discrete.ext
            dsimp [p, q]
            simp))
  exact
    (Functor.associator
        (F.map p).toFunctor (F.map q).toFunctor aX.toFunctor).symm ≪≫
      isoWhiskerRight unitF.symm aX.toFunctor ≪≫
      Functor.leftUnitor aX.toFunctor ≪≫
      ((Functor.associator
          (F.map p).toFunctor aY.toFunctor (G.map q).toFunctor).symm ≪≫
        isoWhiskerRight hpNat (G.map q).toFunctor ≪≫
        Functor.associator
          aX.toFunctor (G.map p).toFunctor (G.map q).toFunctor ≪≫
        isoWhiskerLeft aX.toFunctor unitG.symm ≪≫
        Functor.rightUnitor aX.toFunctor).symm

/-- Naturality on the inverse of any localized isomorphism is obtained by
fully-faithfully pulling back the preceding whiskered square. -/
noncomputable def higherLocalizedStrongTransNaturality_invOfIso
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : LocalizedContext W} (e : X ≅ Y)
    (hp :
      F.map e.hom.op.op.toLoc ≫
            higherLocalizedStrongTransExtensionApp (W := W) gamma
              (.mk (op (op Y))) ≅
        higherLocalizedStrongTransExtensionApp (W := W) gamma
              (.mk (op (op X))) ≫
          G.map e.hom.op.op.toLoc) :
    F.map e.inv.op.op.toLoc ≫
          higherLocalizedStrongTransExtensionApp (W := W) gamma
            (.mk (op (op X))) ≅
      higherLocalizedStrongTransExtensionApp (W := W) gamma
            (.mk (op (op Y))) ≫
        G.map e.inv.op.op.toLoc := by
  let p := e.hom.op.op.toLoc
  let q := e.inv.op.op.toLoc
  letI : (F.map p).toFunctor.IsEquivalence := by
    dsimp [p]
    exact
      pseudofunctor_map_of_isIso_isEquivalence
        F e.hom.op.op
  apply Cat.Hom.isoMk
  change
    (F.map q).toFunctor ⋙
          (higherLocalizedStrongTransExtensionApp (W := W) gamma
            (.mk (op (op X)))).toFunctor ≅
      (higherLocalizedStrongTransExtensionApp (W := W) gamma
            (.mk (op (op Y)))).toFunctor ⋙
        (G.map q).toFunctor
  exact
    ((Functor.whiskeringLeft
      (F.obj (.mk (op (op X))))
      (F.obj (.mk (op (op Y))))
      (G.obj (.mk (op (op X))))).obj
        (F.map p).toFunctor).preimageIso
      (higherLocalizedStrongTransInverseWhiskeredSquare
        (W := W) gamma e hp)

/-- The fully-faithful preimage recovers the prescribed conjugated square
exactly after whiskering by the forward equivalence. -/
theorem higherLocalizedStrongTransNaturality_invOfIso_spec
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : LocalizedContext W} (e : X ≅ Y)
    (hp :
      F.map e.hom.op.op.toLoc ≫
            higherLocalizedStrongTransExtensionApp (W := W) gamma
              (.mk (op (op Y))) ≅
        higherLocalizedStrongTransExtensionApp (W := W) gamma
              (.mk (op (op X))) ≫
          G.map e.hom.op.op.toLoc) :
    isoWhiskerLeft
        (F.map e.hom.op.op.toLoc).toFunctor
        (Cat.Hom.toNatIso
          (higherLocalizedStrongTransNaturality_invOfIso
            (W := W) gamma e hp)) =
      higherLocalizedStrongTransInverseWhiskeredSquare
        (W := W) gamma e hp := by
  let p := e.hom.op.op.toLoc
  letI : (F.map p).toFunctor.IsEquivalence := by
    dsimp [p]
    exact
      pseudofunctor_map_of_isIso_isEquivalence
        F e.hom.op.op
  apply Iso.ext
  exact
    ((Functor.whiskeringLeft
      (F.obj (.mk (op (op X))))
      (F.obj (.mk (op (op Y))))
      (G.obj (.mk (op (op X))))).obj
        (F.map p).toFunctor).map_preimage
      (higherLocalizedStrongTransInverseWhiskeredSquare
        (W := W) gamma e hp).hom

/-- Specialize the generic inverse-isomorphism construction to the formal
inverse of a declared W-arrow.  The forward square is exactly v4.97. -/
noncomputable def higherLocalizedStrongTransWInverseNaturality
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : Context} (w : X ⟶ Y) (hw : W w) :
    F.map (Localization.Construction.wInv w hw).op.op.toLoc ≫
          higherLocalizedStrongTransExtensionApp (W := W) gamma
            (.mk (op (op (W.Q.obj X)))) ≅
      higherLocalizedStrongTransExtensionApp (W := W) gamma
            (.mk (op (op (W.Q.obj Y)))) ≫
        G.map (Localization.Construction.wInv w hw).op.op.toLoc := by
  let e := Localization.Construction.wIso w hw
  apply
    higherLocalizedStrongTransNaturality_invOfIso
      (W := W) gamma e
  simpa [e, higherPresentationUnitFunctor] using
    (higherLocalizedStrongTransPresentationNaturality
      (W := W) gamma w.toLoc)

/-- Hence the second localization generator, the formal inverse of every
W-arrow, carries a canonical StrongTrans naturality isomorphism. -/
theorem exists_higherLocalizedStrongTransWInverseNaturality
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : Context} (w : X ⟶ Y) (hw : W w) :
    Nonempty
      (F.map (Localization.Construction.wInv w hw).op.op.toLoc ≫
            higherLocalizedStrongTransExtensionApp (W := W) gamma
              (.mk (op (op (W.Q.obj X)))) ≅
        higherLocalizedStrongTransExtensionApp (W := W) gamma
              (.mk (op (op (W.Q.obj Y)))) ≫
          G.map (Localization.Construction.wInv w hw).op.op.toLoc) :=
  ⟨higherLocalizedStrongTransWInverseNaturality
    (W := W) gamma w hw⟩

/-! ## Regression checks -/

#print axioms higherLocalizedStrongTransInverseWhiskeredSquare
#print axioms higherLocalizedStrongTransNaturality_invOfIso
#print axioms higherLocalizedStrongTransNaturality_invOfIso_spec
#print axioms higherLocalizedStrongTransWInverseNaturality
#print axioms exists_higherLocalizedStrongTransWInverseNaturality

end

end KUOS.DependentOriginationExactUniversalAmbientStrongTransWInverseNaturalityV4_98
