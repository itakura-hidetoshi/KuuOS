import KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27
import Mathlib.CategoryTheory.Bicategory.NaturalTransformation.Oplax
import Mathlib.CategoryTheory.Functor.ReflectsIso.Basic

namespace KUOS.DependentOriginationNormalizationChoiceInvariantV1_28

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Bicategory
open scoped Bicategory
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationGlobalDuskinLocalMappingComparisonV1_23
open KUOS.DependentOriginationGlobalDuskinLocalTwoCellComparisonV1_24
open KUOS.DependentOriginationPresentationIndependentInvariantV1_25
open KUOS.DependentOriginationBiequivalencePresentationInvariantV1_26
open KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27

universe u₁ u₂ v₁ v₂ w₁ w₂ z

/-!
# Normalization-choice invariant kernel v1.28

Version 1.27 proved direct global Duskin transport once a model equivalence has
already been presented by a strictly-unitary pseudofunctor. The remaining
presentation issue is the choice of such a normal representative.

The pinned Mathlib revision has native strong transformations between oplax
functors, but its `StrictlyUnitary.lean` file still lists identity-component
icons and automatic normalization as future work. Therefore this layer keeps
both missing constructions explicit instead of postulating them.

There are two levels of certificate.

1. `StrictlyUnitaryNormalizationCertificate E` says that a general v1.26 model
   equivalence `E` admits a chosen strictly-unitary representative, strongly
   equivalent to the original forward pseudofunctor, with equivalence
   components on objects.
2. `NormalizationChoiceComparison E₁ E₂` compares two strictly-unitary model
   equivalences by a native Mathlib strong transformation whose object
   components are intrinsic adjoint equivalences.

The second certificate already suffices to prove the mathematically correct
choice-independence statements:

* transported 1-cells are related by the strong naturality isomorphism;
* transported 2-cells satisfy the exact strong-naturality square;
* every observable invariant under those coherent equivalences has the same
  value for either normalization;
* invertibility of transported intrinsic 2-cells is independent of the chosen
  normal representative, because every hom functor is an equivalence and
  therefore reflects isomorphisms.

Thus literal equality of two normal presentations is neither required nor
claimed. The invariant lives modulo coherent bicategorical equivalence.
-/

/-! ## Explicit normalization existence interface -/

/--
A chosen strictly-unitary normalization of a general bicategorical model
equivalence.

The strong transformation points from the normalized representative to the
original pseudofunctor. Requiring every object component to be an intrinsic
adjoint equivalence makes this a genuine model comparison rather than an
arbitrary transformation.
-/
structure StrictlyUnitaryNormalizationCertificate
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : BicategoricalModelEquivalence B C) where
  normal : StrictlyUnitaryBicategoricalModelEquivalence B C
  comparison :
    CategoryTheory.Oplax.StrongTrans
      normal.forward.toPseudofunctor.toOplax
      E.forward.toOplax
  object_component_equivalence :
    ∀ X : B, IntrinsicEquivalenceOneCell (comparison.app X)

/-! ## Comparison of two normal representatives -/

/--
A coherent comparison between two strictly-unitary choices for the same kind
of cross-model presentation.

This is the pinned-Mathlib replacement for the still-missing bundled notion of
an invertible icon between normal pseudofunctors: we use the native strong
transformation and separately require its object components to be adjoint
equivalences.
-/
structure NormalizationChoiceComparison
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E₁ E₂ : StrictlyUnitaryBicategoricalModelEquivalence B C) where
  strong :
    CategoryTheory.Oplax.StrongTrans
      E₁.forward.toPseudofunctor.toOplax
      E₂.forward.toPseudofunctor.toOplax
  object_component_equivalence :
    ∀ X : B, IntrinsicEquivalenceOneCell (strong.app X)

/-- The canonical strong-naturality isomorphism relating the two transported 1-cells. -/
def normalizationOneCellIso
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {E₁ E₂ : StrictlyUnitaryBicategoricalModelEquivalence B C}
    (K : NormalizationChoiceComparison E₁ E₂)
    {X Y : B}
    (f : X ⟶ Y) :
    E₁.forward.map f ≫ K.strong.app Y ≅
      K.strong.app X ≫ E₂.forward.map f :=
  K.strong.naturality f

