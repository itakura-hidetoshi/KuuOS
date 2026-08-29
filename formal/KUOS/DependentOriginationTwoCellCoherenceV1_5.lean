import Mathlib
import KUOS.DependentOriginationFilteredCofinalCategoryV1_4

namespace KUOS.DependentOriginationTwoCellCoherenceV1_5

open CategoryTheory
open KUOS.DependentOriginationFunctorialTransportV0_1
open KUOS.DependentOriginationFilteredCofinalCategoryV1_4

universe u v w x y z q r

/-!
# Two-cell dependent-origination coherence v1.5

The v1.4 filtered-category layer allows parallel refinement arrows, but its
filteredness certificate eventually replaces two parallel paths by an equality

```text
f ≫ h = g ≫ h.
```

This layer takes the first higher-categorical step: path comparison is retained
as explicit two-cell data instead of being identified at the source.

The construction is intentionally weaker than a full bicategory or
infinity-category.  `Refinement2CellStructure` records typed two-cells,
vertical composition, and left/right whiskering, but does not claim the full
coherence-law package of a bicategory.  This is enough to state precisely what
changes in the dependent-origination spine:

* strict path equality is replaced by a two-cell witness;
* root cocone naturality is replaced by a two-cell witness;
* an ordinary `Type`-valued transport system becomes a set-truncated
  realization only after it explicitly sends related paths to equal state
  transports;
* strict v1.4 filtered refinement embeds as the equality-two-cell special case.

Thus different dependent-origination paths can remain distinct in the source
while the present state/readout semantics may deliberately forget that higher
path information.
-/

/--
A minimal typed two-cell carrier on an ordinary category.

Two-cells are data, not propositions, so distinct witnesses may be retained.
The carrier supplies identity two-cells, vertical composition, and whiskering.
No bicategory coherence laws are claimed at this layer.
-/
structure Refinement2CellStructure
    (C : Type u) [Category.{v} C] where
  cell : {X Y : C} -> (X ⟶ Y) -> (X ⟶ Y) -> Type w
  refl : forall {X Y : C} (f : X ⟶ Y), cell f f
  vcomp : forall {X Y : C} {f g h : X ⟶ Y},
    cell f g -> cell g h -> cell f h
  whiskerLeft : forall {W X Y : C} (a : W ⟶ X) {f g : X ⟶ Y},
    cell f g -> cell (a ≫ f) (a ≫ g)
  whiskerRight : forall {X Y Z : C} {f g : X ⟶ Y},
    cell f g -> (b : Y ⟶ Z) -> cell (f ≫ b) (g ≫ b)

/-- Strict equality, regarded as a degenerate two-cell structure. -/
def equality2CellStructure
    (C : Type u) [Category.{v} C] :
    Refinement2CellStructure C where
  cell := fun f g => PLift (f = g)
  refl := fun _ => ⟨rfl⟩
  vcomp := by
    intro X Y f g h alpha beta
    exact ⟨alpha.down.trans beta.down⟩
  whiskerLeft := by
    intro W X Y a f g alpha
    exact ⟨by rw [alpha.down]⟩
  whiskerRight := by
    intro X Y Z f g alpha b
    exact ⟨by rw [alpha.down]⟩

/--
A current `Type`-valued transport system is a set-truncated realization of a
higher context only when every represented two-cell acts by equal state maps.

This field is deliberately explicit: two-cell structure in the source does not
silently force a higher target structure into `Type`.
-/
structure SetTruncatedTwoRealization
    {C : Type u} [Category.{v} C]
    (D : FunctorialTransportSystem C)
    (H : Refinement2CellStructure C) where
  respectsCell : forall {X Y : C} {f g : X ⟶ Y},
    H.cell f g -> D.transport f = D.transport g

/-- Every ordinary functorial transport realizes equality two-cells. -/
def equalitySetTruncatedRealization
    {C : Type u} [Category.{v} C]
    (D : FunctorialTransportSystem C) :
    SetTruncatedTwoRealization D (equality2CellStructure C) where
  respectsCell := by
    intro X Y f g alpha
    rcases alpha with ⟨h⟩
    subst g
    rfl

