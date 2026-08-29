import KUOS.DependentOriginationBicategoricalCoherenceV1_6
import KUOS.DependentOriginationFunctorialTransportV0_1

namespace KUOS.DependentOriginationOperadicMultiConditionV1_7

open CategoryTheory
open KUOS.DependentOriginationFunctorialTransportV0_1
open KUOS.DependentOriginationBicategoricalCoherenceV1_6

universe u v w y

/-!
# Operadic multi-condition dependent origination v1.7

The parent transport spine is unary: one admissible relation transports a state
from one context to another.  Dependent origination also needs a separate axis
for genuinely joint conditioning, where several conditioned inputs participate
in one resulting state.

This layer adds that axis without replacing the unary parent.  Primitive
positive-arity operations are organized by a colored signature, and recursive
multi-condition expressions form the corresponding planar operadic tree syntax.
The existing contextual transport is embedded as the arity-one part of an
`OperadicDependentOriginationExtension`.

This is intentionally a free tree-level operadic axis, not yet a symmetric
operad quotient or a higher operad.  Permutation actions and their coherence are
left for a later layer.
-/

/--
A colored signature of positive-arity multi-condition operations.

`n` encodes actual arity `n + 1`, so every operation has at least one input.
This avoids treating an unconditioned nullary constant as primitive dependent
origination at this layer.
-/
structure MultiConditionSignature (Color : Type u) where
  operation : (n : Nat) ->
    (Fin (Nat.succ n) -> Color) -> Color -> Type v

/-- An interpretation of a multi-condition signature on a family of carriers. -/
structure MultiConditionAlgebra
    {Color : Type u}
    (signature : MultiConditionSignature.{u, v} Color)
    (Carrier : Color -> Type w) where
  act : forall {n : Nat}
    {inputs : Fin (Nat.succ n) -> Color} {out : Color},
    signature.operation n inputs out ->
      ((i : Fin (Nat.succ n)) -> Carrier (inputs i)) ->
        Carrier out

/--
Free planar multi-condition expression trees over a signature and a family of
atomic conditioned states.

Nesting `compose` nodes is operadic grafting: the output of each child tree is
required by the type to match the corresponding input color of its parent.
-/
inductive MultiConditionExpr
    {Color : Type u}
    (signature : MultiConditionSignature.{u, v} Color)
    (Carrier : Color -> Type w) : Color -> Type (max u v w) where
  | atom {c : Color} (value : Carrier c) :
      MultiConditionExpr signature Carrier c
  | compose {n : Nat}
      {inputs : Fin (Nat.succ n) -> Color} {out : Color}
      (op : signature.operation n inputs out)
      (args : (i : Fin (Nat.succ n)) ->
        MultiConditionExpr signature Carrier (inputs i)) :
      MultiConditionExpr signature Carrier out

namespace MultiConditionExpr

/-- Evaluate a free multi-condition tree in an algebra. -/
def eval
    {Color : Type u}
    {signature : MultiConditionSignature.{u, v} Color}
    {Carrier : Color -> Type w}
    (A : MultiConditionAlgebra signature Carrier)
    {out : Color} :
    MultiConditionExpr signature Carrier out -> Carrier out
  | .atom value => value
  | .compose op args => A.act op (fun i => eval A (args i))

@[simp] theorem eval_atom
    {Color : Type u}
    {signature : MultiConditionSignature.{u, v} Color}
    {Carrier : Color -> Type w}
    (A : MultiConditionAlgebra signature Carrier)
    {c : Color} (value : Carrier c) :
    eval A (.atom value) = value := by
  rfl

@[simp] theorem eval_compose
    {Color : Type u}
    {signature : MultiConditionSignature.{u, v} Color}
    {Carrier : Color -> Type w}
    (A : MultiConditionAlgebra signature Carrier)
    {n : Nat} {inputs : Fin (Nat.succ n) -> Color} {out : Color}
    (op : signature.operation n inputs out)
    (args : (i : Fin (Nat.succ n)) ->
      MultiConditionExpr signature Carrier (inputs i)) :
    eval A (.compose op args) =
      A.act op (fun i => eval A (args i)) := by
  rfl

end MultiConditionExpr

/--
An operadic extension of the ordinary contextual dependent-origination system.

The old unary transport is retained exactly as the arity-one sector.  Additional
operations of arity at least two are extra structure, never inferred from the
unary category alone.
-/
structure OperadicDependentOriginationExtension
    {Context : Type u} [Category.{v} Context]
    (D : FunctorialTransportSystem Context) where
  signature : MultiConditionSignature.{u, v} Context
  algebra : MultiConditionAlgebra.{u, v, w} signature (fun X => D.state.obj X)
  unary : forall {X Y : Context}, (X ⟶ Y) ->
    signature.operation 0 (fun _ : Fin 1 => X) Y
  unary_acts_as_transport : forall {X Y : Context}
    (f : X ⟶ Y) (s : D.state.obj X),
    algebra.act (unary f) (fun _ : Fin 1 => s) = D.transport f s

namespace OperadicDependentOriginationExtension

/-- State-expression type induced by an operadic extension. -/
abbrev StateExpr
    {Context : Type u} [Category.{v} Context]
    {D : FunctorialTransportSystem Context}
    (E : OperadicDependentOriginationExtension D)
    (out : Context) :=
  MultiConditionExpr E.signature (fun X => D.state.obj X) out

