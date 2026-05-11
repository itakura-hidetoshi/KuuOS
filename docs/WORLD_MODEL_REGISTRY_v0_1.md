# WORLD Model Registry v0.1

## WORLDモデル登録簿

This document defines the registry structure for multiple WORLD models inside the KuuOS Mandala.

A WORLD model is a conventional operating surface under 世俗諦. It is not absolute reality and must not replace the fourfold core.

## 1. Registry Purpose

The registry makes each WORLD model explicit.

It prevents hidden WORLD replacement, hidden context shift, and silent collapse of multiple WORLDs into one model.

## 2. WORLD Model Entry

Each WORLD model should declare:

```yaml
world_model_entry:
  world_id: string
  name: string
  world_type: string
  layer: string
  membrane: string
  scope: string
  observer_position: string
  record_surface: string
  qi_flow_scope: string
  yinyang_frame_scope: string
  wuxing_phase_scope: string
  governance_boundary: string
  allowed_transports: list
  prohibited_transports: list
  known_obstructions: list
  status: DRAFT | ACTIVE | HOLD | QUARANTINE | RETIRED
```

## 3. WORLD Types

Examples:

```text
physical_world
body_world
clinical_world
memory_world
belief_world
planning_world
decision_world
proof_world
institutional_world
social_world
symbolic_world
ritual_world
ai_agent_world
```

## 4. Center Rule

No WORLD model is the center.

The center is always:

```text
空・縁起・二諦 gap・中道
```

A WORLD model that tries to replace the center fails the registry check.

## 5. Locality Rule

Each WORLD has local validity.

Its Qi flow, Yin-Yang frame, Wuxing phase, proof surface, and governance boundary are local unless transport is explicitly licensed.

## 6. Obstruction Rule

Known disagreements, conflicts, failed gluing, missing support, and governance barriers must be registered.

Obstruction is not a defect to hide. It is a first-class signal.

## 7. Status Values

```text
DRAFT:
  described but not active

ACTIVE:
  registered and usable under declared scope

HOLD:
  insufficient scope, boundary, or support

QUARANTINE:
  visible but not allowed for active operation

RETIRED:
  preserved for lineage but not active
```

## 8. Version

Version: v0.1
Date: 2026-05-11
Author: Hidetoshi Itakura / 板倉英俊
