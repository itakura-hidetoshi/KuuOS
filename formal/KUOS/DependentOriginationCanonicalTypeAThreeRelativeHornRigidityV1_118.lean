import KUOS.DependentOriginationCanonicalTypeAHigherTopSimplexCoverageObstructionV1_117
import KUOS.DependentOriginationPresentationIndependentSeparationTypeBReverseV1_107

namespace KUOS.DependentOriginationCanonicalTypeAThreeRelativeHornRigidityV1_118

open CategoryTheory
open CategoryTheory.Category
open Opposite
open Simplicial
open MonoidalCategory
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledHornAttachmentLiftingV1_40
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58
open KUOS.DependentOriginationCanonicalTypeAHigherLowerCylinderRetractObstructionV1_112
open KUOS.DependentOriginationCanonicalTypeAHigherTopSimplexCoverageObstructionV1_117
open KUOS.DependentOriginationPresentationIndependentSeparationTypeBReverseV1_107

universe u

noncomputable section

set_option backward.isDefEq.respectTransparency false

/-!
# Degree-three type-(A) relative horn rigidity v1.118

The degree-three type-(A) horn `Λ[3,1] ⟶ Δ[3]` is used as a right-class
separator for the canonical attachment presentation.  The missing face is
`023`.  Relative prism rigidity shows that a canonical attachment square into
this horn cannot create that missing face, hence every canonical attachment
generator lifts against the horn inclusion.  The inclusion does not lift
against itself.  Consequently the standard generated left class is not
contained in the canonical generated left class.
-/

/-! ## The decisive degree-three type-(A) generator -/

/-- The first higher standard type-(A) generator, `n = 3, i = 1`. -/
def typeAThreeOneIndex : StandardTypeAHornGeneratorIndex where
  n := 3
  i := 1
  inner_left := by decide
  inner_right := by decide

set_option allowUnsafeReducibility true in
attribute [local reducible]
  ScaledSSet.of scaledSimplex standardTypeAScaledSimplex typeAThreeOneIndex

/-- The unique missing codimension-one face of `Λ[3,1]`: `023`. -/
def typeAThreeOneMissingTriangle :
    (Δ[3] : SSet.{u}) _⦋2⦌ :=
  SSet.stdSimplex.triangle
    (0 : Fin 4) (2 : Fin 4) (3 : Fin 4) (by decide) (by decide)

/-- The missing triangle is nondegenerate. -/
theorem typeAThreeOneMissingTriangle_nondegenerate :
    typeAThreeOneMissingTriangle ∈
      (Δ[3] : SSet.{u}).nonDegenerate 2 := by
  rw [SSet.stdSimplex.mem_nonDegenerate_iff_strictMono,
    Fin.strictMono_iff_lt_succ]
  intro k
  fin_cases k <;> decide

/-- `023` is not the distinguished type-(A) triangle `012`. -/
theorem typeAThreeOneMissingTriangle_not_distinguished :
    ¬ IsStandardTypeADistinguishedTriangle
        (1 : Fin 4) typeAThreeOneMissingTriangle := by
  intro h
  have hmid := congrArg Fin.val h.1
  change 2 = 1 at hmid
  omega

/-- Therefore `023` is not thin in the sparse degree-three type-(A) scaling. -/
theorem typeAThreeOneMissingTriangle_not_thin :
    ¬ (standardTypeASimplexScaling (1 : Fin 4)).thin
        typeAThreeOneMissingTriangle :=
  standardTypeA_not_thin_of_nondegenerate_of_not_distinguished
    (1 : Fin 4)
    typeAThreeOneMissingTriangle
    typeAThreeOneMissingTriangle_nondegenerate
    typeAThreeOneMissingTriangle_not_distinguished

/-- The triangle `023` is absent from `Λ[3,1]`. -/
theorem typeAThreeOneMissingTriangle_not_mem_horn :
    typeAThreeOneMissingTriangle ∉
      (SSet.horn 3 (1 : Fin 4)).obj (op ⦋2⦌) := by
  intro hmem
  rcases
      (SSet.mem_horn_iff_notMem_range
        typeAThreeOneMissingTriangle (1 : Fin 4)).1 hmem with
    ⟨missing, hmissing_ne, hmissing⟩
  fin_cases missing
  · exact hmissing ⟨0, rfl⟩
  · exact hmissing_ne rfl
  · exact hmissing ⟨1, rfl⟩
  · exact hmissing ⟨2, rfl⟩

/-! ## Thin-triangle rigidity in the sparse target -/

/-- A thin type-(A) triangle ending in `2,3` repeats its first two vertices. -/
theorem typeAThreeOne_thin_eq_left_of_middle_two_right_three
    (y : (Δ[3] : SSet.{u}) _⦋2⦌)
    (hy : (standardTypeASimplexScaling (1 : Fin 4)).thin y)
    (h1 : y 1 = (2 : Fin 4))
    (h2 : y 2 = (3 : Fin 4)) :
    y 0 = y 1 := by
  by_contra h01
  have hnd : y ∈ (Δ[3] : SSet.{u}).nonDegenerate 2 := by
    rw [SSet.stdSimplex.mem_nonDegenerate_iff_strictMono,
      Fin.strictMono_iff_lt_succ]
    intro k
    fin_cases k
    · have hle :=
        SSet.stdSimplex.monotone_apply y
          (show (0 : Fin 3) ≤ 1 by decide)
      exact lt_of_le_of_ne hle h01
    · set_option backward.isDefEq.respectTransparency false in
        change y 1 < y 2
      rw [h1, h2]
      decide
  have hnot : ¬ IsStandardTypeADistinguishedTriangle (1 : Fin 4) y := by
    intro hdist
    have h21 : (2 : Fin 4) = 1 := by
      calc
        (2 : Fin 4) = y 1 := h1.symm
        _ = 1 := hdist.1
    exact (by decide : (2 : Fin 4) ≠ 1) h21
  exact
    (standardTypeA_not_thin_of_nondegenerate_of_not_distinguished
      (1 : Fin 4) y hnd hnot) hy

