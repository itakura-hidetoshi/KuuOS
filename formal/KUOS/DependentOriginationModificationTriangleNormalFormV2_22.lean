import KUOS.DependentOriginationFactorCoherenceLiftingV2_21

namespace KUOS.DependentOriginationModificationTriangleNormalFormV2_22

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationFactorCoherenceLiftingV2_21

open scoped CategoryTheory.Pseudofunctor.StrongTrans

universe u v uH vH

/-!
# Modification-triangle normal form v2.22

The v2.21 layer isolates the exact extra hypothesis needed to transport the
coherent v2.19 universal property to the objectwise v2.18 universal property:
every v2.18 factor morphism must admit a coherent refinement with the same
underlying StrongTrans.

This file shows that the lifting problem contains no additional hidden 1-cell
construction.  For a fixed v2.18 factor morphism `alpha`, a coherent refinement
with unchanged underlying StrongTrans exists if and only if the single
modification-level comparison triangle

```text
restrict(alpha.hom) ≫ K.comparison ≅ H.comparison
```

exists.  Thus the remaining obstruction is purely a 2-cell coherence problem on
an already-given StrongTrans.

No modification triangle is asserted to exist unconditionally.  No global weak
localization principle, strictification principle, or ordinary-localization
substitute is introduced.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- The pure modification-level coherence condition for one v2.18 factor
morphism.  The factor 1-cell is fixed to be `alpha.hom`; only an invertible
modification filling the comparison triangle is requested. -/
def HasFactorModificationTriangle
    {R : RawHigherContextualSystem (Context := Context)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K) : Prop :=
  Nonempty
    ((restrictHigherLocalizedStrongTrans (W := W) alpha.hom ≫ K.comparison) ≅
      H.comparison)

/-- A v2.21 coherent lift exists exactly when the already-given v2.18 factor
StrongTrans admits the required invertible modification triangle. -/
theorem coherentLiftOfV2_18Factor_iff_hasFactorModificationTriangle
    {R : RawHigherContextualSystem (Context := Context)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K) :
    Nonempty (CoherentLiftOfV2_18Factor (W := W) alpha) ↔
      HasFactorModificationTriangle (W := W) alpha := by
  constructor
  · rintro ⟨lift⟩
    exact ⟨by simpa only [lift.hom_eq] using lift.coherent.comparison_triangle⟩
  · rintro ⟨triangle⟩
    exact ⟨{
      coherent := {
        hom := alpha.hom
        comparison_triangle := triangle
      }
      hom_eq := rfl
    }⟩

