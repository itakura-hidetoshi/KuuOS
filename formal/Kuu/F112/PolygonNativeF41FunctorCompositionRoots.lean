import Kuu.F112.PolygonNativeF41FunctorCompositionPrimitives

/-!
# F112-E7Q5-F4-O2-D2 — composition on genuine primitive F41 roots

Compare the actual proof-relevant split and insertNil witnesses under
F ⋙ G versus successive F and G. All Eq.mpr transports introduced by
the original F41 map are retained and compared heterogeneously.

No proof erasure or new coherence axiom is used.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uA vA uB vB uC vC
variable {A : Type uA} [Category.{vA} A]
variable {B : Type uB} [Category.{vB} B]
variable {C : Type uC} [Category.{vC} C]

/-- The split primitive has a genuine two-functor composition law,
including the intermediate original native-path concatenation cast. -/
theorem KuuNativeOneStep.map_comp_split_heq
    (F : A ⥤ B) (G : B ⥤ C)
    {w x y z : A}
    (p : KuuNativeBlocks w x)
    (q : KuuNativePath x y)
    (r : KuuNativePath y z) :
    HEq ((KuuNativeOneStep.split p q r).map (F ⋙ G))
      (((KuuNativeOneStep.split p q r).map F).map G) := by
  have hp :
      (KuuNativeBlocks.snoc p (q.append r)).map F =
        KuuNativeBlocks.snoc (p.map F)
          ((q.map F).append (r.map F)) := by
    simp only [KuuNativeBlocks.map, KuuNativePath.map_append]
  have hq :
      (KuuNativeBlocks.snoc (KuuNativeBlocks.snoc p q) r).map F =
        KuuNativeBlocks.snoc
          (KuuNativeBlocks.snoc (p.map F) (q.map F)) (r.map F) := by
    simp only [KuuNativeBlocks.map]
  have hmap :
      HEq (((KuuNativeOneStep.split p q r).map F).map G)
        ((KuuNativeOneStep.split
          (p.map F) (q.map F) (r.map F)).map G) :=
    KuuNativeOneStep.map_heq_of_heq G
      ((KuuNativeOneStep.split p q r).map F)
      (KuuNativeOneStep.split (p.map F) (q.map F) (r.map F))
      hp hq (KuuNativeOneStep.map_split_heq F p q r)
  exact
    (KuuNativeOneStep.map_split_heq (F ⋙ G) p q r).trans
      ((KuuNativeOneStep.split_heq_of_eq
        (KuuNativeBlocks.map_comp F G p)
        (KuuNativePath.map_comp F G q)
        (KuuNativePath.map_comp F G r)).trans
          ((KuuNativeOneStep.map_split_heq G
            (p.map F) (q.map F) (r.map F)).symm.trans
              hmap.symm))

/-- Insertion of a genuinely empty native block is preserved under
composition of category functors at the actual Type-valued proof. -/
theorem KuuNativeOneStep.map_comp_insertNil_heq
    (F : A ⥤ B) (G : B ⥤ C)
    {x y : A} (p : KuuNativeBlocks x y) :
    HEq ((KuuNativeOneStep.insertNil p).map (F ⋙ G))
      (((KuuNativeOneStep.insertNil p).map F).map G) := by
  have hmap :
      HEq (((KuuNativeOneStep.insertNil p).map F).map G)
        ((KuuNativeOneStep.insertNil (p.map F)).map G) :=
    KuuNativeOneStep.map_heq_of_heq G
      ((KuuNativeOneStep.insertNil p).map F)
      (KuuNativeOneStep.insertNil (p.map F))
      (by rfl)
      (by simp only [KuuNativeBlocks.map, KuuNativePath.map])
      (KuuNativeOneStep.map_insertNil_heq F p)
  exact
    (KuuNativeOneStep.map_insertNil_heq (F ⋙ G) p).trans
      ((KuuNativeOneStep.insertNil_heq_of_eq
        (KuuNativeBlocks.map_comp F G p)).trans
          ((KuuNativeOneStep.map_insertNil_heq G (p.map F)).symm.trans
            hmap.symm))

#print axioms KuuNativeOneStep.map_comp_split_heq
#print axioms KuuNativeOneStep.map_comp_insertNil_heq
end
end Kuu.F112.Physical
