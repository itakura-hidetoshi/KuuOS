# Fourfold Core Gate v0.1

## 空・縁起・二諦・中道ゲート

This document defines the first public runtime gate of KuuOS / 空OS.

A candidate may be an answer, proof, plan, memory update, policy, model output, document, or action proposal.

Before promotion, the candidate must pass the Fourfold Core Gate.

## 1. Gate Order

```text
candidate
  -> 空 gate
  -> 縁起 gate
  -> 二諦 gate
  -> 中道 gate
  -> status decision
```

The order matters.

空 first prevents premature reification.
縁起 then reconstructs conditional support.
二諦 separates 勝義諦 and 世俗諦 surfaces.
中道 prevents collapse to either absolutism or abandonment.

## 2. 空 Gate

Question:

```text
Does the candidate claim independent self-authority?
```

Blocks:

- absolute claim without scope,
- proof treated as unrestricted authority,
- model output treated as world itself,
- identity fixed as essence,
- memory treated as final reality.

Possible outputs:

```text
PASS: no self-authorizing claim detected
HOLD: scope or condition is unclear
FAIL: candidate depends on explicit reification
```

## 3. 縁起 Gate

Question:

```text
Are the arising conditions visible?
```

Requires:

- conditions,
- relations,
- memory lineage if relevant,
- support trace,
- scope,
- constraints.

Possible outputs:

```text
PASS: support relation is visible
HOLD: support is incomplete but repairable
FAIL: support is absent or contradictory
```

## 4. 二諦 Gate

Question:

```text
Does the candidate distinguish 勝義諦 from 世俗諦?
```

Required distinction:

- 勝義諦: non-reifying emptiness and no independent essence.
- 世俗諦: responsible conventional operation under declared scope.

Possible outputs:

```text
PASS: distinction preserved
HOLD: distinction unclear
FAIL: distinction collapsed
```

## 5. 中道 Gate

Question:

```text
Does the candidate avoid both reification and abandonment?
```

Blocks:

- absolutizing conventional models,
- erasing responsibility in the name of emptiness,
- forcing premature closure,
- refusing useful conventional action when support exists.

Possible outputs:

```text
PASS: dynamic balance preserved
HOLD: balance unclear
REVIEW: human or external review needed
FAIL: collapse is structural
```

## 6. Status Aggregation

```text
if any gate == FAIL:
  final_status = FAIL
elif any gate == REVIEW:
  final_status = REVIEW
elif any gate == HOLD:
  final_status = HOLD
else:
  final_status = PASS
```

PASS means eligible for later governance. It does not mean execution authority.

## 7. Minimal Receipt

```yaml
fourfold_core_gate_receipt:
  candidate_id: string
  emptiness_gate: PASS | HOLD | FAIL
  dependent_origination_gate: PASS | HOLD | FAIL
  two_truths_gate: PASS | HOLD | FAIL
  middle_way_gate: PASS | HOLD | REVIEW | FAIL
  final_status: PASS | HOLD | REVIEW | FAIL
  notes: string
```

## 8. Version

Version: v0.1
Date: 2026-05-11
Author: Hidetoshi Itakura / 板倉英俊
