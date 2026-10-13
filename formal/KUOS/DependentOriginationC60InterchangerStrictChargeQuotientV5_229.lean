import KUOS.DependentOriginationC60OriginalSourceInterchangerNaturalityV5_228
import KUOS.DependentOriginationC60PhysicalCechCurvatureRepairV5_222

namespace KUOS.DependentOriginationC60InterchangerStrictChargeQuotientV5_229

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60NativePathFunctorV5_189
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalPresentationV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalThreeHomV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalCompositionV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalGrayCoherenceV5_199
open KUOS.DependentOriginationC60OriginalStrictThreeArrowsV5_227
open KUOS.DependentOriginationC60OriginalSourceInterchangerNaturalityV5_228
open KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196
open KUOS.DependentOriginationGrayC60IntegralBoundaryLinearMapV5_159
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationC60ArbitraryAtlasNerveDescentV5_219
open KUOS.DependentOriginationC60FiniteAtlasCechCoherenceV5_221
open KUOS.DependentOriginationC60PhysicalCechCurvatureRepairV5_222
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.229 / F75: KILL original F43 interchange phase in a new strict charge quotient

THE USER CHOOSES a DIFFERENT STRICTIFICATION instead of preserving
the nontrivial odd/odd original north-pentagon Gray exchange.
Do not change or falsify the old F42/F43 source. Instead add an
explicit CATEGORY QUOTIENT and prove which data it identifies.

The new target identifies ORIGINAL face 2-cell objects according
to their ZMod2 total degree, and identifies original source
three-arrows iff their TWO INTEGER charges match. It discards
the independent ZMod2 exchange phase, so the genuine source F43
left-first/right-first interchanger is IDENTIFIED WITH THE IDENTITY
arrow after its previously distinct endpoint 2-cells have been
identified. In particular the original NORTH C60 pentagon is
collapsed to an identity in this new quotient, even though it was
nontrivial before quotienting. This is an intentional CHANGE OF
THEORY, not an incorrect proof that the old cell was originally zero.

The projection preserves genuine original F42/F43/F51 source
vertical composition, both original integer charge coordinates,
and source face degrees. The independent physical F54/F55 mixed
four-tag category has its own native charge projection.
The true nonzero mixed comparison charge (0,1) SURVIVES.
The original 90-edge/32-face physical north-pentagon second
integer curvature -5 ALSO SURVIVES phase removal.

This is an actual strict one-dimensional Hom-category quotient,
a first step toward stricter THREE-categorical composition.
It does NOT yet establish a globally fully strict 3-category
with every mixed source F54/F55 horizontal coherence law.
-/

/-- A strictified face-2-cell LABEL retaining exact total ZMod2
degree, but intentionally not the two different original F42
left-first/right-first witnesses. -/
structure C60F75StrictChargeGrade where
  degree : ZMod 2
  deriving DecidableEq

/-- Phase-free STRICT three-arrows retain BOTH independent
integer source charges, but no independent F59 exchange phase. -/
structure C60F75StrictChargeThree
    (X Y : C60F75StrictChargeGrade) where
  gradeEq : X.degree = Y.degree
  charge : Int × Int

/-- For fixed strictified 2-cell boundaries, the complete
morphism equality relation is EXACTLY equality of both integer charges. -/
theorem C60F75StrictChargeThree.ext
    {X Y : C60F75StrictChargeGrade}
    {f g : C60F75StrictChargeThree X Y}
    (h : f.charge = g.charge) : f = g := by
  cases f with
  | mk hf cf =>
    cases g with
    | mk hg cg =>
      cases h
      rfl

/-- Equality transport is the zero-charge identity in the
strict quotient, including when the source-object equality arose
from a real original nontrivial F43 interchange. -/
theorem C60F75StrictChargeThree.eqToHom_charge_zero
    {X Y : C60F75StrictChargeGrade} (h : X = Y) :
    (eqToHom h : X ⟶ Y).charge = (0 : Int × Int) := by
  cases h
  rfl

