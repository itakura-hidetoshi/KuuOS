import Kuu.F112.PolygonNativeF54FunctorDepthRoutes
import Kuu.F112.PolygonNativeF55Shadow

/-!
# F112-E7Q5-F1: genuine independent F55 proof-relevant functor comparison

Continue the exact typed F36/F40/F41/F45/F54 source-functor actions
of E7Q5-C/D/E1/E2, rather than equating old and new F55 from their
charges or evaluation alone.

The independent F55 PresentedCell has NINE raw Type-valued
constructors. This module constructs a source action of two
independent ordinary functors on each such raw higher proof tree,
preserving all original F54 depth-route boundaries, the two
independent categorical Blocks axes, local 5/6 C60 sectors, and
the unquotiented proof trees.

Additional results: all nine raw constructor tags and all three
chosen native shadow coordinates are invariant under this typed
transport. Neither old Gray nor frozen KUOS.* is imported. No
historical F55 source equivalence or old braided origin is presumed.
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

/-- Interpret all genuine nine constructors in the raw typed F55
source transported along the two independently selected categorical
functors, not in a quotient of shadow charges. -/
def KuuNativeF45Tree.DepthRotationRoute.PresentedCell.mapAxes
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell p
      (r.mapAxes F G) (s.mapAxes F G) := by
  induction cell with
  | ident route =>
      exact .ident (route.mapAxes F G)
  | pentagon t₁ t₂ t₃ t₄ =>
      simpa only [KuuNativeF45Tree.DepthRotationRoute.mapAxes,
        KuuNativeF45Tree.mapAxes] using
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.pentagon
          (t₁.mapAxes F G) (t₂.mapAxes F G)
          (t₃.mapAxes F G) (t₄.mapAxes F G))
  | disjointSquare left right =>
      simpa only [KuuNativeF45Tree.DepthRotationRoute.mapAxes,
        KuuNativeF45Tree.mapAxes] using
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.disjointSquare
          (left.mapAxes F G) (right.mapAxes F G))
  | symm cell ih =>
      exact .symm ih
  | trans left right ihLeft ihRight =>
      exact .trans ihLeft ihRight
  | leftContext cell later ih =>
      simpa only [KuuNativeF45Tree.DepthRotationRoute.mapAxes,
        KuuNativeF45Tree.mapAxes] using
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.leftContext
          ih (later.mapAxes F G))
  | rightContext earlier cell ih =>
      simpa only [KuuNativeF45Tree.DepthRotationRoute.mapAxes,
        KuuNativeF45Tree.mapAxes] using
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.rightContext
          (earlier.mapAxes F G) ih)
  | precompose prior cell ih =>
      exact .precompose (prior.mapAxes F G) ih
  | postcompose cell suffix ih =>
      exact .postcompose ih (suffix.mapAxes F G)

/-- Exact source-level shape tags (ident, two primitive generators,
inverse, paste, both contexts and pre/post whiskerings) survive
arbitrary source-category functors. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.shapeTag_mapAxes
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    (cell.mapAxes F G).shapeTag = cell.shapeTag := by
  cases cell <;> rfl

/-- Full chosen native 3-coordinate shadow is invariant on the
ACTUAL raw F55 3-source under any two independently chosen functors.
In particular, no odd phase is inferred from signed charges:
the original chosen odd-phase calibration is simply preserved. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.nativeShadow_mapAxes
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    (cell.mapAxes F G).nativeShadow = cell.nativeShadow := by
  induction cell with
  | ident _ => rfl
  | pentagon _ _ _ _ => rfl
  | disjointSquare _ _ => rfl
  | symm c ih =>
      exact congrArg (fun z : KuuNativeF55Shadow => -z) ih
  | trans c d ihc ihd =>
      exact congrArg₂ (fun z w : KuuNativeF55Shadow => z + w) ihc ihd
  | leftContext c later ih => exact ih
  | rightContext earlier c ih => exact ih
  | precompose prior c ih => exact ih
  | postcompose c suffix ih => exact ih

/-- Both independent signed pentagon and square charges are preserved
WITHOUT collapsing the F55 raw source proof terms to those charges. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.charge_mapAxes
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    (cell.mapAxes F G).nativeShadow.1 = cell.nativeShadow.1 :=
  congrArg Prod.fst (cell.nativeShadow_mapAxes F G)

/-- A separately chosen odd-phase coordinate is transported
unchanged for all nine raw constructors, not derived from charges. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.phase_mapAxes
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    (cell.mapAxes F G).nativeShadow.2 = cell.nativeShadow.2 :=
  congrArg Prod.snd (cell.nativeShadow_mapAxes F G)

#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.mapAxes
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.shapeTag_mapAxes
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.nativeShadow_mapAxes
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.charge_mapAxes
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.phase_mapAxes
end
end Kuu.F112.Physical
