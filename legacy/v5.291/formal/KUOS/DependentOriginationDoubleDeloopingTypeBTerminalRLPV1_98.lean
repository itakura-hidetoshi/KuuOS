import KUOS.DependentOriginationDoubleDeloopingTypeBTetrahedralZeroV1_97
import KUOS.DependentOriginationStandardTypeBScalingPushoutV1_56

namespace KUOS.DependentOriginationDoubleDeloopingTypeBTerminalRLPV1_98

open CategoryTheory
open CategoryTheory.Category
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeBScalingPushoutV1_56
open KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95
open KUOS.DependentOriginationDoubleDeloopingThinComparisonZeroV1_96
open KUOS.DependentOriginationDoubleDeloopingTypeBTetrahedralZeroV1_97

/-!
# Concrete standard type-(B) terminal lifting for `B²ℕ` v1.98

Version v1.97 reduced the standard type-(B) scaling cell to the additive
four-simplex implication

```text
012 = 024 = 013 = 134 = 0  ->  014 = 034 = 0.
```

Version v1.96 identifies zero comparison labels with thin Duskin triangles.
This file closes the remaining Yoneda bridge and proves the literal terminal
right lifting property of the standard type-(B) generator for the concrete
scaled Duskin nerve of the additive double delooping.

The lift does not alter the underlying simplicial map.  A source-scaled map
`Delta[4] -> N_D(B²ℕ)` determines, by Yoneda, one Duskin four-simplex `sigma`.
The four source-thin named triangles give zero labels, tetrahedral propagation
gives zero on `014` and `034`, and those two zeros are exactly the additional
scaledness obligations in the type-(B) target.
-/

/-! ## Named standard triangles -/

/-- Triangle `012` in the standard four-simplex. -/
def natTypeBTriangle012 : (Δ[4] : SSet).obj (op ⦋2⦌) :=
  SSet.stdSimplex.triangle
    (0 : Fin 5) 1 2 (by decide) (by decide)

/-- Triangle `024` in the standard four-simplex. -/
def natTypeBTriangle024 : (Δ[4] : SSet).obj (op ⦋2⦌) :=
  SSet.stdSimplex.triangle
    (0 : Fin 5) 2 4 (by decide) (by decide)

/-- Triangle `013` in the standard four-simplex. -/
def natTypeBTriangle013 : (Δ[4] : SSet).obj (op ⦋2⦌) :=
  SSet.stdSimplex.triangle
    (0 : Fin 5) 1 3 (by decide) (by decide)

/-- Triangle `134` in the standard four-simplex. -/
def natTypeBTriangle134 : (Δ[4] : SSet).obj (op ⦋2⦌) :=
  SSet.stdSimplex.triangle
    (1 : Fin 5) 3 4 (by decide) (by decide)

/-- Target-only triangle `014`. -/
def natTypeBTriangle014 : (Δ[4] : SSet).obj (op ⦋2⦌) :=
  SSet.stdSimplex.triangle
    (0 : Fin 5) 1 4 (by decide) (by decide)

/-- Target-only triangle `034`. -/
def natTypeBTriangle034 : (Δ[4] : SSet).obj (op ⦋2⦌) :=
  SSet.stdSimplex.triangle
    (0 : Fin 5) 3 4 (by decide) (by decide)

/-- `012` is source-thin for the standard type-(B) cell. -/
theorem natTypeBTriangle012_source_thin :
    standardTypeBSourceScaling.thin natTypeBTriangle012 := by
  exact Or.inr
    (Or.inr (Or.inr (Or.inr (Or.inr ⟨rfl, rfl, rfl⟩))))

/-- `024` is source-thin for the standard type-(B) cell. -/
theorem natTypeBTriangle024_source_thin :
    standardTypeBSourceScaling.thin natTypeBTriangle024 := by
  exact Or.inr (Or.inl ⟨rfl, rfl, rfl⟩)

