import Mathlib.AlgebraicTopology.Quasicategory.Nerve
import Mathlib.CategoryTheory.Bicategory.Yoneda
import KUOS.DependentOriginationBicategoricalCoherenceV1_6
import KUOS.DependentOriginationGlobularNerveComparisonV1_17

namespace KUOS.DependentOriginationInfinityTwoYonedaV1_18

open CategoryTheory
open Simplicial
open KUOS.DependentOriginationBicategoricalCoherenceV1_6

universe u v w x

/-!
# Locally quasicategorical 2-Yoneda realization v1.18

The pinned Mathlib revision has a native bicategory, native `Cat`-valued
2-Yoneda pseudofunctor, and native quasicategories.  It does not expose a
single completed `InfinityTwoCategory` typeclass or a scaled-simplicial-set
model that we can honestly target directly.

Accordingly this layer constructs the standard data that are available and
provable now:

* every hom-category `B(X,Y)` is sent to its simplicial nerve;
* every such mapping nerve is strict Segal and therefore a native Mathlib
  quasicategory with all inner horn fillers;
* precomposition and postcomposition induce simplicial maps between mapping
  nerves;
* Mathlib's native bicategorical Yoneda pseudofunctor retains the weak
  associator/unitor coherence at the `Cat`-valued level.

This is an `(∞,2)`-realization interface: objects remain objects of `B`, while
mapping objects are quasicategories.  We do not rename this interface into a
native full `(∞,2)`-category model absent the additional model-specific axioms.
-/

/-- The simplicial mapping object associated to a bicategorical hom-category. -/
def mappingNerve
    {B : Type u} [Bicategory.{w, v} B]
    (X Y : B) :=
  CategoryTheory.nerve (X ⟶ Y)

/-- Every mapping nerve is constructively strict Segal. -/
def mappingNerveStrictSegal
    {B : Type u} [Bicategory.{w, v} B]
    (X Y : B) :
    SSet.StrictSegal (mappingNerve X Y) :=
  CategoryTheory.Nerve.strictSegal (X ⟶ Y)

/-- Every mapping nerve has bijective Segal spine maps. -/
theorem mappingNerve_segal
    {B : Type u} [Bicategory.{w, v} B]
    (X Y : B) (n : Nat) :
    Function.Bijective ((mappingNerve X Y).spine n) :=
  (mappingNerveStrictSegal X Y).spineEquiv n |>.bijective

/-- Every bicategorical hom-category nerve is a native Mathlib quasicategory. -/
theorem mappingNerve_quasicategory
    {B : Type u} [Bicategory.{w, v} B]
    (X Y : B) :
    SSet.Quasicategory (mappingNerve X Y) :=
  SSet.StrictSegal.quasicategory (mappingNerveStrictSegal X Y)

/-- Every inner horn in every mapping quasicategory has a filler. -/
theorem mappingNerve_innerHornFilling
    {B : Type u} [Bicategory.{w, v} B]
    (X Y : B)
    {n : Nat} {i : Fin (n + 1)}
    (h0 : 0 < i) (hn : i < Fin.last n)
    (σ₀ : (Λ[n, i] : SSet) ⟶ mappingNerve X Y) :
    ∃ σ : Δ[n] ⟶ mappingNerve X Y,
      σ₀ = Λ[n, i].ι ≫ σ := by
  letI : SSet.Quasicategory (mappingNerve X Y) :=
    mappingNerve_quasicategory X Y
  exact SSet.Quasicategory.hornFilling h0 hn σ₀

/--
Precomposition by a bicategorical 1-morphism induces a map of mapping nerves.
The underlying functor is Mathlib's native `Bicategory.precomp`.
-/
def precompositionNerveMap
    {B : Type u} [Bicategory.{w, v} B]
    {a b : B} (c : B) (f : a ⟶ b) :
    mappingNerve b c ⟶ mappingNerve a c :=
  CategoryTheory.nerveMap (Bicategory.precomp c f)

/--
Postcomposition by a bicategorical 1-morphism induces a map of mapping nerves.
The underlying functor is Mathlib's native `Bicategory.postcomp`.
-/
def postcompositionNerveMap
    {B : Type u} [Bicategory.{w, v} B]
    (a : B) {b c : B} (g : b ⟶ c) :
    mappingNerve a b ⟶ mappingNerve a c :=
  CategoryTheory.nerveMap (Bicategory.postcomp a g)

/--
The native 2-Yoneda pseudofunctor of the source bicategory.

It sends `x` to the `Cat`-valued pseudofunctor `a ↦ (a ⟶ x)` and carries
1- and 2-morphisms by postcomposition.  Its `mapId` and `mapComp` fields are
built from bicategorical unitors and associators.
-/
def twoYoneda
    {B : Type u} [Bicategory.{w, v} B] :=
  Bicategory.yoneda (B := B)

namespace BicategoricalTransportSystem

/--
Every v1.6 dependent-origination bicategorical source therefore has
quasicategorical mapping objects.
-/
theorem has_mapping_quasicategories
    {B : Type u} [Bicategory.{w, v} B]
    (D : BicategoricalTransportSystem B) :
    ∀ X Y : B, SSet.Quasicategory (mappingNerve X Y) := by
  intro X Y
  exact mappingNerve_quasicategory X Y

/-- The v1.6 source admits the native bicategorical 2-Yoneda realization. -/
def toTwoYoneda
    {B : Type u} [Bicategory.{w, v} B]
    (D : BicategoricalTransportSystem B) :=
  twoYoneda (B := B)

end BicategoricalTransportSystem

/-!
The proved higher-realization chain is therefore

```text
v1.6 bicategory B
  -> native bicategorical 2-Yoneda pseudofunctor B -> [Bᵒᵖ, Cat]
  -> hom-categories B(X,Y)
  -> mapping nerves N(B(X,Y))
  -> strict Segal
  -> inner horn filling
  -> native mapping quasicategories.
```

This retains 2-morphisms and weak bicategorical composition coherence.  It is
precisely the locally-quasicategorical data expected of an `(∞,2)`-categorical
realization, but it is not claimed to instantiate a nonexistent pinned-Mathlib
`InfinityTwoCategory` class, nor a scaled-simplicial or complete-Segal model.
-/

end KUOS.DependentOriginationInfinityTwoYonedaV1_18
