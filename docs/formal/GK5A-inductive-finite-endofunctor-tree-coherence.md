# F112-P94D3GK5A — Inductive finite endofunctor-tree chosen-inverse coherence

**Formal date:** 2026-11-01 JST  
**Theorem PR:** [#2897](https://github.com/itakura-hidetoshi/KuuOS/pull/2897) — MERGED  
**Theorem squash / canonical main at theorem merge:** `6a74bc9ea979cd524e37d2fb13b9486fd5583d69`  
**Final exact-source HEAD:** `c87edb4788dc07060372f9f5d6a97b1891d8a706`  
**GitHub test-merge commit:** `ccc48981a02a8ff233cf66db36ada860f33a4ca8`  
**Identical source and test-merge Git tree:** `c792db3e45f8aa05f8cd084af6e9a37e7f07c3ca`  
**Exact-source CI:** [#41304610405](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41304610405) — SUCCESS.

## Authoritative Lean4 source

[PolygonNativeC60AQFullPentagonPhysicalNativeGK5AFiniteEndofunctorTreeCoherence.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5AFiniteEndofunctorTreeCoherence.lean)

Pinned **Lean v4.30.0-rc2** and **mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`**. One append-only Lean file; existing `KuuOSFormal` public root count remains 107. The imported theorem layer is GK4BZ -> GK4BY -> GK4BX -> GK4BW -> GK4BV -> GK4BU -> GK4BT and the original GK4BM/GK4BP/GK4BQ full-subcategory/attained-AH constructions.

## Main result: ALL finite binary endofunctor trees

Let `T` be an arbitrary genuine Mathlib category, fixed for a single instance. A new **inductive finite presentation** `NativeGK5AFiniteTargetTree T` has three constructors:

- `unit`: the real identity target functor `𝟭 T`;
- `atom R`: a genuine endofunctor `R : T ⥤ T`;
- `paste left right`: the ordinary Mathlib composite of the two recursively evaluated endofunctors.

The definition `nativeGK5ATreeComposite t : T ⥤ T` evaluates this tree in Mathlib's real functor category. The new `nativeGK5AChosenInverse_treeIso` is a **genuinely constructed whole Mathlib NatIso** at every tree, recursively pasting via GK4BW's typed `nativeGK4BWChosenInverse_binaryPasting` (including real associators, whiskerings and equality transports). It is not an assumed higher comparison.

The central **structural induction** theorem is:

`nativeGK5AChosenInverse_treeIso_eq_direct`:

`Θ_recursive(t) = Θ_GK4BT(eval(t))` as an **equality of whole Mathlib NatIso**, for **every finite depth and tree shape**.

At `unit` and `atom` the proof is definitional. At `paste(left,right)`, use both induction hypotheses, the **actual GK4BW binaryPasting_ofTheta** theorem, and the already Lean-proved GK4BV two-stage composition coherence. No new assumption is introduced.

## Arbitrary genuine target-NatTrans modification

For any finite trees `left,right` and any genuine natural transformation

`ρ : eval(left) ⟶ eval(right)`,

the whole-NatTrans equation

`(C_ρ ▷ Q_T) ≫ Θ_tree(right).hom = Θ_tree(left).hom ≫ (Q_T ◁ A_ρ)`

is proved as `nativeGK5AChosenInverse_treeNat_square`. The proof transports GK4BU's genuine modification through the arbitrary-depth tree induction equality. There is no claim of definitional strictness of GK4BM's chosen inverse `Q_T`.

The entire tree-level three-factor associativity and arbitrary left/right unit insertion are also proved as whole NatIso equalities:

- `nativeGK5AChosenInverse_tree_assoc`;
- `nativeGK5AChosenInverse_tree_leftUnit`;
- `nativeGK5AChosenInverse_tree_rightUnit`.

## Finite words, presentation-independent comparison with exact transports

The finite list `List (T ⥤ T)` is evaluated by `nativeGK5AListComposite`; the empty list is `𝟭 T`. The full-functor **concatenation equation** `composite(xs ++ ys) = composite(xs) ⋙ composite(ys)` is proved by actual list induction. `nativeGK5ATreeLeaves t` flattens any binary tree, omitting inserted unit nodes. Theorems `nativeGK5ATreeComposite_eq_list`, `nativeGK5ATreeComposite_eq_of_leaves`, and `nativeGK5ATreeOfList_eval` prove that **equal ordered leaf lists imply equal evaluated whole functors**, regardless of finite bracket shape or inserted units.

**Crucially, we do not silently identify dependent NatIso types across only propositionally equal functors.** The general `nativeGK5AChosenInverse_eqTransport` explicitly uses `eqToIso (congrArg ... h)` on the *compatible* side and `eqToIso (congrArg ... h.symm)` on the *attained-AH* side. The theorem `nativeGK5AChosenInverse_sameLeaves_transport` combines these two transports with the tree induction and whole NatIso equation. In symbolic form, with `h: eval(left)=eval(right)`:

`eqToIso(C_h ⋙ Q_T) ≪≫ Θ_tree(right) ≪≫ eqToIso(Q_T ⋙ A_(h.symm)) = Θ_tree(left)`.

This is an exact whole NatIso equality with real type-correct boundary transports, not merely componentwise comparison or raw high-cell existence.

## Exact-source Strict Lean and axiom audit

- **Final source HEAD** `c87edb4788dc07060372f9f5d6a97b1891d8a706`, **test-merge** `ccc48981a02a8ff233cf66db36ada860f33a4ca8`, identical Git tree `c792db3e45f8aa05f8cd084af6e9a37e7f07c3ca`.
- [CI #41304610405](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41304610405): **Strict Lean 3822/3822 SUCCESS**, **Independent Kuu SUCCESS**, **Workflow integrity SUCCESS**, **Governance terminal SUCCESS**. Exact-head terminal completion receipt published.
- **16 public definitions/theorems and 16 `#print axioms`**, plus the new inductive tree constructor family. The actual CI logs show **only** `propext`, `Classical.choice`, `Quot.sound` (some declarations use none). **sorryAx 0**, changed Lean error/warning 0/0.
- **First CI failure:** the empty-list base case of the list-append proof was left unsolved because `simp [nativeGK5AListComposite]` did not close the whole-functor identity law. This introduced `sorryAx` in that failed proof and its dependents, so the initial CI was not accepted. The structural fix explicitly states the whole functor equation and closes it using the **pinned Mathlib `Functor.id_comp`** reversed. No theorem statement, assumption or definition was weakened. The entire changed Lean file, imported signatures, pinned Mathlib, exact source and axiom dependencies were rechecked, and final CI passed.

## Precise scope / authority / continuation

The result is universally quantified over all **finite binary trees of endofunctors of one fixed target category**. It does not yet formalize arbitrary multi-category dependent target chains of unbounded length; the earlier GK4BZ handles its separate finite five-stage case. The theorem does **not** establish unconditional faithfulness of the original F45 dependent source, original source-Q category laws, raw F54/F55/P92B Type-valued higher cells, all-integer-matrix reachability, a global Gray category or unrestricted higher hyperdescent. GK4BM's **chosen `Q_T`** remains distinct from GK4BP's **explicit `P_T`**, connected by the genuine GK4BQ `κ_T : Q_T ≅ P_T`. Strict 空 is central, independent Kuu remains one presentation, and protected validation-only PR #1558 remains Draft/OPEN/unmerged.

**Next candidate GK5B:** extract a proof-relevant normalization/path-independence principle for arbitrary finite target tree rewrites using actual Mathlib associators/unitors and typed natural transformations, or investigate dependent multi-category chains without assuming Q strictness. No raw new source higher cells may be inferred from the present finite endofunctor theorem. README/ROADMAP history is kept append-only via a separate docs-only PR with Strict Lean SKIPPED.
