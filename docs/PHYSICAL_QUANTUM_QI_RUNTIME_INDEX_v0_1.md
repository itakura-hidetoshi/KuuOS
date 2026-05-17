# Physical Quantum Qi Runtime Index v0.1

This index lists the public KuuOS files that implement the first Physical Quantum Qi runtime layer.

## Runtime contract

```text
docs/PHYSICAL_QUANTUM_QI_RUNTIME_CONTRACT_v0_1.md
```

Defines Qi as an evidence-bound relation-flow packet that arises on the conventional appearance side after dependent-origination difference, string/brane organization, gauge transport, curvature/holonomy accounting, current coupling, open quantum thermodynamics, and recovery accounting.

## Machine-readable spec

```text
specs/physical_quantum_qi_runtime_contract_v0_1.json
```

Defines QiType ordering, PhysicalQi evidence, FullPathQi evidence, fatal reject flags, authority boundaries, and the MGAP4D `33/20` mass-gap stability-floor role.

## Example packet

```text
examples/physical_quantum_qi_runtime_packet_v0_1.json
```

A positive example that validates as `FullPathQi` because it includes the PhysicalQi evidence bundle and SK/FV history evidence.

## Validation cases

```text
validation_cases/physical_quantum_qi_runtime_validation_cases_v0_1.json
```

Covers:

- FullPathQi pass,
- claimed FullPathQi downgraded to PhysicalQi when SK/FV evidence is missing,
- missing Ward/leak identity downgraded to CurrentQi,
- gap-as-source rejected,
- attempted execution authority rejected.

## Validator

```text
scripts/validate_physical_quantum_qi_runtime_contract_v0_1.py
```

Classifies Qi from evidence rather than from `claimed_type`, rejects forbidden authority, and keeps the mass gap as a stable floor rather than a Qi source.

## Make target

```bash
make physical-quantum-qi-runtime-checks
```

Passing validation means the public Qi runtime packet structure is internally consistent. It does not grant proof, ontology, clinical, execution, or final decision authority.
