import KUOS.DependentOriginationDoubleDeloopingTypeACocycleLiftingV1_101

namespace KUOS.DependentOriginationDoubleDeloopingTypeALowDimensionalFillersV1_102

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Bicategory
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95
open KUOS.DependentOriginationDoubleDeloopingThinComparisonZeroV1_96
open KUOS.DependentOriginationDoubleDeloopingTypeBTetrahedralZeroV1_97
open KUOS.DependentOriginationDoubleDeloopingHornCoherenceLowDimV1_99
open KUOS.DependentOriginationDoubleDeloopingNormalizedCocycleRealizationV1_100
open KUOS.DependentOriginationDoubleDeloopingTypeACocycleLiftingV1_101

/-!
# Literal low-dimensional type-(A) fillers for `B²ℕ` v1.102

Version v1.101 reduced the complete type-(A) terminal RLP to normalized
`Nat`-valued cocycle completion.  This file closes the genuinely low-dimensional
part of that problem.

First we prove an extensionality theorem specific to the additive double
delooping: a Duskin simplex is determined by all of its composition-comparison
labels.  Objects and 1-cells are unique and all mapped source 2-cells and unit
constraints are zero, so `mapComp` is the only nontrivial datum.

We then construct the three low-dimensional inner-horn fillers:

* `n = 2, i = 1`: the zero cocycle gives the required thin replacement;
* `n = 3, i = 1`: read `013` and `123`, force `012 = 0`, and set
  `023 = 123 + 013`;
* `n = 3, i = 2`: read `012` and `023`, force `123 = 0`, and set
  `013 = 012 + 023`.

The restrictions are proved literally, face by face, using Mathlib's
`SSet.horn.hom_ext` and the comparison extensionality theorem.  Thus after this
file the type-(A) frontier contains no dimension-two or dimension-three
obligation; only the dimension-four four-implies-five step and the
high-dimensional visibility step remain.
-/

/-! ## Comparison extensionality in the additive double delooping -/

/-- Strict unitarity makes every unit constraint in `B²ℕ` equal to zero. -/
theorem natDuskin_mapId_eq_zero
    {n : Nat}
    (sigma : DuskinSimplex NatDoubleDelooping n)
    (a : DuskinOrdinal n) :
    sigma.mapId a = 0 := by
  exact NatDoubleDelooping.isIso_twoCell_eq_zero _

/-- In `B²ℕ`, all non-proof data of a Duskin simplex other than `mapComp` are
forced.  Hence equality of all composition comparisons implies equality of the
whole normal-lax simplex. -/
theorem natDuskinSimplex_eq_of_mapComp_eq
    {n : Nat}
    (sigma tau : DuskinSimplex NatDoubleDelooping n)
    (hcomp :
      ∀ {a b c : DuskinOrdinal n}
        (f : a ⟶ b) (g : b ⟶ c),
        sigma.mapComp f g = tau.mapComp f g) :
    sigma = tau := by
  attribute [local ext] StrictlyUnitaryLaxFunctor
  ext
  · exact Subsingleton.elim _ _
  all_goals
    rw [heq_iff_eq]
    ext
    first
    | exact Subsingleton.elim _ _
    | exact hcomp _ _
    | rw [natDuskin_map₂_eq_zero sigma, natDuskin_map₂_eq_zero tau]
    | rw [natDuskin_mapId_eq_zero sigma, natDuskin_mapId_eq_zero tau]

/-- There is only one Duskin 1-simplex in the additive double delooping. -/
theorem natDuskinOneSimplex_eq
    (sigma tau : DuskinSimplex NatDoubleDelooping 1) :
    sigma = tau := by
  apply natDuskinSimplex_eq_of_mapComp_eq
  intro a b c f g
  rw [natOneSimplex_mapComp_eq_zero sigma,
    natOneSimplex_mapComp_eq_zero tau]

