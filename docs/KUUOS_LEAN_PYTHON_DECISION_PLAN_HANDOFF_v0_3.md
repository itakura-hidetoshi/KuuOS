# Lean → Python Decision / Plural / Wa / Plan handoff v0.3

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Source and scope

The source baseline is canonical `main` at
`3879c5c286ff469dcbf21f18af08db853f76c827` in `itakura-hidetoshi/KuuOS`.
This adds an optional, read-only audit to the existing chain:

```text
DecisionOS → DecisionOSPlural → DecisionOSWa → PlanOS
                                + exact Wa replan activation receipt
```

No original kernel, Lean declaration, public proof root, toolchain, mathlib
pin, host license, or protected PR is modified. The only existing-file change
appends the checker/test pair to the cumulative runtime runner; all previous
checks remain registered. Lean remains v4.30.0-rc2 and mathlib remains
5450b53e5ddc75d46418fabb605edbf36bd0beb6.

## Contract mapping

| Edge | Original constructor | Additional runtime checks |
|---|---|---|
| Decision → Plural | `build_initial_plural_state` | Exact source state / basis / committed digest; admissible candidate IDs; ordered projection of the original option records and its canonical digest |
| Plural → Wa | `build_initial_wa_state` | Exact prior selection and alternatives; option-digest map; recomputed utility, veto, aggregation and appeal-history digests |
| Wa → Plan | `build_initial_plan_state` | Exact Wa identity, basis, selected/endorsed/review options and history bindings; original route map; pending activation; complete replan receipt and its canonical digest |

The original Plural constructor accepts a separate `lineage_id`. This audit
additionally requires the same lineage and mission across the supplied chain.
That is an explicit tightening for this optional audit, not a claim that the
constructor or a Lean theorem already enforces it.

Receipt checks preserve the source Wa ID, lineage, source state/basis/commit,
route, endorsed and review options, and the Plan's replan/context/basis pointers.
The receipt must be future-only, at the replan phase, without memory overwrite
or host authority. Times must satisfy source ≤ receipt ≤ target. Source states
must be committed; a target may be an initial or a subsequently progressed state.

## Formal references and limits

The manifest in `EDGE_SPECS` points to named theorems in:

- `KUOS.DecisionOS.PluralHarmonyAppealKernelV0_2`:
  `pluralCommit_preserves_v01`, `pluralCommit_does_not_execute`.
- `KUOS.DecisionOS.WaRelationalHarmonyV0_3`:
  `waPlurality_preserves_veto_appeal_history`,
  `waPlurality_forbids_silent_substitution`, `wa_does_not_execute`.
- `KUOS.PlanOS.ReplanBoundSynthesisV0_1`:
  `plan_preserves_source_option_identity`,
  `plan_preserves_veto_appeal_history`, `plan_does_not_execute`.

These theorems retain their original Lean structures and hypotheses. Several
are projections of required boundary fields: they are not unconditional claims
about arbitrary Python data. The correspondence checker verifies eight named
declarations, three constructor field inventories, original validators/schema
constants, seven source Git blob hashes, and cumulative CI registration. It
does not run Lean, prove refinement, or prove the real-world interpretation of
any name. Existing formal proofs are not reset by this Python work.

## Results and non-authority

`audit_decision_plan_edge(...)` checks one supported edge.
`audit_decision_plan_chain(states, replan_activation_receipt=receipt)` requires
all four named nodes and all three edges. Decision → Plan is deliberately not
an accepted shortcut.

Results are `RUNTIME_CHECK_PASSED`, `NO_DATA`, or `BLOCKED`. Missing state,
intermediate layer, receipt, binding, or dependency is not silently supplied.
An observed contradiction takes precedence over missing data. `BLOCKED` is
an operational audit result, not a theorem that the mathematical construction
is impossible. Invalid schema data and dependency/validator failures cannot pass.

Only plain JSON-shaped data is admitted; nonfinite values and custom objects
are rejected. Equality preserves types, so `False` is not accepted as `0`.
Original validators run on independent copies; mutations, exceptions and
unexpected return types are reported. This bridge never calls an event apply,
issues an activation receipt, writes to a store, or invokes ActOS/host tools.
The audit does not activate itself inside existing kernels.

PASS certifies only the stated checks on supplied snapshots. It does not prove
receipt authenticity, trusted issuance, collision resistance, whole-history
replay, causal truth, Python/Lean refinement, or authority to execute/merge.
`execution_authority_granted` and `lean_python_refinement_proved` remain false.

## Verification

```sh
python3 scripts/check_kuuos_lean_python_decision_plan_bindings_v0_3.py
python3 -m unittest -v tests.test_kuuos_lean_python_decision_plan_handoff_v0_3
python3 scripts/run_kuuos_runtime_full_check_v0_55.py
```

The new suite contains 16 isolated contract tests and six genuine-kernel tests.
The latter use original state constructors and validators, through Wa and Plan
only, in temporary local stores. No validator is replaced and no ActOS/host
operation is invoked in those six tests. Self-consistently resealed candidate,
identity, history and receipt substitutions are tested, as is static-source
drift detection. The prior v0.1 and v0.2 tests remain part of the cumulative run.

Local isolated PASS is not independent CI certification. Final acceptance must
read the exact source/test-merge tree and completed workflow/job/step logs,
including the new checker and all 22 new tests. CI receipts, not this document,
record which exact commit was executed. Python-only changes do not claim a new
Strict Lean compilation or global formal acceptance.
