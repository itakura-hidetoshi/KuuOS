# KuuOS Lean→Python v0.48 — Original VerifyOS→PlanOS certificate seam

**Research stage: proposal, not independently Lean-certified until the exact PR HEAD succeeds.**

Canonical base: `a32f6e42733015c82a5cde7a465ecacb429675aa`. Fixed Lean: `v4.30.0-rc2`. Fixed mathlib:
`5450b53e5ddc75d46418fabb605edbf36bd0beb6`.
append-only / tighten-only / overwrite-forbidden / same-root.
No canonical root, dependency manifest, older proofs, or Python kernels are modified.

## Actual original Lean source types

- `KUOS.VerifyOS.MiddleWayConditionalContinuityVerificationV0_4.MiddleWayContinuityCertificate`
- `KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03.MiddleWayBoundedSynthesisIntakeCertificate`
- Inherits the separately proved original DecisionOS v0.8↔mapped v0.46 Equiv/Iff from v0.47.

The new `OriginalCertificateSeam` requires exactly seven typed equalities:
transition, conditional status, provenance lineage, predecessor, responsibility,
dissent, and minority evidence. Without this exact seam, it does not transfer
the VerifyOS result to PlanOS. The imported original Finset monotonicity proofs
then preserve membership through the second original type. PlanOS admission
equals the `retain` transition, not host execution.

`inertPlanOfVerify` is an explicitly constructed formal certificate with
unchanged provenance and all authority booleans false. This witnesses
consistency/possible descent of the *formal* seam, not an actual Python call
or an external-issued plan receipt.

## Actual original Python kernel projection

`runtime/kuuos_lean_python_original_verify_plan_certificate_seam_v0_48.py`
reads two supplied outputs of the original, unchanged VerifyOS v0.4 and
PlanOS v1.03 kernels. It verifies full native digest seals, finite route
status, 13 shared source fields, exact native `transition_spec` projection,
canonical provenance lists, predecessor, responsibility monotonicity,
resulting PlanOS responsibility extension, and authority flags. It is read-only.

Unlike a complete Lean Finset representation, actual native PlanOS output
does **not** independently serialize the resulting lineage/dissent/minority
sets. The corresponding Python properties remain **NO_DATA** and the
audit result explicitly sets `plan_resulting_lineage_finset_certified=false`.
Hash equality is not proof that two execution calls share a real causal
history. The Python function does not invoke the original kernels; the
regression tests independently call the original builders in all six cases
and pass the resulting complete certificates.

## Certification and obstruction

Run pinned exact-head Strict Lean with `-DwarningAsError=true` and
`-DsorryAsError=true`, individually inspect eleven `#print axioms` outputs,
run complete Python Runtime and targeted regression, original public-API
tests, Governance, exact-head, and Git tree equality.

No general Lean↔CPython semantic equivalence, no external issuer
authentication, no six-case single causal timeline, no global descent,
no PlanOS synthesis, and no ActOS host execution authority is asserted.

Preference ⇏ Descent ⇏ Authority.

Only source-derived, independently certified claims may be promoted. New
research PR remains Draft/unmerged until the *actual* candidate is green.

## 追加静的認証の独立実行

v0.48で新設した原本ソース固定チェッカーを、Python Runtimeの実際の
unittest suiteから明示的に呼び出す。Git blob一致・原本imports・
全宣言の存在と公理監査命令数に加え、原本Leanの改変と
新Lean宣言の欠落を模擬した負例がfail-closedとなることを検査する。
チェッカーの静的検査はLeanの形式的証明を代用しない。
