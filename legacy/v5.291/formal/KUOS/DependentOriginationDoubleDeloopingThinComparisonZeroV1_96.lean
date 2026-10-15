import KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95

namespace KUOS.DependentOriginationDoubleDeloopingThinComparisonZeroV1_96

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Bicategory
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58
open KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95

/-!
# Thin triangles in the additive double delooping v1.96

Version v1.95 constructed the strict bicategory `B^2 N` and a Duskin
2-simplex whose genuine comparison 2-cell is `1`.  The only remaining local
question before standard A/B/C fibrancy was whether that displayed simplex
could nevertheless be one of the two simplicial degeneracies explicitly
included in the global Duskin scaling.

This file removes that ambiguity uniformly.  In the additive hom-category
`Nat`, a 2-cell is invertible exactly when it is zero.  Every 2-cell obtained
by mapping a 2-cell of a locally discrete ordinal is zero, and every
composition comparison of a Duskin 1-simplex is zero because a composable
pair in `[1]` contains an identity arrow.  Consequently every degenerate
Duskin 2-simplex has comparison zero.

For every Duskin 2-simplex of `B^2 N` we therefore obtain the exact arithmetic
characterization

```text
thin sigma <-> duskinComparison sigma = 0.
```

In particular the comparison-`1` simplex of v1.95 is unconditionally
nondegenerate and non-thin.  The separation certificate is thereby reduced
from two fields to one: standard A/B/C terminal right lifting for the concrete
scaled Duskin nerve.
-/

namespace NatDoubleDelooping

/-- A natural-number 2-cell in the additive double delooping is invertible
exactly when it is zero. -/
theorem twoCell_isIso_iff_eq_zero
    {f g : NatOneCell} (alpha : f ⟶ g) :
    IsIso alpha ↔ alpha = 0 := by
  constructor
  · intro h
    letI : IsIso alpha := h
    have hinv := IsIso.hom_inv_id alpha
    change alpha + inv alpha = 0 at hinv
    omega
  · intro h
    have hfg : f = g := Subsingleton.elim _ _
    subst g
    rw [h]
    change IsIso (𝟙 f)
    infer_instance

/-- Any invertible 2-cell in the additive double delooping is literally zero. -/
theorem isIso_twoCell_eq_zero
    {f g : NatOneCell} (alpha : f ⟶ g) [IsIso alpha] :
    alpha = 0 :=
  (twoCell_isIso_iff_eq_zero alpha).1 inferInstance

end NatDoubleDelooping

/-! ## Locally discrete 2-cells map to zero -/

/-- The source ordinal is locally discrete, so every source 2-cell is an
identity after identifying its endpoints.  Any Duskin simplex into `B^2 N`
therefore sends every source 2-cell to the additive identity `0`. -/
theorem natDuskin_map₂_eq_zero
    {n : Nat}
    (sigma : DuskinSimplex NatDoubleDelooping n)
    {a b : DuskinOrdinal n} {f g : a ⟶ b}
    (eta : f ⟶ g) :
    sigma.map₂ eta = 0 := by
  have hfg : f = g := LocallyDiscrete.eq_of_hom eta
  subst g
  have heta : eta = 𝟙 f := Subsingleton.elim _ _
  rw [heta, sigma.map₂_id]
  rfl

/-! ## Normality forces identity comparisons to zero -/

/-- The comparison with an identity on the left is zero. -/
theorem natDuskin_mapComp_id_left_eq_zero
    {n : Nat}
    (sigma : DuskinSimplex NatDoubleDelooping n)
    {a b : DuskinOrdinal n} (g : a ⟶ b) :
    sigma.mapComp (𝟙 a) g = 0 := by
  have h := sigma.map₂_leftUnitor g
  have hmap₂ : sigma.map₂ (λ_ g).inv = 0 :=
    natDuskin_map₂_eq_zero sigma _
  have hλ : (λ_ (sigma.map g)).inv = 0 :=
    NatDoubleDelooping.isIso_twoCell_eq_zero _
  have heq : eqToHom (by rw [sigma.map_id a]) =
      (0 : (sigma.map (𝟙 a)) ⟶ 𝟙 (sigma.obj a)) :=
    NatDoubleDelooping.isIso_twoCell_eq_zero _
  rw [hmap₂, hλ, heq] at h
  simpa using h.symm

