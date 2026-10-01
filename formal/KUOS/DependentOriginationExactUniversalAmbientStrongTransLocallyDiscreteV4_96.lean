import KUOS.DependentOriginationExactUniversalAmbientStrongTransExtensionV4_95

namespace KUOS.DependentOriginationExactUniversalAmbientStrongTransLocallyDiscreteV4_96

open CategoryTheory
open Opposite
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationExactUniversalAmbientCoverageReductionV4_90
open KUOS.DependentOriginationExactUniversalAmbientStrongTransExtensionV4_95

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory
open scoped Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Locally-discrete StrongTrans reduction v4.96

v4.95 reduces ambient essential surjectivity to construction of a localized
StrongTrans coherence-extension package.  That package lists five pieces:

* naturality isomorphisms on localized 1-cells;
* naturality of those isomorphisms with respect to localized 2-cells;
* identity coherence;
* composition coherence;
* the exact raw-arrow restriction square.

The source bicategory here is
`LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)`.  Consequently the second item
is not independent data.  Any 2-cell identifies its source and target
1-morphisms, and after that identification the 2-cell itself is the unique
endomorphism of that object in a discrete hom-category.  Pseudofunctoriality
then reduces the StrongTrans two-cell naturality equation to identities.

This theorem unit removes that spurious obstruction from the frontier.  We
package only the remaining four one-cell/coherence fields, reconstruct the full
v4.95 package canonically, and prove equivalence of the corresponding existence
conditions, including the ambient condition feeding Whitehead existence.

No localized one-cell naturality isomorphism is constructed here.  In
particular, formal inverses, composition descent, quotient-relation invariance,
and the raw restriction square remain the genuine next obligations.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- For a locally-discrete source, the StrongTrans naturality equation with
respect to 2-cells is automatic for any chosen family of naturality
isomorphisms. -/
theorem higherLocalizedStrongTransNaturalityNaturality_of_locallyDiscrete
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    (naturality :
      ∀ {a b : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)}
        (f : a ⟶ b),
        F.map f ≫ higherLocalizedStrongTransExtensionApp (W := W) gamma b ≅
          higherLocalizedStrongTransExtensionApp (W := W) gamma a ≫ G.map f)
    {a b : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)}
    {f g : a ⟶ b} (eta : f ⟶ g) :
    F.map₂ eta ▷ higherLocalizedStrongTransExtensionApp (W := W) gamma b ≫
          (naturality g).hom =
      (naturality f).hom ≫
        higherLocalizedStrongTransExtensionApp (W := W) gamma a ◁ G.map₂ eta := by
  obtain rfl := obj_ext_of_isDiscrete eta
  have hEta : eta = 𝟙 f := Subsingleton.elim _ _
  subst eta
  simp

/-- The genuinely remaining v4.95 extension data after removing automatic
2-cell naturality of the locally-discrete source. -/
structure HigherLocalizedStrongTransOneCellCoherenceExtension
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G) where
  naturality
      {a b : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)}
      (f : a ⟶ b) :
      F.map f ≫ higherLocalizedStrongTransExtensionApp (W := W) gamma b ≅
        higherLocalizedStrongTransExtensionApp (W := W) gamma a ≫ G.map f
  naturality_id
      (a : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)) :
      (naturality (𝟙 a)).hom ≫
          higherLocalizedStrongTransExtensionApp (W := W) gamma a ◁
            (G.mapId a).hom =
        (F.mapId a).hom ▷
            higherLocalizedStrongTransExtensionApp (W := W) gamma a ≫
          (λ_ (higherLocalizedStrongTransExtensionApp (W := W) gamma a)).hom ≫
          (ρ_ (higherLocalizedStrongTransExtensionApp (W := W) gamma a)).inv
  naturality_comp
      {a b c : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)}
      (f : a ⟶ b) (g : b ⟶ c) :
      (naturality (f ≫ g)).hom ≫
          higherLocalizedStrongTransExtensionApp (W := W) gamma a ◁
            (G.mapComp f g).hom =
        (F.mapComp f g).hom ▷
            higherLocalizedStrongTransExtensionApp (W := W) gamma c ≫
          (α_ _ _ _).hom ≫
          F.map f ◁ (naturality g).hom ≫
          (α_ _ _ _).inv ≫
          (naturality f).hom ▷ G.map g ≫
          (α_ _ _ _).hom
  restrict_modification_naturality
      {X Y : LocallyDiscrete Context} (f : X ⟶ Y) :
      (restrictHigherLocalizedSystem W F).map f ◁
            𝟙
              (higherLocalizedStrongTransExtensionApp (W := W) gamma
                ((higherPresentationUnitFunctor W).toPseudofunctor.obj Y)) ≫
          (gamma.naturality f).hom =
        (naturality
            ((higherPresentationUnitFunctor W).toPseudofunctor.map f)).hom ≫
          𝟙
              (higherLocalizedStrongTransExtensionApp (W := W) gamma
                ((higherPresentationUnitFunctor W).toPseudofunctor.obj X)) ▷
            (restrictHigherLocalizedSystem W G).map f

