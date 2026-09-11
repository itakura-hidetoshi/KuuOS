import KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19

namespace KUOS.DependentOriginationCoherentFactorForgetfulBridgeV2_20

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19

open scoped CategoryTheory.Pseudofunctor.StrongTrans

universe u v uH vH

/-!
# Coherent-factor forgetful bridge v2.20

The v2.19 layer upgrades the comparison triangle of a higher-localization factor
map from an objectwise family of natural isomorphisms to one invertible
modification between StrongTrans.

This file proves the safe forgetful direction for **individual factor maps**:

```text
coherent modification-level factor morphism
                 |
                 | evaluate the modification at each raw context object
                 v
v2.18 objectwise factor morphism.
```

This is deliberately not promoted to an implication between the two universal-
property structures.  The reason is logical, not technical: v2.18 essential
uniqueness quantifies over all v2.18 factor morphisms, whereas the v2.19
uniqueness field quantifies only over coherent factor morphisms.  Forgetting
coherence on individual factors therefore does not by itself enlarge the scope of
the v2.19 uniqueness theorem.

No existence theorem, strictification theorem, or replacement of weak higher
localization by ordinary localization is asserted here.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Evaluate a coherent comparison triangle at one raw context object.

An isomorphism in the StrongTrans hom-category consists of inverse
modifications.  Evaluating those modifications at `X` gives inverse 2-cells in
`Cat`, hence an isomorphism between the corresponding functors. -/
def coherentComparisonComponentIso
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : CoherentHigherLocalizationFactorMorphism (W := W) H K)
    (X : Context) :
    (restrictHigherLocalizedStrongTrans (W := W) alpha.hom ≫ K.comparison).app (.mk X) ≅
      H.comparison.app (.mk X) where
  hom := alpha.comparison_triangle.hom.as.app (.mk X)
  inv := alpha.comparison_triangle.inv.as.app (.mk X)
  hom_inv_id := by
    have h := congrArg
      (fun m => m.as.app (.mk X)) alpha.comparison_triangle.hom_inv_id
    exact h
  inv_hom_id := by
    have h := congrArg
      (fun m => m.as.app (.mk X)) alpha.comparison_triangle.inv_hom_id
    exact h

/-- The modification-level triangle of v2.19 yields exactly the objectwise
natural-isomorphism triangle required by v2.18. -/
def coherentComparisonTriangleNatIso
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : CoherentHigherLocalizationFactorMorphism (W := W) H K)
    (X : Context) :
    (alpha.hom.app (.mk ((higherPresentationUnitFunctor W).obj X))).toFunctor ⋙
        (K.comparison.app (.mk X)).toFunctor ≅
      (H.comparison.app (.mk X)).toFunctor := by
  simpa using
    Cat.Hom.toNatIso (coherentComparisonComponentIso (W := W) alpha X)

/-- Forget the modification-level coherence of a v2.19 factor morphism and
recover a valid v2.18 factor morphism with the same underlying StrongTrans. -/
def coherentHigherLocalizationFactorMorphismToV2_18
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : CoherentHigherLocalizationFactorMorphism (W := W) H K) :
    HigherLocalizationFactorMorphism (W := W) H K where
  hom := alpha.hom
  comparison_triangle X := coherentComparisonTriangleNatIso (W := W) alpha X

/-- Forgetting coherence preserves the underlying StrongTrans definitionally. -/
@[simp] theorem coherentHigherLocalizationFactorMorphismToV2_18_hom
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : CoherentHigherLocalizationFactorMorphism (W := W) H K) :
    (coherentHigherLocalizationFactorMorphismToV2_18 (W := W) alpha).hom = alpha.hom := by
  rfl

/-- Every coherently supplied factor in a v2.19 universal-property datum can be
viewed as an ordinary v2.18 factor morphism into the same chosen factorization.

This theorem intentionally states only factor existence.  It does not claim the
full v2.18 universal property because of the different domains quantified over by
the two essential-uniqueness fields. -/
theorem coherentWeakUniversalProperty_hasV2_18Factor
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (H : HigherLocalizationFactorization (W := W) R) :
    Nonempty (HigherLocalizationFactorMorphism (W := W) H U.chosen) := by
  rcases U.factor H with ⟨alpha⟩
  exact ⟨coherentHigherLocalizationFactorMorphismToV2_18 (W := W) alpha⟩

/-!
The boundary after v2.20 is now sharper:

* v2.19 coherence really does refine the v2.18 triangle on each factor map;
* coherent factor existence therefore forgets to v2.18 factor existence;
* a full implication between universal-property structures still requires either
  a lifting/coherence theorem for arbitrary v2.18 factor morphisms or a reformulated
  uniqueness statement whose quantification domains match.

That remaining mismatch is kept explicit rather than hidden by an unjustified
coercion between universal properties.
-/

end KUOS.DependentOriginationCoherentFactorForgetfulBridgeV2_20
