import KUOS.DependentOriginationStoredTriangleModificationNaturalityV2_23

namespace KUOS.DependentOriginationStoredTriangleModificationRealizationV2_24

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationModificationTriangleNormalFormV2_22
open KUOS.DependentOriginationStoredTriangleModificationNaturalityV2_23

open scoped CategoryTheory.Pseudofunctor.StrongTrans

universe u v uH vH

/-!
# Stored triangle modification realization v2.24

The v2.23 layer gives a direct sufficient condition for a v2.18 factor's stored
objectwise natural-isomorphism family to assemble into an invertible StrongTrans
modification: the stored family must satisfy modification naturality.

This file sharpens that statement without enlarging the claim.  We distinguish
between

* existence of an arbitrary modification triangle on the fixed factor StrongTrans,
  as in v2.22; and
* existence of a modification triangle whose forward object-components are
  exactly the Cat 2-isomorphisms reconstructed from the v2.18 stored NatIso family.

For the second, stored-family notion, modification naturality is not merely
sufficient: it is exactly equivalent to realization by a modification.  This does
not make stored-family naturality necessary for the broader v2.22 triangle
existence problem, because a different modification triangle may still exist.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- The stored v2.18 objectwise triangle is realized by an invertible StrongTrans
modification whose forward component at every raw context object is exactly the
stored Cat 2-isomorphism.

Only the forward component is recorded explicitly.  Since `e` is an isomorphism,
its inverse component is already determined by the forward isomorphism data. -/
def HasStoredV2_18TriangleModification
    {R : RawHigherContextualSystem (Context := Context)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K) : Prop :=
  ∃ e :
      (restrictHigherLocalizedStrongTrans (W := W) alpha.hom ≫ K.comparison) ≅
        H.comparison,
    ∀ X : Context,
      e.hom.as.app (.mk X) =
        (storedV2_18ComparisonComponentIso (W := W) alpha X).hom

/-- Modification naturality of the stored v2.18 family constructs a modification
that realizes that exact stored family. -/
theorem hasStoredV2_18TriangleModification_of_naturality
    {R : RawHigherContextualSystem (Context := Context)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K)
    (hNatural : StoredV2_18TriangleIsModificationNatural (W := W) alpha) :
    HasStoredV2_18TriangleModification (W := W) alpha := by
  refine ⟨Pseudofunctor.StrongTrans.isoMk
    (fun X => storedV2_18ComparisonComponentIso (W := W) alpha X.as) ?_, ?_⟩
  · intro X Y f
    simpa using hNatural f.as
  · intro X
    rfl

/-- Conversely, if an invertible modification realizes the stored v2.18 forward
components, its modification naturality equation is exactly the v2.23 stored-family
naturality condition. -/
theorem storedV2_18TriangleIsModificationNatural_of_hasStoredModification
    {R : RawHigherContextualSystem (Context := Context)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K)
    (h : HasStoredV2_18TriangleModification (W := W) alpha) :
    StoredV2_18TriangleIsModificationNatural (W := W) alpha := by
  rcases h with ⟨e, hApp⟩
  intro X Y f
  have hNatural := e.hom.as.naturality f.toLoc
  rw [hApp Y, hApp X] at hNatural
  exact hNatural

/-- Exact factorwise characterization of coherence of the *stored* v2.18
objectwise triangle family. -/
theorem storedV2_18TriangleIsModificationNatural_iff_hasStoredModification
    {R : RawHigherContextualSystem (Context := Context)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K) :
    StoredV2_18TriangleIsModificationNatural (W := W) alpha ↔
      HasStoredV2_18TriangleModification (W := W) alpha := by
  constructor
  · exact hasStoredV2_18TriangleModification_of_naturality W alpha
  · exact storedV2_18TriangleIsModificationNatural_of_hasStoredModification W alpha

/-- A stored-family realization is, in particular, an arbitrary v2.22 factor
modification triangle after forgetting which objectwise components realize it. -/
theorem hasFactorModificationTriangle_of_hasStoredV2_18TriangleModification
    {R : RawHigherContextualSystem (Context := Context)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K)
    (h : HasStoredV2_18TriangleModification (W := W) alpha) :
    HasFactorModificationTriangle (W := W) alpha := by
  rcases h with ⟨e, _⟩
  exact ⟨e⟩

