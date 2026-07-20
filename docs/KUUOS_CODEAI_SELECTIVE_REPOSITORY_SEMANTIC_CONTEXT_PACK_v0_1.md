# CodeAI Selective Repository Semantic Context Pack v0.1

## Status

Additive, read-only, deterministic context-selection stage after the governed
CodeAI intent and repository observation envelope.

The stage converts one exact repository snapshot into a bounded semantic context
pack for later code-generation stages. It does not generate a patch, invoke a
provider, execute a verification command, mutate the repository, or grant
candidate-selection or execution authority.

```text
supported intent/repository observation receipt
+ exact path-bounded repository snapshot
+ sealed semantic-context request
+ deny-by-default context policy
  -> deterministic language-aware analysis
  -> relevance scoring and bounded selection
  -> line-numbered semantic excerpts
  -> content-addressed context pack and receipt
  -> no full-repository forwarding
  -> no provider, runner, repository, or Git effect
```

## Why this stage exists

The existing structured-edit synthesis surface receives the repository snapshot as a
whole and places all files into the provider prompt. That preserves exact source
material, but it also permits irrelevant files to consume the context window and to
introduce misleading names, APIs, tests, and old implementation patterns.

Repository-level code-generation literature supports a more selective design:

- **RepoCoder** motivates iterative repository retrieval rather than file-local
  completion alone.
- **Repoformer** shows that retrieval should be selective because unnecessary
  context can reduce generation quality.
- **AutoCodeRover** motivates program-structure and fault-localization signals rather
  than treating the repository as an undifferentiated text corpus.
- **Agentless** supports a strong deterministic localization → repair → validation
  pipeline before adding more agent complexity.
- **LeanDojo** and premise-selection work motivate bounded declaration and import
  retrieval for formal code instead of unconstrained theorem-name guessing.

These papers are design evidence, not authority. KuuOS records the exact local
selection policy and evaluates later generation results against the baseline replay
metrics introduced in the preceding stage.

## Position in the CodeAI pipeline

```text
Intent Repository Observation
  -> Selective Repository Semantic Context Pack
  -> Autonomous Structured Edit Synthesis
  -> Unified Diff Candidates
  -> Candidate Portfolio and Isolated Application
  -> Verification and Bounded Repair
```

The v0.1 stage is separately invoked. It creates a governed input that a later
synthesis-wiring stage can use instead of forwarding the complete repository
snapshot to a provider.

## Inputs

### Source observation receipt

The source receipt must be a sealed successful receipt from the CodeAI intent and
repository observation stage. The context stage requires:

- `intent_repository_observation_supported`;
- `read_only` operating mode;
- exact repository and source commit identity;
- an exact tree digest;
- no reported repository mutation.

The receipt digest is checked again and bound into both the context pack and the
route receipt.

### Repository snapshot

The repository snapshot is a canonical mapping:

```text
repository path -> complete UTF-8 text content
```

The request carries its exact canonical digest. Any path, content, or ordering drift
changes the digest and blocks the stage.

The snapshot is input evidence, not repository truth. The stage does not read the
live repository or network.

### Context request

The sealed request contains:

- intent text;
- nonempty query terms;
- optional target path prefixes;
- optional target symbols;
- test-plan identifiers;
- desired semantic roles;
- exact repository snapshot digest;
- exact source observation receipt digest;
- unresolved context questions;
- prior pack digests;
- a bounded creation epoch.

Target path prefixes define permitted search scope. They do not make every file
under the prefix relevant by themselves.

### Context policy

The deny-by-default policy fixes:

- expected repository and source commit;
- allowed and forbidden repository path prefixes;
- supported suffixes;
- maximum repository, file, candidate, selected-file, excerpt, symbol, import, and
  total-context budgets;
- maximum query-term count and request age;
- whether bounded text fallback is permitted;
- whether an empty result may produce an abstention pack;
- all effect and authority flags, which must remain false.

## Semantic analysis

### Python

Python files are parsed with the standard-library AST. The pack records bounded:

- imported modules;
- top-level functions;
- asynchronous functions;
- classes;
- simple top-level assigned names.

A syntax failure either blocks or routes to bounded text fallback according to the
sealed policy. The parse error type is retained without forwarding an unbounded raw
trace.

### Lean

Lean files are scanned deterministically for:

- `import` declarations;
- `def`;
- `theorem`;
- `lemma`;
- `structure`;
- `inductive`;
- `abbrev`;
- `class`;
- `instance`.

This is a bounded lexical semantic profile, not a replacement for Lean elaboration,
`#check`, premise retrieval, or strict compilation. Those remain later verification
operations.

### JSON and TOML

JSON and TOML inputs are parsed and expose bounded top-level keys as semantic
symbols. Invalid syntax follows the same fail-closed or bounded-fallback policy.

### Text, Markdown, YAML, and other allowed text

Text profiles use bounded heading extraction and line matching. YAML is not treated
as fully parsed semantics in v0.1 and is marked as fallback material.

## Relevance scoring

A file becomes a relevant candidate only when it has a semantic match from at least
one of:

