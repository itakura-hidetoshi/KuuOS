import Kuu.F112.PolygonNativeF45FunctorAxes

/-!
# F112-P54 — positive functorial transport of independent F54 rotations

The independently constructed, Type-valued F54 source has three actual
rotation constructors: an associator with TWO separate Nat casts and
both left/right contexts. Unlike merely mapping its underlying trees,
this module maps the *typed rotation proof itself* along two genuinely
independent category functors, preserving its full original-shaped
F19/F28 Blocks and physical C60 sectors.

This is an independent positive presentation. It does not assert an
equivalence with the frozen historical original F54/F55 or reinstate
Gray into the Kuu foundation.
-/

namespace Kuu.F112.Physical
open CategoryTheory

set_option autoImplicit false
set_option warningAsError true
noncomputable section

universe uA vA uB vB uC vC uD vD
variable {A : Type uA} [Category.{vA} A]
variable {B : Type uB} [Category.{vB} B]
variable {C : Type uC} [Category.{vC} C]
variable {D : Type uD} [Category.{vD} D]

/-- Transport an entire genuinely typed F54-shaped associator,
including arbitrary left/right source contexts and both Nat-index
equality transports, along independently selected categorical axes.
The output is a *rotation witness*, never merely equality of erasures. -/
def KuuNativeF45Tree.LocalRotation.mapAxes
    (F : A ⥤ C) (G : B ⥤ D)
    {p : Polygon} {a b : A} {x y : B}
    {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (step : KuuNativeF45Tree.LocalRotation p before after) :
    KuuNativeF45Tree.LocalRotation p
      (before.mapAxes F G) (after.mapAxes F G) := by
  induction step with
  | assoc first second third =>
      rw [KuuNativeF45Tree.mapAxes_castDepths]
      exact KuuNativeF45Tree.LocalRotation.assoc
        (first.mapAxes F G) (second.mapAxes F G)
        (third.mapAxes F G)
  | leftContext step later ih =>
      simpa only [KuuNativeF45Tree.mapAxes] using
        (KuuNativeF45Tree.LocalRotation.leftContext ih (later.mapAxes F G))
  | rightContext earlier step ih =>
      simpa only [KuuNativeF45Tree.mapAxes] using
        (KuuNativeF45Tree.LocalRotation.rightContext (earlier.mapAxes F G) ih)

/-- The resulting typed F54 rotation retains both exact boundaries
of the complete ORDERED physical C60 sector list, through arbitrary
independent functors on both original-shaped categorical axes. -/
theorem KuuNativeF45Tree.LocalRotation.mapAxes_sectors
    (F : A ⥤ C) (G : B ⥤ D)
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (step : KuuNativeF45Tree.LocalRotation p before after) :
    (before.mapAxes F G).sectors = (after.mapAxes F G).sectors := by
  calc
    (before.mapAxes F G).sectors = before.sectors :=
      KuuNativeF45Tree.sectors_mapAxes F G before
    _ = after.sectors := step.sectors_eq
    _ = (after.mapAxes F G).sectors :=
      (KuuNativeF45Tree.sectors_mapAxes F G after).symm

/-- The independent native F54 rotation is still real at the
complete C60 physical leaf carrier, even after both functor maps. -/
theorem KuuNativeF45Tree.LocalRotation.mapAxes_physical_leaves
    (F : A ⥤ C) (G : B ⥤ D)
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (step : KuuNativeF45Tree.LocalRotation p before after) :
    (before.mapAxes F G).erasePhysical.erase.leaves =
      (after.mapAxes F G).erasePhysical.erase.leaves :=
  (step.mapAxes F G).physical_leaves_eq

/-- Every newly transported F54 rotation is still an actual
source witness between TWO categorical history axes; in particular
both original full Blocks flatten invariants remain certified. -/
theorem KuuNativeF45Tree.LocalRotation.mapAxes_both_axes_flatten
    (F : A ⥤ C) (G : B ⥤ D)
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (step : KuuNativeF45Tree.LocalRotation p before after) :
    (ma.map F).flatten = (mb.map F).flatten ∧
      (pa.map G).flatten = (pb.map G).flatten :=
  (step.mapAxes F G).both_axes_flatten

#print axioms KuuNativeF45Tree.LocalRotation.mapAxes
#print axioms KuuNativeF45Tree.LocalRotation.mapAxes_sectors
#print axioms KuuNativeF45Tree.LocalRotation.mapAxes_physical_leaves
#print axioms KuuNativeF45Tree.LocalRotation.mapAxes_both_axes_flatten

end
end Kuu.F112.Physical
