import KUOS.DependentOriginationOperadicMultiConditionV1_7

namespace KUOS.DependentOriginationHigherMulticategoryCoherenceV1_8

open KUOS.DependentOriginationOperadicMultiConditionV1_7

universe u v w z y

/-!
# Higher multicategory dependent-origination coherence v1.8

The v1.7 operadic axis records positive-arity primitive operations and free
planar grafting, but operations with the same input/output profile have no
higher comparison data.  This layer adds a typed two-dimensional coherence
relation between such operations and lifts it through arbitrary expression-tree
grafting.

The construction remains planar and colored.  It does not add permutation
actions.  The new structure is therefore a higher multicategorical coherence
layer rather than a claim of a symmetric higher operad.
-/

/--
Typed two-cells between primitive multi-condition operations with the same
colored profile.
-/
structure HigherMultiConditionStructure
    {Color : Type u}
    (signature : MultiConditionSignature.{u, v} Color) where
  opCell : forall {n : Nat}
    {inputs : Fin (Nat.succ n) -> Color} {out : Color},
    signature.operation n inputs out -> signature.operation n inputs out -> Type z
  idCell : forall {n : Nat}
    {inputs : Fin (Nat.succ n) -> Color} {out : Color}
    (op : signature.operation n inputs out),
    opCell op op
  vcomp : forall {n : Nat}
    {inputs : Fin (Nat.succ n) -> Color} {out : Color}
    {op₁ op₂ op₃ : signature.operation n inputs out},
    opCell op₁ op₂ -> opCell op₂ op₃ -> opCell op₁ op₃

/--
A set-truncated realization of primitive operation two-cells.

The source keeps the higher operation witness; the present carrier semantics
sends related primitive operations to equal action maps.
-/
structure HigherMultiConditionAlgebra
    {Color : Type u}
    {signature : MultiConditionSignature.{u, v} Color}
    {Carrier : Color -> Type w}
    (A : MultiConditionAlgebra signature Carrier)
    (H : HigherMultiConditionStructure.{u, v, z} signature) where
  respectsOpCell : forall {n : Nat}
    {inputs : Fin (Nat.succ n) -> Color} {out : Color}
    {op₁ op₂ : signature.operation n inputs out},
    H.opCell op₁ op₂ -> A.act op₁ = A.act op₂

/--
Two-cells between free planar multi-condition expressions.

`compose` is the multicategorical whiskering/grafting rule: a primitive
operation two-cell and a two-cell in every input subtree induce a two-cell
between the grafted trees.  `vcomp` composes expression two-cells vertically.
-/
inductive Expr2Cell
    {Color : Type u}
    {signature : MultiConditionSignature.{u, v} Color}
    (H : HigherMultiConditionStructure.{u, v, z} signature)
    (Carrier : Color -> Type w) :
    {out : Color} ->
      MultiConditionExpr signature Carrier out ->
      MultiConditionExpr signature Carrier out ->
      Type (max u (max z (max v w))) where
  | refl {out : Color} (e : MultiConditionExpr signature Carrier out) :
      Expr2Cell H Carrier e e
  | compose {n : Nat}
      {inputs : Fin (Nat.succ n) -> Color} {out : Color}
      {op₁ op₂ : signature.operation n inputs out}
      {args₁ args₂ : (i : Fin (Nat.succ n)) ->
        MultiConditionExpr signature Carrier (inputs i)}
      (opCell : H.opCell op₁ op₂)
      (argCell : forall i, Expr2Cell H Carrier (args₁ i) (args₂ i)) :
      Expr2Cell H Carrier (.compose op₁ args₁) (.compose op₂ args₂)
  | vcomp {out : Color}
      {e₁ e₂ e₃ : MultiConditionExpr signature Carrier out}
      (alpha : Expr2Cell H Carrier e₁ e₂)
      (beta : Expr2Cell H Carrier e₂ e₃) :
      Expr2Cell H Carrier e₁ e₃

/-- Grafting is compatible with primitive and subtree two-cells. -/
def graftCell
    {Color : Type u}
    {signature : MultiConditionSignature.{u, v} Color}
    {Carrier : Color -> Type w}
    (H : HigherMultiConditionStructure.{u, v, z} signature)
    {n : Nat}
    {inputs : Fin (Nat.succ n) -> Color} {out : Color}
    {op₁ op₂ : signature.operation n inputs out}
    {args₁ args₂ : (i : Fin (Nat.succ n)) ->
      MultiConditionExpr signature Carrier (inputs i)}
    (alpha : H.opCell op₁ op₂)
    (beta : forall i, Expr2Cell H Carrier (args₁ i) (args₂ i)) :
    Expr2Cell H Carrier (.compose op₁ args₁) (.compose op₂ args₂) :=
  .compose alpha beta

