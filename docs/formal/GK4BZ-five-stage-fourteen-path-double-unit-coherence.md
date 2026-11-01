# F112-P94D3GK4BZ — Five-target 14-path coherence and independent double-unit removal

**Formal theorem date:** 2026-11-01 JST  
**Theorem PR:** [#2895](https://github.com/itakura-hidetoshi/KuuOS/pull/2895) — MERGED  
**Theorem squash / canonical main at merge:** `4ac0281675db8ae00b92e0e71bbe21027ddd6afb`  
**Final source HEAD:** `cc92f709586bac91d03aa1d190832a354470639c`  
**GitHub test-merge commit:** `8bb1421585e6a0d48bee4b459e9d29121d86ec3e`  
**Identical source/test-merge Git tree:** `ed8de1cf7bb61632e2daf0b264887410f76ef6eb`  
**Exact-source CI:** [#41303246207](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41303246207) — SUCCESS.

## Authoritative Lean source

[PolygonNativeC60AQFullPentagonPhysicalNativeGK4BZFiveTargetTwoUnitCoherence.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BZFiveTargetTwoUnitCoherence.lean)

Lean v4.30.0-rc2, mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`. One append-only Lean file. The original F45-dependent structural source `S`, actual attained old-AH category `A_att`, genuine AH-kernel-compatible full subcategory `Comp_T`, GK4BM arbitrary chosen reverse `Q_T`, GK4BP explicit reverse `P_T`, and GK4BQ comparison `κ_T : Q_T ≅ P_T` remain unchanged. No definitional `Q_T = P_T` is claimed.

## Mathematically verified results (42 public declarations)

### 1. All fourteen *actual* five-stage Catalan pastings

For arbitrary five composable target functors `R:T⥤U`, `S:U⥤V`, `L:V⥤W`, `M:W⥤X`, `N:X⥤Y`, there are **14** binary parenthesizations (Catalan number `C_4 = 14`). GK4BZ constructs all fourteen **genuine Mathlib NatIso values** using GK4BW's typed `nativeGK4BWChosenInverse_binaryPasting`, prior genuine GK4BV two-stage comparisons, GK4BW three-/four-stage comparisons, and GK4BT's directly defined chosen-inverse `Θ`.

The four root splits contribute **5 + 2 + 2 + 5 = 14** distinct recursively pasted expressions. Each has a separately proved `_eq_direct` theorem, as an equality of **whole Mathlib NatIso**, to

`Θ_(R⋙S⋙L⋙M⋙N) : (C_(R⋙S⋙L⋙M⋙N) ⋙ Q_Y) ≅ (Q_T ⋙ A_(R⋙S⋙L⋙M⋙N))`.

All fourteen are assembled into `nativeGK4BZChosenInverse_fivePathIndexed (i : Fin 14)`, and the uniform `nativeGK4BZChosenInverse_fivePathIndexed_eq_direct` proves this equality for **every** `i`, with no extra assumptions. The related `nativeGK4BZChosenInverse_fivePathIndexed_targetNat_square` transports an actual target natural transformation of the first stage through each genuine path as a whole NatTrans commutative square, via GK4BU.

### 2. Independent unit removal in either order

On the **actual five-stage** target string

`R ⋙ 𝟭 U ⋙ S ⋙ 𝟭 V ⋙ L`,

construct two distinct, correctly typed *composites* of true Mathlib unitors and whiskerings:

- Order A first removes the identity at `U` (using `isoWhiskerRight (rightUnitor R)`), then the identity at `V` (using GK4BY's true `afterS` unitor).
- Order B first removes the identity at `V` (using `isoWhiskerLeft ... (leftUnitor L)`), then at `U` (using GK4BY's true `afterR` unitor).

Thus `u_A,u_B : R⋙𝟭 U⋙S⋙𝟭 V⋙L ≅ R⋙S⋙L`, and

`nativeGK4BZDoubleUnit_twoOrders_eq` proves the **whole genuine Mathlib NatIso** equation `u_A = u_B`.

The equality is proved by `Iso.ext` on the actual component morphisms of the constructed unitors and whiskers, not by assuming new higher comparison cells.

### 3. Fourteen-path chosen-inverse and whole NatTrans compatibility

For **every `i : Fin 14`**, the genuine five-stage bracket comparison `Φ_i` instantiated at `R,𝟭 U,S,𝟭 V,L` agrees as a whole NatIso with the direct three-stage `Θ_(R⋙S⋙L)`:

`Φ_i = Θ_(R⋙S⋙L)`.

Both unit-removal orders `u_A.hom` and `u_B.hom` satisfy the full GK4BU target-NatTrans modification square with `Φ_i`. The main `nativeGK4BZChosenInverse_doubleUnit_orderIndependent` proves that *both entire left-hand and right-hand NatTrans paste results are equal* when switching from removal order A to B. This is a whole NatTrans equality **uniformly in all fourteen five-target paths**, not merely existence of commutative component diagrams.

This extends GK4BY's one-unit/five-pentagon result by one actual target stage and two **independently positioned** target identities, retaining all prior Mathlib source and category authority boundaries.

## CI, axioms, and exact-source receipts

- Theorem source `cc92f709586bac91d03aa1d190832a354470639c`; test-merge `8bb1421585e6a0d48bee4b459e9d29121d86ec3e`; **identical Git tree** `ed8de1cf7bb61632e2daf0b264887410f76ef6eb`.
- [CI #41303246207](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41303246207): **Strict Lean 3821/3821 SUCCESS**; Independent Kuu core / retained public API **SUCCESS**; Workflow consolidation integrity **SUCCESS**; Governance terminal **SUCCESS**.
- Public declarations **42/42** have `#print axioms`. Exact log inspection shows only the standard three `propext`, `Classical.choice`, and `Quot.sound`; `sorryAx` 0; changed Lean error/warning 0/0.
- No previous Lean theorem source was modified or deleted. The output is scoped to the single appended file, pinned Lean/mathlib versions, the retained 107 public roots, and protected validation-only PR #1558 Draft/OPEN/unmerged. This proof record is added by a separate docs-only PR (Strict Lean SKIPPED).

## Precise authority boundary and next step

No unconditional faithfulness of the original dependent F45 source, original source-Q category laws, raw F54/F55/P92B Type-valued higher cells, all-integer-matrix attainability, global Gray structure, or unlimited hyperdescent is established. These are Mathlib functor-category equalities over a **fixed genuine attained AH image**. Strict 空 is central; independent Kuu is a presentation, not an unconditional reconstruction.

Candidate GK5A (or next available theorem label): a generic finite-length `List`-indexed induction principle for **endofunctor target chains** (fixed target category, clear scope), a second independent *adjacent* unit insertion order, or a universal coherence lemma for arbitrary target-NatIso compositions. None is included as proved in GK4BZ.
