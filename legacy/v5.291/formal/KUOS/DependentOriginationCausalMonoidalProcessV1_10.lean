import KUOS.DependentOriginationMonoidalProcessTheoryV1_9

namespace KUOS.DependentOriginationCausalMonoidalProcessV1_10

open CategoryTheory
open KUOS.DependentOriginationFunctorialTransportV0_1
open KUOS.DependentOriginationMonoidalProcessTheoryV1_9

universe u v w

/-!
# Causal monoidal dependent-origination process structure v1.10

The v1.9 layer provides sequential and independent parallel process composition.
This layer adds a causal axis without reducing dependent origination to a causal
DAG.

Two structures are kept distinct:

* `CausalOrder` records an orientation relation on contexts and requires every
  admitted process arrow to respect that orientation;
* `CausalMonoidalProcessStructure` supplies categorical discarding and defines a
  process to be causal when discarding after the process equals discarding before
  it.

The distinction matters.  Direction of admissible dependence and normalization
of a process are related but not identical notions.

The main closure results are:

* identity processes are causal;
* causal processes compose sequentially;
* causal processes tensor in parallel;
* causal interventions therefore form a sequential/parallel subtheory;
* causal interventions preserve normalized states;
* tensoring normalized states preserves normalization.

This layer does not claim general no-signalling for arbitrary joint processes.
That stronger condition requires explicit marginal/factorization hypotheses.
-/

/--
A preorder-like causal orientation on contextual process interfaces.

Every admitted category morphism must point along the relation.  Tensoring two
oriented pairs preserves the orientation, expressing compatibility of causal
order with independent parallel composition.
-/
structure CausalOrder
    (Context : Type u) [Category.{v} Context] [MonoidalCategory Context] where
  precedes : Context -> Context -> Prop
  refl : forall X : Context, precedes X X
  trans : forall {X Y Z : Context},
    precedes X Y -> precedes Y Z -> precedes X Z
  hom_precedes : forall {X Y : Context}, (X ⟶ Y) -> precedes X Y
  tensor_precedes : forall {X₁ Y₁ X₂ Y₂ : Context},
    precedes X₁ Y₁ -> precedes X₂ Y₂ ->
      precedes
        (MonoidalCategory.tensorObj X₁ X₂)
        (MonoidalCategory.tensorObj Y₁ Y₂)

namespace CausalOrder

/-- If the causal orientation forbids `X` before `Y`, there is no admitted process arrow `X ⟶ Y`. -/
theorem no_process_against_order
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    (C : CausalOrder Context)
    {X Y : Context}
    (h : ¬ C.precedes X Y) :
    IsEmpty (X ⟶ Y) :=
  ⟨fun f => h (C.hom_precedes f)⟩

end CausalOrder

/--
Causal normalization data on a native monoidal process category.

`discard X : X ⟶ I` forgets the output system.  A process is causal exactly when
it preserves discarding.  The tensor law says that independently discarding two
parallel systems is the same as discarding their tensor product, modulo the
native left unitor on the monoidal unit.
-/
structure CausalMonoidalProcessStructure
    (Context : Type u) [Category.{v} Context] [MonoidalCategory Context] where
  order : CausalOrder Context
  discard : (X : Context) -> X ⟶ MonoidalCategory.tensorUnit Context
  discard_unit :
    discard (MonoidalCategory.tensorUnit Context) =
      𝟙 (MonoidalCategory.tensorUnit Context)
  discard_tensor : forall X Y : Context,
    discard (MonoidalCategory.tensorObj X Y) =
      MonoidalCategory.tensorHom (discard X) (discard Y) ≫
        (MonoidalCategory.leftUnitor
          (MonoidalCategory.tensorUnit Context)).hom

namespace CausalMonoidalProcessStructure

/-- A process is causal when discarding its output equals discarding its input. -/
def IsCausal
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    (C : CausalMonoidalProcessStructure Context)
    {X Y : Context}
    (f : X ⟶ Y) : Prop :=
  f ≫ C.discard Y = C.discard X

/-- Identity is causally normalized. -/
@[simp] theorem isCausal_id
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    (C : CausalMonoidalProcessStructure Context)
    (X : Context) :
    C.IsCausal (𝟙 X) := by
  unfold IsCausal
  simp

/-- Sequential composition of causal processes is causal. -/
theorem isCausal_comp
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    (C : CausalMonoidalProcessStructure Context)
    {X Y Z : Context}
    {f : X ⟶ Y} {g : Y ⟶ Z}
    (hf : C.IsCausal f)
    (hg : C.IsCausal g) :
    C.IsCausal (f ≫ g) := by
  unfold IsCausal at hf hg ⊢
  rw [Category.assoc, hg, hf]

/-- Independent parallel composition of causal processes is causal. -/
theorem isCausal_tensor
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    (C : CausalMonoidalProcessStructure Context)
    {X₁ Y₁ X₂ Y₂ : Context}
    {f : X₁ ⟶ Y₁} {g : X₂ ⟶ Y₂}
    (hf : C.IsCausal f)
    (hg : C.IsCausal g) :
    C.IsCausal (MonoidalCategory.tensorHom f g) := by
  unfold IsCausal at hf hg ⊢
  rw [C.discard_tensor Y₁ Y₂, C.discard_tensor X₁ X₂]
  rw [Category.assoc]
  rw [MonoidalCategory.tensorHom_comp_tensorHom]
  rw [hf, hg]

