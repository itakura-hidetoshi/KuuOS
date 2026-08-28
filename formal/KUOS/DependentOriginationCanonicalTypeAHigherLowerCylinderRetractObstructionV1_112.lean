import KUOS.DependentOriginationCanonicalTypeAThreeAdditionObstructionV1_111

namespace KUOS.DependentOriginationCanonicalTypeAHigherLowerCylinderRetractObstructionV1_112

open CategoryTheory
open CategoryTheory.Category
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationCanonicalTypeAThreeAdditionObstructionV1_111

universe u

noncomputable section

/-!
# No one-cell lower-cylinder retract in higher type-(A) dimensions v1.112

Version v1.110 found an exceptional degree-two arrow retract through one
lower-dimensional canonical cylinder.  Version v1.111 proved that its most
obvious degree-three continuation, coordinate addition, is not scaled.

The present file removes the choice of coordinate addition entirely.  Let
`m >= 2`, so the type-(A) target has simplex dimension `m+1 >= 3`.  Suppose
there were arbitrary scaled maps

```text
Delta[m+1] --s--> Delta[m] x Delta[1] --r--> Delta[m+1]
```

with `s >> r = id`, where the middle object carries the canonical cylinder
scaling over an arbitrary scaling on `Delta[m]`.

By Yoneda, the first coordinate of `s` is a monotone map

```text
Fin (m+2) -> Fin (m+1).
```

Cardinality forces this map to identify one adjacent pair `k,k+1`.  We prove
that for every inner type-(A) index and every such adjacent pair there is a
non-thin nondegenerate triangle containing that pair.  Its image under `s`
has degenerate first coordinate and is therefore cylinder-thin for every
possible middle scaling.  Scaledness of `r` would make the original triangle
thin, contradicting its construction and `r s = id`.

Thus the one-cell mechanism of v1.110 is genuinely confined to degree two:
for every type-(A) simplex dimension at least three, no target retract through
one lower canonical cylinder exists at all.  The remaining reverse comparison
must therefore use more than one local prism cell (or a different global
argument); changing the lower-simplex scaling cannot repair the obstruction.
-/

/-! ## Minimal degeneracy facts for an arbitrary scaling -/

/-- In any scaling on a standard simplex, a triangle whose first two vertices
agree is thin because it is a `sigma 0` degeneracy. -/
theorem arbitraryScaling_thin_of_zero_eq_one
    {n : Nat}
    (sΔ : ScaledSimplicialSet (Δ[n] : SSet.{u}))
    (t : (Δ[n] : SSet.{u}).obj (op ⦋2⦌))
    (h01 : t 0 = t 1) :
    sΔ.thin t := by
  let e : (Δ[n] : SSet.{u}).obj (op ⦋1⦌) :=
    (Δ[n] : SSet.{u}).δ (0 : Fin 3) t
  have hσ : (Δ[n] : SSet.{u}).σ (0 : Fin 2) e = t := by
    apply SSet.stdSimplex.ext
    intro a
    fin_cases a <;>
      simp [e, SSet.stdSimplex.σ_apply, SSet.stdSimplex.δ_apply, h01]
  rw [← hσ]
  exact sΔ.thin_sigma_zero e

/-- In any scaling on a standard simplex, a triangle whose last two vertices
agree is thin because it is a `sigma 1` degeneracy. -/
theorem arbitraryScaling_thin_of_one_eq_two
    {n : Nat}
    (sΔ : ScaledSimplicialSet (Δ[n] : SSet.{u}))
    (t : (Δ[n] : SSet.{u}).obj (op ⦋2⦌))
    (h12 : t 1 = t 2) :
    sΔ.thin t := by
  let e : (Δ[n] : SSet.{u}).obj (op ⦋1⦌) :=
    (Δ[n] : SSet.{u}).δ (2 : Fin 3) t
  have hσ : (Δ[n] : SSet.{u}).σ (1 : Fin 2) e = t := by
    apply SSet.stdSimplex.ext
    intro a
    fin_cases a <;>
      simp [e, SSet.stdSimplex.σ_apply, SSet.stdSimplex.δ_apply, h12]
  rw [← hσ]
  exact sΔ.thin_sigma_one e

