import KUOS.DependentOriginationCanonicalTypeATwoStaircaseRetractV1_110

namespace KUOS.DependentOriginationCanonicalTypeAThreeAdditionObstructionV1_111

open CategoryTheory
open CategoryTheory.Category
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationCanonicalTypeATwoStaircaseRetractV1_110

universe u

/-!
# The degree-three obstruction to a one-step addition staircase v1.111

Version v1.110 closes the unique degree-two type-(A) generator by retracting it
from the canonical `n = 1` horn-cylinder attachment.  Its target retraction is
coordinate addition

```text
Delta[1] x Delta[1] -> Delta[2],
(a,b) |-> a+b.
```

It is tempting to continue with

```text
Delta[2] x Delta[1] -> Delta[3].
```

This file proves that this tempting extension is mathematically impossible,
not merely inconvenient in Lean.  The obstruction is forced by the definition
of a scaling: every degenerate triangle in the first cylinder coordinate is
thin for *every* possible base scaling.

For the two inner type-(A) indices in dimension three we exhibit explicit
cylinder-thin triangles whose addition images are respectively

```text
(0,1,3)   for i = 1,
(0,2,3)   for i = 2.
```

Both images are nondegenerate and are not the distinguished consecutive
triangle.  Hence neither is thin in the standard type-(A) scaling.  Therefore
no choice of scaling on `Delta[2]` can make coordinate addition a scaled map to
either dimension-three type-(A) target.

Consequently the v1.110 one-cell retract is genuinely exceptional to dimension
two.  The remaining reverse comparison must use a local multi-prism/cellular
filtration (the rank/staircase machinery of v1.61-v1.77), rather than a single
dimension-raising addition retract.
-/

/-! ## Coordinate addition in the first unresolved dimension -/

/-- Pointwise coordinate addition `Delta[2] x Delta[1] -> Delta[3]`. -/
def typeAThreeAdditionMap :
    ((Δ[2] : SSet.{u}) ⊗ Δ[1]) ⟶ (Δ[3] : SSet.{u}) where
  app := fun ⟨⟨d⟩⟩ => ↾fun z =>
    SSet.stdSimplex.objMk
      { toFun := fun j =>
          ⟨(z.1 j).val + (z.2 j).val, by omega⟩
        monotone' := by
          intro a b hab
          have h₁ := SSet.stdSimplex.monotone_apply z.1 hab
          have h₂ := SSet.stdSimplex.monotone_apply z.2 hab
          apply Fin.mk_le_mk.mpr
          omega }
  naturality := by
    intro d e f
    ext z j
    rfl

@[simp]
theorem typeAThreeAdditionMap_apply
    {d : Nat}
    (z : ((Δ[2] : SSet.{u}) ⊗ Δ[1]) _⦋d⦌)
    (j : Fin (d + 1)) :
    typeAThreeAdditionMap.app (op ⦋d⦌) z j =
      ⟨(z.1 j).val + (z.2 j).val, by omega⟩ :=
  rfl

/-! ## Explicit obstruction at the inner index i = 1 -/

/-- A source triangle with first coordinate `[0,0,2]` and interval coordinate
`[0,1,1]`.  Its first coordinate is a sigma-zero degeneracy. -/
def typeAThreeIndexOneSourceTriangle :
    ((Δ[2] : SSet.{u}) ⊗ Δ[1]) _⦋2⦌ :=
  ⟨SSet.stdSimplex.triangle
      (0 : Fin 3) (0 : Fin 3) (2 : Fin 3) (by decide) (by decide),
    SSet.stdSimplex.triangle
      (0 : Fin 2) (1 : Fin 2) (1 : Fin 2) (by decide) (by decide)⟩

/-- Its addition image is the nonconsecutive triangle `[0,1,3]`. -/
def typeAThreeIndexOneTargetTriangle : (Δ[3] : SSet.{u}) _⦋2⦌ :=
  SSet.stdSimplex.triangle
    (0 : Fin 4) (1 : Fin 4) (3 : Fin 4) (by decide) (by decide)

