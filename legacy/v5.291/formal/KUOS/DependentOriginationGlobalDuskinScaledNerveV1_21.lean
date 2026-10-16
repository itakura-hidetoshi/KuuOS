import Mathlib.AlgebraicTopology.SimplicialSet.Nerve
import Mathlib.CategoryTheory.Bicategory.Functor.LocallyDiscrete
import Mathlib.CategoryTheory.Bicategory.Functor.StrictlyUnitary
import KUOS.DependentOriginationCompleteSegalInfinityTwoV1_20

namespace KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Bicategory
open Simplicial
open Opposite
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19

universe u v w

/-!
# Global Duskin / scaled nerve v1.21

The pinned Mathlib revision already contains the exact normal-lax carrier
needed for the Duskin nerve, namely `StrictlyUnitaryLaxFunctor`, but its own
TODO list explicitly leaves construction of the Duskin nerve unfinished.
This file closes that gap at the KuuOS dependent-origination boundary.

For a bicategory `B`, the `n`-simplices are normal lax functors

```text
LocallyDiscrete (Fin (n+1)) -> B.
```

Simplicial operators act by precomposition with the induced monotone functor
between finite ordinals.  The strict unit and associativity laws already
proved for composition of normal lax functors supply the simplicial laws.

The global scaling is carried by the same simplicial set.  A nondegenerate
2-simplex is declared thin when its lax comparison 2-cell is invertible;
degenerate 2-simplices are included explicitly, as required by the definition
of a scaled simplicial set.
-/

/-- The finite ordinal `[n]` viewed as a locally discrete bicategory. -/
abbrev DuskinOrdinal (n : Nat) := LocallyDiscrete (Fin (n + 1))

/-- A Duskin `n`-simplex: a normal lax functor `[n] -> B`. -/
abbrev DuskinSimplex
    (B : Type u) [Bicategory.{w, v} B] (n : Nat) :=
  StrictlyUnitaryLaxFunctor (DuskinOrdinal n) B

/--
Lift an ordinary functor to a normal lax functor between the corresponding
locally discrete bicategories.
-/
def locallyDiscreteNormalLax
    {C : Type*} {D : Type*} [Category C] [Category D]
    (F : C ⥤ D) :
    StrictlyUnitaryLaxFunctor (LocallyDiscrete C) (LocallyDiscrete D) where
  __ := F.toPseudofunctor.toLax
  map_id := by
    intro X
    rcases X with ⟨X⟩
    simp
  mapId_eq_eqToHom := by
    intro X
    rcases X with ⟨X⟩
    simp

attribute [local ext] StrictlyUnitaryLaxFunctor

set_option backward.isDefEq.respectTransparency false in
@[simp] theorem locallyDiscreteNormalLax_id
    (C : Type*) [Category C] :
    locallyDiscreteNormalLax (Functor.id C) =
      StrictlyUnitaryLaxFunctor.id (LocallyDiscrete C) := by
  ext
  · simp [locallyDiscreteNormalLax]
  all_goals
    · rw [heq_iff_eq]
      ext
      simp [locallyDiscreteNormalLax]

set_option backward.isDefEq.respectTransparency false in
@[simp] theorem locallyDiscreteNormalLax_comp
    {C : Type*} {D : Type*} {E : Type*}
    [Category C] [Category D] [Category E]
    (F : C ⥤ D) (G : D ⥤ E) :
    locallyDiscreteNormalLax (F ⋙ G) =
      (locallyDiscreteNormalLax F).comp (locallyDiscreteNormalLax G) := by
  ext
  · simp [locallyDiscreteNormalLax]
  all_goals
    · rw [heq_iff_eq]
      ext
      simp [locallyDiscreteNormalLax]

