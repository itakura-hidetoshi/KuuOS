import Mathlib
import KUOS.DependentOriginationDirectedCofinalSemanticsV1_3

namespace KUOS.DependentOriginationFilteredCofinalCategoryV1_4

open CategoryTheory
open KUOS.DependentOriginationFunctorialTransportV0_1
open KUOS.DependentOriginationContextualCoreV1_0
open KUOS.DependentOriginationContextualDescentV1_1
open KUOS.DependentOriginationRefinementTransitivityV1_2
open KUOS.DependentOriginationDirectedCofinalSemanticsV1_3

universe u v w x z q y

/-!
# Filtered categorical refinement and cofinal semantics v1.4

The v1.3 layer used a preorder-indexed directed refinement net.  This layer
removes the assumption that refinement indices form a preorder.  Refinement may
have several parallel arrows and therefore carries path information.

The parent structure remains non-quantum and covariant:

```text
root context -> diagram object i -> diagram object j
```

for an arbitrary indexing category.  A filtered indexing certificate records
three pieces of finite consistency:

* the index category is inhabited;
* every two objects admit a common future object;
* every two parallel arrows become equal after a further arrow.

No categorical colimit is assumed.  In particular, the existence of one root
state producing all diagram states remains a separate predicate.

Semantic invariance is stronger.  A coherent state family and an invariant
readout have one unique value on a filtered diagram, and that value can be read
on any explicitly cofinal indexing functor.  Recovering a root-state witness
from the cofinal subsystem still requires an explicit state-separation
hypothesis.
-/

/--
An explicit filteredness certificate for an indexing category.

`common` is the object-amalgamation condition.  `coequalize` records eventual
agreement of parallel arrows.  The semantic theorems below only need `common`,
but the full certificate keeps the categorical refinement carrier honest when
path multiplicity is present.
-/
structure FilteredIndexing
    (J : Type w) [Category.{x} J] where
  nonempty : Nonempty J
  common : forall i j : J,
    exists k : J, Nonempty (i ⟶ k) ∧ Nonempty (j ⟶ k)
  coequalize : forall {i j : J} (f g : i ⟶ j),
    exists k : J, exists h : j ⟶ k, f ≫ h = g ≫ h

/--
A contextual refinement diagram indexed by an arbitrary category.

The root-to-object arrows form a strict cocone over `chart`: following a root
arrow by any indexing morphism gives the chosen root arrow at the target.
-/
structure FilteredRefinementDiagram
    (Context : Type u) [Category.{v} Context]
    (J : Type w) [Category.{x} J] where
  rootContext : Context
  chart : J ⥤ Context
  toChart : (j : J) -> rootContext ⟶ chart.obj j
  root_naturality : forall {i j : J} (f : i ⟶ j),
    toChart i ≫ chart.map f = toChart j

namespace FilteredRefinementDiagram

/-- Change the indexing category by precomposition. -/
def reindex
    {Context : Type u} [Category.{v} Context]
    {J : Type w} [Category.{x} J]
    {K : Type z} [Category.{q} K]
    (R : FilteredRefinementDiagram Context J)
    (F : K ⥤ J) :
    FilteredRefinementDiagram Context K where
  rootContext := R.rootContext
  chart := F ⋙ R.chart
  toChart := fun k => R.toChart (F.obj k)
  root_naturality := by
    intro i j f
    simpa using R.root_naturality (F.map f)

end FilteredRefinementDiagram

/-- Root transport followed by one indexing arrow equals direct root transport. -/
theorem root_transport_hom
    {Context : Type u} [Category.{v} Context]
    {J : Type w} [Category.{x} J]
    (D : FunctorialTransportSystem Context)
    (R : FilteredRefinementDiagram Context J)
    (a : D.state.obj R.rootContext)
    {i j : J} (f : i ⟶ j) :
    D.transport (R.chart.map f) (D.transport (R.toChart i) a) =
      D.transport (R.toChart j) a := by
  rw [← D.transport_comp_apply (R.toChart i) (R.chart.map f) a]
  rw [R.root_naturality f]

