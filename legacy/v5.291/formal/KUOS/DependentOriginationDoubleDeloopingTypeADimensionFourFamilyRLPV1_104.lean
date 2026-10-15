import KUOS.DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103

namespace KUOS.DependentOriginationDoubleDeloopingTypeADimensionFourFamilyRLPV1_104

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
open KUOS.DependentOriginationDoubleDeloopingTypeALowDimensionalFillersV1_102
open KUOS.DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103

/-!
# Dimension-four closure and the complete standard type-(A) terminal RLP v1.104

Versions v1.102 and v1.103 close the standard type-(A) lifting problem in
simplicial dimensions `2`, `3`, and every dimension at least `5`.  The sole
remaining dimension is `4`.

In a four-horn every triangle is visible, so the ten comparison labels are
already prescribed by the horn map.  Four of the five tetrahedral equations
are visible as codimension-one faces.  Version v1.99 proves that any four of
those equations imply the fifth.  This file packages that finite dependency
into a normalized additive cocycle and realizes it as a literal scaled filler.

The last section combines the low-, four-, and high-dimensional constructions
for an arbitrary `StandardTypeAHornGeneratorIndex`.  Hence the concrete
terminal map of the additive double delooping belongs unconditionally to the
right class of the complete standard type-(A) generator family.
-/

/-! ## A tetrahedral equation from any visible horn 3-simplex -/

/-- If a horn 3-simplex has ordered vertices `a <= b <= c <= d`, then the four
ambient visible triangle labels satisfy the corresponding additive Duskin
cocycle equation.  This is the dimension-four form of the naturality argument
used in v1.103, but it only assumes that the particular tetrahedron is present
in the horn. -/
theorem natTypeAHornLabel_tetrahedron_of_hornSimplex
    (g : StandardTypeAHornGeneratorIndex)
    (hn : 4 ≤ g.n)
    (f : standardTypeAScaledHorn g ⟶ natDoubleDeloopingScaledDuskin)
    (a b c d : Fin (g.n + 1))
    (hab : a ≤ b) (hbc : b ≤ c) (hcd : c ≤ d)
    (x : (Λ[g.n, g.i] : SSet).obj (op ⦋3⦌))
    (hx : x.val = natOrderedTetrahedron a b c d hab hbc hcd) :
    NatTetrahedronEquation
      (natTypeAHornLabel g hn f a b c hab hbc)
      (natTypeAHornLabel g hn f a b d hab (hbc.trans hcd))
      (natTypeAHornLabel g hn f a c d (hab.trans hbc) hcd)
      (natTypeAHornLabel g hn f b c d hbc hcd) := by
  let sigma : DuskinSimplex NatDoubleDelooping 3 :=
    f.map.app (op ⦋3⦌) x
  let e01 :
      LocallyDiscrete.mk (0 : Fin 4) ⟶ LocallyDiscrete.mk (1 : Fin 4) :=
    natOrdinalEdge (by decide)
  let e12 :
      LocallyDiscrete.mk (1 : Fin 4) ⟶ LocallyDiscrete.mk (2 : Fin 4) :=
    natOrdinalEdge (by decide)
  let e23 :
      LocallyDiscrete.mk (2 : Fin 4) ⟶ LocallyDiscrete.mk (3 : Fin 4) :=
    natOrdinalEdge (by decide)
  have hcoc := natDuskin_mapComp_additive_cocycle sigma e01 e12 e23
  have h012 := natTypeAHornMap_mapComp_eq_label g hn f x e01 e12
  have h023 :=
    natTypeAHornMap_mapComp_eq_label g hn f x (e01 ≫ e12) e23
  have h123 := natTypeAHornMap_mapComp_eq_label g hn f x e12 e23
  have h013 :=
    natTypeAHornMap_mapComp_eq_label g hn f x e01 (e12 ≫ e23)
  rw [h012, h023, h123, h013] at hcoc
  have hx0 : x.val (0 : Fin 4) = a := by
    rw [hx]
    rfl
  have hx1 : x.val (1 : Fin 4) = b := by
    rw [hx]
    rfl
  have hx2 : x.val (2 : Fin 4) = c := by
    rw [hx]
    rfl
  have hx3 : x.val (3 : Fin 4) = d := by
    rw [hx]
    rfl
  rw [hx0, hx1, hx2, hx3] at hcoc
  simpa [NatTetrahedronEquation, sigma, e01, e12, e23] using hcoc