/-- The comparison with an identity on the right is zero. -/
theorem natDuskin_mapComp_id_right_eq_zero
    {n : Nat}
    (sigma : DuskinSimplex NatDoubleDelooping n)
    {a b : DuskinOrdinal n} (f : a ⟶ b) :
    sigma.mapComp f (𝟙 b) = 0 := by
  have h := sigma.map₂_rightUnitor f
  have hmap₂ : sigma.map₂ (ρ_ f).inv = 0 :=
    natDuskin_map₂_eq_zero sigma _
  have hρ : (ρ_ (sigma.map f)).inv = 0 :=
    NatDoubleDelooping.isIso_twoCell_eq_zero _
  have heq : eqToHom (by rw [sigma.map_id b]) =
      (0 : (sigma.map (𝟙 b)) ⟶ 𝟙 (sigma.obj b)) :=
    NatDoubleDelooping.isIso_twoCell_eq_zero _
  rw [hmap₂, hρ, heq] at h
  simpa using h.symm

/-! ## Every comparison in degree one is zero -/

/-- In `[1]`, a composable pair cannot contain two strict increases.  Hence at
least one arrow is an identity, and normality forces every comparison of a
Duskin 1-simplex to be zero. -/
theorem natOneSimplex_mapComp_eq_zero
    (sigma : DuskinSimplex NatDoubleDelooping 1)
    {a b c : DuskinOrdinal 1}
    (f : a ⟶ b) (g : b ⟶ c) :
    sigma.mapComp f g = 0 := by
  have hab : a.as ≤ b.as := f.as.le
  have hbc : b.as ≤ c.as := g.as.le
  have heq : a.as = b.as ∨ b.as = c.as := by
    by_cases h : a.as = b.as
    · exact Or.inl h
    · right
      apply Fin.ext
      have hne : a.as.val ≠ b.as.val := by
        intro hv
        apply h
        exact Fin.ext hv
      have ha := a.as.isLt
      have hb := b.as.isLt
      have hc := c.as.isLt
      omega
  rcases heq with habEq | hbcEq
  · have habObj : a = b := LocallyDiscrete.ext habEq
    subst b
    have hf : f = 𝟙 a := Subsingleton.elim _ _
    rw [hf]
    exact natDuskin_mapComp_id_left_eq_zero sigma g
  · have hbcObj : b = c := LocallyDiscrete.ext hbcEq
    subst c
    have hg : g = 𝟙 b := Subsingleton.elim _ _
    rw [hg]
    exact natDuskin_mapComp_id_right_eq_zero sigma f

/-! ## Degeneracies have zero comparison -/

/-- Either simplicial degeneracy of a Duskin 1-simplex has comparison zero.
The reindexing contribution is also sent to zero because its source is locally
discrete. -/
theorem natDegeneracy_comparison_eq_zero
    (e : DuskinSimplex NatDoubleDelooping 1)
    (i : Fin 2) :
    duskinComparison ((duskinNerve NatDoubleDelooping).σ i e) = 0 := by
  change
    (((duskinReindex (SimplexCategory.σ i).op).comp e).mapComp
      edge01 edge12) = 0
  change
    (e.mapComp
        ((duskinReindex (SimplexCategory.σ i).op).map edge01)
        ((duskinReindex (SimplexCategory.σ i).op).map edge12) ≫
      e.map₂
        ((duskinReindex (SimplexCategory.σ i).op).mapComp edge01 edge12)) = 0
  rw [natOneSimplex_mapComp_eq_zero, natDuskin_map₂_eq_zero]
  rfl

/-- Every degenerate Duskin 2-simplex in `B^2 N` has zero comparison. -/
theorem natDegenerate_comparison_eq_zero
    (sigma : DuskinSimplex NatDoubleDelooping 2)
    (hdeg : IsDegenerateDuskinTwoSimplex sigma) :
    duskinComparison sigma = 0 := by
  rcases hdeg with ⟨e, rfl⟩ | ⟨e, rfl⟩
  · exact natDegeneracy_comparison_eq_zero e 0
  · exact natDegeneracy_comparison_eq_zero e 1

/-! ## Exact thinness characterization -/

