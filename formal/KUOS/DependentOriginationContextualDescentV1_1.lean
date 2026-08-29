import Mathlib
import KUOS.DependentOriginationContextualCoreV1_0

namespace KUOS.DependentOriginationContextualDescentV1_1

open CategoryTheory
open KUOS.DependentOriginationFunctorialTransportV0_1
open KUOS.DependentOriginationContextualCoreV1_0

universe u v w y

/-!
# Contextual refinement and descent v1.1

This layer stays at the non-quantum parent level of dependent origination.

The direction of refinement is covariant:

```text
root context -> local chart -> pairwise overlap/refinement.
```

Thus a state at the root context can be transported to every local chart and
then to every common refinement.  Pairwise overlap coherence is an equality of
context morphism paths, so the induced state compatibility follows from the
functor laws alone.

State-level gluing and semantic-level gluing are deliberately separated.
A compatible local family need not be postulated to arise from one root state.
However, an invariant readout assigns one unique semantic value to every
nonempty overlap-compatible family.  This is the formal sense in which global
meaning can descend without requiring a global substance-like state carrier.
-/

/--
A family of contextual refinements of one root context.

The arrow `toChart i : rootContext -> chart i` means that chart `i` is a more
conditioned/refined context reached from the root context.
-/
structure RefinementCover
    (Context : Type u) [Category.{v} Context]
    (Index : Type w) where
  rootContext : Context
  chart : Index -> Context
  toChart : (i : Index) -> rootContext ⟶ chart i

/--
Explicit pairwise common refinements for a refinement cover.

For each pair of charts there is a common refinement `meet i j`.  The two paths
from the root to that common refinement are required to agree.  No invertibility,
groupoid structure, topology, or pullback universal property is assumed.
-/
structure OverlapSystem
    {Context : Type u} [Category.{v} Context]
    {Index : Type w}
    (C : RefinementCover Context Index) where
  meet : Index -> Index -> Context
  leftToMeet : (i j : Index) -> C.chart i ⟶ meet i j
  rightToMeet : (i j : Index) -> C.chart j ⟶ meet i j
  root_path_coherent : forall i j,
    C.toChart i ≫ leftToMeet i j =
      C.toChart j ≫ rightToMeet i j

/-- A local state at every chart of a refinement cover. -/
structure LocalStateFamily
    {Context : Type u} [Category.{v} Context]
    {Index : Type w}
    (D : FunctorialTransportSystem Context)
    (C : RefinementCover Context Index) where
  state : (i : Index) -> D.state.obj (C.chart i)

namespace LocalStateFamily

variable {Context : Type u} [Category.{v} Context]
variable {Index : Type w}
variable {D E : FunctorialTransportSystem Context}
variable {C : RefinementCover Context Index}

/-- Transport one root state to all local charts. -/
def ofGlobal
    (D : FunctorialTransportSystem Context)
    (C : RefinementCover Context Index)
    (x : D.state.obj C.rootContext) :
    LocalStateFamily D C where
  state := fun i => D.transport (C.toChart i) x

/-- A transport-compatible system map acts pointwise on a local family. -/
def map
    (eta : SystemHom D E)
    (s : LocalStateFamily D C) :
    LocalStateFamily E C where
  state := fun i => eta.app (C.chart i) (s.state i)

end LocalStateFamily

/--
A local family is overlap-compatible when both local states induce the same
state after transport to every pairwise common refinement.
-/
def OverlapCompatible
    {Context : Type u} [Category.{v} Context]
    {Index : Type w}
    (D : FunctorialTransportSystem Context)
    (C : RefinementCover Context Index)
    (O : OverlapSystem C)
    (s : LocalStateFamily D C) : Prop :=
  forall i j,
    D.transport (O.leftToMeet i j) (s.state i) =
      D.transport (O.rightToMeet i j) (s.state j)

/--
A local state family descends at state level when it is induced by at least one
root-context state.
-/
def StateDescends
    {Context : Type u} [Category.{v} Context]
    {Index : Type w}
    (D : FunctorialTransportSystem Context)
    (C : RefinementCover Context Index)
    (s : LocalStateFamily D C) : Prop :=
  exists x : D.state.obj C.rootContext,
    forall i, D.transport (C.toChart i) x = s.state i

/-- Every overlap-compatible family admits a root-state witness. -/
def HasStateDescent
    {Context : Type u} [Category.{v} Context]
    {Index : Type w}
    (D : FunctorialTransportSystem Context)
    (C : RefinementCover Context Index)
    (O : OverlapSystem C) : Prop :=
  forall s : LocalStateFamily D C,
    OverlapCompatible D C O s -> StateDescends D C s

/--
The local charts separate root states when agreement after every root-to-chart
transport forces equality already at the root.
-/
def CoverSeparatesGlobalStates
    {Context : Type u} [Category.{v} Context]
    {Index : Type w}
    (D : FunctorialTransportSystem Context)
    (C : RefinementCover Context Index) : Prop :=
  forall x y : D.state.obj C.rootContext,
    (forall i, D.transport (C.toChart i) x =
      D.transport (C.toChart i) y) -> x = y