/-- The first obstruction triangle is cylinder-thin for every possible scaling
on `Delta[2]`. -/
theorem typeAThreeIndexOneSourceTriangle_thin
    (sΔ : ScaledSimplicialSet (Δ[2] : SSet.{u})) :
    (simplexCylinderScaling sΔ).thin typeAThreeIndexOneSourceTriangle := by
  change sΔ.thin typeAThreeIndexOneSourceTriangle.1
  let e : (Δ[2] : SSet.{u}) _⦋1⦌ :=
    SSet.stdSimplex.edge 2 (0 : Fin 3) (2 : Fin 3) (by decide)
  have hσ :
      (Δ[2] : SSet.{u}).σ (0 : Fin 2) e =
        typeAThreeIndexOneSourceTriangle.1 := by
    apply SSet.stdSimplex.ext
    intro j
    fin_cases j <;> rfl
  rw [← hσ]
  exact sΔ.thin_sigma_zero e

/-- Coordinate addition sends the first source witness exactly to `[0,1,3]`. -/
theorem typeAThreeAdditionMap_indexOneSource :
    typeAThreeAdditionMap.app (op ⦋2⦌)
        typeAThreeIndexOneSourceTriangle =
      typeAThreeIndexOneTargetTriangle := by
  apply SSet.stdSimplex.ext
  intro j
  fin_cases j <;> rfl

/-- `[0,1,3]` is nondegenerate. -/
theorem typeAThreeIndexOneTargetTriangle_nondegenerate :
    typeAThreeIndexOneTargetTriangle ∈
      (Δ[3] : SSet.{u}).nonDegenerate 2 := by
  rw [SSet.stdSimplex.mem_nonDegenerate_iff_strictMono,
    Fin.strictMono_iff_lt_succ]
  intro j
  fin_cases j <;> decide

/-- `[0,1,3]` is not thin for the standard type-(A) scaling at `i = 1`. -/
theorem typeAThreeIndexOneTargetTriangle_not_thin :
    ¬ (standardTypeASimplexScaling (1 : Fin 4)).thin
        typeAThreeIndexOneTargetTriangle := by
  intro hthin
  rcases hthin with hmin | hdist
  · have hdeg :
        typeAThreeIndexOneTargetTriangle ∈
          (Δ[3] : SSet.{u}).degenerate 2 := by
      rw [SSet.degenerate_eq_iUnion_range_σ]
      simp only [Set.mem_iUnion, Set.mem_range]
      rcases hmin with ⟨x, hx⟩ | ⟨x, hx⟩
      · exact ⟨(0 : Fin 2), x, hx⟩
      · exact ⟨(1 : Fin 2), x, hx⟩
    rw [SSet.mem_degenerate_iff_notMem_nonDegenerate] at hdeg
    exact hdeg typeAThreeIndexOneTargetTriangle_nondegenerate
  · rcases hdist with ⟨_, _, hbad⟩
    change 1 + 1 = 3 at hbad
    omega

/-- Therefore coordinate addition cannot be scaled to the `i = 1` type-(A)
target, independently of the chosen base scaling. -/
theorem typeAThreeAdditionMap_not_scaled_indexOne
    (sΔ : ScaledSimplicialSet (Δ[2] : SSet.{u})) :
    ¬ IsScaledMap
        (simplexCylinderScaling sΔ)
        (standardTypeASimplexScaling (1 : Fin 4))
        typeAThreeAdditionMap := by
  intro hscaled
  have himage := hscaled typeAThreeIndexOneSourceTriangle
    (typeAThreeIndexOneSourceTriangle_thin sΔ)
  rw [typeAThreeAdditionMap_indexOneSource] at himage
  exact typeAThreeIndexOneTargetTriangle_not_thin himage

/-! ## Explicit obstruction at the inner index i = 2 -/