/-- A state at every diagram object, coherent under every indexing morphism. -/
structure FilteredStateFamily
    {Context : Type u} [Category.{v} Context]
    {J : Type w} [Category.{x} J]
    (D : FunctorialTransportSystem Context)
    (R : FilteredRefinementDiagram Context J) where
  state : (j : J) -> D.state.obj (R.chart.obj j)
  coherent : forall {i j : J} (f : i ⟶ j),
    D.transport (R.chart.map f) (state i) = state j

namespace FilteredStateFamily

/-- A root state induces a coherent family on every filtered refinement diagram. -/
def ofGlobal
    {Context : Type u} [Category.{v} Context]
    {J : Type w} [Category.{x} J]
    (D : FunctorialTransportSystem Context)
    (R : FilteredRefinementDiagram Context J)
    (a : D.state.obj R.rootContext) :
    FilteredStateFamily D R where
  state := fun j => D.transport (R.toChart j) a
  coherent := by
    intro i j f
    exact root_transport_hom D R a f

/-- Restrict a coherent family along a change of indexing category. -/
def reindex
    {Context : Type u} [Category.{v} Context]
    {J : Type w} [Category.{x} J]
    {K : Type z} [Category.{q} K]
    {D : FunctorialTransportSystem Context}
    {R : FilteredRefinementDiagram Context J}
    (s : FilteredStateFamily D R)
    (F : K ⥤ J) :
    FilteredStateFamily D (R.reindex F) where
  state := fun k => s.state (F.obj k)
  coherent := by
    intro i j f
    simpa [FilteredRefinementDiagram.reindex] using s.coherent (F.map f)

end FilteredStateFamily

/-- A filtered diagram state family has a root-state witness. -/
def StateDescendsOnFilteredDiagram
    {Context : Type u} [Category.{v} Context]
    {J : Type w} [Category.{x} J]
    (D : FunctorialTransportSystem Context)
    (R : FilteredRefinementDiagram Context J)
    (s : FilteredStateFamily D R) : Prop :=
  exists a : D.state.obj R.rootContext,
    forall j, D.transport (R.toChart j) a = s.state j

/-- The family generated from a root state descends with that root state. -/
theorem ofGlobal_stateDescendsOnFilteredDiagram
    {Context : Type u} [Category.{v} Context]
    {J : Type w} [Category.{x} J]
    (D : FunctorialTransportSystem Context)
    (R : FilteredRefinementDiagram Context J)
    (a : D.state.obj R.rootContext) :
    StateDescendsOnFilteredDiagram D R (FilteredStateFamily.ofGlobal D R a) := by
  refine ⟨a, ?_⟩
  intro j
  rfl

/-- A fixed semantic value is shared by every object of the filtered diagram. -/
def FilteredSemanticStabilizesAt
    {Context : Type u} [Category.{v} Context]
    {J : Type w} [Category.{x} J]
    {D : FunctorialTransportSystem Context}
    {Semantic : Type y}
    (Q : FunctorialTransportSystem.InvariantReadout D Semantic)
    (R : FilteredRefinementDiagram Context J)
    (s : FilteredStateFamily D R)
    (value : Semantic) : Prop :=
  forall j, Q.readout (R.chart.obj j) (s.state j) = value

/-- Unique invariant semantic descent on an arbitrary filtered diagram. -/
def FilteredSemanticDescends
    {Context : Type u} [Category.{v} Context]
    {J : Type w} [Category.{x} J]
    {D : FunctorialTransportSystem Context}
    {Semantic : Type y}
    (Q : FunctorialTransportSystem.InvariantReadout D Semantic)
    (R : FilteredRefinementDiagram Context J)
    (s : FilteredStateFamily D R) : Prop :=
  exists! value : Semantic, FilteredSemanticStabilizesAt Q R s value

