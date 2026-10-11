import KUOS.DependentOriginationGrayC60F55NonneutralBraidingTransportV5_177
import Mathlib.CategoryTheory.Monoidal.Functor

namespace KUOS.DependentOriginationGrayC60F55ParityMonoidalProjectionV5_179

open CategoryTheory
open scoped CategoryTheory.MonoidalCategory
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60F55SourcePhaseLockedAtlasV5_175
open KUOS.DependentOriginationGrayC60F55SourceWhiskeringInterchangeV5_176
open KUOS.DependentOriginationGrayC60F55NonneutralBraidingTransportV5_177
open KUOS.DependentOriginationGrayC60WangBiNativeHigherCoherenceV5_171
open KUOS.DependentOriginationGrayC60WangBiFourImageSixQiF55NaturalityV5_172
open KUOS.DependentOriginationGrayC60WangBiGaugeCollarSixQiCoherenceV5_173
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayC60AllNinetyEdgePastingV5_157
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F31 / v5.179 — genuinely monoidal F55-compatible parity projection

The genuine F59 native braided monoidal CATEGORY of ZMod2-graded
2-cells and nontrivial 3-cells carries a phase independent of the
original F58 integer charges. Actual raw F55 PresentedCells, however,
have an exact parity constraint from F59-F27:

   phase = second F58 square-generator charge modulo 2.

F59-F29 transports raw F55 higher witnesses to arbitrary nonneutral
grade and adds the independently supplied *native* Gray interchanger.
The additional phase defect is a*b, and for odd/odd the interchanger
is distinct from identity even though its charge is (0,0).

Here define an exact NON-IDENTITY ENDOfunctor on the full native
category GrayGrade which preserves the physical graded 2-cell objects
and both original Int generator charges but projects any 3-cell's
independent phase onto the F55-compatible parity:
     (qP,qS;phi) -> (qP,qS;qS mod 2).

Proof includes genuine Mathlib Functor identity/composition, native
monoidal tensor and left/right whiskering, then an ACTUAL Mathlib
strong MONOIDAL functor structure with identity tensorators. The
full native Gray braiding is NOT preserved: the odd/odd braid gets
mapped to identity, precisely because that phase is independent of
source F55 charge. This is why one must not assert the F55 source
already has this independent target braiding.

The projection fixes every actual raw typed F55 PresentedCell
(including all nine constructors and nonneutral source lifts),
yet removes ONLY the external braid phase from F59-F29 compositions.
It is applied to all ninety real F54/F55 C60 physical square cells
and their 360 Wang Bi incidence flags, without adding edges or faces.

No false source-level interchange or full ambient Gray 3-functor.
-/

/-- Preserve the actual ZMod2-grade boundary and both INTEGER
F58 generator charges, while replacing just the independent phase
by the parity forced on original F55 PresentedCells. -/
def c60F31ParityCell {a b : ZMod 2}
    (p : GradedThreeCell a b) : GradedThreeCell a b :=
  ⟨p.gradeEq, p.charge, (p.charge.2 : ZMod 2)⟩

theorem c60F31ParityCell_charge {a b : ZMod 2}
    (p : GradedThreeCell a b) :
    (c60F31ParityCell p).charge = p.charge := rfl

theorem c60F31ParityCell_phase {a b : ZMod 2}
    (p : GradedThreeCell a b) :
    (c60F31ParityCell p).phase = (p.charge.2 : ZMod 2) := rfl

/-- Rephasing is exactly a projection onto ZERO independent
F59-F29 braid defect, for any typed nonneutral Gray 3-cell. -/
theorem c60F31ParityCell_defect_zero {a b : ZMod 2}
    (p : GradedThreeCell a b) :
    c60F29PhaseDefect (c60F31ParityCell p) = 0 := by
  simp [c60F29PhaseDefect, c60F31ParityCell]

theorem c60F31ParityCell_ident (a : ZMod 2) :
    c60F31ParityCell (GradedThreeCell.ident a) =
      GradedThreeCell.ident a := by
  apply GradedThreeCell.ext <;> rfl

