# ObserveOS repository structure

ObserveOS is maintained as a first-class subsystem of KuuOS. This index connects the public architecture, runtime, formal verification, manifests, checks, and CI without packaging the implementation as a ZIP archive.

## Architecture

```text
LearnOS future-only maintenance disposition
  -> ObserveOS v0.6 bounded maintenance-monitoring observation
  -> ObserveOS v0.7 sequential epistemic observability envelope
  -> VerifyOS independent verification
```

Observation remains distinct from verification, learning activation, policy activation, WORLD mutation, tool invocation, and external side effects.

## Stable ownership boundaries

```text
observation != verification
WORLD intake != WORLD update
WORLD sidecar != exact WORLD
receipt composition != receipt construction
learning != present-cycle mutation
```

ObserveOS may accept a source-bound WORLD evidence envelope, but intake does not mutate WORLD and a sidecar representation is not the exact WORLD state. Receipt composition preserves existing receipts rather than constructing or promoting them, and learning remains future-only. These boundaries are compatibility contracts shared with the cumulative runtime checker.

## v0.7 implementation map

### Specification

- [`../OBSERVEOS_SEQUENTIAL_EPISTEMIC_OBSERVABILITY_ENVELOPE_v0_1.md`](../OBSERVEOS_SEQUENTIAL_EPISTEMIC_OBSERVABILITY_ENVELOPE_v0_1.md)

### Runtime entry point

- [`../../runtime/kuuos_observeos_sequential_epistemic_observability_envelope_v0_1.py`](../../runtime/kuuos_observeos_sequential_epistemic_observability_envelope_v0_1.py)

### Runtime layers

1. [`common`](../../runtime/kuuos_observeos_sequential_epistemic_observability_common_v0_1.py) — constants, schemas, canonical digests, result contract
2. [`preflight`](../../runtime/kuuos_observeos_sequential_epistemic_observability_preflight_v0_1.py) — exact packet and policy admission
3. [`validators`](../../runtime/kuuos_observeos_sequential_epistemic_observability_validators_v0_1.py) — Trace Context, PROV-O, confidence sequence, conformal, ADWIN, source receipt
4. [`sampling`](../../runtime/kuuos_observeos_sequential_epistemic_observability_sampling_v0_1.py) — exact sample accounting, missingness, observation window, replay, negative effects
5. [`evaluation`](../../runtime/kuuos_observeos_sequential_epistemic_observability_evaluation_v0_1.py) — deterministic 14-route disposition
6. [`receipt`](../../runtime/kuuos_observeos_sequential_epistemic_observability_receipt_v0_1.py) — immutable observability receipt construction

### Formal verification

- Kernel: [`../../formal/KUOS/ObserveOS/SequentialEpistemicObservabilityEnvelopeV0_7.lean`](../../formal/KUOS/ObserveOS/SequentialEpistemicObservabilityEnvelopeV0_7.lean)
- Formal root: [`../../formal/KuuOSObserveOSV0_7.lean`](../../formal/KuuOSObserveOSV0_7.lean)
- Aggregate import: [`../../formal/KUOS.lean`](../../formal/KUOS.lean)
- Lake target registration: [`../../lakefile.toml`](../../lakefile.toml)

### Machine-readable contract

- [`../../manifests/kuuos_observeos_sequential_epistemic_observability_envelope_v0_1.json`](../../manifests/kuuos_observeos_sequential_epistemic_observability_envelope_v0_1.json)

### Validation

- Route checker: [`../../scripts/check_observeos_sequential_epistemic_observability_envelope_v0_1.py`](../../scripts/check_observeos_sequential_epistemic_observability_envelope_v0_1.py)
- GitHub Actions: [`../../.github/workflows/observeos-sequential-epistemic-observability-v0-1.yml`](../../.github/workflows/observeos-sequential-epistemic-observability-v0-1.yml)

## v0.7 disposition tree

```text
source receipt invalid        -> source repair
trace context invalid         -> trace repair
required signals absent       -> signal repair
provenance invalid            -> provenance repair
sample partition invalid      -> sample-accounting repair
missingness exceeds budget    -> missingness review
distribution shift detected   -> distribution-shift review
sequential evidence invalid   -> sequential-uncertainty repair
conformal gap exceeds budget  -> conformal-calibration repair
observation window invalid    -> observation-window repair
session/nonce/packet replay   -> replay rejection
current-state effect claimed  -> mutation rejection
authority escalation claimed  -> authority rejection
all predicates satisfied      -> supported envelope
```

## Literature and standards bindings

- W3C Trace Context
- OpenTelemetry traces, metrics, logs, and baggage
- W3C PROV-O
- time-uniform confidence sequences and e-process evidence
- conformal prediction calibration evidence
- ADWIN distribution-shift evidence

ObserveOS validates structure, lineage, declared budgets, and routing invariants. Independent statistical reproduction and truth verification remain VerifyOS responsibilities.
