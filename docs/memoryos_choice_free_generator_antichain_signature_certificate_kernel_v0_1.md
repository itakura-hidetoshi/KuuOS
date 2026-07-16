# MemoryOS v0.94 — Choice-Free Minimal-Generator Antichain Signatures

## Status

MemoryOS v0.94 advances the v0.93 closure quotient without choosing one representative from a non-unique minimal-generator class.

For every proper closed sensor-support context, the complete finite family of all inclusion-minimal generators is retained as one canonical, choice-free signature.

The certificate is future-only and read-only. Signature size and antichain width are diagnostic only.

## Source frontier

- source frontier: MemoryOS v0.93
- source runtime: `runtime/kuuos_memoryos_minimal_generator_closure_quotient_certificate_kernel_v0_1.py`
- source manifest: `manifests/kuuos_memoryos_minimal_generator_closure_quotient_certificate_kernel_v0_1.json`
- exact base revision: `ba255f555c4f7eda858fdfa26ccd6c272caf8074`

## Choice-free signature

Let `cl_r` be the finite sensor-support closure and let `MinGen_r(M)` mean that `M` is inclusion-minimal in its closure class.

For a context `C`, define

```text
Sig_r(C) = { M | MinGen_r(M), cl_r(M) = C, and C is proper }.
```

For a support `S`, define its closure-class signature by

```text
ClassSig_r(S) = Sig_r(cl_r(S)).
```

No element of `Sig_r(C)` is selected as the preferred representative. The entire minimal-generator fiber is the invariant.

## Exact formal laws

### Nonempty proper signatures

If `C` is closed and proper, then `Sig_r(C)` is nonempty.

### Signature members remain inside the context

For every `M` in `Sig_r(C)`, `M` is a subset of `C`.

### Antichain law

For `M,N` in the same signature,

```text
M subset N  ->  M = N.
```

Thus every signature is an inclusion antichain. This is an exact structural statement, not a cardinality ranking.

### Context classification

For a proper closed context `C`,

```text
Sig_r(C) = Sig_r(D)  iff  C = D.
```

A generator cannot belong to signatures of two distinct contexts because its closure is unique.

### Kernel classification

For proper closed contexts `C,D`,

```text
Sig_r(C) = Sig_r(D)
  iff K_r^C = K_r^D.
```

For supports `S,T` with proper closure,

```text
ClassSig_r(S) = ClassSig_r(T)
  iff cl_r(S) = cl_r(T)
  iff K_r^S = K_r^T.
```

The antichain signature therefore gives a choice-free complete invariant of the proper closure/kernel quotient.

### Root independence

Both context signatures and support closure-class signatures are independent of the selected route root.

## Why this is a strict advance over v0.93

MemoryOS v0.93 proved that every closure class has at least one inclusion-minimal generator and that all proper minimal generators recover complete saturation.

A class can nevertheless have more than one incomparable minimal generator. Choosing one representative would introduce an arbitrary tie-breaking layer unrelated to closure or kernel truth.

MemoryOS v0.94 removes this ambiguity by making the entire minimal-generator antichain the invariant. Non-uniqueness is preserved rather than hidden.

## Literature alignment

The immediate knowledge-expansion context remains the 2026 Formal Concept Analysis work on iterative implication validation and inspectable counterexamples (`arXiv:2607.01773`).

The 2025 work on translating between irreducible closed sets and implicational bases in acyclic convex geometries (`arXiv:2506.24052`) emphasizes that conversion between closure-system representations is structurally connected to hypergraph dualization and can have nontrivial enumeration complexity.

The minimal-transversal literature (`arXiv:2407.00694`) provides the relevant antichain and hypergraph-dualization background. The certificate imports only the finite antichain pattern; it does not claim a new dualization complexity bound.

Additional alignment:

- `arXiv:2404.12229`
- `arXiv:1503.09025`
- `arXiv:1411.6432`
- Guigues–Duquenne, 1986

No empirical retrieval score or external oracle enters the formal result.

## Exact runtime ledger

- literature records: 7
- profile records: 8
- proper-context signature records: 8
- signature-member records: 8
- signature-nonempty records: 8
- signature-antichain pair records: 8
- proper-support signature records: 11
- signature/closure/kernel equivalence records: 27
- context signature/kernel classification records: 12
- distinct-context signature separation records: 4
- generator-own-signature records: 8
- root-independence records: 176
- confidence-preservation records: 4

The canonical S3 runtime exhaustively checks every proper support, every proper closed context, every ordered proper-support pair, every ordered proper-context pair, and all 16 source/target root pairs.

## Confidence

The inherited confidence vector is preserved exactly:

```text
1/3, 5/18, 11/54, 11/54
```

New penalty: `0`.

Signature cardinality, antichain width, and the number of minimal generators are diagnostic only.

## Scope boundary

This certificate does not introduce representative selection, unique-minimal-generator claims, a globally minimum implication basis, a canonical implication basis, a hypergraph-dualization complexity theorem, optimal query ordering, candidate ranking, plan activation, execution, state mutation, or truth authority.

## Files

- `formal/KUOS/OpenHorizon/MemoryOSChoiceFreeGeneratorAntichainSignaturesV0_94.lean`
- `formal/KuuOSMemoryOSV0_94.lean`
- `runtime/kuuos_memoryos_choice_free_generator_antichain_signature_certificate_kernel_v0_1.py`
- `scripts/check_planos_memoryos_choice_free_generator_antichain_signature_certificate_kernel_v0_1.py`
- `manifests/kuuos_memoryos_choice_free_generator_antichain_signature_certificate_kernel_v0_1.json`
- `runtime/kuuos_current_check_v0_93.py`
- `runtime/kuuos_current_check.py`
