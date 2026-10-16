import KUOS.DependentOriginationBiequivalencePresentationInvariantV1_26
import Mathlib.CategoryTheory.Bicategory.Functor.StrictlyUnitary

namespace KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Bicategory
open Simplicial
open Opposite
open scoped Bicategory
open KUOS.DependentOriginationInfinityTwoYonedaV1_18
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationGlobalDuskinLocalMappingComparisonV1_23
open KUOS.DependentOriginationGlobalDuskinLocalTwoCellComparisonV1_24
open KUOS.DependentOriginationPresentationIndependentInvariantV1_25
open KUOS.DependentOriginationBiequivalencePresentationInvariantV1_26

universe u₁ u₂ v₁ v₂ w₁ w₂

/-!
# Strictly-unitary global Duskin transport v1.27

Version 1.26 proved that the presentation-independent invariant already
transports across Whitehead-style bicategorical model-equivalence data without
requiring a direct map between global Duskin nerves.

The remaining obstruction to direct global-to-global transport is precise:
`DuskinSimplex` is a `StrictlyUnitaryLaxFunctor`, while a general
`Pseudofunctor` need not be strictly unitary.  The pinned Mathlib revision
provides native `StrictlyUnitaryPseudofunctor` and its conversion to
`StrictlyUnitaryLaxFunctor`, but does not provide an automatic normalization
constructor for arbitrary pseudofunctors.

Accordingly this layer does not hide a missing strictification theorem.  It
introduces the stronger, explicit certificate that the chosen model equivalence
is already presented by a strictly-unitary pseudofunctor.  From that data the
global transport is completely automatic:

```text
[n] --σ--> B --F_normal--> C
```

is again a normal lax `[n] -> C` simplex.  Postcomposition commutes with every
simplicial reindexing operator, hence gives a genuine simplicial map between the
two global Duskin nerves in every degree.

The transported comparison 2-cell is not merely `F.map₂` of the old comparison:
pseudofunctorial composition contributes its canonical composition constraint.
The exact formula is

```text
F(f) ≫ F(g)
  --(mapComp f g)⁻¹--> F(f ≫ g)
  --F₂(comparison)--> F(long edge).
```

Thus direct global transport and the v1.26 intrinsic transport agree after the
unique coherence correction forced by pseudofunctoriality.  Invertible source
comparison cells remain invertible, so nondegenerate thin triangles transport
to thin target triangles.
-/

/-! ## Strictly-unitary model-equivalence certificate -/

/--
A Whitehead-style bicategorical model equivalence whose forward map is already
strictly unitary.

This is deliberately stronger than `BicategoricalModelEquivalence`.  The
remaining normalization problem is exactly the construction of such a
certificate from suitable general biequivalence data.
-/
structure StrictlyUnitaryBicategoricalModelEquivalence
    (B : Type u₁) [Bicategory.{w₁, v₁} B]
    (C : Type u₂) [Bicategory.{w₂, v₂} C] where
  forward : StrictlyUnitaryPseudofunctor B C
  homEquiv :
    ∀ X Y : B,
      (X ⟶ Y) ≌ (forward.obj X ⟶ forward.obj Y)
  homEquiv_functor :
    ∀ X Y : B,
      (homEquiv X Y).functor =
        forward.toPseudofunctor.toPrelaxFunctor.mapFunctor X Y
  object_essentially_surjective :
    ∀ Z : C,
      ∃ X : B, IntrinsicObjectEquivalent (forward.obj X) Z

namespace StrictlyUnitaryBicategoricalModelEquivalence

variable
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : StrictlyUnitaryBicategoricalModelEquivalence B C)

/-- Forget strict unitarity and recover the v1.26 model-equivalence certificate. -/
def toModelEquivalence : BicategoricalModelEquivalence B C where
  forward := E.forward.toPseudofunctor
  homEquiv := E.homEquiv
  homEquiv_functor := E.homEquiv_functor
  object_essentially_surjective := E.object_essentially_surjective

@[simp] theorem toModelEquivalence_forward :
    E.toModelEquivalence.forward = E.forward.toPseudofunctor :=
  rfl

end StrictlyUnitaryBicategoricalModelEquivalence

/-! ## Direct transport of every global Duskin simplex -/

/--
Postcompose a global Duskin simplex with the strictly-unitary forward
pseudofunctor.  The result is again a global Duskin simplex in every degree.
-/
def transportDuskinSimplex
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : StrictlyUnitaryBicategoricalModelEquivalence B C)
    {n : Nat}
    (σ : DuskinSimplex B n) :
    DuskinSimplex C n :=
  σ.comp E.forward.toStrictlyUnitaryLaxFunctor

