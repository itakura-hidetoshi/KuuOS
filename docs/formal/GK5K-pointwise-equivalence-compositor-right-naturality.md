# F112-P94D3GK5K — Genuine pointwise-equivalence compositor naturality in the right argument

**Date:** 2026-11-02 JST  
**Theorem PR:** [#2917](https://github.com/itakura-hidetoshi/KuuOS/pull/2917) — MERGED  
**Theorem squash/main HEAD at merge:** `9d63868a33c864ba00c596966b2a0d001df211e7`  
**Final exact-source HEAD:** `41e17a8f06749215c9fb8bf0f74df74a47af3af3`  
**Matching source/squash Git tree:** `6e870e81a6068592c0677d02e246bfc7428b0fe8`  
**Exact-source CI:** [#41363398263](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41363398263) — terminal SUCCESS.

## Canonical source and inherited foundations

[PolygonNativeC60AQFullPentagonPhysicalNativeGK5KCompositorNaturality.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5KCompositorNaturality.lean)

GK5K adds exactly one Lean file, importing the already merged GK5J and inherited GK5G genuine pointwise category-equivalence change, GK5I three-atom associator and GK5H obstruction criterion. It does not change any earlier theorem source or loosen pinned hypotheses. Fix genuine `C,D : I → Cat.{vC,uC}`, `e : ∀ i : I, C i ≌ D i`, and bona fide `R : C i ⥤ C j`, `S,T : C j ⥤ C k`.

Define the genuine change of atom `ChangeAtom(e,R) = (e i).inverse ⋙ R ⋙ (e j).functor` and the genuine nonstrict `ChangeCompIso(e,R,S) : ChangeAtom(e,R) ⋙ ChangeAtom(e,S) ≅ ChangeAtom(e,R ⋙ S)`. The compositor uses the actual inverse `(e j).unitIso.inv`, **not** strict inverse equivalences.

## Exact new theorems

**Whole NatTrans right-variable naturality:** For every genuine natural transformation `β : S ⟶ T`, the verified public theorem `nativeGK5KChangeCompNat_right` proves the equality between whole natural transformations:

```lean
Functor.whiskerLeft (nativeGK5GChangeAtom e R)
    (nativeGK5GChangeNat e β) ≫
  (nativeGK5GChangeCompIso e R T).hom =
(nativeGK5GChangeCompIso e R S).hom ≫
  nativeGK5GChangeNat e (Functor.whiskerLeft R β)
```

This is the genuine naturality of the nontrivial binary pointwise-equivalence compositor in its second argument. In a component `X : D i`, the key equation is the genuine Mathlib `β.naturality` at `(e j).unitIso.inv.app (R.obj ((e i).inverse.obj X))`. The proof applies `congrArg (fun f => (e k).functor.map f)` and functorial map-composition, not an assumed strict cancellation.

**Whole NatIso right-variable naturality:** For any genuine isomorphism `β : S ≅ T`, `nativeGK5KChangeCompIso_right` proves:

```lean
Functor.isoWhiskerLeft (nativeGK5GChangeAtom e R)
    (nativeGK5GChangeIso e β) ≪≫
  nativeGK5GChangeCompIso e R T =
nativeGK5GChangeCompIso e R S ≪≫
  nativeGK5GChangeIso e (Functor.isoWhiskerLeft R β)
```

This is the WHOLE natural-isomorphism counterpart, not just a chosen component; it derives by `Iso.ext`, `Functor.isoWhiskerLeft_hom`, and GK5I's certified exact whole NatIso-to-NatTrans hom identity.

## CI, syntax diagnostic, axioms and provenance

- Initial source commit `bd5c264b455830d2d167c55c14d481bba722484e`: CI #41363094072 exposed `simp made no progress` at an auxiliary `simp only` immediately after `dsimp` had already performed all specified reductions. The dependency signatures and entire changed Lean file were reviewed. Correction was to remove only that redundant, inapplicable second simplifier; the genuine naturality proof and all original hypotheses remained unchanged.
- Final exact-source commit `41e17a8f06749215c9fb8bf0f74df74a47af3af3`.
- Squash/main theorem commit `9d63868a33c864ba00c596966b2a0d001df211e7`; source/squash matching tree `6e870e81a6068592c0677d02e246bfc7428b0fe8`, independently fetched via GitHub MCP.
- Final [CI #41363398263](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41363398263) **Strict Lean 3832/3832 SUCCESS**, Independent Kuu core **SUCCESS**, workflow integrity **SUCCESS**, Governance terminal **SUCCESS**.
- Both `#print axioms` outputs (**2/2**) list only `propext`, `Classical.choice`, `Quot.sound`, with no `sorryAx` or new axiom. Final changed Lean errors/warnings 0/0.
- Pinned Lean `v4.30.0-rc2`; pinned mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`. Existing public root107 retained, protected validation-only PR #1558 remains Draft/open/unmerged. Strict 空 is central; independent Kuu is one presentation. No Gray, arbitrary hyperdescent, original raw Type-valued high cells or unguarded strictification of chosen inverses.

## Exact obstruction boundary and GK5L

GK5K has proved **right-argument naturality of the binary comparator** only; it does not prove analogous left-variable naturality for `α : R ⟶ R'`, the general arbitrary finite-subtree associator, left/right unitor or two contextual whiskering generator squares. The GK5H/GK5J all-path/endpoint/step equivalences remain conditional, and their hypotheses have not been discharged wholesale.

Next GK5L: prove left-argument naturality via the real `(e j).unitIso.inv.naturality` square at `α.app X`, combine both sides to a two-variable `χ` interchange theorem, then use GK5I's three-functor compositor associativity to pursue arbitrary-subtree associator coherence with each true `Φ_a,Φ_b,Φ_c`. Only after additionally discharging both unitor and whiskering generators should GK5H be invoked for unconditional all-finite-path coherence.

Documentation-only PR: leave Strict Lean **SKIPPED**; verify independent Kuu, workflow integrity and governance terminal SUCCESS.
