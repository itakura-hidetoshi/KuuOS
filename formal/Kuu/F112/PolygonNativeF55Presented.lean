import Kuu.F112.PolygonNativeF55Square

/-!
# F112-E7P2 / nine-constructor proof-relevant native F55 presentation

The old F55 PresentedCell is a FREE Type-valued presentation on
GENUINELY parallel original F54 depth routes; it does not identify
two raw routes and is not a globally assumed Gray 3-category law.

E7O reconstructs the F54-shaped source with actual typed native
two-axis F45 Blocks, AxisTrace histories, both Nat depth casts,
bidirectional rotation chains, concatenation and contexts. E7P1
constructs BOTH genuine disjoint-context rotation orders on this
source and proves their raw inequality at an actual six-sector C60
hexagon. E7O already proves the genuine 3-vs-2 pentagon raw inequality.

We now construct the EXACT NINE FORMAL CONSTRUCTOR SHAPES over THIS
new independent source: identity, pentagon, disjoint rotation square,
inverse, vertical pasting, left/right binary contexts, and pre/post
route pasting. All source and target trees, two independent Nat axes
and genuine F40-shaped intermediate categorical Blocks match in types.

An actual C60 north pentagon and top hexagon supply the TWO concrete
primitive 3-cell generators, and their proof terms remain unquotiented.

