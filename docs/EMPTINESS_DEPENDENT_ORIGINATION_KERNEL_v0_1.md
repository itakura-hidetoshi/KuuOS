# Emptiness–Dependent Origination Kernel v0.1

## 空・縁起カーネル

This document defines the first kernel of KuuOS / 空OS.

The root relation is:

```text
空 prevents reification.
縁起 restores relational arising.
```

## 1. 空 as De-Reification

空 is the de-reification operator of KuuOS.

It prevents any surface from becoming self-authorizing:

- answer,
- proof,
- memory,
- plan,
- policy,
- metric,
- model,
- identity,
- module,
- world description.

A surface fails the emptiness check when it claims authority without conditions.

```text
emptiness_kernel:
  input: candidate_surface
  detects:
    - self_authority_claim
    - absolute_identity_fixation
    - hidden_totalization
    - unscoped_truth_claim
  output:
    - de_reified_surface
    - required_conditions
    - hold_if_unresolved
```

## 2. 縁起 as Relational Re-Construction

縁起 is the relational reconstruction operator.

After 空 removes self-authority, 縁起 asks:

```text
Through what conditions does this arise?
Through what relations is this supported?
Through what memory lineage is this traceable?
Through what constraints is this permitted?
Through what world-context is this meaningful?
```

```text
dependent_origination_kernel:
  input: de_reified_surface
  requires:
    - conditions
    - relations
    - lineage
    - causal_or_support_trace
    - scope
    - constraints
  output:
    - conditionally_valid_surface
    - missing_supports
    - relational_trace
```

## 3. Kernel Composition

The core composition is:

```text
candidate_surface
  -> emptiness_kernel
  -> dependent_origination_kernel
  -> two_truths_separation
  -> middle_way_bridge
```

空 without 縁起 can collapse into mere negation.

縁起 without 空 can collapse into reified relationalism.

Therefore, KuuOS requires both.

## 4. Runtime Failure Modes

```text
reification_failure:
  cause: surface claims self-authority
  response: apply emptiness_kernel

empty_negation_failure:
  cause: emptiness used to erase responsibility or operation
  response: require dependent_origination_kernel

unsupported_relation_failure:
  cause: relation is asserted without trace
  response: HOLD and request support trace

scope_failure:
  cause: candidate exceeds declared conditions
  response: rescope or FAIL
```

## 5. Relation to Two Truths and Middle Way

空 prepares 勝義諦 by preventing self-nature claims.

縁起 prepares 世俗諦 by reconstructing responsible operation through conditions.

中道 prevents either side from collapsing into absolutism or abandonment.

## 6. Version

Version: v0.1
Date: 2026-05-11
Author: Hidetoshi Itakura / 板倉英俊
