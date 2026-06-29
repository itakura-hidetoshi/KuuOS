# KuuOS Repository Checkpoint Stability, Finality, and Immutability v1.04

v1.04 is a deterministic, read-only certification layer over a confirmed v1.03 checkpoint creation receipt and delayed independent repository observations.

It verifies that the exact local checkpoint reference remains present, direct, non-symbolic, unchanged, uniquely named, and backed by the expected commit object after a bounded stability interval.

It does not create, overwrite, rename, revoke, retain, delete, recover, branch, tag, push, sign, or otherwise mutate a repository.

## Verification boundary

The verifier requires:

- complete recomputation of the supplied v1.03 receipt from its original inputs;
- a delayed direct reference-store observation of the same repository, transaction, checkpoint name, and OID;
- independent object-database evidence for the exact checkpoint commit;
- a checkpoint-name registry snapshot proving uniqueness without granting name allocation authority;
- an immutable-by-default policy with force update, overwrite, rename, revocation, deletion, remote update, push, and signing disabled;
- bounded evidence age, a minimum stability interval, monotone observation order, and no future evidence.

A missing checkpoint, substituted OID, duplicate name, missing object, stale observation, symbolic reference, or forbidden effect yields a rejected failure receipt. Rejection does not trigger retry, overwrite, rollback, recovery, or deletion.

## Validation

Focused:

```bash
python3 -m unittest -v tests.test_kuuos_repository_checkpoint_stability_finality_v1_04
```

Cumulative:

```bash
python3 runtime/kuuos_v104_check.py
```
