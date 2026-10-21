import Kuu.F112.PolygonNativeF41TraceFunctorIdentity

/-!
# F112-E7Q5-F4-O2-D1 — dependent elementary functor-map coherence

For functor COMPOSITION the mapped F41 primitive proofs must be
compared as real Type-valued witnesses. The independent F41 map
inserts Eq.rec transports at split (the native path append proof)
and subsequent whiskering. The following exact constructor-shaped
heterogeneous comparisons and dependent congruence lemmas are the
building blocks for composing two arbitrary ordinary functors.

No proof erasure, Gray source, or new axioms.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uA vA uB vB
variable {A : Type uA} [Category.{vA} A]
variable {B : Type uB} [Category.{vB} B]

/-- Explicit true mapped root split witness modulo only its
dependent Eq.rec transport; the three actual source paths survive. -/
theorem KuuNativeOneStep.map_split_heq
    (F : A ⥤ B)
    {w x y z : A} (p : KuuNativeBlocks w x)
    (q : KuuNativePath x y) (r : KuuNativePath y z) :
    HEq ((KuuNativeOneStep.split p q r).map F)
      (KuuNativeOneStep.split (p.map F) (q.map F) (r.map F)) := by
  simp [KuuNativeOneStep.map]

/-- The original insertNil root also has a genuine mapped
Type-valued representative, before quotienting or erasing steps. -/
theorem KuuNativeOneStep.map_insertNil_heq
    (F : A ⥤ B)
    {x y : A} (p : KuuNativeBlocks x y) :
    HEq ((KuuNativeOneStep.insertNil p).map F)
      (KuuNativeOneStep.insertNil (p.map F)) := by
  simp [KuuNativeOneStep.map]

/-- Splitting is heterogeneously congruent if all three real path
and Blocks arguments agree. No Type-valued proof irrelevance. -/
theorem KuuNativeOneStep.split_heq_of_eq
    {w x y z : A}
    {p p' : KuuNativeBlocks w x}
    {q q' : KuuNativePath x y}
    {r r' : KuuNativePath y z}
    (hp : p = p') (hq : q = q') (hr : r = r') :
    HEq (KuuNativeOneStep.split p q r)
      (KuuNativeOneStep.split p' q' r') := by
  cases hp
  cases hq
  cases hr
  rfl

/-- Empty-block insertion has its separate dependent congruence. -/
theorem KuuNativeOneStep.insertNil_heq_of_eq
    {x y : A} {p p' : KuuNativeBlocks x y}
    (hp : p = p') :
    HEq (KuuNativeOneStep.insertNil p)
      (KuuNativeOneStep.insertNil p') := by
  cases hp
  rfl

/-- Any TWO explicitly compared Type-valued primitive witnesses can
be mapped through a common ordinary functor while their respective
source/target Blocks are transported together. -/
theorem KuuNativeOneStep.map_heq_of_heq
    (F : A ⥤ B)
    {x y : A} {p q p' q' : KuuNativeBlocks x y}
    (h : KuuNativeOneStep p q)
    (h' : KuuNativeOneStep p' q')
    (hp : p = p') (hq : q = q')
    (hh : HEq h h') :
    HEq (h.map F) (h'.map F) := by
  cases hp
  cases hq
  have he : h = h' := eq_of_heq hh
  cases he
  rfl

#print axioms KuuNativeOneStep.map_split_heq
#print axioms KuuNativeOneStep.map_insertNil_heq
#print axioms KuuNativeOneStep.split_heq_of_eq
#print axioms KuuNativeOneStep.insertNil_heq_of_eq
#print axioms KuuNativeOneStep.map_heq_of_heq
end
end Kuu.F112.Physical
