import KUOS.DependentOriginationCausalMonoidalProcessV1_10

namespace KUOS.DependentOriginationMarginalNoSignallingV1_11

open CategoryTheory
open KUOS.DependentOriginationFunctorialTransportV0_1
open KUOS.DependentOriginationMonoidalProcessTheoryV1_9
open KUOS.DependentOriginationCausalMonoidalProcessV1_10

universe u v w

/-!
# Marginals and no-signalling for causal monoidal dependent origination v1.11

The v1.10 layer separates causal orientation from discard normalization.  This
layer uses the same discard maps to define explicit left and right marginals of
states on a tensor product and proves no-signalling for tensor-separated causal
interventions.

The scope is deliberately precise:

* tensor-separated local causal interventions satisfy the opposite-marginal
  no-signalling equations;
* both one-way equations together define the present operational
  `SpacelikeIndependent` predicate;
* arbitrary higher-multicategory joint operations are not inferred to satisfy
  these equations.

Thus causal normalization plus explicit tensor separation gives a genuine
no-signalling theorem, while general joint dependence still requires extra
factorization structure.
-/

/-- Discard the right tensor factor and identify `X ⊗ I` with `X`. -/
def leftMarginalProcess
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    (C : CausalMonoidalProcessStructure Context)
    (X Y : Context) :
    MonoidalCategory.tensorObj X Y ⟶ X :=
  MonoidalCategory.tensorHom (𝟙 X) (C.discard Y) ≫
    (MonoidalCategory.rightUnitor X).hom

/-- Discard the left tensor factor and identify `I ⊗ Y` with `Y`. -/
def rightMarginalProcess
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    (C : CausalMonoidalProcessStructure Context)
    (X Y : Context) :
    MonoidalCategory.tensorObj X Y ⟶ Y :=
  MonoidalCategory.tensorHom (C.discard X) (𝟙 Y) ≫
    (MonoidalCategory.leftUnitor Y).hom

/-- State-level left marginal induced by categorical discarding. -/
def leftMarginal
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    (D : FunctorialTransportSystem Context)
    (C : CausalMonoidalProcessStructure Context)
    {X Y : Context}
    (s : D.state.obj (MonoidalCategory.tensorObj X Y)) :
    D.state.obj X :=
  D.transport (leftMarginalProcess C X Y) s

/-- State-level right marginal induced by categorical discarding. -/
def rightMarginal
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    (D : FunctorialTransportSystem Context)
    (C : CausalMonoidalProcessStructure Context)
    {X Y : Context}
    (s : D.state.obj (MonoidalCategory.tensorObj X Y)) :
    D.state.obj Y :=
  D.transport (rightMarginalProcess C X Y) s

/-- A normalized right factor is recovered by left marginalization of a product state. -/
theorem leftMarginal_tensorState
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {D : FunctorialTransportSystem Context}
    (P : MonoidalProcessTransportSystem Context D)
    (C : CausalMonoidalProcessStructure Context)
    {X Y : Context}
    (x : D.state.obj X)
    (y : NormalizedState P C Y) :
    leftMarginal D C (P.tensorState x y.1) = x := by
  unfold leftMarginal leftMarginalProcess
  rw [D.transport_comp_apply]
  rw [P.tensor_transport]
  rw [D.transport_id_apply]
  rw [y.2]
  exact P.rightUnitor_state x

/-- A normalized left factor is recovered by right marginalization of a product state. -/
theorem rightMarginal_tensorState
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {D : FunctorialTransportSystem Context}
    (P : MonoidalProcessTransportSystem Context D)
    (C : CausalMonoidalProcessStructure Context)
    {X Y : Context}
    (x : NormalizedState P C X)
    (y : D.state.obj Y) :
    rightMarginal D C (P.tensorState x.1 y) = y := by
  unfold rightMarginal rightMarginalProcess
  rw [D.transport_comp_apply]
  rw [P.tensor_transport]
  rw [D.transport_id_apply]
  rw [x.2]
  exact P.leftUnitor_state y

/-!
## Tensor-separated local interventions
-/