/-- Invariant semantics agree along every indexing morphism. -/
theorem semantic_eq_of_hom
    {Context : Type u} [Category.{v} Context]
    {J : Type w} [Category.{x} J]
    {D : FunctorialTransportSystem Context}
    {Semantic : Type y}
    (Q : FunctorialTransportSystem.InvariantReadout D Semantic)
    (R : FilteredRefinementDiagram Context J)
    (s : FilteredStateFamily D R)
    {i j : J} (f : i ⟶ j) :
    Q.readout (R.chart.obj i) (s.state i) =
      Q.readout (R.chart.obj j) (s.state j) := by
  have hInvariant := Q.transport_invariant (R.chart.map f) (s.state i)
  rw [s.coherent f] at hInvariant
  exact hInvariant.symm

/-- The common-target part of filteredness identifies semantics at any two objects. -/
theorem semantic_eq
    {Context : Type u} [Category.{v} Context]
    {J : Type w} [Category.{x} J]
    {D : FunctorialTransportSystem Context}
    {Semantic : Type y}
    (Q : FunctorialTransportSystem.InvariantReadout D Semantic)
    (H : FilteredIndexing J)
    (R : FilteredRefinementDiagram Context J)
    (s : FilteredStateFamily D R)
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

/-- Every coherent state family on a filtered indexing category has one unique meaning. -/
theorem filteredSemanticDescends_of_coherent
    {Context : Type u} [Category.{v} Context]
    {J : Type w} [Category.{x} J]
    {D : FunctorialTransportSystem Context}
    {Semantic : Type y}
    (Q : FunctorialTransportSystem.InvariantReadout D Semantic)
    (H : FilteredIndexing J)
    (R : FilteredRefinementDiagram Context J)
    (s : FilteredStateFamily D R) :
    FilteredSemanticDescends Q R s := by
  classical
  let anchor : J := Classical.choice H.nonempty
  refine ⟨Q.readout (R.chart.obj anchor) (s.state anchor), ?_, ?_⟩
  · intro j
    exact semantic_eq Q H R s j anchor
  · intro value hValue
    exact (hValue anchor).symm

/-!
## Cofinal changes of indexing category
-/

/--
An explicit objectwise cofinal indexing functor.

Every object of `J` admits a morphism into an object selected from `K`.  This is
the categorical analogue needed for the semantic theorem below.  We deliberately
do not identify this structure with Mathlib's strongest final-functor API or
assert a colimit theorem.
-/
structure CofinalIndexingFunctor
    (J : Type w) [Category.{x} J]
    (K : Type z) [Category.{q} K] where
  functor : K ⥤ J
  reaches : forall j : J, exists k : K, Nonempty (j ⟶ functor.obj k)

/-- A fixed semantic value tested only on objects selected by a cofinal functor. -/
def CofinalSemanticStabilizesAt
    {Context : Type u} [Category.{v} Context]
    {J : Type w} [Category.{x} J]
    {K : Type z} [Category.{q} K]
    {D : FunctorialTransportSystem Context}
    {Semantic : Type y}
    (Q : FunctorialTransportSystem.InvariantReadout D Semantic)
    (R : FilteredRefinementDiagram Context J)
    (s : FilteredStateFamily D R)
    (F : CofinalIndexingFunctor J K)
    (value : Semantic) : Prop :=
  forall k,
    Q.readout (R.chart.obj (F.functor.obj k))
      (s.state (F.functor.obj k)) = value

/-- Unique semantic descent tested only after an objectwise cofinal reindexing. -/
def CofinalSemanticDescends
    {Context : Type u} [Category.{v} Context]
    {J : Type w} [Category.{x} J]
    {K : Type z} [Category.{q} K]
    {D : FunctorialTransportSystem Context}
    {Semantic : Type y}
    (Q : FunctorialTransportSystem.InvariantReadout D Semantic)
    (R : FilteredRefinementDiagram Context J)
    (s : FilteredStateFamily D R)
    (F : CofinalIndexingFunctor J K) : Prop :=
  exists! value : Semantic,
    CofinalSemanticStabilizesAt Q R s F value