/--
Filteredness with eventual two-cell coherence instead of eventual equality.

The object-amalgamation condition is unchanged.  Parallel arrows need only
admit a common future after which a two-cell relates the resulting composites.
-/
structure TwoFilteredIndexing
    (J : Type x) [Category.{y} J]
    (H : Refinement2CellStructure J) where
  nonempty : Nonempty J
  common : forall i j : J,
    exists k : J, Nonempty (i ⟶ k) ∧ Nonempty (j ⟶ k)
  cohere : forall {i j : J} (f g : i ⟶ j),
    exists k : J, exists h : j ⟶ k,
      Nonempty (H.cell (f ≫ h) (g ≫ h))

/-- Strict v1.4 filteredness is the equality-two-cell special case. -/
def FilteredIndexing.toTwoFiltered
    {J : Type x} [Category.{y} J]
    (F : FilteredIndexing J) :
    TwoFilteredIndexing J (equality2CellStructure J) where
  nonempty := F.nonempty
  common := F.common
  cohere := by
    intro i j f g
    rcases F.coequalize f g with ⟨k, h, hh⟩
    exact ⟨k, h, ⟨⟨hh⟩⟩⟩

/--
A refinement diagram carrying two-dimensional coherence.

`indexCellMap` says that two-cells between indexing paths are represented by
context two-cells.  `rootCoherence` weakens the strict v1.4 root-cocone equation
to an explicit two-cell.
-/
structure TwoDimensionalRefinementDiagram
    (Context : Type u) [Category.{v} Context]
    (J : Type x) [Category.{y} J]
    (HC : Refinement2CellStructure Context)
    (HJ : Refinement2CellStructure J) where
  rootContext : Context
  chart : J ⥤ Context
  indexCellMap : forall {i j : J} {f g : i ⟶ j},
    HJ.cell f g -> HC.cell (chart.map f) (chart.map g)
  toChart : (j : J) -> rootContext ⟶ chart.obj j
  rootCoherence : forall {i j : J} (f : i ⟶ j),
    HC.cell (toChart i ≫ chart.map f) (toChart j)

/-- A strict v1.4 refinement diagram embeds using equality two-cells. -/
def FilteredRefinementDiagram.toTwoDimensional
    {Context : Type u} [Category.{v} Context]
    {J : Type x} [Category.{y} J]
    (R : FilteredRefinementDiagram Context J) :
    TwoDimensionalRefinementDiagram Context J
      (equality2CellStructure Context)
      (equality2CellStructure J) where
  rootContext := R.rootContext
  chart := R.chart
  indexCellMap := by
    intro i j f g alpha
    exact ⟨congrArg (fun h => R.chart.map h) alpha.down⟩
  toChart := R.toChart
  rootCoherence := fun f => ⟨R.root_naturality f⟩

/--
A two-cell root cocone becomes ordinary root-transport coherence after choosing
a set-truncated realization.
-/
theorem root_transport_coherent
    {Context : Type u} [Category.{v} Context]
    {J : Type x} [Category.{y} J]
    {D : FunctorialTransportSystem Context}
    {HC : Refinement2CellStructure Context}
    {HJ : Refinement2CellStructure J}
    (T : SetTruncatedTwoRealization D HC)
    (R : TwoDimensionalRefinementDiagram Context J HC HJ)
    (a : D.state.obj R.rootContext)
    {i j : J} (f : i ⟶ j) :
    D.transport (R.chart.map f) (D.transport (R.toChart i) a) =
      D.transport (R.toChart j) a := by
  calc
    D.transport (R.chart.map f) (D.transport (R.toChart i) a) =
        D.transport (R.toChart i ≫ R.chart.map f) a :=
      (D.transport_comp_apply (R.toChart i) (R.chart.map f) a).symm
    _ = D.transport (R.toChart j) a :=
      congrFun (T.respectsCell (R.rootCoherence f)) a

