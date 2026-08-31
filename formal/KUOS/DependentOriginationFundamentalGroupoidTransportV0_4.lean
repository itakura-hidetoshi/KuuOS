import Mathlib
import KUOS.DependentOriginationContextualGaugeCoreFactorizationV0_3

namespace KUOS.DependentOriginationFundamentalGroupoidTransportV0_4

open CategoryTheory
open KUOS.DependentOriginationFunctorialTransportV0_1
open KUOS.DependentOriginationContextualCoreV1_0
open KUOS.DependentOriginationContextualGaugeCoreFactorizationV0_3

universe u v w

/-!
# Fundamental-groupoid contextual transport v0.4

This file supplies the first topological realization layer above the algebraic
contextual-gauge spine.

For a topological space `X`, Mathlib's `FundamentalGroupoid X` has points of `X`
as objects and endpoint-fixed path-homotopy classes as morphisms.  Therefore a
functor

```text
FundamentalGroupoid X ⥤ Type
```

is a KuuOS dependent-origination transport system whose transport is reversible
and depends only on the ordinary path-homotopy class.

This is deliberately a conservative boundary.  It is a homotopy-invariant /
local-system-like transport carrier.  We do **not** identify it here with a
smooth flat principal-bundle connection, and we do **not** claim that a general
non-flat connection factors through the ordinary fundamental groupoid.  Such a
connection requires a finer path/thin-homotopy realization and an explicit
geometric bridge.
-/

variable {X : Type u} [TopologicalSpace X]

/-- A homotopy-invariant transport presentation on a topological space. -/
abbrev FundamentalTransport (X : Type u) [TopologicalSpace X] :=
  FundamentalGroupoid X ⥤ Type v

/-- View a point of the space as an object of its fundamental groupoid. -/
def fundamentalPoint (x : X) : FundamentalGroupoid X :=
  ⟨x⟩

@[simp] theorem fundamentalPoint_as (x : X) :
    (fundamentalPoint x).as = x :=
  rfl

/--
A fundamental-groupoid transport is directly a dependent-origination transport
system on the fundamental-groupoid context.
-/
def asDependentOrigination
    (T : FundamentalTransport (v := v) X) :
    FunctorialTransportSystem (FundamentalGroupoid X) where
  state := T

/--
Because the fundamental groupoid is a genuine Mathlib groupoid, the transport
canonically lands in `Core (Type)`.
-/
noncomputable def fundamentalCoreFunctor
    (T : FundamentalTransport (v := v) X) :
    FundamentalGroupoid X ⥤ Core (Type v) :=
  FunctorialTransportSystem.coreStateFunctor (asDependentOrigination T)

/-- Forgetting the explicit isomorphism witness recovers the original transport. -/
noncomputable def fundamentalCoreFactorizationIso
    (T : FundamentalTransport (v := v) X) :
    fundamentalCoreFunctor T ⋙ Core.inclusion (Type v) ≅ T :=
  FunctorialTransportSystem.coreStateFactorizationIso (asDependentOrigination T)

/-- Every fundamental-groupoid transport morphism acts by an actual equivalence. -/
noncomputable def monodromyEquiv
    (T : FundamentalTransport (v := v) X)
    {a b : FundamentalGroupoid X} (gamma : a ⟶ b) :
    T.obj a ≃ T.obj b :=
  (asDependentOrigination T).transportEquiv gamma

/-- A concrete path determines a morphism by taking its ordinary homotopy class. -/
def pathClass
    {x y : X} (p : Path x y) :
    fundamentalPoint x ⟶ fundamentalPoint y :=
  ⟦p⟧

/-- Transport along a concrete path is transport along its homotopy class. -/
def pathTransport
    (T : FundamentalTransport (v := v) X)
    {x y : X} (p : Path x y) :
    T.obj (fundamentalPoint x) → T.obj (fundamentalPoint y) :=
  T.map (pathClass p)

/-- Homotopic paths define the same fundamental-groupoid arrow. -/
theorem pathClass_eq_of_homotopic
    {x y : X} {p q : Path x y}
    (h : p.Homotopic q) :
    pathClass p = pathClass q := by
  exact Quotient.sound h

/--
The induced contextual transport depends only on ordinary endpoint-fixed path
homotopy, not on the chosen path representative.
-/
theorem pathTransport_eq_of_homotopic
    (T : FundamentalTransport (v := v) X)
    {x y : X} {p q : Path x y}
    (h : p.Homotopic q) :
    pathTransport T p = pathTransport T q := by
  rw [pathTransport, pathTransport, pathClass_eq_of_homotopic h]

/-- Pointwise form of homotopy invariance. -/
theorem pathTransport_apply_eq_of_homotopic
    (T : FundamentalTransport (v := v) X)
    {x y : X} {p q : Path x y}
    (h : p.Homotopic q)
    (psi : T.obj (fundamentalPoint x)) :
    pathTransport T p psi = pathTransport T q psi := by
  rw [pathTransport_eq_of_homotopic T h]

/-- The constant path transports every state identically. -/
@[simp] theorem pathTransport_refl_apply
    (T : FundamentalTransport (v := v) X)
    (x : X) (psi : T.obj (fundamentalPoint x)) :
    pathTransport T (Path.refl x) psi = psi := by
  change T.map (𝟙 (fundamentalPoint x)) psi = psi
  simpa using congrFun (T.map_id (fundamentalPoint x)) psi

/--
The contextual transport attached to any fundamental-groupoid arrow is
invertible; the inverse is transport along the inverse homotopy class.
-/
theorem fundamentalTransport_map_isIso
    (T : FundamentalTransport (v := v) X)
    {a b : FundamentalGroupoid X} (gamma : a ⟶ b) :
    IsIso (T.map gamma) := by
  infer_instance

/-! ## Functorial change of topological context -/

variable {Y : Type w} [TopologicalSpace Y]

/-- Pull back a homotopy-invariant transport along a continuous map. -/
def pullback
    (f : C(X, Y))
    (T : FundamentalTransport (v := v) Y) :
    FundamentalTransport (v := v) X :=
  FundamentalGroupoid.map f ⋙ T

@[simp] theorem pullback_obj
    (f : C(X, Y))
    (T : FundamentalTransport (v := v) Y)
    (x : FundamentalGroupoid X) :
    (pullback f T).obj x = T.obj ((FundamentalGroupoid.map f).obj x) :=
  rfl

@[simp] theorem pullback_map
    (f : C(X, Y))
    (T : FundamentalTransport (v := v) Y)
    {x y : FundamentalGroupoid X} (gamma : x ⟶ y) :
    (pullback f T).map gamma =
      T.map ((FundamentalGroupoid.map f).map gamma) :=
  rfl

/--
Pullback is exactly KuuOS contextual reindexing along the induced fundamental-
groupoid functor.
-/
theorem pullback_asDependentOrigination_state
    (f : C(X, Y))
    (T : FundamentalTransport (v := v) Y) :
    (asDependentOrigination (pullback f T)).state =
      (KUOS.DependentOriginationContextualCoreV1_0.reindex
        (FundamentalGroupoid.map f) (asDependentOrigination T)).state := by
  rfl

end KUOS.DependentOriginationFundamentalGroupoidTransportV0_4