/-- Stabilization on the full diagram is equivalent to stabilization on a cofinal index change. -/
theorem filteredSemanticStabilizesAt_iff_cofinal
    {Context : Type u} [Category.{v} Context]
    {J : Type w} [Category.{x} J]
    {K : Type z} [Category.{q} K]
    {D : FunctorialTransportSystem Context}
    {Semantic : Type y}
    (Q : FunctorialTransportSystem.InvariantReadout D Semantic)
    (R : FilteredRefinementDiagram Context J)
    (s : FilteredStateFamily D R)
    (F : CofinalIndexingFunctor J K)
    (value : Semantic) :
    FilteredSemanticStabilizesAt Q R s value <->
      CofinalSemanticStabilizesAt Q R s F value := by
  constructor
  · intro h k
    exact h (F.functor.obj k)
  · intro h j
    rcases F.reaches j with ⟨k, hk⟩
    rcases hk with ⟨f⟩
    calc
      Q.readout (R.chart.obj j) (s.state j) =
          Q.readout (R.chart.obj (F.functor.obj k))
            (s.state (F.functor.obj k)) :=
        semantic_eq_of_hom Q R s f
      _ = value := h k

/--
Unique semantic descent is exactly invariant under an objectwise cofinal change
of indexing category.
-/
theorem filteredSemanticDescends_iff_cofinal
    {Context : Type u} [Category.{v} Context]
    {J : Type w} [Category.{x} J]
    {K : Type z} [Category.{q} K]
    {D : FunctorialTransportSystem Context}
    {Semantic : Type y}
    (Q : FunctorialTransportSystem.InvariantReadout D Semantic)
    (R : FilteredRefinementDiagram Context J)
    (s : FilteredStateFamily D R)
    (F : CofinalIndexingFunctor J K) :
    FilteredSemanticDescends Q R s <->
      CofinalSemanticDescends Q R s F := by
  constructor
  · rintro ⟨value, hValue, hUnique⟩
    refine ⟨value, ?_, ?_⟩
    · intro k
      exact hValue (F.functor.obj k)
    · intro value' hValue'
      apply hUnique
      exact (filteredSemanticStabilizesAt_iff_cofinal Q R s F value').2 hValue'
  · rintro ⟨value, hValue, hUnique⟩
    refine ⟨value, ?_, ?_⟩
    · exact (filteredSemanticStabilizesAt_iff_cofinal Q R s F value).2 hValue
    · intro value' hValue'
      apply hUnique
      intro k
      exact hValue' (F.functor.obj k)

/-- A root state matches the family on every object selected by a cofinal functor. -/
def CofinalStateWitness
    {Context : Type u} [Category.{v} Context]
    {J : Type w} [Category.{x} J]
    {K : Type z} [Category.{q} K]
    (D : FunctorialTransportSystem Context)
    (R : FilteredRefinementDiagram Context J)
    (s : FilteredStateFamily D R)
    (F : CofinalIndexingFunctor J K) : Prop :=
  exists a : D.state.obj R.rootContext,
    forall k,
      D.transport (R.toChart (F.functor.obj k)) a =
        s.state (F.functor.obj k)

/-- Full state descent always restricts to a cofinal state witness. -/
theorem cofinalStateWitness_of_stateDescends
    {Context : Type u} [Category.{v} Context]
    {J : Type w} [Category.{x} J]
    {K : Type z} [Category.{q} K]
    (D : FunctorialTransportSystem Context)
    (R : FilteredRefinementDiagram Context J)
    (s : FilteredStateFamily D R)
    (F : CofinalIndexingFunctor J K)
    (h : StateDescendsOnFilteredDiagram D R s) :
    CofinalStateWitness D R s F := by
  rcases h with ⟨a, ha⟩
  refine ⟨a, ?_⟩
  intro k
  exact ha (F.functor.obj k)

/--
The cofinal indexing lens separates local states when equality after transport to
every selected future object forces equality already at the original object.
-/
def CofinalFunctorSeparatesLocalStates
    {Context : Type u} [Category.{v} Context]
    {J : Type w} [Category.{x} J]
    {K : Type z} [Category.{q} K]
    (D : FunctorialTransportSystem Context)
    (R : FilteredRefinementDiagram Context J)
    (F : CofinalIndexingFunctor J K) : Prop :=
  forall (j : J)
    (a b : D.state.obj (R.chart.obj j)),
    (forall (k : K) (f : j ⟶ F.functor.obj k),
      D.transport (R.chart.map f) a =
        D.transport (R.chart.map f) b) ->
    a = b

/--
With explicit local-state separation, a cofinal root-state witness extends to a
root-state witness on the whole filtered diagram.
-/
theorem stateDescends_iff_cofinalStateWitness_of_separates
    {Context : Type u} [Category.{v} Context]
    {J : Type w} [Category.{x} J]
    {K : Type z} [Category.{q} K]
    (D : FunctorialTransportSystem Context)
    (R : FilteredRefinementDiagram Context J)
    (s : FilteredStateFamily D R)
    (F : CofinalIndexingFunctor J K)
    (hSeparate : CofinalFunctorSeparatesLocalStates D R F) :
    StateDescendsOnFilteredDiagram D R s <->
      CofinalStateWitness D R s F := by
  constructor
  · exact cofinalStateWitness_of_stateDescends D R s F
  · rintro ⟨a, ha⟩
    refine ⟨a, ?_⟩
    intro j
    apply hSeparate j
    intro k f
    calc
      D.transport (R.chart.map f) (D.transport (R.toChart j) a) =
          D.transport (R.toChart (F.functor.obj k)) a :=
        root_transport_hom D R a f
      _ = s.state (F.functor.obj k) := ha k
      _ = D.transport (R.chart.map f) (s.state j) :=
        (s.coherent f).symm

/-- Under separation, absence of a global root witness is already visible cofinally. -/
theorem no_cofinalStateWitness_of_no_stateDescends
    {Context : Type u} [Category.{v} Context]
    {J : Type w} [Category.{x} J]
    {K : Type z} [Category.{q} K]
    (D : FunctorialTransportSystem Context)
    (R : FilteredRefinementDiagram Context J)
    (s : FilteredStateFamily D R)
    (F : CofinalIndexingFunctor J K)
    (hSeparate : CofinalFunctorSeparatesLocalStates D R F)
    (hNoState : ¬ StateDescendsOnFilteredDiagram D R s) :
    ¬ CofinalStateWitness D R s F := by
  intro hCofinal
  apply hNoState
  exact (stateDescends_iff_cofinalStateWitness_of_separates
    D R s F hSeparate).2 hCofinal

/--
A cofinal indexing change can preserve one unique invariant meaning even when,
under an explicit separation hypothesis, no root-state carrier exists either
globally or on the cofinal subsystem.
-/
theorem semantic_persists_without_cofinal_root_carrier
    {Context : Type u} [Category.{v} Context]
    {J : Type w} [Category.{x} J]
    {K : Type z} [Category.{q} K]
    {D : FunctorialTransportSystem Context}
    {Semantic : Type y}
    (Q : FunctorialTransportSystem.InvariantReadout D Semantic)
    (H : FilteredIndexing J)
    (R : FilteredRefinementDiagram Context J)
    (s : FilteredStateFamily D R)
    (F : CofinalIndexingFunctor J K)
    (hSeparate : CofinalFunctorSeparatesLocalStates D R F)
    (hNoState : ¬ StateDescendsOnFilteredDiagram D R s) :
    (¬ CofinalStateWitness D R s F) ∧
      CofinalSemanticDescends Q R s F := by
  constructor
  · exact no_cofinalStateWitness_of_no_stateDescends
      D R s F hSeparate hNoState
  · apply (filteredSemanticDescends_iff_cofinal Q R s F).1
    exact filteredSemanticDescends_of_coherent Q H R s

end KUOS.DependentOriginationFilteredCofinalCategoryV1_4
