import KUOS.DependentOriginationCoherentBiadjunctionActualLiftFiniteRefinementTracesV5_139

namespace KUOS.DependentOriginationCoherentBiadjunctionFunctorialPrimitiveRefinementV5_140

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRefinementTracesV5_139
open KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135

set_option autoImplicit false
noncomputable section

/-!
# F43-A / v5.140: ACTUAL functorial transport of primitive refinement steps

F42 proved that every finite refinement preserves the value of a
functor. This result is STRONGER at the typed proof level: it sends
EACH original F42 OneStep generator to an actual OneStep of the mapped
F40 block presentations, and sends an n-step derivation to an n-step
derivation without changing the precise primitive step count.

The original split generator needs the genuine F38 functorial equation
mapPath_append; it is not justified by treating a pseudofunctor as
strict. Original empty blocks and arbitrary right whiskering remain.

The construction applies to the ORIGINAL F19 chosen right-mate functor
and actual F28 quotient functors, not to the unrelated F26 chain type.
-/

namespace Grid

open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRefinementTracesV5_139.Grid
open KUOS.DependentOriginationCoherentBiadjunctionConstructiveRefinementV5_138.Grid

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Map a SINGLE genuine F42 primitive refinement operation by an
arbitrary honest functor, preserving its primitive status, including
the nontrivial mapping of a split q.append r. -/
theorem oneStep_mapBlocks (H : D ⥤ E)
    {x y : D} {p q : Blocks x y} (h : OneStep p q) :
    OneStep (mapBlocks H p) (mapBlocks H q) := by
  induction h with
  | split p q r =>
      simpa only [mapBlocks,
        KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135.Finite.mapPath_append]
        using (OneStep.split (mapBlocks H p)
          (KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135.Finite.mapPath H q)
          (KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135.Finite.mapPath H r))
  | insertNil p =>
      simpa only [mapBlocks,
        KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135.Finite.mapPath]
        using (OneStep.insertNil (mapBlocks H p))
  | whisker h t ih =>
      simpa only [mapBlocks] using
        (OneStep.whisker ih
          (KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135.Finite.mapPath H t))

/-- The SPLIT of an original F40 block remains a REAL primitive split
after functor transport; no postulated equality of mapped composites. -/
theorem oneStep_map_split (H : D ⥤ E)
    {w x y z : D}
    (p : Blocks w x) (q : Chain.Path x y) (r : Chain.Path y z) :
    OneStep
      (mapBlocks H (.snoc p (q.append r)))
      (mapBlocks H (.snoc (.snoc p q) r)) :=
  oneStep_mapBlocks H (OneStep.split p q r)

/-- Inserting an EMPTY original F40 block transports as an actual
empty-block primitive refinement and does not create a new arrow. -/
theorem oneStep_map_insertNil (H : D ⥤ E)
    {x y : D} (p : Blocks x y) :
    OneStep (mapBlocks H p)
      (mapBlocks H (.snoc p (Chain.Path.nil y))) :=
  oneStep_mapBlocks H (OneStep.insertNil p)

/-- Arbitrary original right-context whiskering is respected as a
primitive relation after functorial transportation. -/
theorem oneStep_map_whisker (H : D ⥤ E)
    {x y z : D} {p q : Blocks x y}
    (h : OneStep p q) (t : Chain.Path y z) :
    OneStep (mapBlocks H (.snoc p t))
      (mapBlocks H (.snoc q t)) :=
  oneStep_mapBlocks H (OneStep.whisker h t)

/-- Crucially, the mapped witness retains EXACTLY the same original
finite natural-number depth n, not just an existential count. -/
theorem trace_mapBlocks (H : D ⥤ E)
    {x y : D} {n : Nat} {p q : Blocks x y}
    (h : Trace n p q) :
    Trace n (mapBlocks H p) (mapBlocks H q) := by
  induction h with
  | refl p =>
      exact Trace.refl (mapBlocks H p)
  | snoc h step ih =>
      exact Trace.snoc ih (oneStep_mapBlocks H step)

/-- An arbitrary original F41 constructive refinement is
functorially preserved as a refinement WITNESS, not merely as
equality of the final morphisms. -/
theorem refines_mapBlocks (H : D ⥤ E)
    {x y : D} {p q : Blocks x y} (h : Refines p q) :
    Refines (mapBlocks H p) (mapBlocks H q) := by
  rcases Refines.exists_trace h with ⟨n, hn⟩
  exact Trace.toRefines (trace_mapBlocks H hn)

/-- Consequence: mapping an EXACT n-step refinement by a functor
preserves the original categorical evaluation equality. -/
theorem trace_mapBlocks_composite_eq (H : D ⥤ E)
    {x y : D} {n : Nat} {p q : Blocks x y}
    (h : Trace n p q) :
    (mapBlocks H p).composite = (mapBlocks H q).composite :=
  Trace.composite_eq (trace_mapBlocks H h)

#print axioms oneStep_mapBlocks
#print axioms oneStep_map_split
#print axioms oneStep_map_insertNil
#print axioms oneStep_map_whisker
#print axioms trace_mapBlocks
#print axioms refines_mapBlocks
#print axioms trace_mapBlocks_composite_eq

end Grid
end

end KUOS.DependentOriginationCoherentBiadjunctionFunctorialPrimitiveRefinementV5_140
