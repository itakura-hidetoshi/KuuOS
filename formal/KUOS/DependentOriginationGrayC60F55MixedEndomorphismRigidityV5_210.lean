import KUOS.DependentOriginationGrayC60F55DirectCompositePhysicalV5_209

namespace KUOS.DependentOriginationGrayC60F55MixedEndomorphismRigidityV5_210

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false

/-!
# F59-F60-C / v5.210: rigidity of endomorphisms of the original F47
# four-boundary mixed three-Hom category

The real mixed SOURCE category has exactly four original boundary
positions and five RAW constructors (identity, original face,
original F55, and two explicitly adjoined comparison arrows),
plus type-correct composition. Every nonidentity generator strictly
increases a finite boundary rank. Thus every RAW endomorphism has
zero complete native Gray evaluation, and the chosen complete-native-
kernel quotient has at most one endomorphism at each boundary tag.

This theorem is about the existing ORIGINAL SOURCE F47 presentation.
It does not equate unlike original F42/F54 types, erase the two
independent integer charges or phase, or assert global descent.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section OriginalFourBoundaryRank

variable {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : Blocks a b} {pa pb : Blocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}
variable {r s : OriginalF45BracketTree.DepthRotationRoute first last}
variable {v w : IcosahedralDart} {p q : Quiver.Path v w}
variable {α β : C60F42PresentedFaceCell p q}
variable (B : C60F47SquareFrame α β r s)

/-- A strict rank on the ORIGINAL four tagged source 2-cell
boundaries. Unlike grading by Gray charge, this does not forget
which of the actual original boundary positions a raw 3-cell joins. -/
def c60F61FourBoundaryRank : C60F47BoundaryPoint B → Nat
  | .faceBefore => 0
  | .faceAfter => 1
  | .rotationBefore => 1
  | .rotationAfter => 2

/-- Every ACTUAL source F47 constructor is rank-nondecreasing;
each nonidentity primitive is strictly rank-increasing. -/
theorem c60F61RawThreeCell_rank_mono
    {X Y : C60F47BoundaryPoint B}
    (f : C60F47PresentedMixedThreeCell B X Y) :
    c60F61FourBoundaryRank B X ≤ c60F61FourBoundaryRank B Y := by
  induction f with
  | ident _ => exact le_rfl
  | originalFace => decide
  | originalF55 => decide
  | compareBefore => decide
  | compareAfter => decide
  | trans f g hf hg => exact hf.trans hg

/-- No source F47 raw path can return to its original rank
with a positive-rank edge. Thus equal-rank raw paths have ZERO
complete native evaluation, including BOTH integer charges and phase. -/
theorem c60F61RawThreeCell_same_rank_native_zero
    {X Y : C60F47BoundaryPoint B}
    (f : C60F47PresentedMixedThreeCell B X Y) :
    c60F61FourBoundaryRank B X = c60F61FourBoundaryRank B Y →
      f.toNative = 0 := by
  induction f with
  | ident _ =>
      intro _
      rfl
  | originalFace =>
      intro h
      simp [c60F61FourBoundaryRank] at h
  | originalF55 =>
      intro h
      simp [c60F61FourBoundaryRank] at h
  | compareBefore =>
      intro h
      simp [c60F61FourBoundaryRank] at h
  | compareAfter =>
      intro h
      simp [c60F61FourBoundaryRank] at h
  | trans f g hf hg =>
      intro h
      have hleft : f.toNative = 0 := hf (by
        have h₁ := c60F61RawThreeCell_rank_mono B f
        have h₂ := c60F61RawThreeCell_rank_mono B g
        omega)
      have hright : g.toNative = 0 := hg (by
        have h₁ := c60F61RawThreeCell_rank_mono B f
        have h₂ := c60F61RawThreeCell_rank_mono B g
        omega)
      change f.toNative + g.toNative = (0 : GradedThreeCell 0 0)
      simp only [hleft, hright, zero_add]

/-- The COMPLETE native value of any endomorphism of a genuine
F47 boundary tag is exactly zero; this uses the raw source rank,
not a statement about forgetting the signed Gray charges. -/
theorem c60F61MixedEndomorphism_native_zero
    (X : C60F47BoundaryPoint B) (f : X ⟶ X) :
    c60F47MixedEval f = 0 := by
  refine Quot.inductionOn f (fun raw => ?_)
  exact c60F61RawThreeCell_same_rank_native_zero B raw rfl

/-- F47 four-tag endomorphisms are unique in the existing
FULL native-kernel quotient. In particular, two source natural
isomorphism components on one and the same tagged boundary are
genuinely equal there, not just after an uncontrolled grade map. -/
theorem c60F61MixedEndomorphism_unique
    (X : C60F47BoundaryPoint B) (f g : X ⟶ X) : f = g := by
  apply c60F47MixedGrayFunctor_faithful B
  change c60F47MixedEval f = c60F47MixedEval g
  rw [c60F61MixedEndomorphism_native_zero B X f,
    c60F61MixedEndomorphism_native_zero B X g]

#print axioms c60F61RawThreeCell_rank_mono
#print axioms c60F61RawThreeCell_same_rank_native_zero
#print axioms c60F61MixedEndomorphism_native_zero
#print axioms c60F61MixedEndomorphism_unique

end OriginalFourBoundaryRank
end KUOS.DependentOriginationGrayC60F55MixedEndomorphismRigidityV5_210
