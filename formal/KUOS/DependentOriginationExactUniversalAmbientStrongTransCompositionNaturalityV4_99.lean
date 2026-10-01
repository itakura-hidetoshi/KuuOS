import KUOS.DependentOriginationExactUniversalAmbientStrongTransWInverseNaturalityV4_98

namespace KUOS.DependentOriginationExactUniversalAmbientStrongTransCompositionNaturalityV4_99

open CategoryTheory
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationExactUniversalAmbientStrongTransExtensionV4_95

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory
open scoped Bicategory

set_option autoImplicit false

noncomputable section

/-!
# StrongTrans naturality under composition v4.99

v4.97 constructs the naturality isomorphism on presentation-image arrows.
v4.98 constructs it on the formal inverses of declared W-arrows.

The next step is purely bicategorical: if naturality isomorphisms have already
been constructed on two composable one-cells, there is a canonical naturality
isomorphism on their composite.

The formula below is not invented ad hoc.  It is exactly the seven-factor
formula used by the pinned Mathlib theorem

  Pseudofunctor.StrongTrans.naturality_comp_iso

with the two existing naturality isomorphisms supplied as inputs:

  mapComp(F)
  -> associator
  -> naturality(g)
  -> associator^{-1}
  -> naturality(f)
  -> associator
  -> mapComp(G)^{-1}.

Keeping this formula as an actual definition is important for the next stage:
path recursion can use it as the constructor at every composition node, while
the accompanying hom formula gives the exact equality required by the
`naturality_comp` field of the v4.96 reduced extension package.

This theorem unit does not yet quotient paths by localization relations.
It closes only the composition constructor.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Canonical StrongTrans naturality isomorphism on a composite, assuming
naturality isomorphisms have already been supplied on the two factors. -/
noncomputable def higherLocalizedStrongTransNaturality_comp
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {a b c : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)}
    (f : a ⟶ b) (g : b ⟶ c)
    (naturality_f :
      F.map f ≫ higherLocalizedStrongTransExtensionApp (W := W) gamma b ≅
        higherLocalizedStrongTransExtensionApp (W := W) gamma a ≫ G.map f)
    (naturality_g :
      F.map g ≫ higherLocalizedStrongTransExtensionApp (W := W) gamma c ≅
        higherLocalizedStrongTransExtensionApp (W := W) gamma b ≫ G.map g) :
    F.map (f ≫ g) ≫
          higherLocalizedStrongTransExtensionApp (W := W) gamma c ≅
      higherLocalizedStrongTransExtensionApp (W := W) gamma a ≫
        G.map (f ≫ g) :=
  whiskerRightIso (F.mapComp f g)
      (higherLocalizedStrongTransExtensionApp (W := W) gamma c) ≪≫
    (α_ _ _ _) ≪≫
    whiskerLeftIso (F.map f) naturality_g ≪≫
    (α_ _ _ _).symm ≪≫
    whiskerRightIso naturality_f (G.map g) ≪≫
    (α_ _ _ _) ≪≫
    whiskerLeftIso
      (higherLocalizedStrongTransExtensionApp (W := W) gamma a)
      (G.mapComp f g).symm

/-- The hom of the composite constructor is exactly Mathlib's
`StrongTrans.naturality_comp_hom` right-hand side.  This is deliberately
exposed as a regression theorem so later assembly does not need to unfold a
long chain of composed isomorphisms. -/
theorem higherLocalizedStrongTransNaturality_comp_hom
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {a b c : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)}
    (f : a ⟶ b) (g : b ⟶ c)
    (naturality_f :
      F.map f ≫ higherLocalizedStrongTransExtensionApp (W := W) gamma b ≅
        higherLocalizedStrongTransExtensionApp (W := W) gamma a ≫ G.map f)
    (naturality_g :
      F.map g ≫ higherLocalizedStrongTransExtensionApp (W := W) gamma c ≅
        higherLocalizedStrongTransExtensionApp (W := W) gamma b ≫ G.map g) :
    (higherLocalizedStrongTransNaturality_comp
        (W := W) gamma f g naturality_f naturality_g).hom =
      (F.mapComp f g).hom ▷
            higherLocalizedStrongTransExtensionApp (W := W) gamma c ≫
        (α_ _ _ _).hom ≫
        F.map f ◁ naturality_g.hom ≫
        (α_ _ _ _).inv ≫
        naturality_f.hom ▷ G.map g ≫
        (α_ _ _ _).hom ≫
        higherLocalizedStrongTransExtensionApp (W := W) gamma a ◁
          (G.mapComp f g).inv := by
  rfl

/-- Pointwise existence of StrongTrans naturality is closed under composition. -/
theorem exists_higherLocalizedStrongTransNaturality_comp
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {a b c : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)}
    (f : a ⟶ b) (g : b ⟶ c)
    (hf :
      Nonempty
        (F.map f ≫
              higherLocalizedStrongTransExtensionApp (W := W) gamma b ≅
          higherLocalizedStrongTransExtensionApp (W := W) gamma a ≫
            G.map f))
    (hg :
      Nonempty
        (F.map g ≫
              higherLocalizedStrongTransExtensionApp (W := W) gamma c ≅
          higherLocalizedStrongTransExtensionApp (W := W) gamma b ≫
            G.map g)) :
    Nonempty
      (F.map (f ≫ g) ≫
            higherLocalizedStrongTransExtensionApp (W := W) gamma c ≅
        higherLocalizedStrongTransExtensionApp (W := W) gamma a ≫
          G.map (f ≫ g)) := by
  rcases hf with ⟨naturality_f⟩
  rcases hg with ⟨naturality_g⟩
  exact
    ⟨higherLocalizedStrongTransNaturality_comp
      (W := W) gamma f g naturality_f naturality_g⟩

/-- Packaging of the preceding theorem as a compositional closure predicate.
This is the shape needed by localization/path-generation arguments. -/
def HigherLocalizedStrongTransNaturalityExists
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {a b : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)}
    (f : a ⟶ b) : Prop :=
  Nonempty
    (F.map f ≫ higherLocalizedStrongTransExtensionApp (W := W) gamma b ≅
      higherLocalizedStrongTransExtensionApp (W := W) gamma a ≫ G.map f)

/-- The existence predicate is stable under composition. -/
theorem HigherLocalizedStrongTransNaturalityExists.comp
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {a b c : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)}
    (f : a ⟶ b) (g : b ⟶ c)
    (hf : HigherLocalizedStrongTransNaturalityExists (W := W) gamma f)
    (hg : HigherLocalizedStrongTransNaturalityExists (W := W) gamma g) :
    HigherLocalizedStrongTransNaturalityExists (W := W) gamma (f ≫ g) :=
  exists_higherLocalizedStrongTransNaturality_comp
    (W := W) gamma f g hf hg

/-! ## Regression checks -/

#print axioms higherLocalizedStrongTransNaturality_comp
#print axioms higherLocalizedStrongTransNaturality_comp_hom
#print axioms exists_higherLocalizedStrongTransNaturality_comp
#print axioms HigherLocalizedStrongTransNaturalityExists.comp

end

end KUOS.DependentOriginationExactUniversalAmbientStrongTransCompositionNaturalityV4_99