/-- The two transported 2-cells satisfy the exact strong-naturality square. -/
theorem normalizationTwoCellNaturality
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {E₁ E₂ : StrictlyUnitaryBicategoricalModelEquivalence B C}
    (K : NormalizationChoiceComparison E₁ E₂)
    {X Y : B} {f g : X ⟶ Y}
    (α : f ⟶ g) :
    E₁.forward.map₂ α ▷ K.strong.app Y ≫
        (normalizationOneCellIso K g).hom =
      (normalizationOneCellIso K f).hom ≫
        K.strong.app X ◁ E₂.forward.map₂ α := by
  exact K.strong.naturality_naturality α

/-! ## Observables that descend through coherent equivalence -/

/--
A one-cell observable is normalization-invariant when equivalent changes of
source and target objects, together with an isomorphism of the corresponding
transported arrows, do not change its value.
-/
def CoherentOneCellObservable
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {Z : Sort z}
    (Φ : ∀ A B : C, (A ⟶ B) → Z) : Prop :=
  ∀ {A₁ A₂ B₁ B₂ : C}
    (u : A₁ ⟶ A₂) (v : B₁ ⟶ B₂)
    (_hu : IntrinsicEquivalenceOneCell u)
    (_hv : IntrinsicEquivalenceOneCell v)
    (f₁ : A₁ ⟶ B₁) (f₂ : A₂ ⟶ B₂),
      Nonempty (f₁ ≫ v ≅ u ≫ f₂) →
        Φ A₁ B₁ f₁ = Φ A₂ B₂ f₂

/-- Every coherent one-cell observable is independent of the normal representative. -/
theorem oneCellObservable_normalizationIndependent
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {E₁ E₂ : StrictlyUnitaryBicategoricalModelEquivalence B C}
    (K : NormalizationChoiceComparison E₁ E₂)
    {Z : Sort z}
    (Φ : ∀ A B : C, (A ⟶ B) → Z)
    (hΦ : CoherentOneCellObservable Φ)
    {X Y : B}
    (f : X ⟶ Y) :
    Φ (E₁.forward.obj X) (E₁.forward.obj Y) (E₁.forward.map f) =
      Φ (E₂.forward.obj X) (E₂.forward.obj Y) (E₂.forward.map f) := by
  exact hΦ
    (K.strong.app X) (K.strong.app Y)
    (K.object_component_equivalence X)
    (K.object_component_equivalence Y)
    (E₁.forward.map f) (E₂.forward.map f)
    ⟨normalizationOneCellIso K f⟩

/--
A two-cell observable is coherent when it is unchanged under equivalent
changes of endpoints and a commuting conjugacy square for the two 2-cells.
-/
def CoherentTwoCellObservable
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {Z : Sort z}
    (Φ : ∀ (A B : C) (f g : A ⟶ B), (f ⟶ g) → Z) : Prop :=
  ∀ {A₁ A₂ B₁ B₂ : C}
    (u : A₁ ⟶ A₂) (v : B₁ ⟶ B₂)
    (_hu : IntrinsicEquivalenceOneCell u)
    (_hv : IntrinsicEquivalenceOneCell v)
    (f₁ g₁ : A₁ ⟶ B₁) (f₂ g₂ : A₂ ⟶ B₂)
    (ιf : f₁ ≫ v ≅ u ≫ f₂)
    (ιg : g₁ ≫ v ≅ u ≫ g₂)
    (α₁ : f₁ ⟶ g₁) (α₂ : f₂ ⟶ g₂),
      α₁ ▷ v ≫ ιg.hom = ιf.hom ≫ u ◁ α₂ →
        Φ A₁ B₁ f₁ g₁ α₁ = Φ A₂ B₂ f₂ g₂ α₂

/-- Every coherent two-cell observable is independent of the normal representative. -/
theorem twoCellObservable_normalizationIndependent
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {E₁ E₂ : StrictlyUnitaryBicategoricalModelEquivalence B C}
    (K : NormalizationChoiceComparison E₁ E₂)
    {Z : Sort z}
    (Φ : ∀ (A B : C) (f g : A ⟶ B), (f ⟶ g) → Z)
    (hΦ : CoherentTwoCellObservable Φ)
    {X Y : B} {f g : X ⟶ Y}
    (α : f ⟶ g) :
    Φ (E₁.forward.obj X) (E₁.forward.obj Y)
        (E₁.forward.map f) (E₁.forward.map g) (E₁.forward.map₂ α) =
      Φ (E₂.forward.obj X) (E₂.forward.obj Y)
        (E₂.forward.map f) (E₂.forward.map g) (E₂.forward.map₂ α) := by
  exact hΦ
    (K.strong.app X) (K.strong.app Y)
    (K.object_component_equivalence X)
    (K.object_component_equivalence Y)
    (E₁.forward.map f) (E₁.forward.map g)
    (E₂.forward.map f) (E₂.forward.map g)
    (normalizationOneCellIso K f)
    (normalizationOneCellIso K g)
    (E₁.forward.map₂ α) (E₂.forward.map₂ α)
    (normalizationTwoCellNaturality K α)

