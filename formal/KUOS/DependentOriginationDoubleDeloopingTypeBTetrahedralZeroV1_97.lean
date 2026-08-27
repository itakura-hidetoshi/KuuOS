import KUOS.DependentOriginationDoubleDeloopingThinComparisonZeroV1_96

namespace KUOS.DependentOriginationDoubleDeloopingTypeBTetrahedralZeroV1_97

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Bicategory
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95
open KUOS.DependentOriginationDoubleDeloopingThinComparisonZeroV1_96

/-!
# Additive tetrahedral propagation for the standard type-(B) cell v1.97

The v1.96 arithmetic description identifies thin Duskin triangles in `B²ℕ`
with comparison label zero.  The standard type-(B) generator on `Delta[4]`
starts with five designated thin triangles and adds `014` and `034`.

For a normal lax simplex into `B²ℕ`, the lax associativity equation is exactly
the additive 2-cocycle equation on every tetrahedron:

```text
a_ijk + a_ikl = a_jkl + a_ijl.
```

This file extracts that equation directly from Mathlib's
`StrictlyUnitaryLaxFunctor.map₂_associator` and proves the exact zero
propagation needed by type-(B).  On tetrahedron `0124`, zero labels `012` and
`024` force both `124` and `014` to be zero.  On tetrahedron `0134`, zero
labels `013`, `134`, and the newly obtained `014` force `034` to be zero.

Thus the substantive scaling arithmetic of type-(B) is now a finite theorem
in natural-number addition.  The remaining bridge to literal terminal RLP is
only the Yoneda identification between these labels and the seven named
triangles of the standard `Delta[4]` generator.
-/

/-- In the additive double delooping, lax associativity is the ordinary
additive 2-cocycle equation. -/
theorem natDuskin_mapComp_additive_cocycle
    {n : Nat}
    (sigma : DuskinSimplex NatDoubleDelooping n)
    {a b c d : DuskinOrdinal n}
    (f : a ⟶ b) (g : b ⟶ c) (h : c ⟶ d) :
    sigma.mapComp f g + sigma.mapComp (f ≫ g) h =
      sigma.mapComp g h + sigma.mapComp f (g ≫ h) := by
  have hcoh := sigma.map₂_associator f g h
  have hmap₂ : sigma.map₂ (α_ f g h).hom = 0 :=
    natDuskin_map₂_eq_zero sigma _
  rw [hmap₂] at hcoh
  change
    sigma.mapComp f g + sigma.mapComp (f ≫ g) h + 0 =
      0 + sigma.mapComp g h + sigma.mapComp f (g ≫ h) at hcoh
  omega

/-- If the two labels on the left side of a tetrahedral cocycle equation are
zero, both labels on the right side are zero. -/
theorem natDuskin_tetrahedron_zero_split
    {n : Nat}
    (sigma : DuskinSimplex NatDoubleDelooping n)
    {a b c d : DuskinOrdinal n}
    (f : a ⟶ b) (g : b ⟶ c) (h : c ⟶ d)
    (hfg : sigma.mapComp f g = 0)
    (hfg_h : sigma.mapComp (f ≫ g) h = 0) :
    sigma.mapComp g h = 0 ∧ sigma.mapComp f (g ≫ h) = 0 := by
  have hcocycle := natDuskin_mapComp_additive_cocycle sigma f g h
  omega

/-- If three labels in the tetrahedral equation vanish, the remaining
left-hand label vanishes as well. -/
theorem natDuskin_tetrahedron_zero_remaining
    {n : Nat}
    (sigma : DuskinSimplex NatDoubleDelooping n)
    {a b c d : DuskinOrdinal n}
    (f : a ⟶ b) (g : b ⟶ c) (h : c ⟶ d)
    (hfg : sigma.mapComp f g = 0)
    (hgh : sigma.mapComp g h = 0)
    (houter : sigma.mapComp f (g ≫ h) = 0) :
    sigma.mapComp (f ≫ g) h = 0 := by
  have hcocycle := natDuskin_mapComp_additive_cocycle sigma f g h
  omega