/--
Context-path coherence induces equality of the two transported root states on an
overlap.  This is the basic local-coherence theorem and uses only functoriality.
-/
theorem root_transport_to_overlap_coherent
    {Context : Type u} [Category.{v} Context]
    {Index : Type w}
    (D : FunctorialTransportSystem Context)
    (C : RefinementCover Context Index)
    (O : OverlapSystem C)
    (x : D.state.obj C.rootContext)
    (i j : Index) :
    D.transport (O.leftToMeet i j)
        (D.transport (C.toChart i) x) =
      D.transport (O.rightToMeet i j)
        (D.transport (C.toChart j) x) := by
  rw [← D.transport_comp_apply (C.toChart i) (O.leftToMeet i j) x]
  rw [← D.transport_comp_apply (C.toChart j) (O.rightToMeet i j) x]
  rw [O.root_path_coherent i j]

/-- Every family induced from one root state is automatically overlap-compatible. -/
theorem ofGlobal_overlapCompatible
    {Context : Type u} [Category.{v} Context]
    {Index : Type w}
    (D : FunctorialTransportSystem Context)
    (C : RefinementCover Context Index)
    (O : OverlapSystem C)
    (x : D.state.obj C.rootContext) :
    OverlapCompatible D C O (LocalStateFamily.ofGlobal D C x) := by
  intro i j
  exact root_transport_to_overlap_coherent D C O x i j

/-- The local family induced from a root state has that state as a descent witness. -/
theorem ofGlobal_stateDescends
    {Context : Type u} [Category.{v} Context]
    {Index : Type w}
    (D : FunctorialTransportSystem Context)
    (C : RefinementCover Context Index)
    (x : D.state.obj C.rootContext) :
    StateDescends D C (LocalStateFamily.ofGlobal D C x) := by
  refine ⟨x, ?_⟩
  intro i
  rfl

/-- State-level descent implies the necessary pairwise overlap compatibility. -/
theorem overlapCompatible_of_stateDescends
    {Context : Type u} [Category.{v} Context]
    {Index : Type w}
    (D : FunctorialTransportSystem Context)
    (C : RefinementCover Context Index)
    (O : OverlapSystem C)
    (s : LocalStateFamily D C)
    (hDescends : StateDescends D C s) :
    OverlapCompatible D C O s := by
  rcases hDescends with ⟨x, hx⟩
  intro i j
  rw [← hx i, ← hx j]
  exact root_transport_to_overlap_coherent D C O x i j

/-- Transport-compatible maps between systems preserve overlap compatibility. -/
theorem overlapCompatible_map_systemHom
    {Context : Type u} [Category.{v} Context]
    {Index : Type w}
    {D E : FunctorialTransportSystem Context}
    (C : RefinementCover Context Index)
    (O : OverlapSystem C)
    (eta : SystemHom D E)
    (s : LocalStateFamily D C)
    (h : OverlapCompatible D C O s) :
    OverlapCompatible E C O (LocalStateFamily.map eta s) := by
  intro i j
  change E.transport (O.leftToMeet i j)
      (eta.app (C.chart i) (s.state i)) =
    E.transport (O.rightToMeet i j)
      (eta.app (C.chart j) (s.state j))
  rw [← eta.naturality (O.leftToMeet i j) (s.state i)]
  rw [← eta.naturality (O.rightToMeet i j) (s.state j)]
  exact congrArg (eta.app (O.meet i j)) (h i j)

/-- Transport-compatible maps also preserve existence of a root-state witness. -/
theorem stateDescends_map_systemHom
    {Context : Type u} [Category.{v} Context]
    {Index : Type w}
    {D E : FunctorialTransportSystem Context}
    (C : RefinementCover Context Index)
    (eta : SystemHom D E)
    (s : LocalStateFamily D C)
    (h : StateDescends D C s) :
    StateDescends E C (LocalStateFamily.map eta s) := by
  rcases h with ⟨x, hx⟩
  refine ⟨eta.app C.rootContext x, ?_⟩
  intro i
  change E.transport (C.toChart i) (eta.app C.rootContext x) =
    eta.app (C.chart i) (s.state i)
  rw [← eta.naturality (C.toChart i) x]
  rw [hx i]

/--
Existence of state descent together with local separation upgrades gluing to a
unique root-state witness.
-/
theorem existsUnique_globalState_of_descent_and_separation
    {Context : Type u} [Category.{v} Context]
    {Index : Type w}
    (D : FunctorialTransportSystem Context)
    (C : RefinementCover Context Index)
    (O : OverlapSystem C)
    (hDescent : HasStateDescent D C O)
    (hSeparate : CoverSeparatesGlobalStates D C)
    (s : LocalStateFamily D C)
    (hCompatible : OverlapCompatible D C O s) :
    ∃! x : D.state.obj C.rootContext,
      forall i, D.transport (C.toChart i) x = s.state i := by
  rcases hDescent s hCompatible with ⟨x, hx⟩
  refine ⟨x, hx, ?_⟩
  intro y hy
  apply hSeparate y x
  intro i
  rw [hy i, hx i]