/-- Dually, a thin triangle beginning with `0,2` repeats its last two vertices. -/
theorem typeAThreeOne_thin_eq_right_of_left_zero_middle_two
    (y : (Δ[3] : SSet.{u}) _⦋2⦌)
    (hy : (standardTypeASimplexScaling (1 : Fin 4)).thin y)
    (h0 : y 0 = (0 : Fin 4))
    (h1 : y 1 = (2 : Fin 4)) :
    y 1 = y 2 := by
  by_contra h12
  have hnd : y ∈ (Δ[3] : SSet.{u}).nonDegenerate 2 := by
    rw [SSet.stdSimplex.mem_nonDegenerate_iff_strictMono,
      Fin.strictMono_iff_lt_succ]
    intro k
    fin_cases k
    · set_option backward.isDefEq.respectTransparency false in
        change y 0 < y 1
      rw [h0, h1]
      decide
    · have hle :=
        SSet.stdSimplex.monotone_apply y
          (show (1 : Fin 3) ≤ 2 by decide)
      exact lt_of_le_of_ne hle h12
  have hnot : ¬ IsStandardTypeADistinguishedTriangle (1 : Fin 4) y := by
    intro hdist
    have h21 : (2 : Fin 4) = 1 := by
      calc
        (2 : Fin 4) = y 1 := h1.symm
        _ = 1 := hdist.1
    exact (by decide : (2 : Fin 4) ≠ 1) h21
  exact
    (standardTypeA_not_thin_of_nondegenerate_of_not_distinguished
      (1 : Fin 4) y hnd hnot) hy

/-- A thin triangle with endpoints `0` and `3` repeats at one end. -/
theorem typeAThreeOne_thin_middle_eq_endpoint_of_left_zero_right_three
    (y : (Δ[3] : SSet.{u}) _⦋2⦌)
    (hy : (standardTypeASimplexScaling (1 : Fin 4)).thin y)
    (_h0 : y 0 = (0 : Fin 4))
    (h2 : y 2 = (3 : Fin 4)) :
    y 0 = y 1 ∨ y 1 = y 2 := by
  by_contra h
  push Not at h
  have hnd : y ∈ (Δ[3] : SSet.{u}).nonDegenerate 2 := by
    rw [SSet.stdSimplex.mem_nonDegenerate_iff_strictMono,
      Fin.strictMono_iff_lt_succ]
    intro k
    fin_cases k
    · have hle :=
        SSet.stdSimplex.monotone_apply y
          (show (0 : Fin 3) ≤ 1 by decide)
      exact lt_of_le_of_ne hle h.1
    · have hle :=
        SSet.stdSimplex.monotone_apply y
          (show (1 : Fin 3) ≤ 2 by decide)
      exact lt_of_le_of_ne hle h.2
  have hnot : ¬ IsStandardTypeADistinguishedTriangle (1 : Fin 4) y := by
    intro hdist
    have hright := hdist.2.2
    rw [h2] at hright
    change 1 + 1 = 3 at hright
    omega
  exact
    (standardTypeA_not_thin_of_nondegenerate_of_not_distinguished
      (1 : Fin 4) y hnd hnot) hy

/-! ## Vertex evaluation of an arbitrary scaled prism -/

/-- A vertex of `Δ[n] × Δ[1]`. -/
def typeAThreePrismVertex
    (n : Nat) (a : Fin (n + 1)) (e : Fin 2) :
    ((Δ[n] : SSet.{u}) ⊗ Δ[1]) _⦋0⦌ :=
  ⟨SSet.stdSimplex.obj₀Equiv.symm a,
    SSet.stdSimplex.obj₀Equiv.symm e⟩

/-- The vertex value of a prism map into `Δ[3]`. -/
def typeAThreePrismVertexValue
    {n : Nat}
    {sΔ : ScaledSimplicialSet (Δ[n] : SSet.{u})}
    (r : scaledSimplexCylinder sΔ ⟶
      standardTypeAScaledSimplex typeAThreeOneIndex)
    (a : Fin (n + 1)) (e : Fin 2) : Fin 4 :=
  SSet.stdSimplex.obj₀Equiv
    (r.map.app (op ⦋0⦌) (typeAThreePrismVertex n a e))

/-- Simplicial naturality evaluates a prism map through its vertex values. -/
@[simp]
theorem typeAThreePrismMap_apply_eq_vertexValue
    {n : Nat}
    {sΔ : ScaledSimplicialSet (Δ[n] : SSet.{u})}
    (r : scaledSimplexCylinder sΔ ⟶
      standardTypeAScaledSimplex typeAThreeOneIndex)
    {d : Nat}
    (z : ((Δ[n] : SSet.{u}) ⊗ Δ[1]) _⦋d⦌)
    (k : Fin (d + 1)) :
    ((r.map.app (op ⦋d⦌) z : (Δ[3] : SSet.{u}) _⦋d⦌)) k =
      typeAThreePrismVertexValue r (z.1 k) (z.2 k) := by
  let v : (Δ[d] : SSet.{u}) _⦋0⦌ :=
    SSet.stdSimplex.obj₀Equiv.symm k
  let alpha : ⦋0⦌ ⟶ ⦋d⦌ := SSet.stdSimplex.objEquiv v
  have hnat :
      r.map.app (op ⦋0⦌)
          (((Δ[n] : SSet.{u}) ⊗ Δ[1]).map alpha.op z) =
        (Δ[3] : SSet.{u}).map alpha.op
          (r.map.app (op ⦋d⦌) z) := by
    exact ConcreteCategory.congr_hom (r.map.naturality alpha.op) z
  have hpoint := congrArg (fun q => SSet.stdSimplex.obj₀Equiv q) hnat
  set_option backward.isDefEq.respectTransparency false in
    change
      typeAThreePrismVertexValue r (z.1 k) (z.2 k) =
        ((r.map.app (op ⦋d⦌) z : (Δ[3] : SSet.{u}) _⦋d⦌)) k at hpoint
  exact hpoint.symm

/-- Vertex values are monotone in both prism coordinates. -/
theorem typeAThreePrismVertexValue_mono
    {n : Nat}
    {sΔ : ScaledSimplicialSet (Δ[n] : SSet.{u})}
    (r : scaledSimplexCylinder sΔ ⟶
      standardTypeAScaledSimplex typeAThreeOneIndex)
    {a b : Fin (n + 1)} {e f : Fin 2}
    (hab : a ≤ b) (hef : e ≤ f) :
    typeAThreePrismVertexValue r a e ≤
      typeAThreePrismVertexValue r b f := by
  let z : ((Δ[n] : SSet.{u}) ⊗ Δ[1]) _⦋1⦌ :=
    ⟨SSet.stdSimplex.edge n a b hab,
      SSet.stdSimplex.edge 1 e f hef⟩
  have hmono :
      ((r.map.app (op ⦋1⦌) z : (Δ[3] : SSet.{u}) _⦋1⦌) 0) ≤
        ((r.map.app (op ⦋1⦌) z : (Δ[3] : SSet.{u}) _⦋1⦌) 1) :=
    SSet.stdSimplex.monotone_apply
      (r.map.app (op ⦋1⦌) z)
      (show (0 : Fin 2) ≤ 1 by decide)
  rw [typeAThreePrismMap_apply_eq_vertexValue r z 0,
    typeAThreePrismMap_apply_eq_vertexValue r z 1] at hmono
  set_option backward.isDefEq.respectTransparency false in
    change
      typeAThreePrismVertexValue r a e ≤
        typeAThreePrismVertexValue r b f at hmono
  exact hmono

