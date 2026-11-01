# F112-P94D3GK4BY — Four-position pentagon unit insertion and inverse-unitor coherence

**2026-11-01 JST**  
**Canonical theorem PR:** [#2893](https://github.com/itakura-hidetoshi/KuuOS/pull/2893), MERGED  
**Theorem squash / main HEAD at merge:** `a5978505b29ecaea3e80eab105d273fac1ebcb43`  
**Final exact-source HEAD:** `68257c0caf07d6f5be7d8f4aaf88d00e00846faa`  
**Final test-merge commit:** `fcedab4a7e98d406bbc15cdb707f4d762ab95bd5`  
**Matching source/test-merge Git tree:** `153e61366cfb20882c384abd11d1c9c9f6c66206`  
**Exact-source CI:** [#41301271737](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41301271737), SUCCESS.

## Canonical Lean source

[PolygonNativeC60AQFullPentagonPhysicalNativeGK4BYChosenInverseUnitInsertionPentagonInverse.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BYChosenInverseUnitInsertionPentagonInverse.lean)

Pinned Lean v4.30.0-rc2, mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`. The new file imports GK4BX and retains the actual dependent signatures through GK4BW (genuine four-target five-bracketing NatIso), GK4BV (two-step composition), GK4BU (target-NatTrans modification), GK4BT (arbitrary chosen inverse target comparison), and GK4BM/GK4BP/GK4BQ (choice versus explicit inverse transport).

## Precisely proved mathematics (22 public declarations)

For actual target functors `R : T ⥤ U`, `S : U ⥤ V`, and `L : V ⥤ W`, denote their actual composite by `F = R ⋙ S ⋙ L`. Insert a single target identity functor in **any of the four positions**:

- `𝟭 T ⋙ R ⋙ S ⋙ L` (head)
- `R ⋙ 𝟭 U ⋙ S ⋙ L` (after R)
- `R ⋙ S ⋙ 𝟭 V ⋙ L` (after S)
- `R ⋙ S ⋙ L ⋙ 𝟭 W` (tail)

For each position `i`, GK4BY constructs a genuine iterated Mathlib natural isomorphism `u_i : F_i ≅ F`, made only from the actual `Functor.leftUnitor`, `Functor.rightUnitor`, and `Functor.isoWhiskerRight`; it never replaces this by an assumed raw high-dimensional cell.

**Pentagon/unit interchange.** For every `i` and every one of GK4BW's **five actual nested pentagon paths** `K = A,B,C,D,E`, the whole Mathlib NatIso `Θ^K_(F_i)` equals the directly constructed `Θ_F`. Thus **20 whole-NatIso equalities** are formally proved, grouped in four conjunction theorems. The actual GK4BU modification for the whole `NatTrans` `u_i.hom` commutes with every path, and the same is proved separately for the inverse `u_i.inv`: **20 forward plus 20 inverse whole-NatTrans squares**. Each has the fully typed expression
`(C_(u_i.hom) ▷ Q_W) ≫ Θ_F.hom = Θ^K_(F_i).hom ≫ (Q_T ◁ A_(u_i.hom))`, with the inverse equation reversed in target direction and the appropriate placement of `Θ`.

**Inverse unitors and inverse triangle.** The *actual Mathlib inverse* left and right target unitors satisfy the genuine choice-inverse `Θ` comparison squares, rather than strict `Q_T=P_T` equality. The inverse triangle is a whole target NatTrans equality:

`whiskerRight (rightUnitor R).inv S = whiskerLeft R (leftUnitor S).inv ≫ (associator R (𝟭 U) S).inv`.

GK4BY additionally establishes two inverse-triangle whole `Θ` squares through the real GK4BW three-stage left/right pastings, and their whole left/right NatTrans equality via the original GK4BW associativity.

**No added axioms** are needed to link GK4BU's modification, GK4BV composition, GK4BW pentagon/unit, and GK4BX target-naturality/triangle. The chosen inverse `Q_T` is still not definitionally identified with the explicit `P_T`.

## Independent verification receipt

- Final source HEAD `68257c0caf07d6f5be7d8f4aaf88d00e00846faa` and test-merge `fcedab4a7e98d406bbc15cdb707f4d762ab95bd5`: identical Git tree `153e61366cfb20882c384abd11d1c9c9f6c66206`.
- Exact-source Strict Lean **3820/3820 SUCCESS**.
- Independent Kuu core/public API **SUCCESS**, Workflow consolidation integrity **SUCCESS**, Governance terminal **SUCCESS**.
- All **22 public declarations have one `#print axioms` each (22/22)**. Actual log parsing confirms precisely `propext`, `Classical.choice`, `Quot.sound`, no other axioms; `sorryAx` zero; changed Lean file error/warning 0/0.
- Initial CI had **one elaboration failure**, at the final proof: the associativity rewrite simplified both equalities in a conjunction to `True`, so `⟨rfl,rfl⟩` was not a term of `True ∧ True`. The only code repair replaces this terminal step with `all_goals simp`; no assumptions, definitions, or theorem conclusions were weakened. Full source/imports/dependent signatures/pinned Mathlib API were reviewed and the entire exact-head CI rerun.
- Repository policy: append-only one new Lean source, public root107 retained, no Gray reintroduction, validation-only protected PR #1558 remains Draft/OPEN/unmerged. Any GitHub Actions Node deprecation notices are unrelated to the changed Lean source.

## Boundaries and next research

This is precisely finite-target Mathlib functor-category coherence, **not** unconditional original F45 source faithfulness, original source-Q category laws, raw F54/F55/P92B Type-valued higher cells, full integer-matrix attainability, global Gray, or unbounded higher hyperdescent. Strict 空 is central; independent Kuu remains one presentation.

Candidate GK4BZ: coherence for *two or more* independently inserted target identities in a four- or five-stage chain, with explicit actual unitors and bracket reassociation; or a bounded induction principle for finite target chains, if this can be proved without introducing new axioms or conflating chosen and explicit inverses.

Theorem PR and this docs-only sync are distinct. Docs-only CI should SKIP Strict Lean. Prior README/ROADMAP proof history is retained.