/-- A Duskin 2-simplex in `B²ℕ` is determined by its unique strict comparison
`0 -> 1 -> 2`. -/
theorem natDuskinTwoSimplex_eq_of_comparison_eq
    (sigma tau : DuskinSimplex NatDoubleDelooping 2)
    (hcomparison : duskinComparison sigma = duskinComparison tau) :
    sigma = tau := by
  apply natDuskinSimplex_eq_of_mapComp_eq
  intro a b c f g
  by_cases habEq : a.as = b.as
  · have habObj : a = b := LocallyDiscrete.ext habEq
    subst b
    have hf : f = 𝟙 a := Subsingleton.elim _ _
    rw [hf, natDuskin_mapComp_id_left_eq_zero sigma,
      natDuskin_mapComp_id_left_eq_zero tau]
  · by_cases hbcEq : b.as = c.as
    · have hbcObj : b = c := LocallyDiscrete.ext hbcEq
      subst c
      have hg : g = 𝟙 b := Subsingleton.elim _ _
      rw [hg, natDuskin_mapComp_id_right_eq_zero sigma,
        natDuskin_mapComp_id_right_eq_zero tau]
    · have hab : a.as ≤ b.as := f.as.le
      have hbc : b.as ≤ c.as := g.as.le
      have ha := a.as.isLt
      have hb := b.as.isLt
      have hc := c.as.isLt
      have habVal : a.as.val < b.as.val :=
        lt_of_le_of_ne hab (fun h => habEq (Fin.ext h))
      have hbcVal : b.as.val < c.as.val :=
        lt_of_le_of_ne hbc (fun h => hbcEq (Fin.ext h))
      have ha0 : a.as = (0 : Fin 3) := by
        apply Fin.ext
        omega
      have hb1 : b.as = (1 : Fin 3) := by
        apply Fin.ext
        omega
      have hc2 : c.as = (2 : Fin 3) := by
        apply Fin.ext
        omega
      have haObj : a = LocallyDiscrete.mk (0 : Fin 3) :=
        LocallyDiscrete.ext ha0
      have hbObj : b = LocallyDiscrete.mk (1 : Fin 3) :=
        LocallyDiscrete.ext hb1
      have hcObj : c = LocallyDiscrete.mk (2 : Fin 3) :=
        LocallyDiscrete.ext hc2
      subst a
      subst b
      subst c
      have hf : f = edge01 := Subsingleton.elim _ _
      have hg : g = edge12 := Subsingleton.elim _ _
      simpa [duskinComparison, hf, hg] using hcomparison

/-! ## The degree-two filler -/

/-- The unique degree-two standard type-(A) generator. -/
def natTypeATwoIndex : StandardTypeAHornGeneratorIndex where
  n := 2
  i := 1
  inner_left := by decide
  inner_right := by decide

/-- Every degree-two type-(A) horn map into `B²ℕ` has the zero-cocycle
completion.  Its restriction agrees with the prescribed horn because the
target has a unique 1-simplex. -/
theorem natTypeATwo_zero_cocycle_completion
    (f : standardTypeAScaledHorn natTypeATwoIndex ⟶
      natDoubleDeloopingScaledDuskin) :
    Nonempty (NatTypeAHornCocycleCompletion natTypeATwoIndex f) := by
  refine ⟨{
    cocycle := NatNormalizedDuskinCocycle.zero 2
    restrict := ?_
    distinguished_zero :=
      NatNormalizedDuskinCocycle.zero_typeADistinguishedZero
        (1 : Fin 3) }⟩
  change
    (Λ[2, (1 : Fin 3)].ι :
      (Λ[2, (1 : Fin 3)] : SSet) ⟶ (Δ[2] : SSet)) ≫
        (NatNormalizedDuskinCocycle.zero 2).toSimplexMap = f.map
  apply SSet.horn.hom_ext
  intro j hj
  exact natDuskinOneSimplex_eq _ _

/-- Literal terminal RLP for the degree-two type-(A) generator. -/
theorem natDoubleDelooping_hasLiftingProperty_standardTypeA_two :
    HasLiftingProperty
      (standardTypeAScaledHornGeneratorHom natTypeATwoIndex)
      (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin) := by
  exact
    natDoubleDelooping_hasLiftingProperty_standardTypeA_of_cocycleCompletions
      natTypeATwoIndex natTypeATwo_zero_cocycle_completion

/-! ## A normalized cocycle from four strict labels in dimension three -/

