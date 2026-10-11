import KUOS.DependentOriginationGrayNativeSymmetricPhaseV5_156
import KUOS.DependentOriginationTruncatedIcosahedralPatchChargeV5_155

namespace KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154
open KUOS.DependentOriginationTruncatedIcosahedralPentagonRotationBridgeV5_154
open KUOS.DependentOriginationTruncatedIcosahedralHigherChargeV5_155
open KUOS.DependentOriginationTruncatedIcosahedralCyclicChargeV5_155
open KUOS.DependentOriginationTruncatedIcosahedralPatchChargeV5_155
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayF55PhaseRealizationV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayNativeSymmetricPhaseV5_156
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F59-E / v5.156 — real C60 five-square Gray collar and global phase cancellation

F59-A–D has a REAL native symmetric braided monoidal groupoid of typed
3-cells with independent integer F58 charge and ZMod2 exchange phase.
Its neutral endomorphisms admit ordinary native categorical composition.

Using the SAME ACTUAL F57 C60 pentagon-to-hexagon four-flag squares,
the F55 separately supplied original local rotations, and the original
F55 pentagon interpreter, this file builds a five-square cyclic collar
as a COMPOSITE of genuine 3-cells in the independent F59 TARGET.
The five geometric squares remain corner-glued by original F57
incidence proofs. This does NOT imply that all corresponding raw
source F55 PresentedCells were themselves vertically composable.

For an arbitrary finite subpatch S of the twelve REAL C60 pentagons,
sum/compose the target collars and preserve exactly the F58 charge:
  Q(S)=(|S|,5|S|), phase(S)=|S| mod 2.
Each local five-square collar is phase 1, any even-size patch is phase
0, and the entire C60 has integer charge (12,60) but phase zero.

The 20 original hexagons and 30 hexagon-to-hexagon cross edges have
not been reinterpreted as F55 3-cell labels by this file. Nor is this
a global ambient Gray 3-functor, a proof of Stage-II omega equality,
or a reversal of the original G.toOplax comparisons.
-/

/-- The genuine endomorphisms at the neutral GrayGrade form an
additive commutative group. Its group addition IS the original
native categorical vertical composition, not an invented charge sum. -/
instance grayNeutralAddCommGroup : AddCommGroup (GradedThreeCell 0 0) where
  zero := GradedThreeCell.ident 0
  add := GradedThreeCell.comp
  neg := GradedThreeCell.inv
  add_assoc := by
    intro f g h
    exact GradedThreeCell.comp_assoc f g h
  zero_add := by
    intro f
    exact GradedThreeCell.ident_comp f
  add_zero := by
    intro f
    exact GradedThreeCell.comp_ident f
  add_left_neg := by
    intro f
    exact GradedThreeCell.inv_comp f
  add_comm := by
    intro f g
    apply GradedThreeCell.ext
    · change f.charge + g.charge = g.charge + f.charge
      exact add_comm _ _
    · change f.phase + g.phase = g.phase + f.phase
      exact add_comm _ _

/-- Make the correspondence with the ACTUAL native categorical
composition explicit for every pair of neutral 3-cells. -/
theorem grayNeutral_add_eq_native_comp (f g : GradedThreeCell 0 0) :
    f + g = (f ≫ g : GrayGrade.unit ⟶ GrayGrade.unit) :=
  rfl

/-- The original F58 signed generator-charge projection is additive
on the REAL neutral Gray 3-cell categorical endomorphism group. -/
def grayNeutralChargeHom : GradedThreeCell 0 0 →+ (Int × Int) where
  toFun := GradedThreeCell.toHigherCharge
  map_zero' := rfl
  map_add' := by
    intro f g
    rfl

