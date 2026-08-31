# Dependent Origination — Contextual Gauge Theory v0.1

Status: Draft theorem surface

Update mode: append-only / tighten-only

Repository: `itakura-hidetoshi/KuuOS`

Exact base: `main@284ecf8778361367aee6d926bf158985da12ecfc`

Branch: `formal/contextual-gauge-transport-v0-1`

## Purpose

This package organizes gauge theory under the existing KuuOS dependent-origination
parent:

```text
縁起 = composable contextual transport before fixed substance
```

The intended hierarchy is not

```text
KuuOS = Yang--Mills
```

and not

```text
every contextual transport = physical gauge theory.
```

Instead, the claim is structural:

```text
ordinary reversible gauge transport
        ⊂
contextual transport with explicit composition
        ⊂
higher / process-dependent contextual transport.
```

The v0.1 theorem package proves the algebraic action-groupoid part of this
inclusion and connects it to the already formalized KuuOS two-cell and
non-invertible transport layers.

## Parent structure

KuuOS already defines

```text
FunctorialTransportSystem Context
```

with a Mathlib functor

\[
D : \mathcal C \to \mathbf{Type}.
\]

Thus each context \(X\) has a state carrier \(D(X)\), each admissible relation
\(f:X\to Y\) has transport

\[
D(f):D(X)\to D(Y),
\]

and the functor laws give

\[
D(\mathrm{id})=\mathrm{id},
\qquad
D(g\circ f)=D(g)\circ D(f).
\]

The important point is that the carrier may depend on the context.  The parent
therefore does not require one globally fixed fiber and does not require every
transport to be invertible.

## Ordinary algebraic gauge theory as a reversible specialization

Let a group `Gauge` act on a space of representatives `X`.  The existing KuuOS
file

```text
formal/KUOS/GaugeInvariantDependentOriginationActionGroupoidV0_1.lean
```

defines

```text
ActionArrow Gauge x y
```

as an explicit gauge element carrying `x` to `y`, together with identity,
composition, inverse, isotropy, stabilizer, and gauge-invariant semantic
results.

The new file

```text
formal/KUOS/DependentOriginationContextualGaugeTheoryV0_1.lean
```

wraps these objects as a genuine Mathlib category

```text
ActionContext Gauge X
```

whose morphisms are precisely `ActionArrow`s.

If `Gauge` also acts on a representation fiber `Fiber`, the new

```text
actionRepresentationFunctor
```

constructs

\[
\mathrm{ActionContext}(G,X)\longrightarrow \mathbf{Type}
\]

with constant object fiber `Fiber` and arrow map

\[
\psi\longmapsto g\cdot\psi.
\]

This gives

```text
actionRepresentationTransportSystem
```

which is a concrete `FunctorialTransportSystem`.

Hence the exact theorem-level statement is:

```text
an ordinary algebraic action-groupoid gauge representation
is a reversible specialization of KuuOS contextual transport.
```

This is a conservative embedding statement at the algebraic transport level.
It is not yet a theorem about arbitrary smooth principal bundles.

## Reversibility

For every action-groupoid arrow `a`, the new package proves

```text
actionRepresentation_inverse_transport_apply
actionRepresentation_transport_inverse_apply
actionRepresentation_transport_bijective
```

corresponding to

\[
T_{a^{-1}}T_a=\mathrm{id},
\qquad
T_aT_{a^{-1}}=\mathrm{id},
\]

and therefore

\[
T_a:D(x)\to D(y)
\]

is bijective.

This separates the ordinary gauge branch from the more general KuuOS parent:

```text
FunctorialTransportSystem
    ├── reversible action-groupoid specialization
    └── non-invertible specializations allowed
```

## Gauge-invariant observables as invariant readouts

The KuuOS parent already defines

```text
FunctorialTransportSystem.InvariantReadout
```

with the condition

\[
R_Y(D(f)x)=R_X(x).
\]

The new constructor

```text
invariantReadoutOfActionGaugeInvariant
```

shows that an ordinary gauge-invariant semantic map

\[
O(g\cdot\psi)=O(\psi)
\]

canonically determines an invariant contextual readout.

Thus the ordinary gauge statement

```text
observable is invariant under gauge transformation
```

becomes the parent statement

```text
observable is invariant under admissible contextual transport.
```

This is the central semantic bridge.

## Existing Čech descent fits the same branch