/--
Semantic descent means that all local states determine one and only one value in
a context-independent semantic codomain.
-/
def SemanticDescends
    {Context : Type u} [Category.{v} Context]
    {Index : Type w}
    {D : FunctorialTransportSystem Context}
    {Semantic : Type y}
    (R : FunctorialTransportSystem.InvariantReadout D Semantic)
    (C : RefinementCover Context Index)
    (s : LocalStateFamily D C) : Prop :=
  ∃! value : Semantic,
    forall i, R.readout (C.chart i) (s.state i) = value

/--
Overlap-compatible local states have the same invariant semantic value on every
pair of charts.
-/
theorem local_semantic_eq_of_overlapCompatible
    {Context : Type u} [Category.{v} Context]
    {Index : Type w}
    {D : FunctorialTransportSystem Context}
    {Semantic : Type y}
    (R : FunctorialTransportSystem.InvariantReadout D Semantic)
    (C : RefinementCover Context Index)
    (O : OverlapSystem C)
    (s : LocalStateFamily D C)
    (hCompatible : OverlapCompatible D C O s)
    (i j : Index) :
    R.readout (C.chart i) (s.state i) =
      R.readout (C.chart j) (s.state j) := by
  have hLeft := R.transport_invariant
    (O.leftToMeet i j) (s.state i)
  have hRight := R.transport_invariant
    (O.rightToMeet i j) (s.state j)
  calc
    R.readout (C.chart i) (s.state i) =
        R.readout (O.meet i j)
          (D.transport (O.leftToMeet i j) (s.state i)) := hLeft.symm
    _ = R.readout (O.meet i j)
          (D.transport (O.rightToMeet i j) (s.state j)) := by
            rw [hCompatible i j]
    _ = R.readout (C.chart j) (s.state j) := hRight

/--
Every nonempty overlap-compatible local family has one unique invariant semantic
value, without assuming that a root-state witness exists.
-/
theorem semanticDescends_of_overlapCompatible
    {Context : Type u} [Category.{v} Context]
    {Index : Type w} [Nonempty Index]
    {D : FunctorialTransportSystem Context}
    {Semantic : Type y}
    (R : FunctorialTransportSystem.InvariantReadout D Semantic)
    (C : RefinementCover Context Index)
    (O : OverlapSystem C)
    (s : LocalStateFamily D C)
    (hCompatible : OverlapCompatible D C O s) :
    SemanticDescends R C s := by
  classical
  let anchor : Index := Classical.choice (inferInstance : Nonempty Index)
  refine ⟨R.readout (C.chart anchor) (s.state anchor), ?_, ?_⟩
  · intro i
    exact local_semantic_eq_of_overlapCompatible
      R C O s hCompatible i anchor
  · intro value hValue
    exact (hValue anchor).symm

/--
If a concrete root-state witness exists, its invariant readout agrees with every
local semantic value.
-/
theorem globalWitness_readout_eq_local
    {Context : Type u} [Category.{v} Context]
    {Index : Type w}
    {D : FunctorialTransportSystem Context}
    {Semantic : Type y}
    (R : FunctorialTransportSystem.InvariantReadout D Semantic)
    (C : RefinementCover Context Index)
    (s : LocalStateFamily D C)
    (x : D.state.obj C.rootContext)
    (hx : forall i, D.transport (C.toChart i) x = s.state i)
    (i : Index) :
    R.readout C.rootContext x =
      R.readout (C.chart i) (s.state i) := by
  have h := R.transport_invariant (C.toChart i) x
  rw [hx i] at h
  exact h.symm

/--
Semantic gluing is logically weaker than state gluing: even under an explicit
hypothesis that no root-state witness exists, overlap compatibility still yields
one unique invariant semantic value.
-/
theorem semanticDescent_without_stateDescent
    {Context : Type u} [Category.{v} Context]
    {Index : Type w} [Nonempty Index]
    {D : FunctorialTransportSystem Context}
    {Semantic : Type y}
    (R : FunctorialTransportSystem.InvariantReadout D Semantic)
    (C : RefinementCover Context Index)
    (O : OverlapSystem C)
    (s : LocalStateFamily D C)
    (hCompatible : OverlapCompatible D C O s)
    (hNoStateDescent : ¬ StateDescends D C s) :
    (¬ StateDescends D C s) ∧ SemanticDescends R C s := by
  exact ⟨hNoStateDescent,
    semanticDescends_of_overlapCompatible R C O s hCompatible⟩

end KUOS.DependentOriginationContextualDescentV1_1