@[simp] theorem transportDuskinSimplex_obj
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : StrictlyUnitaryBicategoricalModelEquivalence B C)
    {n : Nat}
    (σ : DuskinSimplex B n)
    (i : DuskinOrdinal n) :
    (transportDuskinSimplex E σ).obj i = E.forward.obj (σ.obj i) :=
  rfl

@[simp] theorem transportDuskinSimplex_map
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : StrictlyUnitaryBicategoricalModelEquivalence B C)
    {n : Nat}
    (σ : DuskinSimplex B n)
    {i j : DuskinOrdinal n}
    (f : i ⟶ j) :
    (transportDuskinSimplex E σ).map f = E.forward.map (σ.map f) :=
  rfl

@[simp] theorem transportDuskinSimplex_map₂
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : StrictlyUnitaryBicategoricalModelEquivalence B C)
    {n : Nat}
    (σ : DuskinSimplex B n)
    {i j : DuskinOrdinal n}
    {f g : i ⟶ j}
    (α : f ⟶ g) :
    (transportDuskinSimplex E σ).map₂ α = E.forward.map₂ (σ.map₂ α) :=
  rfl

/--
The comparison cell of the composite normal-lax functor is the target
composition constraint followed by the image of the source comparison cell.
-/
@[simp] theorem transportDuskinSimplex_mapComp
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : StrictlyUnitaryBicategoricalModelEquivalence B C)
    {n : Nat}
    (σ : DuskinSimplex B n)
    {i j k : DuskinOrdinal n}
    (f : i ⟶ j) (g : j ⟶ k) :
    (transportDuskinSimplex E σ).mapComp f g =
      (E.forward.mapComp (σ.map f) (σ.map g)).inv ≫
        E.forward.map₂ (σ.mapComp f g) :=
  rfl

/-! ## Simplicial naturality -/