/-- A state at every chart, coherent along every ordinary indexing arrow. -/
structure TwoFilteredStateFamily
    {Context : Type u} [Category.{v} Context]
    {J : Type x} [Category.{y} J]
    {D : FunctorialTransportSystem Context}
    {HC : Refinement2CellStructure Context}
    {HJ : Refinement2CellStructure J}
    (R : TwoDimensionalRefinementDiagram Context J HC HJ) where
  state : (j : J) -> D.state.obj (R.chart.obj j)
  coherent : forall {i j : J} (f : i ⟶ j),
    D.transport (R.chart.map f) (state i) = state j

namespace TwoFilteredStateFamily

/-- A root state induces a coherent family through a set-truncated realization. -/
def ofGlobal
    {Context : Type u} [Category.{v} Context]
    {J : Type x} [Category.{y} J]
    {D : FunctorialTransportSystem Context}
    {HC : Refinement2CellStructure Context}
    {HJ : Refinement2CellStructure J}
    (T : SetTruncatedTwoRealization D HC)
    (R : TwoDimensionalRefinementDiagram Context J HC HJ)
    (a : D.state.obj R.rootContext) :
    TwoFilteredStateFamily (D := D) R where
  state := fun j => D.transport (R.toChart j) a
  coherent := by
    intro i j f
    exact root_transport_coherent T R a f

end TwoFilteredStateFamily

/-- Two related indexing paths act identically in a set-truncated realization. -/
theorem transport_eq_of_indexCell
    {Context : Type u} [Category.{v} Context]
    {J : Type x} [Category.{y} J]
    {D : FunctorialTransportSystem Context}
    {HC : Refinement2CellStructure Context}
    {HJ : Refinement2CellStructure J}
    (T : SetTruncatedTwoRealization D HC)
    (R : TwoDimensionalRefinementDiagram Context J HC HJ)
    (s : TwoFilteredStateFamily (D := D) R)
    {i j : J} {f g : i ⟶ j}
    (alpha : HJ.cell f g) :
    D.transport (R.chart.map f) (s.state i) =
      D.transport (R.chart.map g) (s.state i) := by
  exact congrFun (T.respectsCell (R.indexCellMap alpha)) (s.state i)

/--
Parallel refinement paths need not become equal: after a common future they
only need a two-cell, which is enough for a set-truncated realization to make
their state transports agree.
-/
theorem eventual_parallel_transport_agreement
    {Context : Type u} [Category.{v} Context]
    {J : Type x} [Category.{y} J]
    {D : FunctorialTransportSystem Context}
    {HC : Refinement2CellStructure Context}
    {HJ : Refinement2CellStructure J}
    (T : SetTruncatedTwoRealization D HC)
    (H : TwoFilteredIndexing J HJ)
    (R : TwoDimensionalRefinementDiagram Context J HC HJ)
    (s : TwoFilteredStateFamily (D := D) R)
    {i j : J} (f g : i ⟶ j) :
    exists k : J, exists h : j ⟶ k,
      D.transport (R.chart.map (f ≫ h)) (s.state i) =
        D.transport (R.chart.map (g ≫ h)) (s.state i) := by
  rcases H.cohere f g with ⟨k, h, hcell⟩
  rcases hcell with ⟨alpha⟩
  exact ⟨k, h, transport_eq_of_indexCell T R s alpha⟩

/-- A fixed semantic value on all objects of a two-filtered diagram. -/
def TwoFilteredSemanticStabilizesAt
    {Context : Type u} [Category.{v} Context]
    {J : Type x} [Category.{y} J]
    {D : FunctorialTransportSystem Context}
    {HC : Refinement2CellStructure Context}
    {HJ : Refinement2CellStructure J}
    {Semantic : Type r}
    (Q : FunctorialTransportSystem.InvariantReadout D Semantic)
    (R : TwoDimensionalRefinementDiagram Context J HC HJ)
    (s : TwoFilteredStateFamily (D := D) R)
    (value : Semantic) : Prop :=
  forall j, Q.readout (R.chart.obj j) (s.state j) = value