/-- The normal-lax reindexing functor associated to a simplicial operator. -/
def duskinReindex
    {Δ Δ' : SimplexCategoryᵒᵖ} (f : Δ ⟶ Δ') :
    StrictlyUnitaryLaxFunctor
      (DuskinOrdinal Δ'.unop.len)
      (DuskinOrdinal Δ.unop.len) :=
  locallyDiscreteNormalLax (SimplexCategory.toCat.map f.unop).toFunctor

set_option backward.isDefEq.respectTransparency false in
@[simp] theorem duskinReindex_id (Δ : SimplexCategoryᵒᵖ) :
    duskinReindex (𝟙 Δ) =
      StrictlyUnitaryLaxFunctor.id (DuskinOrdinal Δ.unop.len) := by
  simp [duskinReindex]

set_option backward.isDefEq.respectTransparency false in
@[simp] theorem duskinReindex_comp
    {Δ₀ Δ₁ Δ₂ : SimplexCategoryᵒᵖ}
    (f : Δ₀ ⟶ Δ₁) (g : Δ₁ ⟶ Δ₂) :
    duskinReindex (f ≫ g) =
      (duskinReindex g).comp (duskinReindex f) := by
  simp [duskinReindex, Functor.comp_def]

/--
The global Duskin nerve of a bicategory.

Its simplices are normal lax functors out of finite ordinals, not merely
collections of local mapping nerves.
-/
def duskinNerve (B : Type u) [Bicategory.{w, v} B] : SSet where
  obj Δ := DuskinSimplex B Δ.unop.len
  map f := TypeCat.ofHom fun σ => (duskinReindex f).comp σ
  map_id Δ := by
    ext σ
    change (duskinReindex (𝟙 Δ)).comp σ = σ
    rw [duskinReindex_id]
    exact StrictlyUnitaryLaxFunctor.id_comp σ
  map_comp f g := by
    ext σ
    change (duskinReindex (f ≫ g)).comp σ =
      (duskinReindex g).comp ((duskinReindex f).comp σ)
    rw [duskinReindex_comp]
    exact StrictlyUnitaryLaxFunctor.comp_assoc _ _ _

/-- Every face/degeneracy action is literally normal-lax precomposition. -/
@[simp] theorem duskinNerve_map
    {B : Type u} [Bicategory.{w, v} B]
    {Δ Δ' : SimplexCategoryᵒᵖ} (f : Δ ⟶ Δ')
    (σ : (duskinNerve B).obj Δ) :
    (duskinNerve B).map f σ = (duskinReindex f).comp σ :=
  rfl

/-!
## The global scaling

For a 2-simplex `σ`, the canonical Duskin triangle is the lax comparison

```text
σ(0 -> 1) >> σ(1 -> 2)  ==>  σ(0 -> 2).
```
-/

/-- The edge `0 -> 1` in `[2]`. -/
def edge01 :
    LocallyDiscrete.mk (0 : Fin 3) ⟶ LocallyDiscrete.mk (1 : Fin 3) :=
  (homOfLE (by decide) : (0 : Fin 3) ⟶ (1 : Fin 3)).toLoc

/-- The edge `1 -> 2` in `[2]`. -/
def edge12 :
    LocallyDiscrete.mk (1 : Fin 3) ⟶ LocallyDiscrete.mk (2 : Fin 3) :=
  (homOfLE (by decide) : (1 : Fin 3) ⟶ (2 : Fin 3)).toLoc

/-- The composition-comparison 2-cell carried by a Duskin 2-simplex. -/
def duskinComparison
    {B : Type u} [Bicategory.{w, v} B]
    (σ : DuskinSimplex B 2) :
    σ.map edge01 ≫ σ.map edge12 ⟶ σ.map (edge01 ≫ edge12) :=
  σ.mapComp edge01 edge12

/-- A 2-simplex is one of the two simplicial degeneracies of a 1-simplex. -/
def IsDegenerateDuskinTwoSimplex
    {B : Type u} [Bicategory.{w, v} B]
    (σ : (duskinNerve B).obj (op ⦋2⦌)) : Prop :=
  (∃ e : (duskinNerve B).obj (op ⦋1⦌),
      σ = (duskinNerve B).σ 0 e) ∨
  (∃ e : (duskinNerve B).obj (op ⦋1⦌),
      σ = (duskinNerve B).σ 1 e)

/--
The canonical global Duskin scaling: invertible comparison triangles are thin,
and all degenerate triangles are thin.
-/
def DuskinThin
    {B : Type u} [Bicategory.{w, v} B]
    (σ : (duskinNerve B).obj (op ⦋2⦌)) : Prop :=
  IsIso (duskinComparison σ) ∨ IsDegenerateDuskinTwoSimplex σ

/-- The Duskin nerve carries a genuine global scaled-simplicial-set structure. -/
def duskinScaling
    (B : Type u) [Bicategory.{w, v} B] :
    ScaledSimplicialSet (duskinNerve B) where
  thin := DuskinThin
  thin_sigma_zero := by
    intro e
    exact Or.inr (Or.inl ⟨e, rfl⟩)
  thin_sigma_one := by
    intro e
    exact Or.inr (Or.inr ⟨e, rfl⟩)

/-- Every triangle with invertible lax comparison is thin in the global scaling. -/
theorem invertibleComparison_isThin
    {B : Type u} [Bicategory.{w, v} B]
    (σ : (duskinNerve B).obj (op ⦋2⦌))
    [IsIso (duskinComparison σ)] :
    (duskinScaling B).thin σ := by
  exact Or.inl inferInstance

/-- Every degenerate 2-simplex is thin in the global scaling. -/
theorem degenerate_isThin
    {B : Type u} [Bicategory.{w, v} B]
    (σ : (duskinNerve B).obj (op ⦋2⦌))
    (hσ : IsDegenerateDuskinTwoSimplex σ) :
    (duskinScaling B).thin σ := by
  exact Or.inr hσ

/-- A bundled global scaled Duskin nerve. -/
structure GlobalScaledDuskinNerve
    (B : Type u) [Bicategory.{w, v} B] where
  carrier : SSet
  scaling : ScaledSimplicialSet carrier
  carrier_eq : carrier = duskinNerve B

/-- The canonical bundled global scaled Duskin nerve of a bicategory. -/
def globalScaledDuskinNerve
    (B : Type u) [Bicategory.{w, v} B] :
    GlobalScaledDuskinNerve B where
  carrier := duskinNerve B
  scaling := duskinScaling B
  carrier_eq := rfl

/-!
The construction is global in the precise sense missing from v1.19:

```text
B
  -> N_Duskin(B) : SSet
  -> one global collection of thin 2-simplices on N_Duskin(B).
```

It is not the previous family of separately scaled mapping nerves.
-/

end KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
