import Kuu.F112.PolygonNativeHistoricalF45PhysicalComparison
import Kuu.F112.PolygonNativeF41TraceFunctorComposition

/-!
# F112-E7Q5-F4-P2-A — functorial historical-shaped Prop/Type evidence

The original frozen F42 primitive is Prop-valued, while the F45
history holding its intermediate Blocks is Type-valued.  This file
constructs positive transport through every ordinary category functor
for these exact independent native presentations.

The three real constructor shapes map along functors and the square
  native Type AxisTrace --erase--> historical-shaped Type AxisTrace
           | map F                        | map F
           v                              v
  native Type AxisTrace --erase--> historical-shaped Type AxisTrace
commutes as equality of the ENTIRE Type-valued history, not merely
its Prop existence or evaluated categorical arrow.

Functor identities/compositions are certified by HEq at the dependent
Blocks boundaries. Classical.choose is separately tracked: arbitrary
chosen Type-valued primitive representatives are compared ONLY after
the certified erasure. We assert no unproved raw choice naturality.

No frozen KUOS/Gray/F51/F77 imports; no source equality to the frozen
historical F19/F28/F44/F45 types is inferred.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uA vA uB vB uC vC
variable {A : Type uA} [Category.{vA} A]
variable {B : Type uB} [Category.{vB} B]
variable {C : Type uC} [Category.{vC} C]

/-- Forward action on ALL three genuine historical-shaped
Prop-valued primitive constructors, not a composite-Hom proxy. -/
def KuuNativeHistoricalOneStep.map (F : A ⥤ B)
    {x y : A} {p q : KuuNativeBlocks x y}
    (h : KuuNativeHistoricalOneStep p q) :
    KuuNativeHistoricalOneStep (p.map F) (q.map F) := by
  induction h with
  | split p q r =>
      simpa only [KuuNativeBlocks.map, KuuNativePath.map_append]
        using (KuuNativeHistoricalOneStep.split (p.map F) (q.map F) (r.map F))
  | insertNil p =>
      simpa only [KuuNativeBlocks.map, KuuNativePath.map] using
        (KuuNativeHistoricalOneStep.insertNil (p.map F))
  | whisker h t ih =>
      simpa only [KuuNativeBlocks.map] using
        (KuuNativeHistoricalOneStep.whisker ih (t.map F))

/-- The two forward realizations of the OLD-SHAPED Prop primitive
are equal on precise mapped native Blocks. The equality of proofs
uses the legitimate subsingleton property of Prop, not of raw Type. -/
theorem KuuNativeOneStep.map_toHistorical (F : A ⥤ B)
    {x y : A} {p q : KuuNativeBlocks x y}
    (h : KuuNativeOneStep p q) :
    (h.map F).toHistorical = h.toHistorical.map F :=
  Subsingleton.elim _ _

/-- Exact-Nat-depth historical-shaped Type histories transport
without losing the intermediate KuuNativeBlocks boundaries. -/
def KuuNativeHistoricalAxisTrace.map (F : A ⥤ B)
    {x y : A} {n : Nat} {p q : KuuNativeBlocks x y}
    (h : KuuNativeHistoricalAxisTrace n p q) :
    KuuNativeHistoricalAxisTrace n (p.map F) (q.map F) := by
  induction h with
  | refl p => exact .refl _
  | snoc h step ih => exact .snoc ih (step.map F)

/-- Actual erasure of raw Type history into historical-shaped
Prop-step Type history is NATURAL along every category functor. -/
theorem KuuNativeAxisTrace.map_toHistorical
    (F : A ⥤ B)
    {x y : A} {n : Nat} {p q : KuuNativeBlocks x y}
    (h : KuuNativeAxisTrace n p q) :
    (h.map F).toHistorical = h.toHistorical.map F := by
  induction h with
  | refl p => rfl
  | snoc h step ih =>
      change KuuNativeHistoricalAxisTrace.snoc
          ((h.map F).toHistorical) _ =
        KuuNativeHistoricalAxisTrace.snoc
          (h.toHistorical.map F) _
      rw [ih]

/-- P1's two distinct, but isomorphic, Prop-step Type traces are
naturally compared as ENTIRE history terms under any functor. -/
theorem KuuNativeHistoricalAxisTrace.map_toProp
    (F : A ⥤ B)
    {x y : A} {n : Nat} {p q : KuuNativeBlocks x y}
    (h : KuuNativeHistoricalAxisTrace n p q) :
    (h.map F).toProp = h.toProp.map F := by
  induction h with
  | refl p => rfl
  | snoc h step ih =>
      change KuuNativePropAxisTrace.snoc
        ((h.map F).toProp) _ =
        KuuNativePropAxisTrace.snoc (h.toProp.map F) _
      rw [ih]

theorem KuuNativePropAxisTrace.map_toHistorical
    (F : A ⥤ B)
    {x y : A} {n : Nat} {p q : KuuNativeBlocks x y}
    (h : KuuNativePropAxisTrace n p q) :
    (h.map F).toHistorical = h.toHistorical.map F := by
  induction h with
  | refl p => rfl
  | snoc h step ih =>
      change KuuNativeHistoricalAxisTrace.snoc
        ((h.map F).toHistorical) _ =
        KuuNativeHistoricalAxisTrace.snoc (h.toHistorical.map F) _
      rw [ih]