/-- The existing unary contextual transport as a one-input operadic expression. -/
def unaryExpr
    {Context : Type u} [Category.{v} Context]
    {D : FunctorialTransportSystem Context}
    (E : OperadicDependentOriginationExtension D)
    {X Y : Context} (f : X ⟶ Y) (s : D.state.obj X) :
    E.StateExpr Y :=
  .compose (E.unary f) (fun _ => .atom s)

/-- Evaluating the arity-one embedding is exactly the old contextual transport. -/
@[simp] theorem eval_unaryExpr
    {Context : Type u} [Category.{v} Context]
    {D : FunctorialTransportSystem Context}
    (E : OperadicDependentOriginationExtension D)
    {X Y : Context} (f : X ⟶ Y) (s : D.state.obj X) :
    MultiConditionExpr.eval E.algebra (E.unaryExpr f s) =
      D.transport f s := by
  simpa [unaryExpr] using E.unary_acts_as_transport f s

/-- Every ordinary transport arrow has an explicit unary operation witness. -/
theorem unary_operation_nonempty
    {Context : Type u} [Category.{v} Context]
    {D : FunctorialTransportSystem Context}
    (E : OperadicDependentOriginationExtension D)
    {X Y : Context} (f : X ⟶ Y) :
    Nonempty (E.signature.operation 0 (fun _ : Fin 1 => X) Y) :=
  ⟨E.unary f⟩

end OperadicDependentOriginationExtension

/-- The signature contains at least one genuinely multi-input primitive. -/
def HasGenuineMultiCondition
    {Color : Type u}
    (signature : MultiConditionSignature.{u, v} Color) : Prop :=
  exists n : Nat, 0 < n ∧
    exists (inputs : Fin (Nat.succ n) -> Color) (out : Color),
      Nonempty (signature.operation n inputs out)

/-!
## Shared invariant semantics through multi-condition composition
-/

/--
A semantic readout compatible with joint conditioning.

If all inputs of a primitive multi-condition operation carry the same invariant
semantic value, the resulting output carries that value too.  This is a local
compatibility condition on the new operadic axis; it is not forced by unary
transport alone.
-/
structure SharedSemanticReadout
    {Color : Type u}
    {signature : MultiConditionSignature.{u, v} Color}
    {Carrier : Color -> Type w}
    (A : MultiConditionAlgebra signature Carrier)
    (Semantic : Type y) where
  readout : (c : Color) -> Carrier c -> Semantic
  preserves_shared : forall {n : Nat}
    {inputs : Fin (Nat.succ n) -> Color} {out : Color}
    (op : signature.operation n inputs out)
    (args : (i : Fin (Nat.succ n)) -> Carrier (inputs i))
    (value : Semantic),
    (forall i, readout (inputs i) (args i) = value) ->
      readout out (A.act op args) = value

/-- Every atomic leaf of an expression has one common semantic value. -/
inductive AllAtomsAt
    {Color : Type u}
    {signature : MultiConditionSignature.{u, v} Color}
    {Carrier : Color -> Type w}
    {A : MultiConditionAlgebra signature Carrier}
    {Semantic : Type y}
    (Q : SharedSemanticReadout A Semantic)
    (value : Semantic) :
    {out : Color} -> MultiConditionExpr signature Carrier out -> Prop where
  | atom {c : Color} {s : Carrier c}
      (h : Q.readout c s = value) :
      AllAtomsAt Q value (.atom s)
  | compose {n : Nat}
      {inputs : Fin (Nat.succ n) -> Color} {out : Color}
      (op : signature.operation n inputs out)
      (args : (i : Fin (Nat.succ n)) ->
        MultiConditionExpr signature Carrier (inputs i))
      (h : forall i, AllAtomsAt Q value (args i)) :
      AllAtomsAt Q value (.compose op args)

/--
Operadic grafting preserves one shared invariant meaning through an arbitrarily
nested positive-arity multi-condition tree.
-/
theorem eval_preserves_shared_semantics
    {Color : Type u}
    {signature : MultiConditionSignature.{u, v} Color}
    {Carrier : Color -> Type w}
    {A : MultiConditionAlgebra signature Carrier}
    {Semantic : Type y}
    (Q : SharedSemanticReadout A Semantic)
    (value : Semantic)
    {out : Color}
    {e : MultiConditionExpr signature Carrier out}
    (h : AllAtomsAt Q value e) :
    Q.readout out (MultiConditionExpr.eval A e) = value := by
  induction h with
  | atom hValue =>
      simpa using hValue
  | @compose n inputs out op args hAtoms ih =>
      apply Q.preserves_shared op
        (fun i => MultiConditionExpr.eval A (args i)) value
      intro i
      exact ih i

/-!
The two new axes are intentionally orthogonal:

```text
v1.6 bicategorical axis:
  how different dependent paths are coherently related

v1.7 operadic axis:
  how several conditioned inputs jointly produce one output
```

A future layer may combine them into a genuinely higher operadic or monoidal
process structure.  v1.7 does not make that combined claim.
-/

end KUOS.DependentOriginationOperadicMultiConditionV1_7
