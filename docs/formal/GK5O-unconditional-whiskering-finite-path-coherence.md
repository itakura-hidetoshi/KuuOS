# F112-P94D3GK5O — Unconditional whole NatIso and NatTrans finite typed path coherence

**Date:** 2026-11-02 JST  
**Theorem PR:** [#2925](https://github.com/itakura-hidetoshi/KuuOS/pull/2925) — MERGED  
**Authoritative theorem squash/main at merge:** `dcbdf90631e60673c0156961b4e7ed90e430ad82`  
**Final exact-source HEAD:** `b0068afd2e19117413cbe1cea202b84e004ec9b4`  
**Independently matching source/squash Git tree:** `f01662fe10c98f3f3c795ef2cf4fea704cabea31`  
**Exact-source CI:** [#41374135005](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41374135005) — terminal SUCCESS (all selected jobs).

## New canonical Lean source

[PolygonNativeC60AQFullPentagonPhysicalNativeGK5OWhiskeringFullPathCoherence.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5OWhiskeringFullPathCoherence.lean)

This is one new append-only source file (247 lines). Its imports preserve the exact certified dependency chain GK5D → GK5G → GK5H → GK5J → GK5K → GK5L → GK5M → GK5N → GK5O, using actual pinned Mathlib category theory and true `Iso`/`NatTrans` objects. No previous source or public root is overwritten.

Fix real indexed Mathlib category families `C,D : I → Cat.{vC,uC}`, a genuine family of pointwise category equivalences `e : ∀ i, C i ≌ D i`, and actual dependently typed GK5D finite trees and paths. For each tree `t`, the actual whole comparison `Φ_t = nativeGK5GChangeTreeIso e t` remains a non-strict Mathlib `NatIso`; it is not silently identified with identity or treated as a chosen strict inverse.

## New proved mathematical results

### Genuine right contextual whiskering compatibility

The private `nativeGK5OWhiskerRight_of_square` proves that, for every basic rewrite `s:a⇒b` and all finite typed right subtrees `c`, a whole NatIso square for `s` implies the same square for `whiskerRight(s,c)`. It uses:

- The **actual child** GK5H step square, not an assumed global path condition.
- Mathlib `Functor.isoWhiskerLeft_trans_isoWhiskerRight` for the genuine interchange between `β` and `Φ_c`.
- Certified GK5L `nativeGK5LChangeCompIso_left` for the true non-strict middle equivalence compositor, not cancellation by definitional equality.
- True `Functor.isoWhiskerRight_trans` and `Iso.trans_assoc` laws.

### Genuine left contextual whiskering compatibility

The private `nativeGK5OWhiskerLeft_of_square` proves the symmetric implication for every fixed finite typed left subtree `a` and every `s:b⇒c`. It pastes true Mathlib iso-whiskering interchange, `Functor.isoWhiskerLeft_trans`, and certified GK5K `nativeGK5KChangeCompIso_right`.

### Unconditional local generators, finite paths, NatTrans and endpoints

Five public declarations are certified:

1. `nativeGK5OAllBasicSteps` — induction over all five actual GK5D constructors: arbitrary-subtree `assoc` (GK5M), `leftUnit` and `rightUnit` (GK5N), both `whiskerRight` and `whiskerLeft` (new GK5O). It proves the real GK5H whole **StepIso** compatibility square for each basic generator with no local/global compatibility premise.
2. `nativeGK5OStepCompatible` — `NativeGK5HStepCompatible e` is now unconditional for the specified genuine category families and equivalences.
3. `nativeGK5OAllFinitePaths` — via the already proven GK5H constructive local-to-global lemma, `NativeGK5HPathCompatible e` holds unconditionally for **every proof-relevant finite typed GK5D rewrite path**, including identity, reverse and transitive concatenations. This is a whole Mathlib `NatIso` equality, not a componentwise approximation.
4. `nativeGK5OAllFinitePaths_natTrans` — the `.hom` projections give the corresponding whole Mathlib `NatTrans` equation for every such path.
5. `nativeGK5OEndpointCompatible` — the GK5J canonical normalization-and-reversal endpoint criterion is unconditionally satisfied for all pairs of trees with equal ordered, dependently typed leaf words.

In Lean notation, for every genuine finite path `q:a⇒b`:

```lean
nativeGK5DPathIso (nativeGK5GChangePath e q) ≪≫
  nativeGK5GChangeTreeIso e b =
nativeGK5GChangeTreeIso e a ≪≫
  nativeGK5GChangeIso e (nativeGK5DPathIso q)
```

The statement quantifies over **finite** path syntax and one fixed universe pair. It does not assert global Gray reconstruction, arbitrary hyperdescent, an unconditional original F45 faithfulness theorem, source-Q category axioms, or raw original Type-valued F54/F55/P92B higher-cell identities.

## Lean4 elaboration diagnostics and corrected structural reasons

The developer checked the **entire new Lean source**, all imports and changed theorem signatures, the GK5G recursive tree comparison and the GK5H direct StepIso predicate, plus pinned upstream Mathlib's `Whiskering.lean`, `Iso.lean` and `Equivalence.lean`. Earlier exact-source CI failures of PR #2925 were corrected rather than weakening any theorem.

1. **`change` versus actual Mathlib equality.** Initial proofs tried to force the recursively expanded tree/paste path equation into an explicitly parenthesized whiskering equation by `change`. However `change` requires definitional equality. Mathlib's `Iso.trans_assoc` witnesses true associativity by an equality that is not necessarily Lean's definitional equality. The proof was refactored to the **direct GK5H StepIso square** (`NativeGK5OStepSquare`), avoiding the unnecessary length-one `PathIso` layer until using GK5H for final gluing.
2. **Right-associative `≪≫`.** Pinned Mathlib declares `infixr:80 " ≪≫ " => Iso.trans`. Incorrect bracketing of recursive `Φ` caused an elaboration mismatch. Actual `Functor.isoWhiskerRight_trans`, `Functor.isoWhiskerLeft_trans`, and `Iso.trans_assoc` were used to paste whole NatIsos while respecting that direction.
3. **True whiskering interchange under context.** A raw `rw` did not find `hinter` inside a larger composition. The proof now uses explicitly typed `congrArg` in the appropriate common-prefix or common-suffix context, without inventing filler cells.
4. **`simp made no progress` and remaining local-let equality.** At the end of recursive definitional reduction (`dsimp only`), certain intermediate `simp only` invocations did not close their goals, because the target still used locally bound abbreviations `α,β,Φ_a,Φ_b,Φ_c,T_c`. A diagnostic run printed both fully elaborated goals with `trace_state`. The final source removes these traces and closes three residual definitional equalities using terminal simplification followed by `all_goals rfl`; this combines the true associativity lemmas with Lean's definitional equality rather than treating `simp` as a proof of the residual equation. There is no `sorry`, `admit`, or new axiom.
5. **Tightened dependency boundary.** All five constructor cases use already certified exact-source GK5M/GK5N/GK5K/GK5L and the genuine Mathlib canonical operations. No theorem statements, equivalence assumptions, universes or historical imports were weakened.

Upstream pinned references: [Mathlib Whiskering.lean](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/Whiskering.lean), [Mathlib Iso.lean](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/Iso.lean); see also the [Lean4 tactic reference](https://lean-lang.org/doc/reference/latest/Tactic-Proofs/Tactic-Reference) for `simp`, `simpa`, and definitional simplification.

## CI and authority receipt

- **Exact-source HEAD:** `b0068afd2e19117413cbe1cea202b84e004ec9b4`.
- **Theorem squash/main at merge:** `dcbdf90631e60673c0156961b4e7ed90e430ad82`.
- **Independent source/squash tree:** `f01662fe10c98f3f3c795ef2cf4fea704cabea31` (equal).
- **[Exact-source CI #41374135005](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41374135005):** Strict Lean **3836/3836 SUCCESS**, Independent Kuu core **SUCCESS**, Workflow consolidation integrity **SUCCESS**, Governance gate and audit summary **SUCCESS**.
- **5/5 public `#print axioms` checks:** `propext`, `Classical.choice`, `Quot.sound` only. **`sorryAx` 0**. No new axioms, no Lean errors or warnings.
- Fixed Lean **v4.30.0-rc2**, pinned mathlib **5450b53e5ddc75d46418fabb605edbf36bd0beb6**, public **root107** unchanged, same-root/append-only/tighten-only/overwrite-forbidden. Strict 空 centered; independent Kuu remains one presentation. Protected Lean 4.31 validation-only **PR #1558 remains Draft/open/unmerged**.

## Exact scope and next research

GK5O closes the **whole NatIso/NatTrans path naturality obstruction for all finite GK5D rewrite paths** under genuine pointwise category equivalences. This is not a claim of unrelated higher-dimensional strict equivalence, a global Gray reconstruction, an unbounded hyperdescent theorem, or the original undecided source-F45/source-Q faithfulness/category axioms.

**Next GK5P (candidate):** Derive higher structural consequences of the now-unconditional finite-path naturality: naturality under compatible typed index relabelings, composition of pointwise category equivalences, and precise coherence for recursively assembled presentations, while retaining the same authority, type and fixed-universe boundaries. Do not add new claims until separately checked in pinned Lean.

Docs-only PR policy: **Strict Lean SKIPPED**; require its own independent Kuu, workflow integrity, governance and final main HEAD verification.
