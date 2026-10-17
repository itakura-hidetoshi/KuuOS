import Kuu.F112.PolygonNativeFunctorPrimitiveHistoryLaws

/-!
# F112-E7Q5-F4-O2-B — dependent primitive proof congruence

The raw F41 OneStep is a Type-valued family indexed by TWO
separate F40 Blocks.  Its whisker constructor additionally carries
the actual native categorical path appended to both endpoints.
Rewriting just one indexed endpoint under Eq.mpr can destroy the
type of the next proof term.

This file isolates the exact heterogeneous congruence of the
three pieces of actual source evidence. It does NOT use any
proof-irrelevance for OneStep and does not replace the primitive
data by its Prop/numeric shadow.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uA vA
variable {A : Type uA} [Category.{vA} A]

/-- A dependent source packet retains the beginning Blocks, ending
Blocks, and actual Type-valued primitive witness at once. -/
structure KuuNativeF41StepPacket {x y : A} where
  source : KuuNativeBlocks x y
  target : KuuNativeBlocks x y
  witness : KuuNativeOneStep source target

/-- The proof carrier is packaged without changing or erasing
its actual index or constructor. -/
def KuuNativeOneStep.toPacket
    {x y : A} {p q : KuuNativeBlocks x y}
    (h : KuuNativeOneStep p q) :
    KuuNativeF41StepPacket (x := x) (y := y) :=
  ⟨p, q, h⟩

/-- Every ordinary category functor transports the ENTIRE packet,
including both endpoints and the corresponding proof. -/
def KuuNativeF41StepPacket.map
    {B : Type*} [Category B] (F : A ⥤ B)
    {x y : A} (s : KuuNativeF41StepPacket (x := x) (y := y)) :
    KuuNativeF41StepPacket (x := F.obj x) (y := F.obj y) :=
  ⟨s.source.map F, s.target.map F, s.witness.map F⟩

/-- Dependent congruence: if BOTH endpoint Blocks, the original
Type-valued primitive proof, and the actual appended path match,
the proof-valued right-context operation matches heterogeneously.

This is *not* proof irrelevance. The primitive witness itself is
explicitly compared as HEq and not inferred from its endpoints. -/
theorem KuuNativeOneStep.whisker_heq_of_heq
    {x y z : A}
    {p q p' q' : KuuNativeBlocks x y}
    (h : KuuNativeOneStep p q)
    (h' : KuuNativeOneStep p' q')
    (hp : p = p') (hq : q = q')
    (hh : HEq h h')
    {t t' : KuuNativePath y z} (ht : t = t') :
    HEq (KuuNativeOneStep.whisker h t)
      (KuuNativeOneStep.whisker h' t') := by
  cases hp
  cases hq
  have he : h = h' := eq_of_heq hh
  cases he
  cases ht
  rfl

/-- The corresponding dependent packet can be extended by a
genuine native path without erasing its saved primitive proof. -/
def KuuNativeF41StepPacket.whisker
    {x y z : A}
    (s : KuuNativeF41StepPacket (x := x) (y := y))
    (t : KuuNativePath y z) :
    KuuNativeF41StepPacket (x := x) (y := z) :=
  ⟨.snoc s.source t, .snoc s.target t,
    KuuNativeOneStep.whisker s.witness t⟩

/-- The original native functor transport on a whiskered F41
step has an exact constructor-shaped representative. The target is
heterogeneous because source/target Blocks are dependent indices
and map uses explicit Eq.mpr transports. -/
theorem KuuNativeOneStep.map_whisker_heq
    {B : Type*} [Category B] (F : A ⥤ B)
    {x y z : A} {p q : KuuNativeBlocks x y}
    (h : KuuNativeOneStep p q) (t : KuuNativePath y z) :
    HEq ((KuuNativeOneStep.whisker h t).map F)
      (KuuNativeOneStep.whisker (h.map F) (t.map F)) := by
  simp [KuuNativeOneStep.map]

#print axioms KuuNativeOneStep.whisker_heq_of_heq
#print axioms KuuNativeOneStep.map_whisker_heq
#print axioms KuuNativeOneStep.toPacket
#print axioms KuuNativeF41StepPacket.map
#print axioms KuuNativeF41StepPacket.whisker
end
end Kuu.F112.Physical
