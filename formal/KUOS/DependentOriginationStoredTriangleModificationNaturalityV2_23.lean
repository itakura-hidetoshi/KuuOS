import KUOS.DependentOriginationModificationTriangleNormalFormV2_22

namespace KUOS.DependentOriginationStoredTriangleModificationNaturalityV2_23

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationModificationTriangleNormalFormV2_22

open scoped CategoryTheory.Pseudofunctor.StrongTrans

universe u v uH vH

/-!
# Stored objectwise triangle modification naturality v2.23

The v2.22 layer shows that factor-coherence lifting is a pure 2-cell problem:
for an already-given v2.18 factor `alpha`, one only needs an invertible
modification

```text
restrict(alpha.hom) ≫ K.comparison ≅ H.comparison.
```

A v2.18 factor already stores, at every raw context object, a natural isomorphism
between the underlying Cat functors.  This file isolates the direct sufficient
condition under which that **stored family itself** assembles into the required
invertible modification: it must satisfy the modification naturality equation.

Pinned Mathlib provides `Pseudofunctor.StrongTrans.isoMk`, which constructs an
invertible modification from object-level isomorphisms once forward modification
naturality is supplied.  We therefore convert the stored v2.18 natural
isomorphisms back to Cat 2-isomorphisms and state exactly that equation.

This sufficient condition is deliberately not claimed to be necessary for v2.22
triangle existence.  A v2.18 factor may fail coherence for its stored objectwise
family while a different modification triangle on the same underlying StrongTrans
still exists.  No such alternative triangle is ruled out here.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- The Cat-level 2-isomorphism obtained from the objectwise natural isomorphism
stored in a v2.18 factor morphism. -/
def storedV2_18ComparisonComponentIso
    {R : RawHigherContextualSystem (Context := Context)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K)
    (X : Context) :
    (restrictHigherLocalizedStrongTrans (W := W) alpha.hom ≫ K.comparison).app (.mk X) ≅
      H.comparison.app (.mk X) := by
  simpa using Cat.Hom.isoMk (alpha.comparison_triangle X)

/-- The exact modification-naturality equation for the objectwise triangle family
already stored in a v2.18 factor morphism.

This is the missing coherence equation needed by `StrongTrans.isoMk`; no new
factor 1-cell and no new objectwise triangle are introduced. -/
def StoredV2_18TriangleIsModificationNatural
    {R : RawHigherContextualSystem (Context := Context)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K) : Prop :=
  ∀ {X Y : Context} (f : X ⟶ Y),
    (restrictHigherLocalizedSystem W H.lift).map f.toLoc ◁
          (storedV2_18ComparisonComponentIso (W := W) alpha Y).hom ≫
        (H.comparison.naturality f.toLoc).hom =
      ((restrictHigherLocalizedStrongTrans (W := W) alpha.hom ≫
          K.comparison).naturality f.toLoc).hom ≫
        (storedV2_18ComparisonComponentIso (W := W) alpha X).hom ▷ R.map f.toLoc

/-- If the objectwise triangle family stored in a v2.18 factor satisfies the
modification naturality equation, then that exact family assembles into the
invertible modification triangle required by v2.22. -/
theorem hasFactorModificationTriangle_of_storedV2_18TriangleIsModificationNatural
    {R : RawHigherContextualSystem (Context := Context)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K)
    (hNatural : StoredV2_18TriangleIsModificationNatural (W := W) alpha) :
    HasFactorModificationTriangle (W := W) alpha := by
  refine ⟨Pseudofunctor.StrongTrans.isoMk
    (fun X => storedV2_18ComparisonComponentIso (W := W) alpha X.as) ?_⟩
  intro X Y f
  simpa using hNatural f.as

/-- Uniform stored-triangle coherence for every v2.18 factor into one chosen
coherent universal factorization. -/
def HigherStoredV2_18TriangleModificationNaturality
    {R : RawHigherContextualSystem (Context := Context)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∀ (H : HigherLocalizationFactorization (W := W) R)
    (alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),
    StoredV2_18TriangleIsModificationNatural (W := W) alpha

/-- Uniform modification naturality of the stored v2.18 triangle families is a
sufficient condition for the pure modification-triangle lifting property of
v2.22. -/
theorem higherFactorModificationTriangleLifting_of_storedTriangleNaturality
    {R : RawHigherContextualSystem (Context := Context)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hNatural : HigherStoredV2_18TriangleModificationNaturality (W := W) U) :
    HigherFactorModificationTriangleLifting (W := W) U := by
  intro H alpha
  exact
    hasFactorModificationTriangle_of_storedV2_18TriangleIsModificationNatural
      W alpha (hNatural H alpha)

/-- Hence stored-triangle modification naturality also supplies the v2.21
factor-coherence lifting condition. -/
theorem higherFactorCoherenceLifting_of_storedTriangleNaturality
    {R : RawHigherContextualSystem (Context := Context)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hNatural : HigherStoredV2_18TriangleModificationNaturality (W := W) U) :
    KUOS.DependentOriginationFactorCoherenceLiftingV2_21.HigherFactorCoherenceLifting
      (W := W) U :=
  (higherFactorCoherenceLifting_iff_modificationTriangleLifting
    (W := W) U).mpr
      (higherFactorModificationTriangleLifting_of_storedTriangleNaturality
        W U hNatural)

/-- Global sufficient principle: every stored objectwise v2.18 triangle family
into every coherent universal-property datum satisfies modification naturality.
This remains an explicit proposition, not an axiom. -/
def HigherStoredV2_18TriangleModificationNaturalityPrinciple : Prop :=
  ∀ (R : RawHigherContextualSystem (Context := Context))
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R),
    HigherStoredV2_18TriangleModificationNaturality (W := W) U

/-- The global stored-triangle naturality principle implies the v2.22 pure
modification-triangle lifting principle. -/
theorem higherFactorModificationTriangleLiftingPrinciple_of_storedTriangleNaturality
    (hNatural : HigherStoredV2_18TriangleModificationNaturalityPrinciple (W := W)) :
    HigherFactorModificationTriangleLiftingPrinciple (W := W) := by
  intro R U
  exact
    higherFactorModificationTriangleLifting_of_storedTriangleNaturality
      W U (hNatural R U)

/-- Consequently, the coherent higher universal principle together with the
explicit modification naturality of all stored v2.18 triangle families implies
the v2.18 weak higher localization universal principle.

Neither premise is proved here. -/
theorem higherWeakLocalizationUniversalPrinciple_of_coherent_and_storedTriangleNaturality
    (hCoherent : CoherentHigherWeakLocalizationUniversalPrinciple (W := W))
    (hNatural : HigherStoredV2_18TriangleModificationNaturalityPrinciple (W := W)) :
    HigherWeakLocalizationUniversalPrinciple (W := W) :=
  higherWeakLocalizationUniversalPrinciple_of_coherent_and_modificationTriangles
    W hCoherent
      (higherFactorModificationTriangleLiftingPrinciple_of_storedTriangleNaturality
        W hNatural)

/-!
The boundary after v2.23 is now concrete at the equation level:

```text
v2.18 stored objectwise NatIso family
        +
modification naturality for every raw context arrow
        |
        v
invertible StrongTrans modification triangle
        |
        v
v2.22 factor modification-triangle lifting.
```

Failure of the *stored* family to satisfy this equation is not declared to be a
v2.22 obstruction: a different coherent modification on the same factor
StrongTrans may still exist.  The theorem proved here is therefore a strict,
honest sufficient condition rather than an unjustified equivalence.
-/

end KUOS.DependentOriginationStoredTriangleModificationNaturalityV2_23
