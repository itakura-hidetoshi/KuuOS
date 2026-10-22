import Kuu.F112.PolygonNativeF55P90AssociatorSourceBoundary
import Mathlib.Tactic

/-!
# F112-P90B — explicit triple-route associator naturality boundary

P89 has a genuine Type-valued 4-cell presentation proving strict
interchange for four P89 classes. P90A proves the two original F45
three-factor brackets are NOT raw equal, even after both Nat casts,
although a real typed one-rotation F54 associator relates them.

Here we construct TWO well-typed original F54 route composites for
any triple of genuine F54 input routes:
  left  : (((u ⊗ v) ⊗ w) ≫ assoc(after))
  right : (assoc(before) ≫ (u ⊗ (v ⊗ w))).
Both have exactly the SAME original F45 source and target trees.
They have exactly the SAME genuine primitive rotation count, yet
their FIRST source constructor orientation differs: 1 vs 0.
So the F54 routes are NOT literally equal.

Their necessary comparison slot is an ORIGINAL genuinely Type-valued
F55 PresentedCell between these exact two nonidentical F54 routes.
The slot is defined as a Type; we do NOT assume or fabricate an
inhabitant, nor equate the F54 routes from shadow/sector equality.
Any future strict horizontal associativity across F54 bracketings
requires explicit higher evidence/coherence in a new presentation.

Original 107 public roots, P87/P88 no-go, P89 strict interchange and
true C60 odd exchange phase stay intact. No Gray, sorry or new axioms.
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

/-- Actual F54 2-route horizontal source: old F55's exact original
left-context-then-right-context route, NOT an invented observer. -/
def nativeF54P90HorizontalRoute
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    (u : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter)
    (v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter) :
    KuuNativeF45Tree.DepthRotationRoute p
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter) :=
  .trans (.leftContext u rightBefore) (.rightContext leftAfter v)

/-- True F54 horizontal two-route pasting adds EXACT primitive
rotation counts without losing independent source histories. -/
theorem nativeF54P90HorizontalRoute_count
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    (u : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter)
    (v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter) :
    (nativeF54P90HorizontalRoute u v).rotationCount =
      u.rotationCount + v.rotationCount := rfl

/-- First original triple route: complete LEFT-associated
horizontal changes, then the real F54 target associator. -/
def nativeF54P90AssocNaturalityLeftRoute
    {p : Polygon} {a b : D} {x y : E}
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
    KuuNativeF45Tree.DepthRotationRoute p
      (KuuNativeF45Tree.node
        (KuuNativeF45Tree.node firstBefore secondBefore) thirdBefore)
      (KuuNativeF45Tree.node firstAfter
        (KuuNativeF45Tree.node secondAfter thirdAfter)) :=
  .trans
    (nativeF54P90HorizontalRoute
      (nativeF54P90HorizontalRoute u v) w)
    (KuuNativeF45Tree.DepthRotationRoute.assoc firstAfter secondAfter thirdAfter)

/-- Second original triple route: the real F54 SOURCE associator
first, then complete RIGHT-associated horizontal changes. -/
def nativeF54P90AssocNaturalityRightRoute
    {p : Polygon} {a b : D} {x y : E}
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
    KuuNativeF45Tree.DepthRotationRoute p
      (KuuNativeF45Tree.node
        (KuuNativeF45Tree.node firstBefore secondBefore) thirdBefore)
      (KuuNativeF45Tree.node firstAfter
        (KuuNativeF45Tree.node secondAfter thirdAfter)) :=
  .trans
    (KuuNativeF45Tree.DepthRotationRoute.assoc firstBefore secondBefore thirdBefore)
    (nativeF54P90HorizontalRoute u (nativeF54P90HorizontalRoute v w))

/-- Both well-typed alternatives use identical physical number of
real primitive F54 rotations: each uses the source routes u,v,w
and precisely one genuine associator rotation. -/
theorem nativeF54P90AssocNaturality_rotationCount_eq
    {p : Polygon} {a b : D} {x y : E}
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
    (nativeF54P90AssocNaturalityLeftRoute u v w).rotationCount =
      (nativeF54P90AssocNaturalityRightRoute u v w).rotationCount := by
  change (u.rotationCount + v.rotationCount + w.rotationCount) + 1 =
    1 + (u.rotationCount + (v.rotationCount + w.rotationCount))
  omega

/-- TRUE noncommutative F54 route obstruction: different ordering of
the actual associator and context route changes gives different RAW
Type-valued routes, although endpoints and total counts coincide.
P90 does NOT identify them by full shadow or F54 root casts. -/
theorem nativeF54P90AssocNaturality_routes_ne
    {p : Polygon} {a b : D} {x y : E}
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
    nativeF54P90AssocNaturalityLeftRoute u v w ≠
      nativeF54P90AssocNaturalityRightRoute u v w := by
  intro heq
  have htag := congrArg
    KuuNativeF45Tree.DepthRotationRoute.firstPastingTag heq
  change (1 : Nat) = 0 at htag
  omega

/-- The precise UNFILLED higher coherence comparison required
to exchange source/target F54 reassociation with three simultaneous
original F54 route changes. It is a TYPE OF POSSIBLE EVIDENCE;
NO constructor, assumption or theorem states it is inhabited.
Historical F55 pentagon/square witnesses are not replaced. -/
abbrev NativeF55P90AssocNaturalityCell
    {p : Polygon} {a b : D} {x y : E}
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
    (w : KuuNativeF45Tree.DepthRotationRoute p thirdBefore thirdAfter) :=
  KuuNativeF45Tree.DepthRotationRoute.PresentedCell p
    (nativeF54P90AssocNaturalityLeftRoute u v w)
    (nativeF54P90AssocNaturalityRightRoute u v w)

#print axioms nativeF54P90HorizontalRoute
#print axioms nativeF54P90HorizontalRoute_count
#print axioms nativeF54P90AssocNaturalityLeftRoute
#print axioms nativeF54P90AssocNaturalityRightRoute
#print axioms nativeF54P90AssocNaturality_rotationCount_eq
#print axioms nativeF54P90AssocNaturality_routes_ne
#print axioms NativeF55P90AssocNaturalityCell

end
end Kuu.F112.Physical