/-- Unique invariant semantic value on a two-filtered diagram. -/
def TwoFilteredSemanticDescends
    {Context : Type u} [Category.{v} Context]
    {J : Type x} [Category.{y} J]
    {D : FunctorialTransportSystem Context}
    {HC : Refinement2CellStructure Context}
    {HJ : Refinement2CellStructure J}
    {Semantic : Type r}
    (Q : FunctorialTransportSystem.InvariantReadout D Semantic)
    (R : TwoDimensionalRefinementDiagram Context J HC HJ)
    (s : TwoFilteredStateFamily (D := D) R) : Prop :=
  ∃! value : Semantic, TwoFilteredSemanticStabilizesAt Q R s value

/-- Invariant semantics agree along every ordinary indexing arrow. -/
theorem semantic_eq_of_hom
    {Context : Type u} [Category.{v} Context]
    {J : Type x} [Category.{y} J]
    {D : FunctorialTransportSystem Context}
    {HC : Refinement2CellStructure Context}
    {HJ : Refinement2CellStructure J}
    {Semantic : Type r}
    (Q : FunctorialTransportSystem.InvariantReadout D Semantic)
    (R : TwoDimensionalRefinementDiagram Context J HC HJ)
    (s : TwoFilteredStateFamily (D := D) R)
    {i j : J} (f : i ⟶ j) :
    Q.readout (R.chart.obj i) (s.state i) =
      Q.readout (R.chart.obj j) (s.state j) := by
  have hInvariant := Q.transport_invariant (R.chart.map f) (s.state i)
  rw [s.coherent f] at hInvariant
  exact hInvariant.symm

/-- The common-future condition identifies semantics at any two objects. -/
theorem semantic_eq
    {Context : Type u} [Category.{v} Context]
    {J : Type x} [Category.{y} J]
    {D : FunctorialTransportSystem Context}
    {HC : Refinement2CellStructure Context}
    {HJ : Refinement2CellStructure J}
    {Semantic : Type r}
    (Q : FunctorialTransportSystem.InvariantReadout D Semantic)
    (H : TwoFilteredIndexing J HJ)
    (R : TwoDimensionalRefinementDiagram Context J HC HJ)
    (s : TwoFilteredStateFamily (D := D) R)
    (i j : J) :
    Q.readout (R.chart.obj i) (s.state i) =
      Q.readout (R.chart.obj j) (s.state j) := by
  rcases H.common i j with ⟨k, hik, hjk⟩
  rcases hik with ⟨fik⟩
  rcases hjk with ⟨fjk⟩
  calc
    Q.readout (R.chart.obj i) (s.state i) =
        Q.readout (R.chart.obj k) (s.state k) :=
      semantic_eq_of_hom Q R s fik
    _ = Q.readout (R.chart.obj j) (s.state j) :=
      (semantic_eq_of_hom Q R s fjk).symm

/--
Higher path information can remain present while unique invariant semantics
still descends.  Only the common-future object condition is needed for this
semantic theorem; eventual two-cell coherence records the stronger path layer.
-/
theorem twoFilteredSemanticDescends_of_coherent
    {Context : Type u} [Category.{v} Context]
    {J : Type x} [Category.{y} J]
    {D : FunctorialTransportSystem Context}
    {HC : Refinement2CellStructure Context}
    {HJ : Refinement2CellStructure J}
    {Semantic : Type r}
    (Q : FunctorialTransportSystem.InvariantReadout D Semantic)
    (H : TwoFilteredIndexing J HJ)
    (R : TwoDimensionalRefinementDiagram Context J HC HJ)
    (s : TwoFilteredStateFamily (D := D) R) :
    TwoFilteredSemanticDescends Q R s := by
  classical
  let anchor : J := Classical.choice H.nonempty
  refine ⟨Q.readout (R.chart.obj anchor) (s.state anchor), ?_, ?_⟩
  · intro j
    exact semantic_eq Q H R s j anchor
  · intro value hValue
    exact (hValue anchor).symm

end KUOS.DependentOriginationTwoCellCoherenceV1_5