/-! ## Nondegenerate non-distinguished triangles are not type-(A)-thin -/

/-- A nondegenerate triangle which is not the distinguished consecutive
triangle is not thin in the standard type-(A) scaling. -/
theorem standardTypeA_not_thin_of_nondegenerate_of_not_distinguished
    {n : Nat}
    (i : Fin (n + 1))
    (t : (Δ[n] : SSet.{u}).obj (op ⦋2⦌))
    (hnd : t ∈ (Δ[n] : SSet.{u}).nonDegenerate 2)
    (hnot : ¬ IsStandardTypeADistinguishedTriangle i t) :
    ¬ (standardTypeASimplexScaling i).thin t := by
  intro ht
  rcases ht with hmin | hdist
  · have hdeg : t ∈ (Δ[n] : SSet.{u}).degenerate 2 := by
      rw [SSet.degenerate_eq_iUnion_range_σ]
      simp only [Set.mem_iUnion, Set.mem_range]
      rcases hmin with ⟨x, hx⟩ | ⟨x, hx⟩
      · exact ⟨(0 : Fin 2), x, hx⟩
      · exact ⟨(1 : Fin 2), x, hx⟩
    rw [SSet.mem_degenerate_iff_notMem_nonDegenerate] at hdeg
    exact hdeg hnd
  · exact hnot hdist

/-! ## A non-thin triangle through every adjacent edge -/

/-- Data of a non-thin type-(A) triangle containing a prescribed adjacent
edge.  The edge may occur as the first or the second edge of the triangle. -/
structure TypeAAdjacentNonthinWitness
    (m : Nat)
    (i : Fin (m + 2))
    (k : Fin (m + 1)) where
  triangle : (Δ[m + 1] : SSet.{u}).obj (op ⦋2⦌)
  nonthin : ¬ (standardTypeASimplexScaling i).thin triangle
  containsAdjacent :
    (triangle 0 = k.castSucc ∧ triangle 1 = k.succ) ∨
      (triangle 1 = k.castSucc ∧ triangle 2 = k.succ)

/-- In every target dimension at least three, every adjacent edge belongs to
some non-thin type-(A) triangle.