/-! ## The five codimension-one tetrahedra of `Delta[4]` -/

/-- Face `0` has ordered vertices `1234`. -/
theorem natTypeAFour_face0_val
    (i : Fin 5) (h : (0 : Fin 5) ≠ i) :
    (SSet.horn.face i (0 : Fin 5) h).val =
      natOrderedTetrahedron
        (1 : Fin 5) 2 3 4 (by decide) (by decide) (by decide) := by
  apply SSet.stdSimplex.ext
  intro k
  fin_cases k <;> rfl

/-- Face `1` has ordered vertices `0234`. -/
theorem natTypeAFour_face1_val
    (i : Fin 5) (h : (1 : Fin 5) ≠ i) :
    (SSet.horn.face i (1 : Fin 5) h).val =
      natOrderedTetrahedron
        (0 : Fin 5) 2 3 4 (by decide) (by decide) (by decide) := by
  apply SSet.stdSimplex.ext
  intro k
  fin_cases k <;> rfl

/-- Face `2` has ordered vertices `0134`. -/
theorem natTypeAFour_face2_val
    (i : Fin 5) (h : (2 : Fin 5) ≠ i) :
    (SSet.horn.face i (2 : Fin 5) h).val =
      natOrderedTetrahedron
        (0 : Fin 5) 1 3 4 (by decide) (by decide) (by decide) := by
  apply SSet.stdSimplex.ext
  intro k
  fin_cases k <;> rfl

/-- Face `3` has ordered vertices `0124`. -/
theorem natTypeAFour_face3_val
    (i : Fin 5) (h : (3 : Fin 5) ≠ i) :
    (SSet.horn.face i (3 : Fin 5) h).val =
      natOrderedTetrahedron
        (0 : Fin 5) 1 2 4 (by decide) (by decide) (by decide) := by
  apply SSet.stdSimplex.ext
  intro k
  fin_cases k <;> rfl

/-- Face `4` has ordered vertices `0123`. -/
theorem natTypeAFour_face4_val
    (i : Fin 5) (h : (4 : Fin 5) ≠ i) :
    (SSet.horn.face i (4 : Fin 5) h).val =
      natOrderedTetrahedron
        (0 : Fin 5) 1 2 3 (by decide) (by decide) (by decide) := by
  apply SSet.stdSimplex.ext
  intro k
  fin_cases k <;> rfl

/-! ## Dimension-four inner indexes and their ten visible labels -/

/-- A standard type-(A) dimension-four index with an arbitrary inner vertex. -/
def natTypeAFourIndex
    (i : Fin 5)
    (h0 : 0 < i)
    (h4 : i < Fin.last 4) : StandardTypeAHornGeneratorIndex where
  n := 4
  i := i
  inner_left := h0
  inner_right := h4

