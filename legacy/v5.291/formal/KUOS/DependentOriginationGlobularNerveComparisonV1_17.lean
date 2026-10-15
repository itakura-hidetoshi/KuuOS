import KUOS.DependentOriginationInfinityCoherenceV1_15
import KUOS.DependentOriginationQuasicategoryNerveV1_16

namespace KUOS.DependentOriginationGlobularNerveComparisonV1_17

open CategoryTheory
open Opposite
open SimplexCategory
open KUOS.DependentOriginationFunctorialTransportV0_1
open KUOS.DependentOriginationInfinityCoherenceV1_15
open KUOS.DependentOriginationQuasicategoryNerveV1_16

universe u v x

/-!
# Globular / dependent-nerve comparison boundary v1.17

A v1.15 `ReflexiveGlobularCoherenceTower` and the v1.16 simplicial set
`dependentNerve D = N(∫ D)` are different kinds of higher carrier.

There is therefore no type-correct theorem saying that an arbitrary globular
tower is automatically equivalent to `N(∫ D)`.  Even a necessary levelwise
carrier comparison can fail.

This file makes that boundary explicit.  A tower can be compared to the
v1.16 nerve only after supplying comparison data.  We also give a concrete
level-zero obstruction showing that no universal comparison theorem can hold.
-/

/--
A necessary levelwise carrier comparison between a globular tower and the
simplices of the dependent-origination nerve.

This is intentionally weaker than a globular/simplicial equivalence: source,
target, degeneracy and all simplicial face maps are extra coherence data.
-/
structure LevelwiseNerveCompatible
    (T : ReflexiveGlobularCoherenceTower.{x})
    {Context : Type u} [Category.{v} Context]
    (D : FunctorialTransportSystem Context) where
  cellEquiv : forall n : Nat,
    T.Cell n ≃ (dependentNerve D).obj (op ⦋n⦌)

namespace LevelwiseNerveCompatible

/-- Extract the dimension-`n` carrier equivalence supplied by the certificate. -/
def at
    {T : ReflexiveGlobularCoherenceTower.{x}}
    {Context : Type u} [Category.{v} Context]
    {D : FunctorialTransportSystem Context}
    (C : LevelwiseNerveCompatible T D)
    (n : Nat) :
    T.Cell n ≃ (dependentNerve D).obj (op ⦋n⦌) :=
  C.cellEquiv n

end LevelwiseNerveCompatible

/-- A reflexive globular tower with exactly one cell in every dimension. -/
def unitTower : ReflexiveGlobularCoherenceTower where
  Cell := fun _ => PUnit
  source := fun _ _ => PUnit.unit
  target := fun _ _ => PUnit.unit
  identity := fun _ _ => PUnit.unit
  source_identity := by
    intro n c
    cases c
    rfl
  target_identity := by
    intro n c
    cases c
    rfl
  source_source := by
    intro n c
    cases c
    rfl
  target_source := by
    intro n c
    cases c
    rfl

/-- One discrete context carrying two distinct states. -/
def twoStateSystem :
    FunctorialTransportSystem (Discrete PUnit) where
  state :=
    { obj := fun _ => Fin 2
      map := fun _ x => x
      map_id := by
        intro X
        rfl
      map_comp := by
        intro X Y Z f g
        rfl }

/-- The unique context in `Discrete PUnit`. -/
def twoStateContext : Discrete PUnit :=
  ⟨PUnit.unit⟩

/-- The two distinguished zero-simplices of the dependent nerve. -/
def twoStateZeroSimplex (b : Fin 2) :
    (dependentNerve twoStateSystem).obj (op ⦋0⦌) :=
  CategoryTheory.nerveEquiv.symm
    (stateElement twoStateSystem twoStateContext b)

/-- The two state-labelled vertices of the dependent nerve are distinct. -/
theorem twoStateZeroSimplex_ne :
    twoStateZeroSimplex 0 ≠ twoStateZeroSimplex 1 := by
  intro h
  have h' :
      stateElement twoStateSystem twoStateContext (0 : Fin 2) =
        stateElement twoStateSystem twoStateContext (1 : Fin 2) := by
    exact congrArg
      (CategoryTheory.nerveEquiv :
        (dependentNerve twoStateSystem).obj (op ⦋0⦌) ≃
          twoStateSystem.state.Elements)
      h
  have hb : (0 : Fin 2) = 1 :=
    congrArg (fun z : twoStateSystem.state.Elements => z.2) h'
  have hne : (0 : Fin 2) ≠ 1 := by decide
  exact hne hb

/--
The one-cell-per-dimension globular tower cannot even be levelwise equivalent
at dimension zero to the nerve of the two-state dependent-origination system.
-/
theorem unitTower_not_levelwise_compatible :
    ¬ LevelwiseNerveCompatible unitTower twoStateSystem := by
  intro C
  let e := C.cellEquiv 0
  obtain ⟨u0, hu0⟩ := e.surjective (twoStateZeroSimplex 0)
  obtain ⟨u1, hu1⟩ := e.surjective (twoStateZeroSimplex 1)
  have hu : u0 = u1 := Subsingleton.elim _ _
  apply twoStateZeroSimplex_ne
  calc
    twoStateZeroSimplex 0 = e u0 := hu0.symm
    _ = e u1 := congrArg e hu
    _ = twoStateZeroSimplex 1 := hu1

/--
Consequently an arbitrary v1.15 globular tower is not forced by the parent
axioms to have the same levelwise carriers as `N(∫ D)`.
-/
theorem no_universal_globular_nerve_comparison :
    ∃ (T : ReflexiveGlobularCoherenceTower)
      (D : FunctorialTransportSystem (Discrete PUnit)),
      ¬ LevelwiseNerveCompatible T D :=
  ⟨unitTower, twoStateSystem, unitTower_not_levelwise_compatible⟩

/-!
The corrected hierarchy is therefore

```text
arbitrary v1.15 globular tower
  != automatically N(∫ D)

chosen globular tower
  + explicit levelwise/simplicial compatibility data
  -> comparison with N(∫ D).
```

A genuine equivalence between a globular model and a simplicial model requires
an actual realization/comparison construction, not only the v1.15 reflexive
globular axioms.
-/

end KUOS.DependentOriginationGlobularNerveComparisonV1_17
