# MemoryOS v0.90 — Full Closed-Support Truth-Region Representation

## Scope

MemoryOS v0.90 advances the v0.89 finite sensor-support closure operator into an exact finite context representation.

For a finite homogeneous sensor family

\[
\sigma_i:G\to H,
\qquad i\in I,
\]

let

\[
\operatorname{cl}_r(S)
=
\{i\in I\mid K_r^S\le K_r^{\sigma_i}\}
\]

be the exact v0.89 support closure. The full context family is the collection of all closed supports

\[
\mathcal C_r
=
\{C\subseteq I\mid \operatorname{cl}_r(C)=C\}.
\]

For a sensor \(i\) and a premise support \(S\), define their truth regions inside the full context family by

\[
V_r(i)=\{C\in\mathcal C_r\mid i\in C\},
\qquad
V_r(S)=\{C\in\mathcal C_r\mid S\subseteq C\}.
\]

These regions are finite structural records. Their cardinalities are diagnostic-only and are never used for ranking, pruning, selection, or truth authority.

## Literature alignment

The immediate structural reference is the 2026 finite-closure result that a full indexed family of all closed theories exactly recovers closure consequence, while reduced indexed families may lose separating witnesses:

- Jaehwan Kim, *Closure Atlases and Local-to-Global Obstructions in Finite Closure Systems*, arXiv:2606.24909 (2026).

The lattice and attribute-dependency perspective is also consistent with:

- Bo Xiong and Steffen Staab, *From Tokens to Lattices: Emergent Lattice Structures in Language Models*, arXiv:2504.08778 (2025);
- Paul Poncet, *Order-generation in posets and convolution of closure operators*, arXiv:2509.05299 (2025).

Recent observability and sensor-selection work supplies domain context but not authority or optimization semantics for this certificate:

- Mohamad H. Kazma and Ahmad F. Taha, *Partitioning and Observability in Linear Systems via Submodular Optimization*, arXiv:2505.16169 (2025);
- Natalie L. Brace et al., *Sensor Placement on a Cantilever Beam Using Observability Gramians*, arXiv:2501.01726 (2025);
- Ege C. Kaya et al., *Randomized Greedy Methods for Weak Submodular Sensor Selection with Robustness Considerations*, arXiv:2404.03740 (2024).

MemoryOS v0.90 imports only the finite closure-representation idea. It does not import empirical language-model claims, submodular objectives, physical observability metrics, placement optimality, topological representation theorems, or atlas globalization.

## Selected-context soundness

Let \(\mathcal X\subseteq\mathcal C_r\) be any selected family of closed supports. If

\[
i\in\operatorname{cl}_r(S),
\]

then every selected closed context containing \(S\) also contains \(i\):

\[
\boxed{
 i\in\operatorname{cl}_r(S)
 \Longrightarrow
 V_{\mathcal X}(S)\subseteq V_{\mathcal X}(i)
}.
\]

Thus reduced context families are always sound for exact closure consequence.

The converse is not claimed for arbitrary reduced families. A reduced family may omit the closed support that separates a nonconsequence.

## Full-context completeness

Using every closed support restores the converse exactly:

\[
\boxed{
 i\in\operatorname{cl}_r(S)
 \iff
 V_r(S)\subseteq V_r(i)
}.
\]

More generally, for finite supports \(S,T\subseteq I\),

\[
\boxed{
 T\subseteq\operatorname{cl}_r(S)
 \iff
 V_r(S)\subseteq V_r(T)
}.
\]

The proof is constructive. For the reverse implication, the context

\[
C=\operatorname{cl}_r(S)
\]

is itself closed and contains \(S\). Region inclusion therefore forces every element of \(T\) into \(C\).

## Canonical separator witness

If a sensor is not implied,

\[
i\notin\operatorname{cl}_r(S),
\]

then the closure itself is the canonical separating context:

\[
\boxed{
C=\operatorname{cl}_r(S),
\quad
S\subseteq C,
\quad
\operatorname{cl}_r(C)=C,
\quad
i\notin C.
}
\]

No search or optimization is required. Every failed finite consequence has an explicit exact witness.

## Closure and kernel classification

Closing a premise does not change its truth region:

\[
\boxed{
V_r(\operatorname{cl}_r(S))=V_r(S).
}
\]

Consequently,

\[
\boxed{
V_r(S)=V_r(T)
\iff
\operatorname{cl}_r(S)=\operatorname{cl}_r(T)
\iff
K_r^S=K_r^T.
}
\]

The full truth region is therefore a third exact representation of the same finite observable class already represented by the v0.89 closure and the invisible kernel.

## Root independence

The v0.89 closure is root independent. Therefore the full closed-context family and every full truth region are also root independent:

\[
\mathcal C_r=\mathcal C_s,
\qquad
V_r(S)=V_s(S),
\qquad
V_r(i)=V_s(i).
\]

The four-root runtime records are consistency checks, not distinct physical claims.

## Canonical finite profiles

The full context families are exactly the v0.89 closed supports.

| Family | Full closed-context family |
|---|---|
| empty | \(\{\varnothing\}\) |
| identity | \(\{\varnothing,\{0\}\}\) |
| parity | \(\{\varnothing,\{0\}\}\) |
| terminal | \(\{\{0\}\}\) |
| identity + parity | \(\{\varnothing,\{1\},\{0,1\}\}\) |
| parity + terminal | \(\{\{1\},\{0,1\}\}\) |
| identity + parity + terminal | \(\{\{2\},\{1,2\},\{0,1,2\}\}\) |
| parity + parity | \(\{\varnothing,\{0,1\}\}\) |

The duplicate-parity profile illustrates why the full context family is structural rather than coordinate-counting: the two parity coordinates have identical truth regions and remain one exact kernel/closure class.

## Exact runtime ledger

- literature records: 6
- full-context profiles: 8
- sensor truth-region records: 48
- support truth-region records: 108
- consequence-representation records: 216
- canonical separator records: 60
- support-region equivalence records: 500
- kernel-region equivalence records: 500
- truth-region root-independence records: 432
- confidence-preservation records: 4

## Confidence policy

The v0.89 adjusted confidence values are preserved exactly. The new penalty is zero.

Truth-region size, context count, and separator count are diagnostic-only. They do not modify confidence and are not optimization objectives.

## Fail-closed source binding

The runtime first builds and validates the accepted v0.89 certificate. It binds the complete v0.89 certificate digest and a preservation-surface digest covering confidence and inherited boundary records.

It then verifies exhaustively across all eight canonical profiles and all four roots:

- every v0.89 closed support appears in the full context family;
- closure and premise truth regions are identical;
- closure consequence and full truth-region inclusion agree for every support/sensor pair;
- every nonconsequence has the closure as a valid separating context;
- truth-region equality agrees with closure equality and v0.89 kernel equality;
- all full truth regions are root independent;
- confidence and authority boundaries are unchanged.

Mutation of source digests, representation records, separator witnesses, confidence, or authority boundaries blocks issuance.

## Authority boundary

MemoryOS v0.90 does not claim:

- completeness of an arbitrary reduced context family;
- a universal concept-lattice classification;
- an atlas globalization or local-to-global obstruction theorem;
- a universal sensor classification;
- physical measurement or observability sufficiency;
- sensor placement optimality;
- candidate ranking, pruning, or selection;
- decision commit or receipt issuance;
- plan synthesis, activation, or execution;
- source or persistent-state mutation;
- verification or truth authority.
