# Dependent-origination native CPTP Choi-word formalization v0.11

## Purpose

v0.10 proved the finite-dimensional Choi theorem directly against Mathlib:

\[
J_\Phi \succeq 0
\iff
\Phi\text{ is Mathlib completely positive}.
\]

v0.11 turns that equivalence into the finite-history operational closure needed by the quantum process-tensor spine.

## Native CP composition

For Mathlib native completely-positive maps

\[
\Phi:M_n(\mathbb C)\to M_m(\mathbb C),\qquad
\Psi:M_m(\mathbb C)\to M_k(\mathbb C),
\]

`cpComp Ψ Φ` is constructed by discharging Mathlib's actual amplified positivity field:

\[
(id_r\otimes\Psi\circ\Phi)(X)
=
(id_r\otimes\Psi)((id_r\otimes\Phi)(X))\ge 0
\]

for every amplification size `r` and every positive block matrix `X`.

No separate surrogate notion of complete positivity is introduced.

## Trace-preserving composition

If both maps preserve matrix trace, then

\[
\operatorname{Tr}(\Psi(\Phi(X)))
=
\operatorname{Tr}(\Phi(X))
=
\operatorname{Tr}(X).
\]

This yields causal composition of `MathlibCPChannelCertificate` values, i.e. native CPTP maps.

## Choi link product closure

For two CPTP certificates, v0.9 gives

\[
J_{\Psi\circ\Phi}=J_\Phi\star J_\Psi.
\]

Combining v0.10 complete positivity with trace preservation proves

\[
J_\Phi\star J_\Psi\succeq0
\]

and

\[
\operatorname{Tr}_{out}(J_\Phi\star J_\Psi)=I.
\]

Thus the link product is itself packaged as a normalized positive Choi channel certificate.

## Finite ordered CPTP words

For an ordered word of channels

\[
w=[\Phi_1,\dots,\Phi_N],
\]

`cptpWordOperator` uses the same convention as the earlier dependent-origination history spine:

\[
\operatorname{Op}([])=I,
\qquad
\operatorname{Op}(\Phi::w)=\Phi\circ\operatorname{Op}(w).
\]

The underlying complex-linear map is exactly v0.9 `complexInterventionWordOperator`.

The complete linked Choi word

\[
J_w
=
J_{\Phi_N}\star\cdots\star J_{\Phi_1}
\]

is proved equal to

\[
J_{\operatorname{Op}(w)}.
\]

Therefore every finite CPTP word satisfies

\[
J_w\succeq0,
\qquad
\operatorname{Tr}_{out}J_w=I.
\]

The file packages this as `cptpWordChoiCertificate`.

## Density matrices

A `DensityMatrix d` contains

\[
\rho\succeq0,
\qquad
\operatorname{Tr}\rho=1.
\]

Every native CPTP channel maps density matrices to density matrices. Hence every finite CPTP history preserves both positivity and unit trace.

The evolved density matrix also has exact linked-Choi reconstruction:

\[
\rho_w
=
\operatorname{fromChoi}(J_w)(\rho).
\]

This is theorem `evolveDensity_matrix_eq_fromChoi`.

## Architectural consequence

The quantum spine now has the exact chain

```text
non-Markov enlarged-state transport
→ operational process tensor
→ exact finite-dimensional Choi representation
→ deterministic quantum-comb matrix causality
→ Choi positivity iff native Mathlib CP
→ native CPTP channel composition
→ finite positive normalized Choi histories
→ density-state preservation
```

The next independent layer is quantum instruments and contraction against a deterministic comb. That layer must prove probability positivity and total normalization; it is intentionally not inferred from an arbitrary linear readout.

## Scope

This is finite-dimensional complex matrix algebra. It does not assert an infinite-dimensional Choi theorem, a physical Yang–Mills process tensor, or that every v0.8 real-linear intervention is automatically CPTP.
