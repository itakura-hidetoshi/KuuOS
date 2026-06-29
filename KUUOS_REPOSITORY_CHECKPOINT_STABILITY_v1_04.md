# KuuOS Repository Checkpoint Stability v1.04

v1.04 verifies that a checkpoint confirmed by v1.03 remains present, unchanged, uniquely named, and reachable after a bounded delay.

It is a read-only stability and immutability layer. It does not delete, overwrite, restore, retarget, force-update, publish, or push a checkpoint.

## Functional boundary

The verifier revalidates the complete v1.03 creation receipt and its original inputs, then binds three later observations:

1. a delayed direct checkpoint-reference observation,
2. an object-database reachability observation,
3. a checkpoint-namespace uniqueness observation.

A stable checkpoint must retain the exact authorized OID, remain a direct non-symbolic reference under `refs/kuuos/checkpoints/`, resolve to a present commit object, and have one unique checkpoint name.

## Failure dispositions

The result distinguishes:

- `CHECKPOINT_LOST`,
- `CHECKPOINT_SUBSTITUTED`,
- `CHECKPOINT_NAME_CONFLICT`,
- `CHECKPOINT_OBJECT_UNREACHABLE`,
- `CHECKPOINT_UNSTABLE_WINDOW`,
- `EVIDENCE_INVALID`.

No failure disposition grants recovery or mutation authority.

## Validation

```bash
python3 -m unittest -v tests.test_kuuos_repository_checkpoint_stability_v1_04
python3 runtime/kuuos_v104_check.py
```