/-- `013` is source-thin for the standard type-(B) cell. -/
theorem natTypeBTriangle013_source_thin :
    standardTypeBSourceScaling.thin natTypeBTriangle013 := by
  exact Or.inr
    (Or.inr (Or.inr (Or.inl ⟨rfl, rfl, rfl⟩)))

/-- `134` is source-thin for the standard type-(B) cell. -/
theorem natTypeBTriangle134_source_thin :
    standardTypeBSourceScaling.thin natTypeBTriangle134 := by
  exact Or.inr
    (Or.inr (Or.inr (Or.inr (Or.inl ⟨rfl, rfl, rfl⟩))))

/-- A triangle in `Delta[4]` is determined by its ordered three vertices. -/
theorem standardVertexTriangle_eq_triangle
    {a b c : Fin 5}
    (hab : a ≤ b) (hbc : b ≤ c)
    {t : (Δ[4] : SSet).obj (op ⦋2⦌)}
    (ht : IsStandardVertexTriangle a b c t) :
    t = SSet.stdSimplex.triangle a b c hab hbc := by
  apply SSet.stdSimplex.ext
  intro j
  fin_cases j
  · exact ht.1
  · exact ht.2.1
  · exact ht.2.2

/-! ## Yoneda face comparison -/

/-- Restricting a Duskin four-simplex to the standard triangle `abc` sends
its Duskin comparison to the corresponding comparison label of the original
four-simplex. -/
theorem natFour_triangle_face_comparison
    (sigma : DuskinSimplex NatDoubleDelooping 4)
    (a b c : Fin 5)
    (hab : a ≤ b) (hbc : b ≤ c) :
    duskinComparison
        ((duskinNerve NatDoubleDelooping).map
          (SSet.stdSimplex.objEquiv
            (SSet.stdSimplex.triangle a b c hab hbc)).op sigma) =
      sigma.mapComp (natFourEdge hab) (natFourEdge hbc) := by
  change
    (sigma.mapComp
        ((duskinReindex
          (SSet.stdSimplex.objEquiv
            (SSet.stdSimplex.triangle a b c hab hbc)).op).map edge01)
        ((duskinReindex
          (SSet.stdSimplex.objEquiv
            (SSet.stdSimplex.triangle a b c hab hbc)).op).map edge12) ≫
      sigma.map₂
        ((duskinReindex
          (SSet.stdSimplex.objEquiv
            (SSet.stdSimplex.triangle a b c hab hbc)).op).mapComp
              edge01 edge12)) = _
  rw [natDuskin_map₂_eq_zero]
  change _ + 0 = _
  rw [Nat.add_zero]
  rfl

/-- Re-express a simplicial map out of `Delta[4]` as its Yoneda four-simplex. -/
theorem natFour_map_eq_yoneda
    (F : (Δ[4] : SSet) ⟶ duskinNerve NatDoubleDelooping) :
    F = SSet.yonedaEquiv.symm (SSet.yonedaEquiv F) := by
  apply SSet.yonedaEquiv.injective
  simp

/-- The image of a named triangle under a map out of `Delta[4]` has the
comparison label obtained by evaluating the Yoneda four-simplex on those
vertices. -/
theorem natFour_map_triangle_comparison
    (F : (Δ[4] : SSet) ⟶ duskinNerve NatDoubleDelooping)
    (a b c : Fin 5)
    (hab : a ≤ b) (hbc : b ≤ c) :
    duskinComparison
        (F.app (op ⦋2⦌)
          (SSet.stdSimplex.triangle a b c hab hbc)) =
      (SSet.yonedaEquiv F).mapComp
        (natFourEdge hab) (natFourEdge hbc) := by
  rw [natFour_map_eq_yoneda F, SSet.yonedaEquiv_symm_app]
  exact natFour_triangle_face_comparison
    (SSet.yonedaEquiv F) a b c hab hbc

