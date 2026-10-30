import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeF55PrimitiveCountability

/-!
# F112-P94D3GJ2 — full nine-constructor finite code for original native F55

The pinned Mathlib Countable deriving handler is for simple inductive
presentations with countable constructor argument types. The ACTUAL
native F55 source is a strongly indexed dependent Type-valued family
over arbitrary two-category D/E object/Hom/Blocks evidence. Therefore
we code the complete original original constructors in a separately
countable finite syntax while retaining actual original typed atoms.
This is NOT a scalar, quotient, or proof-irrelevant observer.

Raw primitive F55 pentagon stores four ACTUAL original F45 stage
proofs; square stores two actual LocalRotation source witnesses.
Every ident, symm, trans, left/right-context and pre/post-composition
remembers the exact original F54 route or F45 context Type-valued
proof. Encoding uses all original nine constructors, recursively.
A dependent partial decoder and a strict left inverse are subsequent
independent obligations; Countable of the code alone never implies
Countable of the original F55 proof total.

Append-only; 107 public roots; no Gray imports.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
Pinned Lean v4.30.0-rc2 / mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE u v w z

/-- Nine exact *shapes* of the original F55 syntax, retaining true
typed source atoms, all intermediate routes and physical F45 trees. -/
inductive NativeGJ2NinePlainSyntax
    (Route : Type u) (Pentagon : Type v)
    (Square : Type w) (Tree : Type z) :
    Type (max (max u v) (max w z)) where
  | ident (route : Route)
  | pentagon (source : Pentagon)
  | disjointSquare (source : Square)
  | symm (cell : NativeGJ2NinePlainSyntax Route Pentagon Square Tree)
  | trans (left right : NativeGJ2NinePlainSyntax Route Pentagon Square Tree)
  | leftContext (cell : NativeGJ2NinePlainSyntax Route Pentagon Square Tree)
      (later : Tree)
  | rightContext (earlier : Tree)
      (cell : NativeGJ2NinePlainSyntax Route Pentagon Square Tree)
  | precompose (prior : Route)
      (cell : NativeGJ2NinePlainSyntax Route Pentagon Square Tree)
  | postcompose (cell : NativeGJ2NinePlainSyntax Route Pentagon Square Tree)
      (suffix : Route)
  deriving Countable

/-- Uniform full original proof-token code at generic input D/E. -/
abbrev NativeGJ2FullNineCode (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    Type (max (max uD uE) (max vD vE)) :=
  NativeGJ2NinePlainSyntax
    (NativeGIOriginalDepthTotal p D E)
    (NativeGJPentagonAtomTotal p D E)
    (NativeGJSquareAtomTotal p D E)
    (NativeGHOriginalF45Total p D E)

/-- Store every original depth-route boundary in the unmodified GI
Type-valued proof total, with both independent Nat grades and F45 ends. -/
def nativeGJ2PackRoute
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeGIOriginalDepthTotal p D E :=
  ⟨⟨a, b, x, y, ma, pa, mb, pb, n, n', m, m',
    first, last⟩, route⟩

/-- Fully original pentagon atom: four stage proofs, five D/E block
presentations on each axis and both independent Nat depths at each
stage. This is the original Type-valued source, not its charge. -/
def nativeGJ2PackPentagon
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    {p₀ p₁ p₂ p₃ p₄ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ q₄ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
    (t₄ : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄) :
    NativeGJPentagonAtomTotal p D E :=
  ⟨a, b, x, y, p₀, p₁, p₂, p₃, p₄,
    q₀, q₁, q₂, q₃, q₄,
    n₁, m₁, n₂, m₂, n₃, m₃, n₄, m₄,
    (t₁, t₂, t₃, t₄)⟩

/-- Actual two proof-relevant disjoint native local rotations at
the exact matching original F45 middle Blocks and both Nat axes. -/
def nativeGJ2PackSquare
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {n m n' m' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore leftAfter : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {rightBefore rightAfter : KuuNativeF45Tree p n' m' p₁ q₁ p₂ q₂}
    (left : KuuNativeF45Tree.LocalRotation p leftBefore leftAfter)
    (right : KuuNativeF45Tree.LocalRotation p rightBefore rightAfter) :
    NativeGJSquareAtomTotal p D E :=
  ⟨a, b, x, y, p₀, p₁, p₂, q₀, q₁, q₂,
    n, m, n', m', leftBefore, leftAfter, rightBefore,
    rightAfter, (left, right)⟩

/-- Full ORIGINAL F55 nine-constructor recursive *encoder*.
No original proof witness is dropped, quotiented, or replaced by
a scalar. Dependent boundary consistency will be checked by
the subsequent partial decoder. -/
def nativeGJ2EncodePresented
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    NativeGJ2FullNineCode p D E :=
  match cell with
  | .ident route =>
      .ident (nativeGJ2PackRoute route)
  | .pentagon t₁ t₂ t₃ t₄ =>
      .pentagon (nativeGJ2PackPentagon t₁ t₂ t₃ t₄)
  | .disjointSquare left right =>
      .disjointSquare (nativeGJ2PackSquare left right)
  | .symm prior =>
      .symm (nativeGJ2EncodePresented prior)
  | .trans left right =>
      .trans (nativeGJ2EncodePresented left) (nativeGJ2EncodePresented right)
  | .leftContext prior later =>
      .leftContext (nativeGJ2EncodePresented prior) (nativeGIPackTree later)
  | .rightContext earlier prior =>
      .rightContext (nativeGIPackTree earlier) (nativeGJ2EncodePresented prior)
  | .precompose route prior =>
      .precompose (nativeGJ2PackRoute route) (nativeGJ2EncodePresented prior)
  | .postcompose prior route =>
      .postcompose (nativeGJ2EncodePresented prior) (nativeGJ2PackRoute route)

/-- A genuinely countable finite syntax alphabet for all NINE original
proof constructors, provided object and EACH Hom-fiber smallness of
both independent original categories. -/
theorem nativeGJ2FullNineCode_countable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    Countable (NativeGJ2FullNineCode p D E) := by
  letI : Countable (NativeGIOriginalDepthTotal p D E) :=
    nativeGIOriginalDepthTotal_countable hobjD hhomD hobjE hhomE
  letI : Countable (NativeGJPentagonAtomTotal p D E) :=
    nativeGJPentagonAtomTotal_countable hobjD hhomD hobjE hhomE
  letI : Countable (NativeGJSquareAtomTotal p D E) :=
    nativeGJSquareAtomTotal_countable hobjD hhomD hobjE hhomE
  letI : Countable (NativeGHOriginalF45Total p D E) :=
    nativeGHOriginalF45Total_countable hobjD hhomD hobjE hhomE
  infer_instance

/-- True C60 physical Site×Site specialization. -/
theorem nativeGJ2PhysicalNineCode_countable (p : Polygon) :
    Countable (NativeGJ2FullNineCode p Site Site) :=
  nativeGJ2FullNineCode_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable

#print axioms nativeGJ2FullNineCode_countable
#print axioms nativeGJ2PhysicalNineCode_countable

end
end Kuu.F112.Physical
