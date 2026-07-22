# CodeAI Frozen Cohort Prediction-Pack and Execution-Shard Contract v0.1

This stage follows **Baseline-versus-CodeAI and Ablation Comparison v0.1**. It freezes the evidence-production contract without claiming that performance evidence already exists.

## Frozen comparison surface

- one shared 100-slot opaque holdout ledger;
- five cohorts: deterministic baseline, full CodeAI, and three one-feature ablations;
- authentic prediction generation under each cohort's own variant configuration;
- ten external-only shards of ten samples per cohort, fifty shards total;
- the prior non-gold CodeAI smoke prediction remains traceable but is excluded from performance evidence.

The reference contract is admitted but not execution-ready. Dataset materialization, authentic prediction packs, and ready shards are all false. No external or kernel execution authority is granted.

## Fixed predecessor

- main: `083ee7ef65d53bd1a8e231c73b82e4946dd1eaf7`
- comparison pack: `aee1ad7919af50124c79cb27b86fc8c6d9a54192237e963b62e1869d986fdf23`
- comparison receipt: `1629e68f87175bf0ce7393e652d58df6bd3611832db84995feb1566644fd2ce4`
- sample binding: `d3162c78a1552f22411b87c019271cfbc692ffa048a039067f4c83c65d42012c`
- holdout partition: `b88c73c43b0a14c23cdd58269ccba3c5437ffba3651c0f3dc2ceb7aa7ebcf2e6`
- comparison contract: `f99ae02bd48c51563060a7b0de6be53f9ea98278efe0e837ab73bdd77e4c7016`

## Integrity rules

Structural tampering invalidates admission. Semantic admission is forbidden by label-only relabeling, gold-derived packs, raw test names or logs, smoke promotion into performance evidence, incomplete or overlapping shard coverage, kernel execution, repository or Git authority, and correctness or performance claims.

Pending authentic packs are not protocol failure. They preserve contract admission while keeping execution readiness false.

## Next evidence-producing stage

Materialize the exact pinned holdout outside the kernel, generate 100 authentic predictions for each frozen variant, seal those five packs, transition the fifty shards to ready, and only then grant bounded external-harness execution authority.
