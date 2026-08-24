# Dependent Origination — Functorial Transport Formal v0.1

Status: Draft theorem surface

Update mode: append-only / tighten-only

Repository: `itakura-hidetoshi/KuuOS`

Exact base: `main@af955f63ff3f7c852d1146904cd7d94d05379d2d`

Branch: `formal/dependent-origination-functorial-transport-v0-1`

## Purpose

This package places one common mathematical layer above the existing KuuOS
action-groupoid / Čech dependent-origination line and the positive-time
transfer-operator pattern developed in `itakura-hidetoshi/4d-mass-gap`.

The core principle is:

```text
縁起 = functorial composable transport before object-substance
```

This is not the claim that every dependent-origination transport is a gauge
transformation, nor that the transfer operator is identical to dependent
origination.  Rather:

```text
dependent origination
    = general compositional transport principle

gauge / Čech dependent origination
    = reversible specialization

positive-time transfer semigroup
    = generally non-invertible additive specialization
```

## Generic formal object

The Lean structure

```text
FunctorialTransportSystem Context
```

contains a Mathlib functor

\[
F : \mathcal C \to \mathbf{Type},
\]

where:

- objects of `Context` are conditioned presentations / contexts;
- morphisms are admissible relations;
- `F.obj X` is the state type over context `X`;
- `F.map f` is transport along the relation `f`.

The Mathlib functor laws give the two basic dependent-origination transport
laws:

\[
T_{\mathrm{id}_X}(x)=x,
\]

and

\[
T_{g\circ f}(x)=T_g(T_f(x)).
\]

Thus the composition law is not introduced as a new ad hoc axiom: it is inherited
from `CategoryTheory.Functor`.

## Invariant semantic/readout layer

`InvariantReadout` assigns a semantic value to each transported state and
requires

\[
R_Z(T_f x)=R_X(x).
\]

This is the elementwise invariant-semantic surface corresponding to the KuuOS
principle:

```text
meaning is invariant; presentation and transition data are equivariant.
```

The theorem `InvariantReadout.readout_comp` proves invariance along an arbitrary
two-step composite path by functoriality.

## Additive positive-time specialization

`AdditiveEndoTransport Time State` records

\[
T_0=\mathrm{id},
\qquad
T_{s+t}=T_s\circ T_t.
\]

No inverse is required.

`ContractiveAdditiveEndoTransport` strengthens this with

\[
\|T_t x\|\le \|x\|,
\]

and `VacuumContractiveAdditiveEndoTransport` further adds a distinguished
reference/vacuum state \(\Omega\) with

\[
T_t\Omega=\Omega.
\]

This is the KuuOS-side structural interface corresponding to the OS
positive-time contraction-semigroup pattern in `4d-mass-gap`.  KuuOS does not
import the physical repository here; the relation is architectural and can be
bridged by an explicit adapter later.

## Existing gauge / Čech specialization

The bridge file

```text
formal/KUOS/GaugeInvariantDependentOriginationFunctorialTransportBridgeV0_1.lean
```

reuses the already formalized

```text
ActionGroupoidCechDatum Gauge X Index
```

and exposes its existing laws as the reversible branch of the common transport
picture:

\[
g_{ii}=1,
\]

\[
g_{jk}\circ g_{ij}=g_{ik}.
\]

The existing arrow-constancy theorem then gives transport-invariant semantics,
and nonempty compatible Čech presentations have one unique glued semantic
value.

Nothing in this bridge replaces or weakens the existing action-groupoid theorem.
It only places that theorem under a broader compositional-transport reading.

## Structural hierarchy

```text
                         Dependent Origination
                    functorial composable transport
                              /        \
                             /          \
                            /            \
             reversible transport      non-invertible transport
                    |                         |
             action groupoid             additive semigroup
                    |                         |
              Čech cocycle               OS contraction
                    |                         |
        invariant semantic glue        fixed vacuum/reference
                                              |
                                   Hamiltonian / mass-gap bridge
                                   (physical specialization only)
```

The common law is composition:

\[
T_{g\circ f}=T_g\circ T_f.
\]

For gauge transport this is the Čech/groupoid cocycle law.  For positive time it
becomes

\[
T_{s+t}=T_sT_t.
\]

## KuuOS reading

```text
空
  = no local object, chart, state representative, or transport presentation is
    granted independent semantic substance

縁起
  = admissible presentations are connected by explicit composable transport

中道
  = preserve objects and morphisms without reifying either an object as
    independent substance or collapsing all structure to a bare quotient

世俗的意味
  = invariant/readout structure compatible with transport
```

The formal package deliberately does **not** identify the categorical structure
itself with ultimate truth.  It remains conventional mathematical structure.

## Relation to `4d-mass-gap`

The physical repository contains the concrete analytic chain

```text
positive-time observable algebra
→ physical contraction semigroup
→ strong continuity
→ infinitesimal generator
→ Hamiltonian
→ vacuum-orthogonal lower bound / mass gap
```

KuuOS now has a structurally matching generic interface at the first two levels:

```text
AdditiveEndoTransport
→ ContractiveAdditiveEndoTransport
→ VacuumContractiveAdditiveEndoTransport
```

A future cross-repository adapter may certify that a selected physical transfer
semigroup realizes this interface.  Such an adapter should be one-way and
explicit: KuuOS should not manufacture physical theorems, and the physical
repository should remain authoritative for Yang–Mills analysis.

## Formal files

```text
formal/KUOS/DependentOriginationFunctorialTransportV0_1.lean
formal/KUOS/GaugeInvariantDependentOriginationFunctorialTransportBridgeV0_1.lean
```

## Proof boundary

This v0.1 package proves/records only the structural transport layer.

It does not claim:

- that every KuuOS process is invertible;
- that every dependent-origination context is an action groupoid;
- that every additive transport has a generator;
- strong continuity of a generic additive transport;
- existence or self-adjointness of a Hamiltonian;
- a mass gap from the generic KuuOS structures;
- a quotient-stack, higher-stack, or arbitrary-site descent theorem;
- a physical identification without an explicit bridge to `4d-mass-gap`.

These boundaries keep the abstraction strictly additive and prevent the
philosophical reading from being promoted into unsupported physical authority.