/-! ## Reusable prism triangles -/

/-- The prism triangle determined by two monotone triples. -/
def typeAThreePrismTriangle
    {n : Nat}
    (a b c : Fin (n + 1))
    (e f h : Fin 2)
    (hab : a ≤ b) (hbc : b ≤ c)
    (hef : e ≤ f) (hfh : f ≤ h) :
    ((Δ[n] : SSet.{u}) ⊗ Δ[1]) _⦋2⦌ :=
  ⟨SSet.stdSimplex.triangle a b c hab hbc,
    SSet.stdSimplex.triangle e f h hef hfh⟩

/-- Fix the interval coordinate of a prism triangle to one endpoint. -/
def typeAThreeEndpointTriangle
    {n : Nat}
    (e : Fin 2)
    (t : ((Δ[n] : SSet.{u}) ⊗ Δ[1]) _⦋2⦌) :
    ((Δ[n] : SSet.{u}) ⊗ Δ[1]) _⦋2⦌ :=
  ⟨t.1,
    SSet.stdSimplex.triangle e e e (le_refl e) (le_refl e)⟩

@[simp]
theorem typeAThreeEndpointTriangle_zero
    {n : Nat}
    (t : ((Δ[n] : SSet.{u}) ⊗ Δ[1]) _⦋2⦌) :
    typeAThreeEndpointTriangle (0 : Fin 2) t =
      (SSet.ι₀ : (Δ[n] : SSet.{u}) ⟶
        (Δ[n] : SSet.{u}) ⊗ Δ[1]).app (op ⦋2⦌) t.1 := by
  apply Prod.ext
  · simp [typeAThreeEndpointTriangle]
  · apply SSet.stdSimplex.ext
    intro k
    fin_cases k <;> rfl

@[simp]
theorem typeAThreeEndpointTriangle_one
    {n : Nat}
    (t : ((Δ[n] : SSet.{u}) ⊗ Δ[1]) _⦋2⦌) :
    typeAThreeEndpointTriangle (1 : Fin 2) t =
      (SSet.ι₁ : (Δ[n] : SSet.{u}) ⟶
        (Δ[n] : SSet.{u}) ⊗ Δ[1]).app (op ⦋2⦌) t.1 := by
  apply Prod.ext
  · simp [typeAThreeEndpointTriangle]
  · apply SSet.stdSimplex.ext
    intro k
    fin_cases k <;> rfl

/-! ## Endpoint propagation of the missing triangle -/