/-- Every v2.18 factor into one chosen coherent universal factorization has its
stored objectwise triangle realized by an invertible modification. -/
def HigherStoredV2_18TriangleModificationRealization
    {R : RawHigherContextualSystem (Context := Context)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∀ (H : HigherLocalizationFactorization (W := W) R)
    (alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),
    HasStoredV2_18TriangleModification (W := W) alpha

/-- Uniform v2.23 stored-family naturality is exactly uniform realization of the
stored family by invertible modifications. -/
theorem higherStoredV2_18TriangleModificationNaturality_iff_realization
    {R : RawHigherContextualSystem (Context := Context)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherStoredV2_18TriangleModificationNaturality (W := W) U ↔
      HigherStoredV2_18TriangleModificationRealization (W := W) U := by
  constructor
  · intro hNatural H alpha
    exact
      hasStoredV2_18TriangleModification_of_naturality
        W alpha (hNatural H alpha)
  · intro hReal H alpha
    exact
      storedV2_18TriangleIsModificationNatural_of_hasStoredModification
        W alpha (hReal H alpha)

/-- Failure of stored-family realization is witnessed by a v2.18 factor whose
stored objectwise triangle cannot itself be assembled into an invertible
modification.  This is deliberately narrower than the v2.22 obstruction to all
possible modification triangles. -/
def HigherStoredV2_18TriangleRealizationObstruction
    {R : RawHigherContextualSystem (Context := Context)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∃ (H : HigherLocalizationFactorization (W := W) R)
    (alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),
    ¬ HasStoredV2_18TriangleModification (W := W) alpha

/-- Uniform realization of the stored family is exactly absence of the explicit
stored-family realization obstruction. -/
theorem higherStoredV2_18TriangleModificationRealization_iff_no_obstruction
    {R : RawHigherContextualSystem (Context := Context)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherStoredV2_18TriangleModificationRealization (W := W) U ↔
      ¬ HigherStoredV2_18TriangleRealizationObstruction (W := W) U := by
  constructor
  · intro hReal hObs
    rcases hObs with ⟨H, alpha, hNoRealization⟩
    exact hNoRealization (hReal H alpha)
  · intro hNoObs H alpha
    classical
    by_contra hNoRealization
    exact hNoObs ⟨H, alpha, hNoRealization⟩

/-- Consequently, v2.23 stored-family modification naturality is exactly absence
of the stored-family realization obstruction.  No statement about arbitrary
alternative modification triangles is inferred. -/
theorem higherStoredV2_18TriangleModificationNaturality_iff_no_realizationObstruction
    {R : RawHigherContextualSystem (Context := Context)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherStoredV2_18TriangleModificationNaturality (W := W) U ↔
      ¬ HigherStoredV2_18TriangleRealizationObstruction (W := W) U :=
  (higherStoredV2_18TriangleModificationNaturality_iff_realization
    (W := W) U).trans
      (higherStoredV2_18TriangleModificationRealization_iff_no_obstruction
        (W := W) U)

/-- Global realization principle for the stored v2.18 triangle families.  This is
an explicit proposition, not an axiom. -/
def HigherStoredV2_18TriangleModificationRealizationPrinciple : Prop :=
  ∀ (R : RawHigherContextualSystem (Context := Context))
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R),
    HigherStoredV2_18TriangleModificationRealization (W := W) U

/-- The global v2.23 naturality principle and the global stored-family realization
principle are equivalent formulations of the same additional coherence demand. -/
theorem higherStoredV2_18TriangleModificationNaturalityPrinciple_iff_realizationPrinciple :
    HigherStoredV2_18TriangleModificationNaturalityPrinciple (W := W) ↔
      HigherStoredV2_18TriangleModificationRealizationPrinciple (W := W) := by
  constructor
  · intro hNatural R U
    exact
      (higherStoredV2_18TriangleModificationNaturality_iff_realization
        (W := W) U).mp (hNatural R U)
  · intro hReal R U
    exact
      (higherStoredV2_18TriangleModificationNaturality_iff_realization
        (W := W) U).mpr (hReal R U)

/-!
The boundary after v2.24 is therefore:

```text
stored v2.18 objectwise triangle family is modification-natural
                    ↕              exact equivalence
that same stored family is realized by an invertible modification
                    ↓              forget stored-component identity
some v2.22 modification triangle exists.
```

Only the first equivalence is claimed.  The final downward arrow is one-way:
an arbitrary coherent modification triangle need not coincide with the objectwise
NatIso family originally stored in the v2.18 factor.
-/

end KUOS.DependentOriginationStoredTriangleModificationRealizationV2_24
