# CodeAI / MemoryOS Lean repair memory v0.1

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Scope and implementation

A new external-evidence layer for the existing Lean repair process. It preserves failures as well as successes; it is not model-weight training and does not grant proof, Git, WORLD-update, or merge authority. Existing Lean statements, assumptions, pins, public roots, parent #3522, child #3530 and protected #1558 are not modified by this feature.

The runtime directly calls the existing MemoryOS GitHub external memory API in `examples/memoryos_github_external_memory_minimal.py`: `GitHubExternalMemoryRecord`, `validate_record`, and `compile_context_candidate`. MemoryOS owns source pointers and read-only context; the separate CodeAI guard owns a decision not to repeat an exact known failed candidate.

The existing `runtime/kuuos_codeai_version_bound_repair_memory_v0_1.py` remains unchanged. Its stronger independent-verification preconditions are NOT fabricated for unverified compiler observations. This new intake retains those observations below the certification boundary.

## Ordered execution

1. Read and validate MemoryOS records before candidate generation. Corrupt/missing history is an explicit obstruction, not an empty history.
2. Supply scoped lessons to `candidates_with_memory(advice)` when the producer implements it. Static existing portfolios retain their generator and receive exact-replay filtering; they are not falsely described as learning model weights.
3. Compare proposed candidate bytes against prior failures. Only fully identical repository, source HEAD/tree, target, Lean, mathlib, manifest, runner, imports, declaration-signature fingerprint, compiler flags, and candidate blob qualify for suppression.
4. Compile remaining candidates with fixed direct Lean. Only direct-green candidates enter the existing real Lean MCP stage.
5. Independently certify the same promoted bytes through the existing separate CI. Memory never substitutes for this stage.
6. Capture all full candidate logs and create immutable observations, including failures, resource limits and NO_DATA. Import the resulting records into the repository through GitHub MCP after checking source/run identity.

Entry point, from the exact parent-PR isolated runner where the existing generator is valid:

```sh
PYTHONPATH=. python3 -m scripts.kuuos_codeai_memoryos_lean_v0_1 \
  --generator scripts.kuuos_v1106_codeai_label_table_round2_v1 \
  --history memoryos/lean_repairs/v0_1 \
  --output /tmp/kuuos-memoryos-lean-run
```

The inherited runner still requires its actual #3522 pull-request event. This adapter does not spoof that event or broaden execution permissions. A new candidate generator can expose `candidates_with_memory(advice) -> dict[str, str]` to consume remembered causes before building sources. Existing scripts are not rewritten or silently switched by installing this additive PR.

An exact-repeat independent replication is possible only with a recorded `--retry-reason`. An all-blocked portfolio returns `REGENERATE_REQUIRED`, not success. The adapter also returns a nonzero status if the old experiment script returned zero but no actual direct-Lean/MCP success was observed.

## Memory records

Each content-addressed record contains the full diagnostic, compressed losslessly, its hash, candidate Git blob, compiler exit/olean observations, exact available context, workflow/job/artifact pointers, inferred error families, explicit causal uncertainty and optional earlier observation IDs. The raw goal remains available through `diagnostic(record)`. Missing import/signature/environment evidence remains null. Hashes ensure integrity, not external authenticity.

An immutable seed bundle contains nine actual candidate observations from:

- run 43687692238: three v1.105 dependent-index failures;
- run 43687986358: three v1.105 direct-Lean successes;
- run 43689373291: three v1.106 finite-label failures.

The downloaded archive hashes were checked against GitHub artifact metadata. The successful `Nat.le_refl 4` repair is linked to the three earlier failures and the exact source generator blob `d76af7743d6cd133664d8eb3c8af567a9b0e2b25`. This supports a scoped repair lesson, not a universal ban on `decide`. These older archives lack full environment/import/signature evidence and therefore remain advisory-only, even when a compiler success is observed.

## Conflict, persistence and authority

Opposed success/failure observations are both retained as `CONFLICT_REVERIFY`. A corrected explanation adds a new linked record; it never overwrites a failed attempt. Changing a HEAD, signature, pin or dependency returns the case to re-verification. A success memory always yields `REVERIFY_NOT_CERTIFIED` for a candidate; it cannot certify a new source.

Repository seed/JSON files provide durable versioned storage. Run-local observations and GitHub Actions artifacts are NOT automatically durable repository admission. The workflow uses read-only GitHub permissions and never commits records itself. On a later session, read this PR's immutable journal and import new observations through GitHub MCP with expected-HEAD checks; preserve provenance and failed runs.

Untrusted diagnostic text is data, not instructions. Nothing in a memory record is evaluated, executed, or used to change runtime permissions. The memory layer cannot relax compiler flags, add axioms, suppress an independent CI failure, discharge a mathematical obstruction, or merge the parent PR.

## Verification

Run `python3 -m unittest discover -s tests -p 'test_codeai_memoryos_lean*.py' -v`.

Tests cover exact failures, new contexts, corrupt records, NO_DATA, timeouts, conflicting evidence, typed stage status, append-only publication, source/log digests, prompt-like text as data, full-goal preservation and the actual adapter protocol. Test doubles exercise wiring only; they are not Lean/MCP proof certificates. The new CI is Python-only because no Lean source is changed. The original fixed-Lean -> real MCP -> independent CI order remains necessary for every mathematical repair.