/-- If a scaled prism sends a triangle to `023`, either fixed interval endpoint
with the same first-coordinate triangle is also sent to `023`. -/
theorem typeAThreeOne_missingTriangle_endpoint_propagation
    {n : Nat}
    {sΔ : ScaledSimplicialSet (Δ[n] : SSet.{u})}
    (r : scaledSimplexCylinder sΔ ⟶
      standardTypeAScaledSimplex typeAThreeOneIndex)
    (e : Fin 2)
    (t : ((Δ[n] : SSet.{u}) ⊗ Δ[1]) _⦋2⦌)
    (himage :
      r.map.app (op ⦋2⦌) t = typeAThreeOneMissingTriangle) :
    r.map.app (op ⦋2⦌) (typeAThreeEndpointTriangle e t) =
      typeAThreeOneMissingTriangle := by
  have hx01 : t.1 0 ≤ t.1 1 :=
    SSet.stdSimplex.monotone_apply t.1 (by decide)
  have hx12 : t.1 1 ≤ t.1 2 :=
    SSet.stdSimplex.monotone_apply t.1 (by decide)
  have hx02 : t.1 0 ≤ t.1 2 := hx01.trans hx12
  have hq01 : t.2 0 ≤ t.2 1 :=
    SSet.stdSimplex.monotone_apply t.2 (by decide)
  have hq12 : t.2 1 ≤ t.2 2 :=
    SSet.stdSimplex.monotone_apply t.2 (by decide)
  have hv0 :
      typeAThreePrismVertexValue r (t.1 0) (t.2 0) = (0 : Fin 4) := by
    rw [← typeAThreePrismMap_apply_eq_vertexValue r t 0, himage]
    rfl
  have hv1 :
      typeAThreePrismVertexValue r (t.1 1) (t.2 1) = (2 : Fin 4) := by
    rw [← typeAThreePrismMap_apply_eq_vertexValue r t 1, himage]
    rfl
  have hv2 :
      typeAThreePrismVertexValue r (t.1 2) (t.2 2) = (3 : Fin 4) := by
    rw [← typeAThreePrismMap_apply_eq_vertexValue r t 2, himage]
    rfl
  fin_cases e
  · have he0 :
        typeAThreePrismVertexValue r (t.1 0) (0 : Fin 2) =
          (0 : Fin 4) := by
      apply le_antisymm
      · calc
          typeAThreePrismVertexValue r (t.1 0) (0 : Fin 2) ≤
              typeAThreePrismVertexValue r (t.1 0) (t.2 0) :=
            typeAThreePrismVertexValue_mono r le_rfl (Fin.zero_le _)
          _ = 0 := hv0
      · exact Fin.zero_le _
    have he1 :
        typeAThreePrismVertexValue r (t.1 1) (0 : Fin 2) =
          (2 : Fin 4) := by
      by_cases hq1zero : t.2 1 = (0 : Fin 2)
      · simpa [hq1zero] using hv1
      · have hq1 : t.2 1 = (1 : Fin 2) :=
          Fin.eq_one_of_ne_zero _ hq1zero
        have hq2 : t.2 2 = (1 : Fin 2) := by
          apply le_antisymm
          · exact Fin.le_last _
          · have hh := hq12
            rw [hq1] at hh
            exact hh
        let v : ((Δ[n] : SSet.{u}) ⊗ Δ[1]) _⦋2⦌ :=
          typeAThreePrismTriangle
            (t.1 1) (t.1 1) (t.1 2)
            (0 : Fin 2) 1 1
            le_rfl hx12 (by decide) le_rfl
        have hthin : (simplexCylinderScaling sΔ).thin v := by
          change sΔ.thin v.1
          apply arbitraryScaling_thin_of_zero_eq_one sΔ
          rfl
        have hy := r.scaled v hthin
        have hy1 : (r.map.app (op ⦋2⦌) v) 1 = (2 : Fin 4) := by
          rw [typeAThreePrismMap_apply_eq_vertexValue]
          set_option backward.isDefEq.respectTransparency false in
            change
              typeAThreePrismVertexValue r (t.1 1) (1 : Fin 2) =
                (2 : Fin 4)
          simpa [hq1] using hv1
        have hy2 : (r.map.app (op ⦋2⦌) v) 2 = (3 : Fin 4) := by
          rw [typeAThreePrismMap_apply_eq_vertexValue]
          set_option backward.isDefEq.respectTransparency false in
            change
              typeAThreePrismVertexValue r (t.1 2) (1 : Fin 2) =
                (3 : Fin 4)
          simpa [hq2] using hv2
        have hEq :=
          typeAThreeOne_thin_eq_left_of_middle_two_right_three
            (r.map.app (op ⦋2⦌) v) hy hy1 hy2
        rw [typeAThreePrismMap_apply_eq_vertexValue,
          typeAThreePrismMap_apply_eq_vertexValue] at hEq
        set_option backward.isDefEq.respectTransparency false in
          change
            typeAThreePrismVertexValue r (t.1 1) (0 : Fin 2) =
              typeAThreePrismVertexValue r (t.1 1) (1 : Fin 2) at hEq
        have hv1' :
            typeAThreePrismVertexValue r (t.1 1) (1 : Fin 2) =
              (2 : Fin 4) := by
          simpa [hq1] using hv1
        exact hEq.trans hv1'
    have he2 :
        typeAThreePrismVertexValue r (t.1 2) (0 : Fin 2) =
          (3 : Fin 4) := by
      by_cases hq2zero : t.2 2 = (0 : Fin 2)
      · simpa [hq2zero] using hv2
      · have hq2 : t.2 2 = (1 : Fin 2) :=
          Fin.eq_one_of_ne_zero _ hq2zero
        let v : ((Δ[n] : SSet.{u}) ⊗ Δ[1]) _⦋2⦌ :=
          typeAThreePrismTriangle
            (t.1 0) (t.1 2) (t.1 2)
            (0 : Fin 2) 0 1
            hx02 le_rfl le_rfl (by decide)
        have hthin : (simplexCylinderScaling sΔ).thin v := by
          change sΔ.thin v.1
          apply arbitraryScaling_thin_of_one_eq_two sΔ
          rfl
        have hy := r.scaled v hthin
        have hy0 : (r.map.app (op ⦋2⦌) v) 0 = (0 : Fin 4) := by
          rw [typeAThreePrismMap_apply_eq_vertexValue]
          set_option backward.isDefEq.respectTransparency false in
            change
              typeAThreePrismVertexValue r (t.1 0) (0 : Fin 2) =
                (0 : Fin 4)
          exact he0
        have hy2 : (r.map.app (op ⦋2⦌) v) 2 = (3 : Fin 4) := by
          rw [typeAThreePrismMap_apply_eq_vertexValue]
          set_option backward.isDefEq.respectTransparency false in
            change
              typeAThreePrismVertexValue r (t.1 2) (1 : Fin 2) =
                (3 : Fin 4)
          simpa [hq2] using hv2
        have hrep :=
          typeAThreeOne_thin_middle_eq_endpoint_of_left_zero_right_three
            (r.map.app (op ⦋2⦌) v) hy hy0 hy2
        rcases hrep with hleft | hright
        · rw [typeAThreePrismMap_apply_eq_vertexValue,
            typeAThreePrismMap_apply_eq_vertexValue] at hleft
          set_option backward.isDefEq.respectTransparency false in
            change
              typeAThreePrismVertexValue r (t.1 0) (0 : Fin 2) =
                typeAThreePrismVertexValue r (t.1 2) (0 : Fin 2) at hleft
          have hz :
              typeAThreePrismVertexValue r (t.1 2) (0 : Fin 2) =
                (0 : Fin 4) := by
            exact hleft.symm.trans he0
          have hle := typeAThreePrismVertexValue_mono
            (e := (0 : Fin 2)) (f := (0 : Fin 2)) r hx12 le_rfl
          rw [he1, hz] at hle
          omega
        · rw [typeAThreePrismMap_apply_eq_vertexValue,
            typeAThreePrismMap_apply_eq_vertexValue] at hright
          set_option backward.isDefEq.respectTransparency false in
            change
              typeAThreePrismVertexValue r (t.1 2) (0 : Fin 2) =
                typeAThreePrismVertexValue r (t.1 2) (1 : Fin 2) at hright
          have hv2' :
              typeAThreePrismVertexValue r (t.1 2) (1 : Fin 2) =
                (3 : Fin 4) := by
            simpa [hq2] using hv2
          exact hright.trans hv2'
    apply SSet.stdSimplex.ext
    intro k
    fin_cases k
    · rw [typeAThreePrismMap_apply_eq_vertexValue]
      set_option backward.isDefEq.respectTransparency false in
        change typeAThreePrismVertexValue r (t.1 0) 0 = (0 : Fin 4)
      exact he0
    · rw [typeAThreePrismMap_apply_eq_vertexValue]
      set_option backward.isDefEq.respectTransparency false in
        change typeAThreePrismVertexValue r (t.1 1) 0 = (2 : Fin 4)
      exact he1
    · rw [typeAThreePrismMap_apply_eq_vertexValue]
      set_option backward.isDefEq.respectTransparency false in
        change typeAThreePrismVertexValue r (t.1 2) 0 = (3 : Fin 4)
      exact he2
  · have he2 :
        typeAThreePrismVertexValue r (t.1 2) (1 : Fin 2) =
          (3 : Fin 4) := by
      apply le_antisymm
      · exact Fin.le_last _
      · calc
          (3 : Fin 4) =
              typeAThreePrismVertexValue r (t.1 2) (t.2 2) := hv2.symm
          _ ≤ typeAThreePrismVertexValue r (t.1 2) (1 : Fin 2) :=
            typeAThreePrismVertexValue_mono r le_rfl (Fin.le_last _)
    have he1 :
        typeAThreePrismVertexValue r (t.1 1) (1 : Fin 2) =
          (2 : Fin 4) := by
      by_cases hq1zero : t.2 1 = (0 : Fin 2)
      · have hq1 : t.2 1 = (0 : Fin 2) := hq1zero
        have hq0 : t.2 0 = (0 : Fin 2) := by
          apply le_antisymm
          · have hh := hq01
            rw [hq1] at hh
            exact hh
          · exact Fin.zero_le _
        let v : ((Δ[n] : SSet.{u}) ⊗ Δ[1]) _⦋2⦌ :=
          typeAThreePrismTriangle
            (t.1 0) (t.1 1) (t.1 1)
            (0 : Fin 2) 0 1
            hx01 le_rfl le_rfl (by decide)
        have hthin : (simplexCylinderScaling sΔ).thin v := by
          change sΔ.thin v.1
          apply arbitraryScaling_thin_of_one_eq_two sΔ
          rfl
        have hy := r.scaled v hthin
        have hy0 : (r.map.app (op ⦋2⦌) v) 0 = (0 : Fin 4) := by
          rw [typeAThreePrismMap_apply_eq_vertexValue]
          set_option backward.isDefEq.respectTransparency false in
            change
              typeAThreePrismVertexValue r (t.1 0) (0 : Fin 2) =
                (0 : Fin 4)
          simpa [hq0] using hv0
        have hy1 : (r.map.app (op ⦋2⦌) v) 1 = (2 : Fin 4) := by
          rw [typeAThreePrismMap_apply_eq_vertexValue]
          set_option backward.isDefEq.respectTransparency false in
            change
              typeAThreePrismVertexValue r (t.1 1) (0 : Fin 2) =
                (2 : Fin 4)
          simpa [hq1] using hv1
        have hEq :=
          typeAThreeOne_thin_eq_right_of_left_zero_middle_two
            (r.map.app (op ⦋2⦌) v) hy hy0 hy1
        rw [typeAThreePrismMap_apply_eq_vertexValue,
          typeAThreePrismMap_apply_eq_vertexValue] at hEq
        set_option backward.isDefEq.respectTransparency false in
          change
            typeAThreePrismVertexValue r (t.1 1) (0 : Fin 2) =
              typeAThreePrismVertexValue r (t.1 1) (1 : Fin 2) at hEq
        have hv1' :
            typeAThreePrismVertexValue r (t.1 1) (0 : Fin 2) =
              (2 : Fin 4) := by
          simpa [hq1] using hv1
        exact hEq.symm.trans hv1'
      · have hq1 : t.2 1 = (1 : Fin 2) :=
          Fin.eq_one_of_ne_zero _ hq1zero
        simpa [hq1] using hv1
    have he0 :
        typeAThreePrismVertexValue r (t.1 0) (1 : Fin 2) =
          (0 : Fin 4) := by
      by_cases hq0zero : t.2 0 = (0 : Fin 2)
      · have hq0 : t.2 0 = (0 : Fin 2) := hq0zero
        let v : ((Δ[n] : SSet.{u}) ⊗ Δ[1]) _⦋2⦌ :=
          typeAThreePrismTriangle
            (t.1 0) (t.1 0) (t.1 2)
            (0 : Fin 2) 1 1
            le_rfl hx02 (by decide) le_rfl
        have hthin : (simplexCylinderScaling sΔ).thin v := by
          change sΔ.thin v.1
          apply arbitraryScaling_thin_of_zero_eq_one sΔ
          rfl
        have hy := r.scaled v hthin
        have hy0 : (r.map.app (op ⦋2⦌) v) 0 = (0 : Fin 4) := by
          rw [typeAThreePrismMap_apply_eq_vertexValue]
          set_option backward.isDefEq.respectTransparency false in
            change
              typeAThreePrismVertexValue r (t.1 0) (0 : Fin 2) =
                (0 : Fin 4)
          simpa [hq0] using hv0
        have hy2 : (r.map.app (op ⦋2⦌) v) 2 = (3 : Fin 4) := by
          rw [typeAThreePrismMap_apply_eq_vertexValue]
          set_option backward.isDefEq.respectTransparency false in
            change
              typeAThreePrismVertexValue r (t.1 2) (1 : Fin 2) =
                (3 : Fin 4)
          exact he2
        have hrep :=
          typeAThreeOne_thin_middle_eq_endpoint_of_left_zero_right_three
            (r.map.app (op ⦋2⦌) v) hy hy0 hy2
        rcases hrep with hleft | hright
        · rw [typeAThreePrismMap_apply_eq_vertexValue,
            typeAThreePrismMap_apply_eq_vertexValue] at hleft
          set_option backward.isDefEq.respectTransparency false in
            change
              typeAThreePrismVertexValue r (t.1 0) (0 : Fin 2) =
                typeAThreePrismVertexValue r (t.1 0) (1 : Fin 2) at hleft
          have hv0' :
              typeAThreePrismVertexValue r (t.1 0) (0 : Fin 2) =
                (0 : Fin 4) := by
            simpa [hq0] using hv0
          exact hleft.symm.trans hv0'
        · rw [typeAThreePrismMap_apply_eq_vertexValue,
            typeAThreePrismMap_apply_eq_vertexValue] at hright
          set_option backward.isDefEq.respectTransparency false in
            change
              typeAThreePrismVertexValue r (t.1 0) (1 : Fin 2) =
                typeAThreePrismVertexValue r (t.1 2) (1 : Fin 2) at hright
          have hle := typeAThreePrismVertexValue_mono
            (e := (1 : Fin 2)) (f := (1 : Fin 2)) r hx01 le_rfl
          rw [hright, he1, he2] at hle
          omega
      · have hq0 : t.2 0 = (1 : Fin 2) :=
          Fin.eq_one_of_ne_zero _ hq0zero
        simpa [hq0] using hv0
    apply SSet.stdSimplex.ext
    intro k
    fin_cases k
    · rw [typeAThreePrismMap_apply_eq_vertexValue]
      set_option backward.isDefEq.respectTransparency false in
        change typeAThreePrismVertexValue r (t.1 0) 1 = (0 : Fin 4)
      exact he0
    · rw [typeAThreePrismMap_apply_eq_vertexValue]
      set_option backward.isDefEq.respectTransparency false in
        change typeAThreePrismVertexValue r (t.1 1) 1 = (2 : Fin 4)
      exact he1
    · rw [typeAThreePrismMap_apply_eq_vertexValue]
      set_option backward.isDefEq.respectTransparency false in
        change typeAThreePrismVertexValue r (t.1 2) 1 = (3 : Fin 4)
      exact he2

