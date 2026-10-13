import Mathlib
import KUOS.DependentOriginationContextualDescentV1_1

namespace KUOS.DependentOriginationRefinementTransitivityV1_2

open CategoryTheory
open KUOS.DependentOriginationFunctorialTransportV0_1
open KUOS.DependentOriginationContextualCoreV1_0
open KUOS.DependentOriginationContextualDescentV1_1

universe u v w z y

/-!
# Contextual refinement composition and descent transitivity v1.2

This layer remains inside the non-quantum dependent-origination core.

v1.1 introduced one refinement stage

```text
root -> chart_i -> pairwise common refinement.
```

v1.2 adds refinement of each chart itself:

```text
root -> chart_i -> subchart_(i,j).
```

The two stages can be flattened to one cover indexed by `Sigma SubIndex`.
Functoriality proves that transport through the two stages is exactly transport
along the flattened composite morphism.

The main state theorem is an exact equivalence:

```text
there is an intermediate local family descending from the root,
and every subchart family descends from that intermediate family

iff

the flattened subchart family descends directly from the root.
```

Semantic descent is separately transitive.  If the top local family already has
one invariant semantic value and every subchart state has the same invariant
meaning as its parent chart state, then the flattened family has that same
unique semantic value.  No root-state witness is needed for this semantic
statement.
-/

/--
A second refinement stage over every chart of an existing refinement cover.
`SubIndex i` indexes the refinements internal to chart `i`.
-/
structure RefinementOfCover
    {Context : Type u} [Category.{v} Context]
    {Index : Type w}
    (C : RefinementCover Context Index)
    (SubIndex : Index -> Type z) where
  subchart : (i : Index) -> SubIndex i -> Context
  chartToSubchart : (i : Index) -> (j : SubIndex i) ->
    C.chart i ⟶ subchart i j

namespace RefinementOfCover

variable {Context : Type u} [Category.{v} Context]
variable {Index : Type w}
variable {SubIndex : Index -> Type z}
variable {C : RefinementCover Context Index}

/-- The refinement cover internal to one parent chart. -/
def localCover
    (R : RefinementOfCover C SubIndex)
    (i : Index) :
    RefinementCover Context (SubIndex i) where
  rootContext := C.chart i
  chart := R.subchart i
  toChart := R.chartToSubchart i

/--
Flatten two refinement stages into one root-to-subchart cover.
The flattened index remembers both the outer chart and its inner subchart.
-/
def flatten
    (R : RefinementOfCover C SubIndex) :
    RefinementCover Context (Sigma SubIndex) where
  rootContext := C.rootContext
  chart := fun p => R.subchart p.1 p.2
  toChart := fun p => C.toChart p.1 ≫ R.chartToSubchart p.1 p.2

@[simp] theorem flatten_rootContext
    (R : RefinementOfCover C SubIndex) :
    R.flatten.rootContext = C.rootContext := by
  rfl

@[simp] theorem flatten_chart
    (R : RefinementOfCover C SubIndex)
    (p : Sigma SubIndex) :
    R.flatten.chart p = R.subchart p.1 p.2 := by
  rfl

@[simp] theorem flatten_toChart
    (R : RefinementOfCover C SubIndex)
    (p : Sigma SubIndex) :
    R.flatten.toChart p =
      C.toChart p.1 ≫ R.chartToSubchart p.1 p.2 := by
  rfl

end RefinementOfCover

/-- A state at every subchart of a two-stage refinement. -/
structure NestedLocalStateFamily
    {Context : Type u} [Category.{v} Context]
    {Index : Type w}
    {SubIndex : Index -> Type z}
    (D : FunctorialTransportSystem Context)
    {C : RefinementCover Context Index}
    (R : RefinementOfCover C SubIndex) where
  state : (i : Index) -> (j : SubIndex i) ->
    D.state.obj (R.subchart i j)

namespace NestedLocalStateFamily

variable {Context : Type u} [Category.{v} Context]
variable {Index : Type w}
variable {SubIndex : Index -> Type z}
variable {D : FunctorialTransportSystem Context}
variable {C : RefinementCover Context Index}
variable {R : RefinementOfCover C SubIndex}

/-- View a nested family as one family on the flattened cover. -/
def flatten
    (u : NestedLocalStateFamily D R) :
    LocalStateFamily D R.flatten where
  state := fun p => u.state p.1 p.2