/-- A real morphism-preserving operation: parallel Gray 3-cell
VERTICAL composition is preserved with all F58 charges. -/
theorem c60F31ParityCell_comp
    {a b c : ZMod 2}
    (p : GradedThreeCell a b) (q : GradedThreeCell b c) :
    c60F31ParityCell (p.comp q) =
      (c60F31ParityCell p).comp (c60F31ParityCell q) := by
  apply GradedThreeCell.ext
  · rfl
  · change ((p.charge.2 + q.charge.2 : ℤ) : ZMod 2) =
      (p.charge.2 : ZMod 2) + (q.charge.2 : ZMod 2)
    rw [Int.cast_add]

/-- Genuine MONOIDAL bifunctor tensor composition is preserved,
including nonneutral 2-cell grades and both charge coordinates. -/
theorem c60F31ParityCell_tensor
    {a b c d : ZMod 2}
    (p : GradedThreeCell a b) (q : GradedThreeCell c d) :
    c60F31ParityCell (p.tensor q) =
      (c60F31ParityCell p).tensor (c60F31ParityCell q) := by
  apply GradedThreeCell.ext
  · rfl
  · change ((p.charge.2 + q.charge.2 : ℤ) : ZMod 2) =
      (p.charge.2 : ZMod 2) + (q.charge.2 : ZMod 2)
    rw [Int.cast_add]

theorem c60F31ParityCell_inv
    {a b : ZMod 2} (p : GradedThreeCell a b) :
    c60F31ParityCell p.inv = (c60F31ParityCell p).inv := by
  apply GradedThreeCell.ext
  · rfl
  · change ((-p.charge.2 : ℤ) : ZMod 2) =
      -(p.charge.2 : ZMod 2)
    rw [Int.cast_neg]

/-- IDEMPOTENT on all original native 3-cells, not just
separately chosen F55 generator values. -/
theorem c60F31ParityCell_idempotent {a b : ZMod 2}
    (p : GradedThreeCell a b) :
    c60F31ParityCell (c60F31ParityCell p) = c60F31ParityCell p := by
  apply GradedThreeCell.ext <;> rfl

/-- Exact FIXED-POINT criterion: a nonneutral native 3-cell
is fixed precisely when it has no independent braided defect. -/
theorem c60F31ParityCell_fixed_iff {a b : ZMod 2}
    (p : GradedThreeCell a b) :
    c60F31ParityCell p = p ↔ c60F29PhaseDefect p = 0 := by
  constructor
  · intro h
    have hp := congrArg GradedThreeCell.phase h
    change (p.charge.2 : ZMod 2) = p.phase at hp
    simp [c60F29PhaseDefect, hp.symm]
  · intro h
    have hp : p.phase = (p.charge.2 : ZMod 2) :=
      sub_eq_zero.mp h
    apply GradedThreeCell.ext
    · rfl
    · exact hp.symm

/-- A REAL, not identity, Mathlib ENDOfunctor of the native
monoidal category of F59 graded higher 2- and 3-cells. -/
def c60F31ParityFunctor : GrayGrade ⥤ GrayGrade where
  obj := id
  map := fun {_ _} p => c60F31ParityCell p
  map_id := by
    intro X
    exact c60F31ParityCell_ident X.degree
  map_comp := by
    intro X Y Z p q
    exact c60F31ParityCell_comp p q

/-- The Functor is strict on genuine native object degrees. -/
theorem c60F31ParityFunctor_obj (X : GrayGrade) :
    c60F31ParityFunctor.obj X = X := rfl

/-- A concrete exact criterion for the functor to act trivially
on a morphism: membership in the phase-compatible original F55 image. -/
theorem c60F31ParityFunctor_map_fixed_iff
    {X Y : GrayGrade} (p : X ⟶ Y) :
    c60F31ParityFunctor.map p = p ↔ c60F29PhaseDefect p = 0 :=
  c60F31ParityCell_fixed_iff p

