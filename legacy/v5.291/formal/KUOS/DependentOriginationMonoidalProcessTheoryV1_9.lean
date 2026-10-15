import Mathlib.CategoryTheory.Monoidal.Category
import KUOS.DependentOriginationHigherMulticategoryCoherenceV1_8
import KUOS.DependentOriginationFunctorialTransportV0_1

namespace KUOS.DependentOriginationMonoidalProcessTheoryV1_9

open CategoryTheory
open KUOS.DependentOriginationFunctorialTransportV0_1
open KUOS.DependentOriginationHigherMulticategoryCoherenceV1_8

universe u v w y

/-!
# Monoidal process dependent origination v1.9

The parent contextual transport already gives sequential composition.  This
layer adds an independent parallel-composition axis using Mathlib's native
monoidal-category structure.

```text
sequential process composition = categorical composition
parallel process composition   = monoidal tensor
```

The state realization is not inferred from the monoidal source alone.  A
`MonoidalProcessTransportSystem` explicitly supplies a parallel state
constructor and requires it to be natural under tensor products of processes,
as well as coherent with the source associator and unitors.
-/

/--
A contextual transport system equipped with a state-level realization of a
native monoidal process structure.
-/
structure MonoidalProcessTransportSystem
    (Context : Type u) [Category.{v} Context] [MonoidalCategory Context]
    (D : FunctorialTransportSystem Context) where
  tensorState : forall {X Y : Context},
    D.state.obj X -> D.state.obj Y ->
      D.state.obj (MonoidalCategory.tensorObj X Y)
  unitState : D.state.obj (MonoidalCategory.tensorUnit Context)
  tensor_transport : forall {X₁ Y₁ X₂ Y₂ : Context}
    (f : X₁ ⟶ Y₁) (g : X₂ ⟶ Y₂)
    (x : D.state.obj X₁) (y : D.state.obj X₂),
    D.transport (MonoidalCategory.tensorHom f g) (tensorState x y) =
      tensorState (D.transport f x) (D.transport g y)
  associator_state : forall {X Y Z : Context}
    (x : D.state.obj X) (y : D.state.obj Y) (z : D.state.obj Z),
    D.transport (MonoidalCategory.associator X Y Z).hom
        (tensorState (tensorState x y) z) =
      tensorState x (tensorState y z)
  leftUnitor_state : forall {X : Context} (x : D.state.obj X),
    D.transport (MonoidalCategory.leftUnitor X).hom
        (tensorState unitState x) = x
  rightUnitor_state : forall {X : Context} (x : D.state.obj X),
    D.transport (MonoidalCategory.rightUnitor X).hom
        (tensorState x unitState) = x

namespace MonoidalProcessTransportSystem

/-- Sequential composition is exactly the original contextual functor law. -/
theorem sequential
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {D : FunctorialTransportSystem Context}
    (P : MonoidalProcessTransportSystem Context D)
    {X Y Z : Context}
    (f : X ⟶ Y) (g : Y ⟶ Z) (x : D.state.obj X) :
    D.transport (f ≫ g) x = D.transport g (D.transport f x) := by
  exact D.transport_comp_apply f g x

/-- Parallel composition transports each component independently. -/
theorem parallel
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {D : FunctorialTransportSystem Context}
    (P : MonoidalProcessTransportSystem Context D)
    {X₁ Y₁ X₂ Y₂ : Context}
    (f : X₁ ⟶ Y₁) (g : X₂ ⟶ Y₂)
    (x : D.state.obj X₁) (y : D.state.obj X₂) :
    D.transport (MonoidalCategory.tensorHom f g) (P.tensorState x y) =
      P.tensorState (D.transport f x) (D.transport g y) := by
  exact P.tensor_transport f g x y

/--
The native source interchange law: composing two parallel process pairs equals
tensoring the two sequential composites.
-/
theorem source_sequential_parallel_interchange
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {X₁ Y₁ Z₁ X₂ Y₂ Z₂ : Context}
    (f₁ : X₁ ⟶ Y₁) (f₂ : X₂ ⟶ Y₂)
    (g₁ : Y₁ ⟶ Z₁) (g₂ : Y₂ ⟶ Z₂) :
    MonoidalCategory.tensorHom f₁ f₂ ≫ MonoidalCategory.tensorHom g₁ g₂ =
      MonoidalCategory.tensorHom (f₁ ≫ g₁) (f₂ ≫ g₂) := by
  exact MonoidalCategory.tensorHom_comp_tensorHom f₁ f₂ g₁ g₂