/-! ## The seven type-(B) labels inside a Duskin four-simplex -/

/-- The unique ordinal edge `i -> j` in `[4]` for `i ≤ j`. -/
def natFourEdge {i j : Fin 5} (hij : i ≤ j) :
    LocallyDiscrete.mk i ⟶ LocallyDiscrete.mk j :=
  (homOfLE hij).toLoc

/-- Comparison label on triangle `012`. -/
def natFourLabel012
    (sigma : DuskinSimplex NatDoubleDelooping 4) : Nat :=
  sigma.mapComp
    (natFourEdge (i := (0 : Fin 5)) (j := 1) (by decide))
    (natFourEdge (i := (1 : Fin 5)) (j := 2) (by decide))

/-- Comparison label on triangle `024`. -/
def natFourLabel024
    (sigma : DuskinSimplex NatDoubleDelooping 4) : Nat :=
  sigma.mapComp
    (natFourEdge (i := (0 : Fin 5)) (j := 2) (by decide))
    (natFourEdge (i := (2 : Fin 5)) (j := 4) (by decide))

/-- Comparison label on triangle `124`. -/
def natFourLabel124
    (sigma : DuskinSimplex NatDoubleDelooping 4) : Nat :=
  sigma.mapComp
    (natFourEdge (i := (1 : Fin 5)) (j := 2) (by decide))
    (natFourEdge (i := (2 : Fin 5)) (j := 4) (by decide))

/-- Comparison label on triangle `014`. -/
def natFourLabel014
    (sigma : DuskinSimplex NatDoubleDelooping 4) : Nat :=
  sigma.mapComp
    (natFourEdge (i := (0 : Fin 5)) (j := 1) (by decide))
    (natFourEdge (i := (1 : Fin 5)) (j := 4) (by decide))

/-- Comparison label on triangle `013`. -/
def natFourLabel013
    (sigma : DuskinSimplex NatDoubleDelooping 4) : Nat :=
  sigma.mapComp
    (natFourEdge (i := (0 : Fin 5)) (j := 1) (by decide))
    (natFourEdge (i := (1 : Fin 5)) (j := 3) (by decide))

/-- Comparison label on triangle `134`. -/
def natFourLabel134
    (sigma : DuskinSimplex NatDoubleDelooping 4) : Nat :=
  sigma.mapComp
    (natFourEdge (i := (1 : Fin 5)) (j := 3) (by decide))
    (natFourEdge (i := (3 : Fin 5)) (j := 4) (by decide))

/-- Comparison label on triangle `034`. -/
def natFourLabel034
    (sigma : DuskinSimplex NatDoubleDelooping 4) : Nat :=
  sigma.mapComp
    (natFourEdge (i := (0 : Fin 5)) (j := 3) (by decide))
    (natFourEdge (i := (3 : Fin 5)) (j := 4) (by decide))

/-! ## The two tetrahedra used by type-(B) -/

/-- On tetrahedron `0124`, source-zero labels `012` and `024` force both
`124` and the target-only label `014` to vanish. -/
theorem natFour_first_typeB_tetrahedron_zero
    (sigma : DuskinSimplex NatDoubleDelooping 4)
    (h012 : natFourLabel012 sigma = 0)
    (h024 : natFourLabel024 sigma = 0) :
    natFourLabel124 sigma = 0 ∧ natFourLabel014 sigma = 0 := by
  let e01 := natFourEdge (i := (0 : Fin 5)) (j := 1) (by decide)
  let e12 := natFourEdge (i := (1 : Fin 5)) (j := 2) (by decide)
  let e24 := natFourEdge (i := (2 : Fin 5)) (j := 4) (by decide)
  let e02 := natFourEdge (i := (0 : Fin 5)) (j := 2) (by decide)
  let e14 := natFourEdge (i := (1 : Fin 5)) (j := 4) (by decide)
  have he02 : e01 ≫ e12 = e02 := Subsingleton.elim _ _
  have he14 : e12 ≫ e24 = e14 := Subsingleton.elim _ _
  have h012' : sigma.mapComp e01 e12 = 0 := by
    simpa [natFourLabel012, e01, e12] using h012
  have h024' : sigma.mapComp (e01 ≫ e12) e24 = 0 := by
    rw [he02]
    simpa [natFourLabel024, e02, e24] using h024
  rcases natDuskin_tetrahedron_zero_split sigma e01 e12 e24 h012' h024' with
    ⟨h124, h014⟩
  constructor
  · simpa [natFourLabel124, e12, e24] using h124
  · rw [he14] at h014
    simpa [natFourLabel014, e01, e14] using h014

