# Qi Motion Chain Runbook v0.1

## Status

This runbook is an append-only operational entrypoint for the current KuuOS Qi implementation chain.

It does not add new authority. It only orders existing validators and adapters into a reproducible check sequence.

## Chain

```text
Samvrti Qi Runtime
  -> Samvrti Qi to Physical Motion Evidence Builder
  -> Physical Quantum Qi Runtime
  -> Physical Quantum Qi Dynamics Kernel
  -> Physical Quantum Qi Motion Pipeline
```

## Core invariant

The chain keeps the following rule:

```text
observed conventional flow
  -> conservative evidence packet
  -> evidence-bound validated_type
  -> licensed dynamics terms
  -> bounded motion candidate
  -> observe-only output
```

## Non-authority boundary

Every stage must preserve:

```text
execution_authority = false
belief_commit_authority = false
memory_overwrite_authority = false
world_root_rewrite_authority = false
safety_override_authority = false
direct_execution_allowed = false
authority_expansion = false
observe_only = true
```

## Local command

```bash
make qi-motion-chain-checks
```

Equivalent direct command:

```bash
python3 scripts/run_qi_motion_chain_checks_v0_1.py
```

## Included checks

The runner executes:

```text
examples/samvrti_qi_runtime_adapter_minimal.py
scripts/validate_samvrti_qi_runtime_v0_1.py
examples/samvrti_qi_to_physical_motion_evidence_builder_minimal.py
scripts/validate_samvrti_qi_to_physical_motion_evidence_builder_v0_1.py
scripts/validate_physical_quantum_qi_runtime_contract_v0_1.py
scripts/validate_physical_quantum_qi_runtime_release_packet_v0_1.py
examples/physical_quantum_qi_dynamics_kernel_minimal.py
scripts/validate_physical_quantum_qi_dynamics_kernel_v0_1.py
examples/physical_quantum_qi_motion_pipeline_minimal.py
scripts/validate_physical_quantum_qi_motion_pipeline_v0_1.py
```

## Meaning of PASS

PASS means the public Qi motion chain is structurally consistent and self-checking.

PASS does not mean:

```text
truth authority
clinical authority
execution authority
final theorem authority
institutional authority
```

The output remains a bounded, evidence-grounded, observe-only Qi motion candidate.
