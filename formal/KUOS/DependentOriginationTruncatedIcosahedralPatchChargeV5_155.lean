import KUOS.DependentOriginationTruncatedIcosahedralGlobalHigherChargeParityV5_155

namespace KUOS.DependentOriginationTruncatedIcosahedralPatchChargeV5_155

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralCyclicChargeV5_155
open KUOS.DependentOriginationTruncatedIcosahedralGlobalHigherChargeV5_155
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F58-G / v5.155 — real C60 finite subpatch charges and exact mod-two loss

F58-E gives each of the twelve genuine cyclic pentagonal square collars
the independently interpreted integer higher-generator charge (1,5).
F58-F proves their global charge (12,60), its mod-two image zero, and
the independent additive reduction Int × Int →+ ZMod 2 × ZMod 2.

Here the same ACTUAL geometric collars are summed over an arbitrary
finite subset of the original C60 pentagons, not just all twelve.
The resulting integer charge records the exact selected-face cardinality,
while its mod-two image retains only that cardinality modulo two.
In particular any two distinct pentagons have a nonzero integer charge
(2,10) whose mod-two image is zero. The genuine total (12,60) is
another nonzero kernel witness, so *no* right reconstruction of all
integer charge pairs from the mod-two reduction is possible.

This is a concrete nonfaithfulness result for the NEW independent
F58 generator-charge coefficient reduction. It does not identify
these coefficients with the historic Stage-II omega obstruction,
nor assert that the geometric flags are composable external 3-cells.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section ActualSubpatch
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

/-- Charge of an arbitrary FINITE set of genuine C60 pentagonal
faces, each carrying the actual cyclic five-square F55-labelled collar. -/
def originalC60PatchCharge
    (S : Finset IcosahedralVertex) : Int × Int :=
  S.sum (fun v =>
    originalC60PentagonSquareCollarCharge t₁ t₂ left right v)

/-- The integer charge of a real C60 pentagonal subpatch is exactly
(cardinality, five times cardinality), not merely a formal global
cardinality statement. Each summand is the actual F58-E collar. -/
theorem originalC60PatchCharge_exact
    (S : Finset IcosahedralVertex) :
    originalC60PatchCharge t₁ t₂ left right S =
      ((S.card : Int), 5 * (S.card : Int)) := by
  classical
  induction S using Finset.induction_on with
  | empty =>
      simp [originalC60PatchCharge]
      rfl
  | @insert v S hv ih =>
      unfold originalC60PatchCharge at ih ⊢
      rw [Finset.sum_insert hv,
        originalC60PentagonSquareCollarCharge_eq t₁ t₂ left right v,
        ih, Finset.card_insert_of_notMem hv]
      simp [Prod.add_def, Nat.cast_add, mul_add, add_comm]

/-- On the very same real subset of C60 pentagon collars, the
coordinatewise additive mod-two image retains precisely the selected
number of pentagons modulo two on BOTH independent generators. -/
theorem originalC60PatchCharge_mod2
    (S : Finset IcosahedralVertex) :
    originalC60HigherChargeMod2
      (originalC60PatchCharge t₁ t₂ left right S) =
      ((S.card : ZMod 2), (S.card : ZMod 2)) := by
  rw [originalC60PatchCharge_exact t₁ t₂ left right S]
  have h5 : (5 : ZMod 2) = 1 := by decide
  simp [originalC60HigherChargeMod2, h5]

/-- For ANY selected set of genuine C60 pentagons, mod-two
generator-charge cancellation is equivalent to the number of selected
pentagons being even. This is the complete finite subpatch parity test,
not an identification with any Stage-II obstruction class. -/
theorem originalC60PatchCharge_mod2_zero_iff_even
    (S : Finset IcosahedralVertex) :
    originalC60HigherChargeMod2
      (originalC60PatchCharge t₁ t₂ left right S) =
        ((0 : ZMod 2), (0 : ZMod 2)) ↔ Even S.card := by
  rw [originalC60PatchCharge_mod2 t₁ t₂ left right S]
  constructor
  · intro h
    have hfirst : (S.card : ZMod 2) = 0 := congrArg Prod.fst h
    exact ZMod.natCast_eq_zero_iff_even.mp hfirst
  · intro heven
    have hzero : (S.card : ZMod 2) = 0 :=
      ZMod.natCast_eq_zero_iff_even.mpr heven
    simp [hzero]