/-- In the additive double delooping, the global Duskin scaling is exactly the
zero locus of the comparison label. -/
theorem natDuskin_thin_iff_comparison_eq_zero
    (sigma : DuskinSimplex NatDoubleDelooping 2) :
    (duskinScaling NatDoubleDelooping).thin sigma ↔
      duskinComparison sigma = 0 := by
  change
    (IsIso (duskinComparison sigma) ∨
      IsDegenerateDuskinTwoSimplex sigma) ↔
      duskinComparison sigma = 0
  constructor
  · intro h
    rcases h with hIso | hdeg
    · exact
        (NatDoubleDelooping.twoCell_isIso_iff_eq_zero
          (duskinComparison sigma)).1 hIso
    · exact natDegenerate_comparison_eq_zero sigma hdeg
  · intro hzero
    exact Or.inl
      ((NatDoubleDelooping.twoCell_isIso_iff_eq_zero
        (duskinComparison sigma)).2 hzero)

/-- The comparison-`1` simplex of v1.95 is therefore nondegenerate without any
additional simplicial hypothesis. -/
theorem natNoninvertibleTriangle_nondegenerate :
    ¬ IsDegenerateDuskinTwoSimplex natNoninvertibleTriangle := by
  intro hdeg
  have hzero := natDegenerate_comparison_eq_zero
    natNoninvertibleTriangle hdeg
  rw [natNoninvertibleTriangle_comparison] at hzero
  omega

/-- The same simplex is unconditionally non-thin. -/
theorem natNoninvertibleTriangle_not_thin :
    ¬ (duskinScaling NatDoubleDelooping).thin natNoninvertibleTriangle := by
  rw [natDuskin_thin_iff_comparison_eq_zero,
    natNoninvertibleTriangle_comparison]
  omega

/-! ## The separator certificate now has one field -/

/-- After the local arithmetic theorem above, the only remaining obligation for
strict standard/canonical separation is standard A/B/C terminal right lifting
of the concrete scaled Duskin nerve. -/
structure NatDoubleDeloopingStandardRightCertificate : Prop where
  standardRight :
    (standardGeneratedScaledAnodyneABC : MorphismProperty ScaledSSet).rlp
      (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin)

/-- The one-field certificate supplies the v1.95 two-field interface. -/
def NatDoubleDeloopingStandardRightCertificate.toSeparatorCertificate
    (C : NatDoubleDeloopingStandardRightCertificate) :
    NatDoubleDeloopingStandardSeparatorCertificate where
  nondegenerate := natNoninvertibleTriangle_nondegenerate
  standardRight := C.standardRight

/-- A standard-right certificate makes the terminal map fail thinness
reflection. -/
theorem terminal_not_reflects_of_standardRightCertificate
    (C : NatDoubleDeloopingStandardRightCertificate) :
    ¬ KUOS.DependentOriginationCanonicalFibrationThinReflectionV1_92.ReflectsThinTwoSimplices
      (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin) :=
  certificate_terminal_not_reflects C.toSeparatorCertificate

/-- The pure-scaling waypoint is open as soon as standard A/B/C terminal
right lifting is established for this concrete model. -/
theorem not_standardArbitraryScalingObstructionClosed_of_standardRightCertificate
    (C : NatDoubleDeloopingStandardRightCertificate) :
    ¬ KUOS.DependentOriginationStandardArbitraryScalingWaypointV1_89.StandardArbitraryScalingObstructionClosed :=
  not_standardArbitraryScalingObstructionClosed_of_certificate
    C.toSeparatorCertificate

/-- Likewise the forward presentation order `canonical <= standard` fails from
the same single standard-right theorem. -/
theorem not_canonicalKuuOS_le_standardABC_of_standardRightCertificate
    (C : NatDoubleDeloopingStandardRightCertificate) :
    ¬ KUOS.DependentOriginationGeneratedPresentationPosetalReflectionV1_83.canonicalKuuOSPresentation ≤
      KUOS.DependentOriginationGeneratedPresentationPosetalReflectionV1_83.standardABCPresentation :=
  not_canonicalKuuOS_le_standardABC_of_certificate
    C.toSeparatorCertificate

/-!
The remaining separation frontier is now a single concrete theorem:

```text
(standardGeneratedScaledAnodyneABC).rlp
  (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin).
```

There is no longer a separate nondegeneracy obligation.  The next unit can
therefore focus entirely on the standard A/B/C lifting arithmetic of
`B^2 N`.
-/

end KUOS.DependentOriginationDoubleDeloopingThinComparisonZeroV1_96
