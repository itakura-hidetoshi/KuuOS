# Dependent Origination Higher Multicategory — Formal v1.8

## Purpose

v1.7 introduced positive-arity colored operations and free planar expression
trees.  v1.8 adds the missing higher comparison layer between operations with
the same colored input/output profile.

The new axis is:

```text
operation
  -> operation two-cell
  -> subtree two-cells
  -> grafted expression two-cell
```

This is multicategorical coherence: higher comparison data is stable under
multi-input substitution/grafting.

## Core structures

`HigherMultiConditionStructure` supplies typed cells between primitive
operations with one fixed profile, identity cells, and vertical composition.

`Expr2Cell` lifts this relation to arbitrary free planar multi-condition trees.
Its `compose` constructor is the key grafting rule: one cell between parent
operations plus one cell for every child tree induces a cell between the whole
grafted expressions.

`HigherMultiConditionAlgebra` is the current set-truncated realization.  It
requires related primitive operations to induce equal carrier maps.

The theorem

```text
eval_eq_of_expr2Cell
```

then proves that any expression two-cell induces equality after evaluation.
The readout theorem

```text
readout_eq_of_expr2Cell
```

shows that higher multicategorical path information can remain in the source
without changing the present set-valued semantic readout.

## Unary compatibility

`HigherOperadicDependentOriginationExtension` packages the v1.7 operadic
extension together with the new operation-cell layer.  The theorem

```text
eval_unaryExpr
```

re-exports the exact v1.7 fact that ordinary contextual transport remains the
arity-one sector.

Thus no existing unary theorem is weakened:

```text
ordinary contextual transport
  subset of
positive-arity operadic extension
  subset of
higher multicategorical extension
```

## Relation to bicategorical coherence

v1.6 and v1.8 are independent but compatible structural axes:

```text
v1.6:
  relation between unary dependent paths

v1.8:
  relation between multi-input operations and grafted trees
```

They are intentionally not collapsed into one opaque master definition.

## Scope boundary

v1.8 does not require permutation symmetry, braided input exchange, a symmetric
higher operad, a monoidal process theory, stack descent, enriched hom objects,
unbounded higher cells, quantum authority in the parent core, or physical
Yang--Mills authority.