/-- A source triangle with first coordinate `[0,2,2]` and interval coordinate
`[0,0,1]`.  Its first coordinate is a sigma-one degeneracy. -/
def typeAThreeIndexTwoSourceTriangle :
    ((Δ[2] : SSet.{u}) ⊗ Δ[1]) _⦋2⦌ :=
  ⟨SSet.stdSimplex.triangle
      (0 : Fin 3) (2 : Fin 3) (2 : Fin 3) (by decide) (by decide),
    SSet.stdSimplex.triangle
      (0 : Fin 2) (0 : Fin 2) (1 : Fin 2) (by decide) (by decide)⟩

/-- Its addition image is the nonconsecutive triangle `[0,2,3]`. -/
def typeAThreeIndexTwoTargetTriangle : (Δ[3] : SSet.{u}) _⦋2⦌ :=
  SSet.stdSimplex.triangle
    (0 : Fin 4) (2 : Fin 4) (3 : Fin 4) (by decide) (by decide)

/-- The second obstruction triangle is cylinder-thin for every possible scaling
on `Delta[2]`. -/
theorem typeAThreeIndexTwoSourceTriangle_thin
    (sΔ : ScaledSimplicialSet (Δ[2] : SSet.{u})) :
    (simplexCylinderScaling sΔ).thin typeAThreeIndexTwoSourceTriangle := by
  change sΔ.thin typeAThreeIndexTwoSourceTriangle.1
  let e : (Δ[2] : SSet.{u}) _⦋1⦌ :=
    SSet.stdSimplex.edge 2 (0 : Fin 3) (2 : Fin 3) (by decide)
  have hσ :
      (Δ[2] : SSet.{u}).σ (1 : Fin 2) e =
        typeAThreeIndexTwoSourceTriangle.1 := by
    apply SSet.stdSimplex.ext
    intro j
    fin_cases j <;> rfl
  rw [← hσ]
  exact sΔ.thin_sigma_one e

/-- Coordinate addition sends the second source witness exactly to `[0,2,3]`. -/
theorem typeAThreeAdditionMap_indexTwoSource :
    typeAThreeAdditionMap.app (op ⦋2⦌)
        typeAThreeIndexTwoSourceTriangle =
      typeAThreeIndexTwoTargetTriangle := by
  apply SSet.stdSimplex.ext
  intro j
  fin_cases j <;> rfl

/-- `[0,2,3]` is nondegenerate. -/
theorem typeAThreeIndexTwoTargetTriangle_nondegenerate :
    typeAThreeIndexTwoTargetTriangle ∈
      (Δ[3] : SSet.{u}).nonDegenerate 2 := by
  rw [SSet.stdSimplex.mem_nonDegenerate_iff_strictMono,
    Fin.strictMono_iff_lt_succ]
  intro j
  fin_cases j <;> decide

/-- `[0,2,3]` is not thin for the standard type-(A) scaling at `i = 2`. -/
theorem typeAThreeIndexTwoTargetTriangle_not_thin :
    ¬ (standardTypeASimplexScaling (2 : Fin 4)).thin
        typeAThreeIndexTwoTargetTriangle := by
  intro hthin
  rcases hthin with hmin | hdist
  · have hdeg :
        typeAThreeIndexTwoTargetTriangle ∈
          (Δ[3] : SSet.{u}).degenerate 2 := by
      rw [SSet.degenerate_eq_iUnion_range_σ]
      simp only [Set.mem_iUnion, Set.mem_range]
      rcases hmin with ⟨x, hx⟩ | ⟨x, hx⟩
      · exact ⟨(0 : Fin 2), x, hx⟩
      · exact ⟨(1 : Fin 2), x, hx⟩
    rw [SSet.mem_degenerate_iff_notMem_nonDegenerate] at hdeg
    exact hdeg typeAThreeIndexTwoTargetTriangle_nondegenerate
  · rcases hdist with ⟨_, hbad, _⟩
    change 0 + 1 = 2 at hbad
    omega