/-! ## Endpoint source of a canonical lifting square lands in the horn -/

/-- In a canonical attachment square, every fixed-endpoint triangle maps into
`Λ[3,1]`. -/
theorem typeAThreeOne_square_endpointTriangle_mem_horn
    (c : ScaledHornAttachmentGeneratorIndex.{u})
    {f : minimallyScaledHornCylinderAttachment c.n c.i c.endpoint ⟶
      standardTypeAScaledHorn typeAThreeOneIndex}
    {g : scaledSimplexCylinder c.simplexScaling ⟶
      standardTypeAScaledSimplex typeAThreeOneIndex}
    (sq : CommSq f (scaledHornAttachmentGeneratorHom c)
      (standardTypeAScaledHornGeneratorHom typeAThreeOneIndex) g)
    (x : (Δ[c.n] : SSet.{u}) _⦋2⦌) :
    g.map.app (op ⦋2⦌)
        (typeAThreeEndpointTriangle c.endpoint
          ⟨x,
            SSet.stdSimplex.triangle c.endpoint c.endpoint c.endpoint
              (le_refl _) (le_refl _)⟩) ∈
      (SSet.horn 3 (1 : Fin 4)).obj (op ⦋2⦌) := by
  rcases c with ⟨n, i, endpoint, sΔ⟩
  let c : ScaledHornAttachmentGeneratorIndex.{u} :=
    ⟨n, i, endpoint, sΔ⟩
  have hsqmap := congrArg ScaledSSet.ScaledMap.map sq.w
  fin_cases endpoint
  · let a :=
      (endpointIntoAttachment c.n c.i 0).app (op ⦋2⦌) x
    have hp :=
      ConcreteCategory.congr_hom (congr_app hsqmap (op ⦋2⦌)) a
    have hcyl :
        (scaledHornAttachmentGeneratorHom c).map.app (op ⦋2⦌) a =
          (SSet.ι₀ : (Δ[c.n] : SSet.{u}) ⟶
            (Δ[c.n] : SSet.{u}) ⊗ Δ[1]).app (op ⦋2⦌) x := by
      have h := ConcreteCategory.congr_hom
        (congr_app (endpointIntoAttachment_ι_zero c.n c.i) (op ⦋2⦌)) x
      simpa [a, c, scaledHornAttachmentGeneratorHom,
        scaledHornCylinderAttachmentInclusion] using h
    change
      (f.map.app (op ⦋2⦌) a).val =
        g.map.app (op ⦋2⦌)
          ((scaledHornAttachmentGeneratorHom c).map.app (op ⦋2⦌) a) at hp
    rw [hcyl] at hp
    have hmem := (f.map.app (op ⦋2⦌) a).property
    change
      g.map.app (op ⦋2⦌)
          ((SSet.ι₀ : (Δ[c.n] : SSet.{u}) ⟶
            (Δ[c.n] : SSet.{u}) ⊗ Δ[1]).app (op ⦋2⦌) x) ∈
        (SSet.horn 3 (1 : Fin 4)).obj (op ⦋2⦌)
    rw [← hp]
    exact hmem
  · let a :=
      (endpointIntoAttachment c.n c.i 1).app (op ⦋2⦌) x
    have hp :=
      ConcreteCategory.congr_hom (congr_app hsqmap (op ⦋2⦌)) a
    have hcyl :
        (scaledHornAttachmentGeneratorHom c).map.app (op ⦋2⦌) a =
          (SSet.ι₁ : (Δ[c.n] : SSet.{u}) ⟶
            (Δ[c.n] : SSet.{u}) ⊗ Δ[1]).app (op ⦋2⦌) x := by
      have h := ConcreteCategory.congr_hom
        (congr_app (endpointIntoAttachment_ι_one c.n c.i) (op ⦋2⦌)) x
      simpa [a, c, scaledHornAttachmentGeneratorHom,
        scaledHornCylinderAttachmentInclusion] using h
    change
      (f.map.app (op ⦋2⦌) a).val =
        g.map.app (op ⦋2⦌)
          ((scaledHornAttachmentGeneratorHom c).map.app (op ⦋2⦌) a) at hp
    rw [hcyl] at hp
    have hmem := (f.map.app (op ⦋2⦌) a).property
    change
      g.map.app (op ⦋2⦌)
          ((SSet.ι₁ : (Δ[c.n] : SSet.{u}) ⟶
            (Δ[c.n] : SSet.{u}) ⊗ Δ[1]).app (op ⦋2⦌) x) ∈
        (SSet.horn 3 (1 : Fin 4)).obj (op ⦋2⦌)
    rw [← hp]
    exact hmem

