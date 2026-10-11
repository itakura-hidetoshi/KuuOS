import KUOS.DependentOriginationTruncatedIcosahedralCyclicSquareCollarGluingV5_154
import KUOS.DependentOriginationCoherentBiadjunctionOriginalF45HigherCellPastingObstructionV5_153

namespace KUOS.DependentOriginationTruncatedIcosahedralHigherChargeV5_155

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationTruncatedIcosahedralStarRefinementV3_83
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154
open KUOS.DependentOriginationTruncatedIcosahedralPentagonRotationBridgeV5_154
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F58-A / v5.155 — an independent path-sensitive, additive higher-cell target

F56-C/D proves the original F44 and full typed F19/F28-history
observation of a presented higher cell is a subsingleton at a
fixed pair of paths. F57-A–D constructs real closed C60 pentagons
with five signed F55 rotation edges, genuine vertex/face four-flag
incidence squares, and cyclic shared-corner flag pasting.

Here a NEW independently defined additive higher-cell target records
the signed number of genuine freely presented PENTAGON and DISJOINT
SQUARE generators as two integers. The F56-A interpreter is a real
recursive computation on all F55 PresentedCell constructors:
  pentagon -> (1,0); disjoint square -> (0,1);
  formal inverse -> negation; vertical pasting -> addition;
  identity -> zero; four contextual/pasting whiskerings -> unchanged.

We prove actual nonzero pentagon and square signatures, group-like
vertical operation laws, and evaluate the canonical F57-B ORIGINAL
geometric C60 pentagon together with its five real flag squares.
We also attach an independently supplied real pair of F54 local
rotations to any genuine C60 pentagon/hexagon flag square and
evaluate its concrete F55 disjoint-square generator.

This target retains algebraic generator information beyond F44
endpoint equality; it is NOT claimed to be faithful on all raw
free PresentedCell syntax, a geometric map from each C60 edge to
a unique local rotation, or a native Gray/tricategory 3-cell.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- A genuinely independent target of two signed additive generator
charges, not a copy of the source free path-cell structure and not
the Prop-only F44 observational certificate. -/
def OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.generatorCharge :
    OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget D E where
  Cell := fun {a b} {x y} {n n' m m'} {ma mb} {pa pb}
    {first last} _ _ => Int × Int
  ident := fun _ => (0, 0)
  pentagon := fun _ _ _ _ => (1, 0)
  disjointSquare := fun _ _ => (0, 1)
  symm := fun c => -c
  trans := fun c d => c + d
  leftContext := fun c _ => c
  rightContext := fun _ c => c
  precompose := fun _ c => c
  postcompose := fun c _ => c

/-- This is a real signed higher-cell generator signature: the original
five-vertex F55 path pentagon maps to the nonzero pentagon charge. -/
theorem originalF55Pentagon_generatorCharge
    {a b : D} {x y : E}
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    {p₀ p₁ p₂ p₃ p₄ : Blocks a b}
    {q₀ q₁ q₂ q₃ q₄ : Blocks x y}
    (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : OriginalF45BracketTree n₃ m₃ p₂ q₂ p₃ q₃)
    (t₄ : OriginalF45BracketTree n₄ m₄ p₃ q₃ p₄ q₄) :
    (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.pentagon
      t₁ t₂ t₃ t₄).interpret
      OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.generatorCharge =
        ((1 : Int), (0 : Int)) := by
  rfl

/-- The independent genuine F55 local-rotation square maps to the
OTHER nonzero coordinate, rather than being confused with pentagon
length or four Prop-only original F44 observational certificates. -/
theorem originalF55Square_generatorCharge
    {a b : D} {x y : E}
    {n m n' m' : Nat}
    {p₀ p₁ p₂ : Blocks a b} {q₀ q₁ q₂ : Blocks x y}
    {leftBefore leftAfter : OriginalF45BracketTree n m p₀ q₀ p₁ q₁}
    {rightBefore rightAfter : OriginalF45BracketTree n' m' p₁ q₁ p₂ q₂}
    (left : OriginalF45BracketTree.LocalRotation leftBefore leftAfter)
    (right : OriginalF45BracketTree.LocalRotation rightBefore rightAfter) :
    (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.disjointSquare
      left right).interpret
      OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.generatorCharge =
        ((0 : Int), (1 : Int)) := by
  rfl