/-- The four strict triangle labels of a `3`-simplex determine its normalized
cocycle once the single tetrahedron equation holds. -/
def natThreeCocycleOfLabels
    (a012 a013 a023 a123 : Nat)
    (hcoh : NatTetrahedronEquation a012 a013 a023 a123) :
    NatNormalizedDuskinCocycle 3 where
  label a b c _ _ :=
    if a.val = 0 ∧ b.val = 1 ∧ c.val = 2 then a012
    else if a.val = 0 ∧ b.val = 1 ∧ c.val = 3 then a013
    else if a.val = 0 ∧ b.val = 2 ∧ c.val = 3 then a023
    else if a.val = 1 ∧ b.val = 2 ∧ c.val = 3 then a123
    else 0
  left_normalized := by
    intro a b hab
    dsimp
    split_ifs <;> simp_all <;> omega
  right_normalized := by
    intro a b hab
    dsimp
    split_ifs <;> simp_all <;> omega
  tetrahedron := by
    intro a b c d hab hbc hcd
    fin_cases a <;> fin_cases b <;> fin_cases c <;> fin_cases d <;>
      simp_all [NatTetrahedronEquation] <;> omega

@[simp]
theorem natThreeCocycleOfLabels_label012
    (a012 a013 a023 a123 : Nat)
    (hcoh : NatTetrahedronEquation a012 a013 a023 a123) :
    (natThreeCocycleOfLabels a012 a013 a023 a123 hcoh).label
      (0 : Fin 4) 1 2 (by decide) (by decide) = a012 := by
  simp [natThreeCocycleOfLabels]

@[simp]
theorem natThreeCocycleOfLabels_label013
    (a012 a013 a023 a123 : Nat)
    (hcoh : NatTetrahedronEquation a012 a013 a023 a123) :
    (natThreeCocycleOfLabels a012 a013 a023 a123 hcoh).label
      (0 : Fin 4) 1 3 (by decide) (by decide) = a013 := by
  simp [natThreeCocycleOfLabels]

@[simp]
theorem natThreeCocycleOfLabels_label023
    (a012 a013 a023 a123 : Nat)
    (hcoh : NatTetrahedronEquation a012 a013 a023 a123) :
    (natThreeCocycleOfLabels a012 a013 a023 a123 hcoh).label
      (0 : Fin 4) 2 3 (by decide) (by decide) = a023 := by
  simp [natThreeCocycleOfLabels]

@[simp]
theorem natThreeCocycleOfLabels_label123
    (a012 a013 a023 a123 : Nat)
    (hcoh : NatTetrahedronEquation a012 a013 a023 a123) :
    (natThreeCocycleOfLabels a012 a013 a023 a123 hcoh).label
      (1 : Fin 4) 2 3 (by decide) (by decide) = a123 := by
  simp [natThreeCocycleOfLabels]

/-- If `012 = 0`, the four-label cocycle has the type-(A) distinguished-zero
condition at inner index `1`. -/
theorem natThreeCocycle_typeA_i1_zero
    (a013 a023 a123 : Nat)
    (hcoh : NatTetrahedronEquation 0 a013 a023 a123) :
    (natThreeCocycleOfLabels 0 a013 a023 a123 hcoh).
      TypeADistinguishedZero (1 : Fin 4) := by
  intro a b c hab hbc hbi ha hc
  have hb : b.val = 1 := by simpa using congrArg Fin.val hbi
  have ha0 : a.val = 0 := by omega
  have hc2 : c.val = 2 := by omega
  simp [natThreeCocycleOfLabels, ha0, hb, hc2]

/-- If `123 = 0`, the four-label cocycle has the type-(A) distinguished-zero
condition at inner index `2`. -/
theorem natThreeCocycle_typeA_i2_zero
    (a012 a013 a023 : Nat)
    (hcoh : NatTetrahedronEquation a012 a013 a023 0) :
    (natThreeCocycleOfLabels a012 a013 a023 0 hcoh).
      TypeADistinguishedZero (2 : Fin 4) := by
  intro a b c hab hbc hbi ha hc
  have hb : b.val = 2 := by simpa using congrArg Fin.val hbi
  have ha1 : a.val = 1 := by omega
  have hc3 : c.val = 3 := by omega
  simp [natThreeCocycleOfLabels, ha1, hb, hc3]

/-! ## Concrete codimension-one faces of the two 3-horns -/

/-- In `Λ[3,1]`, face `0` is triangle `123`. -/
theorem typeAThree_i1_face0_val
    (h : (0 : Fin 4) ≠ 1) :
    (SSet.horn.face (1 : Fin 4) (0 : Fin 4) h).val =
      SSet.stdSimplex.triangle
        (1 : Fin 4) 2 3 (by decide) (by decide) := by
  apply SSet.stdSimplex.ext
  intro k
  fin_cases k <;> rfl