/-- The ten visible triangle labels of a dimension-four type-(A) horn. -/
def natTypeAFourLabels
    (i : Fin 5)
    (h0 : 0 < i)
    (h4 : i < Fin.last 4)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i h0 h4) ⟶
      natDoubleDeloopingScaledDuskin) : NatFourSimplexTriangleLabels where
  a012 := natTypeAHornLabel (natTypeAFourIndex i h0 h4) (by decide) f
    (0 : Fin 5) 1 2 (by decide) (by decide)
  a013 := natTypeAHornLabel (natTypeAFourIndex i h0 h4) (by decide) f
    (0 : Fin 5) 1 3 (by decide) (by decide)
  a014 := natTypeAHornLabel (natTypeAFourIndex i h0 h4) (by decide) f
    (0 : Fin 5) 1 4 (by decide) (by decide)
  a023 := natTypeAHornLabel (natTypeAFourIndex i h0 h4) (by decide) f
    (0 : Fin 5) 2 3 (by decide) (by decide)
  a024 := natTypeAHornLabel (natTypeAFourIndex i h0 h4) (by decide) f
    (0 : Fin 5) 2 4 (by decide) (by decide)
  a034 := natTypeAHornLabel (natTypeAFourIndex i h0 h4) (by decide) f
    (0 : Fin 5) 3 4 (by decide) (by decide)
  a123 := natTypeAHornLabel (natTypeAFourIndex i h0 h4) (by decide) f
    (1 : Fin 5) 2 3 (by decide) (by decide)
  a124 := natTypeAHornLabel (natTypeAFourIndex i h0 h4) (by decide) f
    (1 : Fin 5) 2 4 (by decide) (by decide)
  a134 := natTypeAHornLabel (natTypeAFourIndex i h0 h4) (by decide) f
    (1 : Fin 5) 3 4 (by decide) (by decide)
  a234 := natTypeAHornLabel (natTypeAFourIndex i h0 h4) (by decide) f
    (2 : Fin 5) 3 4 (by decide) (by decide)

/-- Visible face `0` gives equation `1234`. -/
theorem natTypeAFour_face0_eq1234
    (i : Fin 5) (h0 : 0 < i) (h4 : i < Fin.last 4)
    (hi : (0 : Fin 5) ≠ i)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i h0 h4) ⟶
      natDoubleDeloopingScaledDuskin) :
    (natTypeAFourLabels i h0 h4 f).eq1234 := by
  have h := natTypeAHornLabel_tetrahedron_of_hornSimplex
    (natTypeAFourIndex i h0 h4) (by decide) f
    (1 : Fin 5) 2 3 4 (by decide) (by decide) (by decide)
    (SSet.horn.face i (0 : Fin 5) hi)
    (natTypeAFour_face0_val i hi)
  simpa [natTypeAFourLabels, NatFourSimplexTriangleLabels.eq1234] using h

/-- Visible face `1` gives equation `0234`. -/
theorem natTypeAFour_face1_eq0234
    (i : Fin 5) (h0 : 0 < i) (h4 : i < Fin.last 4)
    (hi : (1 : Fin 5) ≠ i)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i h0 h4) ⟶
      natDoubleDeloopingScaledDuskin) :
    (natTypeAFourLabels i h0 h4 f).eq0234 := by
  have h := natTypeAHornLabel_tetrahedron_of_hornSimplex
    (natTypeAFourIndex i h0 h4) (by decide) f
    (0 : Fin 5) 2 3 4 (by decide) (by decide) (by decide)
    (SSet.horn.face i (1 : Fin 5) hi)
    (natTypeAFour_face1_val i hi)
  simpa [natTypeAFourLabels, NatFourSimplexTriangleLabels.eq0234] using h

/-- Visible face `2` gives equation `0134`. -/
theorem natTypeAFour_face2_eq0134
    (i : Fin 5) (h0 : 0 < i) (h4 : i < Fin.last 4)
    (hi : (2 : Fin 5) ≠ i)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i h0 h4) ⟶
      natDoubleDeloopingScaledDuskin) :
    (natTypeAFourLabels i h0 h4 f).eq0134 := by
  have h := natTypeAHornLabel_tetrahedron_of_hornSimplex
    (natTypeAFourIndex i h0 h4) (by decide) f
    (0 : Fin 5) 1 3 4 (by decide) (by decide) (by decide)
    (SSet.horn.face i (2 : Fin 5) hi)
    (natTypeAFour_face2_val i hi)
  simpa [natTypeAFourLabels, NatFourSimplexTriangleLabels.eq0134] using h

/-- Visible face `3` gives equation `0124`. -/
theorem natTypeAFour_face3_eq0124
    (i : Fin 5) (h0 : 0 < i) (h4 : i < Fin.last 4)
    (hi : (3 : Fin 5) ≠ i)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i h0 h4) ⟶
      natDoubleDeloopingScaledDuskin) :
    (natTypeAFourLabels i h0 h4 f).eq0124 := by
  have h := natTypeAHornLabel_tetrahedron_of_hornSimplex
    (natTypeAFourIndex i h0 h4) (by decide) f
    (0 : Fin 5) 1 2 4 (by decide) (by decide) (by decide)
    (SSet.horn.face i (3 : Fin 5) hi)
    (natTypeAFour_face3_val i hi)
  simpa [natTypeAFourLabels, NatFourSimplexTriangleLabels.eq0124] using h

