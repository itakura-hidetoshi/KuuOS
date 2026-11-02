# F112-P94D3GK5M — Genuine arbitrary finite typed subtree associator coherence

**Date:** 2026-11-02 JST  
**Theorem PR:** [#2921](https://github.com/itakura-hidetoshi/KuuOS/pull/2921) — MERGED  
**Theorem squash/main HEAD at theorem merge:** `3d7397eaa7d9db905cf2eec3d6dc33022c3e9079`  
**Final exact-source HEAD:** `56692513432a1b1f0ad744871dc6bfd2989117b4`  
**Matching source/squash Git tree:** `9f6994ad162fd003dca2cfc58ccad59243b129be`  
**Exact-source CI:** [#41366413951](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41366413951) — terminal SUCCESS.

## Canonical proof source

[PolygonNativeC60AQFullPentagonPhysicalNativeGK5MArbitraryTreeAssociator.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5MArbitraryTreeAssociator.lean)

One append-only Lean file following GK5L. Ambient objects: actual indexed Mathlib category families `C,D:I→Cat.{vC,uC}`; specified genuine equivalences `e:∀i,C i≌D i`; arbitrary dependently typed finite GK5D trees `a:C_i→C_j`, `b:C_j→C_k`, `c:C_k→C_l`; actual GK5G whole comparison NatIsos `Φ_t : eval_D(ChangeTree(e,t)) ≅ ChangeAtom(e,eval_C(t))`. Neither the middle equivalence unit nor any arbitrary chosen inverse is strictified.

## Proven declarations and mathematical structure

### Genuine compositor associativity for arbitrary three whole functors

`nativeGK5MCompositor_associator e R S T` establishes the actual nonstrict binary comparator associativity, for arbitrary genuine composable Mathlib functors `R,S,T`:

```lean
Functor.associator (ChangeAtom e R) (ChangeAtom e S) (ChangeAtom e T) ≪≫
  Functor.isoWhiskerLeft (ChangeAtom e R) (ChangeCompIso e S T) ≪≫
  ChangeCompIso e R (S ⋙ T)
=
Functor.isoWhiskerRight (ChangeCompIso e R S) (ChangeAtom e T) ≪≫
  ChangeCompIso e (R ⋙ S) T ≪≫
  ChangeIso e (Functor.associator R S T)
```

Here `ChangeAtom`, `ChangeCompIso` and `ChangeIso` denote the genuine already certified GK5G definitions. The Lean proof is a precise theorem extraction from GK5I's real three-atom associator, with actual Mathlib associator, iso-whiskering and nonstrict pointwise category equivalence cancellation preserved. No assumption that the whole functors originally arose as atom leaves is required.

### Arbitrary finite-subtree local associator square

The new public theorem `nativeGK5MAssociator_subtrees e a b c` proves the GK5H/GK5J **whole NatIso coherence square** with the actual GK5D associator generator for **all finite typed subtrees**:

```lean
NativeGK5JPathSquare e
  (NativeGK5DTypedPath.basic (NativeGK5DTypedStep.assoc a b c))
```

Expanding the predicate gives

```lean
nativeGK5DStepIso (nativeGK5GChangeStep e (.assoc a b c)) ≪≫
  nativeGK5GChangeTreeIso e (.paste a (.paste b c))
=
nativeGK5GChangeTreeIso e (.paste (.paste a b) c) ≪≫
  nativeGK5GChangeIso e (nativeGK5DStepIso (.assoc a b c))
```

This is **unconditional for any actual finite typed GK5D subtree**, with nontrivial recursive `Φ_a`, `Φ_b`, `Φ_c`, not limited to the three atomic leaves proved in GK5I. It is genuine whole Mathlib NatIso equality, not merely a witness label or equality at a selected object.

### Actual naturality bridge

A new private verified helper `nativeGK5MUnitComparisonNaturality` proves the nontrivial interchange of an arbitrary genuine NatIso `φ:S≅ChangeAtom(e,R)` with the inverse equivalence unit natural transformation. At each `f:Y⟶Z` in the intermediate category it establishes a morphism equality relating:
- `φ.hom.app (e_k.functor.obj Y)`;
- the genuine mapped `(e_k).unitIso.inv.app Y` followed by `f`;
- `S.map (e_k.functor.map f)`, `φ.hom.app (e_k.functor.obj Z)`, and the corresponding mapped inverse unit at `Z`.

The proof uses the **actual** pinned Mathlib `unitIso.inv.naturality f`, `φ.hom.naturality (e_k.functor.map f)`, functor mapping of composition, category associativity and explicitly typed `congrArg` on morphism composition. The arbitrary-subtree theorem applies this bridge in exactly the common-prefix context of the third subtree `c`. This is nontrivial: `Φ_c` cannot be replaced by reflexivity for non-atomic `c`.

## Exact-source certification and Lean diagnostic record

- Final source `56692513432a1b1f0ad744871dc6bfd2989117b4`, theorem squash/main `3d7397eaa7d9db905cf2eec3d6dc33022c3e9079`. Both GitHub MCP raw commit Git trees agree exactly: `9f6994ad162fd003dca2cfc58ccad59243b129be`.
- Exact source [CI #41366413951](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41366413951) terminal **Strict Lean 3834/3834 SUCCESS**, Independent Kuu **SUCCESS**, Workflow integrity **SUCCESS**, Governance **SUCCESS**.
- **2/2 public `#print axioms`** outputs list only `propext`, `Classical.choice`, and `Quot.sound`; `sorryAx0`, no new axioms, changed Lean errors/warnings 0/0. The private helper is used by the public theorem, so its axiom dependencies are included in the latter audit.
- Initial exact-source CI proved the general three-functor compositor associativity but left a large nontrivial `Φ_c`/middle-unit naturality goal. The next attempt explicitly surfaced `Φ_c.hom.naturality` and `unitIso.inv.naturality`; the goal showed the need to map the inverse-unit naturality into the correct downstream functor.
- The naturality bridge was extracted as its own private proven helper. Two subsequent fixes addressed only Lean elaboration and rewriting mechanics: category composition parentheses were made explicit, and `congrArg` was used to apply equalities under actual functor maps and their true common-prefix composition. No theorem was weakened and no previous historical file overwritten.
- Fixed Lean `v4.30.0-rc2`, pinned mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`. root107 unchanged; protected validation PR #1558 stays Draft/open/unmerged; strict 空 center and independent Kuu one presentation. The historical distinction between arbitrary chosen inverse `Q_T` and explicit `P_T` through genuine `κ_T` is retained.

## Precise remaining obstruction and next stage GK5N

GK5M discharges the **unconditional associator-generator class** for every finite typed subtree. It does **not** prove either left/right unit generator or either contextual whiskering generator class. Therefore `NativeGK5HStepCompatible e` as a universal predicate and `NativeGK5HPathCompatible e` for *all* paths are not yet established unconditionally. The GK5H/GK5J local/global/endpoint obstruction equivalences remain valid conditional statements.

Next GK5N: prove the genuine unit/counit triangle compatibility for the actual `leftUnit a` and `rightUnit a` whole NatIso squares, with recursive `Φ_a` and the nonstrict GK5G change-unit comparison; then prove contextual left and right whiskering squares, combining GK5K/GK5L compositor naturality with induction on structural steps. Only once all generators are discharged can the already verified GK5H local-to-global equivalence yield unconditional whole NatIso/whole NatTrans finite-path naturality. The original F45 unconditional faithfulness, source-Q category axioms, raw Type-valued F54/F55/P92B high cells, unrestricted Gray/hyperdescent and changing-universe arbitrary chains remain outside this result.

Documentation-only follow-up: **Strict Lean SKIPPED**; verify docs governance separately.