/-- In `Λ[3,1]`, face `2` is triangle `013`. -/
theorem typeAThree_i1_face2_val
    (h : (2 : Fin 4) ≠ 1) :
    (SSet.horn.face (1 : Fin 4) (2 : Fin 4) h).val =
      SSet.stdSimplex.triangle
        (0 : Fin 4) 1 3 (by decide) (by decide) := by
  apply SSet.stdSimplex.ext
  intro k
  fin_cases k <;> rfl

/-- In `Λ[3,1]`, face `3` is triangle `012`. -/
theorem typeAThree_i1_face3_val
    (h : (3 : Fin 4) ≠ 1) :
    (SSet.horn.face (1 : Fin 4) (3 : Fin 4) h).val =
      SSet.stdSimplex.triangle
        (0 : Fin 4) 1 2 (by decide) (by decide) := by
  apply SSet.stdSimplex.ext
  intro k
  fin_cases k <;> rfl

/-- In `Λ[3,2]`, face `0` is triangle `123`. -/
theorem typeAThree_i2_face0_val
    (h : (0 : Fin 4) ≠ 2) :
    (SSet.horn.face (2 : Fin 4) (0 : Fin 4) h).val =
      SSet.stdSimplex.triangle
        (1 : Fin 4) 2 3 (by decide) (by decide) := by
  apply SSet.stdSimplex.ext
  intro k
  fin_cases k <;> rfl

/-- In `Λ[3,2]`, face `1` is triangle `023`. -/
theorem typeAThree_i2_face1_val
    (h : (1 : Fin 4) ≠ 2) :
    (SSet.horn.face (2 : Fin 4) (1 : Fin 4) h).val =
      SSet.stdSimplex.triangle
        (0 : Fin 4) 2 3 (by decide) (by decide) := by
  apply SSet.stdSimplex.ext
  intro k
  fin_cases k <;> rfl

/-- In `Λ[3,2]`, face `3` is triangle `012`. -/
theorem typeAThree_i2_face3_val
    (h : (3 : Fin 4) ≠ 2) :
    (SSet.horn.face (2 : Fin 4) (3 : Fin 4) h).val =
      SSet.stdSimplex.triangle
        (0 : Fin 4) 1 2 (by decide) (by decide) := by
  apply SSet.stdSimplex.ext
  intro k
  fin_cases k <;> rfl

/-! ## The `n = 3, i = 1` filler -/

/-- The first inner type-(A) generator in dimension three. -/
def natTypeAThreeIndex1 : StandardTypeAHornGeneratorIndex where
  n := 3
  i := 1
  inner_left := by decide
  inner_right := by decide

/-- Label `013` read from a `Λ[3,1]` horn map. -/
def natTypeAThreeI1Label013
    (f : standardTypeAScaledHorn natTypeAThreeIndex1 ⟶
      natDoubleDeloopingScaledDuskin) : Nat :=
  duskinComparison
    (f.map.app (op ⦋2⦌)
      (SSet.horn.face (1 : Fin 4) (2 : Fin 4) (by decide)))

/-- Label `123` read from a `Λ[3,1]` horn map. -/
def natTypeAThreeI1Label123
    (f : standardTypeAScaledHorn natTypeAThreeIndex1 ⟶
      natDoubleDeloopingScaledDuskin) : Nat :=
  duskinComparison
    (f.map.app (op ⦋2⦌)
      (SSet.horn.face (1 : Fin 4) (0 : Fin 4) (by decide)))

/-- The distinguished source face `012` of a scaled `Λ[3,1]` map has zero
comparison. -/
theorem natTypeAThreeI1Label012_eq_zero
    (f : standardTypeAScaledHorn natTypeAThreeIndex1 ⟶
      natDoubleDeloopingScaledDuskin) :
    duskinComparison
      (f.map.app (op ⦋2⦌)
        (SSet.horn.face (1 : Fin 4) (3 : Fin 4) (by decide))) = 0 := by
  apply
    (natDuskin_thin_iff_comparison_eq_zero
      (f.map.app (op ⦋2⦌)
        (SSet.horn.face (1 : Fin 4) (3 : Fin 4) (by decide)))).1
  apply f.scaled
  change
    (standardTypeASimplexScaling (1 : Fin 4)).thin
      (SSet.horn.face (1 : Fin 4) (3 : Fin 4) (by decide)).val
  rw [typeAThree_i1_face3_val]
  exact Or.inr (by simp [IsStandardTypeADistinguishedTriangle])