/-- On tetrahedron `0134`, zero labels `013`, `134`, and `014` force the other
target-only label `034` to vanish. -/
theorem natFour_second_typeB_tetrahedron_zero
    (sigma : DuskinSimplex NatDoubleDelooping 4)
    (h013 : natFourLabel013 sigma = 0)
    (h134 : natFourLabel134 sigma = 0)
    (h014 : natFourLabel014 sigma = 0) :
    natFourLabel034 sigma = 0 := by
  let e01 := natFourEdge (i := (0 : Fin 5)) (j := 1) (by decide)
  let e13 := natFourEdge (i := (1 : Fin 5)) (j := 3) (by decide)
  let e34 := natFourEdge (i := (3 : Fin 5)) (j := 4) (by decide)
  let e03 := natFourEdge (i := (0 : Fin 5)) (j := 3) (by decide)
  let e14 := natFourEdge (i := (1 : Fin 5)) (j := 4) (by decide)
  have he03 : e01 ≫ e13 = e03 := Subsingleton.elim _ _
  have he14 : e13 ≫ e34 = e14 := Subsingleton.elim _ _
  have h013' : sigma.mapComp e01 e13 = 0 := by
    simpa [natFourLabel013, e01, e13] using h013
  have h134' : sigma.mapComp e13 e34 = 0 := by
    simpa [natFourLabel134, e13, e34] using h134
  have h014' : sigma.mapComp e01 (e13 ≫ e34) = 0 := by
    rw [he14]
    simpa [natFourLabel014, e01, e14] using h014
  have h034 :=
    natDuskin_tetrahedron_zero_remaining
      sigma e01 e13 e34 h013' h134' h014'
  rw [he03] at h034
  simpa [natFourLabel034, e03, e34] using h034

/-- The four source labels actually needed by the type-(B) propagation force
both target-only labels to vanish.  The fifth standard source triangle `123`
is compatible but not needed for this implication. -/
theorem natFour_typeB_target_zero_of_source_zero
    (sigma : DuskinSimplex NatDoubleDelooping 4)
    (h012 : natFourLabel012 sigma = 0)
    (h024 : natFourLabel024 sigma = 0)
    (h013 : natFourLabel013 sigma = 0)
    (h134 : natFourLabel134 sigma = 0) :
    natFourLabel014 sigma = 0 ∧ natFourLabel034 sigma = 0 := by
  have hfirst := natFour_first_typeB_tetrahedron_zero sigma h012 h024
  have h014 := hfirst.2
  exact ⟨h014,
    natFour_second_typeB_tetrahedron_zero sigma h013 h134 h014⟩

/-!
The type-(B) scaling implication is therefore fully arithmetic:

```text
012 = 024 = 013 = 134 = 0
  -> 014 = 034 = 0.
```

Together with v1.96 (`thin <-> comparison = 0`), the only remaining step for
literal type-(B) terminal RLP is to identify the images of the named standard
triangles under Yoneda with the seven labels above.  No further bicategorical
coherence theorem is required.
-/

end KUOS.DependentOriginationDoubleDeloopingTypeBTetrahedralZeroV1_97
