import KUOS.DependentOriginationHigherMulticategoryCoherenceV1_8
import KUOS.DependentOriginationMarginalNoSignallingV1_11

namespace KUOS.DependentOriginationJointCausalFactorizationV1_12

open CategoryTheory
open KUOS.DependentOriginationFunctorialTransportV0_1
open KUOS.DependentOriginationOperadicMultiConditionV1_7
open KUOS.DependentOriginationHigherMulticategoryCoherenceV1_8
open KUOS.DependentOriginationMonoidalProcessTheoryV1_9
open KUOS.DependentOriginationCausalMonoidalProcessV1_10
open KUOS.DependentOriginationMarginalNoSignallingV1_11

universe u v w z

/-!
# Joint causal factorization for dependent origination v1.12

The v1.8 higher-multicategory layer permits genuinely joint multi-condition
operations.  The v1.11 causal-process layer proves no-signalling only in an
explicit tensor-separated sector.  This file connects those two axes without
identifying them.

For a binary joint operation

```text
(X, Y) -> X' ⊗ Y'
```

we introduce an explicit `CausalTensorFactorization` certificate.  Such a
certificate says that, on product inputs, evaluation of the joint primitive is
exactly the tensor state obtained by two causal local interventions.

The resulting theorem is deliberately one-way:

```text
causal tensor factorization
  -> joint no-signalling on normalized varied inputs.
```

Arbitrary higher-multicategory joint operations do not receive this property.
The higher operation two-cell remains source data; the current algebra is
set-truncated, so factorization and no-signalling transport across represented
operation cells.
-/

/-- Two input colors, in left/right order. -/
def binaryInputs (X Y : Type u) : Fin 2 -> Type u :=
  Fin.cases X (fun _ => Y)

/-!
The generic `binaryInputs` above is useful only as a shape.  For contextual
operations we use the universe-polymorphic versions below so the colors remain
actual context objects rather than types.
-/

/-- Ordered left/right context profile for a binary operation. -/
def binaryContextInputs
    {Context : Type u}
    (X Y : Context) : Fin 2 -> Context :=
  Fin.cases X (fun _ => Y)

/-- Ordered left/right state arguments matching `binaryContextInputs`. -/
def binaryStateArgs
    {Context : Type u} [Category.{v} Context]
    {D : FunctorialTransportSystem Context}
    {X Y : Context}
    (x : D.state.obj X)
    (y : D.state.obj Y) :
    (i : Fin 2) -> D.state.obj (binaryContextInputs X Y i) :=
  Fin.cases x (fun _ => y)

/--
A binary higher-operadic primitive whose output is a bipartite tensor context.

No factorization or no-signalling property is included in this carrier.
-/
structure BipartiteJointOperation
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {D : FunctorialTransportSystem Context}
    (E : HigherOperadicDependentOriginationExtension D)
    (X Y X' Y' : Context) where
  op : E.base.signature.operation 1
    (binaryContextInputs X Y)
    (MonoidalCategory.tensorObj X' Y')

namespace BipartiteJointOperation

/-- Evaluate a binary joint primitive on ordered left/right states. -/
def eval
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {D : FunctorialTransportSystem Context}
    {E : HigherOperadicDependentOriginationExtension D}
    {X Y X' Y' : Context}
    (J : BipartiteJointOperation E X Y X' Y')
    (x : D.state.obj X)
    (y : D.state.obj Y) :
    D.state.obj (MonoidalCategory.tensorObj X' Y') :=
  E.base.algebra.act J.op (binaryStateArgs x y)

/-- A primitive operation two-cell gives equal joint evaluation in the current set truncation. -/
theorem eval_eq_of_opCell
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {D : FunctorialTransportSystem Context}
    {E : HigherOperadicDependentOriginationExtension D}
    {X Y X' Y' : Context}
    (J K : BipartiteJointOperation E X Y X' Y')
    (alpha : E.higher.opCell J.op K.op)
    (x : D.state.obj X)
    (y : D.state.obj Y) :
    J.eval x y = K.eval x y := by
  exact congrFun (E.algebraHigher.respectsOpCell alpha) (binaryStateArgs x y)

end BipartiteJointOperation

/--
Explicit semantic factorization of one joint primitive through two local causal
processes and the v1.9 tensor-state constructor.
-/
structure CausalTensorFactorization
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {D : FunctorialTransportSystem Context}
    (P : MonoidalProcessTransportSystem Context D)
    (C : CausalMonoidalProcessStructure Context)
    {E : HigherOperadicDependentOriginationExtension D}
    {X Y X' Y' : Context}
    (J : BipartiteJointOperation E X Y X' Y') where
  left : CausalIntervention C X X'
  right : CausalIntervention C Y Y'
  factorizes : forall (x : D.state.obj X) (y : D.state.obj Y),
    J.eval x y =
      P.tensorState
        (D.transport left.process x)
        (D.transport right.process y)