/-! ## Invertibility is an intrinsic normalization-independent predicate -/

/-- A strictly-unitary model equivalence preserves and reflects 2-cell invertibility. -/
theorem transportedTwoCell_isIso_iff_source
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : StrictlyUnitaryBicategoricalModelEquivalence B C)
    {X Y : B} {f g : X ⟶ Y}
    (α : f ⟶ g) :
    IsIso (E.forward.map₂ α) ↔ IsIso α := by
  change
    IsIso ((E.forward.toPseudofunctor.toPrelaxFunctor.mapFunctor X Y).map α) ↔
      IsIso α
  rw [← E.homEquiv_functor X Y]
  exact isIso_iff_of_reflects_iso α (E.homEquiv X Y).functor

/-- Hence invertibility of the transported intrinsic 2-cell is independent of normalization choice. -/
theorem transportedTwoCell_invertibility_normalizationIndependent
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E₁ E₂ : StrictlyUnitaryBicategoricalModelEquivalence B C)
    {X Y : B} {f g : X ⟶ Y}
    (α : f ⟶ g) :
    IsIso (E₁.forward.map₂ α) ↔ IsIso (E₂.forward.map₂ α) := by
  exact (transportedTwoCell_isIso_iff_source E₁ α).trans
    (transportedTwoCell_isIso_iff_source E₂ α).symm

/-! ## Global Duskin consequences -/

/-- Direct global edge transports chosen by two normalizations are coherently isomorphic. -/
theorem transportedGlobalEdge_coherentlyEquivalent
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {E₁ E₂ : StrictlyUnitaryBicategoricalModelEquivalence B C}
    (K : NormalizationChoiceComparison E₁ E₂)
    (σ : DuskinSimplex B 1) :
    Nonempty
      (duskinEdgeArrow (transportDuskinSimplex E₁ σ) ≫
          K.strong.app (duskinEdgeTarget σ) ≅
        K.strong.app (duskinEdgeSource σ) ≫
          duskinEdgeArrow (transportDuskinSimplex E₂ σ)) := by
  change Nonempty
    (E₁.forward.map (duskinEdgeArrow σ) ≫ K.strong.app (duskinEdgeTarget σ) ≅
      K.strong.app (duskinEdgeSource σ) ≫ E₂.forward.map (duskinEdgeArrow σ))
  exact ⟨normalizationOneCellIso K (duskinEdgeArrow σ)⟩

/-- Every coherent observable of a transported global edge is normalization-independent. -/
theorem transportedGlobalEdgeObservable_normalizationIndependent
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {E₁ E₂ : StrictlyUnitaryBicategoricalModelEquivalence B C}
    (K : NormalizationChoiceComparison E₁ E₂)
    {Z : Sort z}
    (Φ : ∀ A B : C, (A ⟶ B) → Z)
    (hΦ : CoherentOneCellObservable Φ)
    (σ : DuskinSimplex B 1) :
    Φ (duskinEdgeSource (transportDuskinSimplex E₁ σ))
        (duskinEdgeTarget (transportDuskinSimplex E₁ σ))
        (duskinEdgeArrow (transportDuskinSimplex E₁ σ)) =
      Φ (duskinEdgeSource (transportDuskinSimplex E₂ σ))
        (duskinEdgeTarget (transportDuskinSimplex E₂ σ))
        (duskinEdgeArrow (transportDuskinSimplex E₂ σ)) := by
  change
    Φ (E₁.forward.obj (duskinEdgeSource σ))
        (E₁.forward.obj (duskinEdgeTarget σ))
        (E₁.forward.map (duskinEdgeArrow σ)) =
      Φ (E₂.forward.obj (duskinEdgeSource σ))
        (E₂.forward.obj (duskinEdgeTarget σ))
        (E₂.forward.map (duskinEdgeArrow σ))
  exact oneCellObservable_normalizationIndependent K Φ hΦ (duskinEdgeArrow σ)

/-- Invertibility of the intrinsically transported Duskin comparison is independent of normalization. -/
theorem transportedIntrinsicComparisonInvertibility_normalizationIndependent
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E₁ E₂ : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (σ : DuskinSimplex B 2) :
    IsIso (E₁.forward.map₂ (duskinComparison σ)) ↔
      IsIso (E₂.forward.map₂ (duskinComparison σ)) := by
  exact transportedTwoCell_invertibility_normalizationIndependent
    E₁ E₂ (duskinComparison σ)

