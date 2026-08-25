import Mathlib.AlgebraicTopology.Quasicategory.Nerve
import Mathlib.CategoryTheory.Elements
import KUOS.DependentOriginationCoreSpineV1_15

namespace KUOS.DependentOriginationQuasicategoryNerveV1_16

open CategoryTheory
open Simplicial
open KUOS.DependentOriginationFunctorialTransportV0_1

universe u v w

/-!
# Quasicategorical nerve realization of dependent origination v1.16

The v1.15 layer supplied an all-dimensional coherence interface but deliberately
stopped before claiming horn filling or a quasicategory. This layer gives a
concrete native simplicial-set realization for the original dependent-
origination parent.

For a state functor

```text
D.state : Context ⥤ Type
```

Mathlib's category of elements `D.state.Elements` has:

* objects `(X, x)` with `X : Context` and `x : D.state.obj X`;
* morphisms `(X, x) ⟶ (Y, y)` given by `f : X ⟶ Y` satisfying
  `D.state.map f x = y`.

We define the dependent-origination simplicial set to be the ordinary nerve

```text
N_D := nerve D.state.Elements.
```

This is stronger than taking only the nerve of `Context`: the simplices retain
both contextual objects and the state-transport compatibility carried by the
Grothendieck/category-of-elements construction.

Repository-pinned Mathlib proves:

* the nerve of every category is strict Segal;
* every strict Segal simplicial set is a quasicategory;
* a quasicategory satisfies all inner-horn filling conditions.

The theorems below instantiate that chain on `N_D`.
-/

/-- A conditioned state as an object of the category of elements. -/
def stateElement
    {Context : Type u} [Category.{v} Context]
    (D : FunctorialTransportSystem Context)
    (X : Context) (x : D.state.obj X) :
    D.state.Elements :=
  ⟨X, x⟩

/--
Every parent transport arrow gives an actual morphism in the category of
elements from a conditioned state to its transported state.
-/
def transportElementHom
    {Context : Type u} [Category.{v} Context]
    (D : FunctorialTransportSystem Context)
    {X Y : Context} (f : X ⟶ Y) (x : D.state.obj X) :
    stateElement D X x ⟶ stateElement D Y (D.transport f x) :=
  CategoryOfElements.homMk _ _ f rfl

/-- Forgetting the element component recovers the original context morphism. -/
@[simp] theorem transportElementHom_val
    {Context : Type u} [Category.{v} Context]
    (D : FunctorialTransportSystem Context)
    {X Y : Context} (f : X ⟶ Y) (x : D.state.obj X) :
    (transportElementHom D f x).val = f :=
  rfl

/--
The concrete simplicial-set realization of dependent origination: the nerve of
the category of context-state elements.
-/
def dependentNerve
    {Context : Type u} [Category.{v} Context]
    (D : FunctorialTransportSystem Context) :=
  CategoryTheory.nerve D.state.Elements

/--
The dependent-origination nerve satisfies the constructive strict Segal
condition: every composable spine has a unique simplex extending it.
-/
def dependentNerveStrictSegal
    {Context : Type u} [Category.{v} Context]
    (D : FunctorialTransportSystem Context) :
    SSet.StrictSegal (dependentNerve D) :=
  CategoryTheory.Nerve.strictSegal D.state.Elements

/-- The Segal map from `n`-simplices to composable length-`n` spines is bijective. -/
theorem dependentNerve_segal
    {Context : Type u} [Category.{v} Context]
    (D : FunctorialTransportSystem Context)
    (n : ℕ) :
    Function.Bijective ((dependentNerve D).spine n) :=
  (dependentNerveStrictSegal D).spineEquiv n |>.bijective

/-- The proposition-level native strict-Segal certificate. -/
theorem dependentNerve_isStrictSegal
    {Context : Type u} [Category.{v} Context]
    (D : FunctorialTransportSystem Context) :
    SSet.IsStrictSegal (dependentNerve D) :=
  (dependentNerveStrictSegal D).isStrictSegal

/--
Strict Segal structure supplies the native Mathlib quasicategory structure.
This is the actual implication used in `Quasicategory.StrictSegal`.
-/
theorem dependentNerve_quasicategory
    {Context : Type u} [Category.{v} Context]
    (D : FunctorialTransportSystem Context) :
    SSet.Quasicategory (dependentNerve D) :=
  SSet.StrictSegal.quasicategory (dependentNerveStrictSegal D)

/--
Every inner horn in the dependent-origination nerve has a filler.

For `0 < i < n`, any map `Λ[n,i] ⟶ N_D` extends across the standard simplex
`Δ[n]`. This is the native quasicategory horn-filling condition, not a
KuuOS-local surrogate.
-/
theorem dependentNerve_innerHornFilling
    {Context : Type u} [Category.{v} Context]
    (D : FunctorialTransportSystem Context)
    {n : ℕ} {i : Fin (n + 1)}
    (h0 : 0 < i) (hn : i < Fin.last n)
    (σ₀ : (Λ[n, i] : SSet) ⟶ dependentNerve D) :
    ∃ σ : Δ[n] ⟶ dependentNerve D,
      σ₀ = Λ[n, i].ι ≫ σ := by
  letI : SSet.Quasicategory (dependentNerve D) :=
    dependentNerve_quasicategory D
  exact SSet.Quasicategory.hornFilling h0 hn σ₀

/-!
The exact hierarchy proved here is therefore

```text
D : Context ⥤ Type
  -> category of elements ∫ D
  -> nerve N(∫ D)
  -> strict Segal
  -> inner horn filling
  -> native Mathlib Quasicategory.
```

This is a genuine quasicategorical realization of the one-categorical parent
transport system. It is intentionally not yet a theorem that the independent
v1.15 globular higher-cell tower is equivalent to this nerve, nor does this
claim a nontrivial `(∞,2)`-categorical enhancement of the v1.6 bicategory.
Those are stronger comparison problems.
-/

end KUOS.DependentOriginationQuasicategoryNerveV1_16
