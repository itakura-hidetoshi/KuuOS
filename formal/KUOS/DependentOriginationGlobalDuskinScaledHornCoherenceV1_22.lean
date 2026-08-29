import KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21

namespace KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Bicategory
open Simplicial
open Opposite
open scoped Bicategory
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationCompleteSegalInfinityTwoV1_20
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21

universe u v w

/-!
# Global Duskin scaled-horn coherence kernel v1.22

The v1.21 global Duskin nerve gives a single simplicial carrier together with
its thin 2-simplices.  The next mathematical step is to separate two issues
that must not be conflated:

1. low-dimensional coherence already forced by a normal lax `[n] -> B`
   simplex;
2. a scaled-anodyne / scaled-horn *fibrancy* theorem, which requires a precise
   choice of admissible scaled horn generators and is not automatic merely from
   the existence of a bicategory.

This file formalizes the first point completely in dimensions 2 and 3 and adds
an exact interface for the second point without claiming it unconditionally.

For every Duskin 3-simplex, the normal-lax associativity law is exposed as the
tetrahedral equality comparing the two composites of its three principal
edges.  For every Duskin 1-simplex, the normal-lax left and right unit laws are
exposed explicitly.  Thinness of invertible comparison triangles is inherited
from v1.21.

In parallel, `ScaledHornExtensionProblem` packages a horn map together with
scalings on the horn and simplex and the requirement that the horn inclusion
and horn map preserve thin 2-simplices.  A separate `ScaledHornFamily` chooses
which such problems are the admissible generators.  Thus a future standard
scaled-anodyne presentation can be inserted without changing the parent
contextual-transport definition or overclaiming current Mathlib support.
-/

/-! ## Scaled maps and scaled horn extension problems -/

/-- A simplicial map is scaled when it sends every thin 2-simplex to a thin 2-simplex. -/
def IsScaledMap
    {X Y : SSet}
    (sX : ScaledSimplicialSet X)
    (sY : ScaledSimplicialSet Y)
    (f : X ⟶ Y) : Prop :=
  ∀ t : X.obj (op ⦋2⦌), sX.thin t → sY.thin (f.app (op ⦋2⦌) t)

/-- Identity maps preserve every scaling. -/
theorem isScaledMap_id
    {X : SSet} (sX : ScaledSimplicialSet X) :
    IsScaledMap sX sX (𝟙 X) := by
  intro t ht
  simpa using ht

/-- Scaled maps are closed under simplicial composition. -/
theorem IsScaledMap.comp
    {X Y Z : SSet}
    {sX : ScaledSimplicialSet X}
    {sY : ScaledSimplicialSet Y}
    {sZ : ScaledSimplicialSet Z}
    {f : X ⟶ Y} {g : Y ⟶ Z}
    (hf : IsScaledMap sX sY f)
    (hg : IsScaledMap sY sZ g) :
    IsScaledMap sX sZ (f ≫ g) := by
  intro t ht
  exact hg _ (hf _ ht)

/--
A scaled horn-extension problem in a target scaled simplicial set.

The horn and the ambient simplex carry explicit scalings.  The horn inclusion
must preserve thin triangles, and the prescribed horn map must preserve thin
triangles into the target.  No particular scaled-anodyne generating family is
hard-coded here.
-/
structure ScaledHornExtensionProblem
    (X : SSet) (sX : ScaledSimplicialSet X)
    (n : Nat) (i : Fin (n + 1)) where
  hornScaling : ScaledSimplicialSet (Λ[n, i] : SSet)
  simplexScaling : ScaledSimplicialSet (Δ[n] : SSet)
  inclusion_scaled :
    IsScaledMap hornScaling simplexScaling Λ[n, i].ι
  hornMap : (Λ[n, i] : SSet) ⟶ X
  hornMap_scaled : IsScaledMap hornScaling sX hornMap

/-- A scaled filler extends the horn map and is itself a scaled simplicial map. -/
structure ScaledHornFiller
    {X : SSet} {sX : ScaledSimplicialSet X}
    {n : Nat} {i : Fin (n + 1)}
    (P : ScaledHornExtensionProblem X sX n i) where
  simplexMap : Δ[n] ⟶ X
  extends_horn : P.hornMap = Λ[n, i].ι ≫ simplexMap
  simplexMap_scaled : IsScaledMap P.simplexScaling sX simplexMap

/--
An explicit family of admissible scaled horn problems.

