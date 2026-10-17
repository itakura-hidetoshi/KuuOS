import Kuu.F112.PolygonNativeF54DepthRoutes

/-!
# F112-E7P1 / genuine F55 disjoint contextual square on native F54 routes

The original F55's second basic generator is a SQUARE built from
TWO independently supplied, fully typed F54 LocalRotation witnesses.
The rotations are embedded in disjoint original binary contexts and
their two pasting orders have exactly the SAME four-axis boundaries.

This file constructs the original-shaped square on the NEW independent
F19/F28-style Blocks+AxisTrace native F45 source. Every elementary
rotation is an actual F54 Type-valued witness and a real RotationChain
edge. Both Nat source depths remain independently typed. We prove
counts, raw source non-equality by a structurally derived first
context tag, and a six-real-sector true C60 hexagon specialization.

No numerical phase or Gray coherence is used to assert the square.
The independently presented F55 THREE-CELL is constructed in the
following module; it is not an equality of the raw two-step paths.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Embed exactly ONE actual F54 local witness into a one-edge
RotationChain, retaining its original intermediate F45 tree. -/
def KuuNativeF45Tree.DepthRotationRoute.ofLocalRotation
    {p : Polygon} {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (rotation : KuuNativeF45Tree.LocalRotation p before after) :
    KuuNativeF45Tree.DepthRotationRoute p before after :=
  .chain (.snoc (.refl _) (.forward rotation))

theorem KuuNativeF45Tree.DepthRotationRoute.ofLocalRotation_count
    {p : Polygon} {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (rotation : KuuNativeF45Tree.LocalRotation p before after) :
    (KuuNativeF45Tree.DepthRotationRoute.ofLocalRotation
      rotation).rotationCount = 1 := by
  rfl

section DisjointNativeRotations

variable {p : Polygon} {a b : D} {x y : E}
variable {n m n' m' : Nat}
variable {p₀ p₁ p₂ : KuuNativeBlocks a b}
variable {q₀ q₁ q₂ : KuuNativeBlocks x y}
variable {leftBefore leftAfter : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
variable {rightBefore rightAfter : KuuNativeF45Tree p n' m' p₁ q₁ p₂ q₂}
variable
  (left : KuuNativeF45Tree.LocalRotation p leftBefore leftAfter)
  (right : KuuNativeF45Tree.LocalRotation p rightBefore rightAfter)

/-- Left reassociation first, then the genuinely DISJOINT right
reassociation: both are typed original-shaped F54 local witnesses. -/
def KuuNativeF45Tree.DepthRotationRoute.squareLeftFirst :
    KuuNativeF45Tree.DepthRotationRoute p
      (.node leftBefore rightBefore) (.node leftAfter rightAfter) :=
  .trans
    (.ofLocalRotation (.leftContext left rightBefore))
    (.ofLocalRotation (.rightContext leftAfter right))

/-- Right reassociation first, then the disjoint left one.
The source and target are definitionally identical to the above. -/
def KuuNativeF45Tree.DepthRotationRoute.squareRightFirst :
    KuuNativeF45Tree.DepthRotationRoute p
      (.node leftBefore rightBefore) (.node leftAfter rightAfter) :=
  .trans
    (.ofLocalRotation (.rightContext leftBefore right))
    (.ofLocalRotation (.leftContext left rightAfter))

theorem KuuNativeF45Tree.DepthRotationRoute.squareLeftFirst_count :
    (KuuNativeF45Tree.DepthRotationRoute.squareLeftFirst
      left right).rotationCount = 2 := by
  rfl

theorem KuuNativeF45Tree.DepthRotationRoute.squareRightFirst_count :
    (KuuNativeF45Tree.DepthRotationRoute.squareRightFirst
      left right).rotationCount = 2 := by
  rfl

end DisjointNativeRotations

/-- Structural first-context signature of a TRUE F54 generator;
the signature is not inferred from its native shadow grade. -/
def KuuNativeF45Tree.LocalRotation.contextTag
    {p : Polygon} {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {before after : KuuNativeF45Tree p n m ma pa mb pb} :
    KuuNativeF45Tree.LocalRotation p before after → Nat
  | .assoc _ _ _ => 0
  | .leftContext _ _ => 1
  | .rightContext _ _ => 2

/-- A genuinely oriented source RotationEdge retains its
first-context tag even if the edge is traversed backward. -/
def KuuNativeF45Tree.RotationEdge.contextTag
    {p : Polygon} {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {before after : KuuNativeF45Tree p n m ma pa mb pb} :
    KuuNativeF45Tree.RotationEdge p before after → Nat
  | .forward rot => rot.contextTag
  | .backward rot => rot.contextTag

/-- A finite Type-valued original-shaped RotationChain exposes the
context of its ACTUAL final primitive rotation rather than a grade. -/
def KuuNativeF45Tree.RotationChain.finalContextTag
    {p : Polygon} {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {before after : KuuNativeF45Tree p n m ma pa mb pb} :
    KuuNativeF45Tree.RotationChain p before after → Nat
  | .refl _ => 0
  | .snoc _ edge => edge.contextTag

/-- Inspect the FIRST nontrivial outermost pasted step of an E7O
raw path without dependent elimination of the whole bracket tree. -/
def KuuNativeF45Tree.DepthRotationRoute.firstPastingTag
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {before : KuuNativeF45Tree p n m ma pa mb pb}
    {after : KuuNativeF45Tree p n' m' ma pa mb pb} :
    KuuNativeF45Tree.DepthRotationRoute p before after → Nat
  | .chain storedPath => storedPath.finalContextTag
  | .castDepths _ _ _ => 0
  | .trans first _ => first.firstPastingTag
  | .leftContext _ _ => 1
  | .rightContext _ _ => 2

/-- The two typed square routes are NOT syntactically equal: their
first concrete F54 LocalRotation has distinct original binary context.
Both nevertheless contain exactly TWO primitive rotations. -/
theorem KuuNativeF45Tree.DepthRotationRoute.squareLeft_ne_right
    {p : Polygon} {a b : D} {x y : E}
    {n m n' m' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore leftAfter : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {rightBefore rightAfter : KuuNativeF45Tree p n' m' p₁ q₁ p₂ q₂}
    (left : KuuNativeF45Tree.LocalRotation p leftBefore leftAfter)
    (right : KuuNativeF45Tree.LocalRotation p rightBefore rightAfter) :
    KuuNativeF45Tree.DepthRotationRoute.squareLeftFirst left right ≠
      KuuNativeF45Tree.DepthRotationRoute.squareRightFirst left right := by
  intro h
  have ht := congrArg
    KuuNativeF45Tree.DepthRotationRoute.firstPastingTag h
  change (1 : Nat) = 2 at ht
  exact (by decide : (1 : Nat) ≠ 2) ht

/-- A TRUE six-sided C60 polygon sector, with its physical
original boundary index checked rather than an arbitrary label. -/
def northHexagonNativeSector (i : Fin 6) :
    PolygonBoundarySector (.hexagon (.top 0)) :=
  ⟨i, by simp [polygonSideCount]⟩

/-- The two independent typed F40-shaped native blocks on an ACTUAL
true hexagon vertex-edge-face vs direct vertex-face sector. -/
def northHexagonNativeFrame :=
  canonicalPolygonNativeDualAxisFrame (.hexagon (.top 0))
    (northHexagonNativeSector 0)

/-- Six distinct ORIGINAL C60 physical sectors, each a genuine
native F45 source unit with two independent categorical Blocks axes. -/
def northHexagonNativeUnit (i : Fin 6) :
    KuuNativeF45Tree (.hexagon (.top 0)) 0 0
      northHexagonNativeFrame.firstAxis northHexagonNativeFrame.secondAxis
      northHexagonNativeFrame.firstAxis northHexagonNativeFrame.secondAxis :=
  .refl (northHexagonNativeSector i)
    northHexagonNativeFrame.firstAxis northHexagonNativeFrame.secondAxis

/-- An ACTUAL left triple and independent right triple of physical
hexagon F45 units, containing six distinct source sector labels.
The F54 local witnesses are original-shaped root associators. -/
def northHexagonNativeLeftRotation :=
  KuuNativeF45Tree.LocalRotation.assoc
    (northHexagonNativeUnit 0)
    (northHexagonNativeUnit 1)
    (northHexagonNativeUnit 2)

def northHexagonNativeRightRotation :=
  KuuNativeF45Tree.LocalRotation.assoc
    (northHexagonNativeUnit 3)
    (northHexagonNativeUnit 4)
    (northHexagonNativeUnit 5)

/-- Both explicit square routes exist on the actual C60 hexagon,
with the original two-axis native categorical Blocks preserved. -/
def northHexagonNativeSquareLeft :=
  KuuNativeF45Tree.DepthRotationRoute.squareLeftFirst
    northHexagonNativeLeftRotation northHexagonNativeRightRotation

def northHexagonNativeSquareRight :=
  KuuNativeF45Tree.DepthRotationRoute.squareRightFirst
    northHexagonNativeLeftRotation northHexagonNativeRightRotation

theorem northHexagonNativeSquare_ne :
    northHexagonNativeSquareLeft ≠ northHexagonNativeSquareRight :=
  KuuNativeF45Tree.DepthRotationRoute.squareLeft_ne_right
    northHexagonNativeLeftRotation northHexagonNativeRightRotation

theorem northHexagonNativeSquare_counts :
    northHexagonNativeSquareLeft.rotationCount = 2 ∧
      northHexagonNativeSquareRight.rotationCount = 2 := by
  constructor <;> rfl

#print axioms KuuNativeF45Tree.DepthRotationRoute.ofLocalRotation
#print axioms KuuNativeF45Tree.DepthRotationRoute.ofLocalRotation_count
#print axioms KuuNativeF45Tree.DepthRotationRoute.squareLeftFirst_count
#print axioms KuuNativeF45Tree.DepthRotationRoute.squareRightFirst_count
#print axioms KuuNativeF45Tree.LocalRotation.contextTag
#print axioms KuuNativeF45Tree.DepthRotationRoute.squareLeft_ne_right
#print axioms northHexagonNativeSquare_ne
#print axioms northHexagonNativeSquare_counts
end
end Kuu.F112.Physical