/-- A genuinely CONSTRUCTED strict Mathlib category: same-grade
arrows carry the product group ℤ × ℤ with strictly associative
addition, both units and both independent charge components.
The former nontrivial F59 odd/odd braiding phase is absent. -/
instance : Category C60F75StrictChargeGrade where
  Hom := C60F75StrictChargeThree
  id X := ⟨rfl, 0⟩
  comp f g := ⟨f.gradeEq.trans g.gradeEq, f.charge + g.charge⟩
  id_comp := by
    intro X Y f
    apply C60F75StrictChargeThree.ext
    exact zero_add f.charge
  comp_id := by
    intro X Y f
    apply C60F75StrictChargeThree.ext
    exact add_zero f.charge
  assoc := by
    intro W X Y Z f g h
    apply C60F75StrictChargeThree.ext
    exact add_assoc f.charge g.charge h.charge

/-- The concrete quotient/evaluation of the ORIGINAL native
F59 Gray category: two integer charges and two-cell degree survive,
and ONLY the extra independent ZMod2 exchange phase is discarded. -/
def c60F75ForgetGrayExchangePhase :
    GrayGrade ⥤ C60F75StrictChargeGrade where
  obj X := ⟨X.degree⟩
  map := fun {X Y} f => ⟨f.gradeEq, f.charge⟩
  map_id := by
    intro X
    apply C60F75StrictChargeThree.ext
    rfl
  map_comp := by
    intro X Y Z f g
    apply C60F75StrictChargeThree.ext
    rfl

/-- All original F42/F43/F51 THREE-ARROWS act on the quotient
through the real source three-Hom category first, followed by
its already constructed native full-Gray functor. -/
def c60F75OriginalFaceStrictification
    {v w : IcosahedralDart}
    (p q : Quiver.Path v w) :
    C60F51OriginalTwo p q ⥤ C60F75StrictChargeGrade :=
  c60F51GrayFunctor p q ⋙ c60F75ForgetGrayExchangePhase

/-- The old raw F42/F43 source category likewise maps via
the existing ORIGINAL F43 inclusion, NOT directly from raw words
into invented source-level category equalities. -/
def c60F75OriginalF43Strictification
    {v w : IcosahedralDart}
    (p q : Quiver.Path v w) :
    C60F42PresentedFaceCell p q ⥤ C60F75StrictChargeGrade :=
  c60F51OriginalInclusion p q ⋙
    c60F75OriginalFaceStrictification p q

/-- The new strictified 2-cell object retains the EXACT
original source F42 face-degree from the true F51 witness. -/
theorem c60F75OriginalFaceStrictification_degree
    {v w : IcosahedralDart}
    {p q : Quiver.Path v w}
    (X : C60F51OriginalTwo p q) :
    ((c60F75OriginalFaceStrictification p q).obj X).degree =
      c60F43FaceDegree X.original := rfl

/-- The source F43/F51 three-arrow maps to precisely its two
native integer charges. A separate F59 exchange phase is discarded. -/
theorem c60F75OriginalFaceStrictification_charge
    {v w : IcosahedralDart}
    {p q : Quiver.Path v w}
    {X Y : C60F51OriginalTwo p q}
    (f : X ⟶ Y) :
    ((c60F75OriginalFaceStrictification p q).map f).charge =
      (c60F51Eval f).charge := rfl

/-- The TWO genuinely different F42 horizontal pastings
become EQUAL objects in the deliberately STRICTIFIED target.
This equality follows from the original source F43 three-arrow
degree-preservation, not an unfounded raw F42 equality. -/
theorem c60F75OriginalInterchanger_objects_identified
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (X : C60F51OriginalTwo p q)
    (Y : C60F51OriginalTwo r s) :
    (c60F75OriginalFaceStrictification (p.comp r) (q.comp s)).obj
        (c60F51OriginalTwoHorizontal X Y) =
    (c60F75OriginalFaceStrictification (p.comp r) (q.comp s)).obj
        (c60F51OriginalTwoHorizontalRight X Y) := by
  exact congrArg C60F75StrictChargeGrade.mk
    (c60F51Hom_degreeEq (c60F51OriginalInterchanger X Y))

