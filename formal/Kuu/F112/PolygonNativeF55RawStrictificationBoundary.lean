import Kuu.F112.PolygonNativeF55HorizontalFunctoriality
import Mathlib.CategoryTheory.PathCategory.Basic
import Mathlib.Tactic

/-!
# F112-P58 — strictification boundary of independent raw F55 proof trees

The independently constructed nine-constructor, Type-valued F55
presentation is NOT silently equated with its chosen numerical shadow.
In particular, the designated raw identity and raw vertical constructor
do not satisfy the strict category axioms as equalities of raw trees.

We prove universal source-level obstructions (not just one special C60
pentagon), using an actual recursive count of constructors. The
association obstruction is witnessed by the *left branch* size, not by
the total size, which is invariant under reassociation.

Then we separately construct the Mathlib free path category on the
original typed raw-cell quiver: this is a legitimate strict **path
envelope**, with the native F54 routes as objects and actual raw F55
cells as *generating arrows*. Its ordinary categorical strictness comes
from paths, not from a forbidden claim that the original raw trees
already obey strict identities or interchange.

The map from this path envelope to the existing chosen full-shadow
quotient is explicitly functorial. This does not identify the raw
syntax with its shadow, prove a global strict 3-category, or establish
historical source equivalence. No imported historical or external
higher-category structure, no new axioms, no sorry/admit.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Actual number of constructors in a proof-relevant, independent
raw F55 tree, including units and pastings (none is erased). -/
def KuuNativeF45Tree.DepthRotationRoute.PresentedCell.nodeCount
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last} :
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s → Nat
  | .ident _ => 1
  | .pentagon _ _ _ _ => 1
  | .disjointSquare _ _ => 1
  | .symm c => c.nodeCount + 1
  | .trans c d => c.nodeCount + d.nodeCount + 1
  | .leftContext c _ => c.nodeCount + 1
  | .rightContext _ c => c.nodeCount + 1
  | .precompose _ c => c.nodeCount + 1
  | .postcompose c _ => c.nodeCount + 1

/-- Every source raw 3-cell, not merely the distinguished C60
pentagon, is different from itself followed by a *raw* unit. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ne_trans_ident
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    cell ≠ .trans cell (.ident s) := by
  intro h
  have hc := congrArg
    (fun t : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s =>
      t.nodeCount) h
  change cell.nodeCount = cell.nodeCount + (1 : Nat) + 1 at hc
  omega

/-- Likewise a raw left unit is *not* a source-term identity.
A strict identity requires a further, explicitly accounted relation. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ne_ident_trans
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    (.trans (.ident r) cell) ≠ cell := by
  intro h
  have hc := congrArg
    (fun t : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s =>
      t.nodeCount) h
  change (1 : Nat) + cell.nodeCount + 1 = cell.nodeCount at hc
  omega

/-- The size of the LEFT child of an outer vertical-composition
constructor. This can detect reassociation while total size cannot. -/
def KuuNativeF45Tree.DepthRotationRoute.PresentedCell.leftTransCount
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last} :
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s → Nat
  | .trans c _ => c.nodeCount
  | _ => 0

/-- Source-level vertical association fails as LITERAL equality
for any three composable raw cells: the two constructed trees have
different left-subtree sizes. No collapse by shadow is used. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ne_assoc_raw
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s t u : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p s t)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p t u) :
    (.trans (.trans f g) h) ≠ (.trans f (.trans g h)) := by
  intro heq
  have hc := congrArg
    (fun z : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r u =>
      z.leftTransCount) heq
  change f.nodeCount + g.nodeCount + 1 = f.nodeCount at hc
  omega

/-- New, separate vertices for the raw F55 quiver, keeping the exact
dependent F54 depth and endpoint types without inheriting the
previously selected numerical-shadow Hom structure. -/
structure NativeF55RawRouteVertex
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) where
  route : KuuNativeF45Tree.DepthRotationRoute p first last

/-- Actual raw F55 3-proof trees are arrows of a quiver, not yet
a category. Each one of the nine constructors survives as a term. -/
instance nativeF55RawRouteQuiver
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    Quiver (NativeF55RawRouteVertex first last) where
  Hom r s :=
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r.route s.route

/-- A distinct strict, freely generated path envelope.
It does NOT assert strict unit/association on the raw trees
themselves, and does NOT quotient by charge/phase. -/
abbrev NativeF55RawPathCategory
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :=
  CategoryTheory.Paths (NativeF55RawRouteVertex first last)

/-- Strict path extension to the earlier CHOSEN shadow quotient.
The quiver-to-category map sends each complete source raw witness
to its actual class; Mathlib extends it along free paths. -/
def nativeF55RawPathsToShadow
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    NativeF55RawPathCategory first last ⥤
      (KuuNativeF45Tree.DepthRotationRoute p first last) :=
  CategoryTheory.Paths.lift {
    obj := fun v => v.route
    map := fun {X Y} cell => nativeF55ThreeOf cell
  }

#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.nodeCount
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ne_trans_ident
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ne_ident_trans
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.leftTransCount
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ne_assoc_raw
#print axioms NativeF55RawRouteVertex
#print axioms nativeF55RawRouteQuiver
#print axioms NativeF55RawPathCategory
#print axioms nativeF55RawPathsToShadow

end
end Kuu.F112.Physical