/-- The underlying original monoidal tensor is STRICTLY
preserved by the phase projection, before tensorator witnesses. -/
theorem c60F31ParityFunctor_tensor
    {X Y Z W : GrayGrade} (p : X ⟶ Y) (q : Z ⟶ W) :
    c60F31ParityFunctor.map (p ⊗ₘ q) =
      (c60F31ParityFunctor.map p) ⊗ₘ
        (c60F31ParityFunctor.map q) :=
  c60F31ParityCell_tensor p q

/-- The native left whiskering preserves the FULL F55 integer charge
while dropping only the extra independent braided phase. -/
theorem c60F31ParityFunctor_whiskerLeft
    (X : GrayGrade) {Y Z : GrayGrade} (p : Y ⟶ Z) :
    c60F31ParityFunctor.map (X ◁ p) =
      X ◁ (c60F31ParityFunctor.map p) := by
  exact c60F31ParityCell_tensor (GradedThreeCell.ident X.degree) p

theorem c60F31ParityFunctor_whiskerRight
    {X Y : GrayGrade} (p : X ⟶ Y) (Z : GrayGrade) :
    c60F31ParityFunctor.map (p ▷ Z) =
      (c60F31ParityFunctor.map p) ▷ Z := by
  exact c60F31ParityCell_tensor p (GradedThreeCell.ident Z.degree)

/-- A GENUINE Mathlib strong MONOIDAL structure on the independently
defined nonidentity Gray phase-projection functor, with strict
identity unit and tensor comparison ISOMORPHISMS. -/
def c60F31ParityCoreMonoidal :
    c60F31ParityFunctor.CoreMonoidal where
  εIso := Iso.refl _
  μIso := fun X Y => Iso.refl _
  μIso_hom_natural_left := by
    intro X Y p Z
    simpa using (c60F31ParityFunctor_whiskerRight p Z).symm
  μIso_hom_natural_right := by
    intro X Y Z p
    simpa using (c60F31ParityFunctor_whiskerLeft Z p).symm
  associativity := by
    intro X Y Z
    apply GradedThreeCell.ext <;>
      rfl
  left_unitality := by
    intro X
    apply GradedThreeCell.ext <;>
      rfl
  right_unitality := by
    intro X
    apply GradedThreeCell.ext <;>
      rfl

/-- The native mathlib MONOIDAL FUNCTOR instance: this is not
a hand-written fake set of associativity equalities. -/
instance c60F31ParityMonoidalFunctor :
    c60F31ParityFunctor.Monoidal :=
  c60F31ParityCoreMonoidal.toMonoidal

/- All ORIGINAL source F55 proof-relevant PresentedCells are fixed
by the monoidal rephasing functor, at ANY nonneutral 2-cell grade. -/
universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

