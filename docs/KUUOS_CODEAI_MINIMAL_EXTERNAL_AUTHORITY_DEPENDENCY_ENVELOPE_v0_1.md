# KuuOS CodeAI Minimal External Authority Dependency Envelope v0.1

Status: additive authority-minimization sibling

Version: v0.1

Predecessor: CodeAI Autonomous Git Lifecycle Envelope v0.1

## 1. Purpose

This surface prevents human handover, deploy authority, and secret mutation from
becoming the default CodeAI critical path. It does not erase those authority
boundaries. It orders the available responses so that the narrowest dependency
is always considered first:

```text
internal substitute
  -> unaffected internal work
  -> existing short-lived capability
  -> one minimal request packet
  -> non-blocking hold / degrade / abstain
```

Each evaluation emits at most one next-effect lease. A completed autonomous Git
lifecycle receipt supplies provenance only; it does not grant external
authority.

## 2. Relationship to existing surfaces

This sibling does not replace Autonomous Git Lifecycle v0.1, the repository
live-mutation series, deployment systems, secret stores, or human decision
owners. Their validators retain their own branches.

The adapter owns dependency reduction and exact capability matching. The
external system owns the actual deploy, secret mutation, or nondelegable human
decision. The runtime records an authorization candidate or observed result but
does not execute an effect itself.

## 3. Preserved invariants

```text
source receipt != external authority
internal substitute authority != deploy authority
request packet authority != external effect authority
deploy authority != secret mutation authority
secret mutation authority != secret read authority
opaque handle digest != secret material
human request packet != human handover performed
external result != truth
one dependency receipt <= one next-effect lease
missing authority != authority self-escalation
```

The following remain unavailable:

- plaintext secret access or disclosure;
- human-handover authority;
- persistent or multi-use external capabilities;
- scope widening, target substitution, or action substitution;
- blocking handover as a policy default;
- production deploy unless an exact target is explicitly allowed by a future
  policy sibling;
- capability creation, privilege escalation, or external effect execution by
  the kernel.

## 4. Bottleneck-minimization ladder

### 4.1 Internal substitute

If an internal simulation, preview, package, local verification, dry run, or
equivalent artifact can satisfy the dependency, the adapter authorizes that
substitute before any external request.

### 4.2 Unaffected internal work

If the external dependency is not on the current critical path, the adapter
issues one lease to continue independent internal work. The dependency remains
visible; it is not silently treated as completed.

### 4.3 Existing preauthorization

Deploy and secret mutation may receive one external-effect lease only when an
already issued capability is:

- bound to the exact effect kind and scope digest;
- short lived and unexpired;
- one shot and unconsumed;
- allowed by the sealed policy;
- represented by a digest rather than exposed credentials.

The adapter cannot create or widen this capability.

### 4.4 Minimal request packet

When no substitute or valid capability exists, the adapter may authorize the
creation of one packet containing only:

- effect kind, target, action, and scope digest;
- payload or artifact digest;
- provenance and source receipt digest;
- a single decision or capability request.

Packet creation is an internal preparation effect. It is not a handover,
deploy, or secret mutation.

### 4.5 Non-blocking hold

After a packet is prepared, the dependency enters hold. Independent work may
continue when declared available. `critical_path_blocked` becomes true only
when no authorized substitute or parallel route remains and the external
result is actually necessary.

## 5. Domain contracts

### 5.1 Human and external-authority handover

Human handover is a last-resort request packet for an explicitly
nondelegable decision. This surface never grants human-handover authority and
never marks control transfer as performed. A returned bounded decision receipt
may satisfy the dependency without transferring the rest of the trajectory.

### 5.2 Deploy

Deploy authority is restricted to the exact artifact digest, target, action,
scope, and one-shot capability. The base policy example allows a staging
activation only. Build, test, packaging, preview, and rollback preparation stay
internal wherever possible.

### 5.3 Secret mutation

Secret mutation uses an opaque broker capability. The permitted operation is
an exact mutation such as version rotation; secret read and plaintext return
remain forbidden. Receipts carry only capability, scope, request, and result
digests.

## 6. Inputs

The envelope consumes four sealed inputs:

