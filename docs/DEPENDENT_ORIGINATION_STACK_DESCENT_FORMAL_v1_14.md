# Dependent Origination — Stack Descent v1.14

## Purpose

v1.14 adds a **strong optional stack layer** above the weak contextual-descent parent.

Earlier dependent-origination descent deliberately established that local compatibility does not by itself imply reconstruction of one global root state. That boundary remains unchanged.

The stack layer is introduced only after explicitly supplying:

1. a context category `C`;
2. a Grothendieck topology `J` on `C`;
3. a Cat-valued pseudofunctor
   ```text
   F : LocallyDiscrete Cᵒᵖ ⥤ᵖ Cat;
   ```
4. a native Mathlib certificate
   ```text
   Pseudofunctor.IsStack F J.
   ```

## Native Mathlib stack API

The implementation imports

```lean
Mathlib.CategoryTheory.Sites.Descent.IsStack
```

and uses Mathlib's actual `Pseudofunctor.IsStack` typeclass.

For a covering family, Mathlib gives that the canonical functor to descent data is an equivalence of categories:

```text
F(base) ≃ descent data over the cover.
```

The KuuOS theorem `descentData_isEquivalence` is a direct bridge to this native result.

## Relation to parent states

`StackDependentOriginationLayer` also carries the existing `FunctorialTransportSystem` and an explicit interpretation

```text
parent state at X -> object of the stack fiber F(X).
```

This interpretation does not silently assert naturality or effective descent for the parent state functor itself. Those stronger claims would require additional bridges.

## Why stack is stronger than the parent

The hierarchy is:

```text
compatible local state family
  -> semantic descent may exist
  -/-> global state witness in general
```

whereas a supplied stack layer has effective categorical descent for the chosen topology and pseudofunctor.

Thus the correct relationship is

```text
dependent-origination parent
  + site/topology
  + Cat-valued pseudofunctor
  + IsStack proof
  -> stack specialization.
```

It is not

```text
dependent origination = stack.
```

## Boundary

v1.14 does not claim:

- every KuuOS state carrier forms a stack;
- every refinement cover is a Grothendieck cover;
- all compatible local parent states glue globally;
- higher-stack or infinity-stack descent;
- physical or quantum authority.

Those require additional structure and proofs.
