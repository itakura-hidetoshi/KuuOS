import KUOS.DependentOriginationStoredTriangleModificationRealizationV2_24

namespace KUOS.DependentOriginationArbitraryTrianglePresentationV2_25

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationModificationTriangleNormalFormV2_22
open KUOS.DependentOriginationStoredTriangleModificationNaturalityV2_23
open KUOS.DependentOriginationStoredTriangleModificationRealizationV2_24

open scoped CategoryTheory.Pseudofunctor.StrongTrans

universe u v uH vH

/-!
# Arbitrary modification-triangle presentations v2.25

The v2.22--v2.24 layers distinguish two logically different questions for a
fixed v2.18 factor morphism `alpha`:

* does the particular objectwise NatIso family stored in `alpha` assemble into
  an invertible modification? and
* does any invertible modification triangle exist on the already-fixed factor
  StrongTrans?

The first question was characterized exactly in v2.24 by modification naturality
of the stored family.  This file now gives the corresponding exact
characterization of the second, broader question.

An arbitrary modification triangle is presented by an arbitrary family of
objectwise Cat 2-isomorphisms with the same endpoints as the comparison triangle,
together with the modification naturality equation.  Such a coherent objectwise
presentation can be assembled by `Pseudofunctor.StrongTrans.isoMk`; conversely,
evaluating any invertible modification gives precisely such a presentation.

Thus the general v2.22 obstruction is not "the stored family is non-natural".
It is the stronger statement that **no coherent objectwise 2-isomorphism family
with the required endpoints exists at all**.  The stored family is only one
distinguished candidate among those possible presentations.

No existence of such a presentation is asserted unconditionally.  No
strictification theorem, general weak higher localization theorem, or ordinary
localization substitute is introduced.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- A coherent objectwise presentation of an arbitrary modification triangle for
one v2.18 factor morphism.

Unlike the v2.23 condition, `component` is not required to be the objectwise
NatIso family stored in `alpha`.  It may be any family of Cat 2-isomorphisms with
the correct endpoints, provided that its forward components satisfy the
modification naturality equation. -/
@[ext]
structure FactorModificationTrianglePresentation
    {R : RawHigherContextualSystem (Context := Context)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K) where
  component : ∀ X : Context,
    (restrictHigherLocalizedStrongTrans (W := W) alpha.hom ≫ K.comparison).app (.mk X) ≅
      H.comparison.app (.mk X)
  naturality : ∀ {X Y : Context} (f : X ⟶ Y),
    (restrictHigherLocalizedSystem W H.lift).map f.toLoc ◁
          (component Y).hom ≫
        (H.comparison.naturality f.toLoc).hom =
      ((restrictHigherLocalizedStrongTrans (W := W) alpha.hom ≫
          K.comparison).naturality f.toLoc).hom ≫
        (component X).hom ▷ R.map f.toLoc

/-- Evaluate an actual invertible modification triangle at one raw context
object, obtaining its objectwise Cat 2-isomorphism. -/
def factorModificationTriangleComponentIso
    {R : RawHigherContextualSystem (Context := Context)}
    {H K : HigherLocalizationFactorization (W := W) R}
    {alpha : HigherLocalizationFactorMorphism (W := W) H K}
    (e :
      (restrictHigherLocalizedStrongTrans (W := W) alpha.hom ≫ K.comparison) ≅
        H.comparison)
    (X : Context) :
    (restrictHigherLocalizedStrongTrans (W := W) alpha.hom ≫ K.comparison).app (.mk X) ≅
      H.comparison.app (.mk X) where
  hom := e.hom.as.app (.mk X)
  inv := e.inv.as.app (.mk X)
  hom_inv_id := by
    have h := congrArg (fun m => m.as.app (.mk X)) e.hom_inv_id
    exact h
  inv_hom_id := by
    have h := congrArg (fun m => m.as.app (.mk X)) e.inv_hom_id
    exact h

/-- Assemble a coherent objectwise presentation into the corresponding
invertible StrongTrans modification triangle. -/
def factorModificationTriangleOfPresentation
    {R : RawHigherContextualSystem (Context := Context)}
    {H K : HigherLocalizationFactorization (W := W) R}
    {alpha : HigherLocalizationFactorMorphism (W := W) H K}
    (P : FactorModificationTrianglePresentation (W := W) alpha) :
    (restrictHigherLocalizedStrongTrans (W := W) alpha.hom ≫ K.comparison) ≅
      H.comparison := by
  refine Pseudofunctor.StrongTrans.isoMk (fun X => P.component X.as) ?_
  intro X Y f
  simpa using P.naturality f.as

