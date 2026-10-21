import Kuu.F112.PolygonNativeF55ContextSquareComparisonP68

/-!
F112-P69: proof-relevant higher-Hom transport boundary.

A quotient of F54 route objects does not canonically choose source
representatives. We retain actual F55 raw evidence and its typed
endpoints in a sigma package, together with the exact class equalities.
This is a source presentation of arrows OVER quotient classes, not
yet a category on those classes: composition requires witness choices
and compatibility beyond the data proved here.
No new axioms, sorry, admit, or Gray.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Original proof-relevant higher arrows, with explicitly chosen
source representatives of two F54 comparison classes. -/
structure NativeF55HigherArrowOverClasses
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (source target : NativeF55ContextSquareRouteClasses first last) where
  before : KuuNativeF45Tree.DepthRotationRoute p first last
  after : KuuNativeF45Tree.DepthRotationRoute p first last
  source_eq : nativeF55ContextSquareRouteClass first last before = source
  target_eq : nativeF55ContextSquareRouteClass first last after = target
  raw : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p before after

/-- Every actual original raw 3-cell has an explicit representative
over its two quotient F54 classes. -/
def nativeF55HigherArrowOverClasses_ofRaw
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (raw : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) :
    NativeF55HigherArrowOverClasses first last
      (nativeF55ContextSquareRouteClass first last u)
      (nativeF55ContextSquareRouteClass first last v) where
  before := u
  after := v
  source_eq := rfl
  target_eq := rfl
  raw := raw

/-- The package retains its original proof history exactly. -/
theorem nativeF55HigherArrowOverClasses_ofRaw_history
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (raw : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) :
    (nativeF55HigherArrowOverClasses_ofRaw first last raw).raw = raw := rfl

/-- An equality of quotient classes yields existence of an actual
square-only source witness, but does not canonically select it. -/
theorem nativeF55ClassEquality_has_squareOnlyWitness
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last)
    (h : nativeF55ContextSquareRouteClass first last u =
      nativeF55ContextSquareRouteClass first last v) :
    Nonempty (NativeF55SquareOnlyCell (p := p) (u := u) (v := v)) :=
  (nativeF55ContextSquareRouteClass_eq_iff first last u v).mp h

/-- The genuine C60 odd exchange square has a proof-relevant
higher-arrow package over the equal comparison class. -/
def northHexagonNativeHigherArrowOverClasses :=
  nativeF55HigherArrowOverClasses_ofRaw _ _
    northHexagonNativeF55SquareCell

/-- The underlying physical C60 source witness is not erased by
packaging it over quotient F54 route classes. -/
theorem northHexagonNativeHigherArrowOverClasses_history :
    northHexagonNativeHigherArrowOverClasses.raw =
      northHexagonNativeF55SquareCell := rfl

#print axioms NativeF55HigherArrowOverClasses
#print axioms nativeF55HigherArrowOverClasses_ofRaw
#print axioms nativeF55HigherArrowOverClasses_ofRaw_history
#print axioms nativeF55ClassEquality_has_squareOnlyWitness
#print axioms northHexagonNativeHigherArrowOverClasses
#print axioms northHexagonNativeHigherArrowOverClasses_history

end
end Kuu.F112.Physical