/-- THE PRIMARY NEW STRICTIFICATION THEOREM.
Every genuine ORIGINAL F43 interchanger is sent to the
identity transport after identifying the original two
horizontal F42 pasting objects in the new phase-killing quotient.
In particular this handles the ACTUAL NORTH PENTAGON. -/
theorem c60F75OriginalInterchanger_collapses
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (X : C60F51OriginalTwo p q)
    (Y : C60F51OriginalTwo r s) :
    (c60F75OriginalFaceStrictification (p.comp r) (q.comp s)).map
        (c60F51OriginalInterchanger X Y) =
      eqToHom (c60F75OriginalInterchanger_objects_identified X Y) := by
  apply C60F75StrictChargeThree.ext
  calc
    ((c60F75OriginalFaceStrictification (p.comp r) (q.comp s)).map
        (c60F51OriginalInterchanger X Y)).charge =
      (c60F51Eval (c60F51OriginalInterchanger X Y)).charge :=
      c60F75OriginalFaceStrictification_charge _
    _ = (0 : Int × Int) :=
      (c60F51OriginalInterchanger_nativeComponents X Y).1
    _ = (eqToHom
          (c60F75OriginalInterchanger_objects_identified X Y)).charge :=
      (C60F75StrictChargeThree.eqToHom_charge_zero _).symm

/-- The SAME ACTUAL original north C60 pentagon now has its
previously nonidentity F43 source exchange reduced to an
identity in the new strict quotient, rather than in the old source. -/
theorem c60F75NorthOriginalInterchanger_collapses :
    (c60F75OriginalFaceStrictification
       ((c60F41PentagonBoundaryLoop .north).comp
          (c60F41PentagonBoundaryLoop .north))
       (Quiver.Path.nil.comp Quiver.Path.nil)).map
         c60F51NorthOriginalInterchanger =
      eqToHom
        (c60F75OriginalInterchanger_objects_identified
          c60F51NorthFaceSourceTwo c60F51NorthFaceSourceTwo) :=
  c60F75OriginalInterchanger_collapses
    c60F51NorthFaceSourceTwo c60F51NorthFaceSourceTwo

/-- The original north F43 interchange USED TO carry phase=1
before the explicitly selected quotient. There is no contradiction:
the quotient intentionally forgets the phase, and identifies
the two original boundary objects as above. -/
theorem c60F75North_originalPhaseOne_quotientIdentity :
    (c60F51Eval c60F51NorthOriginalInterchanger).phase =
      (1 : ZMod 2) ∧
    (c60F75OriginalFaceStrictification
       ((c60F41PentagonBoundaryLoop .north).comp
          (c60F41PentagonBoundaryLoop .north))
       (Quiver.Path.nil.comp Quiver.Path.nil)).map
         c60F51NorthOriginalInterchanger =
      eqToHom
        (c60F75OriginalInterchanger_objects_identified
          c60F51NorthFaceSourceTwo c60F51NorthFaceSourceTwo) :=
  ⟨c60F51NorthOriginalInterchanger_phaseOne,
    c60F75NorthOriginalInterchanger_collapses⟩

/-! ## Independent F54/F55 mixed source and physical curvature -/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section GenuineF47Sources
variable {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : Blocks a b} {pa pb : Blocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}
variable {v w : IcosahedralDart} {p q : Quiver.Path v w}
variable {α β : C60F42PresentedFaceCell p q}
variable {r s : OriginalF45BracketTree.DepthRotationRoute first last}

/-- Original four-boundary F42/F54/F55 source three-arrows
also admit a genuine STRICT charge-only quotient functor. -/
def c60F75MixedStrictification
    (B : C60F47SquareFrame α β r s) :
    C60F47BoundaryPoint B ⥤ C60F75StrictChargeGrade :=
  c60F47MixedGrayFunctor B ⋙ c60F75ForgetGrayExchangePhase

