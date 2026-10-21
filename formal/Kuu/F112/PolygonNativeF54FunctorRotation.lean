import Kuu.F112.PolygonNativeF54FunctorChains

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

/-!
The existing E7Q5-E1 module PolygonNativeF54FunctorChains already
proves LocalRotation.mapAxes and LocalRotation.mapAxes_sectors on
the full original-shaped, two-axis dependent source. P54 must reuse
those canonical Lean constants rather than independently redeclare
the same fully-qualified names in separate import branches.

The following two theorems are P54's genuinely additional results:
preservation of complete physical leaves and both primitive axes.
-/

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