/-- Every admitted process follows the declared causal orientation. -/
theorem process_precedes
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    (C : CausalMonoidalProcessStructure Context)
    {X Y : Context}
    (f : X ⟶ Y) :
    C.order.precedes X Y :=
  C.order.hom_precedes f

end CausalMonoidalProcessStructure

/-- A causal intervention is an admitted process together with its discard-preservation certificate. -/
structure CausalIntervention
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    (C : CausalMonoidalProcessStructure Context)
    (X Y : Context) where
  process : X ⟶ Y
  causal : C.IsCausal process

namespace CausalIntervention

/-- Identity intervention. -/
def id
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    (C : CausalMonoidalProcessStructure Context)
    (X : Context) :
    CausalIntervention C X X where
  process := 𝟙 X
  causal := C.isCausal_id X

/-- Sequential composition of interventions. -/
def comp
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {C : CausalMonoidalProcessStructure Context}
    {X Y Z : Context}
    (f : CausalIntervention C X Y)
    (g : CausalIntervention C Y Z) :
    CausalIntervention C X Z where
  process := f.process ≫ g.process
  causal := C.isCausal_comp f.causal g.causal

/-- Independent parallel tensor product of interventions. -/
def tensor
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {C : CausalMonoidalProcessStructure Context}
    {X₁ Y₁ X₂ Y₂ : Context}
    (f : CausalIntervention C X₁ Y₁)
    (g : CausalIntervention C X₂ Y₂) :
    CausalIntervention C
      (MonoidalCategory.tensorObj X₁ X₂)
      (MonoidalCategory.tensorObj Y₁ Y₂) where
  process := MonoidalCategory.tensorHom f.process g.process
  causal := C.isCausal_tensor f.causal g.causal

/-- Every causal intervention also respects the declared orientation. -/
theorem precedes
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {C : CausalMonoidalProcessStructure Context}
    {X Y : Context}
    (f : CausalIntervention C X Y) :
    C.order.precedes X Y :=
  C.order.hom_precedes f.process

/-- Parallel interventions respect the tensor-compatible causal orientation. -/
theorem tensor_precedes
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {C : CausalMonoidalProcessStructure Context}
    {X₁ Y₁ X₂ Y₂ : Context}
    (f : CausalIntervention C X₁ Y₁)
    (g : CausalIntervention C X₂ Y₂) :
    C.order.precedes
      (MonoidalCategory.tensorObj X₁ X₂)
      (MonoidalCategory.tensorObj Y₁ Y₂) :=
  C.order.tensor_precedes f.precedes g.precedes

end CausalIntervention

/-!
## Normalized state realization
-/

/--
A state is normalized when discarding it gives the monoidal unit state supplied
by the v1.9 process realization.
-/
def NormalizedState
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {D : FunctorialTransportSystem Context}
    (P : MonoidalProcessTransportSystem Context D)
    (C : CausalMonoidalProcessStructure Context)
    (X : Context) :=
  {x : D.state.obj X //
    D.transport (C.discard X) x = P.unitState}

namespace CausalIntervention

/-- Causal intervention preserves normalization. -/
def mapNormalized
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {D : FunctorialTransportSystem Context}
    (P : MonoidalProcessTransportSystem Context D)
    {C : CausalMonoidalProcessStructure Context}
    {X Y : Context}
    (f : CausalIntervention C X Y)
    (x : NormalizedState P C X) :
    NormalizedState P C Y :=
  ⟨D.transport f.process x.1, by
    calc
      D.transport (C.discard Y) (D.transport f.process x.1) =
          D.transport (f.process ≫ C.discard Y) x.1 :=
        (D.transport_comp_apply f.process (C.discard Y) x.1).symm
      _ = D.transport (C.discard X) x.1 := by
        rw [f.causal]
      _ = P.unitState := x.2⟩

end CausalIntervention

/-- Parallel tensoring of normalized states is normalized. -/
def tensorNormalized
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {D : FunctorialTransportSystem Context}
    (P : MonoidalProcessTransportSystem Context D)
    (C : CausalMonoidalProcessStructure Context)
    {X Y : Context}
    (x : NormalizedState P C X)
    (y : NormalizedState P C Y) :
    NormalizedState P C (MonoidalCategory.tensorObj X Y) :=
  ⟨P.tensorState x.1 y.1, by
    rw [C.discard_tensor X Y]
    rw [D.transport_comp_apply]
    rw [P.tensor_transport]
    rw [x.2, y.2]
    exact P.leftUnitor_state P.unitState⟩

/-!
The causal hierarchy is intentionally conservative:

```text
general dependent origination
  -> monoidal process structure
  -> causal orientation + discard normalization
  -> causal interventions closed under sequential/parallel composition
  -> normalized-state preservation
```

This does not identify causality with Markovianity and does not claim that every
joint multi-condition process is no-signalling.  A later layer may add explicit
marginal/no-signalling factorization while retaining memory and higher path data.
-/

end KUOS.DependentOriginationCausalMonoidalProcessV1_10
