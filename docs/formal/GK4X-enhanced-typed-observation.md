# F112-P94D3GK4X — true F45 Boolean×cast-charge observation and second-kernel comparison

**2026-10-31 JST.** Repository `itakura-hidetoshi/KuuOS`; authoritative theorem-carrier branch `main`.
[Theorem PR #2781](https://github.com/itakura-hidetoshi/KuuOS/pull/2781) **MERGED**.
Theorem squash SHA `eaa66af512371fb9c8a051cd565188ec842bc809` exactly matched canonical `main` HEAD immediately after theorem merge.
Final exact PR source HEAD `36ceae9208e40c6dcb8bf6c6755639a112e8f155`.
[Exact-source GitHub CI #41172335888](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41172335888) **3732/3732 Strict Lean SUCCESS** and **5/5 Governance jobs completed SUCCESS** (all relevant steps completed). The **43** new Lean declarations have individually printed `#print axioms` receipts using only subsets of `propext`, `Classical.choice`, `Quot.sound`; **sorryAx 0**, changed Lean warning/error **0/0**.

## Original three authorities retained

- `Q`: ORIGINAL P92B Type-valued comparison-EXISTENCE quotient over original F54 dependent routes, still not a category under its unproved source composition laws.
- `S`: independently extended GK4E F54 structural-comparison existence quotient, made a TRUE Mathlib Category on all actual dependent F45 stages by GK4I/H.
- `K_{O_X}`: GK4S's SECOND quotient of `Q` by equality of the new `O_X` values. This is a distinct quotient of actual original P92B source classes, NOT a fabricated raw Type-valued P92B comparison or automatic identification with `S`.

All D/E categories, four true F19/F28 Blocks, paired Nat depth indices, genuine C60 F45 trees and original F54/P92B witness types remain unaltered. The GK4W original fully typed `castCharge(r)=#castDepths(r)-#physicalRotations(r)` has already been proved sound across all original F55/P92B comparison generators and all independent structural F54 seams.

## New true quotient observations

[EnhancedObserver source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4XEnhancedObserver.lean) independently descends the signed `Int` castCharge to both original `Q` and distinct independent `S` by `Quotient.lift` and W's proven comparison-constructor invariance. It proves actual commuting `Q→S→Int = Q→Int`, additive charge laws under original `Q` and genuine structural `S` composition, and witnessed charge zero for both original zero-route representative and the TRUE structural identity. **It does not infer Q associativity or its missing unit laws.**

The true enhanced observation is `O_X(q)=(G_P92(q),Charge_P92(q))` at every original dependent F45 boundary, and `O_X(s)=(G_S(s),Charge_S(s))` separately on `S`. Its exact multiplication and unit are:

```text
(b,c) ⋄ (d,e) = (b && d, c + e)         (b,d : Bool, c,e : Int)
identity = (true, 0)
```

Lean proves associativity, left/right value units and TRUE original F54 composition observation law, plus both actual original F45 left/right context laws with identity value actions. New `O_X` is globally preserved by genuine F54 independent structural seams, using GK4W's all-14 proof-relevant seam induction and GK4N Boolean seam preservation.

## Actual Mathlib functor and old grading factorization

[EnhancedFunctor source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4XEnhancedFunctor.lean) constructs a separate new one-object `NativeGK4XValuePoint` Mathlib Category with Hom `Bool×Int`, associative product `⋄` and genuine unit `(true,0)`. It then constructs a true Mathlib Functor from GK4I's independent fully-typed F45 STRUCTURAL category into this value category, with its arrow map equal to `O_X:S→Bool×Int` and its identity/compose laws proved from the real original F54/H/W source facts. Independently construct a forgetful Functor `Bool×Int→Bool` and prove BOTH object-map and arrow-map pointwise factorization to the existing GK4I Boolean grading functor.

**Authority boundary:** This is an ambient monoid-value one-object Category; we do NOT assert every possible `Bool×Int` value is actually attained on every original typed F45 Hom, nor prove source equivalence/faithfulness/fullness.

## Actual second P92B observation-kernel quotient

Using GK4X's original P92B observer family, GK4P's observed composition/context laws and complete new F54 seam invariance, invoke GK4T's exact universal property to construct a genuinely typed `S→K_{O_X}` map. Its canonical `Q→S→K_{O_X}` triangle commutes, it is SURJECTIVE, and its equality kernel is the exact new observation-pair equality:

```text
F_X(u) = F_X(v)   iff   O_X(u) = O_X(v)
                       iff   grade(u) = grade(v) and charge(u) = charge(v).
```

The actual `K_{O_X} ≃ Im(O_X)` equivalence comes from GK4S and is used explicitly in the Lean comparison-value proof. The enhanced comparison is injective iff the genuinely typed structural observer pair is injective. **We do not assume it IS injective on all source homs.**

## Cast tower is separated: strict improvement over GK4W Boolean collapse

At every inhabited original F45 self-stage, GK4W's original F54 tower `T_k` is defined by true `castDepths rfl rfl tree` source constructors, and was proven to satisfy rotationCount zero and castCharge k. The new proofs show:

```text
O_X([T_k]_S) = (true, (k:Int)).
Injective (k:Nat -> O_X([T_k]_S)).
Injective (k:Nat -> F_X([T_k]_S))  in the ACTUAL K_{O_X} quotient.
```

The true cast route has `O_X=(true,1)` while the genuine structural zero-route identity class has `O_X=(true,0)`. They have the SAME old Boolean grade true but are now distinguished by the enhanced observation AND by the actual second original P92B kernel quotient. This does not generate an original Type-valued P92B 3-cell or prove arbitrary full structural witness recovery.

## Lean elaboration corrections

Initial theorem source HEAD `1d8d260b41426dce3c264c6234271ad3925ee1d9`: Lean reported a rewrite failure in `nativeGK4XEnhancedStructural_castTower_injective`. After `intro i j hij`, the hypothesis was a *lambda-application* equality and plain `rw` did not locate the fully applied source theorem. Repair in intermediate HEAD `85715417d2623c64448708bd09ad0580d5955c3b`: `change` the hypothesis into the exact two fully typed GK4W tower class applications before applying each specific `nativeGK4XEnhancedStructural_castTower tree i/j` rewrite.

The next attempt elaborated the tower values but `exact_mod_cast` failed on an unnormalized `Prod.snd` equality of `(true,(i:Int)).2=(true,(j:Int)).2`. Final HEAD `36ceae9208e40c6dcb8bf6c6755639a112e8f155` explicitly `change (i:Int)=(j:Int) at hcast` then uses `exact_mod_cast hcast`. That final exact source passed both new complete files, all axioms, warnings/errors and Governance. **Neither failed previous CI is a completion receipt.**

## Governance and next research

Unproved: the enhanced functor's universal faithfulness/fullness or equivalence; the complete true structural quotient classification; a separately instantiated Mathlib Category on the actual `K_{O_X}` attained-kernel homs (GK4Y candidate); original P92B associativity and unit laws, alternative source multiplication, historical complete P92B/F19/F28/F54/F55 typed equivalence, genuine original 14D unconditional Countable, original 19D filler, global strict n or hyperdescent. We do not upgrade equality of observations to historical Type-valued 3-cell evidence.

Append-only, tighten-only, overwrite-forbidden, same-root; 107 public roots untouched; Lean v4.30.0-rc2, mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`, strict 空 central, independent Kuu one presentation, no Gray. Protected validation-only PR #1558 remains Draft/open/unmerged.

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