/-- Visible face `4` gives equation `0123`. -/
theorem natTypeAFour_face4_eq0123
    (i : Fin 5) (h0 : 0 < i) (h4 : i < Fin.last 4)
    (hi : (4 : Fin 5) ≠ i)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i h0 h4) ⟶
      natDoubleDeloopingScaledDuskin) :
    (natTypeAFourLabels i h0 h4 f).eq0123 := by
  have h := natTypeAHornLabel_tetrahedron_of_hornSimplex
    (natTypeAFourIndex i h0 h4) (by decide) f
    (0 : Fin 5) 1 2 3 (by decide) (by decide) (by decide)
    (SSet.horn.face i (4 : Fin 5) hi)
    (natTypeAFour_face4_val i hi)
  simpa [natTypeAFourLabels, NatFourSimplexTriangleLabels.eq0123] using h

/-- For every inner dimension-four index, the four visible face equations plus
the v1.99 dependency give all five tetrahedral equations. -/
theorem natTypeAFourLabels_all_equations
    (i : Fin 5) (h0 : 0 < i) (h4 : i < Fin.last 4)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i h0 h4) ⟶
      natDoubleDeloopingScaledDuskin) :
    (natTypeAFourLabels i h0 h4 f).eq0123 ∧
      (natTypeAFourLabels i h0 h4 f).eq0124 ∧
      (natTypeAFourLabels i h0 h4 f).eq0134 ∧
      (natTypeAFourLabels i h0 h4 f).eq0234 ∧
      (natTypeAFourLabels i h0 h4 f).eq1234 := by
  fin_cases i
  · omega
  · have h0123 := natTypeAFour_face4_eq0123
      (1 : Fin 5) h0 h4 (by decide) f
    have h0124 := natTypeAFour_face3_eq0124
      (1 : Fin 5) h0 h4 (by decide) f
    have h0134 := natTypeAFour_face2_eq0134
      (1 : Fin 5) h0 h4 (by decide) f
    have h1234 := natTypeAFour_face0_eq1234
      (1 : Fin 5) h0 h4 (by decide) f
    have h0234 := natFour_typeA_index1_missing_face
      (natTypeAFourLabels (1 : Fin 5) h0 h4 f)
      h0123 h0124 h0134 h1234
    exact ⟨h0123, h0124, h0134, h0234, h1234⟩
  · have h0123 := natTypeAFour_face4_eq0123
      (2 : Fin 5) h0 h4 (by decide) f
    have h0124 := natTypeAFour_face3_eq0124
      (2 : Fin 5) h0 h4 (by decide) f
    have h0234 := natTypeAFour_face1_eq0234
      (2 : Fin 5) h0 h4 (by decide) f
    have h1234 := natTypeAFour_face0_eq1234
      (2 : Fin 5) h0 h4 (by decide) f
    have h0134 := natFour_typeA_index2_missing_face
      (natTypeAFourLabels (2 : Fin 5) h0 h4 f)
      h0123 h0124 h0234 h1234
    exact ⟨h0123, h0124, h0134, h0234, h1234⟩
  · have h0123 := natTypeAFour_face4_eq0123
      (3 : Fin 5) h0 h4 (by decide) f
    have h0134 := natTypeAFour_face2_eq0134
      (3 : Fin 5) h0 h4 (by decide) f
    have h0234 := natTypeAFour_face1_eq0234
      (3 : Fin 5) h0 h4 (by decide) f
    have h1234 := natTypeAFour_face0_eq1234
      (3 : Fin 5) h0 h4 (by decide) f
    have h0124 := natFour_typeA_index3_missing_face
      (natTypeAFourLabels (3 : Fin 5) h0 h4 f)
      h0123 h0134 h0234 h1234
    exact ⟨h0123, h0124, h0134, h0234, h1234⟩
  · omega