/-- The additive completion cocycle for `Λ[3,1]`. -/
def natTypeAThreeI1CompletionCocycle
    (f : standardTypeAScaledHorn natTypeAThreeIndex1 ⟶
      natDoubleDeloopingScaledDuskin) :
    NatNormalizedDuskinCocycle 3 :=
  natThreeCocycleOfLabels
    0
    (natTypeAThreeI1Label013 f)
    (natTypeAThreeI1Label123 f + natTypeAThreeI1Label013 f)
    (natTypeAThreeI1Label123 f)
    (natTypeAThree_i1_additive_completion
      (natTypeAThreeI1Label013 f) (natTypeAThreeI1Label123 f))

/-- The completed `Λ[3,1]` cocycle restricts to the original horn map. -/
theorem natTypeAThreeI1CompletionCocycle_restrict
    (f : standardTypeAScaledHorn natTypeAThreeIndex1 ⟶
      natDoubleDeloopingScaledDuskin) :
    (Λ[3, (1 : Fin 4)].ι :
      (Λ[3, (1 : Fin 4)] : SSet) ⟶ (Δ[3] : SSet)) ≫
        (natTypeAThreeI1CompletionCocycle f).toSimplexMap = f.map := by
  apply SSet.horn.hom_ext
  intro j hj
  fin_cases j
  · apply natDuskinTwoSimplex_eq_of_comparison_eq
    change
      duskinComparison
          ((natTypeAThreeI1CompletionCocycle f).toSimplexMap.app
            (op ⦋2⦌)
            (SSet.horn.face (1 : Fin 4) (0 : Fin 4) hj).val) =
        duskinComparison
          (f.map.app (op ⦋2⦌)
            (SSet.horn.face (1 : Fin 4) (0 : Fin 4) hj))
    rw [typeAThree_i1_face0_val,
      NatNormalizedDuskinCocycle.toSimplexMap_triangle_comparison]
    simp [natTypeAThreeI1CompletionCocycle, natTypeAThreeI1Label123]
  · exact (hj rfl).elim
  · apply natDuskinTwoSimplex_eq_of_comparison_eq
    change
      duskinComparison
          ((natTypeAThreeI1CompletionCocycle f).toSimplexMap.app
            (op ⦋2⦌)
            (SSet.horn.face (1 : Fin 4) (2 : Fin 4) hj).val) =
        duskinComparison
          (f.map.app (op ⦋2⦌)
            (SSet.horn.face (1 : Fin 4) (2 : Fin 4) hj))
    rw [typeAThree_i1_face2_val,
      NatNormalizedDuskinCocycle.toSimplexMap_triangle_comparison]
    simp [natTypeAThreeI1CompletionCocycle, natTypeAThreeI1Label013]
  · apply natDuskinTwoSimplex_eq_of_comparison_eq
    change
      duskinComparison
          ((natTypeAThreeI1CompletionCocycle f).toSimplexMap.app
            (op ⦋2⦌)
            (SSet.horn.face (1 : Fin 4) (3 : Fin 4) hj).val) =
        duskinComparison
          (f.map.app (op ⦋2⦌)
            (SSet.horn.face (1 : Fin 4) (3 : Fin 4) hj))
    rw [typeAThree_i1_face3_val,
      NatNormalizedDuskinCocycle.toSimplexMap_triangle_comparison]
    simpa [natTypeAThreeI1CompletionCocycle] using
      (natTypeAThreeI1Label012_eq_zero f).symm

/-- Literal cocycle completion for every scaled `Λ[3,1]` horn map. -/
theorem natTypeAThreeI1_cocycle_completion
    (f : standardTypeAScaledHorn natTypeAThreeIndex1 ⟶
      natDoubleDeloopingScaledDuskin) :
    Nonempty (NatTypeAHornCocycleCompletion natTypeAThreeIndex1 f) := by
  refine ⟨{
    cocycle := natTypeAThreeI1CompletionCocycle f
    restrict := natTypeAThreeI1CompletionCocycle_restrict f
    distinguished_zero := ?_ }⟩
  exact natThreeCocycle_typeA_i1_zero
    (natTypeAThreeI1Label013 f)
    (natTypeAThreeI1Label123 f + natTypeAThreeI1Label013 f)
    (natTypeAThreeI1Label123 f)
    (natTypeAThree_i1_additive_completion
      (natTypeAThreeI1Label013 f) (natTypeAThreeI1Label123 f))

