import KUOS.DependentOriginationCoherentBiadjunctionOriginalF45RotationContextsV5_151
import KUOS.DependentOriginationCoherentBiadjunctionOriginalF45PentagonTreesV5_150

namespace KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F55-A / v5.152 — real rotation chains with explicit double-depth bridges

F53 gives five ACTUAL original F45 binary bracket trees, with distinct
parenthesized F19 and F28 Nat indices. F54 provides genuine Type-valued
local associativity RotationChain evidence, but an individual such chain
has exactly one pair of depth indices at both its endpoints.

We add an indexed, Type-valued finite route carrier in which every
actual F54 RotationChain is retained, while changes in the *notation*
for its original two depth indices occur only through independently
specified equality proofs. Contextual embeddings keep both original
axes separate. Cast bridges count as zero elementary rotations.

This makes the F53 3-versus-2-edge pentagon into two concrete, different
typed routes of ORIGINAL F54 local-rotation witnesses rather than merely
a proof of equal endpoints in the original F44 quotient. The resulting
generator is an explicitly constructed path relation, not an assertion
of arbitrary tricategorical 3-cell coherence or an equality of raw paths.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- A genuinely typed ORIGINAL F45 rotation route that retains every
F54 finite RotationChain step, and separately records *both* exact
F19/F28 Nat index casts. Contexts and concatenation remain real Type
constructors; no arbitrary F19/F28 Hom identification is introduced. -/
inductive OriginalF45BracketTree.DepthRotationRoute :
    ∀ {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : Blocks a b} {pa pb : Blocks x y},
      OriginalF45BracketTree n m ma pa mb pb →
      OriginalF45BracketTree n' m' ma pa mb pb →
      Type (max (max uD uE) (max vD vE)) where
  | chain
      {a b : D} {x y : E} {n m : Nat}
      {ma mb : Blocks a b} {pa pb : Blocks x y}
      {first last : OriginalF45BracketTree n m ma pa mb pb}
      (path : OriginalF45BracketTree.RotationChain first last) :
      DepthRotationRoute first last
  | castDepths
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : Blocks a b} {pa pb : Blocks x y}
      (hn : n = n') (hm : m = m')
      (tree : OriginalF45BracketTree n m ma pa mb pb) :
      DepthRotationRoute tree
        (OriginalF45BracketTree.castDepths hn hm tree)
  | trans
      {a b : D} {x y : E}
      {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
      {ma mb : Blocks a b} {pa pb : Blocks x y}
      {first : OriginalF45BracketTree n₁ m₁ ma pa mb pb}
      {middle : OriginalF45BracketTree n₂ m₂ ma pa mb pb}
      {last : OriginalF45BracketTree n₃ m₃ ma pa mb pb}
      (left : DepthRotationRoute first middle)
      (right : DepthRotationRoute middle last) :
      DepthRotationRoute first last
  | leftContext
      {a b : D} {x y : E}
      {n n' m m' k l : Nat}
      {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
      {before : OriginalF45BracketTree n m ma pa mb pb}
      {after : OriginalF45BracketTree n' m' ma pa mb pb}
      (path : DepthRotationRoute before after)
      (later : OriginalF45BracketTree k l mb pb mc pc) :
      DepthRotationRoute
        (OriginalF45BracketTree.node before later)
        (OriginalF45BracketTree.node after later)
  | rightContext
      {a b : D} {x y : E}
      {k l n n' m m' : Nat}
      {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
      (earlier : OriginalF45BracketTree k l ma pa mb pb)
      {before : OriginalF45BracketTree n m mb pb mc pc}
      {after : OriginalF45BracketTree n' m' mb pb mc pc}
      (path : DepthRotationRoute before after) :
      DepthRotationRoute
        (OriginalF45BracketTree.node earlier before)
        (OriginalF45BracketTree.node earlier after)

/-- Count only genuine original F54 rotation edges, not the two-depth
equality transports required to type different parentheses. This
retains the distinction between 3 and 2 paths around a pentagon. -/
def OriginalF45BracketTree.DepthRotationRoute.rotationCount
    {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    (route : OriginalF45BracketTree.DepthRotationRoute first last) : Nat := by
  induction route with
  | chain path =>
      exact path.length
  | castDepths _ _ _ =>
      exact 0
  | trans left right ihLeft ihRight =>
      exact ihLeft + ihRight
  | leftContext path later ih =>
      exact ih
  | rightContext earlier path ih =>
      exact ih

/-- One actual 3-subtree associativity step, WITH a genuine F54
one-edge RotationChain and independent F19/F28 Nat.add_assoc casts. -/
def OriginalF45BracketTree.DepthRotationRoute.assoc
    {a b : D} {x y : E}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {p₀ p₁ p₂ p₃ : Blocks a b}
    {q₀ q₁ q₂ q₃ : Blocks x y}
    (first : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
    (second : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
    (third : OriginalF45BracketTree n₃ m₃ p₂ q₂ p₃ q₃) :
    OriginalF45BracketTree.DepthRotationRoute
      (OriginalF45BracketTree.node
        (OriginalF45BracketTree.node first second) third)
      (OriginalF45BracketTree.node first
        (OriginalF45BracketTree.node second third)) :=
  OriginalF45BracketTree.DepthRotationRoute.trans
    (OriginalF45BracketTree.DepthRotationRoute.castDepths
      (Nat.add_assoc n₁ n₂ n₃) (Nat.add_assoc m₁ m₂ m₃)
      (OriginalF45BracketTree.node
        (OriginalF45BracketTree.node first second) third))
    (OriginalF45BracketTree.DepthRotationRoute.chain
      (OriginalF45BracketTree.RotationChain.snoc
        (OriginalF45BracketTree.RotationChain.refl _)
        (OriginalF45BracketTree.RotationEdge.forward
          (OriginalF45BracketTree.LocalRotation.assoc first second third))))

/-- A real associativity step is exactly ONE original F54 rotation,
although its two independent original depth casts are also retained. -/
theorem OriginalF45BracketTree.DepthRotationRoute.assoc_rotationCount
    {a b : D} {x y : E}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {p₀ p₁ p₂ p₃ : Blocks a b}
    {q₀ q₁ q₂ q₃ : Blocks x y}
    (first : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
    (second : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
    (third : OriginalF45BracketTree n₃ m₃ p₂ q₂ p₃ q₃) :
    (OriginalF45BracketTree.DepthRotationRoute.assoc
      first second third).rotationCount = 1 := by
  rfl

section FourOriginalTrees

variable {a b : D} {x y : E}
variable {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
variable {p₀ p₁ p₂ p₃ p₄ : Blocks a b}
variable {q₀ q₁ q₂ q₃ q₄ : Blocks x y}
variable
  (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
  (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
  (t₃ : OriginalF45BracketTree n₃ m₃ p₂ q₂ p₃ q₃)
  (t₄ : OriginalF45BracketTree n₄ m₄ p₃ q₃ p₄ q₄)

/-- A concrete THREE-ROTATION route through original F53 vertices
0 -> 1 -> 2 -> 3, with exact original F19/F28 casts at every step. -/
def OriginalF45BracketTree.DepthRotationRoute.pentagonLong :
    OriginalF45BracketTree.DepthRotationRoute
      (OriginalF45BracketTree.pentagon0 t₁ t₂ t₃ t₄)
      (OriginalF45BracketTree.pentagon3 t₁ t₂ t₃ t₄) :=
  OriginalF45BracketTree.DepthRotationRoute.trans
    (OriginalF45BracketTree.DepthRotationRoute.trans
      (OriginalF45BracketTree.DepthRotationRoute.leftContext
        (OriginalF45BracketTree.DepthRotationRoute.assoc t₁ t₂ t₃) t₄)
      (OriginalF45BracketTree.DepthRotationRoute.assoc
        t₁ (OriginalF45BracketTree.node t₂ t₃) t₄))
    (OriginalF45BracketTree.DepthRotationRoute.rightContext t₁
      (OriginalF45BracketTree.DepthRotationRoute.assoc t₂ t₃ t₄))

/-- A genuinely different TWO-ROTATION route through original F53
vertices 0 -> 4 -> 3, not a quotient-equality replacement. -/
def OriginalF45BracketTree.DepthRotationRoute.pentagonShort :
    OriginalF45BracketTree.DepthRotationRoute
      (OriginalF45BracketTree.pentagon0 t₁ t₂ t₃ t₄)
      (OriginalF45BracketTree.pentagon3 t₁ t₂ t₃ t₄) :=
  OriginalF45BracketTree.DepthRotationRoute.trans
    (OriginalF45BracketTree.DepthRotationRoute.assoc
      (OriginalF45BracketTree.node t₁ t₂) t₃ t₄)
    (OriginalF45BracketTree.DepthRotationRoute.assoc
      t₁ t₂ (OriginalF45BracketTree.node t₃ t₄))

/-- The actual long route contains THREE genuine elementary
F54 RotationChain edges, regardless of the two-axis index casts. -/
theorem OriginalF45BracketTree.DepthRotationRoute.pentagonLong_rotationCount :
    (OriginalF45BracketTree.DepthRotationRoute.pentagonLong
      t₁ t₂ t₃ t₄).rotationCount = 3 := by
  rfl

/-- The actual short route contains TWO genuine elementary
F54 RotationChain edges, distinct from the three-rotation route. -/
theorem OriginalF45BracketTree.DepthRotationRoute.pentagonShort_rotationCount :
    (OriginalF45BracketTree.DepthRotationRoute.pentagonShort
      t₁ t₂ t₃ t₄).rotationCount = 2 := by
  rfl

/-- The two explicit witnesses are NOT equal as raw typed routes.
Their future coherence must therefore have its own higher relation,
rather than being inferred from equality of their F44 endpoints. -/
theorem OriginalF45BracketTree.DepthRotationRoute.pentagonLong_ne_short :
    OriginalF45BracketTree.DepthRotationRoute.pentagonLong t₁ t₂ t₃ t₄ ≠
      OriginalF45BracketTree.DepthRotationRoute.pentagonShort t₁ t₂ t₃ t₄ := by
  intro h
  have hc := congrArg
    OriginalF45BracketTree.DepthRotationRoute.rotationCount h
  rw [OriginalF45BracketTree.DepthRotationRoute.pentagonLong_rotationCount,
    OriginalF45BracketTree.DepthRotationRoute.pentagonShort_rotationCount] at hc
  exact (by decide : (3 : Nat) ≠ 2) hc

end FourOriginalTrees

#print axioms OriginalF45BracketTree.DepthRotationRoute
#print axioms OriginalF45BracketTree.DepthRotationRoute.rotationCount
#print axioms OriginalF45BracketTree.DepthRotationRoute.assoc
#print axioms OriginalF45BracketTree.DepthRotationRoute.assoc_rotationCount
#print axioms OriginalF45BracketTree.DepthRotationRoute.pentagonLong
#print axioms OriginalF45BracketTree.DepthRotationRoute.pentagonShort
#print axioms OriginalF45BracketTree.DepthRotationRoute.pentagonLong_rotationCount
#print axioms OriginalF45BracketTree.DepthRotationRoute.pentagonShort_rotationCount
#print axioms OriginalF45BracketTree.DepthRotationRoute.pentagonLong_ne_short

end
end KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
