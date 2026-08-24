# Dependent-Origination Linear Transfer and Connected Readout — formal v0.3

## Status

KuuOS structural formalization.

This layer extends the v0.2 dependent-origination transport spine without changing
or weakening the existing groupoid/Čech or exponential-gap layers.

The central distinction is:

- dependent origination at the most general level is composable transport;
- a transfer operator is a **linear realization** of the positive-time branch of
  that transport;
- vacuum subtraction then becomes compatible with transport by linearity and
  vacuum fixation.

No Yang–Mills Hamiltonian, spectral measure, physical vacuum-orthogonal sector,
or physical mass gap is asserted in this file. Those remain obligations of the
authoritative `itakura-hidetoshi/4d-mass-gap` proof repository.

## Mathematical spine

```text
Dependent Origination
= functorial composable transport
        |
        +-- reversible gauge / Čech branch
        |
        +-- positive-time branch
              |
              +-- additive semigroup
              +-- contraction
              +-- fixed vacuum/reference state Ω
              +-- exponential excitation decay
                    |
                    +-- linear transfer realization T_t
                          |
                          +-- T_t (x - Ω) = T_t x - Ω
                                |
                                +-- connected readout
                                      |
                                      +-- exponential connected decay
```

## Linear transfer realization

Given an existing v0.2 transport `D`, a `LinearTransferRealization D` supplies

```text
operator : NNReal → State →ₗ[ℝ] State
```

with exact agreement

```text
operator t x = D.transport t x.
```

The semigroup law is therefore inherited rather than re-assumed:

```text
T_0 x = x,
T_(s+t) x = T_s (T_t x).
```

This is deliberately a realization/witness layer. It does not replace the more
general nonlinear transport abstraction.

## Vacuum subtraction

For the fixed reference state `Ω = D.vacuum`, linearity gives

```text
T_t (x - Ω)
  = T_t x - T_t Ω
  = T_t x - Ω.
```

This identity is the key bridge from generic transfer decay to connected or
vacuum-subtracted observables.

## Centered excitation

Define

```text
centeredState x = x - Ω
```

and declare a presentation centered-excitatory exactly when

```text
D.Excitation (x - Ω).
```

No claim is made that this abstract predicate is already the physical
vacuum-orthogonal Hilbert sector. A physical specialization may prove that
identification separately.

## Connected readout

For a bounded scalar readout `R`, define

```text
C_R(t,x) = R(T_t x - Ω).
```

By the linear vacuum-subtraction identity,

```text
C_R(t,x) = R(T_t (x - Ω)).
```

Therefore the v0.2 excitation estimate

```text
‖T_t y‖ ≤ exp(-m t) ‖y‖
```

and boundedness

```text
|R(y)| ≤ C_R ‖y‖
```

give

```text
|C_R(t,x)|
  ≤ C_R exp(-m t) ‖x - Ω‖.
```

This is the KuuOS-side abstract form of the transfer-operator → connected
correlation-decay step.

## Two-step coherence

Because the underlying transport is a semigroup,

```text
T_s(T_t x) = T_(s+t) x.
```

Hence the connected readout after two successive transfers is exactly the
summed-time connected readout and obeys

```text
|C_R(s+t,x)|
  ≤ C_R exp(-m(s+t)) ‖x-Ω‖
  = C_R exp(-ms) exp(-mt) ‖x-Ω‖.
```

This keeps the original dependent-origination composition law visible all the
way to the observable decay estimate.

## Conceptual interpretation

The hierarchy is now:

```text
object/presentation
    ↓
composable relation
    ↓
functorial transport
    ↓
positive-time semigroup
    ↓
linear transfer realization
    ↓
vacuum-centered excitation transport
    ↓
connected observable/readout decay
```

Thus the transfer operator is not identified with dependent origination itself.
It is a particularly strong linear realization of the non-invertible temporal
branch of the more general dependent-origination transport principle.

## Authority boundary

This layer establishes only the abstract implication

```text
linear realization
+ fixed vacuum
+ supplied exponential excitation gap
+ bounded readout
⇒ exponential connected-readout decay.
```

It does not infer a physical mass from KuuOS, does not identify Kū with a Hilbert
vacuum or the zero vector, and does not replace the physical proof carrier.
