# Qi Change Loop Forward Policy v2.6

This addendum clarifies the posture of the Qi change loop.

## Principle

The loop begins in a forward-biased posture.

It stops only when a concrete stop reason is observed.

## Concrete stop reasons

- repository scope mismatch
- branch scope mismatch
- head SHA mismatch
- unsuccessful required checks
- draft pull request
- non-mergeable pull request
- failed downstream call
- missing receipt surface
- missing audit surface

## Non-stop condition

The presence of a change loop is not itself a stop reason.

## Flow

```text
intent
  -> plan
  -> bridge
  -> gate
  -> result
  -> receipt
  -> audit
```

Future runtime changes should preserve this forward-biased posture while keeping concrete stop reasons visible.