/-! ## The completed normalized cocycle in dimension four -/

/-- All ten horn labels form a normalized additive cocycle in dimension four.
Repeated adjacent vertices are handled by normalization; a strict ordered
quadruple in `Fin 5` is one of the five tetrahedra above. -/
def natTypeAFourCocycle
    (i : Fin 5) (h0 : 0 < i) (h4 : i < Fin.last 4)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i h0 h4) ⟶
      natDoubleDeloopingScaledDuskin) : NatNormalizedDuskinCocycle 4 where
  label := natTypeAHornLabel (natTypeAFourIndex i h0 h4) (by decide) f
  left_normalized := by
    intro a b hab
    exact natTypeAHornLabel_left_zero
      (natTypeAFourIndex i h0 h4) (by decide) f a b hab
  right_normalized := by
    intro a b hab
    exact natTypeAHornLabel_right_zero
      (natTypeAFourIndex i h0 h4) (by decide) f a b hab
  tetrahedron := by
    intro a b c d hab hbc hcd
    rcases natTypeAFourLabels_all_equations i h0 h4 f with
      ⟨h0123, h0124, h0134, h0234, h1234⟩
    by_cases habEq : a = b
    · subst b
      rw [natTypeAHornLabel_left_zero
            (natTypeAFourIndex i h0 h4) (by decide) f a c hbc,
          natTypeAHornLabel_left_zero
            (natTypeAFourIndex i h0 h4) (by decide) f a d
              (hbc.trans hcd)]
      simp
    · by_cases hbcEq : b = c
      · subst c
        rw [natTypeAHornLabel_right_zero
              (natTypeAFourIndex i h0 h4) (by decide) f a b hab,
            natTypeAHornLabel_left_zero
              (natTypeAFourIndex i h0 h4) (by decide) f b d hcd]
        simp
      · by_cases hcdEq : c = d
        · subst d
          rw [natTypeAHornLabel_right_zero
                (natTypeAFourIndex i h0 h4) (by decide) f a c
                  (hab.trans hbc),
              natTypeAHornLabel_right_zero
                (natTypeAFourIndex i h0 h4) (by decide) f b c hbc]
          simp
        · have habVal : a.val < b.val := by
            have hne : a.val ≠ b.val := by
              intro h
              exact habEq (Fin.ext h)
            omega
          have hbcVal : b.val < c.val := by
            have hne : b.val ≠ c.val := by
              intro h
              exact hbcEq (Fin.ext h)
            omega
          have hcdVal : c.val < d.val := by
            have hne : c.val ≠ d.val := by
              intro h
              exact hcdEq (Fin.ext h)
            omega
          have haBound := a.isLt
          have hbBound := b.isLt
          have hcBound := c.isLt
          have hdBound := d.isLt
          have hcases :
              (a.val = 0 ∧ b.val = 1 ∧ c.val = 2 ∧ d.val = 3) ∨
              (a.val = 0 ∧ b.val = 1 ∧ c.val = 2 ∧ d.val = 4) ∨
              (a.val = 0 ∧ b.val = 1 ∧ c.val = 3 ∧ d.val = 4) ∨
              (a.val = 0 ∧ b.val = 2 ∧ c.val = 3 ∧ d.val = 4) ∨
              (a.val = 1 ∧ b.val = 2 ∧ c.val = 3 ∧ d.val = 4) := by
            omega
          rcases hcases with h | h | h | h | h
          · rcases h with ⟨ha, hb, hc, hd⟩
            have ha' : a = (0 : Fin 5) := by apply Fin.ext; omega
            have hb' : b = (1 : Fin 5) := by apply Fin.ext; omega
            have hc' : c = (2 : Fin 5) := by apply Fin.ext; omega
            have hd' : d = (3 : Fin 5) := by apply Fin.ext; omega
            subst a
            subst b
            subst c
            subst d
            simpa [natTypeAFourLabels,
              NatFourSimplexTriangleLabels.eq0123,
              NatTetrahedronEquation] using h0123
          · rcases h with ⟨ha, hb, hc, hd⟩
            have ha' : a = (0 : Fin 5) := by apply Fin.ext; omega
            have hb' : b = (1 : Fin 5) := by apply Fin.ext; omega
            have hc' : c = (2 : Fin 5) := by apply Fin.ext; omega
            have hd' : d = (4 : Fin 5) := by apply Fin.ext; omega
            subst a
            subst b
            subst c
            subst d
            simpa [natTypeAFourLabels,
              NatFourSimplexTriangleLabels.eq0124,
              NatTetrahedronEquation] using h0124
          · rcases h with ⟨ha, hb, hc, hd⟩
            have ha' : a = (0 : Fin 5) := by apply Fin.ext; omega
            have hb' : b = (1 : Fin 5) := by apply Fin.ext; omega
            have hc' : c = (3 : Fin 5) := by apply Fin.ext; omega
            have hd' : d = (4 : Fin 5) := by apply Fin.ext; omega
            subst a
            subst b
            subst c
            subst d
            simpa [natTypeAFourLabels,
              NatFourSimplexTriangleLabels.eq0134,
              NatTetrahedronEquation] using h0134
          · rcases h with ⟨ha, hb, hc, hd⟩
            have ha' : a = (0 : Fin 5) := by apply Fin.ext; omega
            have hb' : b = (2 : Fin 5) := by apply Fin.ext; omega
            have hc' : c = (3 : Fin 5) := by apply Fin.ext; omega
            have hd' : d = (4 : Fin 5) := by apply Fin.ext; omega
            subst a
            subst b
            subst c
            subst d
            simpa [natTypeAFourLabels,
              NatFourSimplexTriangleLabels.eq0234,
              NatTetrahedronEquation] using h0234
          · rcases h with ⟨ha, hb, hc, hd⟩
            have ha' : a = (1 : Fin 5) := by apply Fin.ext; omega
            have hb' : b = (2 : Fin 5) := by apply Fin.ext; omega
            have hc' : c = (3 : Fin 5) := by apply Fin.ext; omega
            have hd' : d = (4 : Fin 5) := by apply Fin.ext; omega
            subst a
            subst b
            subst c
            subst d
            simpa [natTypeAFourLabels,
              NatFourSimplexTriangleLabels.eq1234,
              NatTetrahedronEquation] using h1234