/-- The TRUE adjoined original mixed F47 comparison retains its
NONZERO integer-generator charge (0,1) after phase strictification.
Hence NOT all original F55/Delta physical structure is collapsed. -/
theorem c60F75F47Comparison_charge_survives
    (B : C60F47SquareFrame α β r s) :
    ((c60F75MixedStrictification B).map
      (c60F47CompareAfter B)).charge = ((0 : Int), (1 : Int)) := by
  exact (c60F47CompareAfter_native_components B).1

theorem c60F75F47Comparison_remains_nonzero
    (B : C60F47SquareFrame α β r s) :
    ((c60F75MixedStrictification B).map
      (c60F47CompareAfter B)).charge ≠ (0 : Int × Int) := by
  rw [c60F75F47Comparison_charge_survives]
  norm_num

end GenuineF47Sources

section ActualNorthCurvature
variable {a b : D} {x y : E}
variable {n₁ n₂ m₁ m₂ : Nat}
variable {p₀ p₁ p₂ : Blocks a b} {q₀ q₁ q₂ : Blocks x y}
variable
  (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
  (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
variable
  {leftAfter : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁}
  {rightAfter : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂}
  (left : OriginalF45BracketTree.LocalRotation t₁ leftAfter)
  (right : OriginalF45BracketTree.LocalRotation t₂ rightAfter)

/-- The ACTUAL north-pentagon signed physical Čech curvature
still has SECOND integer charge -5 even in the new strict
phase-forgetting quotient. In particular phase-killing DOES
NOT AUTOMATICALLY produce an uncorrected global flat gauge. -/
theorem c60F75NorthCurvature_secondCharge_survives
    (sigma : C60F67Atlas) :
    (((c60F75ForgetGrayExchangePhase).map
      (c60F68PhysicalPatchCurvature t₁ t₂ left right sigma
        (Finsupp.single (.aroundVertex .north) (1 : ℤ)))).charge).2 =
          (-5 : ℤ) :=
  c60F68PhysicalPatchCurvature_northSecondCharge
    t₁ t₂ left right sigma

/-- The genuine physical north curvature remains NONIDENTITY
after collapsing all independent exchange phases, since the
original second integer generator charge is still nonzero. -/
theorem c60F75NorthCurvature_notIdentity_afterQuotient
    (sigma : C60F67Atlas) :
    (c60F75ForgetGrayExchangePhase).map
        (c60F68PhysicalPatchCurvature t₁ t₂ left right sigma
          (Finsupp.single (.aroundVertex .north) (1 : ℤ))) ≠
      (𝟙 (⟨0⟩ : C60F75StrictChargeGrade)) := by
  intro h
  have hCharge := congrArg
    (fun g : C60F75StrictChargeThree ⟨0⟩ ⟨0⟩ => g.charge.2) h
  change
    ((c60F75ForgetGrayExchangePhase).map
      (c60F68PhysicalPatchCurvature t₁ t₂ left right sigma
        (Finsupp.single (.aroundVertex .north) (1 : ℤ)))).charge.2 =
      (0 : ℤ) at hCharge
  rw [c60F75NorthCurvature_secondCharge_survives] at hCharge
  norm_num at hCharge

end ActualNorthCurvature

#print axioms C60F75StrictChargeThree
#print axioms C60F75StrictChargeThree.ext
#print axioms C60F75StrictChargeThree.eqToHom_charge_zero
#print axioms c60F75ForgetGrayExchangePhase
#print axioms c60F75OriginalFaceStrictification
#print axioms c60F75OriginalF43Strictification
#print axioms c60F75OriginalFaceStrictification_degree
#print axioms c60F75OriginalFaceStrictification_charge
#print axioms c60F75OriginalInterchanger_objects_identified
#print axioms c60F75OriginalInterchanger_collapses
#print axioms c60F75NorthOriginalInterchanger_collapses
#print axioms c60F75North_originalPhaseOne_quotientIdentity
#print axioms c60F75MixedStrictification
#print axioms c60F75F47Comparison_charge_survives
#print axioms c60F75F47Comparison_remains_nonzero
#print axioms c60F75NorthCurvature_secondCharge_survives
#print axioms c60F75NorthCurvature_notIdentity_afterQuotient

end
end KUOS.DependentOriginationC60InterchangerStrictChargeQuotientV5_229
