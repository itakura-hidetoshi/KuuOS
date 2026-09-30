import KUOS.DependentOriginationExactUniversalLabelledBiequivalenceV4_89

namespace KUOS.DependentOriginationExactUniversalAmbientCoverageReductionV4_90

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMappingHomCategoryV4_60
open KUOS.DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70
open KUOS.DependentOriginationExactUniversalHomEquivalenceV4_83
open KUOS.DependentOriginationExactUniversalLabelledBiequivalenceV4_89

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory
open scoped Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Ambient DO₂ object-coverage reduction v4.90

v4.83 already proves that, for every pair of existing exact-universal source
objects, the actual realization induces an equivalence of hom categories.
v4.70 packages the same realization globally as a strict pseudofunctor.

Consequently the only additional Whitehead condition needed to pass from the
object-labelled sector of v4.89 to the full ambient DO₂ bicategory is
essential surjectivity on objects.

This file isolates that remaining condition as an explicit proposition and
proves both directions:

* ambient object coverage gives Whitehead biequivalence data whose forward
  pseudofunctor is exactly the v4.70 realization;
* any Whitehead biequivalence datum whose forward pseudofunctor is exactly
  that realization implies ambient object coverage.

Thus, for the actual exact-universal realization, existence of ambient
Whitehead data is equivalent to ambient object coverage.  No coverage theorem
is asserted unconditionally here.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

abbrev Source :=
  ExactUniversalRawObject.{u, v, uH, vH} (W := W) A

abbrev Ambient :=
  DependentOriginationCompletion2 (W := W) A

/-- The remaining object-level condition for extending the exact-universal
realization from its labelled image to all ambient DO₂ objects. -/
def ExactUniversalAmbientObjectCoverage : Prop :=
  ∀ Z : Ambient (W := W) A,
    ∃ X : Source (W := W) A,
      Nonempty (Bicategory.Equivalence X.carrier Z)

/-- The already proved v4.83 local equivalence, restated with the ambient target
of the v4.70 strict realization visible in the type. -/
def exactUniversalAmbientHomEquivalence
    (X Y : Source (W := W) A) :
    CategoryTheory.Equivalence
      (X ⟶ Y)
      ((exactUniversalRealization (W := W) A).obj X ⟶
        (exactUniversalRealization (W := W) A).obj Y) := by
  change CategoryTheory.Equivalence (X ⟶ Y) (X.carrier ⟶ Y.carrier)
  exact exactUniversalHomEquivalence (W := W) A X Y

/-- The forward functor of the local equivalence is exactly the hom functor of
the actual v4.70 strict realization. -/
theorem exactUniversalAmbientHomEquivalence_functor
    (X Y : Source (W := W) A) :
    (exactUniversalAmbientHomEquivalence (W := W) A X Y).functor =
      (exactUniversalRealization (W := W) A).mapFunctor X Y := by
  apply CategoryTheory.Functor.hext
  · intro f
    rfl
  · intro f g eta
    exact heq_of_eq rfl

/-- Ambient Whitehead data follows from object coverage; no additional local
1-cell or 2-cell hypothesis is needed. -/
def exactUniversalAmbientWhiteheadBiequivalenceOfCoverage
    (hcoverage : ExactUniversalAmbientObjectCoverage (W := W) A) :
    WhiteheadBiequivalenceData
      (Source (W := W) A)
      (Ambient (W := W) A) where
  forward :=
    (exactUniversalRealization (W := W) A).toPseudofunctor
  homEquiv X Y :=
    exactUniversalAmbientHomEquivalence (W := W) A X Y
  homEquiv_functor X Y := by
    apply CategoryTheory.Functor.hext
    · intro f
      rfl
    · intro f g eta
      exact heq_of_eq rfl
  object_essentially_surjective := by
    intro Z
    rcases hcoverage Z with ⟨X, hX⟩
    exact ⟨X, hX⟩

/-- If a Whitehead datum has exactly the actual v4.70 realization as its
forward pseudofunctor, then its object essential-surjectivity field is precisely
ambient object coverage. -/
theorem exactUniversalAmbientObjectCoverage_of_whitehead
    (data :
      WhiteheadBiequivalenceData
        (Source (W := W) A)
        (Ambient (W := W) A))
    (hforward :
      data.forward =
        (exactUniversalRealization (W := W) A).toPseudofunctor) :
    ExactUniversalAmbientObjectCoverage (W := W) A := by
  intro Z
  rcases data.object_essentially_surjective Z with ⟨X, hX⟩
  refine ⟨X, ?_⟩
  rw [hforward] at hX
  exact hX

/-- Existence of ambient Whitehead data with the actual realization fixed as
forward pseudofunctor. -/
def ExactUniversalAmbientWhiteheadExistence : Prop :=
  ∃ data :
      WhiteheadBiequivalenceData
        (Source (W := W) A)
        (Ambient (W := W) A),
    data.forward =
      (exactUniversalRealization (W := W) A).toPseudofunctor

/-- Main reduction theorem: for the actual exact-universal realization, the
ambient Whitehead problem is equivalent to ambient object coverage. -/
theorem exactUniversalAmbientWhiteheadExistence_iff_objectCoverage :
    ExactUniversalAmbientWhiteheadExistence (W := W) A ↔
      ExactUniversalAmbientObjectCoverage (W := W) A := by
  constructor
  · rintro ⟨data, hforward⟩
    exact exactUniversalAmbientObjectCoverage_of_whitehead
      (W := W) A data hforward
  · intro hcoverage
    exact ⟨
      exactUniversalAmbientWhiteheadBiequivalenceOfCoverage
        (W := W) A hcoverage,
      rfl⟩

/-! ## Regression checks -/

variable {X Y : Source (W := W) A}

example :
    CategoryTheory.Equivalence
      (X ⟶ Y)
      ((exactUniversalRealization (W := W) A).obj X ⟶
        (exactUniversalRealization (W := W) A).obj Y) :=
  exactUniversalAmbientHomEquivalence (W := W) A X Y

example
    (hcoverage : ExactUniversalAmbientObjectCoverage (W := W) A) :
    WhiteheadBiequivalenceData
      (Source (W := W) A)
      (Ambient (W := W) A) :=
  exactUniversalAmbientWhiteheadBiequivalenceOfCoverage
    (W := W) A hcoverage

example :
    ExactUniversalAmbientWhiteheadExistence (W := W) A ↔
      ExactUniversalAmbientObjectCoverage (W := W) A :=
  exactUniversalAmbientWhiteheadExistence_iff_objectCoverage
    (W := W) A

#print axioms exactUniversalAmbientHomEquivalence
#print axioms exactUniversalAmbientHomEquivalence_functor
#print axioms exactUniversalAmbientWhiteheadBiequivalenceOfCoverage
#print axioms exactUniversalAmbientObjectCoverage_of_whitehead
#print axioms exactUniversalAmbientWhiteheadExistence_iff_objectCoverage

end

end KUOS.DependentOriginationExactUniversalAmbientCoverageReductionV4_90
