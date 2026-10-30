import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGKSeamFullCountability

/-!
# F112-P94D3GK3 — original typed P92B nine-constructor code

A distinct P92B extension is faithfully coded, keeping the entire
original nine-constructor F55 PresentedCell atom and the independently
adjoined P92B associator-naturality atom. All remaining original
refl/symm/trans/context/pre/post constructors preserve full Type-valued
F54 routes, original F45 trees, D/E blocks and two Nat depths.

The countability of this finite code does NOT imply source countability
without a strict dependent partial decoder and original left inverse.
No identification with GJ2 PresentedCell, GK2 StructuralSeam or
historical P92B. No Gray, no sorry, no new axioms, append-only.
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

universe uD vD uE vE u v w z

/-- Free finite syntax for the distinct P92B nine-constructor source. -/
inductive NativeGK3P92PlainSyntax
    (Original : Type u) (Naturality : Type v)
    (Route : Type w) (Tree : Type z) :
    Type (max (max u v) (max w z)) where
  | original (cell : Original)
  | assocNaturality (atom : Naturality)
  | refl (route : Route)
  | symm (cell : NativeGK3P92PlainSyntax Original Naturality Route Tree)
  | trans (left right : NativeGK3P92PlainSyntax Original Naturality Route Tree)
  | leftContext (cell : NativeGK3P92PlainSyntax Original Naturality Route Tree)
      (later : Tree)
  | rightContext (earlier : Tree)
      (cell : NativeGK3P92PlainSyntax Original Naturality Route Tree)
  | precompose (prior : Route)
      (cell : NativeGK3P92PlainSyntax Original Naturality Route Tree)
  | postcompose (cell : NativeGK3P92PlainSyntax Original Naturality Route Tree)
      (suffix : Route)
  deriving Countable

abbrev NativeGK3P92TypedCode
    (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    Type (max (max uD uE) (max vD vE)) :=
  NativeGK3P92PlainSyntax
    (NativeGJOriginalPresentedTotal p D E)
    (NativeGKP92NaturalityAtomTotal p D E)
    (NativeGIOriginalDepthTotal p D E)
    (NativeGHOriginalF45Total p D E)

/-- Preserve complete original P92B source and target route proofs. -/
def nativeGK3PackP92
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
    (cell : NativeF55P92AssocComparison p r s) :
    NativeGKOriginalP92Total p D E :=
  ⟨⟨nativeGJ2PackRoute r, s⟩, cell⟩

/-- Complete actual six F45 trees, three F54 proof routes and all
twelve depth grades of a genuine adjoined P92B naturality generator. -/
def nativeGK3PackNaturality
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {n₁ n₁' n₂ n₂' n₃ n₃' m₁ m₁' m₂ m₂' m₃ m₃' : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    {firstBefore : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁}
    {firstAfter : KuuNativeF45Tree p n₁' m₁' p₀ q₀ p₁ q₁}
    {secondBefore : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂}
    {secondAfter : KuuNativeF45Tree p n₂' m₂' p₁ q₁ p₂ q₂}
    {thirdBefore : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃}
    {thirdAfter : KuuNativeF45Tree p n₃' m₃' p₂ q₂ p₃ q₃}
    (u : KuuNativeF45Tree.DepthRotationRoute p firstBefore firstAfter)
    (v : KuuNativeF45Tree.DepthRotationRoute p secondBefore secondAfter)
    (w : KuuNativeF45Tree.DepthRotationRoute p thirdBefore thirdAfter) :
    NativeGKP92NaturalityAtomTotal p D E :=
  ⟨a, b, x, y, p₀, p₁, p₂, p₃, q₀, q₁, q₂, q₃,
    n₁, n₁', n₂, n₂', n₃, n₃',
    m₁, m₁', m₂, m₂', m₃, m₃',
    firstBefore, firstAfter, secondBefore, secondAfter,
    thirdBefore, thirdAfter, (u, v, w)⟩

/-- Full recursively typed original P92B proof encoder. -/
def nativeGK3P92Encode
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
    (cell : NativeF55P92AssocComparison p r s) :
    NativeGK3P92TypedCode p D E :=
  match cell with
  | .original source => .original (nativeGJPackPresented source)
  | .assocNaturality u v w => .assocNaturality (nativeGK3PackNaturality u v w)
  | .refl route => .refl (nativeGJ2PackRoute route)
  | .symm inner => .symm (nativeGK3P92Encode inner)
  | .trans left right =>
      .trans (nativeGK3P92Encode left) (nativeGK3P92Encode right)
  | .leftContext inner later =>
      .leftContext (nativeGK3P92Encode inner) (nativeGIPackTree later)
  | .rightContext earlier inner =>
      .rightContext (nativeGIPackTree earlier) (nativeGK3P92Encode inner)
  | .precompose prior inner =>
      .precompose (nativeGJ2PackRoute prior) (nativeGK3P92Encode inner)
  | .postcompose inner suffix =>
      .postcompose (nativeGK3P92Encode inner) (nativeGJ2PackRoute suffix)

/-- The code is Countable with both independent D/E object and
each original Hom-fiber Countable explicitly assumed. -/
theorem nativeGK3P92TypedCode_countable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    Countable (NativeGK3P92TypedCode p D E) := by
  letI : Countable (NativeGJOriginalPresentedTotal p D E) :=
    nativeGJ2OriginalPresentedTotal_countable hobjD hhomD hobjE hhomE
  letI : Countable (NativeGKP92NaturalityAtomTotal p D E) :=
    nativeGKP92NaturalityAtomTotal_countable hobjD hhomD hobjE hhomE
  letI : Countable (NativeGIOriginalDepthTotal p D E) :=
    nativeGIOriginalDepthTotal_countable hobjD hhomD hobjE hhomE
  letI : Countable (NativeGHOriginalF45Total p D E) :=
    nativeGHOriginalF45Total_countable hobjD hhomD hobjE hhomE
  infer_instance

theorem nativeGK3PhysicalP92TypedCode_countable (p : Polygon) :
    Countable (NativeGK3P92TypedCode p Site Site) :=
  nativeGK3P92TypedCode_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable

#print axioms nativeGK3P92TypedCode_countable
#print axioms nativeGK3PhysicalP92TypedCode_countable

end
end Kuu.F112.Physical
