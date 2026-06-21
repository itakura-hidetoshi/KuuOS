# KuuOS Qi Process Window Trajectory v0.29

## Purpose

v0.29 turns ordered v0.28 candidate reports into a non-Markov trajectory candidate.

```text
ordered v0.28 reports
+ Qi Process Tensor lineage
+ visible uncertainty
→ process-window trajectory
```

The current report never replaces the full history.

## Core invariants

```text
single decline != future-window closure
oscillation != noise to erase
prior visible window != disposable history
constrained present != irreversibility
```

## Classes

```text
INSUFFICIENT_HISTORY
WINDOW_OPENING
WINDOW_STABLE_VISIBLE
WINDOW_OSCILLATING
WINDOW_CONSTRICTING
WINDOW_DORMANT_REOPENABLE
REVIEW_HANDOFF
```

A dormant-reopenable window preserves previous peak, scar depth, and reopening memory.

## Hysteresis

Repeated evidence is required before constriction. A single lower report cannot close the future window.

Stored metrics include:

- global and recent slope
- reversal count
- previous peak center
- scar depth
- reopening memory
- support and burden history
- evidence quality

## Classification order

```text
review handoff
→ insufficient history
→ oscillation preservation
→ dormant-reopenable
→ repeated constriction
→ opening
→ stable visible
→ reobserve
```

## Routes

```text
REOBSERVE
CONTINUE_TRAJECTORY_OBSERVATION
PRESERVE_OSCILLATION
PRESERVE_REOPENING_MEMORY
REVIEW_HANDOFF
HOLD
```

Routes remain candidate-only review surfaces.

## Persistence

```text
qi-window-trajectory-ledger-v0-29.jsonl
```

The ledger is append-only and replay-safe.

## Formal module

```text
KUOS.OpenHorizon.QiWindowTrajectoryKernelV0_29
```

Key theorems:

```lean
history_remains_primary
hysteresis_preserves_reopening
trajectory_remains_nonauthoritative
v028_open_future_is_preserved_by_v029
qi_window_trajectory_boundary
```

## Validation

```bash
PYTHONPATH=. python scripts/check_qi_window_v0_29.py
PYTHONPATH=. python -m unittest -v tests.test_qi_window_v0_29
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.OpenHorizon.QiWindowTrajectoryKernelV0_29
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
```