/-- The dimension-four realized cocycle restricts literally to the original
horn map. -/
theorem natTypeAFourCocycle_restrict
    (i : Fin 5) (h0 : 0 < i) (h4 : i < Fin.last 4)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i h0 h4) ⟶
      natDoubleDeloopingScaledDuskin) :
    (Λ[4, i].ι : (Λ[4, i] : SSet) ⟶ (Δ[4] : SSet)) ≫
        (natTypeAFourCocycle i h0 h4 f).toSimplexMap = f.map := by
  ext Δ x
  rcases Δ with ⟨⟨m⟩⟩
  apply natDuskinSimplex_eq_of_mapComp_eq
  intro a b c p q
  change
    ((natTypeAFourCocycle i h0 h4 f).toSimplexMap.app
      (op ⦋m⦌) x.val).mapComp p q =
      (f.map.app (op ⦋m⦌) x).mapComp p q
  rw [NatNormalizedDuskinCocycle.toSimplexMap_mapComp]
  exact
    (natTypeAHornMap_mapComp_eq_label
      (natTypeAFourIndex i h0 h4) (by decide) f x p q).symm

/-- The completed dimension-four cocycle vanishes on the distinguished
consecutive type-(A) triangle. -/
theorem natTypeAFourCocycle_distinguished_zero
    (i : Fin 5) (h0 : 0 < i) (h4 : i < Fin.last 4)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i h0 h4) ⟶
      natDoubleDeloopingScaledDuskin) :
    (natTypeAFourCocycle i h0 h4 f).TypeADistinguishedZero i := by
  intro a b c hab hbc hbi ha hc
  change
    natTypeAHornLabel (natTypeAFourIndex i h0 h4) (by decide) f
      a b c hab hbc = 0
  exact natTypeAHornLabel_distinguished_zero
    (natTypeAFourIndex i h0 h4) (by decide) f
    a b c hab hbc hbi ha hc

