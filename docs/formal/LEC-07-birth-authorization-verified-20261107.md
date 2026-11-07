# Living Engi Cycle LEC-07 — Birth, authorization, and effect receipt separation (verified)

**Date:** 2026-11-07 JST  
**Canonical repository:** `itakura-hidetoshi/KuuOS`  
**Theorem PR:** [#3250](https://github.com/itakura-hidetoshi/KuuOS/pull/3250) — MERGED  
**Exact-source CI:** [#42348497450](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42348497450) — SUCCESS  
**Verified final source HEAD:** `6f8d4d5c831264f20e3f8bdd74377b6be86defe9`  
**Test-merge SHA:** `28d164d9f8c413005808ce989df26ff1e781b13f`  
**Source/test-merge Git tree:** `8ecac9fb37da15911cf6d7c330980f652997fa75` (exact equality)  
**Merged main SHA:** `359bb1c59ff0c137e71979fa57e1a55b5143983d`  
**Lean file:** [`formal/Kuu/LivingEngi/BirthAuthorization.lean`](../../formal/Kuu/LivingEngi/BirthAuthorization.lean) (279 lines; 12 theorems, 12 explicit `#print axioms`)  
**Public root:** `KuuOSFormal`, existing root 107 unchanged

## 1. Mathematical object, not metaphysical claim

The source imports only [LEC-06 `ConditionedBhava.lean`](../../formal/Kuu/LivingEngi/ConditionedBhava.lean). Its `ConventionalBhava` retains exact dependent local source sections, their certified conventional readout, the entire prior snapshot history, and a caller-supplied candidate-generating kernel.

LEC-07 proves that four distinct objects must **not** be identified:

```text
certified ConventionalBhava
    └── kernel + source history + input → BirthPacket (generated candidate + exact equality)
                                            ↓ not automatic
          caller Governance proof AND separate typed external receipt
                                            ↓
                            LicensedRequest (not an effect)
                                            ↓ not automatic
                        caller supplied EffectReceipt
                                            ↓
                             EffectRecord (evidence only)
```

This represents the **有 → 生** boundary as a *candidate construction*, not an execution. Creating a candidate does not manufacture a valid external receipt, an ActOS effect, or a truth claim about an exact WORLD.

## 2. Proven API and exact statements

- `BirthPacket b input` is indexed by the **complete** originating Bhava `b` and exact `input`; its `sourceEq` witness proves `candidate = birthCandidate b input`.
- `ActionBoundary` is caller-supplied and stores two independent families, both indexed by the entire Bhava, input, declared scope and candidate:
  - `governance : … → Prop`
  - `externalReceipt : … → Type`
- `LicensedRequest` contains a `BirthPacket`, the exact governance proof and the *separate* external receipt.
- `licensedRequest_exists_iff` proves:
  ```text
  Nonempty (LicensedRequest B b input scope)
      ↔ B.governance b input scope (birthCandidate b input)
        ∧ Nonempty (B.externalReceipt b input scope (birthCandidate b input)).
  ```
- `no_request_of_governance_denied` and `no_request_of_external_refutation` derive nonexistence from an *actual negative proof*. Failure to supply a certificate does **not** prove mathematical nonexistence.
- `licensedRequest_preserves_source_support` retains the original certified Bhava local-global support.
- `birth_exists_but_unlicensed` constructs a counterexample: the generated birth always exists, but with an impossible `Empty` external receipt **no** licensed request can be built.
- `EffectRecord` requires a distinct `EffectReceipt` indexed by the request. `no_effect_without_effect_receipt` shows even a request alone does not prove an effect.
- `freshOnlyBoundary` is a **deliberately narrow mathematical example** of a receipt valid only while `b.history = []`.
  - `freshly_begun_bhava_has_fresh_license` constructs a valid **mathematical** fresh-only license on an initialized Bhava.
  - `revision_invalidates_fresh_only_license` proves this particular receipt type is empty after any `reviseBhava`, because the complete old snapshot is appended to history. It does **not** claim that no other/new permission could be issued.

Neither governance proof nor external witness is automatically derived from a born candidate. The caller-supplied external witness has no self-validating institutional or cryptographic semantics until independently instantiated.

## 3. Exact-source CI and error repair

Initial source SHA `89284c9c6f8c489197b5da039894f4b067e325ed` failed [run #42348204461](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42348204461). The entire new 279-line Lean file, its imported dependent signatures, and the compiler log were inspected.

**Root cause:** using `matches` as a record field collided with Lean4 parser syntax. The first errors occurred at the structure field declaration and constructor; subsequent missing-field errors and "declaration uses sorry" were **elaboration consequences**, not intentional proofs by `sorry`. The only source correction was replacing that field consistently by `sourceEq` in the structure, constructor, projections and dependent proof rewrites. No theorem statement, assumption, external receipt condition or mathematical scope was weakened.

| Verification | Final result |
| --- | --- |
| Source HEAD / exact pinned Lean | `6f8d4d5c831264f20e3f8bdd74377b6be86defe9` |
| Strict Lean | **10,312 / 10,312 SUCCESS** |
| Changed module built | `Kuu.LivingEngi.BirthAuthorization` |
| Workflow consolidation integrity | **SUCCESS** |
| Independent Kuu core and public proof API | **SUCCESS** |
| Governance Gate and exact-head terminal | **SUCCESS** |
| Source / test-merge Git tree | **identical** |
| Twelve `#print axioms` | **standard `Quot.sound`, `propext`, `Classical.choice` only** |
| New `sorryAx` | **none** |
| Changed Lean warning/error | **0 / 0** |

Pinned Lean `v4.30.0-rc2`, mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`; existing `KuuOSFormal` roots 107 unchanged. Protected PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) remains Draft / Open / unmerged. Independent `Kuu` does not import legacy `KUOS`/Qi/Gray. All original F55/P77/GK5CG proof-relevant evidence and source definitions remain unchanged.

## 4. Living Engi Cycle interpretation

- **取 (upādāna):** an unchecked/refuted global promotion would evade scoped compatibility/coherence.
- **有 (bhava):** LEC-06 packages *only a certified conditional conventional WORLD model*, history and generation rule.
- **生 (jāti) candidate:** LEC-07 uses the existing generation kernel to construct an exact, source-indexed output candidate.
- **Act / external event:** a licensed request requires independent Governance + receipt; an effect record demands yet another witness. Neither is entailed by prior stages.
- **還滅 / repair:** revision preserves complete source/history and invalidates only permissions whose declared conditions cease to hold. Re-evaluation may lead to a newly scoped permission but never retroactively changes old evidence.

```text
Preference ⇏ Descent
Certified Bhava ⇏ Authorized action
Born candidate ⇏ Licensed request
Licensed request ⇏ Effect evidence
History revision ⇏ automatic license carryover
```

## 5. Next separated obligations

- **LEC-08:** non-Markov feedback and recoverability in a history-aware process, with explicit conditions for recurrence, observation and future-only updates. A declared history-dependent function is not an empirical non-Markov proof by itself.
- **LEC-09:** typed comparisons of actual original F55/P77/GK5CG source histories; neither a shared numeric quotient nor a licensed request supplies missing higher cells.
- **Further LEC-05 frontier:** untrivialized context-dependent higher transport, actual obstruction and higher stack effectivity; the current flat frame model does not prove these.

Related: [Living Engi Cycle research spec](../LIVING_ENGI_CYCLE_VEDANA_TANHA_UPADANA_BHAVA_v0_1.md) and [LEC-05/06 verified record](LEC-05-06-typed-transport-bhava-verified-20261107.md).

---

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0. This record is append-only and records exact mathematical scope rather than a new runtime authorization.
