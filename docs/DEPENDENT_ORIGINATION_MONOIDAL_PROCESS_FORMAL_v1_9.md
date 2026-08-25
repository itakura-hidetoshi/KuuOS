# Dependent Origination Monoidal Process Theory — Formal v1.9

## Purpose

v1.9 adds the process-theoretic parallel-composition axis to the parent
non-quantum dependent-origination spine.

The interpretation is:

```text
objects     = contextual process interfaces
morphisms   = processes
f >> g      = sequential composition
f tensor g  = parallel composition
```

The source structure is Mathlib's native monoidal category rather than a local
look-alike definition.

## State realization

`MonoidalProcessTransportSystem` extends an existing contextual transport
system by explicitly supplying:

- `tensorState`, combining states at two process interfaces;
- `unitState`, the neutral parallel state;
- naturality under tensor products of morphisms;
- state coherence under the native monoidal associator;
- state coherence under the native left and right unitors.

Nothing in the ordinary contextual functor silently manufactures this parallel
state structure.

## Sequential / parallel interchange

Mathlib supplies the source relation

```text
(f1 tensor f2) >> (g1 tensor g2)
  =
(f1 >> g1) tensor (f2 >> g2).
```

The KuuOS theorem

```text
source_sequential_parallel_interchange
```

re-exports that relation at the dependent-origination boundary.

The state theorem

```text
sequential_parallel_interchange
```

shows that applying two parallel stages equals independently transporting both
state components through the two sequential process chains.

## Semantic readout

`MonoidalProcessReadout` adds a semantic parallel-composition operation and a
semantic unit.  The theorem

```text
readout_parallel_transport
```

shows that invariant semantic readout is compatible with independent parallel
process transport.

## Relation to v1.8

The v1.8 and v1.9 axes are distinct:

```text
higher multicategory:
  arbitrary joint multi-input dependence and coherence under grafting

monoidal process theory:
  independent parallel composition plus sequential composition
```

An arbitrary multi-condition primitive is therefore not assumed to factor as a
tensor product of independent processes.  Any such bridge must be supplied
explicitly in a later specialization.

## Scope boundary

v1.9 does not require symmetric or braided monoidal structure, compact closure,
feedback/traces, causal no-signalling, stack descent, enriched hom objects,
unbounded higher cells, quantum authority in the parent core, or physical
Yang--Mills authority.