The construction uses three cases.  At the left endpoint we use
`(0,1,last)`.  If the ordinary `(0,k,k+1)` triangle would be the distinguished
one, then necessarily `k=i=1`, and we use `(1,2,last)` instead.  In every other
case `(0,k,k+1)` works. -/
theorem typeAAdjacentNonthinWitness_exists
    (m : Nat)
    (hm : 2 ≤ m)
    (i : Fin (m + 2))
    (hi0 : 0 < i)
    (hilast : i < Fin.last (m + 1))
    (k : Fin (m + 1)) :
    Nonempty (TypeAAdjacentNonthinWitness.{u} m i k) := by
  by_cases hk0 : k = 0
  · subst k
    let t : (Δ[m + 1] : SSet.{u}).obj (op ⦋2⦌) :=
      SSet.stdSimplex.triangle
        (0 : Fin (m + 2)) (1 : Fin (m + 2)) (Fin.last (m + 1))
        (by omega) (by omega)
    have hnd : t ∈ (Δ[m + 1] : SSet.{u}).nonDegenerate 2 := by
      rw [SSet.stdSimplex.mem_nonDegenerate_iff_strictMono,
        Fin.strictMono_iff_lt_succ]
      intro a
      fin_cases a <;>
        simp [t, SSet.stdSimplex.triangle] <;> omega
    have hnot : ¬ IsStandardTypeADistinguishedTriangle i t := by
      intro hdist
      have hmid := congrArg Fin.val hdist.1
      have hright := hdist.2.2
      change 1 = i.val at hmid
      change i.val + 1 = m + 1 at hright
      omega
    refine ⟨{
      triangle := t
      nonthin :=
        standardTypeA_not_thin_of_nondegenerate_of_not_distinguished
          i t hnd hnot
      containsAdjacent := ?_ }⟩
    left
    constructor <;> rfl
  · have hkval_ne : k.val ≠ 0 := by
      intro hkval
      apply hk0
      apply Fin.ext
      simpa using hkval
    have hkpos : 0 < k.val := Nat.pos_of_ne_zero hkval_ne
    by_cases hspecial : k.val = 1 ∧ i.val = 1
    · let t : (Δ[m + 1] : SSet.{u}).obj (op ⦋2⦌) :=
        SSet.stdSimplex.triangle
          k.castSucc k.succ (Fin.last (m + 1))
          (by omega) (by
            change k.val + 1 ≤ m + 1
            omega)
      have hnd : t ∈ (Δ[m + 1] : SSet.{u}).nonDegenerate 2 := by
        rw [SSet.stdSimplex.mem_nonDegenerate_iff_strictMono,
          Fin.strictMono_iff_lt_succ]
        intro a
        fin_cases a
        · change k.val < k.val + 1
          omega
        · change k.val + 1 < m + 1
          omega
      have hnot : ¬ IsStandardTypeADistinguishedTriangle i t := by
        intro hdist
        have hmid := congrArg Fin.val hdist.1
        change k.val + 1 = i.val at hmid
        omega
      refine ⟨{
        triangle := t
        nonthin :=
          standardTypeA_not_thin_of_nondegenerate_of_not_distinguished
            i t hnd hnot
        containsAdjacent := ?_ }⟩
      left
      constructor <;> rfl
    · let t : (Δ[m + 1] : SSet.{u}).obj (op ⦋2⦌) :=
        SSet.stdSimplex.triangle
          (0 : Fin (m + 2)) k.castSucc k.succ
          (by
            change 0 ≤ k.val
            omega)
          (by omega)
      have hnd : t ∈ (Δ[m + 1] : SSet.{u}).nonDegenerate 2 := by
        rw [SSet.stdSimplex.mem_nonDegenerate_iff_strictMono,
          Fin.strictMono_iff_lt_succ]
        intro a
        fin_cases a
        · change 0 < k.val
          exact hkpos
        · change k.val < k.val + 1
          omega
      have hnot : ¬ IsStandardTypeADistinguishedTriangle i t := by
        intro hdist
        apply hspecial
        have hmid := congrArg Fin.val hdist.1
        have hleft := hdist.2.1
        change k.val = i.val at hmid
        change 0 + 1 = i.val at hleft
        constructor <;> omega
      refine ⟨{
        triangle := t
        nonthin :=
          standardTypeA_not_thin_of_nondegenerate_of_not_distinguished
            i t hnd hnot
        containsAdjacent := ?_ }⟩
      right
      constructor <;> rfl

/-! ## The first coordinate of an arbitrary lower-cylinder section -/

/-- The first coordinate of an arbitrary simplicial map from the
`(m+1)`-simplex into the lower cylinder, read on its top simplex via Yoneda. -/
def typeAHigherLowerCylinderSectionFirstCoordinate
    (m : Nat)
    (i : Fin (m + 2))
    {sΔ : ScaledSimplicialSet (Δ[m] : SSet.{u})}
    (s : scaledSimplex (standardTypeASimplexScaling i) ⟶
      scaledSimplexCylinder sΔ) :
    Fin (m + 2) →o Fin (m + 1) :=
  SSet.stdSimplex.asOrderHom (SSet.yonedaEquiv s.map).1