/-- Every dimension-four standard type-(A) horn map has a literal normalized
cocycle completion. -/
theorem natTypeAFour_cocycle_completion
    (i : Fin 5) (h0 : 0 < i) (h4 : i < Fin.last 4)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i h0 h4) ⟶
      natDoubleDeloopingScaledDuskin) :
    Nonempty (NatTypeAHornCocycleCompletion (natTypeAFourIndex i h0 h4) f) := by
  refine ⟨{
    cocycle := natTypeAFourCocycle i h0 h4 f
    restrict := natTypeAFourCocycle_restrict i h0 h4 f
    distinguished_zero := natTypeAFourCocycle_distinguished_zero i h0 h4 f }⟩

/-- Literal terminal RLP for every standard type-(A) generator in dimension
four. -/
theorem natDoubleDelooping_hasLiftingProperty_standardTypeA_four
    (i : Fin 5) (h0 : 0 < i) (h4 : i < Fin.last 4) :
    HasLiftingProperty
      (standardTypeAScaledHornGeneratorHom (natTypeAFourIndex i h0 h4))
      (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin) := by
  exact natDoubleDelooping_hasLiftingProperty_standardTypeA_of_cocycleCompletions
    (natTypeAFourIndex i h0 h4)
    (natTypeAFour_cocycle_completion i h0 h4)

/-! ## Assemble all dimensions -/

/-- The low-dimensional explicit fillers, the dimension-four dependency, and
the high-dimensional visibility construction together complete every standard
type-(A) inner horn cocycle. -/
theorem natDoubleDelooping_hasAllStandardTypeAHornCocycleCompletions :
    HasAllStandardTypeAHornCocycleCompletions := by
  intro g f
  rcases g with ⟨n, i, h0, hN⟩
  have h0v := h0
  have hNv := hN
  simp only [← Fin.val_fin_lt, Fin.val_zero, Fin.val_last] at h0v hNv
  have hnLower : 2 ≤ n := by omega
  by_cases hn2 : n = 2
  · subst n
    fin_cases i
    · omega
    · simpa [natTypeATwoIndex] using natTypeATwo_zero_cocycle_completion f
    · omega
  · by_cases hn3 : n = 3
    · subst n
      fin_cases i
      · omega
      · simpa [natTypeAThreeIndex1] using natTypeAThreeI1_cocycle_completion f
      · simpa [natTypeAThreeIndex2] using natTypeAThreeI2_cocycle_completion f
      · omega
    · by_cases hn4 : n = 4
      · subst n
        exact natTypeAFour_cocycle_completion i h0 hN f
      · have hn5 : 5 ≤ n := by omega
        exact natTypeAHigh_cocycle_completion
          ⟨n, i, h0, hN⟩ hn5 f

/-- The concrete terminal map of `B²ℕ` has the right lifting property against
the complete standard type-(A) generator family. -/
theorem natDoubleDelooping_standardTypeA_rlp :
    (standardTypeAScaledHornGenerators : MorphismProperty ScaledSSet).rlp
      (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin) := by
  exact natDoubleDelooping_standardTypeA_rlp_of_cocycleCompletions
    natDoubleDelooping_hasAllStandardTypeAHornCocycleCompletions

/-!
The standard type-(A) terminal obligation is now completely closed:

```text
n = 2      zero thin replacement                 -- v1.102
n = 3      additive completion                    -- v1.102
n = 4      four visible equations imply fifth    -- v1.104
n >= 5     all tetrahedra visible                 -- v1.103
-----------------------------------------------------------
all type-(A) generators have terminal RLP
```

Together with the already completed standard type-(B) terminal RLP of v1.98,
the only remaining generator-family obligation for the explicit standard
A/B/C right-class certificate is type-(C) collapsed-edge lifting.
-/

end KUOS.DependentOriginationDoubleDeloopingTypeADimensionFourFamilyRLPV1_104