This is the slot in which the standard scaled-anodyne generators, or any other
chosen presentation, must eventually be supplied.  Keeping the family explicit
prevents a generic bicategory from being silently promoted to a fibrant
`(infinity,2)` model.
-/
structure ScaledHornFamily
    (X : SSet) (sX : ScaledSimplicialSet X) where
  admissible :
    ∀ {n : Nat} {i : Fin (n + 1)},
      ScaledHornExtensionProblem X sX n i → Prop

/-- A scaled simplicial set fills every inner horn selected by a given family. -/
class HasScaledHornFillers
    (X : SSet) (sX : ScaledSimplicialSet X)
    (F : ScaledHornFamily X sX) : Prop where
  fill :
    ∀ {n : Nat} {i : Fin (n + 1)}
      (P : ScaledHornExtensionProblem X sX n i),
      F.admissible P →
      0 < i → i < Fin.last n →
      Nonempty (ScaledHornFiller P)

/-- The global Duskin scaled nerve is the target of the future admissible horn family. -/
abbrev GlobalDuskinScaledHornFamily
    (B : Type u) [Bicategory.{w, v} B] :=
  ScaledHornFamily (duskinNerve B) (duskinScaling B)

/-! ## Principal edges in dimensions one and three -/

/-- The unique nonidentity principal edge `0 -> 1` in `[1]`. -/
def edge01One :
    LocallyDiscrete.mk (0 : Fin 2) ⟶ LocallyDiscrete.mk (1 : Fin 2) :=
  (homOfLE (by decide) : (0 : Fin 2) ⟶ (1 : Fin 2)).toLoc

/-- The principal edge `0 -> 1` in `[3]`. -/
def edge01Three :
    LocallyDiscrete.mk (0 : Fin 4) ⟶ LocallyDiscrete.mk (1 : Fin 4) :=
  (homOfLE (by decide) : (0 : Fin 4) ⟶ (1 : Fin 4)).toLoc

/-- The principal edge `1 -> 2` in `[3]`. -/
def edge12Three :
    LocallyDiscrete.mk (1 : Fin 4) ⟶ LocallyDiscrete.mk (2 : Fin 4) :=
  (homOfLE (by decide) : (1 : Fin 4) ⟶ (2 : Fin 4)).toLoc

/-- The principal edge `2 -> 3` in `[3]`. -/
def edge23Three :
    LocallyDiscrete.mk (2 : Fin 4) ⟶ LocallyDiscrete.mk (3 : Fin 4) :=
  (homOfLE (by decide) : (2 : Fin 4) ⟶ (3 : Fin 4)).toLoc

/-! ## Tetrahedral associativity coherence -/

/--
The 3-simplex tetrahedron equation: the two ways to compare the image of a
threefold composite agree after the target bicategory associator is inserted.
-/
def SatisfiesDuskinAssociativityTetrahedron
    {B : Type u} [Bicategory.{w, v} B]
    (σ : DuskinSimplex B 3) : Prop :=
  σ.mapComp edge01Three edge12Three ▷ σ.map edge23Three ≫
      σ.mapComp (edge01Three ≫ edge12Three) edge23Three ≫
      σ.map₂ (α_ edge01Three edge12Three edge23Three).hom =
    (α_ (σ.map edge01Three) (σ.map edge12Three) (σ.map edge23Three)).hom ≫
      σ.map edge01Three ◁ σ.mapComp edge12Three edge23Three ≫
      σ.mapComp edge01Three (edge12Three ≫ edge23Three)

/-- Every global Duskin 3-simplex satisfies the tetrahedral associativity law. -/
theorem duskinAssociativityTetrahedron
    {B : Type u} [Bicategory.{w, v} B]
    (σ : DuskinSimplex B 3) :
    SatisfiesDuskinAssociativityTetrahedron σ := by
  exact σ.map₂_associator edge01Three edge12Three edge23Three

/-! ## Unitary coherence on global Duskin edges -/

/-- The left-unit coherence equation carried by a Duskin 1-simplex. -/
def SatisfiesDuskinLeftUnit
    {B : Type u} [Bicategory.{w, v} B]
    (σ : DuskinSimplex B 1) : Prop :=
  σ.map₂ (λ_ edge01One).inv =
    (λ_ (σ.map edge01One)).inv ≫
      σ.mapId (LocallyDiscrete.mk (0 : Fin 2)) ▷ σ.map edge01One ≫
      σ.mapComp (𝟙 (LocallyDiscrete.mk (0 : Fin 2))) edge01One

/-- Every global Duskin edge satisfies the normal-lax left-unit equation. -/
theorem duskinLeftUnitCoherence
    {B : Type u} [Bicategory.{w, v} B]
    (σ : DuskinSimplex B 1) :
    SatisfiesDuskinLeftUnit σ := by
  exact σ.map₂_leftUnitor edge01One

