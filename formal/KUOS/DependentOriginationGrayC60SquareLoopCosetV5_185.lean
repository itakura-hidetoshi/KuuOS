import KUOS.DependentOriginationGrayC60FullF55ChargeObstructionV5_184

namespace KUOS.DependentOriginationGrayC60SquareLoopCosetV5_185

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayF55PhaseRealizationV5_156
open KUOS.DependentOriginationTruncatedIcosahedralHigherChargeV5_155
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60CochainDescentV5_166
open KUOS.DependentOriginationGrayC60IntegralBoundaryLinearMapV5_159
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationGrayC60F55SourcePhaseLockedAtlasV5_175
open KUOS.DependentOriginationGrayC60F55NonneutralBraidingTransportV5_177
open KUOS.DependentOriginationGrayC60WangBiGlobalGrayDescentV5_174
open KUOS.DependentOriginationGrayC60BraidedFlatRepairV5_181
open KUOS.DependentOriginationGrayC60BraidedSharpSupportV5_182
open KUOS.DependentOriginationGrayC60TypedF55LiftV5_183
open KUOS.DependentOriginationGrayC60FullF55ChargeObstructionV5_184
open KUOS.DependentOriginationGrayC60WangBiZhouyiTimeV5_170
open KUOS.DependentOriginationGrayC60WangBiNativeHigherCoherenceV5_171
open KUOS.DependentOriginationGrayC60WangBiFourImageSixQiF55NaturalityV5_172
open KUOS.DependentOriginationGrayC60WangBiGaugeCollarSixQiCoherenceV5_173
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F37 / v5.185 — exact square-charge cosets for ALL original F55 constructors

F59-F36 proved that the first original F58 pentagon charge of any
genuine original typed F55 PresentedCell r ⇒ s is the difference
between the lengths of the two actual original F54 rotation routes.

We now completely organize the SECOND independent F58 square charge
for ALL NINE original F55 constructors without declaring any raw
PresentedCell equal, introducing an arbitrary ambient Gray 3-functor,
or guessing that every phase-compatible target value is realizable.

For a fixed original route r, the actual square charges of the
genuine freely generated F55 LOOP CELLS r ⇒ r form an AddSubgroup
of Int. Identity / reversal / vertical composition supply its
real group laws; all nine constructors remain available as source
syntax.  A FIXED original typed witness w : r ⇒ s then makes the
realizable square charges for r ⇒ s EXACTLY the affine coset
qS(w) + LoopSquareCharge(r).  This description is independent of
the chosen witness.  Conjugating real source loops along w proves
the loop-charge subgroup is invariant along typed source transport.

Full F55 source lifting of a neutral Gray 3-cell has exactly THREE
conditions: F55 phase lock, the actual F54 rotation-length
pentagon charge, and membership of its square-charge displacement
in this typed source-loop subgroup.  Unlike F59-F35's existential
charge witness, the remaining source condition is now an explicit
coset membership invariant, with BOTH directions constructively
witnessed by actual original typed PresentedCell compositions.

For the physically original fixed disjoint-square routes this
becomes qP = 0 and qS - 1 in the genuine source-loop subgroup,
without claiming the subgroup is zero or all of Int.

Finally the local exact criterion is applied independently at
all original NINETY C60 edge positions, then transported by
faithfulness into the genuinely existing Mathlib Wang Bi 360-flag
natural transformations and combined with all THIRTY-TWO original
signed face-flatness and the independent Gray braid phase-defect
equations.  No independent 3-cell, Stage-II omega, or historical
meaning is silently identified with a free source witness.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section OriginalTypedSource
variable {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : Blocks a b} {pa pb : Blocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}
variable {r s : OriginalF45BracketTree.DepthRotationRoute first last}

/-- Second F58 integer square-generator charge of the actual
original freely generated typed F55 source cell. -/
def c60F37SquareCharge
    (cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) : ℤ :=
  (c60F55SourceNative cell).charge.2

