# Cross-WORLD Transport Gate v0.1

## WORLD間輸送ゲート

This document defines how KuuOS transports candidates between WORLD models inside the Multi-WORLD Mandala.

Transport is not automatic.

A candidate may move from one WORLD model to another only through a declared gate, membrane, and transport law.

## 1. Transport Chain

```text
WORLD_A
  -> source membrane
  -> transport gate
  -> transport law
  -> target membrane
  -> WORLD_B
```

## 2. Transport Candidate

A candidate may be:

- concept,
- meaning,
- Qi pattern,
- Yin-Yang frame,
- Wuxing phase,
- proof surface,
- memory trace,
- plan,
- policy,
- action candidate,
- clinical interpretation,
- symbolic or ritual structure.

## 3. Required Fields

```yaml
cross_world_transport_request:
  candidate_id: string
  source_world_id: string
  target_world_id: string
  candidate_type: string
  source_scope: string
  target_scope: string
  source_membrane: string
  target_membrane: string
  declared_transport_law: string
  expected_transformation: preserve | transform | reinterpret | quarantine | reject
  obstruction_check: string
  governance_boundary_check: string
```

## 4. Transport Modes

```text
preserve:
  candidate is carried with meaning largely preserved

transform:
  candidate is translated through declared rules

reinterpret:
  candidate becomes advisory or symbolic in target WORLD

quarantine:
  candidate is visible but not active in target WORLD

reject:
  candidate may not enter target WORLD
```

## 5. Gate Checks

### 5.1 Source Validity

Is the candidate valid in the source WORLD under declared scope?

### 5.2 Target Eligibility

Can the target WORLD receive this kind of candidate?

### 5.3 Membrane Compatibility

Are source and target membranes declared?

### 5.4 Transport Law

Is there a visible law for how meaning, Qi, polarity, proof, or action changes across the transport?

### 5.5 Obstruction Visibility

Are conflicts, mismatches, proof gaps, or risk signals preserved?

### 5.6 Governance Boundary

Does transport preserve safety, privacy, authority, and release constraints?

## 6. Output

```text
PASS:
  transport is allowed under declared scope

HOLD:
  insufficient support or unclear law

TRANSFORM:
  transport allowed only with declared transformation

QUARANTINE:
  target WORLD may see candidate but not activate it

REJECT:
  transport is not allowed
```

## 7. Guardrails

Cross-WORLD Transport Gate must not allow:

- hidden transport,
- silent reinterpretation,
- source WORLD authority overriding target WORLD boundary,
- target WORLD absorbing source WORLD without trace,
- proof surface becoming execution authority,
- clinical or operational action without governance.

## 8. Version

Version: v0.1
Date: 2026-05-11
Author: Hidetoshi Itakura / 板倉英俊