/-- Therefore coordinate addition cannot be scaled to the `i = 2` type-(A)
target, independently of the chosen base scaling. -/
theorem typeAThreeAdditionMap_not_scaled_indexTwo
    (sΔ : ScaledSimplicialSet (Δ[2] : SSet.{u})) :
    ¬ IsScaledMap
        (simplexCylinderScaling sΔ)
        (standardTypeASimplexScaling (2 : Fin 4))
        typeAThreeAdditionMap := by
  intro hscaled
  have himage := hscaled typeAThreeIndexTwoSourceTriangle
    (typeAThreeIndexTwoSourceTriangle_thin sΔ)
  rw [typeAThreeAdditionMap_indexTwoSource] at himage
  exact typeAThreeIndexTwoTargetTriangle_not_thin himage

/-! ## Exhaust the dimension-three type-(A) family -/

/-- The first dimension-three inner type-(A) index. -/
def standardTypeAThreeIndexOne : StandardTypeAHornGeneratorIndex where
  n := 3
  i := 1
  inner_left := by decide
  inner_right := by decide

/-- The second dimension-three inner type-(A) index. -/
def standardTypeAThreeIndexTwo : StandardTypeAHornGeneratorIndex where
  n := 3
  i := 2
  inner_left := by decide
  inner_right := by decide

/-- Every dimension-three inner type-(A) index is one of the preceding two. -/
theorem standardTypeAHornGeneratorIndex_dim_three_cases
    (g : StandardTypeAHornGeneratorIndex)
    (hn : g.n = 3) :
    g = standardTypeAThreeIndexOne ∨
      g = standardTypeAThreeIndexTwo := by
  rcases g with ⟨n, i, hleft, hright⟩
  subst n
  change 0 < i.val at hleft
  change i.val < 3 at hright
  have hi : i.val = 1 ∨ i.val = 2 := by omega
  rcases hi with hi | hi
  · left
    have : i = (1 : Fin 4) := Fin.ext hi
    subst i
    rfl
  · right
    have : i = (2 : Fin 4) := Fin.ext hi
    subst i
    rfl

/-- Thus for every literal dimension-three type-(A) generator, no scaling on
`Delta[2]` makes the coordinate-addition target retraction scaled. -/
theorem typeAThreeAdditionMap_not_scaled
    (g : StandardTypeAHornGeneratorIndex)
    (hn : g.n = 3)
    (sΔ : ScaledSimplicialSet (Δ[2] : SSet.{u})) :
    ¬ IsScaledMap
        (simplexCylinderScaling sΔ)
        (standardTypeASimplexScaling g.i)
        typeAThreeAdditionMap := by
  rcases standardTypeAHornGeneratorIndex_dim_three_cases g hn with hg | hg
  · subst g
    exact typeAThreeAdditionMap_not_scaled_indexOne sΔ
  · subst g
    exact typeAThreeAdditionMap_not_scaled_indexTwo sΔ

/-- In existential form: the target half of a one-step addition staircase
retract does not exist for any dimension-three type-(A) generator. -/
theorem typeAThree_no_oneStepAdditionTargetRetraction
    (g : StandardTypeAHornGeneratorIndex)
    (hn : g.n = 3) :
    ¬ ∃ sΔ : ScaledSimplicialSet (Δ[2] : SSet.{u}),
        IsScaledMap
          (simplexCylinderScaling sΔ)
          (standardTypeASimplexScaling g.i)
          typeAThreeAdditionMap := by
  rintro ⟨sΔ, hsΔ⟩
  exact typeAThreeAdditionMap_not_scaled g hn sΔ hsΔ

/-!
The dimension-two mechanism is therefore sharply delimited:

```text
n = 2:
  one lower-dimensional canonical cylinder
  + coordinate addition
  + staircase section
  => genuine arrow retract (v1.110).

n = 3:
  coordinate addition already fails scaledness
  for every possible scaling on Delta[2].
```

The failure is forced by degenerate first-coordinate triangles, so enriching
the base scaling cannot repair it.  The next positive unit must instead break
the higher horn into local prism cells whose individual target maps send each
mandatory mixed-thin triangle only to a degeneracy or to the distinguished
type-(A) triangle.  This is precisely the geometric role of the existing
rank/staircase decomposition in v1.61-v1.77.
-/

end KUOS.DependentOriginationCanonicalTypeAThreeAdditionObstructionV1_111