/--
Every coherent observable of the intrinsic transported comparison 2-cell is
normalization-independent. The actual target global comparison then differs
from this intrinsic cell only by the canonical `mapComp` coherence already
isolated in v1.27.
-/
theorem transportedIntrinsicComparisonObservable_normalizationIndependent
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {E₁ E₂ : StrictlyUnitaryBicategoricalModelEquivalence B C}
    (K : NormalizationChoiceComparison E₁ E₂)
    {Z : Sort z}
    (Φ : ∀ (A B : C) (f g : A ⟶ B), (f ⟶ g) → Z)
    (hΦ : CoherentTwoCellObservable Φ)
    (σ : DuskinSimplex B 2) :
    Φ (E₁.forward.obj (duskinTriangleSource σ))
        (E₁.forward.obj (duskinTriangleTarget σ))
        (E₁.forward.map (duskinTriangleCompositeArrow σ))
        (E₁.forward.map (duskinTriangleLongArrow σ))
        (E₁.forward.map₂ (duskinComparison σ)) =
      Φ (E₂.forward.obj (duskinTriangleSource σ))
        (E₂.forward.obj (duskinTriangleTarget σ))
        (E₂.forward.map (duskinTriangleCompositeArrow σ))
        (E₂.forward.map (duskinTriangleLongArrow σ))
        (E₂.forward.map₂ (duskinComparison σ)) := by
  exact twoCellObservable_normalizationIndependent K Φ hΦ (duskinComparison σ)

/-! ## Bundled normalization-choice invariant kernel -/

/--
The theorem-level content showing that a strong comparison removes the chosen
normal representative from the presentation-independent invariant.
-/
structure NormalizationChoiceInvariantKernel
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {E₁ E₂ : StrictlyUnitaryBicategoricalModelEquivalence B C}
    (K : NormalizationChoiceComparison E₁ E₂) : Prop where
  one_cell_coherence :
    ∀ {X Y : B} (f : X ⟶ Y),
      Nonempty
        (E₁.forward.map f ≫ K.strong.app Y ≅
          K.strong.app X ≫ E₂.forward.map f)
  two_cell_coherence :
    ∀ {X Y : B} {f g : X ⟶ Y} (α : f ⟶ g),
      E₁.forward.map₂ α ▷ K.strong.app Y ≫
          (normalizationOneCellIso K g).hom =
        (normalizationOneCellIso K f).hom ≫
          K.strong.app X ◁ E₂.forward.map₂ α
  two_cell_invertibility :
    ∀ {X Y : B} {f g : X ⟶ Y} (α : f ⟶ g),
      IsIso (E₁.forward.map₂ α) ↔ IsIso (E₂.forward.map₂ α)

/-- Every explicit strong comparison yields the normalization-choice invariant kernel. -/
def normalizationChoiceInvariantKernel
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {E₁ E₂ : StrictlyUnitaryBicategoricalModelEquivalence B C}
    (K : NormalizationChoiceComparison E₁ E₂) :
    NormalizationChoiceInvariantKernel K where
  one_cell_coherence := by
    intro X Y f
    exact ⟨normalizationOneCellIso K f⟩
  two_cell_coherence := by
    intro X Y f g α
    exact normalizationTwoCellNaturality K α
  two_cell_invertibility := by
    intro X Y f g α
    exact transportedTwoCell_invertibility_normalizationIndependent E₁ E₂ α

/-!
The formal boundary after v1.28 is now precise:

```text
general model equivalence E
  + StrictlyUnitaryNormalizationCertificate E
  -> a chosen normal representative with direct global Duskin transport

normal representatives E₁, E₂
  + NormalizationChoiceComparison E₁ E₂
  -> coherent 1-cell correspondence
  -> coherent 2-cell naturality square
  -> every coherent observable agrees
  -> transported intrinsic IsIso predicates agree
```

Still not claimed:

* existence of a strictly-unitary normalization for every pseudofunctorial
  biequivalence in the pinned Mathlib revision;
* automatic construction of `NormalizationChoiceComparison` between arbitrary
  normalization certificates;
* a bundled Mathlib `Icon` at this pinned revision;
* full scaled-horn/filler transport or equivalence of the complete global
  `(∞,2)` models.

Those are now cleanly separated from the presentation-independent invariant
itself.
-/

end KUOS.DependentOriginationNormalizationChoiceInvariantV1_28