/-! ## A canonical square can never create the missing face -/

/-- The bottom prism in a canonical attachment square never maps a triangle to
`023`. -/
theorem typeAThreeOne_square_missingTriangle_not_image
    (c : ScaledHornAttachmentGeneratorIndex.{u})
    {f : minimallyScaledHornCylinderAttachment c.n c.i c.endpoint ⟶
      standardTypeAScaledHorn typeAThreeOneIndex}
    {g : scaledSimplexCylinder c.simplexScaling ⟶
      standardTypeAScaledSimplex typeAThreeOneIndex}
    (sq : CommSq f (scaledHornAttachmentGeneratorHom c)
      (standardTypeAScaledHornGeneratorHom typeAThreeOneIndex) g)
    (t : ((Δ[c.n] : SSet.{u}) ⊗ Δ[1]) _⦋2⦌) :
    g.map.app (op ⦋2⦌) t ≠ typeAThreeOneMissingTriangle := by
  intro himage
  have hend :=
    typeAThreeOne_missingTriangle_endpoint_propagation
      g c.endpoint t himage
  have hmem :=
    typeAThreeOne_square_endpointTriangle_mem_horn c sq t.1
  have hendpoint :
      typeAThreeEndpointTriangle c.endpoint
          ⟨t.1,
            SSet.stdSimplex.triangle c.endpoint c.endpoint c.endpoint
              (le_refl _) (le_refl _)⟩ =
        typeAThreeEndpointTriangle c.endpoint t := by
    rfl
  rw [hendpoint, hend] at hmem
  exact typeAThreeOneMissingTriangle_not_mem_horn hmem

/-! ## Factor every canonical square through the horn -/

