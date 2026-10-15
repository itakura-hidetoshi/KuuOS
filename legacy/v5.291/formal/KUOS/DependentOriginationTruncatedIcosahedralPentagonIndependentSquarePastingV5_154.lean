import KUOS.DependentOriginationCoherentBiadjunctionOriginalF45IndependentDepthSquaresV5_154

namespace KUOS.DependentOriginationTruncatedIcosahedralPentagonRotationBridgeV5_154

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F57-C2 / v5.154 — all five ACTUAL C60 pentagon-edge square pastings

F57-B assigns each actual physical C60 pentagon edge its distinct
original F55 signed finite local associativity rotation path, with
its exact original F19 and F28 depth transports, along with a
genuine geometric four-flag square between adjacent pentagon and
hexagon faces.

F57-C1 produces the TWO actual compositional orders for any
two independently typed F55 depth-aware paths. Here the second
path is an arbitrary independent genuine F45 refinement path
beginning where the original C60 pentagon-labelled path ends.

Each of the FIVE old C60 pentagon edges is therefore equipped
with an actual labelled two-order square of Type-valued F55
finite refinement routes, and both paths carry real F44 quotient
and complete F19/F28 native history endpoint certificates.

The square comparison itself is now a *record of two actual paths
and their preserved invariants*, not a proof that this geometric
incidence square equals an arbitrary external Gray 3-cell, nor
a new inverse of a potentially noninvertible G.toOplax cell.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- A signed ORIGINAL F55 one-edge path and an independent
depth-aware path determine a genuine two-order pasting square.
Its type depends on the authentic original signed orientation. -/
def SignedOriginalF45PentagonSide.independentSquareType
    {a b : D} {x y : E}
    {p₀ p₄ p₅ : Blocks a b}
    {q₀ q₄ q₅ : Blocks x y}
    {u v : OriginalF45PentagonIndexedVertex p₀ p₄ q₀ q₄}
    (signed : SignedOriginalF45PentagonSide u v)
    {k k' l l' : Nat}
    {auxBefore : OriginalF45BracketTree k l p₄ q₄ p₅ q₅}
    {auxAfter : OriginalF45BracketTree k' l' p₄ q₄ p₅ q₅}
    (aux : OriginalF45BracketTree.DepthRotationRoute auxBefore auxAfter) :
    Type (max (max uD uE) (max vD vE)) :=
  match signed with
  | .forward left =>
      OriginalF45BracketTree.DepthRotationRoute.IndependentSquare left aux
  | .backward left =>
      OriginalF45BracketTree.DepthRotationRoute.IndependentSquare left aux

/-- The F57-C1 independent square is constructed for BOTH genuine
orientation cases. No quotient-only replacement of the first path. -/
noncomputable def SignedOriginalF45PentagonSide.independentSquareCanonical
    {a b : D} {x y : E}
    {p₀ p₄ p₅ : Blocks a b}
    {q₀ q₄ q₅ : Blocks x y}
    {u v : OriginalF45PentagonIndexedVertex p₀ p₄ q₀ q₄}
    (signed : SignedOriginalF45PentagonSide u v)
    {k k' l l' : Nat}
    {auxBefore : OriginalF45BracketTree k l p₄ q₄ p₅ q₅}
    {auxAfter : OriginalF45BracketTree k' l' p₄ q₄ p₅ q₅}
    (aux : OriginalF45BracketTree.DepthRotationRoute auxBefore auxAfter) :
    signed.independentSquareType aux := by
  cases signed with
  | forward left =>
      exact OriginalF45BracketTree.DepthRotationRoute.IndependentSquare.canonical
        left aux
  | backward left =>
      exact OriginalF45BracketTree.DepthRotationRoute.IndependentSquare.canonical
        left aux

section ActualPentagonPrism