theorem c60F31ParityFunctor_fixes_source
    (a : ZMod 2)
    {x y : D} {z w : E} {n n' m m' : Nat}
    {ma mb : Blocks x y} {pa pb : Blocks z w}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    (cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    c60F31ParityCell (c60F29ShiftedSource a cell) =
      c60F29ShiftedSource a cell :=
  (c60F31ParityCell_fixed_iff _).2
    (c60F29ShiftedSource_defect_zero a cell)

/-- The independent native Gray exchange is projected to the
charge-zero phase-zero morphism, which is not the actual native
braiding for odd/odd grade. -/
theorem c60F31ParityOddBraiding_collapse :
    c60F31ParityFunctor.map
      (BraidedCategory.braiding GrayGrade.odd GrayGrade.odd).hom =
    (𝟙 (GrayGrade.tensor GrayGrade.odd GrayGrade.odd)) := by
  apply GradedThreeCell.ext <;>
    rfl

/-- EXACT non-braidedness of the genuinely monoidal functor:
source F55 parity cannot recover the extra independent
native odd/odd Gray braiding by forcing a fake source equality. -/
theorem c60F31ParityFunctor_not_braided :
    c60F31ParityFunctor.map
      (BraidedCategory.braiding GrayGrade.odd GrayGrade.odd).hom ≠
      (BraidedCategory.braiding GrayGrade.odd GrayGrade.odd).hom := by
  intro h
  have hh := h.symm.trans c60F31ParityOddBraiding_collapse
  exact GrayGrade.native_braiding_odd_nonidentity hh

/-- Rephasing preserves every native F55 generator charge and
ONLY removes the independently supplied a*b braiding phase. -/
theorem c60F31ParityBraidedSource_components
    (a b : ZMod 2)
    {x y : D} {z w : E} {n n' m m' : Nat}
    {ma mb : Blocks x y} {pa pb : Blocks z w}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    (cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    (c60F31ParityCell (c60F29BraidedSource a b cell)).charge =
      (c60F55SourceNative cell).charge ∧
    (c60F31ParityCell (c60F29BraidedSource a b cell)).phase =
      (c60F55SourceNative cell).phase := by
  constructor
  · exact (c60F29BraidedSource_components a b cell).1
  · rw [c60F31ParityCell_phase]
    have h := c60F55SourceNative_mem cell
    change (c60F55SourceNative cell).phase =
      ((c60F55SourceNative cell).charge.2 : ZMod 2) at h
    rw [(c60F29BraidedSource_components a b cell).1]
    exact h.symm

/-! ## True source-typed C60 physical 90-edge Wang Bi data. -/
section OriginalC60
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

/-- Actual original 90 C60 F54/F55 square data plus its
genuine independent nonneutral braid, projected by
the FULL native strong monoidal parity endofunctor. -/
def c60F31ProjectedPhysicalSquare (a b : ZMod 2)
    (edge : TruncatedIcosahedralEdge) :
    GradedThreeCell (a + b) (b + a) :=
  c60F31ParityCell
    (c60F29ActualBraidedSquare t₁ t₂ left right a b edge)

/-- Independent braid projection returns the ORIGINAL
square charge (0,1) and F55-native exchange phase 1,
even when a*b=1 in the larger Gray target. -/
theorem c60F31ProjectedPhysicalSquare_components
    (a b : ZMod 2) (edge : TruncatedIcosahedralEdge) :
    (c60F31ProjectedPhysicalSquare t₁ t₂ left right a b edge).charge =
      ((0 : Int), (1 : Int)) ∧
    (c60F31ProjectedPhysicalSquare t₁ t₂ left right a b edge).phase =
      (1 : ZMod 2) := by
  rw [c60F31ProjectedPhysicalSquare]
  constructor
  · rw [c60F31ParityCell_charge]
    exact (c60F29ActualBraidedSquare_components
      t₁ t₂ left right a b edge).1
  · rw [c60F31ParityCell_phase,
      (c60F29ActualBraidedSquare_components t₁ t₂ left right a b edge).1]
    rfl

/-- The repaired projected Wang Bi atlas is an ACTUAL native
Cat-valued natural transformation over all 360 ORIGINAL flags. -/
def c60F31ProjectedPhysicalAtlas (a b : ZMod 2)
    (side : C60DartSideGauge) :
    c60ActualCornerFunctor ⟶ c60F29BraidedSixYaoFunctor a b :=
  c60F29BraidedCornerNatTrans a b side
    (c60F31ProjectedPhysicalSquare t₁ t₂ left right a b)

#print axioms c60F31ParityCell_defect_zero
#print axioms c60F31ParityCell_comp
#print axioms c60F31ParityCell_tensor
#print axioms c60F31ParityCell_inv
#print axioms c60F31ParityCell_idempotent
#print axioms c60F31ParityCell_fixed_iff
#print axioms c60F31ParityFunctor
#print axioms c60F31ParityFunctor_tensor
#print axioms c60F31ParityFunctor_whiskerLeft
#print axioms c60F31ParityFunctor_whiskerRight
#print axioms c60F31ParityCoreMonoidal
#print axioms c60F31ParityMonoidalFunctor
#print axioms c60F31ParityFunctor_fixes_source
#print axioms c60F31ParityOddBraiding_collapse
#print axioms c60F31ParityFunctor_not_braided
#print axioms c60F31ParityBraidedSource_components
#print axioms c60F31ProjectedPhysicalSquare_components
#print axioms c60F31ProjectedPhysicalAtlas

end OriginalC60
end
end KUOS.DependentOriginationGrayC60F55ParityMonoidalProjectionV5_179