/-- Actual higher identity is zero under the independent additive
target, instead of a freely invented comparison 3-morphism. -/
theorem originalF55Identity_generatorCharge
    {a b : D} {x y : E}
    {n n' m m' : Nat}
    {p₀ p₁ : Blocks a b} {q₀ q₁ : Blocks x y}
    {first : OriginalF45BracketTree n m p₀ q₀ p₁ q₁}
    {last : OriginalF45BracketTree n' m' p₀ q₀ p₁ q₁}
    (route : OriginalF45BracketTree.DepthRotationRoute first last) :
    (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.ident
      route).interpret
      OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.generatorCharge =
        (0 : Int × Int) := by
  rfl

/-- The target vertical pasting operation is actual addition,
and the native F56 interpreter computes it on real PresentedCell
vertical compositions with no F44 quotient proof replacement. -/
theorem originalF55Pasting_generatorCharge
    {a b : D} {x y : E}
    {n n' m m' : Nat}
    {p₀ p₁ : Blocks a b} {q₀ q₁ : Blocks x y}
    {first : OriginalF45BracketTree n m p₀ q₀ p₁ q₁}
    {last : OriginalF45BracketTree n' m' p₀ q₀ p₁ q₁}
    {r s t : OriginalF45BracketTree.DepthRotationRoute first last}
    (c : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s)
    (d : OriginalF45BracketTree.DepthRotationRoute.PresentedCell s t) :
    (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.trans c d).interpret
      OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.generatorCharge =
      c.interpret
        OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.generatorCharge +
      d.interpret
        OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.generatorCharge := by
  rfl

/-- The ORIGINAL formal higher-cell reversal acts as additive
negation. This does NOT invert any potentially noninvertible
G.toOplax comparison cell. -/
theorem originalF55Reverse_generatorCharge
    {a b : D} {x y : E}
    {n n' m m' : Nat}
    {p₀ p₁ : Blocks a b} {q₀ q₁ : Blocks x y}
    {first : OriginalF45BracketTree n m p₀ q₀ p₁ q₁}
    {last : OriginalF45BracketTree n' m' p₀ q₀ p₁ q₁}
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    (c : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.symm c).interpret
      OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.generatorCharge =
      -(c.interpret
        OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.generatorCharge) := by
  rfl

/-- In the independent target, vertical addition has genuine
associative composition and both zero-unit and inverse laws.
These are algebraic target properties, not inferred external
tricategorical interchange/coherence laws. -/
theorem generatorCharge_additive_laws
    (p q r : Int × Int) :
    (p + q) + r = p + (q + r) ∧
    (0 : Int × Int) + p = p ∧
    p + (0 : Int × Int) = p ∧
    p + -p = 0 := by
  exact ⟨add_assoc p q r, zero_add p, add_zero p, add_neg_cancel p⟩

/-- Each ACTUAL original C60 vertex-origin pentagon from F57-B,
with FIVE separately proved edge-local four-flag squares, has an
independent nonzero higher pentagon-generator signature. -/
theorem originalC60Pentagon_generatorCharge
    {a b : D} {x y : E}
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    {p₀ p₁ p₂ p₃ p₄ : Blocks a b}
    {q₀ q₁ q₂ q₃ q₄ : Blocks x y}
    (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : OriginalF45BracketTree n₃ m₃ p₂ q₂ p₃ q₃)
    (t₄ : OriginalF45BracketTree n₄ m₄ p₃ q₃ p₄ q₄)
    (v : IcosahedralVertex) :
    (originalF45C60PentagonPasting t₁ t₂ t₃ t₄ v).interpret
      OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.generatorCharge =
        ((1 : Int), (0 : Int)) := by
  rfl

/-- The actual C60 pentagon generator is algebraically different
from the higher identity signature. This is strictly richer than
an unlabelled subsingleton of F44 endpoint certificates, without
claiming faithfulness on all raw F55 free PresentedCell terms. -/
theorem originalC60Pentagon_generatorCharge_ne_zero
    {a b : D} {x y : E}
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    {p₀ p₁ p₂ p₃ p₄ : Blocks a b}
    {q₀ q₁ q₂ q₃ q₄ : Blocks x y}
    (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : OriginalF45BracketTree n₃ m₃ p₂ q₂ p₃ q₃)
    (t₄ : OriginalF45BracketTree n₄ m₄ p₃ q₃ p₄ q₄)
    (v : IcosahedralVertex) :
    (originalF45C60PentagonPasting t₁ t₂ t₃ t₄ v).interpret
      OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.generatorCharge ≠
        (0 : Int × Int) := by
  rw [originalC60Pentagon_generatorCharge]
  decide