/-- Refine one top-level local family by transport to every subchart. -/
def ofTop
    (D : FunctorialTransportSystem Context)
    (R : RefinementOfCover C SubIndex)
    (s : LocalStateFamily D C) :
    NestedLocalStateFamily D R where
  state := fun i j =>
    D.transport (R.chartToSubchart i j) (s.state i)

/-- Refine one root state through both contextual refinement stages. -/
def ofGlobal
    (D : FunctorialTransportSystem Context)
    (C : RefinementCover Context Index)
    (R : RefinementOfCover C SubIndex)
    (x : D.state.obj C.rootContext) :
    NestedLocalStateFamily D R :=
  ofTop D R (LocalStateFamily.ofGlobal D C x)

@[simp] theorem flatten_state
    (u : NestedLocalStateFamily D R)
    (p : Sigma SubIndex) :
    u.flatten.state p = u.state p.1 p.2 := by
  rfl

end NestedLocalStateFamily

/--
A nested family descends locally to a chosen top-level family when each subchart
state is obtained by transport from its parent chart state.
-/
def LocallyDescendsTo
    {Context : Type u} [Category.{v} Context]
    {Index : Type w}
    {SubIndex : Index -> Type z}
    (D : FunctorialTransportSystem Context)
    {C : RefinementCover Context Index}
    (R : RefinementOfCover C SubIndex)
    (u : NestedLocalStateFamily D R)
    (s : LocalStateFamily D C) : Prop :=
  forall i j,
    D.transport (R.chartToSubchart i j) (s.state i) = u.state i j

/--
Two-stage state descent: first the top family descends from the root, then every
nested subchart family descends from its parent top-level state.
-/
def NestedStateDescends
    {Context : Type u} [Category.{v} Context]
    {Index : Type w}
    {SubIndex : Index -> Type z}
    (D : FunctorialTransportSystem Context)
    (C : RefinementCover Context Index)
    (R : RefinementOfCover C SubIndex)
    (u : NestedLocalStateFamily D R) : Prop :=
  exists s : LocalStateFamily D C,
    StateDescends D C s ∧ LocallyDescendsTo D R u s

/-- Transport through two refinement stages equals transport along the flattened path. -/
theorem twoStep_transport_eq_flatten_transport
    {Context : Type u} [Category.{v} Context]
    {Index : Type w}
    {SubIndex : Index -> Type z}
    (D : FunctorialTransportSystem Context)
    (C : RefinementCover Context Index)
    (R : RefinementOfCover C SubIndex)
    (x : D.state.obj C.rootContext)
    (i : Index) (j : SubIndex i) :
    D.transport (R.chartToSubchart i j)
        (D.transport (C.toChart i) x) =
      D.transport (R.flatten.toChart ⟨i, j⟩) x := by
  rw [← D.transport_comp_apply (C.toChart i) (R.chartToSubchart i j) x]
  rfl

/-- The nested global construction is pointwise identical to direct flattened transport. -/
theorem nested_ofGlobal_flatten_state_eq
    {Context : Type u} [Category.{v} Context]
    {Index : Type w}
    {SubIndex : Index -> Type z}
    (D : FunctorialTransportSystem Context)
    (C : RefinementCover Context Index)
    (R : RefinementOfCover C SubIndex)
    (x : D.state.obj C.rootContext)
    (p : Sigma SubIndex) :
    (NestedLocalStateFamily.ofGlobal D C R x).flatten.state p =
      (LocalStateFamily.ofGlobal D R.flatten x).state p := by
  rcases p with ⟨i, j⟩
  exact twoStep_transport_eq_flatten_transport D C R x i j

/--
State descent is transitive under contextual refinement: two-stage descent is
exactly the same existence statement as descent on the flattened cover.
-/
theorem nestedStateDescends_iff_flattenStateDescends
    {Context : Type u} [Category.{v} Context]
    {Index : Type w}
    {SubIndex : Index -> Type z}
    (D : FunctorialTransportSystem Context)
    (C : RefinementCover Context Index)
    (R : RefinementOfCover C SubIndex)
    (u : NestedLocalStateFamily D R) :
    NestedStateDescends D C R u ↔
      StateDescends D R.flatten u.flatten := by
  constructor
  · rintro ⟨s, ⟨x, hx⟩, hLocal⟩
    refine ⟨x, ?_⟩
    intro p
    rcases p with ⟨i, j⟩
    change D.transport (R.flatten.toChart ⟨i, j⟩) x = u.state i j
    calc
      D.transport (R.flatten.toChart ⟨i, j⟩) x =
          D.transport (R.chartToSubchart i j)
            (D.transport (C.toChart i) x) := by
              symm
              exact twoStep_transport_eq_flatten_transport D C R x i j
      _ = D.transport (R.chartToSubchart i j) (s.state i) := by
            rw [hx i]
      _ = u.state i j := hLocal i j
  · rintro ⟨x, hx⟩
    let s : LocalStateFamily D C := LocalStateFamily.ofGlobal D C x
    refine ⟨s, ofGlobal_stateDescends D C x, ?_⟩
    intro i j
    change D.transport (R.chartToSubchart i j)
      (D.transport (C.toChart i) x) = u.state i j
    calc
      D.transport (R.chartToSubchart i j)
          (D.transport (C.toChart i) x) =
        D.transport (R.flatten.toChart ⟨i, j⟩) x :=
          twoStep_transport_eq_flatten_transport D C R x i j
      _ = u.state i j := by
        simpa [NestedLocalStateFamily.flatten] using hx ⟨i, j⟩