/-- Evaluation of the represented first coordinate on any lower-dimensional
simplex is pointwise evaluation of the top first-coordinate simplex. -/
@[simp]
theorem typeAHigherLowerCylinderSectionFirstCoordinate_apply
    (m : Nat)
    (i : Fin (m + 2))
    {sΔ : ScaledSimplicialSet (Δ[m] : SSet.{u})}
    (s : scaledSimplex (standardTypeASimplexScaling i) ⟶
      scaledSimplexCylinder sΔ)
    {d : Nat}
    (t : (Δ[m + 1] : SSet.{u}).obj (op ⦋d⦌))
    (a : Fin (d + 1)) :
    ((s.map.app (op ⦋d⦌) t).1) a =
      typeAHigherLowerCylinderSectionFirstCoordinate m i s (t a) := by
  change
    ((s.map.app (op ⦋d⦌) t).1) a =
      (SSet.yonedaEquiv s.map).1 (t a)
  have hs :
      SSet.yonedaEquiv.symm (SSet.yonedaEquiv s.map) = s.map :=
    (SSet.yonedaEquiv
      (X := ((Δ[m] : SSet.{u}) ⊗ Δ[1]))
      (n := ⦋m + 1⦌)).symm_apply_apply s.map
  rw [← hs]
  rfl

/-- The first coordinate cannot be injective: its finite domain has one more
vertex than its codomain. -/
theorem typeAHigherLowerCylinderSectionFirstCoordinate_not_injective
    (m : Nat)
    (i : Fin (m + 2))
    {sΔ : ScaledSimplicialSet (Δ[m] : SSet.{u})}
    (s : scaledSimplex (standardTypeASimplexScaling i) ⟶
      scaledSimplexCylinder sΔ) :
    ¬ Function.Injective
      (typeAHigherLowerCylinderSectionFirstCoordinate m i s) := by
  intro hinj
  have hcard := Fintype.card_le_of_injective _ hinj
  simp only [Fintype.card_fin] at hcard
  omega

/-- Monotonicity plus non-injectivity forces one adjacent pair to be
identified by the first coordinate. -/
theorem typeAHigherLowerCylinderSectionFirstCoordinate_exists_adjacent_eq
    (m : Nat)
    (i : Fin (m + 2))
    {sΔ : ScaledSimplicialSet (Δ[m] : SSet.{u})}
    (s : scaledSimplex (standardTypeASimplexScaling i) ⟶
      scaledSimplexCylinder sΔ) :
    ∃ k : Fin (m + 1),
      typeAHigherLowerCylinderSectionFirstCoordinate m i s k.castSucc =
        typeAHigherLowerCylinderSectionFirstCoordinate m i s k.succ := by
  have hnot :=
    typeAHigherLowerCylinderSectionFirstCoordinate_not_injective m i s
  rw [Fin.orderHom_injective_iff] at hnot
  push_neg at hnot
  exact hnot

/-! ## The adjacent-collapse witness is forced thin in the cylinder -/

/-- If the first-coordinate section collapses the adjacent edge carried by a
witness triangle, the image triangle is thin in the lower cylinder. -/
theorem typeAHigherLowerCylinderSection_witness_image_thin
    (m : Nat)
    (i : Fin (m + 2))
    {sΔ : ScaledSimplicialSet (Δ[m] : SSet.{u})}
    (s : scaledSimplex (standardTypeASimplexScaling i) ⟶
      scaledSimplexCylinder sΔ)
    (k : Fin (m + 1))
    (hk :
      typeAHigherLowerCylinderSectionFirstCoordinate m i s k.castSucc =
        typeAHigherLowerCylinderSectionFirstCoordinate m i s k.succ)
    (W : TypeAAdjacentNonthinWitness.{u} m i k) :
    (simplexCylinderScaling sΔ).thin
      (s.map.app (op ⦋2⦌) W.triangle) := by
  change sΔ.thin (s.map.app (op ⦋2⦌) W.triangle).1
  rcases W.containsAdjacent with hfirst | hsecond
  · apply arbitraryScaling_thin_of_zero_eq_one sΔ
    rw [typeAHigherLowerCylinderSectionFirstCoordinate_apply,
      typeAHigherLowerCylinderSectionFirstCoordinate_apply,
      hfirst.1, hfirst.2]
    exact hk
  · apply arbitraryScaling_thin_of_one_eq_two sΔ
    rw [typeAHigherLowerCylinderSectionFirstCoordinate_apply,
      typeAHigherLowerCylinderSectionFirstCoordinate_apply,
      hsecond.1, hsecond.2]
    exact hk