@[simp]
theorem natFour_map_triangle012_comparison
    (F : (Δ[4] : SSet) ⟶ duskinNerve NatDoubleDelooping) :
    duskinComparison (F.app (op ⦋2⦌) natTypeBTriangle012) =
      natFourLabel012 (SSet.yonedaEquiv F) := by
  simpa [natTypeBTriangle012, natFourLabel012] using
    natFour_map_triangle_comparison F
      (0 : Fin 5) 1 2 (by decide) (by decide)

@[simp]
theorem natFour_map_triangle024_comparison
    (F : (Δ[4] : SSet) ⟶ duskinNerve NatDoubleDelooping) :
    duskinComparison (F.app (op ⦋2⦌) natTypeBTriangle024) =
      natFourLabel024 (SSet.yonedaEquiv F) := by
  simpa [natTypeBTriangle024, natFourLabel024] using
    natFour_map_triangle_comparison F
      (0 : Fin 5) 2 4 (by decide) (by decide)

@[simp]
theorem natFour_map_triangle013_comparison
    (F : (Δ[4] : SSet) ⟶ duskinNerve NatDoubleDelooping) :
    duskinComparison (F.app (op ⦋2⦌) natTypeBTriangle013) =
      natFourLabel013 (SSet.yonedaEquiv F) := by
  simpa [natTypeBTriangle013, natFourLabel013] using
    natFour_map_triangle_comparison F
      (0 : Fin 5) 1 3 (by decide) (by decide)

@[simp]
theorem natFour_map_triangle134_comparison
    (F : (Δ[4] : SSet) ⟶ duskinNerve NatDoubleDelooping) :
    duskinComparison (F.app (op ⦋2⦌) natTypeBTriangle134) =
      natFourLabel134 (SSet.yonedaEquiv F) := by
  simpa [natTypeBTriangle134, natFourLabel134] using
    natFour_map_triangle_comparison F
      (1 : Fin 5) 3 4 (by decide) (by decide)

@[simp]
theorem natFour_map_triangle014_comparison
    (F : (Δ[4] : SSet) ⟶ duskinNerve NatDoubleDelooping) :
    duskinComparison (F.app (op ⦋2⦌) natTypeBTriangle014) =
      natFourLabel014 (SSet.yonedaEquiv F) := by
  simpa [natTypeBTriangle014, natFourLabel014] using
    natFour_map_triangle_comparison F
      (0 : Fin 5) 1 4 (by decide) (by decide)

@[simp]
theorem natFour_map_triangle034_comparison
    (F : (Δ[4] : SSet) ⟶ duskinNerve NatDoubleDelooping) :
    duskinComparison (F.app (op ⦋2⦌) natTypeBTriangle034) =
      natFourLabel034 (SSet.yonedaEquiv F) := by
  simpa [natTypeBTriangle034, natFourLabel034] using
    natFour_map_triangle_comparison F
      (0 : Fin 5) 3 4 (by decide) (by decide)

/-! ## Literal type-(B) terminal RLP -/

