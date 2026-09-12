import KUOS.DependentOriginationStrictHigherLocalizationV2_11

namespace KUOS.DependentOriginationStrictHigherFactorizationV2_12

open CategoryTheory
open Opposite
open KUOS.DependentOriginationPresentationUniversalityV2_0
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationStrictHigherLocalizationV2_11

open scoped CategoryTheory.Pseudofunctor.StrongTrans

attribute [local simp]
  CategoryTheory.Bicategory.Strict.leftUnitor_eqToIso
  CategoryTheory.Bicategory.Strict.rightUnitor_eqToIso
  CategoryTheory.Bicategory.Strict.associator_eqToIso
  CategoryTheory.PrelaxFunctor.map₂_eqToHom
  CategoryTheory.eqToHom_map

universe u v uH vH

/-!
# Strict higher presentation-localization factorization v2.12

The v2.11 layer proves that an ordinary Cat-valued functor

```text
G : C ⥤ Cat
```

which sends every arrow in `W` to an isomorphism in the 1-category `Cat`
admits the ordinary localized lift

```text
Gbar : C[W⁻¹] ⥤ Cat.
```

It also promotes both the raw and localized ordinary functors to the exact
pseudofunctor shapes used by the higher KuuOS stack layer.  What remained was
to connect the ordinary localization factorization natural isomorphism to the
v2.10 `HigherLocalizationFactorization` interface, whose comparison 1-cell is a
strong transformation of pseudofunctors.

In the strict sector this bridge is canonical.  The component functors of the
ordinary natural isomorphism are used as the components of a strong
transformation.  Ordinary naturality is an equality of functors in `Cat`, hence
supplies the required invertible 2-cell by `eqToIso`.  This closes existence of
the v2.10 factorization interface for the strict sector, while leaving the weak
"equivalence of categories" sector genuinely open.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- The ordinary localization natural isomorphism promoted to the strong
comparison required by the higher localization interface. -/
noncomputable def strictHigherLocalizationComparison
    (G : Context ⥤ Cat.{vH, uH})
    (hG : W.IsInvertedBy G) :
    restrictHigherLocalizedSystem W
        (strictLocalizedHigherSystem W G hG) ⟶
      strictRawHigherSystem G where
  app X := (strictLocalizationFactorizationIso W G hG).hom.app X.as
  naturality {X Y} f := eqToIso (by
    change
      (strictLocalizedFunctor W G hG).map (W.Q.map f.as) ≫
          (strictLocalizationFactorizationIso W G hG).hom.app Y.as =
        (strictLocalizationFactorizationIso W G hG).hom.app X.as ≫ G.map f.as
    simpa using
      (strictLocalizationFactorizationIso W G hG).hom.naturality f.as)
  naturality_naturality η := by
    obtain rfl := obj_ext_of_isDiscrete η
    apply Cat.Hom₂.ext
    ext X
    simp [restrictHigherLocalizedSystem, strictLocalizedHigherSystem,
      CategoryTheory.Pseudofunctor.comp,
      CategoryTheory.Functor.toPseudofunctor,
      CategoryTheory.Functor.toPseudofunctor',
      CategoryTheory.pseudofunctorOfIsLocallyDiscrete] <;>
      simp
  naturality_id X := by
    apply Cat.Hom₂.ext
    ext Y
    simp [restrictHigherLocalizedSystem, strictLocalizedHigherSystem,
      CategoryTheory.Pseudofunctor.comp,
      CategoryTheory.Functor.toPseudofunctor,
      CategoryTheory.Functor.toPseudofunctor',
      CategoryTheory.pseudofunctorOfIsLocallyDiscrete] <;>
      simp
  naturality_comp f g := by
    apply Cat.Hom₂.ext
    ext X
    simp [restrictHigherLocalizedSystem, strictLocalizedHigherSystem,
      CategoryTheory.Pseudofunctor.comp,
      CategoryTheory.Functor.toPseudofunctor,
      CategoryTheory.Functor.toPseudofunctor',
      CategoryTheory.pseudofunctorOfIsLocallyDiscrete] <;>
      simp

/-- Every component of the strict comparison is an equivalence of categories.
Indeed it is already an isomorphism in `Cat`, because it is a component of the
ordinary localization natural isomorphism. -/
theorem strictHigherLocalizationComparison_app_isEquivalence
    (G : Context ⥤ Cat.{vH, uH})
    (hG : W.IsInvertedBy G)
    (X : Context) :
    ((strictHigherLocalizationComparison W G hG).app (.mk X)).toFunctor.IsEquivalence := by
  change
    ((strictLocalizationFactorizationIso W G hG).hom.app X).toFunctor.IsEquivalence
  let eCat := (strictLocalizationFactorizationIso W G hG).app X
  let e :
      (strictLocalizedFunctor W G hG).obj (W.Q.obj X) ≌ G.obj X :=
    CategoryTheory.Equivalence.mk eCat.hom.toFunctor eCat.inv.toFunctor
      (eqToIso (congrArg Cat.Hom.toFunctor eCat.hom_inv_id).symm)
      (eqToIso (congrArg Cat.Hom.toFunctor eCat.inv_hom_id))
  simpa [e, eCat] using e.isEquivalence_functor

/-- Canonical v2.10 higher localization factorization data for the strict
Cat-valued sector. -/
noncomputable def strictHigherLocalizationFactorization
    (G : Context ⥤ Cat.{vH, uH})
    (hG : W.IsInvertedBy G) :
    HigherLocalizationFactorization (W := W)
      (strictRawHigherSystem G) where
  lift := strictLocalizedHigherSystem W G hG
  comparison := strictHigherLocalizationComparison W G hG
  comparison_isEquivalence :=
    strictHigherLocalizationComparison_app_isEquivalence W G hG

/-- Thus every ordinary Cat-valued contextual functor which strictly inverts
`W` has an actual higher localization factorization in the exact v2.10 sense. -/
theorem strictSector_hasHigherLocalizationFactorization
    (G : Context ⥤ Cat.{vH, uH})
    (hG : W.IsInvertedBy G) :
    HasHigherLocalizationFactorization (W := W)
      (strictRawHigherSystem G) :=
  ⟨strictHigherLocalizationFactorization W G hG⟩

/-!
The strict existence route is now fully closed:

```text
G : C ⥤ Cat
+ W.IsInvertedBy G
        ↓
ordinary localization lift Gbar
        ↓
localized Cat-valued pseudofunctor
        ↓
strong comparison (restriction Gbar) ⟶ G
+ pointwise category equivalence
        ↓
HigherLocalizationFactorization.
```

This theorem still does not extend from strict isomorphisms in `Cat` to arbitrary
categorical equivalences.  The remaining universal problem is therefore exactly
the weak bicategorical localization / strictification step, not the packaging of
strict ordinary localization into the higher KuuOS interface.
-/

end KUOS.DependentOriginationStrictHigherFactorizationV2_12