/-- All three dependent native Blocks indices are compared before
building a heterogeneous equality of full historical-shaped traces.
The Prop primitive proofs need no extra arbitrary equality axiom. -/
theorem KuuNativeHistoricalAxisTrace.snoc_heq_of_heq
    {x y : A} {n : Nat}
    {p q r p' q' r' : KuuNativeBlocks x y}
    (h : KuuNativeHistoricalAxisTrace n p q)
    (h' : KuuNativeHistoricalAxisTrace n p' q')
    (f : KuuNativeHistoricalOneStep q r)
    (f' : KuuNativeHistoricalOneStep q' r')
    (hp : p = p') (hq : q = q') (hr : r = r')
    (hh : HEq h h') :
    HEq (KuuNativeHistoricalAxisTrace.snoc h f)
        (KuuNativeHistoricalAxisTrace.snoc h' f') := by
  cases hp
  cases hq
  cases hr
  have he : h = h' := eq_of_heq hh
  cases he
  have fe : f = f' := Subsingleton.elim f f'
  cases fe
  rfl

/-- Identity is a dependent HEq law on the COMPLETE Type-valued
historical-shaped trace, including its actual intermediate Blocks. -/
theorem KuuNativeHistoricalAxisTrace.map_id_heq
    {x y : A} {n : Nat} {p q : KuuNativeBlocks x y}
    (h : KuuNativeHistoricalAxisTrace n p q) :
    HEq (h.map (𝟭 A)) h := by
  induction h with
  | refl p =>
      simp only [KuuNativeHistoricalAxisTrace.map]
      rw [KuuNativeBlocks.map_id p]
      rfl
  | snoc h step ih =>
      exact KuuNativeHistoricalAxisTrace.snoc_heq_of_heq
        (h.map (𝟭 A)) h (step.map (𝟭 A)) step
        (KuuNativeBlocks.map_id _)
        (KuuNativeBlocks.map_id _)
        (KuuNativeBlocks.map_id _)
        ih

/-- General composite functors act coherently on old-shaped
Type-valued histories with both dependent Blocks casts explicit. -/
theorem KuuNativeHistoricalAxisTrace.map_comp_heq
    (F : A ⥤ B) (G : B ⥤ C)
    {x y : A} {n : Nat} {p q : KuuNativeBlocks x y}
    (h : KuuNativeHistoricalAxisTrace n p q) :
    HEq (h.map (F ⋙ G)) ((h.map F).map G) := by
  induction h with
  | refl p =>
      simp only [KuuNativeHistoricalAxisTrace.map]
      rw [KuuNativeBlocks.map_comp F G p]
      rfl
  | snoc h step ih =>
      exact KuuNativeHistoricalAxisTrace.snoc_heq_of_heq
        (h.map (F ⋙ G)) ((h.map F).map G)
        (step.map (F ⋙ G)) ((step.map F).map G)
        (KuuNativeBlocks.map_comp F G _)
        (KuuNativeBlocks.map_comp F G _)
        (KuuNativeBlocks.map_comp F G _)
        ih

/-- A chosen lift is compatible with arbitrary functor transport
AFTER the precise historical erasure. It is deliberately NOT an
equality of arbitrarily selected raw Type witnesses. -/
theorem KuuNativeHistoricalAxisTrace.chooseNative_map_observed
    (F : A ⥤ B)
    {x y : A} {n : Nat} {p q : KuuNativeBlocks x y}
    (h : KuuNativeHistoricalAxisTrace n p q) :
    ((h.chooseNative.map F).toHistorical) =
      ((h.map F).chooseNative.toHistorical) := by
  calc
    (h.chooseNative.map F).toHistorical =
        h.chooseNative.toHistorical.map F :=
      KuuNativeAxisTrace.map_toHistorical F h.chooseNative
    _ = h.map F :=
      congrArg (KuuNativeHistoricalAxisTrace.map F)
        h.toHistorical_chooseNative
    _ = (h.map F).chooseNative.toHistorical :=
      ((h.map F).toHistorical_chooseNative).symm

#print axioms KuuNativeHistoricalOneStep.map
#print axioms KuuNativeOneStep.map_toHistorical
#print axioms KuuNativeHistoricalAxisTrace.map
#print axioms KuuNativeAxisTrace.map_toHistorical
#print axioms KuuNativeHistoricalAxisTrace.map_toProp
#print axioms KuuNativePropAxisTrace.map_toHistorical
#print axioms KuuNativeHistoricalAxisTrace.snoc_heq_of_heq
#print axioms KuuNativeHistoricalAxisTrace.map_id_heq
#print axioms KuuNativeHistoricalAxisTrace.map_comp_heq
#print axioms KuuNativeHistoricalAxisTrace.chooseNative_map_observed
end
end Kuu.F112.Physical
