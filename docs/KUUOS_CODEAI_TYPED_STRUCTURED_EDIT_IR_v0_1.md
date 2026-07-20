# CodeAI Typed Structured Edit IR v0.1

## Status

Additive, read-only, deterministic typed-edit normalization stage after the
Selective Repository Semantic Context Pack.

The stage converts one sealed typed-edit proposal into a content-addressed
intermediate representation whose existing-file edits are symbol-anchored and
whose source preconditions are exact.

It does not generate a patch, apply an edit, invoke a provider, run a verifier,
mutate a repository, perform a Git effect, select a candidate, or grant execution
authority.

```text
exact semantic context pack and receipt
+ exact repository snapshot
+ sealed typed-edit proposal
+ deny-by-default typed-edit policy
  -> context-lineage verification
  -> language and path verification
  -> symbol localization
  -> exact file, anchor-digest, and line preconditions
  -> normalized deterministic application order
  -> sealed typed structured edit IR and receipt
  -> no whole-file modification contract
  -> no repository, provider, runner, or Git effect
```

## Why this stage exists

The original autonomous structured-edit synthesis contract uses three broad edit
operations:

- add;
- modify;
- delete.

For a modification, it requires complete replacement content for the file. That
contract is deterministic and produces a valid unified diff, but it leaves the
provider responsible for reproducing every unchanged line correctly. A small
intended change can therefore accidentally:

- remove unrelated declarations;
- restore an obsolete implementation from prompt context;
- duplicate imports;
- change formatting outside the intended symbol;
- overwrite a concurrent repository change;
- target a symbol that was only guessed from prose;
- pass a small test while silently damaging another surface.

The typed IR does not claim to solve semantic correctness. It narrows the edit
surface before later application and verification.

```text
whole-file replacement
  -> symbol-anchored operation
  -> exact source precondition
  -> deterministic normalized IR
```

## Position in the CodeAI pipeline

```text
Intent Repository Observation
  -> Selective Repository Semantic Context Pack
  -> Typed Structured Edit IR
  -> Candidate Static Admissibility Preflight
  -> Evidence-Bearing Candidate Portfolio
  -> Isolated Application and Verification
  -> Bounded Repair
```

The v0.1 stage is separately invoked. Existing synthesis is not silently rewired.
A later integration stage can require provider output to satisfy this IR contract.

## Inputs

### Context pack

The context pack must be a sealed successful
`CodeAI Selective Repository Semantic Context Pack v0.1` result.

The typed IR stage requires:

- `selective_repository_semantic_context_pack_built`;
- `context_only` operating mode;
- at least one selected entry;
- an exact pack digest;
- exact repository, source-commit, and snapshot identity;
- read-only repository handling;
- no provider, repository, Git, selection-authority, or execution-authority effect.

An abstention pack is not silently upgraded into edit context.

### Context receipt

The matching context receipt must:

- have a valid digest;
- name the exact context-pack digest;
- preserve the same repository, commit, and snapshot identity;
- preserve the exact selected-path order;
- report read-only operation and no effects or authority.

### Repository snapshot

The repository snapshot is the exact canonical mapping used by the context stage:

```text
repository path -> complete UTF-8 text content
```

The proposal, pack, receipt, and actual mapping must carry the same canonical
snapshot digest.

The stage reads this mapping only to validate symbol locations and preconditions.
It does not write a modified mapping.

### Typed-edit proposal

A proposal contains:

- proposal identity and revision;
- exact context-pack and context-receipt digests;
- exact repository snapshot digest and source commit;
- selected supporting-context paths;
- one or more typed operations;
- requirement, test-plan, and risk trace identifiers;
- unresolved questions;
- prior IR digests;
- creation epoch;
- an explicit authority-claim flag;
- one canonical proposal digest.

Unresolved questions or an authority claim block normalization.

### Typed-edit policy

The sealed policy fixes:

- expected repository and source commit;
- allowed and forbidden path prefixes;
- allowed operation and language sets;
- operation-count and new-text budgets;
- supporting-context-path budget;
- maximum anchor span;
- trace-list budgets;
- request-age bound;
- whether creation and symbol deletion are permitted;
- whether existing-file targets must be selected context paths;
- all effect and authority flags.

The following policy flags must remain false:

- repository mutation;
- provider invocation;
- verification-runner invocation;
- candidate-selection authority;
- execution authority.

## Typed operations

### `create_file`

Creates candidate material for a path that is absent from the exact repository
snapshot.

Required precondition:

```text
precondition_kind = path_absent
```

Required shape:

- empty anchor kind and symbol;
- empty expected file and anchor digests;
- zero expected start and end lines;
- nonempty canonical new text;
- path suffix and declared language agree.

The IR records candidate creation material. It does not create the file.

### `replace_symbol`

Replaces exactly one resolved top-level symbol span.

Required precondition:

```text
precondition_kind = symbol_exact
```

The proposal must match:

- selected context path;
- exact current file digest;
- exact symbol kind;
- exact symbol name;
- exact anchor digest;
- exact start line;
- exact end line.

### `insert_before_symbol`

Inserts new text immediately before an exact symbol span.

The symbol precondition is identical to `replace_symbol`. The normalized
application interval is empty and begins at the anchor start line.

### `insert_after_symbol`

Inserts new text immediately after an exact symbol span.

The symbol precondition is identical to `replace_symbol`. The normalized
application interval is empty and begins after the anchor end line.

### `delete_symbol`

Deletes exactly one symbol span.