- a query term in the path;
- a query term in declared symbols;
- a query term in imports;
- a query term in content;
- an exact requested target symbol.

After relevance is established, requested role and test-plan support can raise its
score. A target path prefix limits and annotates search scope but does not by itself
select every file.

The stable ordering is:

```text
higher score first
then canonical repository path
```

No model performs the ranking.

## Bounded excerpts

For each selected file, the pack records:

- canonical path;
- SHA-256 content digest;
- language;
- semantic role;
- score and explicit selection reasons;
- parse status and bounded parse error type;
- bounded imports;
- bounded declared symbols;
- bounded line-numbered excerpts.

Matching lines receive one adjacent line of context on each side. If no individual
line was matched but the file is otherwise relevant, a small initial window is used.
The policy caps both per-file excerpt bytes and total context bytes.

Complete file contents are not copied into the pack.

## Roles

The deterministic role classifier distinguishes:

- `source`;
- `test`;
- `formal`;
- `config`;
- `workflow`;
- `documentation`.

Role classification is a retrieval feature, not an ownership or authority claim.

## Empty selection and abstention

When no relevant file is found, the policy chooses one of two outcomes:

```text
allow_empty_context_abstention = true
  -> ready abstention pack with zero selected files

allow_empty_context_abstention = false
  -> blocked with no pack or receipt
```

This prevents the system from filling the context window with unrelated files merely
because a generation step expects some input.

## Oversized and omitted files

Eligible files that exceed the per-file byte budget are not forwarded. Their paths
are recorded as oversized eligible paths.

Relevant files may also be omitted because of selected-file or total-context
budgets. The pack records the omitted relevant-file count. Omission is visible and
is not converted into evidence completeness.

## Determinism and content addressing

For fixed source receipt, repository snapshot, request, and policy, semantic
analysis, scores, ordering, excerpts, pack, and receipt are deterministic.

The stage seals:

- request;
- policy;
- repository snapshot digest;
- every selected file content digest;
- complete context pack;
- route receipt.

```text
deterministic selection != complete context
deterministic excerpt != semantic truth
content digest != correctness proof
```

## Failure behavior

The stage blocks before emitting a pack or receipt for:

- malformed, missing, or extra schema fields;
- digest mismatch;
- unsupported or non-read-only source receipt;
- repository or source-commit mismatch;
- repository snapshot drift;
- stale or future request;
- query, repository, file, candidate, excerpt, or context budget violation;
- invalid or escaping paths;
- forbidden target scope;
- duplicate query material;
- relevant semantic parse failure when fallback is disabled;
- any policy that enables mutation, network, secret, candidate-selection, or
  execution authority;
- no relevant context when abstention is disabled.

Blocked results contain no context pack and no route receipt.

## Outputs

A successful invocation returns:

1. a sealed selective semantic context pack;
2. a sealed read-only route receipt.

The receipt records selected paths and exact source digests while preserving:

- no provider invocation;
- no verification-runner invocation;
- no repository mutation;
- no Git effect;
- no network or secret access;
- no candidate selection;
- no execution, merge, deployment, or successor authority.

## Fixed boundaries

```text
context pack != repository truth
semantic match != correctness proof
context selection != candidate selection
path scope != relevance
role classification != ownership
text fallback != parsed semantics
empty abstention != failure to govern
context pack emission != provider invocation
context pack emission != repository mutation
context receipt != execution authority
context receipt != Git authority
```

## Evaluation connection

The preceding Generated Patch Error Baseline Replay Evaluation v0.1 records stage
pass rates, first failures, repair cost, provider cost, and repeated error
fingerprints. Later integration should compare at least:

- unknown-symbol rate;
- import-error rate;
- typecheck pass rate;
- targeted-test pass rate;
- provider calls per verified patch;
- generated bytes per verified patch;
- no-admissible-candidate or abstention frequency.

The context pack should be retained only if those measurements improve without
weakening governance boundaries.

## Planned successor

The next planned stage is **Typed Structured Edit IR v0.1**. It should consume exact
context-pack lineage and replace unrestricted whole-file modification with
symbol-anchored, preconditioned edit operations.

A later synthesis-wiring stage should ensure:

```text
provider-visible repository context = exact governed context pack
full repository snapshot = downstream patch-construction witness only
```

## Machine-readable artifacts

- runtime: `runtime/kuuos_codeai_selective_repository_semantic_context_pack_v0_1.py`
- checker: `scripts/check_codeai_selective_repository_semantic_context_pack_v0_1.py`
- tests: `tests/test_kuuos_codeai_selective_repository_semantic_context_pack_v0_1.py`
- example: `examples/codeai_selective_repository_semantic_context_pack_v0_1.json`
- manifest: `manifests/kuuos_codeai_selective_repository_semantic_context_pack_v0_1.json`
- formal kernel: `formal/KUOS/CodeAI/SelectiveRepositorySemanticContextPackV0_1.lean`
- formal root: `formal/KuuOSCodeAISelectiveRepositorySemanticContextPackV0_1.lean`