KuuOS already has

```text
formal/KUOS/GaugeInvariantDependentOriginationFunctorialTransportBridgeV0_1.lean
```

which identifies the existing action-groupoid Čech laws with the reversible
transport laws:

\[
g_{ii}=1,
\]

and

\[
g_{jk}\circ g_{ij}=g_{ik}.
\]

It also reuses gauge-arrow constancy to obtain a unique glued semantic value for
nonempty compatible Čech presentations.

Therefore the reversible side now has the structural chain

```text
Gauge group action
    ↓
ActionArrow / action groupoid
    ↓
ActionContext as a Mathlib category
    ↓
actionRepresentationFunctor
    ↓
FunctorialTransportSystem
    ↓
Čech composition / descent
    ↓
InvariantReadout
```

## Higher gauge direction

The existing KuuOS higher spine already separates source-level path data from a
set-truncated `Type` realization.

In

```text
formal/KUOS/DependentOriginationTwoCellCoherenceV1_5.lean
```

`Refinement2CellStructure` stores two-cells between parallel context arrows, and
`SetTruncatedTwoRealization` states that represented two-cells induce equal
state maps.

The new theorems

```text
higherContextualGaugeCell_transport_eq
higherContextualGaugeCell_transport_apply_eq
```

make this explicitly available to the contextual-gauge layer:

\[
\alpha:f\Rightarrow g
\quad\Longrightarrow\quad
D(f)=D(g)
\]

for a selected set-truncated realization.

This should be read carefully.  The source may retain distinct paths and their
higher comparison data; only the chosen `Type`-valued realization identifies
the induced transports.

The higher-gauge route is therefore

```text
1-morphism transport
    ↓
2-cell path comparison
    ↓
bicategorical / higher coherence
    ↓
optional set-truncated observable realization.
```

The v0.1 package does **not** define curvature as an arbitrary two-cell.  A
future differential-geometric realization must show how holonomy and curvature
arise from a suitable smooth/path higher context.

## Non-invertible extension

The parent was deliberately defined without invertibility.  Existing KuuOS
structures already include

```text
AdditiveEndoTransport
ContractiveAdditiveEndoTransport
VacuumContractiveAdditiveEndoTransport
```

with

\[
T_{s+t}=T_s\circ T_t
\]

and, in the contractive case,

\[
\lVert T_t x\rVert\le \lVert x\rVert.
\]

The quantum/process branch also contains Choi, complete positivity, CPTP finite
words, instruments, combs, and testers.

Therefore contextual gauge theory is organized inside a larger transport
hierarchy rather than forcing all arrows to be gauge equivalences:

```text
                        contextual transport
                         /       |        \
                        /        |         \
             reversible        higher      irreversible
                |                 |             |
          action groupoid       2-cells      semigroup/CPTP
                |                 |             |
             Čech          bicategorical     process tensor
                \                 |             /
                 \                |            /
                  presentation-independent observables
```

## Differential-geometric realization frontier

The next mathematically substantial layer is the smooth/path realization.

For a manifold or suitable space \(M\), the target picture is a transport
functor of the form

\[
\Pi_1(M)\longrightarrow G\text{-Tors}
\]

or an associated representation-valued form.  Parallel transport along

\[
\gamma:x\to y
\]

should become contextual transport

\[
T_\gamma:F_x\to F_y.
\]

This would permit a theorem-level chain

```text
principal-bundle connection
    ↓
path-groupoid parallel transport
    ↓
KuuOS contextual transport
```

with gauge transformations represented by suitable natural equivalences.

That smooth realization is a future theorem package.  It requires explicit
Mathlib differential geometry and must not be inferred from the algebraic
v0.1 action-groupoid result.

## Curvature / holonomy frontier

Once a smooth path or thin-path context is available, the intended structural
reading is

```text
connection  = coherent infinitesimal/path transport
holonomy    = transport around a loop
curvature   = infinitesimal obstruction measured by loop transport
```

and in a higher context

```text
parallel paths + comparison 2-cells
```

provide the natural carrier for higher holonomy/coherence.

But the physical equation

\[
F_A=dA+A\wedge A
\]

is not proved merely by possessing two-cell data.  Its realization must be
constructed and verified independently.

## Yang--Mills authority boundary

`itakura-hidetoshi/4d-mass-gap` remains authoritative for concrete physical
Yang--Mills statements.