/-- Literal terminal RLP for the `n = 3, i = 1` type-(A) generator. -/
theorem natDoubleDelooping_hasLiftingProperty_standardTypeA_three_i1 :
    HasLiftingProperty
      (standardTypeAScaledHornGeneratorHom natTypeAThreeIndex1)
      (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin) := by
  exact
    natDoubleDelooping_hasLiftingProperty_standardTypeA_of_cocycleCompletions
      natTypeAThreeIndex1 natTypeAThreeI1_cocycle_completion

/-! ## The `n = 3, i = 2` filler -/

/-- The second inner type-(A) generator in dimension three. -/
def natTypeAThreeIndex2 : StandardTypeAHornGeneratorIndex where
  n := 3
  i := 2
  inner_left := by decide
  inner_right := by decide

/-- Label `012` read from a `Λ[3,2]` horn map. -/
def natTypeAThreeI2Label012
    (f : standardTypeAScaledHorn natTypeAThreeIndex2 ⟶
      natDoubleDeloopingScaledDuskin) : Nat :=
  duskinComparison
    (f.map.app (op ⦋2⦌)
      (SSet.horn.face (2 : Fin 4) (3 : Fin 4) (by decide)))

/-- Label `023` read from a `Λ[3,2]` horn map. -/
def natTypeAThreeI2Label023
    (f : standardTypeAScaledHorn natTypeAThreeIndex2 ⟶
      natDoubleDeloopingScaledDuskin) : Nat :=
  duskinComparison
    (f.map.app (op ⦋2⦌)
      (SSet.horn.face (2 : Fin 4) (1 : Fin 4) (by decide)))

/-- The distinguished source face `123` of a scaled `Λ[3,2]` map has zero
comparison. -/
theorem natTypeAThreeI2Label123_eq_zero
    (f : standardTypeAScaledHorn natTypeAThreeIndex2 ⟶
      natDoubleDeloopingScaledDuskin) :
    duskinComparison
      (f.map.app (op ⦋2⦌)
        (SSet.horn.face (2 : Fin 4) (0 : Fin 4) (by decide))) = 0 := by
  apply
    (natDuskin_thin_iff_comparison_eq_zero
      (f.map.app (op ⦋2⦌)
        (SSet.horn.face (2 : Fin 4) (0 : Fin 4) (by decide)))).1
  apply f.scaled
  change
    (standardTypeASimplexScaling (2 : Fin 4)).thin
      (SSet.horn.face (2 : Fin 4) (0 : Fin 4) (by decide)).val
  rw [typeAThree_i2_face0_val]
  exact Or.inr (by simp [IsStandardTypeADistinguishedTriangle])

/-- The additive completion cocycle for `Λ[3,2]`. -/
def natTypeAThreeI2CompletionCocycle
    (f : standardTypeAScaledHorn natTypeAThreeIndex2 ⟶
      natDoubleDeloopingScaledDuskin) :
    NatNormalizedDuskinCocycle 3 :=
  natThreeCocycleOfLabels
    (natTypeAThreeI2Label012 f)
    (natTypeAThreeI2Label012 f + natTypeAThreeI2Label023 f)
    (natTypeAThreeI2Label023 f)
    0
    (natTypeAThree_i2_additive_completion
      (natTypeAThreeI2Label012 f) (natTypeAThreeI2Label023 f))