/-! ## Generic obstruction to a one-cell target retract -/

/-- In every type-(A) dimension at least three, no choice of scaling on the
one-dimension-lower simplex admits a scaled split

`Delta[m+1] -> Delta[m] x Delta[1] -> Delta[m+1]`.

This is independent of the source half of any proposed arrow retract. -/
theorem typeAHigher_no_oneLowerCylinderTargetRetract
    (m : Nat)
    (hm : 2 ≤ m)
    (i : Fin (m + 2))
    (hi0 : 0 < i)
    (hilast : i < Fin.last (m + 1)) :
    ¬ ∃ (sΔ : ScaledSimplicialSet (Δ[m] : SSet.{u}))
        (s : scaledSimplex (standardTypeASimplexScaling i) ⟶
          scaledSimplexCylinder sΔ)
        (r : scaledSimplexCylinder sΔ ⟶
          scaledSimplex (standardTypeASimplexScaling i)),
        s ≫ r = 𝟙 _ := by
  rintro ⟨sΔ, s, r, hretract⟩
  obtain ⟨k, hk⟩ :=
    typeAHigherLowerCylinderSectionFirstCoordinate_exists_adjacent_eq m i s
  obtain ⟨W⟩ := typeAAdjacentNonthinWitness_exists m hm i hi0 hilast k
  have hcyl :
      (simplexCylinderScaling sΔ).thin
        (s.map.app (op ⦋2⦌) W.triangle) :=
    typeAHigherLowerCylinderSection_witness_image_thin m i s k hk W
  have htarget := r.scaled _ hcyl
  have hback :
      r.map.app (op ⦋2⦌)
          (s.map.app (op ⦋2⦌) W.triangle) =
        W.triangle := by
    have h := congrArg
      (fun f :
        scaledSimplex (standardTypeASimplexScaling i) ⟶
          scaledSimplex (standardTypeASimplexScaling i) =>
        f.map.app (op ⦋2⦌) W.triangle)
      hretract
    simpa using h
  rw [hback] at htarget
  exact W.nonthin htarget

/-- The first unresolved degree `3` is the specialization `m = 2`; hence
v1.111's addition obstruction is a shadow of a map-independent theorem. -/
theorem typeAThree_no_arbitraryOneLowerCylinderTargetRetract
    (i : Fin 4)
    (hi0 : 0 < i)
    (hilast : i < Fin.last 3) :
    ¬ ∃ (sΔ : ScaledSimplicialSet (Δ[2] : SSet.{u}))
        (s : scaledSimplex (standardTypeASimplexScaling i) ⟶
          scaledSimplexCylinder sΔ)
        (r : scaledSimplexCylinder sΔ ⟶
          scaledSimplex (standardTypeASimplexScaling i)),
        s ≫ r = 𝟙 _ := by
  exact typeAHigher_no_oneLowerCylinderTargetRetract 2 (by decide) i hi0 hilast

/-!
The one-cell branch is now completely closed:

```text
type-A dimension 2:
  one lower canonical cylinder can work (v1.110)

type-A dimension >= 3:
  every map into one lower cylinder collapses an adjacent edge
  -> a non-thin triangle through that edge becomes cylinder-thin
  -> no scaled target retraction can split the map.
```

Therefore higher reverse comparison should not spend further effort on a
single lower-cylinder arrow retract.  The next positive candidate is a
multi-cell local-prism construction: individual cells may collapse different
edges, while the rank filtration controls which thin triangles are exposed at
each stage.  A logically independent retained alternative is to search for a
canonical-right map failing a standard higher type-(A) lifting property.
-/

end KUOS.DependentOriginationCanonicalTypeAHigherLowerCylinderRetractObstructionV1_112