/-- The independent F59 exchange phase is ALSO an additive
homomorphism on that SAME genuine 3-cell endomorphism group. -/
def grayNeutralPhaseHom : GradedThreeCell 0 0 →+ ZMod 2 where
  toFun := GradedThreeCell.phase
  map_zero' := rfl
  map_add' := by
    intro f g
    rfl

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section GenuineC60
variable {a b : D} {x y : E}
variable {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
variable {p₀ p₁ p₂ p₃ p₄ : Blocks a b}
variable {q₀ q₁ q₂ q₃ q₄ : Blocks x y}
variable
  (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
  (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
  (t₃ : OriginalF45BracketTree n₃ m₃ p₂ q₂ p₃ q₃)
  (t₄ : OriginalF45BracketTree n₄ m₄ p₃ q₃ p₄ q₄)
variable
  {leftAfter : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁}
  {rightAfter : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂}
  (left : OriginalF45BracketTree.LocalRotation t₁ leftAfter)
  (right : OriginalF45BracketTree.LocalRotation t₂ rightAfter)

/-- The ACTUAL F55 pentagon higher generator, on a particular
original C60 geometric pentagonal face, interpreted in the
independent F59 native 3-cell target. -/
def c60GrayPentagon (v : IcosahedralVertex) : GradedThreeCell 0 0 :=
  OriginalF45C60PentagonPasting.interpret
    t₁ t₂ t₃ t₄ (originalF45C60PentagonPasting t₁ t₂ t₃ t₄ v)
    (OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.braidedPhase
      (D := D) (E := E))

/-- Precisely the five original C60 pentagon-to-hexagon edge flag
squares, each interpreted using the supplied F54 pair as an honest
F55 disjoint-square generator in the independent Gray target. -/
def c60GraySquareList (v : IcosahedralVertex) :
    List (GradedThreeCell 0 0) :=
  ([PentagonalSlot.s0, .s1, .s2, .s3, .s4] : List PentagonalSlot).map
    (fun s =>
      (OriginalC60FlagSquareWithF55Generator.canonical
        ⟨v, s⟩ left right).squareCell.interpret
      (OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.braidedPhase
        (D := D) (E := E)))

/-- Each selected original geometric edge square has the EXACT
F59-B nontrivial odd/odd exchange 3-cell label, with no new choices. -/
theorem c60GraySquareList_eq (v : IcosahedralVertex) :
    c60GraySquareList t₁ t₂ left right v =
      [originalF55BraidedSquareGenerator,
       originalF55BraidedSquareGenerator,
       originalF55BraidedSquareGenerator,
       originalF55BraidedSquareGenerator,
       originalF55BraidedSquareGenerator] := by
  rfl

/-- The five REAL F55-labelled squares, after native 3-cell
composition in the neutral Gray target, retain square-charge five
and have NONZERO exchange phase one. -/
theorem c60GrayFiveSquares_components (v : IcosahedralVertex) :
    (c60GraySquareList t₁ t₂ left right v).sum.charge =
      ((0 : Int), (5 : Int)) ∧
    (c60GraySquareList t₁ t₂ left right v).sum.phase =
      (1 : ZMod 2) := by
  rw [c60GraySquareList_eq t₁ t₂ left right v]
  constructor <;>
    decide

/-- Genuinely composite target 3-cell: the ACTUAL pentagon F55
generator followed by its FIVE corner-glued original C60 squares.
Both summands are neutral-grade endomorphisms, hence composable
in the NATIVE F59-C Category instance. -/
def c60GrayCollar (v : IcosahedralVertex) : GradedThreeCell 0 0 :=
  c60GrayPentagon t₁ t₂ t₃ t₄ v +
    (c60GraySquareList t₁ t₂ left right v).sum

theorem c60GrayCollar_native_comp (v : IcosahedralVertex) :
    c60GrayCollar t₁ t₂ t₃ t₄ left right v =
      (c60GrayPentagon t₁ t₂ t₃ t₄ v ≫
        (c60GraySquareList t₁ t₂ left right v).sum :
          GrayGrade.unit ⟶ GrayGrade.unit) :=
  rfl

/-- The genuine central pentagon contributes (1,0;0), and the
five actual edge-squares contribute (0,5;1). Thus the LOCAL
native Gray collar has F58 charge (1,5) and new phase one. -/
theorem c60GrayCollar_components (v : IcosahedralVertex) :
    (c60GrayCollar t₁ t₂ t₃ t₄ left right v).charge =
      ((1 : Int), (5 : Int)) ∧
    (c60GrayCollar t₁ t₂ t₃ t₄ left right v).phase =
      (1 : ZMod 2) := by
  have hp :=
    originalC60Pentagon_braidedPhase t₁ t₂ t₃ t₄ v
  have hs := c60GrayFiveSquares_components t₁ t₂ left right v
  constructor
  · change (c60GrayPentagon t₁ t₂ t₃ t₄ v).charge +
        (c60GraySquareList t₁ t₂ left right v).sum.charge =
        ((1 : Int), (5 : Int))
    rw [hp.1, hs.1]
    norm_num [Prod.add_def]
  · change (c60GrayPentagon t₁ t₂ t₃ t₄ v).phase +
        (c60GraySquareList t₁ t₂ left right v).sum.phase =
        (1 : ZMod 2)
    rw [hp.2, hs.2]
    simp

/-- The geometric cyclic gluing is carried by precisely the
same F57-D adjacent four-flag squares as those whose ACTUAL
F55 labels form the new nontrivial neutral Gray 3-cell collar. -/
theorem c60GrayCollar_cyclic_geometric_complete
    (v : IcosahedralVertex) :
    (∀ s : PentagonalSlot,
      (((OriginalC60FlagSquareWithF55Generator.canonical
        ⟨v, s⟩ left right).geometricSquare.vertex true),
       ((OriginalC60FlagSquareWithF55Generator.canonical
        ⟨v, s⟩ left right).geometricSquare.face false)) =
      (((OriginalC60FlagSquareWithF55Generator.canonical
        ⟨v, pentagonalSlotNext s⟩ left right).geometricSquare.vertex false),
       ((OriginalC60FlagSquareWithF55Generator.canonical
        ⟨v, pentagonalSlotNext s⟩ left right).geometricSquare.face false))) ∧
    (c60GrayCollar t₁ t₂ t₃ t₄ left right v).charge =
      ((1 : Int), (5 : Int)) ∧
    (c60GrayCollar t₁ t₂ t₃ t₄ left right v).phase =
      (1 : ZMod 2) := by
  exact ⟨originalC60ChargedSquareCollar_consecutive_sharedFlag
      t₁ t₂ left right v,
    (c60GrayCollar_components t₁ t₂ t₃ t₄ left right v).1,
    (c60GrayCollar_components t₁ t₂ t₃ t₄ left right v).2⟩

/-- A finite collection of ACTUAL C60 pentagonal collars is
now aggregated by the SAME native 3-cell vertical-composition law.
Since all are neutral-grade endomorphisms, the Finset sum is typed
and independent of its enumeration order. -/
def c60GrayPatch (S : Finset IcosahedralVertex) :
    GradedThreeCell 0 0 :=
  S.sum (fun v => c60GrayCollar t₁ t₂ t₃ t₄ left right v)

/-- The genuine target 3-cell charge equals, for ANY finite
subpatch, the previously proved original F58-G signed integer
generator-charge sum. -/
theorem c60GrayPatch_charge_eq_F58
    (S : Finset IcosahedralVertex) :
    (c60GrayPatch t₁ t₂ t₃ t₄ left right S).charge =
      originalC60PatchCharge t₁ t₂ left right S := by
  change grayNeutralChargeHom
      (S.sum (fun v => c60GrayCollar t₁ t₂ t₃ t₄ left right v)) =
        S.sum (fun v =>
          originalC60PentagonSquareCollarCharge t₁ t₂ left right v)
  rw [map_sum]
  apply Finset.sum_congr rfl
  intro v _
  rw [(c60GrayCollar_components t₁ t₂ t₃ t₄ left right v).1,
    originalC60PentagonSquareCollarCharge_eq t₁ t₂ left right v]

/-- The new independent exchange phase of ANY actual finite C60
pentagon subpatch counts exactly the selected pentagons modulo two. -/
theorem c60GrayPatch_phase
    (S : Finset IcosahedralVertex) :
    (c60GrayPatch t₁ t₂ t₃ t₄ left right S).phase =
      (S.card : ZMod 2) := by
  change grayNeutralPhaseHom
      (S.sum (fun v => c60GrayCollar t₁ t₂ t₃ t₄ left right v)) =
        (S.card : ZMod 2)
  rw [map_sum]
  change S.sum (fun v =>
      (c60GrayCollar t₁ t₂ t₃ t₄ left right v).phase) =
      (S.card : ZMod 2)
  calc
    S.sum (fun v => (c60GrayCollar t₁ t₂ t₃ t₄ left right v).phase) =
        S.sum (fun _ => (1 : ZMod 2)) := by
          apply Finset.sum_congr rfl
          intro v _
          exact (c60GrayCollar_components t₁ t₂ t₃ t₄ left right v).2
    _ = (S.card : ZMod 2) := by simp

/-- Exact local-to-global cancellation criterion in the REAL
native symmetric braided Gray target: even-size subpatches
have zero phase, odd-size subpatches retain phase one. -/
theorem c60GrayPatch_phase_zero_iff_even
    (S : Finset IcosahedralVertex) :
    (c60GrayPatch t₁ t₂ t₃ t₄ left right S).phase = 0 ↔
      Even S.card := by
  rw [c60GrayPatch_phase t₁ t₂ t₃ t₄ left right S]
  exact ZMod.natCast_eq_zero_iff_even

/-- For arbitrary actual C60 subpatches, the NEW phase
coincides with the independent F58 square-generator-charge
coordinate mod 2. This is a comparison of the TWO new
invariants; it is NOT an old Stage-II obstruction map. -/
theorem c60GrayPatch_phase_eq_F58_square_mod2
    (S : Finset IcosahedralVertex) :
    (c60GrayPatch t₁ t₂ t₃ t₄ left right S).phase =
      ((originalC60PatchCharge t₁ t₂ left right S).2 : ZMod 2) := by
  rw [c60GrayPatch_phase t₁ t₂ t₃ t₄ left right S,
    originalC60PatchCharge_exact t₁ t₂ left right S]
  have h5 : (5 : ZMod 2) = 1 := by decide
  simp [h5]

/-- The ENTIRE genuine C60 (twelve pentagons and their sixty
actual square labels) has a nonzero integer 3-cell charge but
zero exchange phase in the SAME native composable target 3-cell. -/
theorem c60GrayGlobal_components :
    (c60GrayPatch t₁ t₂ t₃ t₄ left right Finset.univ).charge =
      ((12 : Int), (60 : Int)) ∧
    (c60GrayPatch t₁ t₂ t₃ t₄ left right Finset.univ).phase =
      (0 : ZMod 2) := by
  constructor
  · rw [c60GrayPatch_charge_eq_F58 t₁ t₂ t₃ t₄ left right,
      originalC60PatchCharge_exact t₁ t₂ left right,
      Finset.card_univ, originalC60IcosahedralVertex_card_kernel]
    decide
  · rw [c60GrayPatch_phase t₁ t₂ t₃ t₄ left right,
      Finset.card_univ, originalC60IcosahedralVertex_card_kernel]
    decide

/-- The final contrast is genuine: NONZERO local exchange phase
on every authentic pentagon and ZERO global exchange phase,
yet the original full integer (12,60) never vanishes. -/
theorem c60GrayLocalNonzeroGlobalZero (v : IcosahedralVertex) :
    (c60GrayCollar t₁ t₂ t₃ t₄ left right v).phase ≠ 0 ∧
    (c60GrayPatch t₁ t₂ t₃ t₄ left right Finset.univ).phase = 0 ∧
    (c60GrayPatch t₁ t₂ t₃ t₄ left right Finset.univ).charge ≠
      (0 : Int × Int) := by
  refine ⟨?_, (c60GrayGlobal_components
      t₁ t₂ t₃ t₄ left right).2, ?_⟩
  · rw [(c60GrayCollar_components t₁ t₂ t₃ t₄ left right v).2]
    decide
  · rw [(c60GrayGlobal_components t₁ t₂ t₃ t₄ left right).1]
    decide

#print axioms grayNeutralAddCommGroup
#print axioms grayNeutral_add_eq_native_comp
#print axioms grayNeutralChargeHom
#print axioms grayNeutralPhaseHom
#print axioms c60GraySquareList_eq
#print axioms c60GrayFiveSquares_components
#print axioms c60GrayCollar_native_comp
#print axioms c60GrayCollar_components
#print axioms c60GrayCollar_cyclic_geometric_complete
#print axioms c60GrayPatch_charge_eq_F58
#print axioms c60GrayPatch_phase
#print axioms c60GrayPatch_phase_zero_iff_even
#print axioms c60GrayPatch_phase_eq_F58_square_mod2
#print axioms c60GrayGlobal_components
#print axioms c60GrayLocalNonzeroGlobalZero

end GenuineC60
end
end KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