/-- Extract the coherent objectwise presentation carried by an actual invertible
modification triangle. -/
def factorModificationTrianglePresentationOfIso
    {R : RawHigherContextualSystem (Context := Context)}
    {H K : HigherLocalizationFactorization (W := W) R}
    {alpha : HigherLocalizationFactorMorphism (W := W) H K}
    (e :
      (restrictHigherLocalizedStrongTrans (W := W) alpha.hom ≫ K.comparison) ≅
        H.comparison) :
    FactorModificationTrianglePresentation (W := W) alpha where
  component X := factorModificationTriangleComponentIso (W := W) e X
  naturality f := by
    simpa [factorModificationTriangleComponentIso] using e.hom.as.naturality f.toLoc

/-- Extracting a presentation from one assembled by `isoMk` recovers the same
objectwise coherent presentation. -/
theorem presentationOfIso_ofPresentation
    {R : RawHigherContextualSystem (Context := Context)}
    {H K : HigherLocalizationFactorization (W := W) R}
    {alpha : HigherLocalizationFactorMorphism (W := W) H K}
    (P : FactorModificationTrianglePresentation (W := W) alpha) :
    factorModificationTrianglePresentationOfIso
        (W := W) (factorModificationTriangleOfPresentation (W := W) P) = P := by
  ext X
  apply Iso.ext
  rfl

/-- Reassembling the objectwise presentation extracted from an actual
modification triangle recovers the original modification triangle. -/
theorem isoOfPresentation_ofIso
    {R : RawHigherContextualSystem (Context := Context)}
    {H K : HigherLocalizationFactorization (W := W) R}
    {alpha : HigherLocalizationFactorMorphism (W := W) H K}
    (e :
      (restrictHigherLocalizedStrongTrans (W := W) alpha.hom ≫ K.comparison) ≅
        H.comparison) :
    factorModificationTriangleOfPresentation
        (W := W) (factorModificationTrianglePresentationOfIso (W := W) e) = e := by
  apply Iso.ext
  apply Pseudofunctor.StrongTrans.homCategory.ext
  intro X
  rfl

/-- Exact data-level equivalence between arbitrary invertible modification
triangles and coherent objectwise 2-isomorphism presentations. -/
def factorModificationTrianglePresentationEquiv
    {R : RawHigherContextualSystem (Context := Context)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K) :
    FactorModificationTrianglePresentation (W := W) alpha ≃
      ((restrictHigherLocalizedStrongTrans (W := W) alpha.hom ≫ K.comparison) ≅
        H.comparison) where
  toFun := factorModificationTriangleOfPresentation (W := W)
  invFun := factorModificationTrianglePresentationOfIso (W := W)
  left_inv := presentationOfIso_ofPresentation (W := W)
  right_inv := isoOfPresentation_ofIso (W := W)

/-- Existence of at least one coherent objectwise presentation for the factor
triangle.  This is deliberately broader than realization of the stored v2.18
family. -/
def HasCoherentFactorModificationTrianglePresentation
    {R : RawHigherContextualSystem (Context := Context)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K) : Prop :=
  Nonempty (FactorModificationTrianglePresentation (W := W) alpha)

/-- The general v2.22 modification-triangle condition is exactly existence of an
arbitrary coherent objectwise presentation. -/
theorem hasFactorModificationTriangle_iff_hasCoherentPresentation
    {R : RawHigherContextualSystem (Context := Context)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K) :
    HasFactorModificationTriangle (W := W) alpha ↔
      HasCoherentFactorModificationTrianglePresentation (W := W) alpha := by
  constructor
  · rintro ⟨e⟩
    exact ⟨factorModificationTrianglePresentationOfIso (W := W) e⟩
  · rintro ⟨P⟩
    exact ⟨factorModificationTriangleOfPresentation (W := W) P⟩

/-- When the stored v2.18 family is modification-natural, it determines a
distinguished coherent presentation among all possible arbitrary presentations. -/
def storedFactorModificationTrianglePresentation
    {R : RawHigherContextualSystem (Context := Context)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K)
    (hNatural : StoredV2_18TriangleIsModificationNatural (W := W) alpha) :
    FactorModificationTrianglePresentation (W := W) alpha where
  component X := storedV2_18ComparisonComponentIso (W := W) alpha X
  naturality f := hNatural f

/-- The distinguished presentation above has exactly the originally stored
objectwise components. -/
@[simp] theorem storedFactorModificationTrianglePresentation_component
    {R : RawHigherContextualSystem (Context := Context)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K)
    (hNatural : StoredV2_18TriangleIsModificationNatural (W := W) alpha)
    (X : Context) :
    (storedFactorModificationTrianglePresentation
      (W := W) alpha hNatural).component X =
        storedV2_18ComparisonComponentIso (W := W) alpha X := by
  rfl

