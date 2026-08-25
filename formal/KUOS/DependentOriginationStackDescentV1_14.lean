import Mathlib.CategoryTheory.Sites.Descent.IsStack
import KUOS.DependentOriginationCoreSpineV1_13

namespace KUOS.DependentOriginationStackDescentV1_14

open CategoryTheory
open Opposite
open KUOS.DependentOriginationFunctorialTransportV0_1

universe t u v u' v'

/-!
# Stack descent dependent origination v1.14

The earlier contextual-descent layer deliberately did not infer a global state
from compatible local states.  That weak parent boundary remains unchanged.

This file adds a stronger, optional local-to-global layer only after supplying:

* a Grothendieck topology `J` on the context category;
* a `Cat`-valued pseudofunctor on the opposite context category;
* Mathlib's native `Pseudofunctor.IsStack F J` certificate.

Thus "stack" is used only where effective descent has actually been supplied.
-/

/--
A stack-valued dependent-origination layer over one context category.

`interpretState` places each parent state into an object of the corresponding
stack fiber.  No transport compatibility is silently inferred from this map;
the native pseudofunctor and stack certificate carry the actual descent data.
-/
structure StackDependentOriginationLayer
    (Context : Type u) [Category.{v} Context] where
  base : FunctorialTransportSystem Context
  fiber : LocallyDiscrete Contextᵒᵖ ⥤ᵖ Cat.{v', u'}
  topology : GrothendieckTopology Context
  interpretState : forall X : Context,
    base.state.obj X -> fiber.obj (LocallyDiscrete.mk (op X))
  isStack : Pseudofunctor.IsStack fiber topology

namespace StackDependentOriginationLayer

/--
For every covering family, native stack descent identifies the fiber over the
base with the corresponding category of descent data up to equivalence.
-/
theorem descentData_isEquivalence
    {Context : Type u} [Category.{v} Context]
    (S : StackDependentOriginationLayer Context)
    {ι : Type t} {T : Context} {X : ι -> Context}
    (f : forall i, X i ⟶ T)
    (hf : Sieve.ofArrows X f ∈ S.topology T) :
    (S.fiber.toDescentData f).IsEquivalence := by
  letI : Pseudofunctor.IsStack S.fiber S.topology := S.isStack
  exact S.fiber.isEquivalence_toDescentData f hf

/-- The supplied stack certificate is retained as an explicit stronger layer. -/
theorem has_effective_descent
    {Context : Type u} [Category.{v} Context]
    (S : StackDependentOriginationLayer Context) :
    Pseudofunctor.IsStack S.fiber S.topology :=
  S.isStack

end StackDependentOriginationLayer

/-!
The logical hierarchy is therefore:

```text
parent contextual compatibility
  != automatic global state descent

parent contextual compatibility
  + chosen Grothendieck topology
  + Cat-valued pseudofunctor
  + native IsStack certificate
  -> effective stack descent.
```

This layer does not turn every dependent-origination context system into a
stack.  The topology, pseudofunctor, and effectiveness proof are additional
structure.
-/

end KUOS.DependentOriginationStackDescentV1_14
