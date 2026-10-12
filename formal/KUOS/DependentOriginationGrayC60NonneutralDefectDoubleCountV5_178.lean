import KUOS.DependentOriginationGrayC60F55NonneutralBraidingTransportV5_177
import KUOS.DependentOriginationGrayC60AllThirtyTwoFaceCycleV5_158

namespace KUOS.DependentOriginationGrayC60NonneutralDefectDoubleCountV5_178

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayC60F55NonneutralBraidingTransportV5_177
open KUOS.DependentOriginationGrayC60AllThirtyTwoFaceCycleV5_158
open KUOS.DependentOriginationTruncatedIcosahedralCrossHexagonFlagSquaresV5_157
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F59-F30 / v5.178 — nonneutral F55 source braid defect over actual C60 geometry

F59-F29 constructed genuinely nonneutral braided 3-cells on all original
90 physical C60 F55 squares, and proved that their INDEPENDENT phase
defect is a*b even when the F58 square charge stays fixed at (0,1).

We now transport that exact source-typed defect through the F59-F7
real all-32-face incidence geometry. Any finite subset S of original
90 edges has total defect |S|*(a*b) mod 2, so an individual odd/odd
edge detects nonzero independent braid data. On the full 90-edge
carrier the sum is zero; on all 32 real face boundaries it is zero
coefficientwise because EVERY physical edge occurs exactly twice.

Crucially this is a statement about the ORIGINAL geometrically
attached F55 source cell plus the separately supplied native Gray
interchanger. It is not a claim that the source F55 freely presented
cell itself possesses an external braiding or that Stage-II omega
has been computed. The full-surface cancellation is true for any
edge-dependent defect weight, not only the uniform F29 case.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section ActualC60Source
variable {x y : D} {z w : E}
variable {n₁ n₂ m₁ m₂ : Nat}
variable {p₀ p₁ p₂ : Blocks x y}
variable {q₀ q₁ q₂ : Blocks z w}
variable
  (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
  (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
variable
  {leftAfter : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁}
  {rightAfter : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂}
  (left : OriginalF45BracketTree.LocalRotation t₁ leftAfter)
  (right : OriginalF45BracketTree.LocalRotation t₂ rightAfter)

/-- Independent F29 defect of the genuine original physical F55
square together with the NONNEUTRAL native a/b Gray braid. -/
def c60F30OriginalSquareDefect (a b : ZMod 2)
    (edge : TruncatedIcosahedralEdge) : ZMod 2 :=
  c60F29PhaseDefect
    (c60F29ActualBraidedSquare t₁ t₂ left right a b edge)

/-- Every physical square retains the SAME independent native
braid defect a*b; this is not inferred from the old integer charge. -/
theorem c60F30OriginalSquareDefect_eq
    (a b : ZMod 2) (edge : TruncatedIcosahedralEdge) :
    c60F30OriginalSquareDefect t₁ t₂ left right a b edge = a * b := by
  rw [c60F30OriginalSquareDefect,
    c60F29ActualBraidedSquare_eq_originalSource]
  exact c60F29BraidedSource_defect a b
    (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.disjointSquare left right)

/-- For an arbitrary PHYSICAL finite C60 edge subpatch, sum
the independent defect of each genuine source-labelled braided cell. -/
def c60F30SourceDefectPatch (a b : ZMod 2)
    (S : Finset TruncatedIcosahedralEdge) : ZMod 2 :=
  ∑ edge ∈ S, c60F30OriginalSquareDefect t₁ t₂ left right a b edge

/-- The exact local-to-global F29 source/Gray defect:
the number of actual edges times the independent a*b phase. -/
theorem c60F30SourceDefectPatch_eq
    (a b : ZMod 2) (S : Finset TruncatedIcosahedralEdge) :
    c60F30SourceDefectPatch t₁ t₂ left right a b S =
      (S.card : ZMod 2) * (a * b) := by
  unfold c60F30SourceDefectPatch
  simp_rw [c60F30OriginalSquareDefect_eq t₁ t₂ left right a b]
  simp

/-- The physical odd/odd independent braiding remains nonzero
even for ONE genuine original C60 F55 four-flag square. -/
theorem c60F30OddOddSingleSquare_nonzero
    (edge : TruncatedIcosahedralEdge) :
    c60F30OriginalSquareDefect t₁ t₂ left right 1 1 edge ≠ 0 := by
  rw [c60F30OriginalSquareDefect_eq]
  decide

/-- On all 90 physically distinct C60 squares, each original
source/Gray braided defect appears once, and its total is zero. -/
theorem c60F30AllNinetySourceDefect_zero
    (a b : ZMod 2) :
    c60F30SourceDefectPatch t₁ t₂ left right a b Finset.univ = 0 := by
  rw [c60F30SourceDefectPatch_eq, Finset.card_univ]
  rw [allOriginalTruncatedEdge_card_kernel]
  have h90 : (90 : ZMod 2) = 0 := by decide
  change (90 : ZMod 2) * (a * b) = 0
  rw [h90, zero_mul]

/-- The stronger FULL original C60 surface boundary identity:
sum the SOURCE-TYPED F55/nonneutral-Gray independent defect along
each of 32 REAL polygonal face boundaries. Geometric multiplicity
two at EVERY edge forces total phase zero over ZMod2. -/
theorem c60F30ThirtyTwoFaceSourceDefect_zero
    (a b : ZMod 2) :
    (∑ face : TruncatedIcosahedralSeedFace,
      ((kernelC60FullFaceBoundaryEdges face).map
        (c60F30OriginalSquareDefect t₁ t₂ left right a b)).sum) = 0 := by
  rw [kernelC60FullSurfaceWeightedDoubleCount
    (c60F30OriginalSquareDefect t₁ t₂ left right a b)]
  have htwo : (2 : ZMod 2) = 0 := by decide
  simp [nsmul_eq_mul, htwo]

/-- This is NOT merely special to equal source-cell labels:
the entire original C60 all-32-face incidence geometry cancels
ANY independently prescribed mod-two edge defect. -/
theorem c60F30AnyEdgeDefect_surface_zero
    (defect : TruncatedIcosahedralEdge → ZMod 2) :
    (∑ face : TruncatedIcosahedralSeedFace,
      ((kernelC60FullFaceBoundaryEdges face).map defect).sum) = 0 := by
  rw [kernelC60FullSurfaceWeightedDoubleCount defect]
  have htwo : (2 : ZMod 2) = 0 := by decide
  simp [nsmul_eq_mul, htwo]

#print axioms c60F30OriginalSquareDefect
#print axioms c60F30OriginalSquareDefect_eq
#print axioms c60F30SourceDefectPatch
#print axioms c60F30SourceDefectPatch_eq
#print axioms c60F30OddOddSingleSquare_nonzero
#print axioms c60F30AllNinetySourceDefect_zero
#print axioms c60F30ThirtyTwoFaceSourceDefect_zero
#print axioms c60F30AnyEdgeDefect_surface_zero

end ActualC60Source
end
end KUOS.DependentOriginationGrayC60NonneutralDefectDoubleCountV5_178
