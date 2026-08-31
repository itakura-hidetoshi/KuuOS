# Dependent Origination — Fundamental Descent NatIso Invariance v0.6

Status: theorem-level tightening of the contextual-gauge transport frontier

Update mode: additive / tighten-only

## Purpose

This note records the theorem boundary reached after the contextual-gauge v0.1–v0.5 spine and tightens an earlier differential-geometric frontier statement.

The formal chain is now:

```text
algebraic action-groupoid gauge transport
    ↓
gauge-equivariant fiber equivalence → natural isomorphism
    ↓
reversible transport landing in Core(Type)
    ↓
ordinary fundamental-groupoid transport
    ↓
fine-context → fundamental-groupoid descent criterion
    ↓
quotient-kernel obstruction
    ↓
NatIso invariance of descent / obstruction
```

The new Lean file is

```text
formal/KUOS/DependentOriginationFundamentalGroupoidDescentNatIsoInvarianceV0_6.lean
```

## Presentation-independent transport equality

Let

\[
Q:P\to\Pi_1(M)
\]

be a functor from a finer context to Mathlib's ordinary fundamental groupoid, and let

\[
S_1,S_2:P\to\mathbf{Type}
\]

be naturally isomorphic transport presentations:

\[
e:S_1\cong S_2.
\]

Naturality gives conjugate transport maps. Therefore, for parallel arrows \(f,g\),

\[
S_1(f)=S_1(g)
\quad\Longleftrightarrow\quad
S_2(f)=S_2(g).
\]

The v0.6 file promotes this pointwise fact to the v0.5 descent predicates.

## Kernel compatibility and obstruction are NatIso invariants

The v0.5 kernel condition is

\[
Q(f)=Q(g)\Longrightarrow S(f)=S(g).
\]

The v0.6 theorem proves

\[
\operatorname{QuotientKernelCompatible}(Q,S_1)
\iff
\operatorname{QuotientKernelCompatible}(Q,S_2).
\]

Likewise the concrete obstruction

\[
Q(f)=Q(g),\qquad S(f)\ne S(g)
\]

is invariant:

\[
\operatorname{HasQuotientKernelObstruction}(Q,S_1)
\iff
\operatorname{HasQuotientKernelObstruction}(Q,S_2).
\]

Thus a descent obstruction is not an artefact of a chosen naturally isomorphic fiber presentation.

## Descent existence is NatIso invariant

A v0.5 descent witness consists of a fundamental-groupoid transport \(T\) and a natural isomorphism

\[
S\cong Q^*T.
\]

If \(e:S_1\cong S_2\), a descent witness for \(S_1\) transports to one for \(S_2\) by composing

\[
S_2\xrightarrow{e^{-1}}S_1\xrightarrow{\sim}Q^*T.
\]

Hence

\[
\operatorname{Nonempty}(\operatorname{FundamentalDescent}(Q,S_1))
\iff
\operatorname{Nonempty}(\operatorname{FundamentalDescent}(Q,S_2)).
\]

Non-descent is therefore invariant as well.

## Gauge-equivariant specialization

The contextual-gauge v0.2 layer already proves that a gauge-equivariant fiber equivalence

\[
E:F_1\simeq F_2
\]

induces a natural isomorphism between the corresponding action-representation transport functors.

The v0.6 file composes that result with the generic descent invariance theorem. Consequently, for any chosen quotient

\[
Q:\operatorname{ActionContext}(G,X)\to\Pi_1(M),
\]

fundamental-groupoid descent existence and quotient-kernel obstruction are unchanged by a gauge-equivariant change of representation fiber.

This is the precise theorem-level sense in which the descent question is presentation/gauge independent at the current categorical layer.

## Tightening of the earlier v0.1 differential-geometric frontier

The original contextual-gauge v0.1 note displayed a prospective transport

\[
\Pi_1(M)\to G\text{-Tor}
\]

under a broad heading about smooth principal-bundle/path-groupoid transport.

That picture must now be read more narrowly.

Mathlib's `FundamentalGroupoid M` quotients endpoint-fixed paths by ordinary homotopy. A general smooth connection with curvature need not have parallel transport invariant under ordinary path homotopy. Therefore the ordinary fundamental-groupoid branch represents the homotopy-invariant / local-system-like / flat side of the intended geometry, not arbitrary non-flat connection transport.

The correct hierarchy is:

```text
homotopy-invariant / flat-like transport
    → ordinary FundamentalGroupoid M

general curvature-sensitive connection transport
    → finer path or thin-path context
    → ordinary FundamentalGroupoid M only when an additional descent condition holds
```

The v0.5 obstruction theorem measures a necessary condition for that latter descent.

Accordingly, no theorem in the current KuuOS spine identifies an arbitrary smooth principal-bundle connection with a functor on the ordinary fundamental groupoid.

## Current Mathlib boundary

The pinned Mathlib tree contains substantial differential-geometric and ODE infrastructure, including vector-bundle covariant derivatives and Picard–Lindelöf existence/uniqueness tools. However the current audit did not identify a ready-made theorem-level bridge constructing general vector-bundle parallel transport from a covariant derivative, nor a built-in thin-path groupoid API suitable for simply importing the non-flat connection realization.

Therefore the future non-flat realization must be proved as an independent layer rather than inferred from existing APIs.

## Authority boundary

The v0.6 result is structural and categorical. It proves invariance of descent properties under natural isomorphism of transport functors.

It does **not** prove:

```text
smooth connection → parallel transport
thin-homotopy invariance
curvature formula
Yang–Mills action
quantization
Hamiltonian construction
continuum limit
mass gap
```

Concrete physical Yang–Mills theorem authority remains in `itakura-hidetoshi/4d-mass-gap` and requires explicit realization bridges.

## Formal frontier after v0.6

The next geometric frontier is not to relabel ordinary `FundamentalGroupoid` transport as a general connection. It is to construct or isolate a finer path context capable of retaining curvature-sensitive information, then prove the relevant descent and realization statements.

Conceptually:

\[
\boxed{
\text{fine path transport}
\longrightarrow
\text{NatIso-invariant descent theory}
\longrightarrow
\Pi_1(M)\text{ only when justified}
}
\]

This preserves the KuuOS principle that presentation-independent meaning should be proved rather than obtained by prematurely collapsing path/coherence information.