/-- Reinsert the automatic locally-discrete 2-cell naturality field and recover
the full v4.95 coherence-extension package. -/
noncomputable def
    HigherLocalizedStrongTransOneCellCoherenceExtension.toCoherenceExtension
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    {gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G}
    (D : HigherLocalizedStrongTransOneCellCoherenceExtension (W := W) gamma) :
    HigherLocalizedStrongTransCoherenceExtension (W := W) gamma where
  naturality := D.naturality
  naturality_naturality eta :=
    higherLocalizedStrongTransNaturalityNaturality_of_locallyDiscrete
      (W := W) gamma D.naturality eta
  naturality_id := D.naturality_id
  naturality_comp := D.naturality_comp
  restrict_modification_naturality := D.restrict_modification_naturality

/-- Forget the automatic 2-cell naturality field from a full v4.95 package. -/
noncomputable def
    HigherLocalizedStrongTransOneCellCoherenceExtension.ofCoherenceExtension
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    {gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G}
    (D : HigherLocalizedStrongTransCoherenceExtension (W := W) gamma) :
    HigherLocalizedStrongTransOneCellCoherenceExtension (W := W) gamma where
  naturality := D.naturality
  naturality_id := D.naturality_id
  naturality_comp := D.naturality_comp
  restrict_modification_naturality := D.restrict_modification_naturality

/-- Existence of the reduced four-field extension package for every raw
StrongTrans between one pair of localized systems. -/
def HigherLocalizedStrongTransOneCellExtensionExists
    (F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)) : Prop :=
  ∀ gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G,
    Nonempty
      (HigherLocalizedStrongTransOneCellCoherenceExtension (W := W) gamma)

/-- The v4.95 five-field existence condition is exactly equivalent to the
four-field condition because 2-cell naturality is automatic. -/
theorem higherLocalizedStrongTransExtensionExists_iff_oneCellExtensionExists
    (F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)) :
    HigherLocalizedStrongTransExtensionExists (W := W) F G ↔
      HigherLocalizedStrongTransOneCellExtensionExists (W := W) F G := by
  constructor
  · intro h gamma
    rcases h gamma with ⟨D⟩
    exact
      ⟨HigherLocalizedStrongTransOneCellCoherenceExtension.ofCoherenceExtension
        (W := W) D⟩
  · intro h gamma
    rcases h gamma with ⟨D⟩
    exact
      ⟨HigherLocalizedStrongTransOneCellCoherenceExtension.toCoherenceExtension
        (W := W) D⟩

/-- Ambient version of the reduced four-field extension obligation. -/
def ExactUniversalAmbientRestrictionStrongTransOneCellExtension
    (A : RefinementAtlas (LocalizedContext W)) : Prop :=
  ∀
    X Y :
      DependentOriginationCompletion2.{u, v, uH, uH, vH}
        (W := W) A,
    HigherLocalizedStrongTransOneCellExtensionExists
      (W := W)
      (higherStackObjectVal (W := W) A X)
      (higherStackObjectVal (W := W) A Y)

/-- Ambient v4.95 extension existence is equivalent to the reduced v4.96
four-field condition. -/
theorem
    exactUniversalAmbientRestrictionStrongTransExtension_iff_oneCellExtension
    (A : RefinementAtlas (LocalizedContext W)) :
    ExactUniversalAmbientRestrictionStrongTransExtension.{u, v, uH, vH}
        (W := W) A ↔
      ExactUniversalAmbientRestrictionStrongTransOneCellExtension.{u, v, uH, vH}
        (W := W) A := by
  constructor
  · intro h X Y
    exact
      (higherLocalizedStrongTransExtensionExists_iff_oneCellExtensionExists
        (W := W)
        (higherStackObjectVal (W := W) A X)
        (higherStackObjectVal (W := W) A Y)).mp
        (h X Y)
  · intro h X Y
    exact
      (higherLocalizedStrongTransExtensionExists_iff_oneCellExtensionExists
        (W := W)
        (higherStackObjectVal (W := W) A X)
        (higherStackObjectVal (W := W) A Y)).mpr
        (h X Y)

/-- The reduced four-field condition is already sufficient for the v4.95
ambient Whitehead conclusion. -/
theorem exactUniversalAmbientWhiteheadExistence_of_oneCellExtension
    (A : RefinementAtlas (LocalizedContext W))
    (hExt :
      ExactUniversalAmbientRestrictionStrongTransOneCellExtension.{u, v, uH, vH}
        (W := W) A) :
    ExactUniversalAmbientWhiteheadExistence.{u, v, uH, vH}
      (W := W) A := by
  apply exactUniversalAmbientWhiteheadExistence_of_strongTransExtension
    (W := W) A
  exact
    (exactUniversalAmbientRestrictionStrongTransExtension_iff_oneCellExtension
      (W := W) A).mpr hExt

/-! ## Regression checks -/

#print axioms higherLocalizedStrongTransNaturalityNaturality_of_locallyDiscrete
#print axioms
  HigherLocalizedStrongTransOneCellCoherenceExtension.toCoherenceExtension
#print axioms higherLocalizedStrongTransExtensionExists_iff_oneCellExtensionExists
#print axioms
  exactUniversalAmbientRestrictionStrongTransExtension_iff_oneCellExtension
#print axioms exactUniversalAmbientWhiteheadExistence_of_oneCellExtension

end

end KUOS.DependentOriginationExactUniversalAmbientStrongTransLocallyDiscreteV4_96