/-- A single actual C60 pentagon retains its nonzero higher-generator
signature under the independent mod-two charge reduction. -/
theorem originalC60SingletonPatch_mod2_ne_zero
    (v : IcosahedralVertex) :
    originalC60HigherChargeMod2
      (originalC60PatchCharge t₁ t₂ left right ({v} : Finset IcosahedralVertex)) ≠
      ((0 : ZMod 2), (0 : ZMod 2)) := by
  rw [originalC60PatchCharge_mod2 t₁ t₂ left right]
  simp only [Finset.card_singleton]
  decide

/-- Any pair of DISTINCT true C60 pentagons has nonzero integer
higher-generator charge (2,10), even though that same pair has
zero mod-two image. No quadrilateral C60 faces are introduced. -/
theorem originalC60DistinctPairPatch_cancels_mod2
    (v w : IcosahedralVertex) (hvw : v ≠ w) :
    originalC60PatchCharge t₁ t₂ left right
      ({v, w} : Finset IcosahedralVertex) =
        ((2 : Int), (10 : Int)) ∧
    originalC60HigherChargeMod2
      (originalC60PatchCharge t₁ t₂ left right
        ({v, w} : Finset IcosahedralVertex)) =
          ((0 : ZMod 2), (0 : ZMod 2)) := by
  have hcard :
      ({v, w} : Finset IcosahedralVertex).card = 2 := by
    simp [hvw]
  constructor
  · rw [originalC60PatchCharge_exact t₁ t₂ left right, hcard]
    norm_num
  · rw [originalC60PatchCharge_mod2 t₁ t₂ left right, hcard]
    decide

/-- Charges add exactly over DISJOINT geometric collections of
pentagons; this is ordinary finite additive aggregation, not a
claim of external vertical 3-cell composability. -/
theorem originalC60DisjointPatchCharge_add
    (S T : Finset IcosahedralVertex) (hST : Disjoint S T) :
    originalC60PatchCharge t₁ t₂ left right (S ∪ T) =
      originalC60PatchCharge t₁ t₂ left right S +
        originalC60PatchCharge t₁ t₂ left right T := by
  exact Finset.sum_union hST

/-- The entire real C60 pentagon-collar aggregate is nonzero over
integers, even though F58-F computed a ZERO mod-two image. -/
theorem originalC60GlobalCharge_int_ne_zero :
    (∑ v : IcosahedralVertex,
      originalC60PentagonSquareCollarCharge t₁ t₂ left right v) ≠
      (0 : Int × Int) := by
  rw [originalC60GlobalPentagonCollarCharge t₁ t₂ left right]
  decide

/-- The actual nonzero C60 total (12,60) and the zero total have
identical mod-two generator-charge images. Thus there is no function
recovering every original integer generator charge from only its
mod-two reduction; this is a witnessed global information-loss
obstruction, not an identification with the old Stage-II omega. -/
theorem originalC60NoUniversalChargeRecoveryFromMod2 :
    ¬ ∃ recover : (ZMod 2 × ZMod 2) → (Int × Int),
      ∀ q : Int × Int,
        recover (originalC60HigherChargeMod2 q) = q := by
  rintro ⟨recover, hrecover⟩
  -- This exact nonzero pair is the previous F58-F actual C60 total.
  -- Its reduction equals the zero pair, hence any global left inverse
  -- would force a false integer equality.
  have hparity :
      originalC60HigherChargeMod2 ((12 : Int), (60 : Int)) =
        originalC60HigherChargeMod2 (0 : Int × Int) := by
    change ((12 : ZMod 2), (60 : ZMod 2)) =
      ((0 : ZMod 2), (0 : ZMod 2))
    decide
  have heq := congrArg recover hparity
  rw [hrecover ((12 : Int), (60 : Int)),
    hrecover (0 : Int × Int)] at heq
  exact (by decide : ((12 : Int), (60 : Int)) ≠ (0 : Int × Int)) heq

#print axioms originalC60PatchCharge
#print axioms originalC60PatchCharge_exact
#print axioms originalC60PatchCharge_mod2
#print axioms originalC60PatchCharge_mod2_zero_iff_even
#print axioms originalC60SingletonPatch_mod2_ne_zero
#print axioms originalC60DistinctPairPatch_cancels_mod2
#print axioms originalC60DisjointPatchCharge_add
#print axioms originalC60GlobalCharge_int_ne_zero
#print axioms originalC60NoUniversalChargeRecoveryFromMod2

end ActualSubpatch
end
end KUOS.DependentOriginationTruncatedIcosahedralPatchChargeV5_155
