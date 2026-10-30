import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeF55FullCountability
import Kuu.F112.PolygonNativeF55P94DK5TypedStructuralSeam

/-!
# F112-P94D3GK — all fourteen actual F54 structural seam constructors

The independent NativeF54StructuralSeam has fourteen proof-relevant
constructors on genuine two-category F54 DepthRotationRoute proofs.
It is not identical to the nine-constructor original F55 PresentedCell,
the distinct P92B associator-naturality extension, or the extended F55
StructuralComparison.

We record a faithful finite syntax retaining every actual original
Type-valued F54 route, D/E block, F45 tree, both Nat depths and every
intermediate typed proof. A countable code by itself does NOT prove
countability of the full original seam Type; an exact dependent partial
decoder and strict left inverse are further independent obligations.

Append-only; strict Kuu primary; 107 public roots; no Gray or axioms.
Pinned Lean v4.30.0-rc2, mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE u v

/-- Every original fourteen-constructor shape, with original
proof-typed route/tree atoms rather than scalar observations. -/
inductive NativeGKStructuralPlainSyntax
    (Route : Type u) (Tree : Type v) : Type (max u v) where
  | refl (route : Route)
  | symm (w : NativeGKStructuralPlainSyntax Route Tree)
  | trans (w v : NativeGKStructuralPlainSyntax Route Tree)
  | reassoc (u v w : Route)
  | leftUnit (route : Route)
  | rightUnit (route : Route)
  | precompose (route : Route) (w : NativeGKStructuralPlainSyntax Route Tree)
  | postcompose (w : NativeGKStructuralPlainSyntax Route Tree) (route : Route)
  | leftContextTrans (u v : Route) (later : Tree)
  | rightContextTrans (earlier : Tree) (u v : Route)
  | leftContextUnit (earlier later : Tree)
  | rightContextUnit (earlier later : Tree)
  | leftContextCongruence (w : NativeGKStructuralPlainSyntax Route Tree)
      (later : Tree)
  | rightContextCongruence (earlier : Tree)
      (w : NativeGKStructuralPlainSyntax Route Tree)
  deriving Countable

/-- Genuinely original Type-valued source alphabets on both
independent original D/E categories. -/
abbrev NativeGKStructuralCode
    (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    Type (max (max uD uE) (max vD vE)) :=
  NativeGKStructuralPlainSyntax
    (NativeGIOriginalDepthTotal p D E)
    (NativeGHOriginalF45Total p D E)

/-- Constructor-preserving recursive encoding of every actual F54
structural seam: no original F45 or F54 Type proof is dropped. -/
def nativeGKEncodeStructural
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (w : NativeF54StructuralSeam p r s) :
    NativeGKStructuralCode p D E :=
  match w with
  | .refl route => .refl (nativeGJ2PackRoute route)
  | .symm inner => .symm (nativeGKEncodeStructural inner)
  | .trans inner outer =>
      .trans (nativeGKEncodeStructural inner) (nativeGKEncodeStructural outer)
  | .reassoc u v z =>
      .reassoc (nativeGJ2PackRoute u)
        (nativeGJ2PackRoute v) (nativeGJ2PackRoute z)
  | .leftUnit route => .leftUnit (nativeGJ2PackRoute route)
  | .rightUnit route => .rightUnit (nativeGJ2PackRoute route)
  | .precompose route inner =>
      .precompose (nativeGJ2PackRoute route) (nativeGKEncodeStructural inner)
  | .postcompose inner route =>
      .postcompose (nativeGKEncodeStructural inner) (nativeGJ2PackRoute route)
  | .leftContextTrans u v later =>
      .leftContextTrans (nativeGJ2PackRoute u) (nativeGJ2PackRoute v)
        (nativeGIPackTree later)
  | .rightContextTrans earlier u v =>
      .rightContextTrans (nativeGIPackTree earlier)
        (nativeGJ2PackRoute u) (nativeGJ2PackRoute v)
  | .leftContextUnit earlier later =>
      .leftContextUnit (nativeGIPackTree earlier) (nativeGIPackTree later)
  | .rightContextUnit earlier later =>
      .rightContextUnit (nativeGIPackTree earlier) (nativeGIPackTree later)
  | .leftContextCongruence inner later =>
      .leftContextCongruence
        (nativeGKEncodeStructural inner) (nativeGIPackTree later)
  | .rightContextCongruence earlier inner =>
      .rightContextCongruence
        (nativeGIPackTree earlier) (nativeGKEncodeStructural inner)

/-- The full fourteen-constructor code is Countable under
explicit D/E object and EACH categorical Hom fiber Countable. -/
theorem nativeGKStructuralCode_countable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    Countable (NativeGKStructuralCode p D E) := by
  letI : Countable (NativeGIOriginalDepthTotal p D E) :=
    nativeGIOriginalDepthTotal_countable hobjD hhomD hobjE hhomE
  letI : Countable (NativeGHOriginalF45Total p D E) :=
    nativeGHOriginalF45Total_countable hobjD hhomD hobjE hhomE
  infer_instance

/-- Physical C60 with both original axes Site: all needed
object/Hom Countable assumptions are discharged by GE. -/
theorem nativeGKPhysicalStructuralCode_countable (p : Polygon) :
    Countable (NativeGKStructuralCode p Site Site) :=
  nativeGKStructuralCode_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable

theorem nativeGKPhysicalAllPolygonStructuralCode_countable :
    Countable (Σ p : Polygon, NativeGKStructuralCode p Site Site) := by
  letI : Countable Polygon := nativeC60GEPhysicalPolygon_countable
  letI : ∀ p : Polygon, Countable (NativeGKStructuralCode p Site Site) :=
    nativeGKPhysicalStructuralCode_countable
  infer_instance

#print axioms nativeGKStructuralCode_countable
#print axioms nativeGKPhysicalStructuralCode_countable
#print axioms nativeGKPhysicalAllPolygonStructuralCode_countable

end
end Kuu.F112.Physical