The KuuOS contextual-gauge hierarchy provides structural interfaces such as

```text
context
transport
reversibility
higher coherence
invariant observable
non-invertible process specialization
```

but it does not manufacture the physical claims

```text
Yang--Mills measure
Hamiltonian
self-adjointness
mass gap
continuum limit
```

without an explicit cross-repository realization theorem.

Thus

```text
KuuOS structural contextual-gauge theorem
!=
4d-mass-gap physical Yang--Mills theorem authority.
```

## Proposed full hierarchy

The conceptual hierarchy can now be stated as

\[
\boxed{
\text{ordinary gauge transport}
\subset
\text{reversible contextual transport}
\subset
\text{higher contextual transport}
\subset
\text{general dependent-origination transport}
}
\]

where the last parent also admits irreversible/process realizations.

A more detailed dependency diagram is

```text
Dependent Origination
= composable contextual transport

├── Reversible contextual gauge branch
│   ├── group actions
│   ├── action groupoids
│   ├── representation transport
│   ├── Čech descent
│   └── gauge-invariant readouts
│
├── Higher contextual gauge branch
│   ├── parallel 1-morphisms
│   ├── explicit 2-cells
│   ├── bicategorical coherence
│   ├── scaled / infinity coherence
│   └── presentation-independent invariants
│
└── Non-invertible process branch
    ├── additive semigroups
    ├── contractions
    ├── CPTP maps
    ├── instruments / combs / testers
    └── memory / causal process realizations
```

The differential-geometric gauge theory frontier should connect into the first
and second branches through path-groupoid and higher-path transport.

## Formal status matrix

| Layer | Status | Main KuuOS surface |
|---|---|---|
| Generic contextual transport | formalized | `FunctorialTransportSystem` |
| Action-groupoid gauge arrows | formalized | `ActionArrow` |
| Action groupoid as Mathlib category | formalized in v0.1 | `ActionContext` |
| Representation transport functor | formalized in v0.1 | `actionRepresentationFunctor` |
| Explicit transport reversibility | formalized in v0.1 | inverse/bijective theorems |
| Gauge invariant → invariant readout | formalized in v0.1 | `invariantReadoutOfActionGaugeInvariant` |
| Čech reversible descent | already formalized | functorial transport bridge |
| Two-cell/higher coherence | already formalized + v0.1 bridge | `Refinement2CellStructure` |
| Additive non-invertible transport | already formalized | `AdditiveEndoTransport` |
| CPTP/process realizations | already formalized downstream | quantum/process files |
| Smooth principal-bundle transport | frontier | not claimed |
| Differential connection/curvature realization | frontier | not claimed |
| Yang--Mills action/quantization | external physical authority | `4d-mass-gap` |

## KuuOS reading

```text
空
  = no chart, representative, fiber presentation, path presentation, or chosen
    gauge is granted independent semantic substance

縁起
  = state and meaning arise relative to contexts connected by explicit
    composable transport

中道
  = neither reify one presentation nor erase transport/coherence information
    prematurely

gauge invariance
  = a special reversible form of transport-invariant semantics

higher gauge
  = retain comparison data between paths rather than collapsing all paths to
    equality at the source
```

This is a mathematical architecture statement.  It does not promote the
category, groupoid, or higher-category presentation itself to an ultimate
substance.

## Formal files

New:

```text
formal/KUOS/DependentOriginationContextualGaugeTheoryV0_1.lean
docs/DEPENDENT_ORIGINATION_CONTEXTUAL_GAUGE_THEORY_v0_1.md
```

Existing dependencies:

```text
formal/KUOS/DependentOriginationFunctorialTransportV0_1.lean
formal/KUOS/GaugeInvariantDependentOriginationActionGroupoidV0_1.lean
formal/KUOS/GaugeInvariantDependentOriginationFunctorialTransportBridgeV0_1.lean
formal/KUOS/DependentOriginationTwoCellCoherenceV1_5.lean
```

## Next theorem frontier

The most natural next proof package is:

```text
smooth principal-bundle/path-groupoid parallel transport
    → KuuOS FunctorialTransportSystem
```

followed by a natural-transformation formulation of gauge equivalence and only
then a rigorous curvature/holonomy realization.

That ordering keeps the extension conservative:

```text
existing gauge theory is recovered first,
then generalized,
then higher/non-invertible realizations are added.
```
