import Kuu.F112.PolygonNativeF40FunctorComparison
import Kuu.F112.PolygonNativeF54Rotation

/-!
# F112-E7Q5-D — independent two-category F45 typed functor comparison

Having proved positive F36/F40 map and exact F41/AxisTrace
transport in E7Q5-C, transport an ACTUAL double-category F45
bracket tree along TWO separately supplied functors.

The source retains:
* BOTH independent Type-valued primitive histories, at exact n/m;
* ALL intermediate original-shaped categorical Blocks;
* the F45 leaf execution-order constructor;
* EVERY actual 5/6-sided physical C60 boundary sector;
* arbitrary full binary parentheses, with typed intermediate Blocks.

This is positive source construction, not a graded interpretation.
We prove exact preservation of ordered physical sectors, original
double-Nat depth physical erasure, and each axis's categorical
evaluation. We also prove that F54's explicit double-Nat casts
commute with this two-category transport.

This is not a theorem asserting equivalence with frozen historical
F19/F28/F45/F54 or restoring original Gray/old KUOS imports.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uA vA uB vB uA₂ vA₂ uB₂ vB₂
variable {A : Type uA} [Category.{vA} A]
variable {B : Type uB} [Category.{vB} B]
variable {A₂ : Type uA₂} [Category.{vA₂} A₂]
variable {B₂ : Type uB₂} [Category.{vB₂} B₂]

/-- Positively transport both old-F19/F28-SHAPED independent axes
along genuine categorical functors. Unlike a composite-Hom erasure,
all raw F41 proof trees, intermediate block boundaries, execution
orders and physical C60 sector leaves are retained. -/
def KuuNativeF45Tree.mapAxes (F : A ⥤ A₂) (G : B ⥤ B₂)
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    KuuNativeF45Tree p n m
      (ma.map F) (pa.map G) (mb.map F) (pb.map G) := by
  induction tree with
  | refl i ma pa =>
      exact .refl i (ma.map F) (pa.map G)
  | leaf i order firstAxis secondAxis =>
      exact .leaf i order (firstAxis.map F) (secondAxis.map G)
  | node first second ihFirst ihSecond =>
      exact .node ihFirst ihSecond

/-- No physical sector is inferred, forgotten or changed by either
functor: preserve the COMPLETE original ordered list of C60 leaves. -/
theorem KuuNativeF45Tree.sectors_mapAxes
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    (tree.mapAxes F G).sectors = tree.sectors := by
  induction tree with
  | refl i ma pa => rfl
  | leaf i order firstAxis secondAxis => rfl
  | node first second ihFirst ihSecond =>
      change (first.mapAxes F G).sectors ++
          (second.mapAxes F G).sectors =
        first.sectors ++ second.sectors
      rw [ihFirst, ihSecond]

/-- BOTH exact Nat depths and the WHOLE true physical polygon
bracketing commute with typed functor transportation, not merely
the numeric list of leaves. -/
theorem KuuNativeF45Tree.erasePhysical_mapAxes
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    (tree.mapAxes F G).erasePhysical = tree.erasePhysical := by
  induction tree with
  | refl i ma pa => rfl
  | leaf i order firstAxis secondAxis => rfl
  | node first second ihFirst ihSecond =>
      change PolygonDepthTree.node
          (first.mapAxes F G).erasePhysical
          (second.mapAxes F G).erasePhysical =
        PolygonDepthTree.node first.erasePhysical second.erasePhysical
      rw [ihFirst, ihSecond]

/-- Every mapped physical F45 source preserves BOTH original
categorical evaluations, obtained by independently transporting
actual native primitive source witnesses rather than identifying
different histories by a terminal Hom equality. -/
theorem KuuNativeF45Tree.mapAxes_evaluations
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    (ma.map F).composite = (mb.map F).composite ∧
    (pa.map G).composite = (pb.map G).composite := by
  constructor
  · rw [KuuNativeBlocks.composite_map, KuuNativeBlocks.composite_map]
    exact congrArg (fun h : a ⟶ b => F.map h)
      tree.axis_composite_preserved.1
  · rw [KuuNativeBlocks.composite_map, KuuNativeBlocks.composite_map]
    exact congrArg (fun h : x ⟶ y => G.map h)
      tree.axis_composite_preserved.2

/-- Original-shaped F54 transport of the TWO independent Nat
depth equalities is compatible with genuine two-category functor
transport. No raw rotation equivalence has been asserted. -/
theorem KuuNativeF45Tree.mapAxes_castDepths
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (hn : n = n') (hm : m = m')
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    (KuuNativeF45Tree.castDepths hn hm tree).mapAxes F G =
      KuuNativeF45Tree.castDepths hn hm (tree.mapAxes F G) := by
  cases hn
  cases hm
  rfl

/-- The actual north C60 pentagon has two genuinely independent
source histories; transport to any two categories separately. -/
theorem northNativeF45TwoStages_functor_physical
    (F : Site ⥤ A₂) (G : Site ⥤ B₂) :
    (northNativeF45TwoStages.mapAxes F G).erasePhysical =
      northNativeF45TwoStages.erasePhysical :=
  KuuNativeF45Tree.erasePhysical_mapAxes F G northNativeF45TwoStages

#print axioms KuuNativeF45Tree.mapAxes
#print axioms KuuNativeF45Tree.sectors_mapAxes
#print axioms KuuNativeF45Tree.erasePhysical_mapAxes
#print axioms KuuNativeF45Tree.mapAxes_evaluations
#print axioms KuuNativeF45Tree.mapAxes_castDepths
#print axioms northNativeF45TwoStages_functor_physical

end
end Kuu.F112.Physical
