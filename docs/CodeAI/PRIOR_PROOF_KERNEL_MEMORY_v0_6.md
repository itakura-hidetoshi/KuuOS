# CodeAI v0.6 — three-generation immutable kernel memory and research admission

## Source and historical evidence

Additive successor to merged PR #3641, canonical starting HEAD
`38d9cc8a26aa47161b13c047eb57b47297126a5d`. The v0.4 (3 observations) and v0.5 (10 observations)
packets and implementation remain byte-for-byte unchanged.
Post-merge v0.5 replay 45538753353, full Governance 45538753300,
runtime 45538753321 and MemoryOS 45538753400 succeeded.

The v0.6 frontier consists of the eight previously unobserved,
explicitly recorded repository-local references (five LivingEngi, two Qi,
one F112). The original source HEAD is
`8afa360f0eee06a8bc648e2957c9e4b9b4af7117`, tree
`ee52f0a2805c012aae05fea0e20624f1e9ea00e3`.

[Run 45539451502](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45539451502)
completed SUCCESS: direct Lean, actual Lean MCP 0.30.0, and separate
runner independent observation, with 8408 dependency jobs and 16 local
contract tests. Jobs 138954083259 and 138956949097; actual archive IDs
14989101416 and 14989630413. Direct receipt digests agree exactly:
`a21faff25607d162cdf7bb4f900a5c733784e2dc3b7af077b0b3c2519463ccf1`.
MCP receipt digest:
`1e87bd3c24016437efe2b20536c5c49d8fc0c81bf6a29ea443f6ed0db3a4c070`.
Only standard reported axioms, no sorryAx or direct diagnostics.

[Run 45541463689](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45541463689)
reconstructed the v0.6 packet from actual archives, matched 21 current
source declarations and rejected six tampered receipt/packet cases.
The three immutable packet digests (canonical JSON, not Git blobs) are:

- v0.4: `bfcf9fde9a27fea2e1bad35c44cf46544ae92f42bf54bed7db3f267327b1d271`
- v0.5: `23336f58b6613514063df5f1aad4e433fd9f98a461b2fae4152fd296054620ac`
- v0.6: `d3d60f6b73cf837b63245fc952907de98a7e196c2990d41c9d3355be706c4257`

The formal/lean subtrees, Lake configuration and manifest, Lean
v4.30.0-rc2 and mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6
are unchanged. The three packets keep independent historical identities.

## Combined recall and original research gate

[Run 45541638422](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45541638422)
completed SUCCESS at `d90465c739dc535224f6d2a69c956c921d50828e`, tree
`1dd87bfb52573b190a5f8461d41fac944e6dec16`, job 138961311531.
Actual archived packet reproduction, 21/21 recall, 13 regression tests,
and 6/6 tamper rejections succeeded. Original CodeAI boundary replay:

`matched=7 provider_calls=1 candidate_count=0 duplicate_provider_calls=0
synthetic_scope_contract=true external_model=false`.

The provider callback deterministically returns HOLD. The actual source
retrieval and original CodeAI call path are exercised, but the review
and canonical scope label are explicitly synthetic test fixtures.
No external model, new mathematical theorem, proof adoption, semantic
novelty, execution, repository mutation or merge authority is certified.

The runtime exposes explicitly recorded unresolved references separately
from unobserved lexical hits: `Kuu.LivingEngi.glue_agrees`,
`KUOS.Architecture.WuxingCyclicPaths.rotation_injective` and external
`congrArg`. This is a bounded explicit-reference frontier, not the full
type/proof expression dependency closure. The next local frontier must
be selected by reobserving canonical source and exact packet identities.

## Integration admission (pending)

First registry registration requires full Governance including Strict
Lean. The dedicated same-repository PR and main push replay workflow
already exists and must reproduce the actual archives; expiry is HOLD,
not a positive certificate. Preserve certified runtime, tests, scripts,
packets and formal source bytes. No assumptions, pins or public roots
are changed. Merge only after exact-head full Governance, dedicated
replay and source/test-merge tree equality. Reobserve independent main
CI after integration before new frontier implementation.