/--
Sequential and parallel dependent-origination transport commute in the expected
process-theoretic way.
-/
theorem sequential_parallel_interchange
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {D : FunctorialTransportSystem Context}
    (P : MonoidalProcessTransportSystem Context D)
    {X₁ Y₁ Z₁ X₂ Y₂ Z₂ : Context}
    (f₁ : X₁ ⟶ Y₁) (f₂ : X₂ ⟶ Y₂)
    (g₁ : Y₁ ⟶ Z₁) (g₂ : Y₂ ⟶ Z₂)
    (x₁ : D.state.obj X₁) (x₂ : D.state.obj X₂) :
    D.transport
        (MonoidalCategory.tensorHom f₁ f₂ ≫
          MonoidalCategory.tensorHom g₁ g₂)
        (P.tensorState x₁ x₂) =
      P.tensorState
        (D.transport g₁ (D.transport f₁ x₁))
        (D.transport g₂ (D.transport f₂ x₂)) := by
  calc
    D.transport
        (MonoidalCategory.tensorHom f₁ f₂ ≫
          MonoidalCategory.tensorHom g₁ g₂)
        (P.tensorState x₁ x₂) =
      D.transport (MonoidalCategory.tensorHom g₁ g₂)
        (D.transport (MonoidalCategory.tensorHom f₁ f₂)
          (P.tensorState x₁ x₂)) :=
      D.transport_comp_apply _ _ _
    _ = D.transport (MonoidalCategory.tensorHom g₁ g₂)
        (P.tensorState (D.transport f₁ x₁) (D.transport f₂ x₂)) := by
      rw [P.tensor_transport f₁ f₂ x₁ x₂]
    _ = P.tensorState
        (D.transport g₁ (D.transport f₁ x₁))
        (D.transport g₂ (D.transport f₂ x₂)) := by
      exact P.tensor_transport g₁ g₂
        (D.transport f₁ x₁) (D.transport f₂ x₂)

/-- The parallel state constructor respects reassociation through the native associator. -/
theorem reassociate_parallel_state
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {D : FunctorialTransportSystem Context}
    (P : MonoidalProcessTransportSystem Context D)
    {X Y Z : Context}
    (x : D.state.obj X) (y : D.state.obj Y) (z : D.state.obj Z) :
    D.transport (MonoidalCategory.associator X Y Z).hom
        (P.tensorState (P.tensorState x y) z) =
      P.tensorState x (P.tensorState y z) := by
  exact P.associator_state x y z

end MonoidalProcessTransportSystem

/-!
## Process-level invariant semantics
-/

/--
An invariant semantic readout that also interprets parallel composition.
-/
structure MonoidalProcessReadout
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {D : FunctorialTransportSystem Context}
    (P : MonoidalProcessTransportSystem Context D)
    (Semantic : Type y) where
  readout : (X : Context) -> D.state.obj X -> Semantic
  parallelSemantic : Semantic -> Semantic -> Semantic
  unitSemantic : Semantic
  transport_invariant : forall {X Y : Context}
    (f : X ⟶ Y) (x : D.state.obj X),
    readout Y (D.transport f x) = readout X x
  tensor_readout : forall {X Y : Context}
    (x : D.state.obj X) (y : D.state.obj Y),
    readout (MonoidalCategory.tensorObj X Y) (P.tensorState x y) =
      parallelSemantic (readout X x) (readout Y y)
  unit_readout :
    readout (MonoidalCategory.tensorUnit Context) P.unitState = unitSemantic

namespace MonoidalProcessReadout

/-- Parallel process transport preserves the composed semantic readout. -/
theorem readout_parallel_transport
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {D : FunctorialTransportSystem Context}
    {P : MonoidalProcessTransportSystem Context D}
    {Semantic : Type y}
    (Q : MonoidalProcessReadout P Semantic)
    {X₁ Y₁ X₂ Y₂ : Context}
    (f : X₁ ⟶ Y₁) (g : X₂ ⟶ Y₂)
    (x : D.state.obj X₁) (y : D.state.obj X₂) :
    Q.readout (MonoidalCategory.tensorObj Y₁ Y₂)
        (D.transport (MonoidalCategory.tensorHom f g) (P.tensorState x y)) =
      Q.parallelSemantic (Q.readout X₁ x) (Q.readout X₂ y) := by
  rw [P.tensor_transport f g x y]
  rw [Q.tensor_readout]
  rw [Q.transport_invariant f x, Q.transport_invariant g y]

end MonoidalProcessReadout

/-!
The v1.9 process-theoretic reading is therefore:

```text
objects     = contextual process interfaces
morphisms   = sequential processes
composition = sequential execution
tensor      = parallel composition
unit        = empty/neutral parallel interface
state tensor realization = explicit additional structure
```

The higher multicategory and monoidal-process axes coexist but are not silently
identified: an arbitrary multi-input primitive need not be a tensor product of
independent processes.
-/

end KUOS.DependentOriginationMonoidalProcessTheoryV1_9