/-- Stored-family modification naturality is therefore sufficient for existence
of an arbitrary coherent presentation, but the converse is intentionally not
claimed. -/
theorem hasCoherentPresentation_of_storedTriangleNaturality
    {R : RawHigherContextualSystem (Context := Context)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K)
    (hNatural : StoredV2_18TriangleIsModificationNatural (W := W) alpha) :
    HasCoherentFactorModificationTrianglePresentation (W := W) alpha :=
  ⟨storedFactorModificationTrianglePresentation (W := W) alpha hNatural⟩

/-- Uniform existence of coherent objectwise presentations for every v2.18
factor into one chosen coherent universal-property datum. -/
def HigherCoherentFactorModificationTrianglePresentationLifting
    {R : RawHigherContextualSystem (Context := Context)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∀ (H : HigherLocalizationFactorization (W := W) R)
    (alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),
    HasCoherentFactorModificationTrianglePresentation (W := W) alpha

/-- Uniform coherent-presentation lifting is exactly the v2.22 arbitrary
modification-triangle lifting condition. -/
theorem higherCoherentPresentationLifting_iff_modificationTriangleLifting
    {R : RawHigherContextualSystem (Context := Context)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherCoherentFactorModificationTrianglePresentationLifting (W := W) U ↔
      HigherFactorModificationTriangleLifting (W := W) U := by
  constructor
  · intro h H alpha
    exact
      (hasFactorModificationTriangle_iff_hasCoherentPresentation
        (W := W) alpha).mpr (h H alpha)
  · intro h H alpha
    exact
      (hasFactorModificationTriangle_iff_hasCoherentPresentation
        (W := W) alpha).mp (h H alpha)

/-- Failure of the arbitrary coherent-presentation lifting problem.  A witness
factor has no coherent objectwise 2-isomorphism family at all with the required
endpoints. -/
def HigherCoherentFactorModificationTrianglePresentationObstruction
    {R : RawHigherContextualSystem (Context := Context)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∃ (H : HigherLocalizationFactorization (W := W) R)
    (alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),
    ¬ HasCoherentFactorModificationTrianglePresentation (W := W) alpha

/-- The arbitrary coherent-presentation obstruction is exactly the v2.22
modification-triangle obstruction. -/
theorem higherCoherentPresentationObstruction_iff_modificationTriangleObstruction
    {R : RawHigherContextualSystem (Context := Context)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherCoherentFactorModificationTrianglePresentationObstruction (W := W) U ↔
      HigherFactorModificationTriangleObstruction (W := W) U := by
  constructor
  · rintro ⟨H, alpha, hNoPresentation⟩
    refine ⟨H, alpha, ?_⟩
    intro hTriangle
    exact hNoPresentation
      ((hasFactorModificationTriangle_iff_hasCoherentPresentation
        (W := W) alpha).mp hTriangle)
  · rintro ⟨H, alpha, hNoTriangle⟩
    refine ⟨H, alpha, ?_⟩
    intro hPresentation
    exact hNoTriangle
      ((hasFactorModificationTriangle_iff_hasCoherentPresentation
        (W := W) alpha).mpr hPresentation)

/-- Uniform arbitrary coherent-presentation lifting is exactly absence of its
explicit obstruction. -/
theorem higherCoherentPresentationLifting_iff_no_obstruction
    {R : RawHigherContextualSystem (Context := Context)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherCoherentFactorModificationTrianglePresentationLifting (W := W) U ↔
      ¬ HigherCoherentFactorModificationTrianglePresentationObstruction
        (W := W) U := by
  rw [higherCoherentPresentationLifting_iff_modificationTriangleLifting (W := W) U]
  rw [higherFactorModificationTriangleLifting_iff_no_obstruction (W := W) U]
  rw [← higherCoherentPresentationObstruction_iff_modificationTriangleObstruction
    (W := W) U]

/-- If no arbitrary coherent presentation exists for some factor, then in
particular the distinguished stored family cannot be realized there.  Hence the
general v2.22 obstruction implies the narrower stored-family realization
obstruction.

The converse is deliberately not asserted. -/
theorem higherStoredRealizationObstruction_of_coherentPresentationObstruction
    {R : RawHigherContextualSystem (Context := Context)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hObs : HigherCoherentFactorModificationTrianglePresentationObstruction
      (W := W) U) :
    HigherStoredV2_18TriangleRealizationObstruction (W := W) U := by
  rcases hObs with ⟨H, alpha, hNoPresentation⟩
  refine ⟨H, alpha, ?_⟩
  intro hStored
  have hTriangle : HasFactorModificationTriangle (W := W) alpha :=
    hasFactorModificationTriangle_of_hasStoredV2_18TriangleModification
      W alpha hStored
  exact hNoPresentation
    ((hasFactorModificationTriangle_iff_hasCoherentPresentation
      (W := W) alpha).mp hTriangle)

/-- Uniform realization of the stored v2.18 family implies uniform existence of
arbitrary coherent presentations. -/
theorem higherCoherentPresentationLifting_of_storedRealization
    {R : RawHigherContextualSystem (Context := Context)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hStored : HigherStoredV2_18TriangleModificationRealization (W := W) U) :
    HigherCoherentFactorModificationTrianglePresentationLifting (W := W) U := by
  intro H alpha
  have hTriangle : HasFactorModificationTriangle (W := W) alpha :=
    hasFactorModificationTriangle_of_hasStoredV2_18TriangleModification
      W alpha (hStored H alpha)
  exact
    (hasFactorModificationTriangle_iff_hasCoherentPresentation
      (W := W) alpha).mp hTriangle

/-- Global arbitrary coherent-presentation lifting principle.  This proposition
is a reformulation of the existing v2.22 global triangle-lifting principle, not
an additional axiom. -/
def HigherCoherentFactorModificationTrianglePresentationPrinciple : Prop :=
  ∀ (R : RawHigherContextualSystem (Context := Context))
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R),
    HigherCoherentFactorModificationTrianglePresentationLifting (W := W) U

/-- The global coherent-presentation principle and the v2.22 global arbitrary
modification-triangle principle are equivalent. -/
theorem higherCoherentPresentationPrinciple_iff_modificationTrianglePrinciple :
    HigherCoherentFactorModificationTrianglePresentationPrinciple (W := W) ↔
      HigherFactorModificationTriangleLiftingPrinciple (W := W) := by
  constructor
  · intro h R U
    exact
      (higherCoherentPresentationLifting_iff_modificationTriangleLifting
        (W := W) U).mp (h R U)
  · intro h R U
    exact
      (higherCoherentPresentationLifting_iff_modificationTriangleLifting
        (W := W) U).mpr (h R U)

/-- The global stored-family naturality principle supplies one distinguished
coherent presentation for every factor, and hence implies the general coherent-
presentation principle. -/
theorem higherCoherentPresentationPrinciple_of_storedTriangleNaturality
    (hStored : HigherStoredV2_18TriangleModificationNaturalityPrinciple (W := W)) :
    HigherCoherentFactorModificationTrianglePresentationPrinciple (W := W) := by
  intro R U H alpha
  exact
    hasCoherentPresentation_of_storedTriangleNaturality
      W alpha (hStored R U H alpha)

/-- Consequently, a coherent higher universal principle together with the exact
arbitrary coherent-presentation lifting principle implies the v2.18 weak higher
localization universal principle.

This remains conditional: neither global premise is proved here. -/
theorem higherWeakLocalizationUniversalPrinciple_of_coherent_and_presentations
    (hCoherent : CoherentHigherWeakLocalizationUniversalPrinciple (W := W))
    (hPresentations : HigherCoherentFactorModificationTrianglePresentationPrinciple
      (W := W)) :
    HigherWeakLocalizationUniversalPrinciple (W := W) :=
  higherWeakLocalizationUniversalPrinciple_of_coherent_and_modificationTriangles
    W hCoherent
      ((higherCoherentPresentationPrinciple_iff_modificationTrianglePrinciple
        (W := W)).mp hPresentations)

/-!
The frontier is now organized as an exact hierarchy:

```text
stored v2.18 family is modification-natural
                 |
                 | chooses the stored family itself
                 v
stored-family modification realization
                 |
                 | forget which components were stored
                 v
some coherent objectwise 2-Iso presentation exists
                 <->
some arbitrary invertible modification triangle exists
```

Therefore the two obstruction notions have different strengths:

```text
no arbitrary coherent presentation exists
                 |
                 v
stored family cannot be realized.
```

The reverse implication is not claimed: failure of the stored family may still
be repairable by choosing a different coherent objectwise 2-isomorphism family.
The remaining general weak higher-localization problem is thus a genuine
**coherent replacement existence problem**, not merely a naturality check on the
particular triangles stored by the v2.18 presentation.
-/

end KUOS.DependentOriginationArbitraryTrianglePresentationV2_25