/--
Every inner refinement cover separates states of its parent chart.  This is the
local analogue of the v1.1 global-state separation condition.
-/
def SubcoversSeparateChartStates
    {Context : Type u} [Category.{v} Context]
    {Index : Type w}
    {SubIndex : Index -> Type z}
    (D : FunctorialTransportSystem Context)
    {C : RefinementCover Context Index}
    (R : RefinementOfCover C SubIndex) : Prop :=
  forall i, CoverSeparatesGlobalStates D (R.localCover i)

/--
If the top family has no root-state witness and each inner refinement separates
its parent chart states, further refinement cannot manufacture a flattened
root-state witness.
-/
theorem no_flattenStateDescent_of_no_topStateDescent
    {Context : Type u} [Category.{v} Context]
    {Index : Type w}
    {SubIndex : Index -> Type z}
    (D : FunctorialTransportSystem Context)
    (C : RefinementCover Context Index)
    (R : RefinementOfCover C SubIndex)
    (s : LocalStateFamily D C)
    (u : NestedLocalStateFamily D R)
    (hNoTop : ¬ StateDescends D C s)
    (hSeparate : SubcoversSeparateChartStates D R)
    (hLocal : LocallyDescendsTo D R u s) :
    ¬ StateDescends D R.flatten u.flatten := by
  intro hFlat
  apply hNoTop
  rcases hFlat with ⟨x, hx⟩
  refine ⟨x, ?_⟩
  intro i
  apply hSeparate i
  intro j
  change D.transport (R.chartToSubchart i j)
      (D.transport (C.toChart i) x) =
    D.transport (R.chartToSubchart i j) (s.state i)
  calc
    D.transport (R.chartToSubchart i j)
        (D.transport (C.toChart i) x) =
      D.transport (R.flatten.toChart ⟨i, j⟩) x :=
        twoStep_transport_eq_flatten_transport D C R x i j
    _ = u.state i j := by
      simpa [NestedLocalStateFamily.flatten] using hx ⟨i, j⟩
    _ = D.transport (R.chartToSubchart i j) (s.state i) :=
      (hLocal i j).symm

/--
The invariant semantic value of every subchart agrees with the invariant
semantic value of its chosen parent chart state.
-/
def SemanticRefinesTo
    {Context : Type u} [Category.{v} Context]
    {Index : Type w}
    {SubIndex : Index -> Type z}
    {D : FunctorialTransportSystem Context}
    {Semantic : Type y}
    (Readout : FunctorialTransportSystem.InvariantReadout D Semantic)
    {C : RefinementCover Context Index}
    (R : RefinementOfCover C SubIndex)
    (u : NestedLocalStateFamily D R)
    (s : LocalStateFamily D C) : Prop :=
  forall i j,
    Readout.readout (R.subchart i j) (u.state i j) =
      Readout.readout (C.chart i) (s.state i)

/-- Local state descent automatically gives semantic refinement compatibility. -/
theorem semanticRefinesTo_of_locallyDescendsTo
    {Context : Type u} [Category.{v} Context]
    {Index : Type w}
    {SubIndex : Index -> Type z}
    {D : FunctorialTransportSystem Context}
    {Semantic : Type y}
    (Readout : FunctorialTransportSystem.InvariantReadout D Semantic)
    {C : RefinementCover Context Index}
    (R : RefinementOfCover C SubIndex)
    (u : NestedLocalStateFamily D R)
    (s : LocalStateFamily D C)
    (hLocal : LocallyDescendsTo D R u s) :
    SemanticRefinesTo Readout R u s := by
  intro i j
  have h := Readout.transport_invariant
    (R.chartToSubchart i j) (s.state i)
  rw [hLocal i j] at h
  exact h