/-!
## Joint-operation no-signalling predicates

The varied side is required to be normalized.  This is exactly what permits
categorical discarding to recover the opposite factor from the factorized
output.  The unvaried opposite input may be arbitrary.
-/

/-- Changing the normalized left input cannot change the right output marginal. -/
def JointNoSignallingLeftToRight
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {D : FunctorialTransportSystem Context}
    (P : MonoidalProcessTransportSystem Context D)
    (C : CausalMonoidalProcessStructure Context)
    {E : HigherOperadicDependentOriginationExtension D}
    {X Y X' Y' : Context}
    (J : BipartiteJointOperation E X Y X' Y') : Prop :=
  forall (x₁ x₂ : NormalizedState P C X) (y : D.state.obj Y),
    rightMarginal D C (J.eval x₁.1 y) =
      rightMarginal D C (J.eval x₂.1 y)

/-- Changing the normalized right input cannot change the left output marginal. -/
def JointNoSignallingRightToLeft
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {D : FunctorialTransportSystem Context}
    (P : MonoidalProcessTransportSystem Context D)
    (C : CausalMonoidalProcessStructure Context)
    {E : HigherOperadicDependentOriginationExtension D}
    {X Y X' Y' : Context}
    (J : BipartiteJointOperation E X Y X' Y') : Prop :=
  forall (x : D.state.obj X) (y₁ y₂ : NormalizedState P C Y),
    leftMarginal D C (J.eval x y₁.1) =
      leftMarginal D C (J.eval x y₂.1)

/-- Two-way normalized-input no-signalling for a binary joint primitive. -/
def JointNoSignalling
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {D : FunctorialTransportSystem Context}
    (P : MonoidalProcessTransportSystem Context D)
    (C : CausalMonoidalProcessStructure Context)
    {E : HigherOperadicDependentOriginationExtension D}
    {X Y X' Y' : Context}
    (J : BipartiteJointOperation E X Y X' Y') : Prop :=
  JointNoSignallingLeftToRight P C J ∧
    JointNoSignallingRightToLeft P C J

namespace CausalTensorFactorization

/-- Causal tensor factorization implies left-to-right no-signalling. -/
theorem leftToRight_noSignalling
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {D : FunctorialTransportSystem Context}
    {P : MonoidalProcessTransportSystem Context D}
    {C : CausalMonoidalProcessStructure Context}
    {E : HigherOperadicDependentOriginationExtension D}
    {X Y X' Y' : Context}
    {J : BipartiteJointOperation E X Y X' Y'}
    (F : CausalTensorFactorization P C J) :
    JointNoSignallingLeftToRight P C J := by
  intro x₁ x₂ y
  rw [F.factorizes x₁.1 y, F.factorizes x₂.1 y]
  have hx₁ : NormalizedState P C X' := F.left.mapNormalized P x₁
  have hx₂ : NormalizedState P C X' := F.left.mapNormalized P x₂
  calc
    rightMarginal D C
        (P.tensorState
          (D.transport F.left.process x₁.1)
          (D.transport F.right.process y)) =
      D.transport F.right.process y := by
        simpa [CausalIntervention.mapNormalized] using
          (rightMarginal_tensorState P C hx₁
            (D.transport F.right.process y))
    _ = rightMarginal D C
        (P.tensorState
          (D.transport F.left.process x₂.1)
          (D.transport F.right.process y)) := by
        symm
        simpa [CausalIntervention.mapNormalized] using
          (rightMarginal_tensorState P C hx₂
            (D.transport F.right.process y))