/-- A simplex of `Δ[3]` outside `Λ[3,1]` has a 2-face equal to `023`. -/
theorem typeAThreeOne_outside_horn_has_missingTriangle_face
    {d : Nat}
    (y : (Δ[3] : SSet.{u}) _⦋d⦌)
    (hy : y ∉ (SSet.horn 3 (1 : Fin 4)).obj (op ⦋d⦌)) :
    ∃ (a b c : Fin (d + 1)) (hab : a ≤ b) (hbc : b ≤ c),
      (Δ[3] : SSet.{u}).map
          (SSet.stdSimplex.objEquiv
            (SSet.stdSimplex.triangle a b c hab hbc)).op y =
        typeAThreeOneMissingTriangle := by
  have h0 : (0 : Fin 4) ∈ Set.range y := by
    by_contra h
    apply hy
    rw [SSet.mem_horn_iff_notMem_range]
    exact ⟨0, by decide, h⟩
  have h2 : (2 : Fin 4) ∈ Set.range y := by
    by_contra h
    apply hy
    rw [SSet.mem_horn_iff_notMem_range]
    exact ⟨2, by decide, h⟩
  have h3 : (3 : Fin 4) ∈ Set.range y := by
    by_contra h
    apply hy
    rw [SSet.mem_horn_iff_notMem_range]
    exact ⟨3, by decide, h⟩
  rcases h0 with ⟨a, ha⟩
  rcases h2 with ⟨b, hb⟩
  rcases h3 with ⟨c, hc⟩
  have hab : a ≤ b := by
    by_contra h
    have hba : b < a := lt_of_not_ge h
    have hm := SSet.stdSimplex.monotone_apply y (le_of_lt hba)
    set_option backward.isDefEq.respectTransparency false in
      change y b ≤ y a at hm
    rw [hb, ha] at hm
    exact (by decide : ¬ (2 : Fin 4) ≤ 0) hm
  have hbc : b ≤ c := by
    by_contra h
    have hcb : c < b := lt_of_not_ge h
    have hm := SSet.stdSimplex.monotone_apply y (le_of_lt hcb)
    set_option backward.isDefEq.respectTransparency false in
      change y c ≤ y b at hm
    rw [hc, hb] at hm
    exact (by decide : ¬ (3 : Fin 4) ≤ 2) hm
  refine ⟨a, b, c, hab, hbc, ?_⟩
  apply SSet.stdSimplex.ext
  intro k
  fin_cases k
  · set_option backward.isDefEq.respectTransparency false in
      change y a = (0 : Fin 4)
    exact ha
  · set_option backward.isDefEq.respectTransparency false in
      change y b = (2 : Fin 4)
    exact hb
  · set_option backward.isDefEq.respectTransparency false in
      change y c = (3 : Fin 4)
    exact hc

/-- Every canonical attachment generator lifts against the degree-three
standard type-(A) horn inclusion. -/
theorem canonicalGenerator_hasLiftingProperty_typeAThreeOne
    (c : ScaledHornAttachmentGeneratorIndex.{u}) :
    HasLiftingProperty
      (scaledHornAttachmentGeneratorHom c)
      (standardTypeAScaledHornGeneratorHom typeAThreeOneIndex) := by
  refine ⟨?_⟩
  intro f g sq
  let lmap :
      ((Δ[c.n] : SSet.{u}) ⊗ Δ[1]) ⟶
        (Λ[3, (1 : Fin 4)] : SSet.{u}) :=
    SSet.Subcomplex.lift g.map (by
      rintro ⟨⟨d⟩⟩ y hy
      rw [Subfunctor.range_obj] at hy
      rcases hy with ⟨z, rfl⟩
      by_contra hmem
      obtain ⟨a, b, cc, hab, hbc, hface⟩ :=
        typeAThreeOne_outside_horn_has_missingTriangle_face
          (g.map.app (op ⦋d⦌) z) hmem
      let s : (Δ[d] : SSet.{u}) _⦋2⦌ :=
        SSet.stdSimplex.triangle a b cc hab hbc
      let t : ((Δ[c.n] : SSet.{u}) ⊗ Δ[1]) _⦋2⦌ :=
        ((Δ[c.n] : SSet.{u}) ⊗ Δ[1]).map
          (SSet.stdSimplex.objEquiv s).op z
      have hnat :
          g.map.app (op ⦋2⦌) t =
            (Δ[3] : SSet.{u}).map
              (SSet.stdSimplex.objEquiv s).op
              (g.map.app (op ⦋d⦌) z) := by
        exact ConcreteCategory.congr_hom
          (g.map.naturality (SSet.stdSimplex.objEquiv s).op) z
      have himage :
          g.map.app (op ⦋2⦌) t = typeAThreeOneMissingTriangle := by
        rw [hnat]
        simpa [s] using hface
      exact typeAThreeOne_square_missingTriangle_not_image c sq t himage)
  have hlift :
      lmap ≫
          (Λ[3, (1 : Fin 4)].ι :
            (Λ[3, (1 : Fin 4)] : SSet.{u}) ⟶ (Δ[3] : SSet.{u})) =
        g.map := by
    dsimp [lmap]
  let l :
      scaledSimplexCylinder c.simplexScaling ⟶
        standardTypeAScaledHorn typeAThreeOneIndex :=
    { map := lmap
      scaled := by
        intro t ht
        change
          (standardTypeASimplexScaling (1 : Fin 4)).thin
            ((Λ[3, (1 : Fin 4)].ι :
              (Λ[3, (1 : Fin 4)] : SSet.{u}) ⟶ (Δ[3] : SSet.{u})).app
              (op ⦋2⦌) (lmap.app (op ⦋2⦌) t))
        have hg := g.scaled t ht
        rw [← NatTrans.comp_app_apply, hlift]
        exact hg }
  refine CommSq.HasLift.mk'
    { l := l
      fac_right := by
        apply ScaledSSet.ScaledMap.ext
        set_option backward.isDefEq.respectTransparency false in
          change
            lmap ≫
                (Λ[3, (1 : Fin 4)].ι :
                  (Λ[3, (1 : Fin 4)] : SSet.{u}) ⟶ (Δ[3] : SSet.{u})) =
              g.map
        exact hlift
      fac_left := by
        apply ScaledSSet.ScaledMap.ext
        apply (cancel_mono
          (Λ[3, (1 : Fin 4)].ι :
            (Λ[3, (1 : Fin 4)] : SSet.{u}) ⟶ (Δ[3] : SSet.{u}))).1
        have hsqmap := congrArg ScaledSSet.ScaledMap.map sq.w
        change
          (scaledHornAttachmentGeneratorHom c).map ≫ lmap ≫
              (Λ[3, (1 : Fin 4)].ι :
                (Λ[3, (1 : Fin 4)] : SSet.{u}) ⟶ (Δ[3] : SSet.{u})) =
            f.map ≫
              (Λ[3, (1 : Fin 4)].ι :
                (Λ[3, (1 : Fin 4)] : SSet.{u}) ⟶ (Δ[3] : SSet.{u}))
        rw [hlift]
        simpa [standardTypeAScaledHornGeneratorHom, typeAThreeOneIndex] using
          hsqmap.symm }

