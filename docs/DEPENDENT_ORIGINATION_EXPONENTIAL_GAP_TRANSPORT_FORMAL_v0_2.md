# Dependent Origination — Exponential Gap Transport v0.2

Status: Draft theorem surface

Update mode: additive / tighten-only

Canonical base for this unit:

```text
main@5f94bffc7cd84ce802c35c35bbf67ec06a5b67ce
```

## Purpose

This package extends the functorial dependent-origination transport spine by a
non-invertible positive-time branch carrying an abstract exponential excitation
gap.

The conceptual chain is

```text
Dependent Origination
  = functorial composable transport
        |
        +-- reversible transport
        |     action groupoid -> Čech descent
        |
        +-- positive-time transport
              additive semigroup
              -> contraction
              -> fixed vacuum/reference state
              -> stable excitation predicate
              -> exponential transport decay
              -> bounded-readout decay
```

The new layer formalizes the statement that a gap in transport is observable as
exponential loss of non-reference information under every bounded readout.

## Formal object

For a seminormed additive state space `State`,

```text
ExponentiallyGappedVacuumTransport State
```

extends the v0.1

```text
VacuumContractiveAdditiveEndoTransport NNReal State
```

and adds:

- a nonnegative real parameter `mass`;
- an abstract predicate `Excitation : State -> Prop`;
- transport stability of the excitation predicate;
- the estimate

\[
\|T_t x\|
\le
\exp(-m t)\,\|x\|
\qquad
(t\in\mathbb R_{\ge 0},\ x\in\mathrm{Excitation}).
\]

The package deliberately calls `Excitation` an abstract predicate rather than a
vacuum-orthogonal Hilbert sector.  A physical specialization may choose
`Excitation = Ω^\perp`, but KuuOS does not manufacture that physical carrier.

## Compositional law

Define

\[
q_m(t)=e^{-mt}.
\]

Mathlib proves in this package

\[
q_m(0)=1,
\qquad
q_m(s+t)=q_m(s)q_m(t),
\qquad
q_m(t)>0.
\]

Thus the quantitative gap law respects the same additive composition that
already governs the transport itself:

\[
T_{s+t}=T_sT_t.
\]

This is the quantitative positive-time specialization of the general KuuOS
functorial transport law

\[
F(g\circ f)=F(g)\circ F(f).
\]

## Bounded readout theorem

A `BoundedReadout State` consists of a scalar readout `R` and a nonnegative
amplitude `C_R` such that

\[
|R(x)|\le C_R\|x\|.
\]

The main theorem is

```text
bounded_readout_decay
```

which proves

\[
|R(T_t x)|
\le
C_R e^{-mt}\|x\|
\]

for every excitation state.

The two-step theorem proves the same bound along the composed path

\[
x\xrightarrow{T_t}T_t x\xrightarrow{T_s}T_sT_t x
\]

and the product form gives

\[
|R(T_sT_t x)|
\le
C_R e^{-ms}e^{-mt}\|x\|.
\]

So the semantic statement is not merely that transport composes, but that the
non-reference component carries a multiplicative contraction certificate under
composition.

## Relation to `4d-mass-gap`

The authoritative physical repository is:

```text
itakura-hidetoshi/4d-mass-gap
```

There, the transfer-operator route has the physical pattern

```text
correlation state
-> transfer operator
-> operator contraction / gap
-> correlation readout
-> exponential connected-correlation decay
```

The KuuOS v0.2 layer extracts only the structural implication

```text
transport decay + bounded readout
-> observable decay
```

and keeps all physical claims outside KuuOS.

In particular this package does **not** assert or construct:

- a Yang--Mills measure;
- Osterwalder--Schrader reconstruction;
- a physical Hamiltonian;
- self-adjointness of a Hamiltonian;
- a spectral measure;
- a vacuum-orthogonal physical Hilbert sector;
- a numerical Yang--Mills mass gap;
- an identity between philosophical `空` and a Hilbert-space zero vector.

## KuuOS reading

The current mathematical reading becomes:

```text
空
  = no state presentation is promoted to independent substance

縁起
  = state/meaning is organized by composable transport

可逆縁起
  = gauge/action-groupoid transport

時間的縁起
  = additive positive-time semigroup transport

縁起 gap
  = non-reference transport information contracts exponentially

観測
  = bounded readout inherits that contraction
```

A concise formulation is

\[
\boxed{\text{dependent origination} = \text{functorial transport before substance}}
\]

with the quantitative refinement

\[
\boxed{\text{gap} = \text{exponential contraction of non-reference transport information}}.
\]

The latter is a structural reading only; physical spectral-gap meaning requires
a separately constructed physical specialization.

## Files

```text
formal/KUOS/DependentOriginationExponentialGapTransportV0_2.lean
formal/KUOS/DependentOriginationTransportSpineV0_2.lean
docs/DEPENDENT_ORIGINATION_EXPONENTIAL_GAP_TRANSPORT_FORMAL_v0_2.md
```

## Proof boundary

The package is append-only and assumption-preserving.  It does not weaken the
v0.1 groupoid/Čech formalization and does not identify reversible gauge
transport with irreversible positive-time transport.

The key separation is:

```text
same compositional law
!=
same morphism type
```

Gauge arrows may be invertible.  Positive-time contraction morphisms need not
be.  Their common parent is functorial composable transport.