variable {a b : D} {x y : E}
variable {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
variable {p₀ p₁ p₂ p₃ p₄ p₅ : Blocks a b}
variable {q₀ q₁ q₂ q₃ q₄ q₅ : Blocks x y}
variable
  (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
  (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
  (t₃ : OriginalF45BracketTree n₃ m₃ p₂ q₂ p₃ q₃)
  (t₄ : OriginalF45BracketTree n₄ m₄ p₃ q₃ p₄ q₄)

/-- A genuine geometric C60 pentagon-to-hexagon four-flag square
with the actual original F55 one-rotation signed pentagon edge and
an additional independent typed finite F45 route.

The dependent square field provides TWO different, equally counted
Type-valued sequences and their separately proved F44/trace
certificates, with no new higher comparison axiom. -/
structure OriginalF45C60AttachedDepthSquare
    (origin : IcosahedralVertex) (slot : PentagonalSlot)
    {k k' l l' : Nat}
    {auxBefore : OriginalF45BracketTree k l p₄ q₄ p₅ q₅}
    {auxAfter : OriginalF45BracketTree k' l' p₄ q₄ p₅ q₅}
    (aux : OriginalF45BracketTree.DepthRotationRoute auxBefore auxAfter) where
  geometricSide : OriginalF45C60GluedPentagonSide
    t₁ t₂ t₃ t₄ origin slot
  twoOrders : geometricSide.rotation.independentSquareType aux

/-- Attach an ACTUAL two-order original depth-aware square to any
of the FIVE existing physical C60 pentagon boundary edges. -/
noncomputable def originalF45C60AttachedDepthSquare
    (origin : IcosahedralVertex) (slot : PentagonalSlot)
    {k k' l l' : Nat}
    {auxBefore : OriginalF45BracketTree k l p₄ q₄ p₅ q₅}
    {auxAfter : OriginalF45BracketTree k' l' p₄ q₄ p₅ q₅}
    (aux : OriginalF45BracketTree.DepthRotationRoute auxBefore auxAfter) :
    OriginalF45C60AttachedDepthSquare t₁ t₂ t₃ t₄ origin slot aux :=
  {
    geometricSide := originalF45C60GluedPentagonSide
      t₁ t₂ t₃ t₄ origin slot
    twoOrders := SignedOriginalF45PentagonSide.independentSquareCanonical
      (originalF45C60GluedPentagonSide
        t₁ t₂ t₃ t₄ origin slot).rotation aux
  }

/-- The attached two-order square really lies on the original
pentagon/hexagon shared edge, and its signed pentagon-side path
still records EXACTLY one original F54 rotation. -/
theorem originalF45C60AttachedDepthSquare_valid
    (origin : IcosahedralVertex) (slot : PentagonalSlot)
    {k k' l l' : Nat}
    {auxBefore : OriginalF45BracketTree k l p₄ q₄ p₅ q₅}
    {auxAfter : OriginalF45BracketTree k' l' p₄ q₄ p₅ q₅}
    (aux : OriginalF45BracketTree.DepthRotationRoute auxBefore auxAfter) :
    (originalF45C60AttachedDepthSquare
      t₁ t₂ t₃ t₄ origin slot aux).geometricSide.incidenceSquare.firstFace =
        .aroundVertex origin ∧
    (originalF45C60AttachedDepthSquare
      t₁ t₂ t₃ t₄ origin slot aux).geometricSide.rotation.rotationCount =
        1 :=
  originalF45C60GluedPentagonSide_valid
    t₁ t₂ t₃ t₄ origin slot

end ActualPentagonPrism

#print axioms SignedOriginalF45PentagonSide.independentSquareType
#print axioms SignedOriginalF45PentagonSide.independentSquareCanonical
#print axioms OriginalF45C60AttachedDepthSquare
#print axioms originalF45C60AttachedDepthSquare
#print axioms originalF45C60AttachedDepthSquare_valid

end
end KUOS.DependentOriginationTruncatedIcosahedralPentagonRotationBridgeV5_154