/-- This source square charge is EXACTLY the original independent
F58 integer generator interpreter, not a new numerical invariant. -/
theorem c60F37SquareCharge_eq_originalF58
    (cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    c60F37SquareCharge cell =
      (cell.interpret
        (OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.generatorCharge
          (D := D) (E := E))).2 := by
  exact congrArg Prod.snd
    (KUOS.DependentOriginationGrayF55PhaseRealizationV5_156.OriginalF45BracketTree.DepthRotationRoute.PresentedCell.braidedPhase_charge_eq_F58 cell)

/-- Original F55 identity has second integer charge zero. -/
theorem c60F37SquareCharge_ident
    (route : OriginalF45BracketTree.DepthRotationRoute first last) :
    c60F37SquareCharge
      (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.ident route) = 0 := by
  rfl

/-- Original F55 inverse reverses the actual signed square charge. -/
theorem c60F37SquareCharge_symm
    (cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    c60F37SquareCharge
      (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.symm cell) =
      -c60F37SquareCharge cell := by
  change (-(c60F55SourceNative cell).charge).2 =
    -(c60F55SourceNative cell).charge.2
  rfl

/-- Exact charge addition for the ORIGINAL source trans constructor,
not an assumed equality between unrelated raw source proofs. -/
theorem c60F37SquareCharge_trans
    {t : OriginalF45BracketTree.DepthRotationRoute first last}
    (α : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s)
    (β : OriginalF45BracketTree.DepthRotationRoute.PresentedCell s t) :
    c60F37SquareCharge
      (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.trans α β) =
      c60F37SquareCharge α + c60F37SquareCharge β := by
  change ((c60F55SourceNative α).charge +
    (c60F55SourceNative β).charge).2 =
      (c60F55SourceNative α).charge.2 +
        (c60F55SourceNative β).charge.2
  rfl

/-- A genuine source loop has ZERO pentagon charge by F59-F36.
This is independent of its possibly nonzero second square charge. -/
theorem c60F37SourceLoop_pentagonCharge_zero
    (route : OriginalF45BracketTree.DepthRotationRoute first last)
    (loop : OriginalF45BracketTree.DepthRotationRoute.PresentedCell route route) :
    (c60F55SourceNative loop).charge.1 = 0 := by
  rw [c60F36FullNinePentagonCharge_eq_rotationDifference loop]
  omega

/-- The ACTUAL integer square charges of ALL original freely generated
F55 endomorphism cells at ONE fixed original F54 typed route form a
genuine AddSubgroup of ℤ, with identity, inverse and vertical paste. -/
def c60F37OriginalSquareLoopSubgroup
    (route : OriginalF45BracketTree.DepthRotationRoute first last) :
    AddSubgroup ℤ where
  carrier := {z | ∃ loop :
    OriginalF45BracketTree.DepthRotationRoute.PresentedCell route route,
      c60F37SquareCharge loop = z}
  zero_mem' := by
    exact ⟨.ident route, c60F37SquareCharge_ident route⟩
  add_mem' := by
    rintro k l ⟨α, hα⟩ ⟨β, hβ⟩
    refine ⟨.trans α β, ?_⟩
    rw [c60F37SquareCharge_trans, hα, hβ]
  neg_mem' := by
    rintro k ⟨α, hα⟩
    refine ⟨.symm α, ?_⟩
    rw [c60F37SquareCharge_symm, hα]

/-- The SECOND F58 charge of an actual F55 cell r⇒s is realizable
iff its displacement from ONE genuine witness is in the original
source-loop square-charge subgroup. No fake F55 source cell is
inserted in either direction. -/
theorem c60F37SquareCharge_realizable_iff_affineCoset
    (anchor : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s)
    (z : ℤ) :
    (∃ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s,
      c60F37SquareCharge cell = z) ↔
      z - c60F37SquareCharge anchor ∈
        c60F37OriginalSquareLoopSubgroup r := by
  constructor
  · rintro ⟨cell, hc⟩
    change ∃ loop : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r r,
      c60F37SquareCharge loop = z - c60F37SquareCharge anchor
    refine ⟨.trans cell (.symm anchor), ?_⟩
    rw [c60F37SquareCharge_trans, c60F37SquareCharge_symm, hc]
    abel
  · intro h
    change ∃ loop : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r r,
      c60F37SquareCharge loop = z - c60F37SquareCharge anchor at h
    obtain ⟨loop, hloop⟩ := h
    refine ⟨.trans loop anchor, ?_⟩
    rw [c60F37SquareCharge_trans, hloop]
    omega

/-- Transport through any genuine original typed F55 cell conjugates
source loops, preserving their second charge EXACTLY. Therefore the
loop-charge subgroup is invariant under source higher transport. -/
theorem c60F37OriginalSquareLoopSubgroup_transport
    (anchor : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    c60F37OriginalSquareLoopSubgroup r =
      c60F37OriginalSquareLoopSubgroup s := by
  apply le_antisymm
  · intro z hz
    change ∃ loop : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r r,
      c60F37SquareCharge loop = z at hz
    obtain ⟨loop, hloop⟩ := hz
    change ∃ loop : OriginalF45BracketTree.DepthRotationRoute.PresentedCell s s,
      c60F37SquareCharge loop = z
    refine ⟨.trans (.symm anchor) (.trans loop anchor), ?_⟩
    rw [c60F37SquareCharge_trans, c60F37SquareCharge_symm,
      c60F37SquareCharge_trans, hloop]
    abel
  · intro z hz
    change ∃ loop : OriginalF45BracketTree.DepthRotationRoute.PresentedCell s s,
      c60F37SquareCharge loop = z at hz
    obtain ⟨loop, hloop⟩ := hz
    change ∃ loop : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r r,
      c60F37SquareCharge loop = z
    refine ⟨.trans anchor (.trans loop (.symm anchor)), ?_⟩
    rw [c60F37SquareCharge_trans, c60F37SquareCharge_trans,
      c60F37SquareCharge_symm, hloop]
    abel

/-- The affine coset is independent of the chosen genuine F55
source witness between the SAME precise original F54 routes. -/
theorem c60F37AffineSquareCoset_anchor_independent
    (w₁ w₂ : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s)
    (z : ℤ) :
    (z - c60F37SquareCharge w₁ ∈ c60F37OriginalSquareLoopSubgroup r) ↔
      (z - c60F37SquareCharge w₂ ∈ c60F37OriginalSquareLoopSubgroup r) := by
  rw [← c60F37SquareCharge_realizable_iff_affineCoset w₁ z,
    ← c60F37SquareCharge_realizable_iff_affineCoset w₂ z]

/-- COMPLETE original F55 neutral Gray-target image condition for any
typed parallel F54 routes *with one actual typed witness*:
  (1) the genuine F55 phase / square-charge parity law,
  (2) the pentagon charge forced by the original rotation lengths,
  (3) the square charge in the genuine affine F55 source-loop coset.
No separate existential charge-realization oracle is needed. -/
theorem c60F37TypedSourceLift_iff_phase_pentagon_squareCoset
    (anchor : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s)
    (g : GradedThreeCell 0 0) :
    (∃ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s,
      c60F55SourceNative cell = g) ↔
      g ∈ c60F55PhaseLocked ∧
      g.charge.1 = (r.rotationCount : ℤ) - (s.rotationCount : ℤ) ∧
      (g.charge.2 - c60F37SquareCharge anchor) ∈
        c60F37OriginalSquareLoopSubgroup r := by
  constructor
  · rintro ⟨cell, hcell⟩
    refine ⟨?_, ?_, ?_⟩
    · rw [← hcell]
      exact c60F55SourceNative_mem cell
    · exact c60F36TypedSourceImage_requires_pentagonDifference g
        ⟨cell, hcell⟩
    · apply (c60F37SquareCharge_realizable_iff_affineCoset anchor
        g.charge.2).mp
      refine ⟨cell, ?_⟩
      rw [← hcell]
      rfl
  · rintro ⟨hlocked, hfirst, hsecond⟩
    obtain ⟨cell, hsq⟩ :=
      (c60F37SquareCharge_realizable_iff_affineCoset anchor
        g.charge.2).mpr hsecond
    have hc : (c60F55SourceNative cell).charge = g.charge := by
      apply Prod.ext
      · exact (c60F36FullNinePentagonCharge_eq_rotationDifference cell).trans
          hfirst.symm
      · exact hsq
    apply (c60F35TypedSourceLift_iff_phaseAndF58Realization g).mpr
    refine ⟨hlocked, ⟨cell, ?_⟩⟩
    exact (KUOS.DependentOriginationGrayF55PhaseRealizationV5_156.OriginalF45BracketTree.DepthRotationRoute.PresentedCell.braidedPhase_charge_eq_F58 cell).symm.trans hc

end OriginalTypedSource

/-! ## Original genuine disjoint-square left-first/right-first source. -/

section OriginalPhysicalSquare
variable {a b : D} {x y : E}
variable {n₁ n₂ m₁ m₂ : Nat}
variable {p₀ p₁ p₂ : Blocks a b}
variable {q₀ q₁ q₂ : Blocks x y}
variable
  (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
  (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
variable
  {leftAfter : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁}
  {rightAfter : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂}
  (left : OriginalF45BracketTree.LocalRotation t₁ leftAfter)
  (right : OriginalF45BracketTree.LocalRotation t₂ rightAfter)

/-- The ACTUAL original F55 square witness has second charge ONE,
not the integer pentagon charge, and is genuinely dependently typed. -/
theorem c60F37OriginalSquareAnchor_squareCharge_one :
    c60F37SquareCharge
      (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.disjointSquare
        left right) = 1 := by
  rfl

/-- All NINE original F55 constructors between the EXACT two
physical F54 disjoint-square routes admit a given full native
Gray target iff qP=0, independent phase is qS mod 2 and qS-1
lies in the real square-loop charge subgroup of the left route. -/
theorem c60F37OriginalSquareAllNineLift_iff_coset
    (g : GradedThreeCell 0 0) :
    (∃ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell
      (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right)
      (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right),
      c60F55SourceNative cell = g) ↔
      g ∈ c60F55PhaseLocked ∧
      g.charge.1 = 0 ∧
      (g.charge.2 - 1) ∈
        c60F37OriginalSquareLoopSubgroup
          (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right) := by
  have h := c60F37TypedSourceLift_iff_phase_pentagon_squareCoset
    (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.disjointSquare
      left right) g
  simpa only [c60F37OriginalSquareAnchor_squareCharge_one,
    OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst_count,
    OriginalF45BracketTree.DepthRotationRoute.squareRightFirst_count,
    Nat.cast_ofNat, sub_self] using h

end OriginalPhysicalSquare

/-! ## All original ninety C60 edges and three exact descent conditions. -/

section C60FullTypedAtlas
variable {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : Blocks a b} {pa pb : Blocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}
variable
  (r s : TruncatedIcosahedralEdge →
    OriginalF45BracketTree.DepthRotationRoute first last)
  (anchor : ∀ e : TruncatedIcosahedralEdge,
    OriginalF45BracketTree.DepthRotationRoute.PresentedCell (r e) (s e))

/-- ALL-NINETY edgewise exact original F55 full-nine source lifting,
with a previously supplied source witness on each original real
physical C60 edge.  Replaces unspecified F58 realizability by an
explicit, source-transport-invariant integer square-loop coset. -/
theorem c60F37All90TypedLift_iff_squareLoopCosets
    (grade : TruncatedIcosahedralEdge → GradedThreeCell 0 0) :
    (∃ cells : ∀ e : TruncatedIcosahedralEdge,
        OriginalF45BracketTree.DepthRotationRoute.PresentedCell (r e) (s e),
      ∀ e : TruncatedIcosahedralEdge,
        c60F55SourceNative (cells e) = grade e) ↔
      ∀ e : TruncatedIcosahedralEdge,
        grade e ∈ c60F55PhaseLocked ∧
        (grade e).charge.1 =
          ((r e).rotationCount : ℤ) - ((s e).rotationCount : ℤ) ∧
        ((grade e).charge.2 - c60F37SquareCharge (anchor e)) ∈
          c60F37OriginalSquareLoopSubgroup (r e) := by
  constructor
  · rintro ⟨cells, hcells⟩ e
    exact (c60F37TypedSourceLift_iff_phase_pentagon_squareCoset
      (anchor e) (grade e)).mp ⟨cells e, hcells e⟩
  · intro h
    classical
    have heach : ∀ e : TruncatedIcosahedralEdge,
        ∃ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell
          (r e) (s e), c60F55SourceNative cell = grade e := by
      intro e
      exact (c60F37TypedSourceLift_iff_phase_pentagon_squareCoset
        (anchor e) (grade e)).mpr (h e)
    choose cells hcells using heach
    exact ⟨cells, hcells⟩

/-- Native Mathlib Wang Bi natural transformations on all original
C60 360 physical flags are faithful in independently measured F55
integer charges and phase; exact original source-image lift is
equivalent to the very same three edgewise typed conditions. -/
theorem c60F37WangBiAll90TypedLift_iff_squareLoopCosets
    (frame : WangBiFrame) (side : C60DartSideGauge)
    (grade : TruncatedIcosahedralEdge → GradedThreeCell 0 0) :
    (∃ cells : ∀ e : TruncatedIcosahedralEdge,
        OriginalF45BracketTree.DepthRotationRoute.PresentedCell (r e) (s e),
      c60WangBiGlobalGradedAtlas side
        (fun e => c60F55SourceNative (cells e)) =
          c60WangBiGlobalGradedAtlas side grade) ↔
      ∀ e : TruncatedIcosahedralEdge,
        grade e ∈ c60F55PhaseLocked ∧
        (grade e).charge.1 =
          ((r e).rotationCount : ℤ) - ((s e).rotationCount : ℤ) ∧
        ((grade e).charge.2 - c60F37SquareCharge (anchor e)) ∈
          c60F37OriginalSquareLoopSubgroup (r e) := by
  rw [← c60F37All90TypedLift_iff_squareLoopCosets r s anchor grade]
  constructor
  · rintro ⟨cells, hatlas⟩
    exact ⟨cells, congrFun (c60WangBiGlobalGradedAtlas_faithful
      frame side hatlas)⟩
  · rintro ⟨cells, hgrade⟩
    refine ⟨cells, ?_⟩
    have heq :
        (fun e => c60F55SourceNative (cells e)) = grade := by
      funext e
      exact hgrade e
    rw [heq]

/-- Exact corrected B_ab classification: genuine original C60
full-Gray face descent, independent a*b phase-defect cancellation
AND the two source-typed F58 integer charge constraints.
The final square obstruction is now an explicit genuine F55 LOOP
subgroup coset, not an unspecified source-charge existential. -/
theorem c60F37BraidedFlatTypedLift_iff_squareLoopCosets
    (α β : ZMod 2)
    (k : C60IntegralOneChains →ₗ[ℤ] GradedThreeCell 0 0) :
    ((∀ face : TruncatedIcosahedralSeedFace,
        c60WangBiSignedGrayFace (c60F33CorrectedEdgeGrade α β k) face = 0) ∧
     (∃ cells : ∀ e : TruncatedIcosahedralEdge,
        OriginalF45BracketTree.DepthRotationRoute.PresentedCell (r e) (s e),
       ∀ e : TruncatedIcosahedralEdge,
        c60F55SourceNative (cells e) =
          c60F33CorrectedEdgeGrade α β k e)) ↔
      ((∃ phi : C60IntegralZeroChains →ₗ[ℤ] GradedThreeCell 0 0,
          k = phi.comp c60IntegralBoundaryOne -
            c60F33BraidedEdgeCochain α β) ∧
       (∀ e : TruncatedIcosahedralEdge,
          c60F29PhaseDefect (k (Finsupp.single e (1 : ℤ))) = -(α * β)) ∧
       (∀ e : TruncatedIcosahedralEdge,
          (c60F33CorrectedEdgeGrade α β k e).charge.1 =
            ((r e).rotationCount : ℤ) - ((s e).rotationCount : ℤ)) ∧
       (∀ e : TruncatedIcosahedralEdge,
          ((c60F33CorrectedEdgeGrade α β k e).charge.2 -
            c60F37SquareCharge (anchor e)) ∈
              c60F37OriginalSquareLoopSubgroup (r e))) := by
  constructor
  · rintro ⟨hflat, hlift⟩
    have htyped := (c60F37All90TypedLift_iff_squareLoopCosets
      r s anchor (c60F33CorrectedEdgeGrade α β k)).mp hlift
    have hphys := (c60F34FlatAndSourcePhaseLocked_iff α β k).mp
      ⟨hflat, fun e => (htyped e).1⟩
    exact ⟨hphys.1, hphys.2,
      (fun e => (htyped e).2.1),
      (fun e => (htyped e).2.2)⟩
  · rintro ⟨hexact, hdefect, hfirst, hsecond⟩
    have hphys := (c60F34FlatAndSourcePhaseLocked_iff α β k).mpr
      ⟨hexact, hdefect⟩
    refine ⟨hphys.1, ?_⟩
    apply (c60F37All90TypedLift_iff_squareLoopCosets
      r s anchor (c60F33CorrectedEdgeGrade α β k)).mpr
    intro e
    exact ⟨hphys.2 e, hfirst e, hsecond e⟩

end C60FullTypedAtlas

#print axioms c60F37SquareCharge_eq_originalF58
#print axioms c60F37SquareCharge_ident
#print axioms c60F37SquareCharge_symm
#print axioms c60F37SquareCharge_trans
#print axioms c60F37SourceLoop_pentagonCharge_zero
#print axioms c60F37OriginalSquareLoopSubgroup
#print axioms c60F37SquareCharge_realizable_iff_affineCoset
#print axioms c60F37OriginalSquareLoopSubgroup_transport
#print axioms c60F37AffineSquareCoset_anchor_independent
#print axioms c60F37TypedSourceLift_iff_phase_pentagon_squareCoset
#print axioms c60F37OriginalSquareAnchor_squareCharge_one
#print axioms c60F37OriginalSquareAllNineLift_iff_coset
#print axioms c60F37All90TypedLift_iff_squareLoopCosets
#print axioms c60F37WangBiAll90TypedLift_iff_squareLoopCosets
#print axioms c60F37BraidedFlatTypedLift_iff_squareLoopCosets

end
end KUOS.DependentOriginationGrayC60SquareLoopCosetV5_185