/--
Semantic descent is transitive through arbitrary further contextual refinement.
Only a semantic link from each subchart to its parent chart is needed; no
root-state witness is required.
-/
theorem semanticDescends_flatten_of_semanticRefinesTo
    {Context : Type u} [Category.{v} Context]
    {Index : Type w}
    {SubIndex : Index -> Type z}
    [Nonempty (Sigma SubIndex)]
    {D : FunctorialTransportSystem Context}
    {Semantic : Type y}
    (Readout : FunctorialTransportSystem.InvariantReadout D Semantic)
    (C : RefinementCover Context Index)
    (R : RefinementOfCover C SubIndex)
    (s : LocalStateFamily D C)
    (u : NestedLocalStateFamily D R)
    (hTop : SemanticDescends Readout C s)
    (hRefines : SemanticRefinesTo Readout R u s) :
    SemanticDescends Readout R.flatten u.flatten := by
  classical
  rcases hTop with ⟨value, hValue, _⟩
  refine ⟨value, ?_, ?_⟩
  · intro p
    rcases p with ⟨i, j⟩
    change Readout.readout (R.subchart i j) (u.state i j) = value
    exact (hRefines i j).trans (hValue i)
  · intro other hOther
    let anchor : Sigma SubIndex :=
      Classical.choice (inferInstance : Nonempty (Sigma SubIndex))
    rcases anchor with ⟨i, j⟩
    have hOtherAnchor := hOther ⟨i, j⟩
    change Readout.readout (R.subchart i j) (u.state i j) = other at hOtherAnchor
    calc
      other = Readout.readout (R.subchart i j) (u.state i j) := hOtherAnchor.symm
      _ = Readout.readout (C.chart i) (s.state i) := hRefines i j
      _ = value := hValue i

/--
Top-level overlap compatibility plus local descent is enough for semantic descent
of the fully refined family.
-/
theorem semanticDescends_flatten_of_top_overlapCompatible_and_localDescent
    {Context : Type u} [Category.{v} Context]
    {Index : Type w} [Nonempty Index]
    {SubIndex : Index -> Type z}
    [Nonempty (Sigma SubIndex)]
    {D : FunctorialTransportSystem Context}
    {Semantic : Type y}
    (Readout : FunctorialTransportSystem.InvariantReadout D Semantic)
    (C : RefinementCover Context Index)
    (O : OverlapSystem C)
    (R : RefinementOfCover C SubIndex)
    (s : LocalStateFamily D C)
    (u : NestedLocalStateFamily D R)
    (hTopCompatible : OverlapCompatible D C O s)
    (hLocal : LocallyDescendsTo D R u s) :
    SemanticDescends Readout R.flatten u.flatten := by
  apply semanticDescends_flatten_of_semanticRefinesTo
    Readout C R s u
  · exact semanticDescends_of_overlapCompatible
      Readout C O s hTopCompatible
  · exact semanticRefinesTo_of_locallyDescendsTo
      Readout R u s hLocal

/--
Further local refinement can preserve one global invariant meaning while still
failing to create any global root-state carrier.
-/
theorem semanticDescent_persists_without_flattenStateDescent
    {Context : Type u} [Category.{v} Context]
    {Index : Type w} [Nonempty Index]
    {SubIndex : Index -> Type z}
    [Nonempty (Sigma SubIndex)]
    {D : FunctorialTransportSystem Context}
    {Semantic : Type y}
    (Readout : FunctorialTransportSystem.InvariantReadout D Semantic)
    (C : RefinementCover Context Index)
    (O : OverlapSystem C)
    (R : RefinementOfCover C SubIndex)
    (s : LocalStateFamily D C)
    (u : NestedLocalStateFamily D R)
    (hTopCompatible : OverlapCompatible D C O s)
    (hNoTopState : ¬ StateDescends D C s)
    (hSeparate : SubcoversSeparateChartStates D R)
    (hLocal : LocallyDescendsTo D R u s) :
    (¬ StateDescends D R.flatten u.flatten) ∧
      SemanticDescends Readout R.flatten u.flatten := by
  constructor
  · exact no_flattenStateDescent_of_no_topStateDescent
      D C R s u hNoTopState hSeparate hLocal
  · exact semanticDescends_flatten_of_top_overlapCompatible_and_localDescent
      Readout C O R s u hTopCompatible hLocal

end KUOS.DependentOriginationRefinementTransitivityV1_2