/-- Postcomposition with the normalized forward map commutes with every Duskin reindexing. -/
theorem transportDuskinSimplex_reindex
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : StrictlyUnitaryBicategoricalModelEquivalence B C)
    {Δ Δ' : SimplexCategoryᵒᵖ}
    (f : Δ ⟶ Δ')
    (σ : (duskinNerve B).obj Δ) :
    transportDuskinSimplex E ((duskinReindex f).comp σ) =
      (duskinReindex f).comp (transportDuskinSimplex E σ) := by
  exact StrictlyUnitaryLaxFunctor.comp_assoc
    (duskinReindex f) σ E.forward.toStrictlyUnitaryLaxFunctor

/-- A normalized model equivalence induces a genuine simplicial map of global Duskin nerves. -/
def normalizedDuskinNerveMap
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : StrictlyUnitaryBicategoricalModelEquivalence B C) :
    duskinNerve B ⟶ duskinNerve C where
  app Δ := TypeCat.ofHom fun σ => transportDuskinSimplex E σ
  naturality f := by
    ext σ
    change
      transportDuskinSimplex E ((duskinReindex f).comp σ) =
        (duskinReindex f).comp (transportDuskinSimplex E σ)
    exact transportDuskinSimplex_reindex E f σ

@[simp] theorem normalizedDuskinNerveMap_app
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (Δ : SimplexCategoryᵒᵖ)
    (σ : (duskinNerve B).obj Δ) :
    (normalizedDuskinNerveMap E).app Δ σ = transportDuskinSimplex E σ :=
  rfl

/-! ## Compatibility with the presentation-independent invariant -/

/-- On global 1-simplices, direct global transport is exactly intrinsic one-cell transport. -/
@[simp] theorem transportDuskinEdge_intrinsicInvariant
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (σ : DuskinSimplex B 1) :
    duskinEdgeArrow (transportDuskinSimplex E σ) =
      transportIntrinsicOneCell E.toModelEquivalence (duskinEdgeArrow σ) :=
  rfl

/--
The target global Duskin comparison factors through the v1.26 intrinsic
transport, preceded only by the canonical pseudofunctor composition constraint.
-/
@[simp] theorem transportDuskinComparison_intrinsicFactorization
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (σ : DuskinSimplex B 2) :
    duskinComparison (transportDuskinSimplex E σ) =
      (E.forward.mapComp (σ.map edge01) (σ.map edge12)).inv ≫
        transportIntrinsicTwoCell E.toModelEquivalence
          (globalTwoCellInvariant σ) :=
  rfl

/-- The same factorization written directly in native pseudofunctor operations. -/
@[simp] theorem transportDuskinComparison
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (σ : DuskinSimplex B 2) :
    duskinComparison (transportDuskinSimplex E σ) =
      (E.forward.mapComp (σ.map edge01) (σ.map edge12)).inv ≫
        E.forward.map₂ (duskinComparison σ) :=
  rfl

/-! ## Invertibility and scaling transport -/

/-- Invertibility of a source comparison cell is preserved by direct normalized global transport. -/
theorem transportDuskinComparison_isIso
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (σ : DuskinSimplex B 2)
    (hiso : IsIso (duskinComparison σ)) :
    IsIso (duskinComparison (transportDuskinSimplex E σ)) := by
  letI : IsIso (duskinComparison σ) := hiso
  rw [transportDuskinComparison]
  infer_instance

/-- Every nondegenerate source-thin triangle transports to a target-thin triangle. -/
theorem nondegenerateThin_transport_isThin
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (σ : DuskinSimplex B 2)
    (hnd : ¬ IsDegenerateDuskinTwoSimplex σ)
    (hthin : (duskinScaling B).thin σ) :
    (duskinScaling C).thin (transportDuskinSimplex E σ) := by
  have hiso : IntrinsicInvertibleTwoCell (globalTwoCellInvariant σ) :=
    (nondegenerate_globalThin_iff_intrinsicInvertible σ hnd).mp hthin
  change IsIso (duskinComparison σ) at hiso
  letI : IsIso (duskinComparison σ) := hiso
  haveI : IsIso (duskinComparison (transportDuskinSimplex E σ)) := by
    rw [transportDuskinComparison]
    infer_instance
  exact invertibleComparison_isThin (transportDuskinSimplex E σ)

/-! ## Bundled theorem-level certificate -/

/--
The direct global presentation transport supplied by any strictly-unitary model
equivalence.
-/
structure StrictlyUnitaryGlobalDuskinTransportCertificate
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : StrictlyUnitaryBicategoricalModelEquivalence B C) : Prop where
  reindex_commutes :
    ∀ {Δ Δ' : SimplexCategoryᵒᵖ}
      (f : Δ ⟶ Δ') (σ : (duskinNerve B).obj Δ),
      transportDuskinSimplex E ((duskinReindex f).comp σ) =
        (duskinReindex f).comp (transportDuskinSimplex E σ)
  edge_intrinsic_exact :
    ∀ σ : DuskinSimplex B 1,
      duskinEdgeArrow (transportDuskinSimplex E σ) =
        transportIntrinsicOneCell E.toModelEquivalence (duskinEdgeArrow σ)
  comparison_intrinsic_factorization :
    ∀ σ : DuskinSimplex B 2,
      duskinComparison (transportDuskinSimplex E σ) =
        (E.forward.mapComp (σ.map edge01) (σ.map edge12)).inv ≫
          transportIntrinsicTwoCell E.toModelEquivalence
            (globalTwoCellInvariant σ)
  nondegenerate_thin_preserved :
    ∀ σ : DuskinSimplex B 2,
      ¬ IsDegenerateDuskinTwoSimplex σ →
      (duskinScaling B).thin σ →
      (duskinScaling C).thin (transportDuskinSimplex E σ)

/-- Every strictly-unitary bicategorical model equivalence has the global transport certificate. -/
def strictlyUnitaryGlobalDuskinTransportCertificate
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : StrictlyUnitaryBicategoricalModelEquivalence B C) :
    StrictlyUnitaryGlobalDuskinTransportCertificate E where
  reindex_commutes := transportDuskinSimplex_reindex E
  edge_intrinsic_exact := transportDuskinEdge_intrinsicInvariant E
  comparison_intrinsic_factorization :=
    transportDuskinComparison_intrinsicFactorization E
  nondegenerate_thin_preserved := nondegenerateThin_transport_isThin E

/-!
The v1.27 boundary is therefore:

```text
StrictlyUnitaryBicategoricalModelEquivalence B C
  -> v1.26 BicategoricalModelEquivalence B C
  -> direct global Duskin simplex transport in every degree
  -> simplicial map N_Duskin(B) -> N_Duskin(C)
  -> exact intrinsic 1-cell transport on global edges
  -> comparison = composition coherence ; transported intrinsic 2-cell
  -> nondegenerate thin triangles remain thin
```

What remains genuinely open is now sharper than before:

* construct a strictly-unitary normalization of sufficiently general
  pseudofunctorial biequivalence data;
* prove independence of the chosen normalization when more than one normal
  representative exists;
* upgrade the nondegenerate thinness theorem to a fully bundled scaled map,
  including degeneracy preservation through the simplicial map;
* compare horn-filler families under normalized model equivalence.

The presentation-independent invariant itself no longer depends on solving
those presentation-normalization questions.
-/

end KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27