/-- The degree-three type-(A) horn inclusion lies in the complete canonical
right class. -/
theorem typeAThreeOne_canonicalRight :
    (scaledHornAttachmentGenerators :
      MorphismProperty (ScaledSSet.{u})).rlp
      (standardTypeAScaledHornGeneratorHom typeAThreeOneIndex) := by
  intro A B h hh
  dsimp [scaledHornAttachmentGenerators] at hh
  cases hh with
  | mk c =>
      exact canonicalGenerator_hasLiftingProperty_typeAThreeOne c

/-! ## The same horn cannot lift against itself -/

/-- The top identity `3`-simplex is not in `Λ[3,1]`. -/
theorem typeAThreeTopSimplex_not_mem_horn :
    typeAHigherTargetTopSimplex 2 ∉
      (SSet.horn 3 (1 : Fin 4)).obj (op ⦋3⦌) := by
  intro hmem
  rcases
      (SSet.mem_horn_iff_notMem_range
        (typeAHigherTargetTopSimplex 2) (1 : Fin 4)).1 hmem with
    ⟨missing, _, hmissing⟩
  apply hmissing
  exact ⟨missing, rfl⟩

/-- A proper horn inclusion has no self-lifting property. -/
theorem typeAThreeOne_not_hasLiftingProperty_self :
    ¬ HasLiftingProperty
      (standardTypeAScaledHornGeneratorHom typeAThreeOneIndex :
        (standardTypeAScaledHorn typeAThreeOneIndex : ScaledSSet.{u}) ⟶
          (standardTypeAScaledSimplex typeAThreeOneIndex : ScaledSSet.{u}))
      (standardTypeAScaledHornGeneratorHom typeAThreeOneIndex :
        (standardTypeAScaledHorn typeAThreeOneIndex : ScaledSSet.{u}) ⟶
          (standardTypeAScaledSimplex typeAThreeOneIndex : ScaledSSet.{u})) := by
  intro h
  let j :
      (standardTypeAScaledHorn typeAThreeOneIndex : ScaledSSet.{u}) ⟶
        (standardTypeAScaledSimplex typeAThreeOneIndex : ScaledSSet.{u}) :=
    standardTypeAScaledHornGeneratorHom typeAThreeOneIndex
  let sq : CommSq
      (𝟙 (standardTypeAScaledHorn typeAThreeOneIndex : ScaledSSet.{u})) j j
      (𝟙 (standardTypeAScaledSimplex typeAThreeOneIndex : ScaledSSet.{u})) :=
    { w := by simp }
  rcases (h.sq_hasLift sq).exists_lift with ⟨L⟩
  have hright := congrArg ScaledSSet.ScaledMap.map L.fac_right
  set_option backward.isDefEq.respectTransparency false in
    change
      L.l.map ≫
          (Λ[3, (1 : Fin 4)].ι :
            (Λ[3, (1 : Fin 4)] : SSet.{u}) ⟶ (Δ[3] : SSet.{u}) =
        𝟙 (Δ[3] : SSet.{u}) at hright
  let x := L.l.map.app (op ⦋3⦌)
    (typeAHigherTargetTopSimplex 2)
  have hpoint := ConcreteCategory.congr_hom
    (congr_app hright (op ⦋3⦌))
    (typeAHigherTargetTopSimplex 2)
  have hx :
      (Λ[3, (1 : Fin 4)].ι :
        (Λ[3, (1 : Fin 4)] : SSet.{u}) ⟶ (Δ[3] : SSet.{u})).app
          (op ⦋3⦌) x =
        typeAHigherTargetTopSimplex 2 := by
    set_option backward.isDefEq.respectTransparency false in
      change
        (Λ[3, (1 : Fin 4)].ι :
          (Λ[3, (1 : Fin 4)] : SSet.{u}) ⟶ (Δ[3] : SSet.{u})).app
            (op ⦋3⦌)
            (L.l.map.app (op ⦋3⦌) (typeAHigherTargetTopSimplex 2)) =
          typeAHigherTargetTopSimplex 2 at hpoint
    simpa [x] using hpoint
  have hmem :
      typeAHigherTargetTopSimplex 2 ∈
        (SSet.horn 3 (1 : Fin 4)).obj (op ⦋3⦌) := by
    rw [← hx]
    exact x.property
  exact typeAThreeTopSimplex_not_mem_horn hmem

/-! ## Generated-class incomparability -/

/-- The degree-three standard generator is not canonical-generated. -/
theorem typeAThreeOne_not_mem_canonicalGenerated :
    ¬ (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
      (standardTypeAScaledHornGeneratorHom typeAThreeOneIndex) := by
  intro hleft
  exact typeAThreeOne_not_hasLiftingProperty_self
    (hleft _ typeAThreeOne_canonicalRight)

/-- Therefore the standard generated left class is not contained in the
canonical generated left class. -/
theorem standardGenerated_not_le_canonicalGenerated :
    ¬ (standardGeneratedScaledAnodyneABC : MorphismProperty (ScaledSSet.{u})) ≤
      (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u})) := by
  intro hle
  exact typeAThreeOne_not_mem_canonicalGenerated
    (hle _ (standardTypeAGenerator_mem_standardGenerated typeAThreeOneIndex))

/-- The two generated left classes are genuinely incomparable. -/
theorem standardCanonicalGenerated_incomparable :
    (¬ (standardGeneratedScaledAnodyneABC : MorphismProperty (ScaledSSet.{u})) ≤
        (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))) ∧
      (¬ (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u})) ≤
        (standardGeneratedScaledAnodyneABC : MorphismProperty (ScaledSSet.{u}))) := by
  exact ⟨standardGenerated_not_le_canonicalGenerated,
    canonicalGenerated_not_le_standardGenerated⟩

end

end KUOS.DependentOriginationCanonicalTypeAThreeRelativeHornRigidityV1_118