/-- The concrete F57-A edge-square geometry together with a
GENUINELY chosen pair of independent original F55 local rotations.
It makes explicit that C60 incidence alone does NOT select such a
pair: they must be supplied and their F55 square generator retained. -/
structure OriginalC60FlagSquareWithF55Generator
    (edge : TruncatedIcosahedralAroundEdge)
    {a b : D} {x y : E}
    {n m n' m' : Nat}
    {p₀ p₁ p₂ : Blocks a b} {q₀ q₁ q₂ : Blocks x y}
    {leftBefore leftAfter : OriginalF45BracketTree n m p₀ q₀ p₁ q₁}
    {rightBefore rightAfter : OriginalF45BracketTree n' m' p₁ q₁ p₂ q₂}
    (left : OriginalF45BracketTree.LocalRotation leftBefore leftAfter)
    (right : OriginalF45BracketTree.LocalRotation rightBefore rightAfter) where
  geometricSquare : TruncatedEdgeFlagSquare (.around edge)
  pentagonFace : geometricSquare.firstFace = .aroundVertex edge.center
  squareCell :
    OriginalF45BracketTree.DepthRotationRoute.PresentedCell
      (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right)
      (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right)

/-- Build the F57-A actual C60 pentagon-to-hexagon flag square with
the independently supplied actual F55 disjoint local-rotation square. -/
noncomputable def OriginalC60FlagSquareWithF55Generator.canonical
    (edge : TruncatedIcosahedralAroundEdge)
    {a b : D} {x y : E}
    {n m n' m' : Nat}
    {p₀ p₁ p₂ : Blocks a b} {q₀ q₁ q₂ : Blocks x y}
    {leftBefore leftAfter : OriginalF45BracketTree n m p₀ q₀ p₁ q₁}
    {rightBefore rightAfter : OriginalF45BracketTree n' m' p₁ q₁ p₂ q₂}
    (left : OriginalF45BracketTree.LocalRotation leftBefore leftAfter)
    (right : OriginalF45BracketTree.LocalRotation rightBefore rightAfter) :
    OriginalC60FlagSquareWithF55Generator edge left right :=
  {
    geometricSquare := aroundPentagonHexagonSquare edge
    pentagonFace := rfl
    squareCell :=
      OriginalF45BracketTree.DepthRotationRoute.PresentedCell.disjointSquare
        left right
  }

/-- This authentic four-flag C60 geometric square, labelled with the
ACTUAL F55 independent local-rotation square generator, carries a
nonzero square charge in the independently defined higher target. -/
theorem originalC60FlagSquare_generatorCharge
    (edge : TruncatedIcosahedralAroundEdge)
    {a b : D} {x y : E}
    {n m n' m' : Nat}
    {p₀ p₁ p₂ : Blocks a b} {q₀ q₁ q₂ : Blocks x y}
    {leftBefore leftAfter : OriginalF45BracketTree n m p₀ q₀ p₁ q₁}
    {rightBefore rightAfter : OriginalF45BracketTree n' m' p₁ q₁ p₂ q₂}
    (left : OriginalF45BracketTree.LocalRotation leftBefore leftAfter)
    (right : OriginalF45BracketTree.LocalRotation rightBefore rightAfter) :
    (OriginalC60FlagSquareWithF55Generator.canonical
      edge left right).squareCell.interpret
        OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.generatorCharge =
          ((0 : Int), (1 : Int)) := by
  rfl

#print axioms OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.generatorCharge
#print axioms originalF55Pentagon_generatorCharge
#print axioms originalF55Square_generatorCharge
#print axioms originalF55Identity_generatorCharge
#print axioms originalF55Pasting_generatorCharge
#print axioms originalF55Reverse_generatorCharge
#print axioms generatorCharge_additive_laws
#print axioms originalC60Pentagon_generatorCharge
#print axioms originalC60Pentagon_generatorCharge_ne_zero
#print axioms OriginalC60FlagSquareWithF55Generator
#print axioms OriginalC60FlagSquareWithF55Generator.canonical
#print axioms originalC60FlagSquare_generatorCharge

end
end KUOS.DependentOriginationTruncatedIcosahedralHigherChargeV5_155