/-- Causal tensor factorization implies right-to-left no-signalling. -/
theorem rightToLeft_noSignalling
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {D : FunctorialTransportSystem Context}
    {P : MonoidalProcessTransportSystem Context D}
    {C : CausalMonoidalProcessStructure Context}
    {E : HigherOperadicDependentOriginationExtension D}
    {X Y X' Y' : Context}
    {J : BipartiteJointOperation E X Y X' Y'}
    (F : CausalTensorFactorization P C J) :
    JointNoSignallingRightToLeft P C J := by
  intro x y₁ y₂
  rw [F.factorizes x y₁.1, F.factorizes x y₂.1]
  have hy₁ : NormalizedState P C Y' := F.right.mapNormalized P y₁
  have hy₂ : NormalizedState P C Y' := F.right.mapNormalized P y₂
  calc
    leftMarginal D C
        (P.tensorState
          (D.transport F.left.process x)
          (D.transport F.right.process y₁.1)) =
      D.transport F.left.process x := by
        simpa [CausalIntervention.mapNormalized] using
          (leftMarginal_tensorState P C
            (D.transport F.left.process x) hy₁)
    _ = leftMarginal D C
        (P.tensorState
          (D.transport F.left.process x)
          (D.transport F.right.process y₂.1)) := by
        symm
        simpa [CausalIntervention.mapNormalized] using
          (leftMarginal_tensorState P C
            (D.transport F.left.process x) hy₂)

/-- Explicit causal tensor factorization implies two-way joint no-signalling. -/
theorem jointNoSignalling
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {D : FunctorialTransportSystem Context}
    {P : MonoidalProcessTransportSystem Context D}
    {C : CausalMonoidalProcessStructure Context}
    {E : HigherOperadicDependentOriginationExtension D}
    {X Y X' Y' : Context}
    {J : BipartiteJointOperation E X Y X' Y'}
    (F : CausalTensorFactorization P C J) :
    JointNoSignalling P C J := by
  exact ⟨F.leftToRight_noSignalling, F.rightToLeft_noSignalling⟩

/--
Transport a causal tensor factorization across a primitive operation two-cell.
The local causal processes are unchanged; only the higher-operadic representative
is replaced.
-/
def ofOpCell
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {D : FunctorialTransportSystem Context}
    {P : MonoidalProcessTransportSystem Context D}
    {C : CausalMonoidalProcessStructure Context}
    {E : HigherOperadicDependentOriginationExtension D}
    {X Y X' Y' : Context}
    {J K : BipartiteJointOperation E X Y X' Y'}
    (F : CausalTensorFactorization P C J)
    (alpha : E.higher.opCell J.op K.op) :
    CausalTensorFactorization P C K where
  left := F.left
  right := F.right
  factorizes := by
    intro x y
    calc
      K.eval x y = J.eval x y :=
        (BipartiteJointOperation.eval_eq_of_opCell J K alpha x y).symm
      _ = P.tensorState
          (D.transport F.left.process x)
          (D.transport F.right.process y) :=
        F.factorizes x y

end CausalTensorFactorization

/-- Joint no-signalling is preserved across a represented operation two-cell. -/
theorem jointNoSignalling_of_opCell
    {Context : Type u} [Category.{v} Context] [MonoidalCategory Context]
    {D : FunctorialTransportSystem Context}
    {P : MonoidalProcessTransportSystem Context D}
    {C : CausalMonoidalProcessStructure Context}
    {E : HigherOperadicDependentOriginationExtension D}
    {X Y X' Y' : Context}
    {J K : BipartiteJointOperation E X Y X' Y'}
    (alpha : E.higher.opCell J.op K.op)
    (hJ : JointNoSignalling P C J) :
    JointNoSignalling P C K := by
  constructor
  · intro x₁ x₂ y
    calc
      rightMarginal D C (K.eval x₁.1 y) =
          rightMarginal D C (J.eval x₁.1 y) := by
        rw [BipartiteJointOperation.eval_eq_of_opCell J K alpha]
      _ = rightMarginal D C (J.eval x₂.1 y) := hJ.1 x₁ x₂ y
      _ = rightMarginal D C (K.eval x₂.1 y) := by
        rw [BipartiteJointOperation.eval_eq_of_opCell J K alpha]
  · intro x y₁ y₂
    calc
      leftMarginal D C (K.eval x y₁.1) =
          leftMarginal D C (J.eval x y₁.1) := by
        rw [BipartiteJointOperation.eval_eq_of_opCell J K alpha]
      _ = leftMarginal D C (J.eval x y₂.1) := hJ.2 x y₁ y₂
      _ = leftMarginal D C (K.eval x y₂.1) := by
        rw [BipartiteJointOperation.eval_eq_of_opCell J K alpha]

/-!
The v1.12 hierarchy is therefore:

```text
higher-multicategory binary joint primitive
  + explicit causal tensor factorization
  -> normalized-input joint no-signalling
  -> property preserved across represented operation two-cells.
```

This remains a certificate theorem, not an automatic property of joint
dependence.  It does not identify arbitrary operadic composition with monoidal
parallel composition, and it does not claim physical spacetime locality.
-/

end KUOS.DependentOriginationJointCausalFactorizationV1_12