This is a new, independently defined raw F55-shaped presentation,
NOT a proof of equivalence with frozen F19/F28/F45/F55 nor a
global Gray/tricategorical 3-cell interpretation. No KUOS.* imports.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Free and completely TYPED nine-generator original-shaped
F55 3-source between actual parallel E7O native depth routes.
The critical pentagon/square generators have genuinely constructed
raw boundaries; no grade equality is used to create any cell. -/
inductive KuuNativeF45Tree.DepthRotationRoute.PresentedCell (p : Polygon) :
    ∀ {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb},
      KuuNativeF45Tree.DepthRotationRoute p first last →
      KuuNativeF45Tree.DepthRotationRoute p first last →
      Type (max (max uD uE) (max vD vE)) where
  | ident
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
      PresentedCell p route route
  | pentagon
      {a b : D} {x y : E}
      {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
      {p₀ p₁ p₂ p₃ p₄ : KuuNativeBlocks a b}
      {q₀ q₁ q₂ q₃ q₄ : KuuNativeBlocks x y}
      (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
      (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
      (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
      (t₄ : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄) :
      PresentedCell p
        (KuuNativeF45Tree.DepthRotationRoute.pentagonLong
          t₁ t₂ t₃ t₄)
        (KuuNativeF45Tree.DepthRotationRoute.pentagonShort
          t₁ t₂ t₃ t₄)
  | disjointSquare
      {a b : D} {x y : E} {n m n' m' : Nat}
      {p₀ p₁ p₂ : KuuNativeBlocks a b}
      {q₀ q₁ q₂ : KuuNativeBlocks x y}
      {leftBefore leftAfter :
        KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
      {rightBefore rightAfter :
        KuuNativeF45Tree p n' m' p₁ q₁ p₂ q₂}
      (left : KuuNativeF45Tree.LocalRotation p leftBefore leftAfter)
      (right : KuuNativeF45Tree.LocalRotation p rightBefore rightAfter) :
      PresentedCell p
        (KuuNativeF45Tree.DepthRotationRoute.squareLeftFirst left right)
        (KuuNativeF45Tree.DepthRotationRoute.squareRightFirst left right)
  | symm
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      (cell : PresentedCell p r s) : PresentedCell p s r
  | trans
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
      (left : PresentedCell p r s)
      (right : PresentedCell p s t) :
      PresentedCell p r t
  | leftContext
      {a b : D} {x y : E} {n n' m m' k l : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      (cell : PresentedCell p r s)
      (later : KuuNativeF45Tree p k l mb pb mc pc) :
      PresentedCell p
        (KuuNativeF45Tree.DepthRotationRoute.leftContext r later)
        (KuuNativeF45Tree.DepthRotationRoute.leftContext s later)
  | rightContext
      {a b : D} {x y : E} {k l n n' m m' : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      (earlier : KuuNativeF45Tree p k l ma pa mb pb)
      {first : KuuNativeF45Tree p n m mb pb mc pc}
      {last : KuuNativeF45Tree p n' m' mb pb mc pc}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      (cell : PresentedCell p r s) :
      PresentedCell p
        (KuuNativeF45Tree.DepthRotationRoute.rightContext earlier r)
        (KuuNativeF45Tree.DepthRotationRoute.rightContext earlier s)
  | precompose
      {a b : D} {x y : E}
      {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
      {middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
      {last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
      (priorRoute : KuuNativeF45Tree.DepthRotationRoute p first middle)
      {r s : KuuNativeF45Tree.DepthRotationRoute p middle last}
      (cell : PresentedCell p r s) :
      PresentedCell p
        (KuuNativeF45Tree.DepthRotationRoute.trans priorRoute r)
        (KuuNativeF45Tree.DepthRotationRoute.trans priorRoute s)
  | postcompose
      {a b : D} {x y : E}
      {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
      {middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
      {last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first middle}
      (cell : PresentedCell p r s)
      (suffix : KuuNativeF45Tree.DepthRotationRoute p middle last) :
      PresentedCell p
        (KuuNativeF45Tree.DepthRotationRoute.trans r suffix)
        (KuuNativeF45Tree.DepthRotationRoute.trans s suffix)

/-- The real north C60 pentagon contains an ACTUAL source-level
free higher-cell generator between distinct 3/2 F54 raw depth paths,
and both independent native Blocks/AxisTrace axes remain typed. -/
def northNativeF55PentagonCell :
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell (.pentagon .north)
      northNativeF45PentagonLong northNativeF45PentagonShort :=
  .pentagon northNativeF45FirstStage northNativeF45SecondStage
    northNativeF45ThirdStage northNativeF45FourthStage

/-- The second basic F55 presentation generator is an ACTUAL
six-sector C60 top-hexagon disjoint-context rotation square,
on the true E7P1 left-first/right-first F54 source boundaries. -/
def northHexagonNativeF55SquareCell :
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell (.hexagon (.top 0))
      northHexagonNativeSquareLeft northHexagonNativeSquareRight :=
  .disjointSquare
    northHexagonNativeLeftRotation northHexagonNativeRightRotation

/-- Independent raw proof-term discriminator, inspecting the
actual NINE constructors before quotient/interpretation. -/
def KuuNativeF45Tree.DepthRotationRoute.PresentedCell.shapeTag
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last} :
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s → Nat
  | .ident _ => 0
  | .pentagon _ _ _ _ => 1
  | .disjointSquare _ _ => 2
  | .symm _ => 3
  | .trans _ _ => 4
  | .leftContext _ _ => 5
  | .rightContext _ _ => 6
  | .precompose _ _ => 7
  | .postcompose _ _ => 8

/-- A unit pasted after the actual C60 pentagon cell does NOT make
the raw 3-cell proof tree syntactically equal to the original generator.
All nine constructors remain proof-relevant prior to quotienting. -/
theorem northNativeF55PentagonCell_ne_withUnit :
    northNativeF55PentagonCell ≠
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
        northNativeF55PentagonCell
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
          northNativeF45PentagonShort)) := by
  intro h
  have ht := congrArg
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell.shapeTag h
  change (1 : Nat) = 4 at ht
  exact (by decide : (1 : Nat) ≠ 4) ht

#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell
#print axioms northNativeF55PentagonCell
#print axioms northHexagonNativeF55SquareCell
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.shapeTag
#print axioms northNativeF55PentagonCell_ne_withUnit
end
end Kuu.F112.Physical