/-- Apply a process to the left factor and identity to the right factor. -/
def leftLocalProcess
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {X X' : Context}
    (f : X ⟶ X')
    (Y : Context) :
    MonoidalCategory.tensorObj X Y ⟶
      MonoidalCategory.tensorObj X' Y :=
  MonoidalCategory.tensorHom f (𝟙 Y)

/-- Apply a process to the right factor and identity to the left factor. -/
def rightLocalProcess
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    (X : Context)
    {Y Y' : Context}
    (g : Y ⟶ Y') :
    MonoidalCategory.tensorObj X Y ⟶
      MonoidalCategory.tensorObj X Y' :=
  MonoidalCategory.tensorHom (𝟙 X) g

/--
A causal left-local intervention followed by right marginalization is exactly
right marginalization before the intervention.
-/
theorem rightMarginalProcess_after_left_causal
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {C : CausalMonoidalProcessStructure Context}
    {X X' Y : Context}
    (f : CausalIntervention C X X') :
    leftLocalProcess f.process Y ≫ rightMarginalProcess C X' Y =
      rightMarginalProcess C X Y := by
  unfold leftLocalProcess rightMarginalProcess
  rw [Category.assoc]
  rw [MonoidalCategory.tensorHom_comp_tensorHom]
  rw [f.causal]
  simp

/--
A causal right-local intervention followed by left marginalization is exactly
left marginalization before the intervention.
-/
theorem leftMarginalProcess_after_right_causal
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {C : CausalMonoidalProcessStructure Context}
    {X Y Y' : Context}
    (g : CausalIntervention C Y Y') :
    rightLocalProcess X g.process ≫ leftMarginalProcess C X Y' =
      leftMarginalProcess C X Y := by
  unfold rightLocalProcess leftMarginalProcess
  rw [Category.assoc]
  rw [MonoidalCategory.tensorHom_comp_tensorHom]
  rw [g.causal]
  simp

/-- Left intervention cannot change the right marginal. -/
theorem rightMarginal_after_leftIntervention
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {D : FunctorialTransportSystem Context}
    {C : CausalMonoidalProcessStructure Context}
    {X X' Y : Context}
    (f : CausalIntervention C X X')
    (s : D.state.obj (MonoidalCategory.tensorObj X Y)) :
    rightMarginal D C
        (D.transport (leftLocalProcess f.process Y) s) =
      rightMarginal D C s := by
  unfold rightMarginal
  calc
    D.transport (rightMarginalProcess C X' Y)
        (D.transport (leftLocalProcess f.process Y) s) =
      D.transport
        (leftLocalProcess f.process Y ≫ rightMarginalProcess C X' Y) s :=
      (D.transport_comp_apply _ _ _).symm
    _ = D.transport (rightMarginalProcess C X Y) s := by
      rw [rightMarginalProcess_after_left_causal f]

/-- Right intervention cannot change the left marginal. -/
theorem leftMarginal_after_rightIntervention
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {D : FunctorialTransportSystem Context}
    {C : CausalMonoidalProcessStructure Context}
    {X Y Y' : Context}
    (g : CausalIntervention C Y Y')
    (s : D.state.obj (MonoidalCategory.tensorObj X Y)) :
    leftMarginal D C
        (D.transport (rightLocalProcess X g.process) s) =
      leftMarginal D C s := by
  unfold leftMarginal
  calc
    D.transport (leftMarginalProcess C X Y')
        (D.transport (rightLocalProcess X g.process) s) =
      D.transport
        (rightLocalProcess X g.process ≫ leftMarginalProcess C X Y') s :=
      (D.transport_comp_apply _ _ _).symm
    _ = D.transport (leftMarginalProcess C X Y) s := by
      rw [leftMarginalProcess_after_right_causal g]

/-!
## Explicit no-signalling predicates
-/

/-- Operational one-way no-signalling from the left intervention to the right marginal. -/
def OneWayNoSignallingLeftToRight
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    (D : FunctorialTransportSystem Context)
    (C : CausalMonoidalProcessStructure Context)
    {X X' Y : Context}
    (f : CausalIntervention C X X') : Prop :=
  forall s : D.state.obj (MonoidalCategory.tensorObj X Y),
    rightMarginal D C
        (D.transport (leftLocalProcess f.process Y) s) =
      rightMarginal D C s

/-- Operational one-way no-signalling from the right intervention to the left marginal. -/
def OneWayNoSignallingRightToLeft
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    (D : FunctorialTransportSystem Context)
    (C : CausalMonoidalProcessStructure Context)
    {X Y Y' : Context}
    (g : CausalIntervention C Y Y') : Prop :=
  forall s : D.state.obj (MonoidalCategory.tensorObj X Y),
    leftMarginal D C
        (D.transport (rightLocalProcess X g.process) s) =
      leftMarginal D C s

/-- Tensor-separated causal interventions satisfy left-to-right no-signalling. -/
theorem causal_left_noSignalling
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {D : FunctorialTransportSystem Context}
    {C : CausalMonoidalProcessStructure Context}
    {X X' Y : Context}
    (f : CausalIntervention C X X') :
    OneWayNoSignallingLeftToRight D C (Y := Y) f := by
  intro s
  exact rightMarginal_after_leftIntervention f s

/-- Tensor-separated causal interventions satisfy right-to-left no-signalling. -/
theorem causal_right_noSignalling
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {D : FunctorialTransportSystem Context}
    {C : CausalMonoidalProcessStructure Context}
    {X Y Y' : Context}
    (g : CausalIntervention C Y Y') :
    OneWayNoSignallingRightToLeft D C (X := X) g := by
  intro s
  exact leftMarginal_after_rightIntervention g s

/--
Current operational spacelike independence: each tensor-separated local causal
intervention leaves the opposite marginal invariant.
-/
def SpacelikeIndependent
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    (D : FunctorialTransportSystem Context)
    (C : CausalMonoidalProcessStructure Context)
    {X X' Y Y' : Context}
    (f : CausalIntervention C X X')
    (g : CausalIntervention C Y Y') : Prop :=
  OneWayNoSignallingLeftToRight D C (Y := Y) f ∧
    OneWayNoSignallingRightToLeft D C (X := X) g

/-- Any pair of tensor-separated causal interventions is spacelike independent in the v1.11 sense. -/
theorem tensorSeparated_causal_spacelikeIndependent
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {D : FunctorialTransportSystem Context}
    {C : CausalMonoidalProcessStructure Context}
    {X X' Y Y' : Context}
    (f : CausalIntervention C X X')
    (g : CausalIntervention C Y Y') :
    SpacelikeIndependent D C f g := by
  constructor
  · exact causal_left_noSignalling f
  · exact causal_right_noSignalling g

/-!
The hierarchy is now:

```text
causal discard normalization
  -> explicit tensor marginals
  -> one-way no-signalling for tensor-separated causal interventions
  -> two-way operational spacelike independence
```

This theorem does not extend automatically to arbitrary operadic joint
conditions.  Such a process may couple the factors and requires an explicit
factorization or marginal law before the no-signalling name is justified.
-/

end KUOS.DependentOriginationMarginalNoSignallingV1_11