/-- Normal-form version of factor-coherence lifting: every v2.18 factor into the
chosen coherent universal factorization carries the modification triangle on its
existing underlying StrongTrans. -/
def HigherFactorModificationTriangleLifting
    {R : RawHigherContextualSystem (Context := Context)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∀ (H : HigherLocalizationFactorization (W := W) R)
    (alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),
    HasFactorModificationTriangle (W := W) alpha

/-- The v2.21 factor-coherence lifting condition is exactly the pure
modification-triangle lifting condition. -/
theorem higherFactorCoherenceLifting_iff_modificationTriangleLifting
    {R : RawHigherContextualSystem (Context := Context)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherFactorCoherenceLifting (W := W) U ↔
      HigherFactorModificationTriangleLifting (W := W) U := by
  constructor
  · intro hLift H alpha
    exact
      (coherentLiftOfV2_18Factor_iff_hasFactorModificationTriangle
        (W := W) alpha).mp (hLift H alpha)
  · intro hTriangle H alpha
    exact
      (coherentLiftOfV2_18Factor_iff_hasFactorModificationTriangle
        (W := W) alpha).mpr (hTriangle H alpha)

/-- The normal-form obstruction: one already-given v2.18 factor StrongTrans has
no invertible modification filling its comparison triangle. -/
def HigherFactorModificationTriangleObstruction
    {R : RawHigherContextualSystem (Context := Context)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∃ (H : HigherLocalizationFactorization (W := W) R)
    (alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),
    ¬ HasFactorModificationTriangle (W := W) alpha

/-- The v2.21 obstruction is equivalent to failure of an invertible
modification triangle on an existing factor StrongTrans. -/
theorem higherFactorCoherenceObstruction_iff_modificationTriangleObstruction
    {R : RawHigherContextualSystem (Context := Context)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherFactorCoherenceObstruction (W := W) U ↔
      HigherFactorModificationTriangleObstruction (W := W) U := by
  constructor
  · rintro ⟨H, alpha, hNoLift⟩
    refine ⟨H, alpha, ?_⟩
    intro hTriangle
    exact hNoLift
      ((coherentLiftOfV2_18Factor_iff_hasFactorModificationTriangle
        (W := W) alpha).mpr hTriangle)
  · rintro ⟨H, alpha, hNoTriangle⟩
    refine ⟨H, alpha, ?_⟩
    intro hLift
    exact hNoTriangle
      ((coherentLiftOfV2_18Factor_iff_hasFactorModificationTriangle
        (W := W) alpha).mp hLift)

/-- Pure triangle lifting is exactly absence of the pure triangle obstruction. -/
theorem higherFactorModificationTriangleLifting_iff_no_obstruction
    {R : RawHigherContextualSystem (Context := Context)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherFactorModificationTriangleLifting (W := W) U ↔
      ¬ HigherFactorModificationTriangleObstruction (W := W) U := by
  rw [← higherFactorCoherenceLifting_iff_modificationTriangleLifting (W := W) U]
  rw [higherFactorCoherenceLifting_iff_no_obstruction (W := W) U]
  rw [higherFactorCoherenceObstruction_iff_modificationTriangleObstruction (W := W) U]

/-- Global normal-form principle: every v2.18 factor into every coherent
universal-property datum admits the required invertible modification triangle on
its existing StrongTrans.  This remains an explicit proposition, not an axiom. -/
def HigherFactorModificationTriangleLiftingPrinciple : Prop :=
  ∀ (R : RawHigherContextualSystem (Context := Context))
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R),
    HigherFactorModificationTriangleLifting (W := W) U

/-- The global v2.21 lifting principle and its pure modification-triangle normal
form are equivalent. -/
theorem higherFactorCoherenceLiftingPrinciple_iff_modificationTrianglePrinciple :
    HigherFactorCoherenceLiftingPrinciple (W := W) ↔
      HigherFactorModificationTriangleLiftingPrinciple (W := W) := by
  constructor
  · intro h R U
    exact
      (higherFactorCoherenceLifting_iff_modificationTriangleLifting
        (W := W) U).mp (h R U)
  · intro h R U
    exact
      (higherFactorCoherenceLifting_iff_modificationTriangleLifting
        (W := W) U).mpr (h R U)

/-- Consequently, the coherent weak-localization universal principle together
with the pure modification-triangle lifting principle implies the v2.18 weak
higher localization universal principle.

This is only a conditional transport theorem: neither premise is proved here. -/
theorem higherWeakLocalizationUniversalPrinciple_of_coherent_and_modificationTriangles
    (hCoherent : CoherentHigherWeakLocalizationUniversalPrinciple (W := W))
    (hTriangles : HigherFactorModificationTriangleLiftingPrinciple (W := W)) :
    HigherWeakLocalizationUniversalPrinciple (W := W) :=
  higherWeakLocalizationUniversalPrinciple_of_coherent_and_factorCoherenceLifting
    W hCoherent
      ((higherFactorCoherenceLiftingPrinciple_iff_modificationTrianglePrinciple
        (W := W)).mpr hTriangles)

/-!
The boundary after v2.22 is therefore sharper:

```text
v2.18 factor alpha : H -> K
        |
        | underlying StrongTrans already fixed
        v
HasFactorModificationTriangle alpha
        <->
Nonempty (CoherentLiftOfV2_18Factor alpha)

HigherFactorCoherenceLifting
        <->
all existing v2.18 factors admit those invertible modification triangles.
```

Thus the unresolved lifting problem is genuinely 2-categorical: it asks for a
coherent invertible modification between two StrongTrans with the factor 1-cell
already fixed.  No additional factor 1-cell, strictification, or ordinary
localization is hidden in the statement.
-/

end KUOS.DependentOriginationModificationTriangleNormalFormV2_22
