# F112-P94D3GK4BW — Genuine chosen-inverse 3-stage coherence, 4-stage pentagon, target units and modification

2026-11-01 JST. **[Theorem PR #2889](https://github.com/itakura-hidetoshi/KuuOS/pull/2889) MERGED.** This append-only record explains the verified theorem; authoritative mathematical statements are the actual Lean source on canonical `main`, not this prose.

## Authoritative source and exact-source CI

- [Complete GK4BW Lean source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BWChosenInverseHigherTargetPentagonUnit.lean) — **473 source lines** (474 when counting terminal split), **25 new public declarations and 25 `#print axioms` checks**. Earlier Lean files and public imports are not modified.
- Final theorem source HEAD `0097f7a692d8f74a61367b148dd325ba03e54091`; test-merge commit `80a21116fac82f0b3c58bb809c205fb9ad36db98`. **Identical Git tree `13afe4f849a7b5024ac57d5f2a754351a71258cb`**. Test-merge parents: canonical base `92acc6866ec6dd0f9d7f2d9de9eb08e2e774078c` and exact source HEAD.
- [Exact-source CI #41297928591](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41297928591): **Strict Lean 3818/3818 SUCCESS**, Independent Kuu SUCCESS, workflow consolidation integrity SUCCESS, terminal Governance SUCCESS. Changed Lean warnings/errors 0/0; **25/25 public declarations use only `propext`, `Classical.choice`, `Quot.sound`, with `sorryAx` 0**.
- Theorem squash and canonical main HEAD after theorem merge: `91b2a9f9dd8287952defbf4657a76bbffc9d28bc`.

## Original mathematical objects remain authoritative

Original fully F45-dependent structural category `S`, **actually attained** old-AH observation category `A_att`, genuine AH-kernel-compatible full subcategory `Comp_T`, GK4BP explicit inverse `P_T`, GK4BM genuinely chosen inverse `Q_T`, and GK4BQ natural iso `κ_T:Q_T≅P_T` are unchanged.

GK4BT's entire Mathlib `NatIso Θ_R: C_R⋙Q_U≅Q_T⋙A_R` is the observed transport comparison. GK4BU proves target-NatTrans modification squares; GK4BV proves the WHOLE two-target composition equality `Θ²_(R,S)=Θ_(R⋙S)`, with equality transports and three real Mathlib `Functor.associator` components.

## GK4BW: actual three-target associative pastings

`nativeGK4BWChosenInverse_binaryPasting` takes **arbitrary whole correctly typed NatIso input witnesses** `α` and `β` and returns an actual two-target Mathlib NatIso. It preserves GK4BV's `eqToIso` endpoint transports and three associators, rather than presuming the two source functor categories are syntactically identical. With `α=Θ_R, β=Θ_S` it is definitionally the already-proven GK4BV two-target comparison.

For arbitrary composable `R:T⥤U`, `S:U⥤V`, `L:V⥤W`, GK4BW defines two distinct nested **actual NatIso values**:

- `nativeGK4BWChosenInverse_threeLeft`: first genuinely paste `(R,S)`, then `L`.
- `nativeGK4BWChosenInverse_threeRight`: first genuinely paste `(S,L)`, then `R`.

It proves BOTH equal `Θ_(R⋙S⋙L)` and therefore that they agree as **whole NatIso values** (`nativeGK4BWChosenInverse_threeAssociativity`). The associativity of the concrete target functors is mathlib's pinned `Functor.assoc` (definitional equality), not an unproved original raw higher cell.

## Four-stage pentagon — all five actual nested NatIso paths

For `R:T⥤U`, `S:U⥤V`, `L:V⥤W`, `M:W⥤X`, GK4BW separately constructs all five Catalan bracketings via the same real binary pasting operator:

| Declaration | Actual nested parenthesization |
| --- | --- |
| `nativeGK4BWChosenInverse_four_pathA` | `(((R⋙S)⋙L)⋙M)` |
| `nativeGK4BWChosenInverse_four_pathB` | `((R⋙(S⋙L))⋙M)` |
| `nativeGK4BWChosenInverse_four_pathC` | `((R⋙S)⋙(L⋙M))` |
| `nativeGK4BWChosenInverse_four_pathD` | `(R⋙((S⋙L)⋙M))` |
| `nativeGK4BWChosenInverse_four_pathE` | `(R⋙(S⋙(L⋙M)))` |

Each has its own Lean proof `four_pathA_eq_direct` through `four_pathE_eq_direct` showing equality to the ACTUAL `Θ_(R⋙S⋙L⋙M)`. **`nativeGK4BWChosenInverse_fourTarget_pentagon`** joins four consecutive equalities of these entire NatIso values. This verifies coherence of the actual chosen-inverse transport across the five 4-stage paths; it does **not** construct an independent Gray 3-cell.

## Unit and natural-transformation compatibility

- `nativeGK4BWChosenInverse_leftUnit` and `...rightUnit` prove actual two-target pasting with `𝟭 T` and `𝟭 U` equals the original `Θ_R`, using GK4BV and mathlib's actual `Functor.id_comp`/`Functor.comp_id`.
- `...threeFirstTarget_square`, `...threeMiddleTarget_square`, and `...threeLastTarget_square` prove whole typed GK4BU modification squares under genuine natural transformations of the first, second, and third target stages respectively.
- `nativeGK4BWTargetNat_threeHorizontal` forms a genuine whole NatTrans by two successive right whiskerings and a final left whiskering. `nativeGK4BWChosenInverse_threeHorizontal_square` proves one whole NatTrans square whose source comparison is **left bracketed** and target comparison **right bracketed**, so the natural transformation is compatible across the proven 3-stage associativity.

## Lean4 errors, fixes, and exact boundary

The initial proof exposed one remaining goal `Θ_((R⋙S)⋙L)=Θ_(R⋙(S⋙L))`. Explicit `rfl` with mathlib's pinned definitional `Functor.assoc` solves it after applying genuine GK4BV composition, rather than assuming arbitrary choice inverse is strictly functorial. Another error was a doc comment `/- ... -/` vs `/-- ... -/`: Lean does not attach declaration documentation to `section`. The pentagon's conjunction simplified to `True ∧ True ∧ True ∧ True`, which must be closed by `simp`, not by `rfl`.

There is **no** unconditional original-`S` faithfulness, source-Q category law, raw F54/F55/P92B `Type`-valued higher filler, unattained integer-matrix reachability, reconstructed global Gray category, or unrestricted higher hyperdescent.

Pinned Lean `v4.30.0-rc2`; pinned mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`. Public `KuuOSFormal` root 107; strict 空 center and independent Kuu one presentation. Protected validation-only PR #1558 remains Draft/OPEN/unmerged.

**Operational discipline:** append-only, tighten-only, overwrite-forbidden, same-root107. Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