/--
Every expression two-cell becomes equality after a set-truncated algebra
realization.
-/
theorem eval_eq_of_expr2Cell
    {Color : Type u}
    {signature : MultiConditionSignature.{u, v} Color}
    {Carrier : Color -> Type w}
    {A : MultiConditionAlgebra signature Carrier}
    {H : HigherMultiConditionStructure.{u, v, z} signature}
    (HA : HigherMultiConditionAlgebra A H)
    {out : Color}
    {e₁ e₂ : MultiConditionExpr signature Carrier out}
    (alpha : Expr2Cell H Carrier e₁ e₂) :
    MultiConditionExpr.eval A e₁ = MultiConditionExpr.eval A e₂ := by
  induction alpha with
  | refl e =>
      rfl
  | @compose n inputs out op₁ op₂ args₁ args₂ hop hargs ih =>
      simp only [MultiConditionExpr.eval_compose]
      calc
        A.act op₁ (fun i => MultiConditionExpr.eval A (args₁ i)) =
            A.act op₂ (fun i => MultiConditionExpr.eval A (args₁ i)) := by
          rw [HA.respectsOpCell hop]
        _ = A.act op₂ (fun i => MultiConditionExpr.eval A (args₂ i)) := by
          apply congrArg (A.act op₂)
          funext i
          exact ih i
  | vcomp alpha beta ihAlpha ihBeta =>
      exact ihAlpha.trans ihBeta

/-- Higher multicategorical coherence is invisible to a set-valued readout. -/
theorem readout_eq_of_expr2Cell
    {Color : Type u}
    {signature : MultiConditionSignature.{u, v} Color}
    {Carrier : Color -> Type w}
    {A : MultiConditionAlgebra signature Carrier}
    {H : HigherMultiConditionStructure.{u, v, z} signature}
    (HA : HigherMultiConditionAlgebra A H)
    {Semantic : Type y}
    (Q : SharedSemanticReadout A Semantic)
    {out : Color}
    {e₁ e₂ : MultiConditionExpr signature Carrier out}
    (alpha : Expr2Cell H Carrier e₁ e₂) :
    Q.readout out (MultiConditionExpr.eval A e₁) =
      Q.readout out (MultiConditionExpr.eval A e₂) := by
  rw [eval_eq_of_expr2Cell HA alpha]

/--
The v1.7 dependent-origination operadic extension equipped with operation-level
higher coherence and a compatible set-truncated realization.
-/
structure HigherOperadicDependentOriginationExtension
    {Context : Type u} [CategoryTheory.Category.{v} Context]
    (D : KUOS.DependentOriginationFunctorialTransportV0_1.FunctorialTransportSystem Context) where
  base : OperadicDependentOriginationExtension D
  higher : HigherMultiConditionStructure.{u, v, z} base.signature
  algebraHigher : HigherMultiConditionAlgebra base.algebra higher

namespace HigherOperadicDependentOriginationExtension

/-- The old contextual transport remains exactly the unary sector. -/
@[simp] theorem eval_unaryExpr
    {Context : Type u} [CategoryTheory.Category.{v} Context]
    {D : KUOS.DependentOriginationFunctorialTransportV0_1.FunctorialTransportSystem Context}
    (E : HigherOperadicDependentOriginationExtension D)
    {X Y : Context} (f : X ⟶ Y) (s : D.state.obj X) :
    MultiConditionExpr.eval E.base.algebra (E.base.unaryExpr f s) =
      D.transport f s := by
  exact E.base.eval_unaryExpr f s

end HigherOperadicDependentOriginationExtension

/-!
The v1.8 boundary is deliberately precise:

```text
primitive n-ary operations
  -> operation two-cells
  -> subtree two-cells
  -> grafted expression two-cells
  -> set-truncated evaluation equality
```

Permutation symmetry, braided input exchange, and unbounded higher cells are
separate later extensions.
-/

end KUOS.DependentOriginationHigherMulticategoryCoherenceV1_8