/-- The additive double-delooping scaled Duskin nerve has the right lifting
property against the literal standard type-(B) generator. -/
theorem natDoubleDelooping_hasLiftingProperty_standardTypeB :
    HasLiftingProperty
      standardTypeBGeneratorHom
      (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin) := by
  apply
    (ScaledSSet.hasLiftingProperty_toPoint_iff
      standardTypeBGeneratorHom).2
  intro f
  let sigma : DuskinSimplex NatDoubleDelooping 4 :=
    SSet.yonedaEquiv f.map
  have h012thin := f.scaled natTypeBTriangle012
    natTypeBTriangle012_source_thin
  have h024thin := f.scaled natTypeBTriangle024
    natTypeBTriangle024_source_thin
  have h013thin := f.scaled natTypeBTriangle013
    natTypeBTriangle013_source_thin
  have h134thin := f.scaled natTypeBTriangle134
    natTypeBTriangle134_source_thin
  have h012 : natFourLabel012 sigma = 0 := by
    have h :=
      (natDuskin_thin_iff_comparison_eq_zero
        (f.map.app (op ⦋2⦌) natTypeBTriangle012)).1 h012thin
    simpa [sigma] using h
  have h024 : natFourLabel024 sigma = 0 := by
    have h :=
      (natDuskin_thin_iff_comparison_eq_zero
        (f.map.app (op ⦋2⦌) natTypeBTriangle024)).1 h024thin
    simpa [sigma] using h
  have h013 : natFourLabel013 sigma = 0 := by
    have h :=
      (natDuskin_thin_iff_comparison_eq_zero
        (f.map.app (op ⦋2⦌) natTypeBTriangle013)).1 h013thin
    simpa [sigma] using h
  have h134 : natFourLabel134 sigma = 0 := by
    have h :=
      (natDuskin_thin_iff_comparison_eq_zero
        (f.map.app (op ⦋2⦌) natTypeBTriangle134)).1 h134thin
    simpa [sigma] using h
  have htarget :=
    natFour_typeB_target_zero_of_source_zero
      sigma h012 h024 h013 h134
  have h014thin :
      (duskinScaling NatDoubleDelooping).thin
        (f.map.app (op ⦋2⦌) natTypeBTriangle014) := by
    apply
      (natDuskin_thin_iff_comparison_eq_zero
        (f.map.app (op ⦋2⦌) natTypeBTriangle014)).2
    simpa [sigma] using htarget.1
  have h034thin :
      (duskinScaling NatDoubleDelooping).thin
        (f.map.app (op ⦋2⦌) natTypeBTriangle034) := by
    apply
      (natDuskin_thin_iff_comparison_eq_zero
        (f.map.app (op ⦋2⦌) natTypeBTriangle034)).2
    simpa [sigma] using htarget.2
  let l : standardTypeBTarget ⟶ natDoubleDeloopingScaledDuskin :=
    { map := f.map
      scaled := by
        intro t ht
        change
          standardTypeBSourceScaling.thin t ∨
            IsStandardVertexTriangle (0 : Fin 5) 1 4 t ∨
            IsStandardVertexTriangle (0 : Fin 5) 3 4 t at ht
        rcases ht with hsrc | h014 | h034
        · exact f.scaled t hsrc
        · have ht014 : t = natTypeBTriangle014 := by
            simpa [natTypeBTriangle014] using
              standardVertexTriangle_eq_triangle
                (a := (0 : Fin 5)) (b := 1) (c := 4)
                (by decide) (by decide) h014
          subst t
          exact h014thin
        · have ht034 : t = natTypeBTriangle034 := by
            simpa [natTypeBTriangle034] using
              standardVertexTriangle_eq_triangle
                (a := (0 : Fin 5)) (b := 3) (c := 4)
                (by decide) (by decide) h034
          subst t
          exact h034thin }
  refine ⟨l, ?_⟩
  apply ScaledSSet.ScaledMap.ext
  simp [standardTypeBGeneratorHom, scalingEnrichmentHom, l]

/-- Equivalently, the terminal map belongs to the right class of the type-(B)
generator property. -/
theorem natDoubleDelooping_standardTypeB_rlp :
    (standardTypeBScaledAnodyneGenerators : MorphismProperty ScaledSSet).rlp
      (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin) := by
  rw [MorphismProperty.rlp_ofHoms_iff_hasLiftingProperty Unit]
  exact natDoubleDelooping_hasLiftingProperty_standardTypeB

/-!
The standard type-(B) obligation for the concrete separator is now closed.
The remaining standard-right theorem has only the type-(A) inner scaled horn
family and the type-(C) collapsed outer horn family left to prove.
-/

end KUOS.DependentOriginationDoubleDeloopingTypeBTerminalRLPV1_98