1. a completed CodeAI Autonomous Git Lifecycle v0.1 receipt;
2. an exact external-dependency request;
3. monotone observed dependency state;
4. a bounded dependency policy.

All inputs require exact field sets, strict types, canonical digests,
provenance confirmation, source correspondence, freshness, and replay-safe
session and nonce lineage.

## 7. Route order

The first matching route wins.

| Priority | Disposition | Mode | Next phase |
|---:|---|---|---|
| 1 | `source_git_lifecycle_receipt_repair_required` | `rejected` | `none` |
| 2 | `external_dependency_provenance_repair_required` | `rejected` | `none` |
| 3 | `external_dependency_state_evidence_repair_required` | `rejected` | `none` |
| 4 | `external_dependency_correspondence_repair_required` | `rejected` | `none` |
| 5 | `external_dependency_window_repair_required` | `rejected` | `none` |
| 6 | `external_dependency_replay_conflict_rejected` | `rejected` | `none` |
| 7 | `unsupported_external_dependency_scope_abstained` | `abstain` | `none` |
| 8 | `plaintext_secret_path_rejected` | `rejected` | `none` |
| 9 | `unowned_external_effect_observed_rejected` | `rejected` | `none` |
| 10 | `external_dependency_state_repair_required` | `rejected` | `none` |
| 11 | `external_effect_failed_degraded` | `degraded_autonomy` | `await_external_authority` |
| 12 | `minimal_external_dependency_completed` | `completed` | `complete` |
| 13 | `autonomous_internal_substitute_authorized` | `internal_substitute_authorized` | `execute_internal_substitute` |
| 14 | `unaffected_internal_work_continues` | `unaffected_internal_work_authorized` | `continue_unaffected_internal_work` |
| 15 | `preauthorized_bounded_deploy_authorized` | `preauthorized_external_effect_authorized` | `execute_bounded_deploy` |
| 16 | `preauthorized_bounded_secret_mutation_authorized` | `preauthorized_external_effect_authorized` | `execute_bounded_secret_mutation` |
| 17 | `minimal_external_request_packet_authorized` | `minimal_external_request_packet_authorized` | `prepare_minimal_external_request_packet` |
| 18 | `external_authority_pending_nonblocking_hold` | `nonblocking_external_authority_hold` | `await_external_authority` |

## 8. Effect and result semantics

```text
effect_execution_performed_by_kernel = false
human_handover_authority_granted = false
secret_access_authority_granted = false
capability_handle_exposed = false
blocking_handover_allowed = false
```

Deploy and secret mutation are distinct one-effect leases. Packet preparation
and internal continuation are also distinct effects. A consumer must return a
fresh sealed state after consuming any lease. Expired, consumed, mismatched, or
multi-use capabilities cannot authorize an external effect.

An observed external result completes only the bounded dependency. It is not a
correctness proof, truth claim, or authority for another dependency.

## 9. Validation

The checker covers all 18 dispositions. Unit tests cover the minimization
ladder, nonblocking work, deploy capability matching, opaque secret mutation,
expired capability fallback, handover packet deferral, plaintext rejection,
degradation, completion, tamper closure, and one-effect exclusivity.

The independent Lean root proves that internal substitution, continuation,
deploy, secret mutation, and request-packet authority are separated; human
handover and secret access remain excluded; and external results are not truth.

## 10. Implementation map

- Runtime:
  `runtime/kuuos_codeai_minimal_external_authority_dependency_envelope_v0_1.py`
- Checker:
  `scripts/check_codeai_minimal_external_authority_dependency_envelope_v0_1.py`
- Tests:
  `tests/test_kuuos_codeai_minimal_external_authority_dependency_envelope_v0_1.py`
- Example:
  `examples/codeai_minimal_external_authority_dependency_envelope_v0_1.json`
- Manifest:
  `manifests/kuuos_codeai_minimal_external_authority_dependency_envelope_v0_1.json`
- Formal package:
  `formal/KUOS/CodeAI/MinimalExternalAuthorityDependencyEnvelopeV0_1.lean`
- Formal root:
  `formal/KuuOSCodeAIMinimalExternalAuthorityDependencyV0_1.lean`
- Workflow:
  `.github/workflows/codeai-minimal-external-authority-dependency-envelope-v0-1.yml`
