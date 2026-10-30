import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGKSeamTypedAtoms

/-!
# F112-P94D3GK2 — faithful dependent syntax for all fourteen
original F54 structural seam constructors

This tightens GK's first finite syntax by preserving the COMPLETE
original dependent composability of EVERY nonrecursive primitive:
three original F54 routes in reassoc, two routes plus a genuine
left/right F45 context in contextual composition, and a truly typed
pair of original F45 trees in context-unit generators.

The full typed source code is Countable under Countable D/E objects
and ALL original categorical Hom fibers. It does not conflate
original P92B, the separately presented nine-constructor F55 source,
or the structurally extended F55 comparison. Original seam total
Countable still requires a strict partial decoder and left inverse.

Append-only, 107 public roots, no Gray, no axioms, no sorry.
Lean v4.30.0-rc2/mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE u v w z t h

/-- Every one of the original fourteen constructors, without
changing any raw Type-valued F54 route, F45 tree or native context. -/
inductive NativeGK2FullStructuralPlainSyntax
    (Route : Type u) (Tree : Type v)
    (Reassoc : Type w) (LeftTrans : Type z)
    (RightTrans : Type t) (Adjacent : Type h) :
    Type (max (max (max u v) (max w z)) (max t h)) where
  | refl (route : Route)
  | symm (w : NativeGK2FullStructuralPlainSyntax
      Route Tree Reassoc LeftTrans RightTrans Adjacent)
  | trans (w v : NativeGK2FullStructuralPlainSyntax
      Route Tree Reassoc LeftTrans RightTrans Adjacent)
  | reassoc (atom : Reassoc)
  | leftUnit (route : Route)
  | rightUnit (route : Route)
  | precompose (route : Route)
      (w : NativeGK2FullStructuralPlainSyntax
        Route Tree Reassoc LeftTrans RightTrans Adjacent)
  | postcompose
      (w : NativeGK2FullStructuralPlainSyntax
        Route Tree Reassoc LeftTrans RightTrans Adjacent)
      (route : Route)
  | leftContextTrans (atom : LeftTrans)
  | rightContextTrans (atom : RightTrans)
  | leftContextUnit (atom : Adjacent)
  | rightContextUnit (atom : Adjacent)
  | leftContextCongruence
      (w : NativeGK2FullStructuralPlainSyntax
        Route Tree Reassoc LeftTrans RightTrans Adjacent)
      (later : Tree)
  | rightContextCongruence (earlier : Tree)
      (w : NativeGK2FullStructuralPlainSyntax
        Route Tree Reassoc LeftTrans RightTrans Adjacent)
  deriving Countable

/-- Exact dependent F54 structural proof-code carrier. -/
abbrev NativeGK2StructuralTypedCode
    (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    Type (max (max uD uE) (max vD vE)) :=
  NativeGK2FullStructuralPlainSyntax
    (NativeGIOriginalDepthTotal p D E)
    (NativeGHOriginalF45Total p D E)
    (NativeGK2ReassocAtom p D E)
    (NativeGK2LeftContextTransAtom p D E)
    (NativeGK2RightContextTransAtom p D E)
    (NativeGK2AdjacentTreesAtom p D E)

/-- Raw constructor faithful all-fourteen encoder.
Primitive payloads are themselves FULLY DEPENDENT original
Type-valued sources and thus cannot lie about middle F54/F45
boundaries. Recursive pasting operations remain distinguishable. -/
def nativeGK2EncodeStructural
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
    NativeGK2StructuralTypedCode p D E :=
  match w with
  | .refl route =>
      .refl (nativeGJ2PackRoute route)
  | .symm inner =>
      .symm (nativeGK2EncodeStructural inner)
  | .trans inner outer =>
      .trans (nativeGK2EncodeStructural inner)
        (nativeGK2EncodeStructural outer)
  | .reassoc u v z =>
      .reassoc (nativeGK2PackReassoc u v z)
  | .leftUnit route =>
      .leftUnit (nativeGJ2PackRoute route)
  | .rightUnit route =>
      .rightUnit (nativeGJ2PackRoute route)
  | .precompose route inner =>
      .precompose (nativeGJ2PackRoute route)
        (nativeGK2EncodeStructural inner)
  | .postcompose inner route =>
      .postcompose (nativeGK2EncodeStructural inner)
        (nativeGJ2PackRoute route)
  | .leftContextTrans u v later =>
      .leftContextTrans (nativeGK2PackLeftContextTrans u v later)
  | .rightContextTrans earlier u v =>
      .rightContextTrans (nativeGK2PackRightContextTrans earlier u v)
  | .leftContextUnit earlier later =>
      .leftContextUnit (nativeGK2PackAdjacentTrees earlier later)
  | .rightContextUnit earlier later =>
      .rightContextUnit (nativeGK2PackAdjacentTrees earlier later)
  | .leftContextCongruence inner later =>
      .leftContextCongruence (nativeGK2EncodeStructural inner)
        (nativeGIPackTree later)
  | .rightContextCongruence earlier inner =>
      .rightContextCongruence (nativeGIPackTree earlier)
        (nativeGK2EncodeStructural inner)

/-- All fourteen faithfully dependent raw syntax sources are
Countable under explicit BOTH D/E objects and all Hom fibers. -/
theorem nativeGK2StructuralTypedCode_countable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    Countable (NativeGK2StructuralTypedCode p D E) := by
  letI : Countable (NativeGIOriginalDepthTotal p D E) :=
    nativeGIOriginalDepthTotal_countable hobjD hhomD hobjE hhomE
  letI : Countable (NativeGHOriginalF45Total p D E) :=
    nativeGHOriginalF45Total_countable hobjD hhomD hobjE hhomE
  letI : Countable (NativeGK2ReassocAtom p D E) :=
    nativeGK2ReassocAtom_countable hobjD hhomD hobjE hhomE
  letI : Countable (NativeGK2LeftContextTransAtom p D E) :=
    nativeGK2LeftContextTransAtom_countable hobjD hhomD hobjE hhomE
  letI : Countable (NativeGK2RightContextTransAtom p D E) :=
    nativeGK2RightContextTransAtom_countable hobjD hhomD hobjE hhomE
  letI : Countable (NativeGK2AdjacentTreesAtom p D E) :=
    nativeGK2AdjacentTreesAtom_countable hobjD hhomD hobjE hhomE
  infer_instance

theorem nativeGK2PhysicalStructuralTypedCode_countable (p : Polygon) :
    Countable (NativeGK2StructuralTypedCode p Site Site) :=
  nativeGK2StructuralTypedCode_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable

theorem nativeGK2PhysicalAllPolygonStructuralTypedCode_countable :
    Countable (Σ p : Polygon, NativeGK2StructuralTypedCode p Site Site) := by
  letI : Countable Polygon := nativeC60GEPhysicalPolygon_countable
  letI : ∀ p : Polygon, Countable (NativeGK2StructuralTypedCode p Site Site) :=
    nativeGK2PhysicalStructuralTypedCode_countable
  infer_instance

#print axioms nativeGK2StructuralTypedCode_countable
#print axioms nativeGK2PhysicalStructuralTypedCode_countable
#print axioms nativeGK2PhysicalAllPolygonStructuralTypedCode_countable

end
end Kuu.F112.Physical
