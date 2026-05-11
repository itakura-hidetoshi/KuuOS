# Formal Verification Policy v0.1

## 1. Purpose

KuuOS uses formal verification as a witness layer. Verification can support claims, constraints, invariants, and release gates, but it does not create direct execution authority.

## 2. Verification Layers

The public core distinguishes:

1. **Specification**: natural-language and structured definitions.
2. **Validator**: executable checks for surface consistency.
3. **Proof Stub**: theorem target with explicit assumptions and gaps.
4. **Proof-Carrying Artifact**: artifact containing proof witness, assumptions, and replay information.
5. **Release Gate**: governance layer deciding whether a verified artifact may be promoted.

## 3. Accepted Proof Surfaces

KuuOS may use:

- Lean 4 / mathlib,
- Coq / MathComp / Coq-Analysis,
- Python validators for structural checks,
- YAML/JSON manifests for audit and release metadata,
- independent human or institutional review.

## 4. Proof Does Not Equal Final Truth

A proof is scoped by:

- assumptions,
- definitions,
- theorem statement,
- library version,
- replay environment,
- declared units,
- and release scope.

Therefore, proof success is a scoped witness, not an absolute metaphysical closure.

## 5. Required Metadata

Every formal artifact should state:

- artifact id,
- version,
- author,
- date,
- assumptions,
- theorem targets,
- known gaps,
- replay instructions,
- upstream dependencies,
- governance status.

## 6. Default Gate

If verification status is uncertain, KuuOS returns HOLD rather than silently promoting the artifact.

## 7. Public-Core Rule

The public repository may include theorem stubs, validators, and proof-carrying manifests. Stronger proof claims should include replayable artifacts or explicit external-review status.