/-- The completed `Λ[3,2]` cocycle restricts to the original horn map. -/
theorem natTypeAThreeI2CompletionCocycle_restrict
    (f : standardTypeAScaledHorn natTypeAThreeIndex2 ⟶
      natDoubleDeloopingScaledDuskin) :
    (Λ[3, (2 : Fin 4)].ι :
      (Λ[3, (2 : Fin 4)] : SSet) ⟶ (Δ[3] : SSet)) ≫
        (natTypeAThreeI2CompletionCocycle f).toSimplexMap = f.map := by
  apply SSet.horn.hom_ext
  intro j hj
  fin_cases j
  · apply natDuskinTwoSimplex_eq_of_comparison_eq
    change
      duskinComparison
          ((natTypeAThreeI2CompletionCocycle f).toSimplexMap.app
            (op ⦋2⦌)
            (SSet.horn.face (2 : Fin 4) (0 : Fin 4) hj).val) =
        duskinComparison
          (f.map.app (op ⦋2⦌)
            (SSet.horn.face (2 : Fin 4) (0 : Fin 4) hj))
    rw [typeAThree_i2_face0_val,
      NatNormalizedDuskinCocycle.toSimplexMap_triangle_comparison]
    simpa [natTypeAThreeI2CompletionCocycle] using
      (natTypeAThreeI2Label123_eq_zero f).symm
  · apply natDuskinTwoSimplex_eq_of_comparison_eq
    change
      duskinComparison
          ((natTypeAThreeI2CompletionCocycle f).toSimplexMap.app
            (op ⦋2⦌)
            (SSet.horn.face (2 : Fin 4) (1 : Fin 4) hj).val) =
        duskinComparison
          (f.map.app (op ⦋2⦌)
            (SSet.horn.face (2 : Fin 4) (1 : Fin 4) hj))
    rw [typeAThree_i2_face1_val,
      NatNormalizedDuskinCocycle.toSimplexMap_triangle_comparison]
    simp [natTypeAThreeI2CompletionCocycle, natTypeAThreeI2Label023]
  · exact (hj rfl).elim
  · apply natDuskinTwoSimplex_eq_of_comparison_eq
    change
      duskinComparison
          ((natTypeAThreeI2CompletionCocycle f).toSimplexMap.app
            (op ⦋2⦌)
            (SSet.horn.face (2 : Fin 4) (3 : Fin 4) hj).val) =
        duskinComparison
          (f.map.app (op ⦋2⦌)
            (SSet.horn.face (2 : Fin 4) (3 : Fin 4) hj))
    rw [typeAThree_i2_face3_val,
      NatNormalizedDuskinCocycle.toSimplexMap_triangle_comparison]
    simp [natTypeAThreeI2CompletionCocycle, natTypeAThreeI2Label012]

/-- Literal cocycle completion for every scaled `Λ[3,2]` horn map. -/
theorem natTypeAThreeI2_cocycle_completion
    (f : standardTypeAScaledHorn natTypeAThreeIndex2 ⟶
      natDoubleDeloopingScaledDuskin) :
    Nonempty (NatTypeAHornCocycleCompletion natTypeAThreeIndex2 f) := by
  refine ⟨{
    cocycle := natTypeAThreeI2CompletionCocycle f
    restrict := natTypeAThreeI2CompletionCocycle_restrict f
    distinguished_zero := ?_ }⟩
  exact natThreeCocycle_typeA_i2_zero
    (natTypeAThreeI2Label012 f)
    (natTypeAThreeI2Label012 f + natTypeAThreeI2Label023 f)
    (natTypeAThreeI2Label023 f)
    (natTypeAThree_i2_additive_completion
      (natTypeAThreeI2Label012 f) (natTypeAThreeI2Label023 f))

/-- Literal terminal RLP for the `n = 3, i = 2` type-(A) generator. -/
theorem natDoubleDelooping_hasLiftingProperty_standardTypeA_three_i2 :
    HasLiftingProperty
      (standardTypeAScaledHornGeneratorHom natTypeAThreeIndex2)
      (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin) := by
  exact
    natDoubleDelooping_hasLiftingProperty_standardTypeA_of_cocycleCompletions
      natTypeAThreeIndex2 natTypeAThreeI2_cocycle_completion

/-!
The literal low-dimensional type-(A) fillers are now complete:

```text
n = 2, i = 1 : zero cocycle;
n = 3, i = 1 : 023 := 123 + 013, with 012 = 0;
n = 3, i = 2 : 013 := 012 + 023, with 123 = 0.
```

Every displayed formula is realized as a genuine scaled simplicial lift, not
merely as arithmetic.  The remaining type-(A) completion theorem is therefore
entirely the `n = 4` missing tetrahedron equation plus the `n ≥ 5` visibility
case established arithmetically in v1.99.
-/

end KUOS.DependentOriginationDoubleDeloopingTypeALowDimensionalFillersV1_102
