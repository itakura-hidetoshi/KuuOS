import Kuu.F112.PolygonNativeF41FunctorCompositionRoots

/-!
# F112-E7Q5-F4-O2-D3 — composition for ALL Type-valued F41 primitives

D2 proves genuine primitive split / insertNil composition in HEq.
The original functor map has a dependent cast in the whisker branch,
so we first transport the mapped actual whisker proof through G
using the proven source/target F40 Block equalities. We then compose
the two genuine map_whisker_heq witnesses with dependent whisker
congruence. Induction proves arbitrary finite whisker depth.

This is actual Type-valued proof-term coherence, not a Prop erasure
or equality of categorical composites. No historical KUOS imports.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uA vA uB vB uC vC
variable {A : Type uA} [Category.{vA} A]
variable {B : Type uB} [Category.{vB} B]
variable {C : Type uC} [Category.{vC} C]

/-- The mapped genuine whisker source proof and the whisker of the
mapped Type-valued primitive become HEq after mapping through G,
even though original F41.map inserts dependent Eq.mpr transports. -/
theorem KuuNativeOneStep.map_map_whisker_heq
    (F : A ⥤ B) (G : B ⥤ C)
    {x y z : A} {p q : KuuNativeBlocks x y}
    (h : KuuNativeOneStep p q) (t : KuuNativePath y z) :
    HEq (((KuuNativeOneStep.whisker h t).map F).map G)
      ((KuuNativeOneStep.whisker (h.map F) (t.map F)).map G) := by
  have hp :
      (KuuNativeBlocks.snoc p t).map F =
        KuuNativeBlocks.snoc (p.map F) (t.map F) := by
    simp only [KuuNativeBlocks.map]
  have hq :
      (KuuNativeBlocks.snoc q t).map F =
        KuuNativeBlocks.snoc (q.map F) (t.map F) := by
    simp only [KuuNativeBlocks.map]
  exact KuuNativeOneStep.map_heq_of_heq G
    ((KuuNativeOneStep.whisker h t).map F)
    (KuuNativeOneStep.whisker (h.map F) (t.map F))
    hp hq (KuuNativeOneStep.map_whisker_heq F h t)

/-- The composition law on any whisker follows from the exact
dependent source and target equalities for the recursively mapped
Type-valued proof, NOT from assuming any proof irrelevance. -/
theorem KuuNativeOneStep.map_comp_whisker_heq
    (F : A ⥤ B) (G : B ⥤ C)
    {x y z : A} {p q : KuuNativeBlocks x y}
    (h : KuuNativeOneStep p q) (t : KuuNativePath y z)
    (ih : HEq (h.map (F ⋙ G)) ((h.map F).map G)) :
    HEq ((KuuNativeOneStep.whisker h t).map (F ⋙ G))
      (((KuuNativeOneStep.whisker h t).map F).map G) := by
  have hbridge :
      HEq (KuuNativeOneStep.whisker (h.map (F ⋙ G))
          (t.map (F ⋙ G)))
        (KuuNativeOneStep.whisker ((h.map F).map G)
          ((t.map F).map G)) :=
    KuuNativeOneStep.whisker_heq_of_heq
      (h.map (F ⋙ G)) ((h.map F).map G)
      (KuuNativeBlocks.map_comp F G p)
      (KuuNativeBlocks.map_comp F G q)
      ih (KuuNativePath.map_comp F G t)
  exact
    (KuuNativeOneStep.map_whisker_heq (F ⋙ G) h t).trans
      (hbridge.trans
        ((KuuNativeOneStep.map_whisker_heq G (h.map F) (t.map F)).symm.trans
          (KuuNativeOneStep.map_map_whisker_heq F G h t).symm))

/-- Every genuinely proof-relevant F41 primitive, with arbitrarily
nested right-whisker contexts, has strictly coherent arbitrary
functor composition UP TO the actual dependent-typed HEq. -/
theorem KuuNativeOneStep.map_comp_heq
    (F : A ⥤ B) (G : B ⥤ C)
    {x y : A} {p q : KuuNativeBlocks x y}
    (h : KuuNativeOneStep p q) :
    HEq (h.map (F ⋙ G)) ((h.map F).map G) := by
  induction h with
  | split p q r =>
      exact KuuNativeOneStep.map_comp_split_heq F G p q r
  | insertNil p =>
      exact KuuNativeOneStep.map_comp_insertNil_heq F G p
  | whisker h t ih =>
      exact KuuNativeOneStep.map_comp_whisker_heq F G h t ih

#print axioms KuuNativeOneStep.map_map_whisker_heq
#print axioms KuuNativeOneStep.map_comp_whisker_heq
#print axioms KuuNativeOneStep.map_comp_heq
end
end Kuu.F112.Physical