Deletion must be enabled by policy and `new_text` must be empty.

## Language profiles

### Python

Python files are parsed with the standard-library AST.

The v0.1 locator recognizes top-level:

- functions;
- asynchronous functions;
- classes;
- simple and annotated assignments.

For functions and classes, decorators are included in the exact anchor span.

Nested declarations are not implicit edit targets in v0.1.

### Lean

Lean files are scanned deterministically for named top-level:

- `def`;
- `theorem`;
- `lemma`;
- `structure`;
- `inductive`;
- `abbrev`;
- `class`;
- `instance`.

The anchor begins at the declaration line and ends before the next recognized
top-level declaration, with trailing blank lines removed.

This lexical profile is deliberately bounded. It is not a complete Lean parser or
a proof of declaration ownership.

## Preconditions

Every existing-file edit requires all of the following to agree:

```text
selected context path
+ repository path
+ inferred language
+ exact file SHA-256
+ exact symbol kind
+ exact symbol name
+ exact anchor SHA-256
+ exact start line
+ exact end line
```

A mismatch blocks the entire IR. The stage does not partially normalize sibling
operations after a failed precondition.

```text
precondition match != semantic correctness
precondition mismatch != automatic repair instruction
```

## Collision and ordering rules

The stage rejects:

- duplicate operation identifiers;
- duplicate file-creation paths;
- multiple operations targeting the same path, symbol kind, and symbol name;
- unsupported or forbidden paths;
- unsupported languages or operations;
- over-budget text or traces.

Normalized operations are ordered deterministically by:

1. path;
2. reverse application start line;
3. operation identifier.

Reverse line order supports a later in-memory application stage without allowing
earlier line edits to shift later symbol locations.

The v0.1 stage records this order but does not apply it.

## Output IR

A successful IR records:

- exact context pack and receipt lineage;
- exact repository, commit, and snapshot lineage;
- exact proposal and policy digests;
- supporting context paths;
- deterministic operation order;
- resolved symbol spans;
- exact source and anchor digests;
- new-text digests and byte counts;
- requirement, test, and risk traces;
- fixed no-effect and no-authority boundaries;
- one canonical IR digest.

The full proposed `new_text` remains candidate material. It is not accepted as
correct code.

## Route receipt

The receipt records:

- exact input and IR digests;
- operation identifiers and target paths;
- operation and byte counts;
- successful context-lineage and precondition verification;
- prohibition of whole-file modification;
- no provider or runner invocation;
- no repository or Git effect;
- no candidate selection or execution authority;
- no correctness-proof claim.

## Blocked conditions

The route blocks for:

- malformed mappings or extra/missing fields;
- digest mismatch;
- unsupported profile state;
- context abstention;
- repository, commit, snapshot, pack, or receipt drift;
- selected-path drift;
- stale or future proposal;
- authority claim;
- unresolved edit questions;
- policy-enabled effects or authority;
- missing supporting context;
- unselected existing-file target;
- duplicate operation identifiers or targets;
- invalid canonical paths or text;
- forbidden path;
- unsupported operation or language;
- file or anchor precondition mismatch;
- missing or ambiguous symbol;
- parse failure;
- excessive anchor span;
- create-file path already present;
- malformed create-file absence precondition;
- disabled creation or deletion;
- nonempty deletion text;
- per-operation or total text-budget excess;
- operation-count or trace-budget excess.

Blocked results contain no IR and no receipt.

## Determinism

For fixed context pack, receipt, repository mapping, proposal, and policy:

- validation order is deterministic;
- symbol resolution is deterministic;
- operation ordering is deterministic;
- IR and receipt digests are deterministic.

Determinism does not establish that the requested edit is useful or correct.

## Fixed boundaries

```text
typed edit IR != patch
typed edit IR != applied edit
typed edit IR != repository truth
typed operation != selected candidate
symbol name != ownership
symbol match != semantic correctness
file digest match != concurrency lease
anchor digest match != proof
line match != proof
create-file operation != file creation
delete-symbol operation != deletion authority
normalized application order != execution
whole-file modification prohibited != semantic safety proof
IR receipt != provider authority
IR receipt != verification authority
IR receipt != execution authority
IR receipt != Git authority
```

## Machine-readable artifacts

- runtime:
  `runtime/kuuos_codeai_typed_structured_edit_ir_v0_1.py`
- checker:
  `scripts/check_codeai_typed_structured_edit_ir_v0_1.py`
- tests:
  `tests/test_kuuos_codeai_typed_structured_edit_ir_v0_1.py`
- example:
  `examples/codeai_typed_structured_edit_ir_v0_1.json`
- manifest:
  `manifests/kuuos_codeai_typed_structured_edit_ir_v0_1.json`
- formal kernel:
  `formal/KUOS/CodeAI/TypedStructuredEditIRV0_1.lean`
- formal root:
  `formal/KuuOSCodeAITypedStructuredEditIRV0_1.lean`
- workflow:
  `.github/workflows/codeai-typed-structured-edit-ir-v0-1.yml`

## Planned successor

The next planned unit is **CodeAI Candidate Static Admissibility Preflight
v0.1**.

It should consume exact typed-IR lineage and perform bounded, effect-free checks
such as:

- operation collision analysis;
- in-memory materialization;
- parser and type-oriented preflight;
- forbidden import and dependency checks;
- changed-symbol and changed-path accounting;
- test-plan correspondence;
- deterministic rejection or abstention before provider-independent verification.

That successor must preserve the distinction:

```text
static admissibility != correctness
```
