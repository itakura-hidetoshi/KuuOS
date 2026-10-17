import Kuu.F112.PolygonNativeF41FunctorIdentity

/-!
# F112-E7Q5-F4-O2-C — full Type-valued F41 history identity law

The proof of identity on ALL primitive OneStep constructors from
F4-O2-B is transported through the dependent, exact-depth F41
AxisTrace grammar, preserving each original intermediate Blocks
presentation and actual primitive proof. Since the trace is a
Type-valued history, its length and its primitive witnesses are
not reconstructed from any Prop or scalar shadow.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uA vA
variable {A : Type uA} [Category.{vA} A]

/-- Dependent congruence for the exact-depth trace constructor:
ALL three source/intermediate/target Blocks and BOTH Type-valued
component proof terms must be compatible. -/
theorem KuuNativeAxisTrace.snoc_heq_of_heq
    {x y : A} {n : Nat}
    {p q r p' q' r' : KuuNativeBlocks x y}
    (h : KuuNativeAxisTrace n p q)
    (h' : KuuNativeAxisTrace n p' q')
    (f : KuuNativeOneStep q r)
    (f' : KuuNativeOneStep q' r')
    (hp : p = p') (hq : q = q') (hr : r = r')
    (hh : HEq h h') (hf : HEq f f') :
    HEq (KuuNativeAxisTrace.snoc h f)
      (KuuNativeAxisTrace.snoc h' f') := by
  cases hp
  cases hq
  cases hr
  have he : h = h' := eq_of_heq hh
  have fe : f = f' := eq_of_heq hf
  cases he
  cases fe
  rfl

/-- ACTUAL arbitrary-depth proof-relevant F41 histories preserve
identity strictly up to the necessary heterogeneous source/target
reindexing. Every original primitive operation survives. -/
theorem KuuNativeAxisTrace.map_id_heq
    {x y : A} {n : Nat} {p q : KuuNativeBlocks x y}
    (h : KuuNativeAxisTrace n p q) :
    HEq (h.map (𝟭 A)) h := by
  induction h with
  | refl p =>
      simp only [KuuNativeAxisTrace.map]
      rw [KuuNativeBlocks.map_id p]
  | snoc h step ih =>
      exact KuuNativeAxisTrace.snoc_heq_of_heq
        (h.map (𝟭 A)) h (step.map (𝟭 A)) step
        (KuuNativeBlocks.map_id _)
        (KuuNativeBlocks.map_id _)
        (KuuNativeBlocks.map_id _)
        ih (KuuNativeOneStep.map_id_heq step)

#print axioms KuuNativeAxisTrace.snoc_heq_of_heq
#print axioms KuuNativeAxisTrace.map_id_heq
end
end Kuu.F112.Physical