/-- The right-unit coherence equation carried by a Duskin 1-simplex. -/
def SatisfiesDuskinRightUnit
    {B : Type u} [Bicategory.{w, v} B]
    (σ : DuskinSimplex B 1) : Prop :=
  σ.map₂ (ρ_ edge01One).inv =
    (ρ_ (σ.map edge01One)).inv ≫
      σ.map edge01One ◁ σ.mapId (LocallyDiscrete.mk (1 : Fin 2)) ≫
      σ.mapComp edge01One (𝟙 (LocallyDiscrete.mk (1 : Fin 2)))

/-- Every global Duskin edge satisfies the normal-lax right-unit equation. -/
theorem duskinRightUnitCoherence
    {B : Type u} [Bicategory.{w, v} B]
    (σ : DuskinSimplex B 1) :
    SatisfiesDuskinRightUnit σ := by
  exact σ.map₂_rightUnitor edge01One

/-! ## Canonical low-dimensional coherence certificate -/

/--
The low-dimensional global scaled-Duskin coherence forced by the bicategory and
normal-lax simplex laws.  This is a theorem-level certificate, not a fibrancy
axiom.
-/
structure GlobalDuskinLowDimensionalCoherence
    (B : Type u) [Bicategory.{w, v} B] : Prop where
  associativity_tetrahedron :
    ∀ σ : DuskinSimplex B 3,
      SatisfiesDuskinAssociativityTetrahedron σ
  left_unit :
    ∀ σ : DuskinSimplex B 1,
      SatisfiesDuskinLeftUnit σ
  right_unit :
    ∀ σ : DuskinSimplex B 1,
      SatisfiesDuskinRightUnit σ
  invertible_comparison_thin :
    ∀ σ : (duskinNerve B).obj (op ⦋2⦌),
      IsIso (duskinComparison σ) →
      (duskinScaling B).thin σ

/-- Every bicategory has the canonical low-dimensional global Duskin coherence certificate. -/
def globalDuskinLowDimensionalCoherence
    (B : Type u) [Bicategory.{w, v} B] :
    GlobalDuskinLowDimensionalCoherence B where
  associativity_tetrahedron := duskinAssociativityTetrahedron
  left_unit := duskinLeftUnitCoherence
  right_unit := duskinRightUnitCoherence
  invertible_comparison_thin := by
    intro σ h
    letI : IsIso (duskinComparison σ) := h
    exact invertibleComparison_isThin σ

/-! ## Conditional bridge to the v1.20 complete-Segal certificate -/

/--
A global complete-Duskin certificate records two genuinely additional inputs:

* a chosen admissible scaled-horn family with fillers;
* object univalence / Rezk completeness.

The low-dimensional Duskin coherence itself is automatic and therefore need
not be repeated as an assumption.
-/
structure GlobalCompleteDuskinCertificate
    (B : Type u) [Bicategory.{w, v} B]
    (F : GlobalDuskinScaledHornFamily B) where
  horn_fillers :
    HasScaledHornFillers (duskinNerve B) (duskinScaling B) F
  object_univalence : ObjectUnivalence B

/--
A global complete-Duskin certificate canonically supplies the existing local
complete-Segal certificate through its explicit object-univalence field.

This is intentionally a one-way implication.  No equivalence between the local
2-Yoneda presentation and the global scaled Duskin presentation is asserted
without a separate local/global mapping-object comparison theorem.
-/
def completeSegalOfGlobalCompleteDuskin
    {B : Type u} [Bicategory.{w, v} B]
    {F : GlobalDuskinScaledHornFamily B}
    (h : GlobalCompleteDuskinCertificate B F) :
    CompleteSegalInfinityTwoCategory B :=
  completeSegalOfObjectUnivalence h.object_univalence

/-!
The proved / unproved boundary after v1.22 is therefore:

```text
Bicategory B
  -> global scaled Duskin nerve                         -- v1.21
  -> thin invertible composition triangles             -- v1.21
  -> associativity tetrahedron + left/right unit laws  -- v1.22, proved

Chosen admissible scaled-horn family F
  + HasScaledHornFillers N_Duskin(B) F                 -- explicit extra certificate
  + ObjectUnivalence B                                 -- explicit extra certificate
  -> local CompleteSegalInfinityTwoCategory B          -- proved one-way bridge
```

Still not claimed:

* that the global Duskin nerve satisfies a particular standard scaled-anodyne
  fibrancy presentation before its generator family is formalized;
* that its global mapping objects are already identified with
  `mappingNerve X Y`;
* that the local complete-Segal and global scaled-Duskin presentations are
  equivalent without those comparison data.
-/

end KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22